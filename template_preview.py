"""
🎨 Template Preview Tool - Xem trước template trước khi render
Giúp validate template settings (font size, color, speed, etc) trước khi finalize
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

@dataclass
class PreviewConfig:
    """Cấu hình preview"""
    show_timeline: bool = True
    show_keyframes: bool = True
    show_transitions: bool = True
    show_slots: bool = True
    validate_urls: bool = False
    detailed_print: bool = True

class TemplatePreviewTool:
    """Preview template trước khi render để kiểm tra settings"""
    
    def __init__(self, template_path: str):
        """Load template"""
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, encoding='utf-8') as f:
            self.template = json.load(f)
        
        self.template_path = template_path
        self.name = self.template.get("name", "unknown")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Lấy tóm tắt template
        
        Returns: {
            "canvas": {...},
            "duration": 15.0,
            "num_slides": 5,
            "transitions": [...],
            "effects": [...],
            "total_duration_estimate": 20.0
        }
        """
        config = self.template.get("settings", {})
        canvas = config.get("canvas", {})
        slots = self.template.get("slots", {})
        track_cfg = self.template.get("tracks", {})
        
        num_slides = len(slots)
        duration_per_slide = config.get("duration_per_slide", 3.0)
        transition_cfg = config.get("transition", {})
        transition_dur = transition_cfg.get("duration", 0.5)
        
        # Tính total duration
        total_duration = (num_slides * duration_per_slide) + ((num_slides - 1) * transition_dur)
        
        # Extract effects
        effects = []
        for track_name, track in track_cfg.items():
            for elem in track.get("elements", []):
                for kf in elem.get("keyframes", []):
                    effects.append({
                        "type": kf.get("type"),
                        "property": kf.get("property_type"),
                        "start": kf.get("at_start"),
                        "end": kf.get("at_end")
                    })
        
        return {
            "name": self.name,
            "canvas": canvas,
            "num_slides": num_slides,
            "duration_per_slide": duration_per_slide,
            "transition": {
                "type": transition_cfg.get("type"),
                "duration": transition_dur
            },
            "total_duration_estimate": total_duration,
            "effects": effects,
            "effects_count": len(effects)
        }
    
    def print_preview(self, config: PreviewConfig = None):
        """
        In ra preview đầy đủ của template
        """
        if config is None:
            config = PreviewConfig()
        
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print(f"📋 TEMPLATE PREVIEW: {self.name}")
        print("="*70)
        
        # Canvas & Resolution
        print(f"\n📺 Canvas:")
        canvas = summary["canvas"]
        print(f"   Resolution: {canvas.get('width')} × {canvas.get('height')}")
        print(f"   Aspect Ratio: {canvas.get('width') / max(canvas.get('height'), 1):.2f}:1")
        
        # Timing
        print(f"\n⏱️  Timing:")
        print(f"   Duration per slide: {summary['duration_per_slide']}s")
        print(f"   Num slides: {summary['num_slides']}")
        print(f"   Transition type: {summary['transition']['type']}")
        print(f"   Transition duration: {summary['transition']['duration']}s")
        print(f"   ➜ Total duration estimate: {summary['total_duration_estimate']:.1f}s")
        
        # Effects/Keyframes
        if config.show_keyframes and summary["effects"]:
            print(f"\n✨ Effects/Keyframes ({len(summary['effects'])} total):")
            for i, effect in enumerate(summary["effects"], 1):
                print(f"   {i}. {effect['type']}")
                print(f"      Property: {effect['property']}")
                print(f"      Animated: {effect['start']} → {effect['end']}")
        
        # Slots
        if config.show_slots:
            print(f"\n📁 Slots (placeholders for content):")
            slots = self.template.get("slots", {})
            for slot_name in sorted(slots.keys()):
                print(f"   • {slot_name}")
        
        # Checks
        print(f"\n✅ Validation:")
        checks = self._validate()
        for check_name, is_valid in checks.items():
            status = "✓" if is_valid else "✗"
            print(f"   [{status}] {check_name}")
        
        print("\n" + "="*70)
    
    def _validate(self) -> Dict[str, bool]:
        """Validate template"""
        checks = {}
        
        # Check 1: Canvas
        canvas = self.template.get("settings", {}).get("canvas", {})
        checks["Canvas defined"] = bool(canvas.get("width") and canvas.get("height"))
        
        # Check 2: Slots
        slots = self.template.get("slots", {})
        checks["Has slots"] = len(slots) > 0
        
        # Check 3: Tracks
        tracks = self.template.get("tracks", {})
        checks["Has tracks"] = len(tracks) > 0
        
        # Check 4: Duration
        config = self.template.get("settings", {})
        checks["Duration set"] = config.get("duration_per_slide") is not None
        
        # Check 5: Transition
        transition = config.get("transition", {})
        checks["Transition configured"] = bool(transition.get("type"))
        
        return checks
    
    def print_detailed_keyframes(self):
        """In chi tiết từng keyframe"""
        print("\n" + "="*70)
        print(f"🔍 DETAILED KEYFRAMES: {self.name}")
        print("="*70)
        
        tracks = self.template.get("tracks", {})
        
        for track_idx, (track_name, track) in enumerate(tracks.items(), 1):
            print(f"\n📍 Track {track_idx}: {track_name}")
            
            elements = track.get("elements", [])
            for elem_idx, elem in enumerate(elements, 1):
                print(f"   Element {elem_idx} ({elem.get('type')}):")
                
                keyframes = elem.get("keyframes", [])
                for kf_idx, kf in enumerate(keyframes, 1):
                    print(f"      KF{kf_idx}: {kf.get('property_type')}")
                    print(f"         Type: {kf.get('type')}")
                    print(f"         Value: {kf.get('at_start')} → {kf.get('at_end')}")
                    if kf.get('description'):
                        print(f"         Desc: {kf.get('description')}")
        
        print("\n" + "="*70)
    
    def compare_with_content(self, content_data: Dict[str, str]) -> Dict[str, Any]:
        """
        So sánh template với content data
        Kiểm tra xem có matching không
        """
        slots = self.template.get("slots", {})
        
        analysis = {
            "template_slots": list(slots.keys()),
            "content_keys": list(content_data.keys()),
            "matching": [],
            "missing_in_content": [],
            "extra_in_content": []
        }
        
        # Matching slots
        for slot in slots.keys():
            if slot in content_data:
                analysis["matching"].append({
                    "slot": slot,
                    "content_preview": (content_data[slot][:50] + "...") if len(content_data[slot]) > 50 else content_data[slot]
                })
            else:
                analysis["missing_in_content"].append(slot)
        
        # Extra content
        for key in content_data.keys():
            if key not in slots:
                analysis["extra_in_content"].append(key)
        
        return analysis
    
    def print_content_analysis(self, content_data: Dict[str, str]):
        """In phân tích matching giữa template và content"""
        analysis = self.compare_with_content(content_data)
        
        print("\n" + "="*70)
        print(f"🔗 TEMPLATE ↔ CONTENT ANALYSIS")
        print("="*70)
        
        print(f"\n📋 Template slots: {len(analysis['template_slots'])}")
        print(f"   {', '.join(analysis['template_slots'])}")
        
        print(f"\n📦 Content keys: {len(analysis['content_keys'])}")
        print(f"   {', '.join(analysis['content_keys'])}")
        
        print(f"\n✅ Matching: {len(analysis['matching'])}")
        for match in analysis["matching"]:
            print(f"   • {match['slot']} ← {match['content_preview']}")
        
        if analysis["missing_in_content"]:
            print(f"\n⚠️  Missing in content: {len(analysis['missing_in_content'])}")
            for missing in analysis["missing_in_content"]:
                print(f"   ✗ {missing}")
        
        if analysis["extra_in_content"]:
            print(f"\n⚠️  Extra in content: {len(analysis['extra_in_content'])}")
            for extra in analysis["extra_in_content"]:
                print(f"   ↳ {extra} (will be ignored)")
        
        # Validate
        print(f"\n📊 Status:")
        if not analysis["missing_in_content"] and not analysis["extra_in_content"]:
            print(f"   ✅ Perfect match! Ready to render")
        elif not analysis["missing_in_content"]:
            print(f"   ✅ Can render (extra content will be ignored)")
        else:
            print(f"   ❌ Cannot render (missing required slots)")
        
        print("\n" + "="*70)
    
    def generate_sample_content(self) -> Dict[str, str]:
        """
        Generate sample content URLs từ template
        Để người dùng test với ảnh mẫu
        """
        slots = self.template.get("slots", {})
        
        # Danh sách ảnh mẫu từ Unsplash (public)
        sample_images = [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop",
            "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720&fit=crop",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720&fit=crop",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1280&h=720&fit=crop",
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1280&h=720&fit=crop",
        ]
        
        sample_content = {}
        for i, slot_name in enumerate(sorted(slots.keys())):
            sample_content[slot_name] = sample_images[i % len(sample_images)]
        
        return sample_content
    
    def export_template_info(self, output_file: str = None) -> str:
        """
        Export template info thành file markdown
        Để reference
        """
        summary = self.get_summary()
        
        md = f"""# Template: {self.name}

## Cấu hình
- **Resolution**: {summary['canvas']['width']} × {summary['canvas']['height']}
- **Duration/Slide**: {summary['duration_per_slide']}s
- **Num Slides**: {summary['num_slides']}
- **Total Duration**: ~{summary['total_duration_estimate']:.1f}s

## Transition
- **Type**: {summary['transition']['type']}
- **Duration**: {summary['transition']['duration']}s

## Effects
- **Count**: {len(summary['effects'])}

"""
        if summary['effects']:
            md += "### Keyframes\n"
            for effect in summary['effects']:
                md += f"- **{effect['type']}**: {effect['property']} ({effect['start']} → {effect['end']})\n"
        
        # Slots
        slots = self.template.get("slots", {})
        md += f"\n## Slots ({len(slots)})\n"
        for slot_name in sorted(slots.keys()):
            md += f"- `{slot_name}`\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"✅ Exported to: {output_file}")
        
        return md


