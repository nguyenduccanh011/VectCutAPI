# VectCutAPI Complete API Reference

## HTTP API Endpoints

### Core Operations

#### POST /create_draft

Create a new video draft project.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| width | int | No | Video width, default 1080 |
| height | int | No | Video height, default 1920 |
| draft_folder | string | No | Draft folder path |

**Common Resolutions:**
- `1080 x 1920` - Portrait (Short video/TikTok)
- `1920 x 1080` - Landscape (YouTube)
- `1080 x 1080` - Square (Instagram)

**Response Example:**

```json
{
  "success": true,
  "output": {
    "draft_id": "draft_1234567890",
    "draft_folder": "dfd_xxxxx"
  }
}
```

---

#### POST /save_draft

Save draft project and generate download link.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| draft_id | string | Yes | Draft ID |
| draft_folder | string | No | Draft folder path |

**Response Example:**

```json
{
  "success": true,
  "output": {
    "draft_url": "https://example.com/draft/downloader?id=xxx",
    "draft_folder": "dfd_xxxxx",
    "message": "Draft saved"
  }
}
```

---

#### POST /query_draft_status

Query draft status.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| draft_id | string | Yes | Draft ID |

---

#### POST /query_script

Query draft script content.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| draft_id | string | Yes | Draft ID |

---

### Material Addition

#### POST /add_video

Add video track to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| video_url | string | Required | Video URL (local or remote) |
| start | float | 0 | Video segment start time (seconds) |
| end | float | 0 | Video segment end time (seconds) |
| target_start | float | 0 | Start time on timeline |
| speed | float | 1.0 | Playback speed |
| volume | float | 1.0 | Volume (0.0-1.0) |
| scale_x | float | 1.0 | Horizontal scale |
| scale_y | float | 1.0 | Vertical scale |
| transform_x | float | 0 | Horizontal position offset |
| transform_y | float | 0 | Vertical position offset |
| track_name | string | "video_main" | Track name |
| relative_index | int | 0 | Relative index |
| duration | float | - | Duration |
| transition | string | - | Transition type |
| transition_duration | float | 0.5 | Transition duration (seconds) |
| mask_type | string | - | Mask type |
| mask_center_x | float | 0.5 | Mask center X |
| mask_center_y | float | 0.5 | Mask center Y |
| mask_size | float | 1.0 | Mask size |
| mask_rotation | float | 0.0 | Mask rotation angle |
| mask_feather | float | 0.0 | Mask feather |
| mask_invert | bool | False | Invert mask |
| background_blur | int | - | Background blur level (1-4) |

**Transition Types:**
- `fade_in` - Fade in
- `fade_out` - Fade out
- `wipe_left` - Left wipe
- `wipe_right` - Right wipe
- `wipe_up` - Up wipe
- `wipe_down` - Down wipe
- More types available via `/get_transition_types`

**Mask Types:**
- `circle` - Circle mask
- `rect` - Rectangle mask
- `linear` - Linear mask
- More types available via `/get_mask_types`

**Example:**

```python
# Add video with fade-in transition
requests.post("http://localhost:9001/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "start": 5,
    "end": 15,
    "target_start": 0,
    "transition": "fade_in",
    "transition_duration": 0.8,
    "volume": 0.7
})
```

---

#### POST /add_audio

Add audio track to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| audio_url | string | Required | Audio URL |
| start | float | 0 | Audio segment start time |
| end | float | None | Audio segment end time |
| target_start | float | 0 | Start time on timeline |
| speed | float | 1.0 | Playback speed |
| volume | float | 1.0 | Volume (0.0-1.0) |
| track_name | string | "audio_main" | Track name |
| duration | float | None | Duration |
| effect_type | string | - | Audio effect type |
| effect_params | list | - | Audio effect parameters |
| width | int | 1080 | Project width |
| height | int | 1920 | Project height |

**Audio Effect Types:**
- Tone effects (Tone_effect_type)
- Scene effects (Audio_scene_effect_type)
- Speech to song (Speech_to_song_type)

---

#### POST /add_image

Add image material to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| image_url | string | Required | Image URL |
| start | float | Required | Start time |
| end | float | Required | End time |
| target_start | float | 0 | Start time on timeline |
| scale_x | float | 1.0 | Horizontal scale |
| scale_y | float | 1.0 | Vertical scale |
| transform_x | float | 0 | Horizontal position offset |
| transform_y | float | 0 | Vertical position offset |
| animation_type | string | - | Animation type |
| transition | string | - | Transition type |
| mask_type | string | - | Mask type |

---

#### POST /add_text

Add text element to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| text | string | Required | Text content |
| start | float | Required | Start time |
| end | float | Required | End time |
| target_start | float | 0 | Start time on timeline |
| font | string | "Noto Sans" | Font name |
| font_size | int | 32 | Font size |
| font_color | string | "#FFFFFF" | Font color (HEX) |
| stroke_enabled | bool | False | Enable stroke |
| stroke_color | string | "#FFFFFF" | Stroke color |
| stroke_width | float | 2.0 | Stroke width |
| stroke_alpha | float | 1.0 | Stroke opacity |
| shadow_enabled | bool | False | Enable shadow |
| shadow_color | string | "#000000" | Shadow color |
| shadow_angle | float | 0 | Shadow angle |
| shadow_distance | float | 0 | Shadow distance |
| shadow_smooth | float | 0 | Shadow smoothness |
| background_color | string | - | Background color |
| background_alpha | float | 1.0 | Background opacity |
| background_round_radius | float | 0 | Background corner radius |
| background_width | float | 0 | Background width |
| background_height | float | 0 | Background height |
| text_intro | string | - | Entrance animation |
| text_outro | string | - | Exit animation |
| is_bold | bool | False | Bold text |
| is_italic | bool | False | Italic text |
| text_styles | array | - | Multi-style text |
| track_name | string | "text" | Track name |
| alignment_h | string | "center" | Horizontal alignment |
| alignment_v | string | "middle" | Vertical alignment |
| pos_x | float | 0 | X position |
| pos_y | float | 0 | Y position |

