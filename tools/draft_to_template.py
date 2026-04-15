"""
📥 Draft to Template Converter
Chuyển đổi CapCut draft hiện tại thành template JSON để tái sử dụng/chia sẻ
"""

import json
import shutil
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import zipfile
from datetime import datetime

class DraftToTemplateConverter:
    """
    Convert CapCut/Jianying draft sang template JSON
    
    Workflow:
    1. Load existing draft (từ folder CapCut)
    2. Extract metadata (canvas, tracks, elements)
    3. Replace content URLs with "slots"
    4. Export thành template JSON
    """
    
    def __init__(self, draft_path: str):
        """
        Initialize converter
        
        Args:
            draft_path: Đường dẫn tới draft folder hoặc zip file
        """
        self.draft_path = draft_path
        self.draft_folder = None
        self.metadata = {}
        self.draft_info = {}
        
        print(f"📂 Loading draft: {draft_path}")
        
        # Check if it's a folder or zip
        if zipfile.is_zipfile(draft_path):
            self._load_from_zip(draft_path)
        elif os.path.isdir(draft_path):
            self._load_from_folder(draft_path)
        else:
            raise FileNotFoundError(f"Draft not found: {draft_path}")
        
        print(f"✅ Draft loaded")
    
    def _load_from_folder(self, folder_path: str):
        """Load draft từ folder"""
        self.draft_folder = folder_path
        
        # Load draft_info.json
        draft_info_path = os.path.join(folder_path, "draft_info.json")
        if os.path.exists(draft_info_path):
            with open(draft_info_path, encoding='utf-8') as f:
                self.draft_info = json.load(f)
        
        # Load draft_meta_info.json
        meta_path = os.path.join(folder_path, "draft_meta_info.json")
        if os.path.exists(meta_path):
            with open(meta_path, encoding='utf-8') as f:
                self.metadata = json.load(f)
    
    def _load_from_zip(self, zip_path: str):
        """Load draft từ zip file"""
        # Extract to temp folder
        temp_folder = f"temp_draft_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)
        
        self.draft_folder = temp_folder
        self._load_from_folder(temp_folder)
    
    def _extract_canvas_config(self) -> Dict[str, Any]:
        """Extract canvas config từ draft"""
        canvas_config = self.draft_info.get("canvas_config", {})
        
        return {
            "width": canvas_config.get("width", 1280),
            "height": canvas_config.get("height", 720)
        }
    
    def _extract_tracks(self) -> Dict[str, Any]:
        """
        Extract tracks từ draft
        
        Ở đây chúng ta extract cấu trúc track, không lấy content URLs
        """
        tracks = self.draft_info.get("tracks", [])
        
        track_config = {}
        
        for track in tracks:
            track_type = track.get("type", "unknown")
            track_name = track.get("name", f"{track_type}_main")
            
            # Extract segments (elements)
            segments = track.get("segments", [])
            
            # Accumulate timeline info
            if track_type not in ["audio", "effect", "text", "sticker"]:
                # Video/Image track
                if "video" not in track_config:
                    track_config["video"] = {
                        "type": "video",
                        "elements": []
                    }
                
                for segment in segments:
                    # Extract để lấy animation info
                    keyframes = segment.get("keyframes", [])
                    
                    if keyframes:
                        for kf in keyframes:
                            track_config["video"]["elements"].append({
                                "type": "image",  # Assume image
                                "keyframes": [
                                    {
                                        "type": kf.get("type", "animation"),
                                        "property_type": kf.get("property_type", "scale_x"),
                                        "at_start": str(kf.get("at_start", "1.0")),
                                        "at_end": str(kf.get("at_end", "1.0"))
                                    }
                                ]
                            })
        
        # Default tracks if empty
        if not track_config:
            track_config = {
                "video": {
                    "type": "video",
                    "elements": [
                        {
                            "type": "image",
                            "keyframes": [
                                {
                                    "type": "zoom",
                                    "property_type": "scale_x",
                                    "at_start": "1.0",
                                    "at_end": "1.25"
                                },
                                {
                                    "type": "zoom",
                                    "property_type": "scale_y",
                                    "at_start": "1.0",
                                    "at_end": "1.25"
                                }
                            ]
                        }
                    ]
                }
            }
        
        return track_config
    
    def _extract_transitions(self) -> Dict[str, Any]:
        """Extract transition settings"""
        # Lấy từ segments
        segments = []
        for track in self.draft_info.get("tracks", []):
            segments.extend(track.get("segments", []))
        
        # Try to detect transition type
        transition_type = "Dissolve"  # Default
        transition_duration = 0.5
        
        for segment in segments:
            if "transition" in segment:
                trans = segment.get("transition", {})
                transition_type = trans.get("type", "Dissolve")
                transition_duration = trans.get("duration", 0.5)
                break
        
        return {
            "type": transition_type,
            "duration": transition_duration
        }
    
    def _count_content_items(self) -> int:
        """Đếm số lượng content items (images/videos)"""
        count = 0
        for track in self.draft_info.get("tracks", []):
            for segment in track.get("segments", []):
                if "path" in segment or "url" in segment:
                    count += 1
        
        return count
    
    def _extract_duration(self) -> float:
        """Extract thời lượng mỗi segment"""
        # Get từ draft
        duration_per_item = 3.0  # Default
        
        segments = []
        for track in self.draft_info.get("tracks", []):
            segments.extend(track.get("segments", []))
        
        if segments:
            # Calculate average duration
            total_duration = 0
            for segment in segments:
                duration = segment.get("duration", 0)
                if duration:
                    total_duration += duration
            
            if total_duration and len(segments):
                duration_per_item = total_duration / len(segments)
        
        return round(duration_per_item, 1)
    
    def to_template(self, template_name: str, num_slots: int = None) -> Dict[str, Any]:
        """
        Convert draft thành template
        
        Args:
            template_name: Tên template
            num_slots: Số lượng slots (nếu None, tính từ draft)
        
        Returns:
            Template dictionary
        """
        # Infer number of slots
        if num_slots is None:
            num_slots = max(self._count_content_items(), 3)
        
        template = {
            "name": template_name,
            "version": "1.0.0",
            "description": f"Template extracted from draft at {datetime.now().isoformat()}",
            "settings": {
                "canvas": self._extract_canvas_config(),
                "duration_per_slide": self._extract_duration(),
                "transition": self._extract_transitions()
            },
            "tracks": self._extract_tracks(),
            "slots": {
                f"image_{i}": {"type": "image", "required": True}
                for i in range(num_slots)
            }
        }
        
        return template
    
    def save_template(self, output_path: str, template_name: str, num_slots: int = None):
        """
        Lưu template thành JSON file
        
        Args:
            output_path: Đường dẫn output (thư mục hoặc file)
            template_name: Tên template
            num_slots: Số slots
        """
        template = self.to_template(template_name, num_slots)
        
        # Determine output file
        if os.path.isdir(output_path):
            output_file = os.path.join(output_path, f"{template_name}.json")
        else:
            output_file = output_path
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Template exported: {output_file}")
        
        return output_file
    
    def print_summary(self):
        """In tóm tắt draft"""
        canvas = self.draft_info.get("canvas_config", {})
        
        print("\n" + "="*70)
        print("📊 DRAFT SUMMARY")
        print("="*70)
        
        print(f"\n📺 Canvas:")
        print(f"   Size: {canvas.get('width')} × {canvas.get('height')}")
        print(f"   FPS: {self.draft_info.get('fps', 30)}")
        
        print(f"\n📽️  Tracks:")
        for track in self.draft_info.get("tracks", []):
            track_type = track.get("type")
            track_name = track.get("name")
            num_segments = len(track.get("segments", []))
            print(f"   • {track_type} - {track_name} ({num_segments} segments)")
        
        print(f"\n📦 Content:")
        content_count = self._count_content_items()
        duration = self._extract_duration()
        print(f"   Items: {content_count}")
        print(f"   Avg duration/item: {duration}s")
        
        print(f"\n🎬 Transition:")
        trans = self._extract_transitions()
        print(f"   Type: {trans['type']}")
        print(f"   Duration: {trans['duration']}s")
        
        print("\n" + "="*70)
    
    def cleanup(self):
        """Cleanup temp files"""
        if self.draft_folder and "temp_draft_" in self.draft_folder:
            shutil.rmtree(self.draft_folder)
            print(f"✅ Cleaned up temp files: {self.draft_folder}")


