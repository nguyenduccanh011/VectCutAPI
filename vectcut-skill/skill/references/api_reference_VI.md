# Tham Chiếu API VectCutAPI Hoàn Chỉnh

## Các Điểm Cuối HTTP API

### Các Thao Tác Cơ Bản

#### POST /create_draft

Tạo dự án bản nháp video mới.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|------|
| width | int | Không | Chiều rộng video, mặc định 1080 |
| height | int | Không | Chiều cao video, mặc định 1920 |
| draft_folder | string | Không | Đường dẫn thư mục bản nháp |

**Độ Phân Giải Phổ Biến:**
- `1080 x 1920` - Dọc (Video ngắn/TikTok)
- `1920 x 1080` - Ngang (YouTube)
- `1080 x 1080` - Hình vuông (Instagram)

**Ví Dụ Phản Hồi:**

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

Lưu dự án bản nháp và tạo liên kết tải xuống.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|------|
| draft_id | string | Có | ID bản nháp |
| draft_folder | string | Không | Đường dẫn thư mục bản nháp |

**Ví Dụ Phản Hồi:**

```json
{
  "success": true,
  "output": {
    "draft_url": "https://example.com/draft/downloader?id=xxx",
    "draft_folder": "dfd_xxxxx",
    "message": "Bản nháp đã lưu"
  }
}
```

---

#### POST /query_draft_status

Truy vấn trạng thái bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|------|
| draft_id | string | Có | ID bản nháp |

---

#### POST /query_script

Truy vấn nội dung tập lệnh bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|------|
| draft_id | string | Có | ID bản nháp |

---

### Thêm Tài Liệu Tham Khảo

#### POST /add_video

Thêm rãnh video vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| video_url | string | Bắt buộc | URL video (cục bộ hoặc từ xa) |
| start | float | 0 | Thời gian bắt đầu clip video (giây) |
| end | float | 0 | Thời gian kết thúc clip video (giây) |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| speed | float | 1.0 | Tốc độ phát lại |
| volume | float | 1.0 | Âm lượng (0.0-1.0) |
| scale_x | float | 1.0 | Thu phóng ngang |
| scale_y | float | 1.0 | Thu phóng dọc |
| transform_x | float | 0 | Dịch chuyển vị trí ngang |
| transform_y | float | 0 | Dịch chuyển vị trí dọc |
| track_name | string | "video_main" | Tên rãnh |
| relative_index | int | 0 | Chỉ số tương đối |
| duration | float | - | Thời lượng |
| transition | string | - | Kiểu hiệu ứng chuyển tiếp |
| transition_duration | float | 0.5 | Độ dài hiệu ứng chuyển tiếp (giây) |
| mask_type | string | - | Kiểu mặt nạ |
| mask_center_x | float | 0.5 | Tâm mặt nạ X |
| mask_center_y | float | 0.5 | Tâm mặt nạ Y |
| mask_size | float | 1.0 | Kích thước mặt nạ |
| mask_rotation | float | 0.0 | Góc quay mặt nạ |
| mask_feather | float | 0.0 | Độ mềm mịn mặt nạ |
| mask_invert | bool | False | Có đảo ngược mặt nạ không |
| background_blur | int | - | Mức mờ nền (1-4) |

**Hình Thức Hiệu Ứng Chuyển Tiếp (transition):**
- `fade_in` - Mờ dần vào
- `fade_out` - Mờ dần ra
- `wipe_left` - Quét trái
- `wipe_right` - Quét phải
- `wipe_up` - Quét lên
- `wipe_down` - Quét xuống
- Xem thêm `GET /get_transition_types`

**Hình Thức Mặt Nạ (mask_type):**
- `circle` - Mặt nạ tròn
- `rect` - Mặt nạ hình chữ nhật
- `linear` - Mặt nạ tuyến tính
- Xem thêm `GET /get_mask_types`

**Ví Dụ:**

