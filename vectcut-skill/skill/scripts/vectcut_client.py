#!/usr/bin/env python3
"""
VectCutAPI Python Client

A Python client library for VectCutAPI video editing service.
Provides a convenient interface for creating video drafts programmatically.

Usage:
    from vectcut_client import VectCutClient

    client = VectCutClient("http://localhost:9001")
    draft = client.create_draft(width=1080, height=1920)
    client.add_video(draft.draft_id, "https://example.com/video.mp4")
    client.add_text(draft.draft_id, "Hello World", start=0, end=5)
    result = client.save_draft(draft.draft_id)
    print(result.draft_url)
"""

import requests
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class Resolution(Enum):
    """Common video resolution presets."""
    VERTICAL = (1080, 1920)      # Vertical - TikTok
    HORIZONTAL = (1920, 1080)    # Horizontal - YouTube
    SQUARE = (1080, 1080)        # Square - Instagram
    WIDE = (1920, 1200)          # Wide


class Transition(Enum):
    """Transition effect types."""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    WIPE_UP = "wipe_up"
    WIPE_DOWN = "wipe_down"


class TextAnimation(Enum):
    """Text animation types."""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    SLIDE_IN_LEFT = "slide_in_left"
    SLIDE_IN_RIGHT = "slide_in_right"
    SLIDE_OUT_LEFT = "slide_out_left"
    SLIDE_OUT_RIGHT = "slide_out_right"
    ROTATE_IN = "rotate_in"
    ROTATE_OUT = "rotate_out"


@dataclass
class DraftInfo:
    """Draft information."""
    draft_id: str
    draft_folder: Optional[str] = None
    draft_url: Optional[str] = None

    def __str__(self):
        return f"Draft(id={self.draft_id}, url={self.draft_url})"


@dataclass
class ApiResult:
    """API response result."""
    success: bool
    output: Dict[str, Any]
    error: Optional[str] = None

    @property
    def draft_id(self) -> Optional[str]:
        return self.output.get("draft_id")

    @property
    def draft_url(self) -> Optional[str]:
        return self.output.get("draft_url")

    @property
    def draft_folder(self) -> Optional[str]:
        return self.output.get("draft_folder")