# ============================================================================
# Workflow: From Draft to Template
# ============================================================================

def draft_to_template_workflow(draft_path: str, template_name: str, num_slots: int = None):
    """
    Complete workflow: Draft → Template
    
    Steps:
    1. Load draft
    2. Extract metadata
    3. Preview extracted settings
    4. Export template
    5. Test template
    """
    print("\n" + "="*70)
    print("🔄 DRAFT TO TEMPLATE WORKFLOW")
    print("="*70)
    
    try:
        # Step 1: Load
        print(f"\n1️⃣  Loading draft...")
        converter = DraftToTemplateConverter(draft_path)
        
        # Step 2: Preview
        print(f"\n2️⃣  Analyzing draft...")
        converter.print_summary()
        
        # Step 3: Ask user
        if num_slots is None:
            default_slots = max(converter._count_content_items(), 3)
            user_input = input(f"\nNumber of slots? (default: {default_slots}): ").strip()
            num_slots = int(user_input) if user_input else default_slots
        
        # Step 4: Convert
        print(f"\n3️⃣  Converting to template...")
        template = converter.to_template(template_name, num_slots)
        print(f"   ✅ Converted: {template_name}")
        print(f"   Canvas: {template['settings']['canvas']}")
        print(f"   Slots: {len(template['slots'])}")
        
        # Step 5: Export
        print(f"\n4️⃣  Exporting template...")
        output_path = converter.save_template("template", template_name, num_slots)
        
        # Step 6: Summary
        print(f"\n✨ Template created successfully!")
        print(f"   File: {output_path}")
        print(f"\n📋 Next steps:")
        print(f"   1. Edit template file to fine-tune settings")
        print(f"   2. Preview: python template_preview.py {output_path}")
        print(f"   3. Test render with TemplateProcessor")
        print(f"   4. Share or reuse template")
        
        # Cleanup
        converter.cleanup()
        
        return output_path
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