**Text Animation Types (text_intro/text_outro):**
- `fade_in` / `fade_out` - Fade in/out
- `slide_in_left` / `slide_out_left` - Slide left
- `slide_in_right` / `slide_out_right` - Slide right
- `zoom_in` / `zoom_out` - Zoom
- `rotate_in` / `rotate_out` - Rotate
- More types via `/get_text_intro_types`

**Multi-Style Text Example:**

```python
requests.post("http://localhost:9001/add_text", json={
    "draft_id": draft_id,
    "text": "Colorful Text Effect",
    "start": 2,
    "end": 8,
    "font_size": 42,
    "text_styles": [
        {"start": 0, "end": 2, "font_color": "#FF6B6B"},
        {"start": 2, "end": 4, "font_color": "#4ECDC4"},
        {"start": 4, "end": 6, "font_color": "#45B7D1"}
    ]
})
```

---

#### POST /add_subtitle

Import SRT subtitle file to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| srt_url | string | Required | SRT file URL |
| font | string | "Noto Sans" | Font name |
| font_size | int | 32 | Font size |
| font_color | string | "#FFFFFF" | Font color |
| stroke_enabled | bool | True | Enable stroke |
| stroke_color | string | "#000000" | Stroke color |
| stroke_width | float | 3.0 | Stroke width |
| background_alpha | float | 0.5 | Background opacity |
| pos_y | float | -0.3 | Vertical position |
| time_offset | float | 0 | Time offset (seconds) |

**SRT File Format:**

```srt
1
00:00:00,000 --> 00:00:03,000
First subtitle text

2
00:00:03,000 --> 00:00:06,000
Second subtitle text
```

---

#### POST /add_sticker

Add sticker to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| sticker_id | string | Required | Sticker ID |
| start | float | Required | Start time |
| end | float | Required | End time |
| target_start | float | 0 | Start time on timeline |
| scale_x | float | 1.0 | Horizontal scale |
| scale_y | float | 1.0 | Vertical scale |
| transform_x | float | 0 | Horizontal position offset |
| transform_y | float | 0 | Vertical position offset |
| flip_horizontal | bool | False | Flip horizontal |
| flip_vertical | bool | False | Flip vertical |
| alpha | float | 1.0 | Opacity |

---

#### POST /add_effect

Add video effect to draft.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| effect_type | string | Required | Effect type |
| start | float | Required | Start time |
| end | float | Required | End time |
| target_start | float | 0 | Start time on timeline |
| intensity | float | 1.0 | Effect intensity |
| effect_params | list | - | Effect parameters |

**Effect Type Categories:**
- Scene effects (Video_scene_effect_type)
- Character effects (Video_character_effect_type)

---

#### POST /add_video_keyframe

Add keyframe animation to video track.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| draft_id | string | Required | Draft ID |
| track_name | string | "video_main" | Track name |
| property_types | list | Required | Property type list |
| times | list | Required | Keyframe time points |
| values | list | Required | Corresponding property values |

**Supported Property Types:**
- `scale_x` - Horizontal scale
- `scale_y` - Vertical scale
- `rotation` - Rotation angle
- `alpha` - Opacity
- `transform_x` - Horizontal position
- `transform_y` - Vertical position

**Example:**

```python
# Create scale and opacity animation
requests.post("http://localhost:9001/add_video_keyframe", json={
    "draft_id": draft_id,
    "track_name": "video_main",
    "property_types": ["scale_x", "scale_y", "alpha"],
    "times": [0, 2, 4],
    "values": ["1.0,1.0,1.0", "1.2,1.2,0.8", "0.8,0.8,1.0"]
})
```

---

### Query Interfaces (GET)

#### GET /get_intro_animation_types

Get list of video entrance animation types.

#### GET /get_outro_animation_types

Get list of video exit animation types.

#### GET /get_combo_animation_types

Get list of combo animation types.

#### GET /get_transition_types

Get list of transition effect types.

#### GET /get_mask_types

Get list of mask types.

#### GET /get_audio_effect_types

Get list of audio effect types.

#### GET /get_font_types

Get list of font types.

#### GET /get_text_intro_types

Get list of text entrance animations.

#### GET /get_text_outro_types

Get list of text exit animations.

#### GET /get_text_loop_anim_types

Get list of text loop animations.

#### GET /get_video_scene_effect_types

Get list of scene effect types.

#### GET /get_video_character_effect_types

Get list of character effect types.

---

### File Upload

#### POST /upload_video

Upload video file to server.

#### POST /upload_image

Upload image file to server.

#### GET /list_uploads

List uploaded files.

#### DELETE /delete_upload/<filename>

Delete specified uploaded file.

---

### Advanced Features

#### POST /get_duration

Get media file duration.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| media_url | string | Yes | Media URL |

#### POST /export_to_capcut

Export draft to CapCut.

#### POST /export_draft_to_video

Export draft as video file.

#### GET /export_status

Query export status.

#### POST /execute_workflow

Execute predefined workflow.

---

## Error Response

All API endpoints return unified format on error:

```json
{
  "success": false,
  "output": "",
  "error": "Error description"
}
```

Common Errors:
- Missing required parameters
- Invalid video/audio URL
- Draft ID does not exist
- Unsupported file format
