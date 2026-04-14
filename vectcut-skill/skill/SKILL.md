---
name: vectcut-api
description: VectCutAPI is a powerful cloud-based video editing API tool that provides programmatic control over CapCut/JianYing for professional video editing. Use this skill when users need to: (1) Create video draft projects programmatically, (2) Add video/audio/image materials with precise control, (3) Add text, subtitles, and captions, (4) Apply effects, transitions, and animations, (5) Add keyframe animations, (6) Process videos in batch, (7) Generate AI-powered videos, (8) Integrate with n8n workflows, (9) Build MCP video editing agents. The API supports HTTP REST and MCP protocols, works with both CapCut (international) and JianYing (China), and provides web preview without downloading.
---

# VectCutAPI - API Chỉnh Sửa Video Chuyên Nghiệp

## Tổng Quan

VectCutAPI là một công cụ API chỉnh sửa video mạnh mẽ dựa trên đám mây, cho phép kiểm soát lập trình CapCut/JianYing để chỉnh sửa video chuyên nghiệp. Nó lấp đầy khoảng cách giữa tài liệu do AI tạo ra và chỉnh sửa video chuyên nghiệp, cung cấp khả năng kiểm soát chỉnh sửa chính xác.

### Lợi Thế Cốt Lõi

1. **Hỗ Trợ Giao Thức Kép** - HTTP REST API và giao thức MCP
2. **Xem Trước Thời Gian Thực** - Xem trước trang web mà không cần tải xuống
3. **Chỉnh Sửa Lần Thứ Hai** - Nhập vào CapCut/JianYing để tinh chỉnh
4. **Xử Lý Trên Đám Mây** - Hoàn toàn trên đám mây để tạo video

---

## ⚠️ Điều Kiện Tiên Quyết - BẮT BUỘC PHẢI LÀM TRƯỚC KHI SỬ DỤNG SKILL

**Skill này cần server VectCutAPI chạy ở nền để hoạt động. Vui lòng làm theo các bước sau:**

### Bước 1: Cài Đặt VectCutAPI Repository

```bash
git clone https://github.com/nguyenduccanh011/VectCutAPI.git
cd VectCutAPI
python -m venv venv-vectcut
# Windows: venv-vectcut\Scripts\activate
# macOS/Linux: source venv-vectcut/bin/activate
pip install -r requirements.txt
```

### Bước 2: Khởi Động Server (QUAN TRỌNG ⚡)

```bash
python capcut_server.py
```

**Kết quả thành công sẽ hiển thị:**
```
 * Running on http://localhost:9001
```

### Bước 3: Xác Minh Server Chạy

Mở trình duyệt hoặc dùng curl:
```bash
curl http://localhost:9001/
```

**Nếu server không chạy:**
- ❌ Skill sẽ không thể hoạt động
- ❌ Copilot sẽ báo lỗi kết nối

### Yêu Cầu Hệ Thống

- Python 3.10+
- JianYing hoặc CapCut Phiên Bản Quốc Tế
- FFmpeg (Tùy chọn, cho một số xử lý video)

### Khởi Động Nhanh

```bash
# Cài đặt các phụ thuộc
pip install -r requirements.txt      # Phụ thuộc cơ bản cho HTTP API
pip install -r requirements-mcp.txt  # Hỗ trợ giao thức MCP (Tùy chọn)

# Tệp cấu hình
cp config.json.example config.json

# Khởi động dịch vụ
python capcut_server.py  # HTTP API Server (Cổng: 9001)
python mcp_server.py     # MCP Protocol Server
```

## Quy Trình Công Việc

### Quy Trình Tạo Video Tiêu Chuẩn

```
1. Tạo Bản Nháp (create_draft)
   - Đặt Độ Phân Giải: 1080x1920 (Dọc) / 1920x1080 (Ngang) / 1080x1080 (Vuông)
   - Lấy draft_id

2. Thêm Track Tài Nguyên
   - add_video: Thêm track video
   - add_audio: Thêm track âm thanh
   - add_image: Thêm tài nguyên hình ảnh

3. Thêm Phần Tử Văn Bản
   - add_text: Thêm tiêu đề, văn bản giải thích
   - add_subtitle: Nhập tệp SRT phụ đề

4. Áp Dụng Hiệu Ứng
   - add_effect: Thêm hiệu ứng video
   - add_sticker: Thêm tài nguyên sticker
   - add_video_keyframe: Thêm hoạt ăn keyframe

5. Lưu Bản Nháp
   - save_draft: Tạo tệp bản nháp có thể nhập vào JianYing
```