# ============================================================================
# Helpers
# ============================================================================

def list_capcut_drafts(capcut_folder: str) -> List[Dict[str, str]]:
    """
    List tất cả CapCut drafts có sẵn trong máy
    
    Returns: [{"name": "draft_name", "path": "/path/to/draft"}, ...]
    """
    drafts = []
    
    draft_path = os.path.expanduser(capcut_folder)
    if not os.path.exists(draft_path):
        return drafts
    
    for item in os.listdir(draft_path):
        full_path = os.path.join(draft_path, item)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "draft_info.json")):
            drafts.append({
                "name": item,
                "path": full_path
            })
    
    return drafts


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Mode 1: Convert specific draft
        if sys.argv[1] == "--draft":
            draft_path = sys.argv[2]
            template_name = sys.argv[3] if len(sys.argv) > 3 else "extracted-template"
            num_slots = int(sys.argv[4]) if len(sys.argv) > 4 else None
            
            draft_to_template_workflow(draft_path, template_name, num_slots)
        
        # Mode 2: List available drafts
        elif sys.argv[1] == "--list":
            # For Windows
            capcut_folder = os.path.expanduser("~/AppData/Local/CapCut/drafts")
            # For macOS
            if not os.path.exists(capcut_folder):
                capcut_folder = os.path.expanduser("~/Movies/CapCut/Draft")
            # For Linux (Jianying)
            if not os.path.exists(capcut_folder):
                capcut_folder = os.path.expanduser("~/.local/share/jianying")
            
            drafts = list_capcut_drafts(capcut_folder)
            
            if drafts:
                print(f"\n📂 Available drafts in {capcut_folder}:")
                for i, draft in enumerate(drafts, 1):
                    print(f"   {i}. {draft['name']}")
                    print(f"      Path: {draft['path']}")
            else:
                print(f"❌ No drafts found in {capcut_folder}")
    
    else:
        # Demo mode
        print("""
🔄 Draft to Template Converter

Usage:
  python draft_to_template.py --list
    → List all available drafts

  python draft_to_template.py --draft <draft_path> <template_name> [num_slots]
    → Convert specific draft to template
    
Example:
  python draft_to_template.py --draft "C:\\Path\\To\\Draft" my-slideshow 5
        """)