class VectCutClient:
    """
    VectCutAPI Python client.

    Provides a simple interface for the VectCutAPI video editing service.
    """

    def __init__(self, base_url: str = "http://localhost:9001", timeout: int = 120):
        """
        Initialize client.

        Args:
            base_url: API server URL.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _post(self, endpoint: str, **kwargs) -> ApiResult:
        """
        Send a POST request.

        Args:
            endpoint: API endpoint.
            **kwargs: Request payload.

        Returns:
            ApiResult: API result.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=kwargs, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return ApiResult(
                success=data.get("success", False),
                output=data.get("output", {}),
                error=data.get("error")
            )
        except requests.RequestException as e:
            return ApiResult(success=False, output={}, error=str(e))

    def _get(self, endpoint: str) -> Any:
        """
        Send a GET request.

        Args:
            endpoint: API endpoint.

        Returns:
            Response data.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    # ==================== Core operations ====================

    def create_draft(self,
                    width: int = 1080,
                    height: int = 1920,
                    draft_folder: Optional[str] = None) -> DraftInfo:
        """
        Create a new draft.

        Args:
            width: Video width.
            height: Video height.
            draft_folder: Draft folder path.

        Returns:
            DraftInfo: Draft information.
        """
        result = self._post("/create_draft",
                           width=width,
                           height=height,
                           draft_folder=draft_folder)
        if result.success:
            return DraftInfo(
                draft_id=result.draft_id,
                draft_folder=result.draft_folder
            )
        raise Exception(f"Failed to create draft: {result.error}")

    def save_draft(self,
                  draft_id: str,
                  draft_folder: Optional[str] = None) -> DraftInfo:
        """
        Save a draft and generate a download URL.

        Args:
            draft_id: Draft ID.
            draft_folder: Draft folder path.

        Returns:
            DraftInfo: Draft info including draft_url.
        """
        result = self._post("/save_draft",
                           draft_id=draft_id,
                           draft_folder=draft_folder)
        if result.success:
            return DraftInfo(
                draft_id=draft_id,
                draft_folder=result.draft_folder,
                draft_url=result.draft_url
            )
        raise Exception(f"Failed to save draft: {result.error}")

    def query_draft_status(self, draft_id: str) -> Dict[str, Any]:
        """Query draft status"""
        return self._post("/query_draft_status", draft_id=draft_id)

    def query_script(self, draft_id: str) -> Dict[str, Any]:
        """Query draft script content"""
        return self._post("/query_script", draft_id=draft_id)

    # ==================== Media operations ====================

    def add_video(self,
                 draft_id: str,
                 video_url: str,
                 start: float = 0,
                 end: float = 0,
                 target_start: float = 0,
                 speed: float = 1.0,
                 volume: float = 1.0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 transform_x: float = 0,
                 transform_y: float = 0,
                 track_name: str = "video_main",
                 transition: Optional[str] = None,
                 transition_duration: float = 0.5,
                 mask_type: Optional[str] = None,
                 background_blur: Optional[int] = None,
                 **kwargs) -> bool:
        """
        Add video track

        Args:
            draft_id: Draft ID
            video_url: Video URL
            start: Video start time (seconds)
            end: Video end time (seconds)
            target_start: Start time on timeline
            speed: Playback speed
            volume: Volume (0.0-1.0)
            scale_x/scale_y: Scale ratio
            transform_x/transform_y: Position offset
            track_name: Track name
            transition: Transition type
            transition_duration: Transition duration (seconds)
            mask_type: Mask type
            background_blur: Background blur level (1-4)

        Returns:
            bool: Success flag
        """
        result = self._post("/add_video",
                           draft_id=draft_id,
                           video_url=video_url,
                           start=start,
                           end=end,
                           target_start=target_start,
                           speed=speed,
                           volume=volume,
                           scale_x=scale_x,
                           scale_y=scale_y,
                           transform_x=transform_x,
                           transform_y=transform_y,
                           track_name=track_name,
                           transition=transition,
                           transition_duration=transition_duration,
                           mask_type=mask_type,
                           background_blur=background_blur,
                           **kwargs)
        return result.success

    def add_audio(self,
                 draft_id: str,
                 audio_url: str,
                 start: float = 0,
                 end: Optional[float] = None,
                 target_start: float = 0,
                 speed: float = 1.0,
                 volume: float = 1.0,
                 track_name: str = "audio_main",
                 **kwargs) -> bool:
        """
        Add audio track

        Args:
            draft_id: Draft ID
            audio_url: Audio URL
            start: Audio start time
            end: Audio end time
            target_start: Start time on timeline
            speed: Playback speed
            volume: Volume (0.0-1.0)
            track_name: Track name

        Returns:
            bool: Success flag
        """
        result = self._post("/add_audio",
                           draft_id=draft_id,
                           audio_url=audio_url,
                           start=start,
                           end=end,
                           target_start=target_start,
                           speed=speed,
                           volume=volume,
                           track_name=track_name,
                           **kwargs)
        return result.success

    def add_image(self,
                 draft_id: str,
                 image_url: str,
                 start: float,
                 end: float,
                 target_start: float = 0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 transform_x: float = 0,
                 transform_y: float = 0,
                 animation_type: Optional[str] = None,
                 transition: Optional[str] = None,
                 **kwargs) -> bool:
        """
        Add image material

        Args:
            draft_id: Draft ID
            image_url: Image URL
            start: Start time
            end: End time
            target_start: Start time on timeline
            scale_x/scale_y: Scale ratio
            transform_x/transform_y: Position offset
            animation_type: Animation type
            transition: Transition type

        Returns:
            bool: Success flag
        """
        result = self._post("/add_image",
                           draft_id=draft_id,
                           image_url=image_url,
                           start=start,
                           end=end,
                           target_start=target_start,
                           scale_x=scale_x,
                           scale_y=scale_y,
                           transform_x=transform_x,
                           transform_y=transform_y,
                           animation_type=animation_type,
                           transition=transition,
                           **kwargs)
        return result.success

    def add_text(self,
                draft_id: str,
                text: str,
                start: float,
                end: float,
                font: str = "思源黑体",
                font_size: int = 32,
                font_color: str = "#FFFFFF",
                stroke_enabled: bool = False,
                stroke_color: str = "#FFFFFF",
                stroke_width: float = 2.0,
                shadow_enabled: bool = False,
                shadow_color: str = "#000000",
                background_color: Optional[str] = None,
                background_alpha: float = 1.0,
                background_round_radius: float = 0,
                text_intro: Optional[str] = None,
                text_outro: Optional[str] = None,
                text_styles: Optional[List[Dict]] = None,
                pos_x: float = 0,
                pos_y: float = 0,
                alignment_h: str = "center",
                alignment_v: str = "middle",
                **kwargs) -> bool:
        """
        Add text element

        Args:
            draft_id: Draft ID
            text: Text content
            start: Start time
            end: End time
            font: Font name
            font_size: Font size
            font_color: Font color (HEX)
            stroke_enabled: Enable stroke
            stroke_color: Stroke color
            stroke_width: Stroke width
            shadow_enabled: Enable shadow
            shadow_color: Shadow color
            background_color: Background color
            background_alpha: Background alpha
            background_round_radius: Background corner radius
            text_intro: Intro animation
            text_outro: Outro animation
            text_styles: Multi-style text
            pos_x/pos_y: Position
            alignment_h: Horizontal alignment
            alignment_v: Vertical alignment

        Returns:
            bool: Success flag
        """
        result = self._post("/add_text",
                           draft_id=draft_id,
                           text=text,
                           start=start,
                           end=end,
                           font=font,
                           font_size=font_size,
                           font_color=font_color,
                           stroke_enabled=stroke_enabled,
                           stroke_color=stroke_color,
                           stroke_width=stroke_width,
                           shadow_enabled=shadow_enabled,
                           shadow_color=shadow_color,
                           background_color=background_color,
                           background_alpha=background_alpha,
                           background_round_radius=background_round_radius,
                           text_intro=text_intro,
                           text_outro=text_outro,
                           text_styles=text_styles,
                           pos_x=pos_x,
                           pos_y=pos_y,
                           alignment_h=alignment_h,
                           alignment_v=alignment_v,
                           **kwargs)
        return result.success

    def add_subtitle(self,
                    draft_id: str,
                    srt_url: str,
                    font: str = "思源黑体",
                    font_size: int = 32,
                    font_color: str = "#FFFFFF",
                    stroke_enabled: bool = True,
                    stroke_color: str = "#000000",
                    stroke_width: float = 3.0,
                    background_alpha: float = 0.5,
                    pos_y: float = -0.3,
                    time_offset: float = 0,
                    **kwargs) -> bool:
        """
        Add SRT subtitles

        Args:
            draft_id: Draft ID
            srt_url: SRT file URL
            font: Font name
            font_size: Font size
            font_color: Font color
            stroke_enabled: Enable stroke
            stroke_color: Stroke color
            stroke_width: Stroke width
            background_alpha: Background alpha
            pos_y: Vertical position
            time_offset: Time offset (seconds)

        Returns:
            bool: Success flag
        """
        result = self._post("/add_subtitle",
                           draft_id=draft_id,
                           srt_url=srt_url,
                           font=font,
                           font_size=font_size,
                           font_color=font_color,
                           stroke_enabled=stroke_enabled,
                           stroke_color=stroke_color,
                           stroke_width=stroke_width,
                           background_alpha=background_alpha,
                           pos_y=pos_y,
                           time_offset=time_offset,
                           **kwargs)
        return result.success

    def add_sticker(self,
                   draft_id: str,
                   sticker_id: str,
                   start: float,
                   end: float,
                   target_start: float = 0,
                   scale_x: float = 1.0,
                   scale_y: float = 1.0,
                   transform_x: float = 0,
                   transform_y: float = 0,
                   flip_horizontal: bool = False,
                   flip_vertical: bool = False,
                   alpha: float = 1.0,
                   **kwargs) -> bool:
        """
        Add sticker

        Args:
            draft_id: Draft ID
            sticker_id: Sticker ID
            start: Start time
            end: End time
            target_start: Start time on timeline
            scale_x/scale_y: Scale ratio
            transform_x/transform_y: Position offset
            flip_horizontal: Flip horizontally
            flip_vertical: Flip vertically
            alpha: Opacity

        Returns:
            bool: Success flag
        """
        result = self._post("/add_sticker",
                           draft_id=draft_id,
                           sticker_id=sticker_id,
                           start=start,
                           end=end,
                           target_start=target_start,
                           scale_x=scale_x,
                           scale_y=scale_y,
                           transform_x=transform_x,
                           transform_y=transform_y,
                           flip_horizontal=flip_horizontal,
                           flip_vertical=flip_vertical,
                           alpha=alpha,
                           **kwargs)
        return result.success

    def add_effect(self,
                  draft_id: str,
                  effect_type: str,
                  start: float,
                  end: float,
                  target_start: float = 0,
                  intensity: float = 1.0,
                  effect_params: Optional[List] = None,
                  **kwargs) -> bool:
        """
        Add video effect

        Args:
            draft_id: Draft ID
            effect_type: Effect type
            start: Start time
            end: End time
            target_start: Start time on timeline
            intensity: Effect intensity
            effect_params: Effect parameters

        Returns:
            bool: Success flag
        """
        result = self._post("/add_effect",
                           draft_id=draft_id,
                           effect_type=effect_type,
                           start=start,
                           end=end,
                           target_start=target_start,
                           intensity=intensity,
                           effect_params=effect_params,
                           **kwargs)
        return result.success

    def add_video_keyframe(self,
                          draft_id: str,
                          track_name: str,
                          property_types: List[str],
                          times: List[float],
                          values: List[str],
                          **kwargs) -> bool:
        """
        Add keyframe animation

        Args:
            draft_id: Draft ID
            track_name: Track name
            property_types: Property type list
            times: Keyframe times
            values: Property values

        Returns:
            bool: Success flag
        """
        result = self._post("/add_video_keyframe",
                           draft_id=draft_id,
                           track_name=track_name,
                           property_types=property_types,
                           times=times,
                           values=values,
                           **kwargs)
        return result.success

    # ==================== Query interfaces ====================

    def get_intro_animation_types(self) -> List[str]:
        """Get intro animation type list"""
        return self._get("/get_intro_animation_types")

    def get_outro_animation_types(self) -> List[str]:
        """Get outro animation type list"""
        return self._get("/get_outro_animation_types")

    def get_transition_types(self) -> List[str]:
        """Get transition type list"""
        return self._get("/get_transition_types")

    def get_mask_types(self) -> List[str]:
        """Get mask type list"""
        return self._get("/get_mask_types")

    def get_audio_effect_types(self) -> List[str]:
        """Get audio effect type list"""
        return self._get("/get_audio_effect_types")

    def get_font_types(self) -> List[str]:
        """Get font type list"""
        return self._get("/get_font_types")

    def get_text_intro_types(self) -> List[str]:
        """Get text intro animation list"""
        return self._get("/get_text_intro_types")

    def get_text_outro_types(self) -> List[str]:
        """Get text outro animation list"""
        return self._get("/get_text_outro_types")

    def get_video_scene_effect_types(self) -> List[str]:
        """Get scene effect type list"""
        return self._get("/get_video_scene_effect_types")

    # ==================== Utilities ====================

    def get_duration(self, media_url: str) -> Optional[float]:
        """
        Get media duration

        Args:
            media_url: Media URL

        Returns:
            Duration in seconds; returns None on failure
        """
        result = self._post("/get_duration", media_url=media_url)
        if result.success:
            return result.output.get("duration")
        return None

    def close(self):
        """Close client session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ==================== Convenience function ====================