```python
# Thêm video với hiệu ứng chuyển tiếp mờ dần vào
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

Thêm rãnh âm thanh vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| audio_url | string | Bắt buộc | URL âm thanh |
| start | float | 0 | Thời gian bắt đầu clip âm thanh |
| end | float | Không | Thời gian kết thúc clip âm thanh |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| speed | float | 1.0 | Tốc độ phát lại |
| volume | float | 1.0 | Âm lượng (0.0-1.0) |
| track_name | string | "audio_main" | Tên rãnh |
| duration | float | Không | Thời lượng |
| effect_type | string | - | Kiểu hiệu ứng âm thanh |
| effect_params | list | - | Tham số hiệu ứng âm thanh |
| width | int | 1080 | Chiều rộng dự án |
| height | int | 1920 | Chiều cao dự án |

**Kiểu Hiệu Ứng Âm Thanh:**
- Hiệu ứng tone (Tone_effect_type)
- Hiệu ứng cảnh (Audio_scene_effect_type)
- Giọng nói thành bài hát (Speech_to_song_type)

---

#### POST /add_image

Thêm tài liệu hình ảnh vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| image_url | string | Bắt buộc | URL hình ảnh |
| start | float | Bắt buộc | Thời gian bắt đầu |
| end | float | Bắt buộc | Thời gian kết thúc |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| scale_x | float | 1.0 | Thu phóng ngang |
| scale_y | float | 1.0 | Thu phóng dọc |
| transform_x | float | 0 | Dịch chuyển vị trí ngang |
| transform_y | float | 0 | Dịch chuyển vị trí dọc |
| animation_type | string | - | Kiểu hoạt ảnh |
| transition | string | - | Kiểu hiệu ứng chuyển tiếp |
| mask_type | string | - | Kiểu mặt nạ |

---

#### POST /add_text

Thêm phần tử văn bản vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| text | string | Bắt buộc | Nội dung văn bản |
| start | float | Bắt buộc | Thời gian bắt đầu |
| end | float | Bắt buộc | Thời gian kết thúc |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| font | string | "Noto Sans CJK" | Tên phông chữ |
| font_size | int | 32 | Kích thước phông chữ |
| font_color | string | "#FFFFFF" | Màu phông chữ (HEX) |
| stroke_enabled | bool | False | Có bật mô tả không |
| stroke_color | string | "#FFFFFF" | Màu mô tả |
| stroke_width | float | 2.0 | Độ rộng mô tả |
| stroke_alpha | float | 1.0 | Độ trong suốt mô tả |
| shadow_enabled | bool | False | Có bật bóng không |
| shadow_color | string | "#000000" | Màu bóng |
| shadow_angle | float | 0 | Góc bóng |
| shadow_distance | float | 0 | Khoảng cách bóng |
| shadow_smooth | float | 0 | Độ mềm mịn bóng |
| background_color | string | - | Màu nền |
| background_alpha | float | 1.0 | Độ trong suốt nền |
| background_round_radius | float | 0 | Bán kính góc nền |
| background_width | float | 0 | Chiều rộng nền |
| background_height | float | 0 | Chiều cao nền |
| text_intro | string | - | Hoạt ảnh vào |
| text_outro | string | - | Hoạt ảnh ra |
| is_bold | bool | False | Có in đậm không |
| is_italic | bool | False | Có in nghiêng không |
| text_styles | array | - | Văn bản đa kiểu |
| track_name | string | "text" | Tên rãnh |
| alignment_h | string | "center" | Căn chỉnh ngang |
| alignment_v | string | "middle" | Căn chỉnh dọc |
| pos_x | float | 0 | Vị trí X |
| pos_y | float | 0 | Vị trí Y |

**Hình Thức Hoạt Ảnh Văn Bản (text_intro/text_outro):**
- `fade_in` / `fade_out` - Mờ dần vào/ra
- `slide_in_left` / `slide_out_left` - Trượt từ trái/sang trái
- `slide_in_right` / `slide_out_right` - Trượt từ phải/sang phải
- `zoom_in` / `zoom_out` - Thu phóng vào/ra
- `rotate_in` / `rotate_out` - Xoay vào/ra
- Xem thêm `GET /get_text_intro_types`

**Ví Dụ Văn Bản Đa Kiểu:**

```python
requests.post("http://localhost:9001/add_text", json={
    "draft_id": draft_id,
    "text": "Hiệu ứng văn bản đa màu",
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

Nhập tệp phụ đề SRT vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| srt_url | string | Bắt buộc | URL tệp SRT |
| font | string | "Noto Sans CJK" | Tên phông chữ |
| font_size | int | 32 | Kích thước phông chữ |
| font_color | string | "#FFFFFF" | Màu phông chữ |
| stroke_enabled | bool | True | Có bật mô tả không |
| stroke_color | string | "#000000" | Màu mô tả |
| stroke_width | float | 3.0 | Độ rộng mô tả |
| background_alpha | float | 0.5 | Độ trong suốt nền |
| pos_y | float | -0.3 | Vị trí dọc |
| time_offset | float | 0 | Dịch chuyển thời gian (giây) |

**Định Dạng Tệp SRT:**

```srt
1
00:00:00,000 --> 00:00:03,000
Đây là câu phụ đề đầu tiên

2
00:00:03,000 --> 00:00:06,000
Đây là câu phụ đề thứ hai
```

---

#### POST /add_sticker

Thêm nhãn dán vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| sticker_id | string | Bắt buộc | ID nhãn dán |
| start | float | Bắt buộc | Thời gian bắt đầu |
| end | float | Bắt buộc | Thời gian kết thúc |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| scale_x | float | 1.0 | Thu phóng ngang |
| scale_y | float | 1.0 | Thu phóng dọc |
| transform_x | float | 0 | Dịch chuyển vị trí ngang |
| transform_y | float | 0 | Dịch chuyển vị trí dọc |
| flip_horizontal | bool | False | Lật ngang |
| flip_vertical | bool | False | Lật dọc |
| alpha | float | 1.0 | Độ trong suốt |

---

#### POST /add_effect

Thêm hiệu ứng video vào bản nháp.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| effect_type | string | Bắt buộc | Kiểu hiệu ứng |
| start | float | Bắt buộc | Thời gian bắt đầu |
| end | float | Bắt buộc | Thời gian kết thúc |
| target_start | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| intensity | float | 1.0 | Cường độ hiệu ứng |
| effect_params | list | - | Tham số hiệu ứng |

**Phân Loại Hiệu Ứng:**
- Hiệu ứng cảnh (Video_scene_effect_type)
- Hiệu ứng ký tự (Video_character_effect_type)

---

#### POST /add_video_keyframe

Thêm hoạt ảnh khóa hình vào rãnh video.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Giá trị mặc định | Mô tả |
|--------|------|-----------------|------|
| draft_id | string | Bắt buộc | ID bản nháp |
| track_name | string | "video_main" | Tên rãnh |
| property_types | list | Bắt buộc | Danh sách kiểu thuộc tính |
| times | list | Bắt buộc | Các điểm thời gian khóa hình |
| values | list | Bắt buộc | Giá trị thuộc tính tương ứng |

**Kiểu Thuộc Tính Được Hỗ Trợ:**
- `scale_x` - Thu phóng ngang
- `scale_y` - Thu phóng dọc
- `rotation` - Góc xoay
- `alpha` - Độ trong suốt
- `transform_x` - Vị trí ngang
- `transform_y` - Vị trí dọc

**Ví Dụ:**

```python
# Tạo hoạt ảnh thu phóng và độ trong suốt
requests.post("http://localhost:9001/add_video_keyframe", json={
    "draft_id": draft_id,
    "track_name": "video_main",
    "property_types": ["scale_x", "scale_y", "alpha"],
    "times": [0, 2, 4],
    "values": ["1.0,1.0,1.0", "1.2,1.2,0.8", "0.8,0.8,1.0"]
})
```

---

### Các Giao Diện Truy Vấn (GET)

#### GET /get_intro_animation_types

Nhận danh sách các kiểu hoạt ảnh vào video.

#### GET /get_outro_animation_types

Nhận danh sách các kiểu hoạt ảnh ra video.

#### GET /get_combo_animation_types

Nhận danh sách các kiểu hoạt ảnh kết hợp.

#### GET /get_transition_types

Nhận danh sách các kiểu hiệu ứng chuyển tiếp.

#### GET /get_mask_types

Nhận danh sách các kiểu mặt nạ.

#### GET /get_audio_effect_types

Nhận danh sách các kiểu hiệu ứng âm thanh.

#### GET /get_font_types

Nhận danh sách các kiểu phông chữ.

#### GET /get_text_intro_types

Nhận danh sách hoạt ảnh vào văn bản.

#### GET /get_text_outro_types

Nhận danh sách hoạt ảnh ra văn bản.

#### GET /get_text_loop_anim_types

Nhận danh sách hoạt ảnh lặp văn bản.

#### GET /get_video_scene_effect_types

Nhận danh sách các kiểu hiệu ứng cảnh.

#### GET /get_video_character_effect_types

Nhận danh sách các kiểu hiệu ứng ký tự.

---

### Tải Lên Tệp

#### POST /upload_video

Tải lên tệp video lên máy chủ.

#### POST /upload_image

Tải lên tệp hình ảnh lên máy chủ.

#### GET /list_uploads

Liệt kê các tệp đã tải lên.

#### DELETE /delete_upload/<filename>

Xóa tệp đã tải lên được chỉ định.

---

### Chức Năng Nâng Cao

#### POST /get_duration

Lấy thời lượng tệp phương tiện.

**Tham Số Yêu Cầu:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|------|
| media_url | string | Có | URL phương tiện |

#### POST /export_to_capcut

Xuất bản nháp sang Jiànyǐng/CapCut.

#### POST /export_draft_to_video

Xuất bản nháp thành tệp video.

#### GET /export_status

Truy vấn trạng thái xuất.

#### POST /execute_workflow

Thực thi quy trình làm việc được định sẵn.

---

## Phản Hồi Lỗi

Tất cả các điểm cuối API trả về định dạng thống nhất khi xảy ra lỗi:

```json
{
  "success": false,
  "output": "",
  "error": "Mô tả thông báo lỗi"
}
```

Các lỗi phổ biến:
- Thiếu tham số bắt buộc
- URL video/âm thanh không hợp lệ
- ID bản nháp không tồn tại
- Định dạng tệp không được hỗ trợ