### Quy Trình Tạo Video AI

```
Tạo Kịch Bản AI
    ↓
TTS Chuyển Văn Bản Thành Giọng → audio_url
    ↓
Tạo Video Từ Ảnh → video_url
    ↓
VectCutAPI Kết Hợp Bản Nháp
    ↓
Xuất Hoặc Chỉnh Sửa Tiếp
```

### Xử Lý Video Hàng Loạt

Sử dụng `auto_video_editor.py` để xử lý tạo video hàng loạt do bảng Excel điều khiển.

## Giao Diện API

### Hoạt Động Cốt Lõi

| Giao Diện | Phương Thức | Chức Năng |
|------|------|------|
| `/create_draft` | POST | Tạo dự án bản nháp mới |
| `/save_draft` | POST | Lưu bản nháp và tạo URL |
| `/query_draft_status` | POST | Truy vấn trạng thái bản nháp |
| `/query_script` | POST | Truy vấn nội dung kịch bản bản nháp |
| `/generate_draft_url` | POST | Tạo URL xem trước bản nháp |

### Thêm Tài Nguyên

| Giao Diện | Phương Thức | Chức Năng |
|------|------|------|
| `/add_video` | POST | Thêm track video |
| `/add_audio` | POST | Thêm track âm thanh |
| `/add_image` | POST | Thêm tài nguyên hình ảnh |
| `/add_text` | POST | Thêm phần tử văn bản |
| `/add_subtitle` | POST | Thêm phụ đề SRT |
| `/add_sticker` | POST | Thêm sticker |
| `/add_effect` | POST | Thêm hiệu ứng video |
| `/add_video_keyframe` | POST | Thêm hoạt ăn keyframe |

### Giao Diện Truy Vấn (GET)

| Giao Diện | Chức Năng |
|------|------|
| `/get_intro_animation_types` | Lấy loại hoạt ăn nhập trường |
| `/get_outro_animation_types` | Lấy loại hoạt ăn ra trường |
| `/get_transition_types` | Lấy loại hiệu ứng chuyển cảnh |
| `/get_mask_types` | Lấy danh sách loại mặt nạ |
| `/get_audio_effect_types` | Lấy loại hiệu ứng âm thanh |
| `/get_font_types` | Lấy danh sách loại phông chữ |
| `/get_video_scene_effect_types` | Lấy loại hiệu ứng cảnh |

## Ví Dụ Sử Dụng

### Tạo Bản Nháp Video Dọc Màn Hình

```python
import requests

# 1. Tạo bản nháp
response = requests.post("http://localhost:9001/create_draft", json={
    "width": 1080,
    "height": 1920
})
draft_id = response.json()["output"]["draft_id"]

# 2. Thêm video nền
requests.post("http://localhost:9001/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/background.mp4",
    "start": 0,
    "end": 10,
    "volume": 0.6
})

# 3. Thêm văn bản tiêu đề
requests.post("http://localhost:9001/add_text", json={
    "draft_id": draft_id,
    "text": "Chào Mừng Sử Dụng VectCutAPI",
    "start": 1,
    "end": 5,
    "font_size": 56,
    "font_color": "#FFD700",
    "shadow_enabled": True,
    "background_color": "#000000"
})

# 4. Lưu bản nháp
response = requests.post("http://localhost:9001/save_draft", json={
    "draft_id": draft_id
})
draft_url = response.json()["output"]["draft_url"]
print(f"Bản nháp đã lưu: {draft_url}")
```

### Thêm Hiệu Ứng Chuyển Cảnh

```python
requests.post("http://localhost:9001/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video2.mp4",
    "transition": "fade_in",           # Loại chuyển cảnh
    "transition_duration": 0.5,        # Thời lượng chuyển cảnh (giây)
    "target_start": 10                 # Bắt đầu tại 10 giây trên dòng thời gian
})
```