def create_quick_video(base_url: str = "http://localhost:9001",
                      video_url: str = "",
                      text_content: str = "",
                      bgm_url: str = "",
                      resolution: Resolution = Resolution.VERTICAL) -> Optional[str]:
    """
    Quickly create a simple video

    Args:
        base_url: API server URL
        video_url: Background video URL
        text_content: Text content
        bgm_url: Background music URL
        resolution: Video resolution

    Returns:
        Draft URL; returns None on failure
    """
    with VectCutClient(base_url) as client:
        draft = client.create_draft(width=resolution.value[0], height=resolution.value[1])

        if video_url:
            client.add_video(draft.draft_id, video_url)

        if bgm_url:
            client.add_audio(draft.draft_id, bgm_url, volume=0.3)

        if text_content:
            client.add_text(
                draft.draft_id,
                text_content,
                start=1,
                end=5,
                font_size=56,
                shadow_enabled=True,
                background_alpha=0.7
            )

        result = client.save_draft(draft.draft_id)
        return result.draft_url


if __name__ == "__main__":
    # Example usage
    with VectCutClient() as client:
        # Create draft
        draft = client.create_draft(width=1080, height=1920)
        print(f"Draft created: {draft.draft_id}")

        # Add video
        client.add_video(
            draft.draft_id,
            "https://example.com/video.mp4",
            volume=0.6
        )

        # Add text
        client.add_text(
            draft.draft_id,
            "Hello VectCutAPI!",
            start=0,
            end=5,
            font_size=64,
            font_color="#FFD700",
            shadow_enabled=True
        )

        # Save draft
        result = client.save_draft(draft.draft_id)
        print(f"Draft saved: {result.draft_url}")