# ============================================================================
# Workflow: Template Development (với Preview)
# ============================================================================

def template_development_workflow():
    """
    Workflow để develop template một cách hiệu quả
    
    Steps:
    1. Tạo template JSON mẫu
    2. Preview template (kiểm tra settings)
    3. Generate sample content
    4. Test render
    5. Adjust nếu cần
    6. Finalize
    """
    print("\n" + "="*70)
    print("🎨 TEMPLATE DEVELOPMENT WORKFLOW")
    print("="*70)
    
    from template_processor import create_default_slideshow_template
    import os
    
    # Step 1: Create template
    print("\n1️⃣  Creating template...")
    template = create_default_slideshow_template()
    template_path = "template/dev-slideshow.json"
    os.makedirs("template", exist_ok=True)
    
    with open(template_path, 'w') as f:
        json.dump(template, f, indent=2)
    print(f"   ✅ Created: {template_path}")
    
    # Step 2: Preview
    print("\n2️⃣  Previewing template...")
    preview = TemplatePreviewTool(template_path)
    preview.print_preview()
    
    # Step 3: Detailed keyframes
    print("\n3️⃣  Detailed keyframes...")
    preview.print_detailed_keyframes()
    
    # Step 4: Generate sample content
    print("\n4️⃣  Generating sample content...")
    sample_content = preview.generate_sample_content()
    print("   Generated sample URLs:")
    for slot, url in sample_content.items():
        print(f"   • {slot}: {url[:60]}...")
    
    # Step 5: Check content matching
    print("\n5️⃣  Analyzing template ↔ content matching...")
    preview.print_content_analysis(sample_content)
    
    # Step 6: Export template info
    print("\n6️⃣  Exporting template info...")
    md_info = preview.export_template_info(f"template/dev-slideshow-INFO.md")
    print("   ✅ Exported to: template/dev-slideshow-INFO.md")
    
    print("\n" + "="*70)
    print("✨ Template development workflow completed!")
    print("="*70)
    print(f"\nNext: Test render with actual content")
    print(f"  from template_processor import TemplateProcessor")
    print(f"  processor = TemplateProcessor('{template_path}')")
    print(f"  result = processor.render(sample_content)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        template_path = sys.argv[1]
        
        # Mode 1: Preview
        if len(sys.argv) > 2 and sys.argv[2] == "--detailed":
            preview = TemplatePreviewTool(template_path)
            preview.print_preview()
            preview.print_detailed_keyframes()
        
        # Mode 2: Preview + compare with content
        elif len(sys.argv) > 2:
            content_path = sys.argv[2]
            with open(content_path) as f:
                content = json.load(f)
            
            preview = TemplatePreviewTool(template_path)
            preview.print_preview()
            preview.print_content_analysis(content)
        
        # Mode 3: Just preview
        else:
            preview = TemplatePreviewTool(template_path)
            preview.print_preview()
    
    else:
        # Run workflow demo
        template_development_workflow()
