# VectCutAPI — Tài liệu Khả năng API

> Tài liệu tham chiếu dành cho AI: mô tả đầy đủ các API, tham số, và khả năng của hệ thống chỉnh sửa video CapCut tự động.

---

## Mục lục

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [API Chính — Thao tác Draft](#2-api-chính--thao-tác-draft)
3. [API Thêm nội dung (Media)](#3-api-thêm-nội-dung-media)
4. [API Text & Subtitle](#4-api-text--subtitle)
5. [API Effect & Sticker](#5-api-effect--sticker)
6. [API Keyframe Animation](#6-api-keyframe-animation)
7. [API Tiện ích (Utility)](#7-api-tiện-ích-utility)
8. [API Template System](#8-api-template-system)
9. [API Query — Truy vấn metadata](#9-api-query--truy-vấn-metadata)
10. [Danh sách Transition](#10-danh-sách-transition)
11. [Danh sách Animation](#11-danh-sách-animation)
12. [Danh sách Mask](#12-danh-sách-mask)
13. [Danh sách Audio Effect](#13-danh-sách-audio-effect)
14. [Danh sách Video Effect](#14-danh-sách-video-effect)
15. [Quy trình làm việc mẫu](#15-quy-trình-làm-việc-mẫu)

---

## 1. Tổng quan hệ thống

### Hai giao thức truy cập

| Giao thức | File | Mô tả |
|-----------|------|--------|
| **REST API** (Flask) | `capcut_server.py` | HTTP JSON endpoints, cổng mặc định `9001` |
| **MCP Server** (stdio JSON-RPC) | `mcp_server.py` | Model Context Protocol cho AI agents |

### Môi trường

Hệ thống chạy với cấu hình `is_capcut_env = true` — dùng metadata CapCut (tên tiếng Anh).

### Luồng hoạt động cơ bản

```
create_draft → add_video/add_image/add_audio/add_text/... → add_keyframe (tuỳ chọn) → save_draft
```

Mỗi thao tác trả về `draft_id` để sử dụng cho các bước tiếp theo. Khi không truyền `draft_id`, hệ thống tự tạo draft mới.

---

## 2. API Chính — Thao tác Draft

### `create_draft` — Tạo draft mới

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |

**Trả về:** `{ draft_id, draft_url }`

**Kích thước canvas phổ biến:**
- `1080×1920` — Dọc (TikTok, Reels, Shorts)
- `1920×1080` — Ngang (YouTube, TV)
- `1080×1080` — Vuông (Instagram)

---

### `save_draft` — Lưu draft

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `draft_id` | string | bắt buộc | ID draft cần lưu |
| `draft_folder` | string | từ config | Thư mục lưu draft |

**Trả về:** `{ draft_url }`

---

### `query_script` — Truy vấn nội dung draft (REST only)

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `draft_id` | string | bắt buộc | ID draft |
| `force_update` | bool | true | Buộc cập nhật cache |

---

### `query_draft_status` — Kiểm tra trạng thái task (REST only)

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `task_id` | string | bắt buộc | ID task từ save_draft |

---

### `generate_draft_url` — Tạo URL xem trước (REST only)

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `draft_id` | string | bắt buộc | ID draft |

---

## 3. API Thêm nội dung (Media)

### `add_video` — Thêm video vào draft

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `video_url` | string | **bắt buộc** | URL video nguồn |
| `draft_id` | string | null | ID draft (null = tạo mới) |
| `start` | float | 0 | Thời điểm bắt đầu cắt trong video nguồn (giây) |
| `end` | float | 0 | Thời điểm kết thúc cắt trong video nguồn (giây) |
| `target_start` | float | 0 | Vị trí đặt trên timeline (giây) |
| `duration` | float | null | Thời lượng hiển thị (giây) |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |
| `transform_x` | float | 0 | Vị trí X (0 = giữa) |
| `transform_y` | float | 0 | Vị trí Y (0 = giữa) |
| `scale_x` | float | 1 | Tỉ lệ phóng X |
| `scale_y` | float | 1 | Tỉ lệ phóng Y |
| `speed` | float | 1.0 | Tốc độ phát (0.1–100) |
| `volume` | float | 1.0 | Âm lượng (0–1) |
| `track_name` | string | "video_main" | Tên track |
| `relative_index` | int | 0 | Thứ tự render layer |
| `transition` | string | null | Loại chuyển cảnh (xem mục 10) |
| `transition_duration` | float | 0.5 | Thời lượng chuyển cảnh (giây) |
| `mask_type` | string | null | Loại mask (xem mục 12) |
| `mask_center_x` | float | 0.5 | Tâm mask X |
| `mask_center_y` | float | 0.5 | Tâm mask Y |
| `mask_size` | float | 1.0 | Kích thước mask (tỉ lệ canvas) |
| `mask_rotation` | float | 0 | Góc xoay mask |
| `mask_feather` | float | 0 | Độ mờ viền mask |
| `mask_invert` | bool | false | Đảo ngược mask |
| `mask_rect_width` | float | null | Chiều rộng mask chữ nhật |
| `mask_round_corner` | float | null | Bo góc mask chữ nhật |
| `background_blur` | int | null | Mức blur nền: 1 (nhẹ), 2 (vừa), 3 (mạnh), 4 (tối đa) |

---

### `add_audio` — Thêm âm thanh

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `audio_url` | string | **bắt buộc** | URL file âm thanh |
| `draft_id` | string | null | ID draft |
| `start` | float | 0 | Thời điểm bắt đầu cắt (giây) |
| `end` | float | null | Thời điểm kết thúc cắt (giây) |
| `target_start` | float | 0 | Vị trí trên timeline (giây) |
| `duration` | float | null | Thời lượng (giây) |
| `volume` | float | 1.0 | Âm lượng |
| `speed` | float | 1.0 | Tốc độ phát |
| `track_name` | string | "audio_main" | Tên track |
| `effect_type` | string | null | Loại audio effect (xem mục 13) |
| `effect_params` | array | null | Danh sách tham số effect |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |

---

### `add_image` — Thêm hình ảnh

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `image_url` | string | **bắt buộc** | URL hình ảnh |
| `draft_id` | string | null | ID draft |
| `start` | float | 0 | Thời điểm bắt đầu (giây) |
| `end` | float | 3.0 | Thời điểm kết thúc (giây) |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |
| `transform_x` | float | 0 | Vị trí X |
| `transform_y` | float | 0 | Vị trí Y |
| `scale_x` | float | 1 | Tỉ lệ phóng X |
| `scale_y` | float | 1 | Tỉ lệ phóng Y |
| `track_name` | string | "image_main" | Tên track |
| `relative_index` | int | 0 | Thứ tự render layer |
| `intro_animation` | string | null | Animation xuất hiện (xem mục 11) |
| `intro_animation_duration` | float | 0.5 | Thời lượng anim xuất hiện |
| `outro_animation` | string | null | Animation biến mất |
| `outro_animation_duration` | float | 0.5 | Thời lượng anim biến mất |
| `combo_animation` | string | null | Animation combo (xuyên suốt) |
| `combo_animation_duration` | float | 0.5 | Thời lượng anim combo |
| `transition` | string | null | Loại chuyển cảnh (xem mục 10) |
| `transition_duration` | float | 0.5 | Thời lượng chuyển cảnh |
| `mask_type` | string | null | Loại mask (xem mục 12) |
| `mask_center_x` | float | 0.0 | Tâm mask X |
| `mask_center_y` | float | 0.0 | Tâm mask Y |
| `mask_size` | float | 0.5 | Kích thước mask |
| `mask_rotation` | float | 0.0 | Góc xoay mask |
| `mask_feather` | float | 0.0 | Độ mờ viền mask |
| `mask_invert` | bool | false | Đảo mask |
| `mask_rect_width` | float | null | Chiều rộng mask chữ nhật |
| `mask_round_corner` | float | null | Bo góc |
| `background_blur` | int | null | Blur nền (1–4) |

---

## 4. API Text & Subtitle

### `add_text` — Thêm text

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `text` | string | **bắt buộc** | Nội dung text |
| `start` | float | **bắt buộc** | Thời điểm bắt đầu (giây) |
| `end` | float | **bắt buộc** | Thời điểm kết thúc (giây) |
| `draft_id` | string | null | ID draft |
| `font` | string | auto (theo locale) | Tên font (xem GET /get_font_types) |
| `font_color` | string | "#FF0000" | Màu chữ (hex) |
| `font_size` | float | 8.0 | Cỡ chữ |
| `font_alpha` | float | 1.0 | Độ trong suốt chữ |
| `transform_x` | float | 0 | Vị trí X |
| `transform_y` | float | 0 | Vị trí Y |
| `vertical` | bool | false | Hiển thị chữ dọc |
| `track_name` | string | "text_main" | Tên track |
| `fixed_width` | int | -1 | Chiều rộng cố định (-1 = tự động) |
| `fixed_height` | int | -1 | Chiều cao cố định (-1 = tự động) |
| **Viền (Border)** | | | |
| `border_width` | float | 0.0 | Độ dày viền |
| `border_color` | string | "#000000" | Màu viền |
| `border_alpha` | float | 1.0 | Độ trong suốt viền |
| **Nền chữ (Background)** | | | |
| `background_color` | string | "#000000" | Màu nền |
| `background_alpha` | float | 0.0 | Độ trong suốt nền (0 = tắt) |
| `background_style` | int | 0 | Kiểu nền |
| `background_round_radius` | float | 0.0 | Bo góc nền |
| `background_height` | float | 0.14 | Chiều cao nền (0–1) |
| `background_width` | float | 0.14 | Chiều rộng nền (0–1) |
| `background_horizontal_offset` | float | 0.5 | Offset ngang nền (0–1) |
| `background_vertical_offset` | float | 0.5 | Offset dọc nền (0–1) |
| **Bóng đổ (Shadow)** | | | |
| `shadow_enabled` | bool | false | Bật bóng đổ |
| `shadow_color` | string | "#000000" | Màu bóng |
| `shadow_alpha` | float | 0.9 | Độ trong suốt bóng |
| `shadow_angle` | float | -45.0 | Góc bóng (-180 → 180) |
| `shadow_distance` | float | 5.0 | Khoảng cách bóng |
| `shadow_smoothing` | float | 0.15 | Độ mịn bóng (0–1) |
| **Hiệu ứng trang trí** | | | |
| `bubble_effect_id` | string | null | ID bubble text |
| `bubble_resource_id` | string | null | ID resource bubble |
| `effect_effect_id` | string | null | ID hiệu ứng chữ |
| **Animation** | | | |
| `intro_animation` | string | null | Animation xuất hiện |
| `intro_duration` | float | 0.5 | Thời lượng intro |
| `outro_animation` | string | null | Animation biến mất |
| `outro_duration` | float | 0.5 | Thời lượng outro |
| **Multi-style text** | | | |
| `text_styles` | array | [] | Danh sách style cho từng đoạn text |

#### Cấu trúc `text_styles` (Multi-style):
```json
[
  {
    "start": 0,
    "end": 5,
    "font": "Arial",
    "style": {
      "size": 10,
      "bold": true,
      "italic": false,
      "underline": false,
      "color": "#FF0000",
      "alpha": 1.0,
      "align": 1,
      "vertical": false,
      "letter_spacing": 0,
      "line_spacing": 0
    },
    "border": {
      "width": 2.0,
      "color": "#000000",
      "alpha": 1.0
    }
  }
]
```

---

### `add_subtitle` — Thêm phụ đề từ SRT

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `srt_path` / `srt` | string | **bắt buộc** | Đường dẫn file SRT hoặc URL |
| `draft_id` | string | null | ID draft |
| `track_name` | string | "subtitle" | Tên track |
| `time_offset` | float | 0 | Dịch thời gian phụ đề (giây) |
| `font` | string | auto | Tên font |
| `font_size` | float | 5.0–8.0 | Cỡ chữ |
| `font_color` | string | "#FFFFFF" | Màu chữ |
| `bold` | bool | false | In đậm |
| `italic` | bool | false | In nghiêng |
| `underline` | bool | false | Gạch chân |
| `vertical` | bool | false | Chữ dọc |
| `alpha` | float | 1 | Độ trong suốt |
| `border_width` | float | 0.0 | Độ dày viền |
| `border_color` | string | "#000000" | Màu viền |
| `border_alpha` | float | 1.0 | Độ trong suốt viền |
| `background_color` | string | "#000000" | Màu nền |
| `background_alpha` | float | 0.0 | Độ trong suốt nền |
| `background_style` | int | 0 | Kiểu nền |
| `transform_x` | float | 0.0 | Vị trí X |
| `transform_y` | float | -0.8 | Vị trí Y (mặc định gần cuối màn hình) |
| `scale_x` | float | 1.0 | Tỉ lệ phóng X |
| `scale_y` | float | 1.0 | Tỉ lệ phóng Y |
| `rotation` | float | 0.0 | Góc xoay |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |

---

## 5. API Effect & Sticker

### `add_effect` — Thêm hiệu ứng video

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `effect_type` | string | **bắt buộc** | Tên hiệu ứng (xem mục 14) |
| `effect_category` | string | "scene" | Loại: `"scene"` hoặc `"character"` |
| `start` | float | 0 | Thời điểm bắt đầu (giây) |
| `end` | float | 3.0 | Thời điểm kết thúc (giây) |
| `draft_id` | string | null | ID draft |
| `track_name` | string | "effect_01" | Tên track effect |
| `params` | array | null | Danh sách tham số effect (mỗi effect có params riêng) |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |

---

### `add_sticker` — Thêm sticker

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `resource_id` / `sticker_id` | string | **bắt buộc** | ID sticker resource |
| `start` | float | 0 | Thời điểm bắt đầu (giây) |
| `end` | float | 5.0 | Thời điểm kết thúc (giây) |
| `draft_id` | string | null | ID draft |
| `transform_x` | float | 0 | Vị trí X |
| `transform_y` | float | 0 | Vị trí Y |
| `scale_x` | float | 1.0 | Tỉ lệ phóng X |
| `scale_y` | float | 1.0 | Tỉ lệ phóng Y |
| `alpha` | float | 1.0 | Độ trong suốt |
| `rotation` | float | 0.0 | Góc xoay |
| `flip_horizontal` | bool | false | Lật ngang |
| `flip_vertical` | bool | false | Lật dọc |
| `track_name` | string | "sticker_main" | Tên track |
| `relative_index` | int | 0 | Thứ tự render |
| `width` | int | 1080 | Chiều rộng canvas |
| `height` | int | 1920 | Chiều cao canvas |

---

## 6. API Keyframe Animation

### `add_video_keyframe` — Thêm keyframe cho animation

Hỗ trợ **chế độ đơn** (1 keyframe) và **chế độ batch** (nhiều keyframe cùng lúc).

#### Chế độ đơn:

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `draft_id` | string | null | ID draft |
| `track_name` | string | "main" | Tên track chứa segment |
| `property_type` | string | "alpha" | Thuộc tính keyframe (xem bảng dưới) |
| `time` | float | 0.0 | Thời điểm keyframe (giây) |
| `value` | string | "1.0" | Giá trị keyframe |

#### Chế độ batch:

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `property_types` | array[string] | Danh sách thuộc tính |
| `times` | array[float] | Danh sách thời điểm |
| `values` | array[string] | Danh sách giá trị |

> Ba mảng phải cùng độ dài. Khi truyền batch, các tham số đơn bị bỏ qua.

#### Bảng `property_type` và định dạng `value`:

| property_type | Phạm vi | Ví dụ value | Mô tả |
|---------------|---------|-------------|-------|
| `position_x` | [-1, 1] | `"0"` (giữa), `"0.5"` (phải) | Vị trí ngang |
| `position_y` | [-1, 1] | `"0"` (giữa), `"-0.5"` (trên) | Vị trí dọc |
| `rotation` | bất kỳ | `"45deg"` | Xoay (độ, theo chiều kim đồng hồ) |
| `scale_x` | > 0 | `"1.5"` | Phóng to X (loại trừ uniform_scale) |
| `scale_y` | > 0 | `"1.5"` | Phóng to Y (loại trừ uniform_scale) |
| `uniform_scale` | > 0 | `"1.2"` | Phóng to đều (loại trừ scale_x/y) |
| `alpha` | [0, 1] | `"50%"` hoặc `"0.5"` | Độ trong suốt |
| `saturation` | [-1, 1] | `"+0.5"`, `"-0.3"` | Độ bão hoà |
| `contrast` | [-1, 1] | `"+0.5"`, `"-0.3"` | Độ tương phản |
| `brightness` | [-1, 1] | `"+0.5"`, `"-0.3"` | Độ sáng |
| `volume` | ≥ 0 | `"80%"` | Âm lượng |

#### Ví dụ: Tạo hiệu ứng zoom-in từ 1x lên 1.3x trong 3 giây

```json
{
  "draft_id": "xxx",
  "track_name": "video_main",
  "property_types": ["uniform_scale", "uniform_scale"],
  "times": [0.0, 3.0],
  "values": ["1.0", "1.3"]
}
```

---

## 7. API Tiện ích (Utility)

### `get_video_duration` — Lấy thời lượng video

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `video_url` | string | URL video |

**Trả về:** `{ duration: float }` (giây)

> Sử dụng `ffprobe`, hỗ trợ retry 3 lần với timeout 10 giây.

---

## 8. API Template System

### `list_templates` — Liệt kê template có sẵn

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `detailed` | bool | false | Trả về chi tiết layer cho mỗi template |

---

### `render_template` — Render video từ template

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `template_name` | string | **bắt buộc** | Tên template (ví dụ: "podcast-video-v1") |
| `segments` | array | **bắt buộc** | Danh sách segment nội dung |
| `logo_url` | string | null | URL logo (hiển thị xuyên suốt) |
| `play_icon_url` | string | null | URL icon play |
| `overlay_url` | string | null | URL overlay tối |

#### Cấu trúc mỗi segment:

```json
{
  "text": "Nội dung text chính",
  "duration": 5.0,
  "image_url": "https://...",
  "title": "Tiêu đề (tuỳ chọn)"
}
```

#### 3 loại layer trong template:

| Layer type | Mô tả |
|-----------|--------|
| `persistent_image` | Hiển thị xuyên suốt video (logo, play icon, overlay) |
| `dynamic_image` | Slideshow ảnh thay đổi theo segment |
| `dynamic_text` | Text thay đổi theo segment |

**Trả về:**
```json
{
  "success": true,
  "draft_id": "...",
  "total_duration": 30.0,
  "segment_count": 6,
  "layers_rendered": ["background", "overlay", "script_text", "logo"]
}
```

---

### `analyze_draft` — Phân tích cấu trúc draft

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `draft_path` | string | Đường dẫn thư mục draft |
| `draft_name` | string | Tên thư mục draft (thay thế draft_path) |

**Trả về:** Danh sách track với thuộc tính: name, type, segment_count, duration, transform, scale, font, transition, suggested_role.

---

### `export_draft_template` — Xuất draft thành template tái sử dụng

| Tham số | Kiểu | Mặc định | Mô tả |
|---------|------|----------|-------|
| `template_name` | string | **bắt buộc** | Tên template xuất ra |
| `draft_path` | string | null | Đường dẫn thư mục draft |
| `draft_name` | string | null | Tên thư mục draft |
| `track_roles` | object | {} | Map track → role |
| `auto_detect` | bool | false | Tự phát hiện role dựa theo tên track |

#### Các role hỗ trợ:

| Role | Layer type | Mô tả |
|------|-----------|--------|
| `background` | dynamic_image | Ảnh nền slideshow (thay đổi theo segment) |
| `overlay` | persistent_image | Overlay phủ lên background (xuyên suốt video) |
| `script_text` | dynamic_text | Text script (thay đổi theo segment) |
| `title_text` | dynamic_text | Tiêu đề (thay đổi, tuỳ chọn) |
| `logo` | persistent_image | Logo (xuyên suốt video) |
| `play_icon` | persistent_image | Icon play (xuyên suốt video) |
| `watermark` | persistent_image | Watermark (xuyên suốt video) |
| `skip` | — | Bỏ qua, không export |

#### Quy ước tên track tự động detect:

> ⚠️ **Lưu ý thực tế:** Giao diện CapCut hiện tại **không có chức năng đổi tên track**, nên tên track mặc định thường là `Video_1`, `Text_1`... — **`auto_detect=true` sẽ không hoạt động trong phần lớn trường hợp.**
>
> **Cách đáng tin cậy hơn:** Chạy `analyze_draft` trước để xem danh sách track theo index, rồi gán `track_roles` bằng số index (ví dụ: `{"0": "background", "1": "logo", "2": "script_text"}`).

Bảng dưới chỉ áp dụng nếu bạn tự đặt tên track theo convention (ví dụ qua JianYing hoặc chỉnh `draft_info.json` thủ công):

| Keyword trong tên track | Role auto-detect |
|------------------------|-----------------|
| `logo` | logo |
| `play` | play_icon |
| `watermark` | watermark |
| `overlay` | overlay |
| `bg`, `background` | background |
| `title` | title_text |
| `script`, `text`, `sub` | script_text |

---

## 9. API Query — Truy vấn metadata (REST GET endpoints)

Các endpoint trả về danh sách giá trị hợp lệ cho từng thuộc tính. Kết quả phụ thuộc biến `is_capcut_env`.

| Endpoint | Mô tả |
|----------|--------|
| `GET /get_intro_animation_types` | Danh sách animation xuất hiện (video/image) |
| `GET /get_outro_animation_types` | Danh sách animation biến mất (video/image) |
| `GET /get_combo_animation_types` | Danh sách animation combo/group |
| `GET /get_transition_types` | Danh sách chuyển cảnh |
| `GET /get_mask_types` | Danh sách mask |
| `GET /get_audio_effect_types` | Danh sách audio effect (kèm params min/max/default) |
| `GET /get_font_types` | Danh sách font |
| `GET /get_text_intro_types` | Danh sách animation text xuất hiện |
| `GET /get_text_outro_types` | Danh sách animation text biến mất |
| `GET /get_text_loop_anim_types` | Danh sách animation text lặp liên tục |
| `GET /get_video_scene_effect_types` | Danh sách hiệu ứng scene |
| `GET /get_video_character_effect_types` | Danh sách hiệu ứng character |

---

## 10. Danh sách Transition

> Dùng cho tham số `transition` trong add_video, add_image.

**101 loại transition:** Anti-CW Swirl, Axis Rotation, B&W Flash, Black Fade, Black smoke, Blanch, Blink, Blocks, Blue Lines, Blur, Blurred Highlight, Bottom Left II, Burn, CW Swirl, Camera Glow, Cartoon Swirl, Circular Slices II, Clock wipe, Cloud, Color Glitch, Color Swirl, Cube, Curling Wave, Cutout Flip, Diagonal Slices, Dissolve, Dissolve II, Dissolve III, Distortion, Dots Right, Flame, Flash, Flip, Flip II, Fold Over, Glitch, Gradient Wipe, Horizontal Blur, Horizontal Lines, Horizontal Slice, Inhale, Left, Light Beam, Light Sweep II, Lightning, Like, Little Devil, Mix, Montage Snippets, Mosaic, Open, Open Horizontally, Open Vertically, Page Turning, Particles, Pull Out, Pull in, RGB Glitch, Radial Blur, Rainbow Filter, Rainbow Warp, Recorder, Right, Rotate CCW II, Rotate CW II, Shake 3, Shutter, Shutter II, Slide, Snow, Split, Split III, Split IV, Squeeze, Stretch, Stretch Left, Stretch Right, Stretch ll, Strobe, Super Like, Switch, Then and Now, Transform Shimmer, Twinkle Zoom, Up, Urban Glitch, Vertical Blur, Vertical Blur II, Vertical Slices, Vintage Screening, Wave Left, Wave Right, Whirlpool, White Flash, White Ink, White smoke, Windmill, Wipe Left, Wipe Right, Wipe Up, Woosh

---

## 11. Danh sách Animation

### 11.1 Video/Image Intro Animation (60+ loại)

> Dùng cho `intro_animation` trong add_image và animation xuất hiện video.

### 11.2 Video/Image Outro Animation (15+ loại)

> Dùng cho `outro_animation` trong add_image.

### 11.3 Group/Combo Animation (100+ loại)

> Dùng cho `combo_animation` trong add_image.

### 11.4 Text Intro Animation (70+ loại)

> Dùng cho `intro_animation` trong add_text.

Ví dụ: Fade In, Zoom In, Slide In, Bounce In, Flip In, Rotate In, Typewriter, Scale Up, Spin In, Pop Up, Wave in, Glitch, Spiral, Dissolve, Float Down, Blur, Wipe, Karaoke, Flicker, Flutter, Wobble...

### 11.5 Text Outro Animation (70+ loại)

> Dùng cho `outro_animation` trong add_text.

Ví dụ: Fade Out, Zoom Out, Slide Out, Bounce Out, Flip Out, Rotate Out, Scale Down, Spin Out, Slide Down, Wipe, Blur, Roll Out, Pop Down...

### 11.6 Text Loop Animation (40+ loại)

> Animation lặp liên tục trên text.

Ví dụ: Blink, Swing, Bounce, Pulse, Glow, Shake, Wave, Rotate, Scale, Flash, Jiggly, Wobble, Dance, Jump, VHS, Space Type, Scroll Up...

> **Lưu ý:** Sử dụng các GET endpoint ở mục 9 để lấy danh sách đầy đủ.

---

## 12. Danh sách Mask

> Dùng cho tham số `mask_type` trong add_video, add_image.

| Mask | Mô tả |
|------|--------|
| **Linear** | Mask đường thẳng |
| **Mirror** | Mask gương |
| **Circle** | Mask hình tròn |
| **Rectangle** | Mask chữ nhật (có thêm `mask_rect_width`, `mask_round_corner`) |
| **Heart** | Mask hình trái tim |
| **Star** | Mask hình ngôi sao |
| **Split** | Mask chia đôi |
| **Filmstrip** | Mask dải phim |
| **Text** | Mask chữ |
| **Brush** | Mask cọ vẽ |
| **Pen** | Mask bút vẽ |

**Thuộc tính chung:** `mask_center_x/y`, `mask_size`, `mask_rotation`, `mask_feather`, `mask_invert`

---

## 13. Danh sách Audio Effect

> Dùng cho `effect_type` trong add_audio.

| Loại | Ví dụ |
|------|-------|
| **Voice Filters** | Big House, Low, Energetic, High, Low Battery, Tremble, Electronic, Sweet, Vinyl, Mic Hog, Lo-Fi, Megaphone, Echo, Synth, Deep |
| **Voice Characters** | Fussy male, Bestie, Queen, Squirrel, Distorted, Chipmunk, Trickster, Elf, Santa, Jessie, Robot |
| **Speech to Song** | Folk |

Mỗi effect có danh sách `params` với `name`, `default_value`, `min_value`, `max_value`.

---

## 14. Danh sách Video Effect

> Dùng cho `effect_type` trong add_effect.

### Hai loại:

| effect_category | Mô tả | Ví dụ |
|----------------|--------|-------|
| `"scene"` | Hiệu ứng toàn cảnh | 1998, 70s, DV录制框, VCR, RGB描边, X-Signal, emoji钻石, ins界面... (100+ loại) |
| `"character"` | Hiệu ứng nhân vật | Các effect áp dụng lên đối tượng/nhân vật cụ thể |

Mỗi effect có tham số tuỳ chỉnh: filter, blur, sharpen, distortion, texture, speed, color, intensity, size, rotation, chromatic aberration...

> Sử dụng `GET /get_video_scene_effect_types` và `GET /get_video_character_effect_types` để lấy danh sách đầy đủ.

---

## 15. Quy trình làm việc mẫu

### A. Tạo video đơn giản với nhạc nền + text

```
1. create_draft(width=1080, height=1920)                    → draft_id
2. add_video(video_url="...", draft_id=draft_id)
3. add_audio(audio_url="...", draft_id=draft_id, volume=0.3)
4. add_text(text="Tiêu đề", start=0, end=3, draft_id=draft_id, font_size=15)
5. save_draft(draft_id=draft_id)
```

### B. Tạo slideshow ảnh với chuyển cảnh

```
1. create_draft(width=1080, height=1920)                    → draft_id
2. add_image(image_url="1.jpg", start=0, end=3, transition="Dissolve", draft_id=draft_id, track_name="main")
3. add_image(image_url="2.jpg", start=3, end=6, transition="Blur", draft_id=draft_id, track_name="main")
4. add_image(image_url="3.jpg", start=6, end=9, transition="Fade", draft_id=draft_id, track_name="main")
5. add_audio(audio_url="bgm.mp3", draft_id=draft_id)
6. add_subtitle(srt_path="sub.srt", draft_id=draft_id)
7. save_draft(draft_id=draft_id)
```

### C. Tạo video từ template podcast

```
1. list_templates()                                          → danh sách template
2. render_template(
     template_name="podcast-video-v1",
     segments=[
       {"text": "Đoạn 1...", "duration": 5, "image_url": "bg1.jpg"},
       {"text": "Đoạn 2...", "duration": 4, "image_url": "bg2.jpg"}
     ],
     logo_url="logo.png"
   )
```

### D. Tạo hiệu ứng zoom-in trên ảnh

```
1. create_draft()                                            → draft_id
2. add_image(image_url="photo.jpg", start=0, end=5, track_name="main", draft_id=draft_id)
3. add_video_keyframe(
     draft_id=draft_id, track_name="main",
     property_types=["uniform_scale", "uniform_scale"],
     times=[0.01, 4.99],
     values=["1.0", "1.3"]
   )
4. save_draft(draft_id=draft_id)
```

### E. Export draft CapCut thành template

```
1. analyze_draft(draft_name="MyProject")                     → danh sách tracks + suggested_role
2. export_draft_template(
     draft_name="MyProject",
     template_name="my-template-v1",
     track_roles={"0": "background", "1": "logo", "2": "script_text"}
   )
3. render_template(template_name="my-template-v1", segments=[...])
```

---

## Tóm tắt nhanh khả năng

| Khả năng | Hỗ trợ |
|----------|--------|
| Thêm video với cắt/tốc độ/âm lượng | ✅ |
| Thêm ảnh với animation intro/outro/combo | ✅ |
| Thêm âm thanh với hiệu ứng giọng nói | ✅ |
| Thêm text với multi-style/shadow/background/border | ✅ |
| Thêm phụ đề SRT tự động | ✅ |
| Chuyển cảnh (101 loại) | ✅ |
| Mask (10+ loại, tuỳ chỉnh vị trí/kích thước/feather/invert) | ✅ |
| Background blur (4 mức) | ✅ |
| Keyframe animation (position/scale/rotation/alpha/color) | ✅ Đơn + Batch |
| Hiệu ứng video scene + character (100+ loại) | ✅ |
| Hiệu ứng âm thanh (30+ loại) | ✅ |
| Sticker | ✅ |
| Template system (render/analyze/export) | ✅ |
| Multi-track composition (nhiều layer đồng thời) | ✅ |
| Lấy thời lượng video (ffprobe) | ✅ |
| Hỗ trợ CapCut (quốc tế) | ✅ |
