"""
📤 Draft Exporter v2 - Export CapCut draft → layer-based template cho VideoBuilder

Vấn đề: CapCut lưu tất cả tracks giống nhau, không phân biệt logo/background/text.
Giải pháp: Đọc draft → hiển thị tracks → user tag role → export template chỉ giữ style.

Cách dùng:
  # Interactive mode (được hỏi tag từng track)
  python draft_exporter.py "path/to/capcut/draft"

  # Convention mode (đặt tên track trong CapCut: bg_track, logo_track, text_track...)
  python draft_exporter.py "path/to/capcut/draft" --auto

  # Programmatic mode
  exporter = DraftExporter("path/to/draft")
  exporter.analyze()
  exporter.tag_track("Video_1", role="background", layer_type="dynamic_image")
  exporter.tag_track("Video_2", role="logo", layer_type="persistent_image")
  exporter.tag_track("Text_1", role="script_text", layer_type="dynamic_text")
  template = exporter.export_template("podcast-from-draft")
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


# ── Đơn vị thời gian CapCut: microseconds ──────────────────────────
def us_to_sec(us: int) -> float:
    """Microseconds → seconds"""
    return us / 1_000_000

def sec_to_us(sec: float) -> int:
    """Seconds → microseconds"""
    return int(sec * 1_000_000)


# ── Role definitions ────────────────────────────────────────────────

LAYER_ROLES = {
    "background":   {"layer_type": "dynamic_image",    "description": "Background images slideshow (thay đổi theo segment)"},
    "overlay":      {"layer_type": "persistent_image",  "description": "Overlay ảnh/màu phủ lên background (xuyên suốt video)"},
    "script_text":  {"layer_type": "dynamic_text",      "description": "Script text (thay đổi theo segment)"},
    "title_text":   {"layer_type": "dynamic_text",      "description": "Tiêu đề segment (thay đổi, optional)"},
    "logo":         {"layer_type": "persistent_image",  "description": "Logo (xuyên suốt video)"},
    "play_icon":    {"layer_type": "persistent_image",  "description": "Play icon (xuyên suốt video)"},
    "watermark":    {"layer_type": "persistent_image",  "description": "Watermark (xuyên suốt video)"},
    "skip":         {"layer_type": None,                "description": "Bỏ qua track này, không export"},
}

# Convention: tên track chứa keyword → tự detect role
AUTO_DETECT_RULES = [
    (r"logo",           "logo"),
    (r"play",           "play_icon"),
    (r"watermark",      "watermark"),
    (r"overlay",        "overlay"),
    (r"bg|background",  "background"),
    (r"title",          "title_text"),
    (r"script|text|sub","script_text"),
]


# ── Data classes ────────────────────────────────────────────────────

@dataclass
class TrackInfo:
    """Thông tin 1 track đã phân tích"""
    name: str
    track_type: str           # video, text, audio, sticker, effect
    segment_count: int
    total_duration_sec: float
    segments: List[Dict]      # Raw segment data
    materials: List[Dict]     # Linked materials
    # Style extracted from first segment
    transform_x: float = 0.0
    transform_y: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    alpha: float = 1.0
    rotation: float = 0.0
    # Text-specific
    font: str = ""
    font_size: float = 0.0
    font_color: str = ""
    # Transition
    transition_type: str = ""
    transition_duration: float = 0.0
    # Role (sẽ được gán bởi user)
    role: str = ""
    relative_index: int = 0
    # Raw
    raw_track: Dict = field(default_factory=dict)


# ── DraftExporter ───────────────────────────────────────────────────

class DraftExporter:
    """Đọc CapCut draft → phân tích tracks → export template JSON"""

    def __init__(self, draft_path: str):
        """
        Args:
            draft_path: Đường dẫn tới draft folder (chứa draft_info.json)
        """
        self.draft_path = draft_path
        self.draft_info: Dict = {}
        self.tracks: List[TrackInfo] = []
        self._materials_map: Dict[str, Dict] = {}

        # Load
        info_path = os.path.join(draft_path, "draft_info.json")
        if not os.path.exists(info_path):
            raise FileNotFoundError(f"draft_info.json not found in: {draft_path}")

        with open(info_path, encoding="utf-8") as f:
            self.draft_info = json.load(f)

        self._build_materials_map()

    # ── Analysis ────────────────────────────────────────────────────

    def analyze(self) -> List[TrackInfo]:
        """Phân tích tất cả tracks trong draft"""
        raw_tracks = self.draft_info.get("tracks", [])
        self.tracks = []

        for i, raw_track in enumerate(raw_tracks):
            info = self._analyze_track(raw_track, i)
            if info:
                self.tracks.append(info)

        return self.tracks

    def _analyze_track(self, raw_track: Dict, index: int) -> Optional[TrackInfo]:
        """Phân tích 1 track"""
        track_type = raw_track.get("type", "unknown")
        track_name = raw_track.get("name", f"Track_{index}")
        segments = raw_track.get("segments", [])

        if not segments:
            return None

        # Tính tổng duration
        total_dur = 0
        for seg in segments:
            tr = seg.get("target_timerange", {})
            total_dur += tr.get("duration", 0)

        # Extract style từ segment đầu tiên
        first_seg = segments[0]
        clip = first_seg.get("clip", {})
        transform = clip.get("transform", {})
        scale = clip.get("scale", {})

        info = TrackInfo(
            name=track_name,
            track_type=track_type,
            segment_count=len(segments),
            total_duration_sec=us_to_sec(total_dur),
            segments=segments,
            materials=[],
            transform_x=transform.get("x", 0.0),
            transform_y=transform.get("y", 0.0),
            scale_x=scale.get("x", 1.0),
            scale_y=scale.get("y", 1.0),
            alpha=clip.get("alpha", 1.0),
            rotation=clip.get("rotation", 0.0),
            relative_index=index,
            raw_track=raw_track,
        )

        # Extract text style nếu là text track
        if track_type == "text":
            self._extract_text_style(info, first_seg)

        # Extract transition
        self._extract_transition(info, segments)

        # Link materials
        for seg in segments:
            mat_id = seg.get("material_id", "")
            if mat_id in self._materials_map:
                info.materials.append(self._materials_map[mat_id])

        return info

    def _extract_text_style(self, info: TrackInfo, segment: Dict):
        """Extract font/color/size từ text material"""
        mat_id = segment.get("material_id", "")
        mat = self._materials_map.get(mat_id, {})

        # Text content là JSON string bên trong material
        content_str = mat.get("content", "{}")
        try:
            content = json.loads(content_str) if isinstance(content_str, str) else content_str
        except json.JSONDecodeError:
            content = {}

        styles = content.get("styles", [])
        if styles:
            first_style = styles[0]
            info.font_size = first_style.get("size", 8.0)

            # Color: [r, g, b] float 0-1 → hex
            fill = first_style.get("fill", {})
            solid = fill.get("content", {}).get("solid", {})
            color_arr = solid.get("color", [1, 1, 1])
            if len(color_arr) >= 3:
                r, g, b = [int(c * 255) for c in color_arr[:3]]
                info.font_color = f"#{r:02X}{g:02X}{b:02X}"

            info.font = first_style.get("font", {}).get("id", "")

    def _extract_transition(self, info: TrackInfo, segments: List[Dict]):
        """Extract transition từ segments"""
        for seg in segments:
            extra_refs = seg.get("extra_material_refs", [])
            for ref_id in extra_refs:
                mat = self._materials_map.get(ref_id, {})
                if mat.get("type") == "transition":
                    info.transition_type = mat.get("name", "")
                    info.transition_duration = us_to_sec(mat.get("duration", 500000))
                    return

    def _build_materials_map(self):
        """Build lookup map: material_id → material data"""
        materials = self.draft_info.get("materials", {})

        for category in ["videos", "audios", "texts", "stickers",
                         "speeds", "material_animations", "effects",
                         "transitions", "canvases", "masks"]:
            items = materials.get(category, [])
            for item in items:
                item_id = item.get("id", "")
                if item_id:
                    self._materials_map[item_id] = item

    # ── Display ─────────────────────────────────────────────────────

    def print_analysis(self):
        """In phân tích tracks"""
        if not self.tracks:
            self.analyze()

        canvas = self.draft_info.get("canvas_config", {})
        print(f"\n{'='*70}")
        print(f"  DRAFT ANALYSIS: {os.path.basename(self.draft_path)}")
        print(f"{'='*70}")
        print(f"  Canvas: {canvas.get('width')}x{canvas.get('height')}")
        print(f"  Tracks: {len(self.tracks)}\n")

        for i, track in enumerate(self.tracks):
            role_label = f" → [{track.role}]" if track.role else ""
            print(f"  [{i}] {track.name} ({track.track_type}){role_label}")
            print(f"      Segments: {track.segment_count} | Duration: {track.total_duration_sec:.1f}s")
            print(f"      Position: x={track.transform_x:.2f}, y={track.transform_y:.2f}")
            print(f"      Scale: x={track.scale_x:.2f}, y={track.scale_y:.2f}")
            if track.font_size:
                print(f"      Font: {track.font} | Size: {track.font_size} | Color: {track.font_color}")
            if track.transition_type:
                print(f"      Transition: {track.transition_type} ({track.transition_duration:.1f}s)")
            print()

        print(f"{'='*70}")

    # ── Tagging ─────────────────────────────────────────────────────

    def tag_track(self, track_name: str, role: str):
        """
        Tag một track với role.

        Args:
            track_name: Tên track hoặc index (e.g., "Video_1" hoặc "0")
            role: "background", "logo", "script_text", "title_text", "overlay", "play_icon", "skip"
        """
        if role not in LAYER_ROLES:
            raise ValueError(f"Invalid role '{role}'. Valid: {list(LAYER_ROLES.keys())}")

        track = self._find_track(track_name)
        if track:
            track.role = role
            print(f"  Tagged '{track.name}' → {role}")
        else:
            print(f"  Track '{track_name}' not found")

    def auto_tag(self):
        """Tự động tag dựa trên tên track (convention)"""
        if not self.tracks:
            self.analyze()

        tagged = 0
        for track in self.tracks:
            name_lower = track.name.lower()
            for pattern, role in AUTO_DETECT_RULES:
                if re.search(pattern, name_lower):
                    track.role = role
                    tagged += 1
                    print(f"  Auto-tagged '{track.name}' → {role}")
                    break

        # Fallback: Nếu chưa tag gì
        untagged = [t for t in self.tracks if not t.role]
        if untagged:
            print(f"\n  ⚠️  {len(untagged)} tracks chưa được tag:")
            for t in untagged:
                print(f"     - {t.name} ({t.track_type}, {t.segment_count} segments)")

        return tagged

    def interactive_tag(self):
        """Interactive mode: hỏi user tag từng track"""
        if not self.tracks:
            self.analyze()

        self.print_analysis()

        print("\nAvailable roles:")
        for role, info in LAYER_ROLES.items():
            print(f"  {role:15s} → {info['description']}")

        print()

        for i, track in enumerate(self.tracks):
            if track.role:
                print(f"  [{i}] {track.name}: already tagged → {track.role}")
                continue

            # Suggest role
            suggestion = self._suggest_role(track)
            prompt_suffix = f" (suggested: {suggestion})" if suggestion else ""

            role = input(f"  [{i}] {track.name} ({track.track_type}, {track.segment_count} segs)"
                        f"{prompt_suffix}\n      Role? ").strip()

            if not role and suggestion:
                role = suggestion

            if role in LAYER_ROLES:
                track.role = role
                print(f"      → Tagged: {role}\n")
            elif role:
                print(f"      ⚠️  Unknown role '{role}', skipping\n")
            else:
                print(f"      → Skipped\n")

    def _suggest_role(self, track: TrackInfo) -> str:
        """Gợi ý role dựa trên đặc điểm track"""
        # Text track
        if track.track_type == "text":
            if track.segment_count > 2:
                return "script_text"
            else:
                return "title_text"

        # Video/image track
        if track.track_type == "video":
            # Nhiều segments → dynamic background
            if track.segment_count > 2:
                return "background"
            # 1 segment nhỏ, scale nhỏ → logo hoặc icon
            elif track.segment_count == 1 and track.scale_x < 0.5:
                return "logo"
            # 1 segment full → overlay hoặc background
            elif track.segment_count == 1:
                return "overlay"

        return ""

    def _find_track(self, name_or_index: str) -> Optional[TrackInfo]:
        """Tìm track theo tên hoặc index"""
        # Thử index
        try:
            idx = int(name_or_index)
            if 0 <= idx < len(self.tracks):
                return self.tracks[idx]
        except ValueError:
            pass

        # Thử tên
        for track in self.tracks:
            if track.name == name_or_index:
                return track

        return None

    # ── Export ───────────────────────────────────────────────────────

    def export_template(self, template_name: str, output_dir: str = "template") -> Dict:
        """
        Export tagged tracks → template JSON cho VideoBuilder.

        Chỉ lưu STYLE & LAYOUT, không lưu content (URLs, text nội dung).

        Returns:
            Template dictionary
        """
        if not self.tracks:
            self.analyze()

        canvas = self.draft_info.get("canvas_config", {})

        # Build layers từ tagged tracks
        layers = []
        motion_presets = self._default_motion_presets()

        for track in self.tracks:
            if not track.role or track.role == "skip":
                continue

            role_info = LAYER_ROLES[track.role]
            layer_type = role_info["layer_type"]
            if not layer_type:
                continue

            layer = self._track_to_layer(track, layer_type)
            layers.append(layer)

        # Sort by relative_index
        layers.sort(key=lambda l: l.get("relative_index", 0))

        template = {
            "name": template_name,
            "version": "2.0.0",
            "description": f"Exported from CapCut draft: {os.path.basename(self.draft_path)}",
            "canvas": {
                "width": canvas.get("width", 1080),
                "height": canvas.get("height", 1920),
            },
            "layers": layers,
            "motion_presets": motion_presets,
        }

        # Save
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{template_name}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"\n  Template exported: {output_path}")
        print(f"  Layers: {len(layers)}")
        for layer in layers:
            opt = " (optional)" if layer.get("optional") else ""
            print(f"    [{layer['relative_index']}] {layer['id']:20s} {layer['type']:20s}{opt}")

        return template

    def _track_to_layer(self, track: TrackInfo, layer_type: str) -> Dict:
        """Convert TrackInfo → layer definition cho template"""

        # Base layer
        layer: Dict[str, Any] = {
            "id": track.role,
            "type": layer_type,
            "description": LAYER_ROLES[track.role]["description"],
            "track_name": f"{track.role}_track",
            "relative_index": track.relative_index,
        }

        # Persistent image layers cần source_key
        if layer_type == "persistent_image":
            layer["source_key"] = f"{track.role}_url"
            # Logo, play_icon, watermark là optional trừ logo
            if track.role in ("play_icon", "watermark", "overlay"):
                layer["optional"] = True

        # Style: position + scale (lưu từ draft)
        layer["style"] = {
            "transform_x": round(track.transform_x, 4),
            "transform_y": round(track.transform_y, 4),
            "scale_x": round(track.scale_x, 4),
            "scale_y": round(track.scale_y, 4),
        }

        # Text-specific style
        if track.track_type == "text":
            layer["style"].update(self._extract_full_text_style(track))

        # Dynamic image: transition + motion
        if layer_type == "dynamic_image":
            if track.transition_type:
                layer["transition"] = {
                    "type": track.transition_type,
                    "duration": round(track.transition_duration, 2),
                }
            else:
                layer["transition"] = {"type": "Dissolve", "duration": 0.5}

            layer["motion"] = {
                "presets": ["zoom_in", "zoom_out", "pan_left_right", "pan_right_left", "pan_top_down"],
                "random": True,
            }

        # Dynamic text: animation (nếu có)
        if layer_type == "dynamic_text":
            layer["intro_animation"] = None
            layer["intro_duration"] = 0.3
            layer["outro_animation"] = None
            layer["outro_duration"] = 0.3

            # Optional layer cho title
            if track.role == "title_text":
                layer["optional"] = True

        return layer

    def _extract_full_text_style(self, track: TrackInfo) -> Dict:
        """Extract đầy đủ text style từ track materials"""
        style: Dict[str, Any] = {
            "font_size": track.font_size or 8.0,
            "font_color": track.font_color or "#FFFFFF",
            "font_alpha": track.alpha,
        }

        if track.font:
            style["font"] = track.font

        # Extract từ text material nếu có
        for mat in track.materials:
            content_str = mat.get("content", "")
            try:
                content = json.loads(content_str) if isinstance(content_str, str) else content_str
            except (json.JSONDecodeError, TypeError):
                continue

            styles_list = content.get("styles", [])
            if not styles_list:
                continue

            first = styles_list[0]

            # Border
            stroke = first.get("stroke", {})
            if stroke:
                stroke_content = stroke.get("content", {}).get("solid", {})
                stroke_color = stroke_content.get("color", [0, 0, 0])
                if len(stroke_color) >= 3:
                    r, g, b = [int(c * 255) for c in stroke_color[:3]]
                    style["border_color"] = f"#{r:02X}{g:02X}{b:02X}"
                style["border_width"] = stroke.get("width", 0.0)
                style["border_alpha"] = stroke_content.get("alpha", 1.0)

            # Shadow
            shadow = first.get("shadow", {})
            if shadow:
                style["shadow_enabled"] = True
                shadow_color = shadow.get("color", {}).get("solid", {}).get("color", [0, 0, 0])
                if len(shadow_color) >= 3:
                    r, g, b = [int(c * 255) for c in shadow_color[:3]]
                    style["shadow_color"] = f"#{r:02X}{g:02X}{b:02X}"
                style["shadow_alpha"] = shadow.get("color", {}).get("solid", {}).get("alpha", 0.8)
                style["shadow_distance"] = shadow.get("distance", 5.0)
                style["shadow_angle"] = shadow.get("angle", -45.0)
                style["shadow_smoothing"] = shadow.get("smoothing", 0.15)

            # Background
            bg = first.get("background_style", {})
            if bg:
                style["background_alpha"] = bg.get("background_alpha", 0.0)
                bg_color = bg.get("background_color", [0, 0, 0])
                if len(bg_color) >= 3:
                    r, g, b = [int(c * 255) for c in bg_color[:3]]
                    style["background_color"] = f"#{r:02X}{g:02X}{b:02X}"
                else:
                    style["background_color"] = "#000000"
                style["background_style"] = bg.get("style", 0)
                style["background_round_radius"] = bg.get("round_radius", 0.0)

            break  # Chỉ cần first style

        # Defaults cho fields chưa có
        style.setdefault("border_width", 0.0)
        style.setdefault("border_color", "#000000")
        style.setdefault("border_alpha", 1.0)
        style.setdefault("shadow_enabled", False)
        style.setdefault("shadow_color", "#000000")
        style.setdefault("shadow_alpha", 0.8)
        style.setdefault("shadow_angle", -45.0)
        style.setdefault("shadow_distance", 3.0)
        style.setdefault("shadow_smoothing", 0.15)
        style.setdefault("background_color", "#000000")
        style.setdefault("background_alpha", 0.0)
        style.setdefault("background_style", 0)
        style.setdefault("background_round_radius", 0.0)
        style.setdefault("fixed_width", -1)
        style.setdefault("fixed_height", -1)

        return style

    def _default_motion_presets(self) -> Dict:
        """Motion presets mặc định"""
        return {
            "zoom_in": {
                "description": "Zoom In: scale 1.0 → 1.25",
                "keyframes": [
                    {"property": "scale_x", "start": "1.0", "end": "1.25"},
                    {"property": "scale_y", "start": "1.0", "end": "1.25"},
                ]
            },
            "zoom_out": {
                "description": "Zoom Out: scale 1.25 → 1.0",
                "keyframes": [
                    {"property": "scale_x", "start": "1.25", "end": "1.0"},
                    {"property": "scale_y", "start": "1.25", "end": "1.0"},
                ]
            },
            "pan_left_right": {
                "description": "Pan trái → phải",
                "keyframes": [
                    {"property": "scale_x", "start": "1.15", "end": "1.15"},
                    {"property": "scale_y", "start": "1.15", "end": "1.15"},
                    {"property": "position_x", "start": "-0.08", "end": "0.08"},
                ]
            },
            "pan_right_left": {
                "description": "Pan phải → trái",
                "keyframes": [
                    {"property": "scale_x", "start": "1.15", "end": "1.15"},
                    {"property": "scale_y", "start": "1.15", "end": "1.15"},
                    {"property": "position_x", "start": "0.08", "end": "-0.08"},
                ]
            },
            "pan_top_down": {
                "description": "Pan trên → dưới",
                "keyframes": [
                    {"property": "scale_x", "start": "1.15", "end": "1.15"},
                    {"property": "scale_y", "start": "1.15", "end": "1.15"},
                    {"property": "position_y", "start": "0.06", "end": "-0.06"},
                ]
            },
        }


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    import sys

    if len(sys.argv) < 2:
        print("""