### Thêm Hoạt Ăn Keyframe

```python
requests.post("http://localhost:9001/add_video_keyframe", json={
    "draft_id": draft_id,
    "track_name": "video_main",
    "property_types": ["scale_x", "scale_y", "alpha"],
    "times": [0, 2, 4],          # Điểm thời gian keyframe
    "values": ["1.0", "1.2", "0.8"]  # Giá trị thuộc tính tương ứng
})
```

### Thêm Phụ Đề SRT

```python
requests.post("http://localhost:9001/add_subtitle", json={
    "draft_id": draft_id,
    "srt_url": "https://example.com/subtitles.srt",
    "font_size": 32,
    "font_color": "#FFFFFF",
    "background_alpha": 0.7
})
```

## Tích Hợp Giao Thức MCP

VectCutAPI hỗ trợ giao thức MCP (Model Context Protocol), có thể được AI Agent gọi trực tiếp.

### Danh Sách Công Cụ MCP

| Tên Công Cụ | Mô Tả Chức Năng |
|---------|----------|
| `create_draft` | Tạo dự án bản nháp video mới |
| `add_video` | Thêm video vào bản nháp |
| `add_audio` | Thêm âm thanh vào bản nháp |
| `add_image` | Thêm tài nguyên hình ảnh |
| `add_text` | Thêm phần tử văn bản |
| `add_subtitle` | Thêm tệp phụ đề |
| `add_effect` | Thêm hiệu ứng hình ảnh |
| `add_sticker` | Thêm phần tử sticker |
| `add_video_keyframe` | Thêm hoạt ăn keyframe |
| `get_video_duration` | Lấy thời lượng video |
| `save_draft` | Lưu dự án bản nháp |

### Cấu Hình Client MCP

Tạo `mcp_config.json`:

```json
{
  "mcpServers": {
    "vectcut-api": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "H:/ComfyUI/web/VectCutAPI",
      "env": {
        "PYTHONPATH": "H:/ComfyUI/web/VectCutAPI",
        "DEBUG": "0"
      }
    }
  }
}
```

## Giải Thích Tham Số

### Tham Số Video (add_video)

| Tham Số | Loại | Giá Trị Mặc Định | Mô Tả |
|------|------|--------|------|
| `draft_id` | string | Bắt buộc | ID Bản Nháp |
| `video_url` | string | Bắt buộc | URL Video |
| `start` | float | 0 | Thời gian bắt đầu video (giây) |
| `end` | float | 0 | Thời gian kết thúc video (giây) |
| `target_start` | float | 0 | Thời gian bắt đầu trên dòng thời gian |
| `speed` | float | 1.0 | Tốc độ phát lại |
| `volume` | float | 1.0 | Âm lượng (0-1) |
| `scale_x/scale_y` | float | 1.0 | Tỷ lệ Thu Phóng |
| `transform_x/transform_y` | float | 0 | Độ Lệch Vị Trí |
| `transition` | string | - | Loại Chuyển Cảnh |
| `transition_duration` | float | 0.5 | Thời Lượng Chuyển Cảnh (giây) |
| `mask_type` | string | - | Loại Mặt Nạ |
| `background_blur` | int | - | Mức Mờ Nền (1-4) |

### Tham Số Văn Bản (add_text)

| Tham Số | Loại | Giá Trị Mặc Định | Mô Tả |
|------|------|--------|------|
| `text` | string | Bắt buộc | Nội Dung Văn Bản |
| `start` | float | Bắt buộc | Thời Gian Bắt Đầu |
| `end` | float | Bắt buộc | Thời Gian Kết Thúc |
| `font` | string | "Source Han Sans" | Tên Phông Chữ |
| `font_size` | int | 32 | Kích Thước Phông Chữ |
| `font_color` | string | "#FFFFFF" | Màu Phông Chữ (HEX) |
| `stroke_enabled` | bool | False | Có Bật Nét Vẽ Hay Không |
| `stroke_color` | string | "#FFFFFF" | Màu Nét Vẽ |
| `stroke_width` | float | 2.0 | Chiều Rộng Nét Vẽ |
| `shadow_enabled` | bool | False | Có Bật Bóng Đổ Hay Không |
| `shadow_color` | string | "#000000" | Màu Bóng Đổ |
| `background_color` | string | - | Màu Nền |
| `background_alpha` | float | 1.0 | Độ Trong Suốt Nền |
| `text_styles` | array | - | Văn Bản Đa Kiểu (Xem Dưới) |

