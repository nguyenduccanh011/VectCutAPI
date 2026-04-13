"""
VideoBuilder v2 - Layer-based template engine cho VectCutAPI

Giải quyết:
- Multi-layer compositions (overlay + background + text + logo)
- Dynamic segment count (số ảnh/text tuỳ script)
- Persistent elements (logo, play icon xuyên suốt video)
- Random motion effects (zoom/pan ngẫu nhiên)
- Script-driven content (text thay đổi theo segment)

Layer types:
- persistent_image: Hiển thị xuyên suốt video (logo, play icon, overlay)
- dynamic_image:    Slideshow ảnh thay đổi theo segment
- dynamic_text:     Text thay đổi theo segment
"""

import json
import random
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field

# ── Imports từ VectCutAPI ──────────────────────────────────────────────
from add_image_impl import add_image_impl
from add_text_impl import add_text_impl
from add_video_keyframe_impl import add_video_keyframe_impl
from save_draft_impl import save_draft_impl
from create_draft import get_or_create_draft


# ── Data classes ───────────────────────────────────────────────────────

@dataclass
class Segment:
    """Một segment trong script video"""
    text: str                        # Nội dung text chính
    duration: float                  # Thời lượng (giây)
    image_url: str                   # URL ảnh background
    title: str = ""                  # Tiêu đề (optional)
    image_urls: list = field(default_factory=list)  # Nhiều ảnh cho 1 segment (future)

    @classmethod
    def from_dict(cls, d: dict) -> "Segment":
        return cls(
            text=d.get("text", ""),
            duration=d.get("duration", 3.0),
            image_url=d.get("image_url", ""),
            title=d.get("title", ""),
            image_urls=d.get("image_urls", []),
        )


@dataclass
class RenderInput:
    """Input để render video từ template"""
    segments: List[Segment]
    logo_url: str = ""
    play_icon_url: str = ""
    overlay_url: str = ""               # Dark overlay (optional)
    extra: Dict[str, Any] = field(default_factory=dict)  # Mở rộng tương lai

    @classmethod
    def from_dict(cls, d: dict) -> "RenderInput":
        segments = [Segment.from_dict(s) for s in d.get("segments", [])]
        return cls(
            segments=segments,
            logo_url=d.get("logo_url", ""),
            play_icon_url=d.get("play_icon_url", ""),
            overlay_url=d.get("overlay_url", ""),
            extra=d.get("extra", {}),
        )


# ── VideoBuilder ──────────────────────────────────────────────────────