Draft Exporter v2 - Export CapCut draft → layer-based template

Usage:
  python draft_exporter.py <draft_path>                    # Interactive tag
  python draft_exporter.py <draft_path> --auto             # Auto-detect roles
  python draft_exporter.py <draft_path> --auto --export <name>  # Auto + export

Examples:
  python draft_exporter.py "C:\\Users\\...\\CapCut\\Draft\\my-podcast"
  python draft_exporter.py "C:\\Users\\...\\CapCut\\Draft\\my-podcast" --auto --export podcast-v1

Available roles:
  background    → Background slideshow (dynamic, thay đổi theo segment)
  overlay       → Dark overlay lên background (persistent, xuyên suốt)
  script_text   → Script text (dynamic, thay đổi theo segment)
  title_text    → Tiêu đề segment (dynamic, optional)
  logo          → Logo (persistent, xuyên suốt video)
  play_icon     → Play icon (persistent, optional)
  watermark     → Watermark (persistent, optional)
  skip          → Bỏ qua track này

Tip: Đặt tên track trong CapCut theo convention để --auto detect:
  bg_track, logo_track, text_track, title_track, overlay_track, play_track
        """)
        return

    draft_path = sys.argv[1]
    auto_mode = "--auto" in sys.argv
    export_name = None

    if "--export" in sys.argv:
        idx = sys.argv.index("--export")
        if idx + 1 < len(sys.argv):
            export_name = sys.argv[idx + 1]

    try:
        exporter = DraftExporter(draft_path)
        exporter.analyze()

        if auto_mode:
            exporter.auto_tag()
        else:
            exporter.interactive_tag()

        exporter.print_analysis()

        if export_name:
            exporter.export_template(export_name)
        else:
            do_export = input("\nExport template? (y/n): ").strip().lower()
            if do_export == "y":
                name = input("Template name: ").strip() or "exported-template"
                exporter.export_template(name)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