### Văn Bản Đa Kiểu (text_styles)

```python
"text_styles": [
    {"start": 0, "end": 2, "font_color": "#FF6B6B"},
    {"start": 2, "end": 4, "font_color": "#4ECDC4"},
    {"start": 4, "end": 6, "font_color": "#45B7D1"}
]
```

## Tệp Cấu Hình

### Cấu Trúc config.json

```json
{
  "is_capcut_env": true,
  "draft_domain": "https://www.capcutapi.top",
  "port": 9001,
  "preview_router": "/draft/downloader",
  "is_upload_draft": false,
  "oss_config": {
    "bucket_name": "your-bucket",
    "access_key_id": "your-key-id",
    "access_key_secret": "your-secret",
    "endpoint": "https://your-endpoint.aliyuncs.com"
  }
}
```

## Chức Năng Nâng Cao

### Xử Lý Video Hàng Loạt

Sử dụng `auto_video_editor.py` để xử lý hàng loạt do Excel điều khiển:

```python
python auto_video_editor.py input.xlsx
```

Định Dạng Bảng Excel:
| Tiêu Đề Video | Kịch Bản Hai Đoạn | Tài Liệu Mở Đầu | Tài Liệu Kết Thúc | Tài Liệu Bìa |
|---------|---------|---------|---------|---------|
| Giới Thiệu Sản Phẩm | ... | video1.mp4 | video2.mp4 | image.png |

### Tích Hợp Nguy Vụ n8n

Dự án bao gồm nhiều nguy vụ n8n được cấu hình sẵn:

- `text-to-video-with-animation.json` - Nguy Vụ Văn Bản Thành Video
- `auto-video-mixing.json` - Trộn Video Tự Động
- `form-upload-processing.json` - Xử Lý Tải Lên Biểu Mẫu

## Tài Nguyên

### scripts/

Kịch Bản Thực Thi, được sử dụng cho các hoạt động VectCutAPI.

- **vectcut_client.py** - Thư viện đóng gói Client Python

### references/

Tài Liệu Tham Khảo và Hướng Dẫn.

- **api_reference.md** - Tham Khảo Giao Diện API Đầy Đủ
- **workflows.md** - Ví Dụ Nguy Vụ và Thực Hành Tốt Nhất
- **animation_types.md** - Tham Khảo Loại Hoạt Ăn
- **transition_types.md** - Tham Khảo Loại Hiệu Ứng Chuyển Cảnh

### assets/examples/

Mã Ví Dụ và Mẫu.

- **basic_video.py** - Ví Dụ Tạo Video Cơ Bản
- **text_animation.py** - Ví Dụ Hoạt Ăn Văn Bản
- **subtitle_import.py** - Ví Dụ Nhập Phụ Đề
- **batch_processing.py** - Ví Dụ Xử Lý Hàng Loạt

## Các Câu Hỏi Thường Gặp

### Vị Trí Tệp Bản Nháp

Sau khi gọi `save_draft`, một thư mục bắt đầu bằng `dfd_` sẽ được tạo trong thư mục hiện tại. Sao chép nó vào thư mục bản nháp JianYing/CapCut.

### Định Dạng Video Được Hỗ Trợ

- MP4 (Được Đề Xuất)
- MOV
- AVI
- MKV

### Định Dạng Hình Ảnh Được Hỗ Trợ

- PNG (Được Đề Xuất, Hỗ Trợ Trong Suốt)
- JPG/JPEG
- WebP

### Định Dạng Âm Thanh Được Hỗ Trợ

- MP3 (Được Đề Xuất)
- AAC
- WAV
- M4A

## Thông Tin Dự Án

- **GitHub**: https://github.com/sun-guannan/VectCutAPI
- **Trải Nghiệm Trực Tuyến**: https://www.vectcut.com
- **Giấy Phép Mã Mở**: Apache License 2.0
- **Số Sao GitHub**: 800+