class VideoBuilder:
    """
    Layer-based video builder sử dụng JSON template.

    Workflow:
        builder = VideoBuilder("template/podcast-video-v1.json")
        result = builder.render(render_input)
    """

    EPSILON = 0.01  # Tránh trùng boundary keyframe

    def __init__(self, template_path: str):
        path = Path(template_path)
        if not path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(path, encoding="utf-8") as f:
            self.template = json.load(f)

        self.canvas = self.template["canvas"]
        self.layers = self.template["layers"]
        self.motion_presets = self.template.get("motion_presets", {})
        self.name = self.template.get("name", "unknown")

        self._draft_id: Optional[str] = None

    # ── Public API ─────────────────────────────────────────────────

    def render(
        self,
        render_input: RenderInput,
        draft_folder: str = None,
        draft_id: str = None,
    ) -> Dict[str, Any]:
        """
        Render video từ template + input.

        Args:
            render_input: RenderInput chứa segments, logo, overlay, v.v.
            draft_folder: Thư mục CapCut để lưu draft (optional)
            draft_id: Draft ID có sẵn (optional, nếu muốn thêm vào draft cũ)

        Returns:
            {
                "success": bool,
                "draft_id": str,
                "total_duration": float,
                "segment_count": int,
                "layers_rendered": list[str],
                "error": str (nếu lỗi)
            }
        """
        self._draft_id = draft_id
        segments = render_input.segments

        if not segments:
            return {"success": False, "error": "Không có segments"}

        # Tính timeline
        timeline = self._build_timeline(segments)
        total_duration = timeline[-1]["end"]

        print(f"\n{'='*60}")
        print(f"🎬 VideoBuilder: {self.name}")
        print(f"   Canvas: {self.canvas['width']}×{self.canvas['height']}")
        print(f"   Segments: {len(segments)}")
        print(f"   Duration: {total_duration:.1f}s")
        print(f"{'='*60}")

        layers_rendered = []

        try:
            # Render từng layer theo thứ tự relative_index (bottom → top)
            sorted_layers = sorted(self.layers, key=lambda l: l.get("relative_index", 0))

            for layer_def in sorted_layers:
                layer_id = layer_def["id"]
                layer_type = layer_def["type"]
                is_optional = layer_def.get("optional", False)

                # Kiểm tra layer optional có source không
                if is_optional and not self._has_source(layer_def, render_input):
                    print(f"\n⏭️  Skip layer '{layer_id}' (optional, no source)")
                    continue

                print(f"\n📍 Layer: {layer_id} ({layer_type})")

                if layer_type == "persistent_image":
                    self._render_persistent_image(layer_def, render_input, total_duration)
                elif layer_type == "dynamic_image":
                    self._render_dynamic_images(layer_def, segments, timeline)
                elif layer_type == "dynamic_text":
                    self._render_dynamic_text(layer_def, segments, timeline)
                else:
                    print(f"   ⚠️  Unknown layer type: {layer_type}")
                    continue

                layers_rendered.append(layer_id)

            # Save draft
            if draft_folder:
                print(f"\n💾 Saving draft...")
                save_draft_impl(self._draft_id, draft_folder)

            return {
                "success": True,
                "draft_id": self._draft_id,
                "total_duration": total_duration,
                "segment_count": len(segments),
                "layers_rendered": layers_rendered,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    # ── Timeline ───────────────────────────────────────────────────

    def _build_timeline(self, segments: List[Segment]) -> List[Dict]:
        """Tính timeline cho từng segment"""
        timeline = []
        current_time = 0.0
        for i, seg in enumerate(segments):
            timeline.append({
                "index": i,
                "start": current_time,
                "end": current_time + seg.duration,
                "duration": seg.duration,
            })
            current_time += seg.duration
        return timeline

    # ── Layer renderers ────────────────────────────────────────────

    def _render_persistent_image(
        self, layer: dict, render_input: RenderInput, total_duration: float
    ):
        """Render ảnh persistent (logo, play icon, overlay) - hiển thị suốt video."""
        source_key = layer.get("source_key", "")
        image_url = self._resolve_source(source_key, render_input)

        if not image_url:
            print(f"   ⚠️  No URL for source_key '{source_key}'")
            return

        style = layer.get("style", {})

        result = add_image_impl(
            image_url=image_url,
            start=0,
            end=total_duration,
            width=self.canvas["width"],
            height=self.canvas["height"],
            track_name=layer["track_name"],
            relative_index=layer.get("relative_index", 0),
            draft_id=self._draft_id,
            transform_x=style.get("transform_x", 0),
            transform_y=style.get("transform_y", 0),
            scale_x=style.get("scale_x", 1.0),
            scale_y=style.get("scale_y", 1.0),
        )

        if result.get("success"):
            self._draft_id = result["output"]["draft_id"]
            print(f"   ✓ Persistent: {source_key} (0s → {total_duration:.1f}s)")
        else:
            print(f"   ✗ Error: {result.get('error')}")

    def _render_dynamic_images(
        self, layer: dict, segments: List[Segment], timeline: List[Dict]
    ):
        """Render slideshow ảnh background - mỗi segment 1 ảnh."""
        style = layer.get("style", {})
        transition_cfg = layer.get("transition", {})
        motion_cfg = layer.get("motion", {})
        bg_blur = layer.get("background_blur")

        # Motion presets
        preset_names = motion_cfg.get("presets", [])
        use_random = motion_cfg.get("random", False)

        for i, (seg, tl) in enumerate(zip(segments, timeline)):
            if not seg.image_url:
                print(f"   ⏭️  Segment {i}: no image_url, skip")
                continue

            # Transition (không cho ảnh đầu tiên)
            transition_type = transition_cfg.get("type") if i > 0 else None
            transition_dur = transition_cfg.get("duration", 0.5)

            result = add_image_impl(
                image_url=seg.image_url,
                start=tl["start"],
                end=tl["end"],
                width=self.canvas["width"],
                height=self.canvas["height"],
                track_name=layer["track_name"],
                relative_index=layer.get("relative_index", 0),
                draft_id=self._draft_id,
                transform_x=style.get("transform_x", 0),
                transform_y=style.get("transform_y", 0),
                scale_x=style.get("scale_x", 1.0),
                scale_y=style.get("scale_y", 1.0),
                transition=transition_type,
                transition_duration=transition_dur,
                background_blur=bg_blur,
            )

            if not result.get("success"):
                print(f"   ✗ Segment {i}: {result.get('error')}")
                continue

            self._draft_id = result["output"]["draft_id"]

            # Apply motion keyframes
            if preset_names:
                if use_random:
                    preset_name = random.choice(preset_names)
                else:
                    preset_name = preset_names[i % len(preset_names)]

                self._apply_motion(
                    layer["track_name"], preset_name,
                    tl["start"], tl["duration"]
                )
                motion_label = preset_name
            else:
                motion_label = "none"

            print(f"   ✓ Seg {i}: {tl['start']:.1f}s→{tl['end']:.1f}s | {motion_label}")

    def _render_dynamic_text(
        self, layer: dict, segments: List[Segment], timeline: List[Dict]
    ):
        """Render text segments - mỗi segment 1 đoạn text."""
        style = layer.get("style", {})
        layer_id = layer["id"]
        intro_anim = layer.get("intro_animation")
        intro_dur = layer.get("intro_duration", 0.3)
        outro_anim = layer.get("outro_animation")
        outro_dur = layer.get("outro_duration", 0.3)

        for i, (seg, tl) in enumerate(zip(segments, timeline)):
            # Xác định text content theo layer_id
            if layer_id == "title_text":
                text_content = seg.title
            else:
                text_content = seg.text

            if not text_content:
                continue

            result = add_text_impl(
                text=text_content,
                start=tl["start"],
                end=tl["end"],
                draft_id=self._draft_id,
                track_name=layer["track_name"],
                width=self.canvas["width"],
                height=self.canvas["height"],
                # Font
                font=style.get("font"),
                font_size=style.get("font_size", 8.0),
                font_color=style.get("font_color", "#FFFFFF"),
                font_alpha=style.get("font_alpha", 1.0),
                # Position
                transform_x=style.get("transform_x", 0),
                transform_y=style.get("transform_y", 0),
                # Border
                border_width=style.get("border_width", 0.0),
                border_color=style.get("border_color", "#000000"),
                border_alpha=style.get("border_alpha", 1.0),
                # Shadow
                shadow_enabled=style.get("shadow_enabled", False),
                shadow_color=style.get("shadow_color", "#000000"),
                shadow_alpha=style.get("shadow_alpha", 0.8),
                shadow_angle=style.get("shadow_angle", -45.0),
                shadow_distance=style.get("shadow_distance", 3.0),
                shadow_smoothing=style.get("shadow_smoothing", 0.15),
                # Background
                background_color=style.get("background_color", "#000000"),
                background_alpha=style.get("background_alpha", 0.0),
                background_style=style.get("background_style", 0),
                background_round_radius=style.get("background_round_radius", 0.0),
                # Size
                fixed_width=style.get("fixed_width", -1),
                fixed_height=style.get("fixed_height", -1),
                # Animation
                intro_animation=intro_anim,
                intro_duration=intro_dur,
                outro_animation=outro_anim,
                outro_duration=outro_dur,
            )

            if result.get("success"):
                self._draft_id = result["output"]["draft_id"]
                preview = text_content[:30] + ("..." if len(text_content) > 30 else "")
                print(f"   ✓ Seg {i}: \"{preview}\" ({tl['start']:.1f}s→{tl['end']:.1f}s)")
            else:
                print(f"   ✗ Seg {i}: {result.get('error')}")

    # ── Motion keyframes ───────────────────────────────────────────

    def _apply_motion(
        self, track_name: str, preset_name: str,
        clip_start: float, clip_duration: float
    ):
        """Apply motion preset keyframes cho 1 segment."""
        preset = self.motion_presets.get(preset_name)
        if not preset:
            return

        for kf in preset.get("keyframes", []):
            prop = kf["property"]
            val_start = kf["start"]
            val_end = kf["end"]

            # Keyframe đầu
            add_video_keyframe_impl(
                draft_id=self._draft_id,
                track_name=track_name,
                property_type=prop,
                time=clip_start + self.EPSILON,
                value=val_start,
            )
            # Keyframe cuối
            add_video_keyframe_impl(
                draft_id=self._draft_id,
                track_name=track_name,
                property_type=prop,
                time=clip_start + clip_duration - self.EPSILON,
                value=val_end,
            )

    # ── Helpers ────────────────────────────────────────────────────

    def _resolve_source(self, source_key: str, render_input: RenderInput) -> str:
        """Resolve source_key thành URL thực tế từ render_input."""
        mapping = {
            "logo_url": render_input.logo_url,
            "play_icon_url": render_input.play_icon_url,
            "overlay_url": render_input.overlay_url,
        }
        url = mapping.get(source_key, "")
        if not url:
            url = render_input.extra.get(source_key, "")
        return url

    def _has_source(self, layer: dict, render_input: RenderInput) -> bool:
        """Kiểm tra layer có source data không."""
        layer_type = layer["type"]

        if layer_type == "persistent_image":
            source_key = layer.get("source_key", "")
            return bool(self._resolve_source(source_key, render_input))
        elif layer_type in ("dynamic_image", "dynamic_text"):
            return bool(render_input.segments)
        return False

    # ── Static helpers ─────────────────────────────────────────────

    @staticmethod
    def list_templates(template_dir: str = "template") -> List[Dict[str, str]]:
        """List tất cả template v2 có sẵn."""
        templates = []
        template_path = Path(template_dir)
        if not template_path.exists():
            return templates

        for f in template_path.glob("*.json"):
            try:
                with open(f, encoding="utf-8") as fh:
                    data = json.load(fh)
                if "layers" in data:  # Chỉ template v2
                    templates.append({
                        "name": data.get("name", f.stem),
                        "path": str(f),
                        "description": data.get("description", ""),
                        "layers": len(data.get("layers", [])),
                    })
            except (json.JSONDecodeError, KeyError):
                continue

        return templates

    @staticmethod
    def preview_template(template_path: str) -> Dict[str, Any]:
        """Preview template không render."""
        with open(template_path, encoding="utf-8") as f:
            template = json.load(f)

        canvas = template.get("canvas", {})
        layers = template.get("layers", [])
        presets = template.get("motion_presets", {})

        layer_summary = []
        for layer in layers:
            layer_summary.append({
                "id": layer["id"],
                "type": layer["type"],
                "track": layer.get("track_name"),
                "z_index": layer.get("relative_index", 0),
                "optional": layer.get("optional", False),
                "description": layer.get("description", ""),
            })

        return {
            "name": template.get("name"),
            "canvas": canvas,
            "layers": layer_summary,
            "motion_presets": list(presets.keys()),
            "layer_count": len(layers),
        }
