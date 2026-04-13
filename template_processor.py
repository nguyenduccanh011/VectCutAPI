"""
Template Processor - Xử lý JSON template và render video
Sử dụng để tách biệt layout (template) và nội dung (content)
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class TemplateProcessor:
    """Process JSON template và render sang MCP calls"""
    
    def __init__(self, template_path: str):
        """Load JSON template"""
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, encoding='utf-8') as f:
            self.template = json.load(f)
        
        self.name = self.template.get("name", "unknown")
        self.config = self.template.get("settings", {})
        self.tracks = self.template.get("tracks", {})
        self.slots = self.template.get("slots", {})
        
        print(f"✅ Loaded template: {self.name}")
    
    def validate_content_map(self, content_map: Dict[str, Any]) -> bool:
        """Kiểm tra content_map có đặy đủ required slots không"""
        required_slots = [k for k, v in self.slots.items() if v.get("required", True)]
        
        for slot in required_slots:
            if slot not in content_map or not content_map[slot]:
                print(f"❌ Missing required content for slot: {slot}")
                return False
        
        return True
    
    def get_element_template(self, track_name: str, element_type: str) -> Optional[Dict]:
        """Lấy template của element trong track"""
        track = self.tracks.get(track_name, {})
        elements = track.get("elements", [])
        
        for elem in elements:
            if elem.get("type") == element_type:
                return elem
        
        return None
    
    def apply_keyframes(self, draft_id: str, track_name: str, 
                       element_template: Dict, clip_start: float, 
                       duration: float) -> None:
        """
        Áp dụng keyframes từ template definition
        """
        # Tránh import circular, import tại function
        from add_video_keyframe_impl import add_video_keyframe_impl
        
        keyframes = element_template.get("keyframes", [])
        
        for kf in keyframes:
            kf_type = kf.get("type")
            property_type = kf.get("property_type")
            at_start = kf.get("at_start")
            at_end = kf.get("at_end")
            
            if not property_type or not at_start or not at_end:
                continue
            
            # Keyframe đầu (offset +0.01 để tránh boundary)
            add_video_keyframe_impl(
                draft_id=draft_id,
                track_name=track_name,
                property_type=property_type,
                time=clip_start + 0.01,
                value=at_start
            )
            
            # Keyframe cuối (offset -0.01 để tránh boundary)
            add_video_keyframe_impl(
                draft_id=draft_id,
                track_name=track_name,
                property_type=property_type,
                time=clip_start + duration - 0.01,
                value=at_end
            )
            
            print(f"    ↳ Applied keyframe: {property_type} ({at_start} → {at_end})")
    
    def render_video_track(self, draft_id: str, track_name: str, 
                          content_map: Dict[str, Any]) -> str:
        """
        Render video track với images/videos
        
        Args:
            draft_id: Draft ID (None = create new)
            track_name: Track name (e.g., "video")
            content_map: {"image_0": "url", "image_1": "url", ...}
        
        Returns:
            updated draft_id
        """
        from add_image_impl import add_image_impl
        
        track = self.tracks.get(track_name, {})
        elements = track.get("elements", [])
        
        if not elements:
            print(f"⚠️  No elements found in track: {track_name}")
            return draft_id
        
        # Lấy config từ template
        canvas = self.config.get("canvas", {"width": 1280, "height": 720})
        duration_per_clip = self.config.get("duration_per_slide", 3.0)
        transition_cfg = self.config.get("transition", {})
        transition_type = transition_cfg.get("type")
        transition_dur = transition_cfg.get("duration", 0.5)
        
        slot_keys = sorted([k for k in self.slots.keys() if k in content_map])
        
        for idx, slot_key in enumerate(slot_keys):
            content_url = content_map[slot_key]
            
            if not content_url:
                print(f"⚠️  Skipping empty slot: {slot_key}")
                continue
            
            clip_start = idx * duration_per_clip
            clip_end = clip_start + duration_per_clip
            
            print(f"\n  [{idx+1}] Adding {slot_key}")
            print(f"      Time: {clip_start:.1f}s → {clip_end:.1f}s")
            
            # Thêm image
            result = add_image_impl(
                image_url=content_url,
                start=clip_start,
                end=clip_end,
                width=canvas.get("width", 1280),
                height=canvas.get("height", 720),
                track_name=track_name,
                draft_id=draft_id,
                transition=transition_type if idx > 0 else None,
                transition_duration=transition_dur,
            )
            
            if not result.get("success"):
                print(f"❌ Failed to add {slot_key}: {result.get('error')}")
                continue
            
            draft_id = result["output"]["draft_id"]
            print(f"      ✓ draft_id: {draft_id}")
            
            # Áp dụng keyframes từ template
            for elem in elements:
                if elem.get("type") == "image":
                    self.apply_keyframes(draft_id, track_name, elem, 
                                        clip_start, duration_per_clip)
        
        return draft_id
    
    def render(self, content_map: Dict[str, Any], 
              draft_folder: str = None) -> Dict[str, Any]:
        """
        Render template với content
        
        Args:
            content_map: {
                "image_0": "https://...",
                "image_1": "https://...",
                ...
            }
            draft_folder: Path to CapCut draft folder
        
        Returns:
            {
                "success": bool,
                "draft_id": str,
                "duration": float,
                "slots_used": int,
                "error": str (if any)
            }
        """
        print(f"\n🎬 Rendering template: {self.name}")
        print(f"📊 Template config: {json.dumps(self.config, indent=2, ensure_ascii=False)}\n")
        
        # Validate
        if not self.validate_content_map(content_map):
            return {
                "success": False,
                "error": "Content map validation failed"
            }
        
        draft_id = None
        
        try:
            # Render each track
            for track_name in self.tracks.keys():
                print(f"\n📹 Processing track: {track_name}")
                draft_id = self.render_video_track(draft_id, track_name, content_map)
            
            # Save
            if draft_folder:
                from save_draft_impl import save_draft_impl
                print(f"\n💾 Saving draft to: {draft_folder}")
                save_result = save_draft_impl(draft_id, draft_folder)
                print(f"    ✓ Saved successfully")
            
            # Calculate duration
            total_slots = len([k for k in self.slots.keys() if k in content_map])
            duration = total_slots * self.config.get("duration_per_slide", 3.0)
            
            return {
                "success": True,
                "draft_id": draft_id,
                "duration": duration,
                "slots_used": total_slots,
                "draft_url": f"https://www.install-ai-guider.top/draft/downloader?draft_id={draft_id}"
            }
        
        except Exception as e:
            print(f"\n❌ Error during rendering: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

# ============================================================================
# Helper: Create default slideshow template
# ============================================================================

def create_default_slideshow_template() -> Dict:
    """
    Tạo template slideshow mặc định
    """
    return {
        "name": "slideshow-basic",
        "version": "1.0.0",
        "description": "Basic slideshow with zoom effects and dissolve transitions",
        "settings": {
            "canvas": {
                "width": 1280,
                "height": 720
            },
            "duration_per_slide": 3.0,
            "transition": {
                "type": "Dissolve",
                "duration": 0.5
            }
        },
        "tracks": {
            "video": {
                "type": "video",
                "elements": [
                    {
                        "type": "image",
                        "description": "Background image with zoom effect",
                        "keyframes": [
                            {
                                "type": "zoom",
                                "property_type": "scale_x",
                                "at_start": "1.0",
                                "at_end": "1.25",
                                "description": "Zoom in X axis"
                            },
                            {
                                "type": "zoom",
                                "property_type": "scale_y",
                                "at_start": "1.0",
                                "at_end": "1.25",
                                "description": "Zoom in Y axis"
                            }
                        ]
                    }
                ]
            }
        },
        "slots": {
            "image_0": {"type": "image", "required": True},
            "image_1": {"type": "image", "required": True},
            "image_2": {"type": "image", "required": True}
        }
    }

def create_template_file(template_name: str, num_slides: int = 3):
    """
    Tiện ích: Tạo template file
    """
    template = create_default_slideshow_template()
    template["name"] = template_name
    
    # Generate slots
    template["slots"] = {f"image_{i}": {"type": "image", "required": True} 
                         for i in range(num_slides)}
    
    filepath = f"template/{template_name}-template.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Template created: {filepath}")
    return filepath

if __name__ == "__main__":
    # 🎯 Example 1: Dùng default template
    print("=" * 60)
    print("Example 1: Using default slideshow template")
    print("=" * 60)
    
    template_dict = create_default_slideshow_template()
    template_path = "template/slideshow-default.json"
    
    # Lưu template
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template_dict, f, indent=2, ensure_ascii=False)
    
    # Load và render
    processor = TemplateProcessor(template_path)
    result = processor.render({
        "image_0": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop",
        "image_1": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720&fit=crop",
        "image_2": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720&fit=crop",
    })
    
    print(f"\n📊 Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 🎯 Example 2: Create custom template
    print("\n" + "=" * 60)
    print("Example 2: Creating custom template")
    print("=" * 60)
    
    create_template_file("my-slideshow", num_slides=5)
