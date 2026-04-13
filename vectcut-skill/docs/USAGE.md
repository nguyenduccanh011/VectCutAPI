# Hướng dẫn sử dụng VectCutAPI Skill

## Mục lục

1. [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
2. [Bắt đầu nhanh](#bắt-đầu-nhanh)
3. [Sử dụng trong Claude Code](#sử-dụng-trong-claude-code)
4. [Sử dụng client Python](#sử-dụng-client-python)
5. [Ví dụ các trường hợp](#ví-dụ-các-trường-hợp)
6. [Khắc phục sự cố](#khắc-phục-sự-cố)
7. [Thực hành tốt nhất](#thực-hành-tốt-nhất)

---

## Hướng dẫn cài đặt

### Yêu cầu tiên quyết

Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt:

- **Python 3.10+** - [Liên kết tải xuống](https://www.python.org/downloads/)
- **Claude Code** - Công cụ CLI chính thức của Anthropic
- **CapCut** hoặc **Jianying** (phần mềm chỉnh sửa video)
- **Git** - Để clone dự án

### Bước 1: Cài đặt VectCutAPI

VectCutAPI là dịch vụ inti được kỹ năng này phụ thuộc, phải được cài đặt và chạy trước.

```bash
# 1. Clone dự án VectCutAPI
git clone https://github.com/nguyenduccanh011/VectCutAPI.git
cd VectCutAPI

# 2. Tạo môi trường ảo (khuyên dùng)
python -m venv venv-vectcut

# Kích hoạt môi trường ảo trên Windows
venv-vectcut\Scripts\activate

# Kích hoạt môi trường ảo trên Linux/macOS
source venv-vectcut/bin/activate

# 3. Cài đặt các phụ thuộc
pip install -r requirements.txt      # Phụ thuộc cơ bản cho HTTP API
pip install -r requirements-mcp.txt  # Hỗ trợ giao thức MCP (tùy chọn)

# 4. Tệp cấu hình
cp config.json.example config.json

# 5. Chỉnh sửa config.json (tùy chọn)
# Sửa đổi cấu hình tùy theo nhu cầu, chẳng hạn như cổng, cài đặt OSS, v.v.

# 6. Khởi động dịch vụ
python capcut_server.py
```

Sau khi dịch vụ được khởi động, nó sẽ lắng nghe tại `http://localhost:9001`

### Bước 2: Cài đặt Skill

```bash
# 1. Clone dự án này
git clone https://github.com/your-username/vectcut-skill.git
cd vectcut-skill

# 2. Sao chép các tệp kỹ năng vào thư mục kỹ năng Claude Code

# Windows (PowerShell)
Copy-Item -Path "skill\*" -Destination "$env:USERPROFILE\.claude\skills\public\vectcut-api\" -Recurse -Force

# Windows (CMD)
xcopy "skill\*" "%USERPROFILE%\.claude\skills\public\vectcut-api\" /E /I /Y

# Linux/macOS
cp -r skill/* ~/.claude/skills/public/vectcut-api/
```

### Bước 3: Xác minh cài đặt

```bash
# Kiểm tra xem thư mục kỹ năng có tồn tại không
# Windows
dir %USERPROFILE%\.claude\skills\public\vectcut-api

# Linux/macOS
ls ~/.claude/skills/public/vectcut-api
```

Bạn nên thấy các tệp sau:
- `SKILL.md`
- `scripts/vectcut_client.py`
- `references/api_reference.md`
- `references/workflows.md`

---

## Bắt đầu nhanh

### Kiểm tra dịch vụ VectCutAPI

```bash
# Kiểm tra API trong terminal mới
curl http://localhost:9001/

# Hoặc truy cập trình duyệt
# http://localhost:9001/
```

Bạn nên thấy trang tài liệu API.

### Kiểm tra client Python

```python
from skill.scripts.vectcut_client import VectCutClient

# Tạo client
client = VectCutClient("http://localhost:9001")

# Tạo bản nháp
draft = client.create_draft(width=1080, height=1920)
print(f"ID bản nháp: {draft.draft_id}")

# Lưu bản nháp
result = client.save_draft(draft.draft_id)
print(f"URL bản nháp: {result.draft_url}")
```

---

## Sử dụng trong Claude Code

### Kích hoạt tự động

Khi bạn đề cập đến các từ khóa sau, Claude Code sẽ tự động tải kỹ năng vectcut-api:

- "tạo bản nháp video"
- "chỉnh sửa video"
- "thêm video track"
- "thêm text vào video"
- "VectCutAPI"
- "bản nháp Jianying"

### Ví dụ cuộc hội thoại

```
Người dùng: Tôi cần tạo video dọc 1080x1920, bao gồm video nền và tiêu đề

Claude: Tôi sẽ giúp bạn tạo video này. Trước tiên, tôi sẽ sử dụng VectCutAPI để tạo bản nháp...

[Tự động tải kỹ năng vectcut-api]

1. Tạo dự án bản nháp (1080x1920)
2. Thêm video nền
3. Thêm tiêu đề text
4. Lưu bản nháp

Vui lòng cung cấp thông tin sau:
- URL hoặc đường dẫn cục bộ của video nền
- Nội dung tiêu đề text
```

### Chỉ định Skill thủ công

Nếu kích hoạt tự động không thành công, bạn có thể chỉ định thủ công:

```
Người dùng: Sử dụng kỹ năng vectcut-api để tạo một bản nháp video
```

---

## Sử dụng client Python

### Cách sử dụng cơ bản

```python
from skill.scripts.vectcut_client import VectCutClient, Resolution, Transition

# Tạo client
with VectCutClient("http://localhost:9001") as client:

    # Tạo bản nháp
    draft = client.create_draft(
        width=Resolution.VERTICAL.value[0],
        height=Resolution.VERTICAL.value[1]
    )

    # Thêm video
    client.add_video(
        draft_id=draft.draft_id,
        video_url="https://example.com/video.mp4",
        volume=0.6,
        transition=Transition.FADE_IN.value
    )

    # Thêm text
    client.add_text(
        draft_id=draft.draft_id,
        text="Tiêu đề",
        start=0,
        end=5,
        font_size=56,
        font_color="#FFD700",
        shadow_enabled=True
    )

    # Lưu bản nháp
    result = client.save_draft(draft.draft_id)
    print(f"Bản nháp đã lưu: {result.draft_url}")
```

### Sử dụng các giá trị cài sẵn

```python
from skill.scripts.vectcut_client import VectCutClient, Resolution, Transition, TextAnimation

with VectCutClient() as client:
    # Sử dụng độ phân giải cài sẵn
    draft = client.create_draft(
        width=Resolution.VERTICAL.value[0],
        height=Resolution.VERTICAL.value[1]
    )

    # Sử dụng hiệu ứng chuyển cảnh cài sẵn
    client.add_video(
        draft.draft_id,
        "video.mp4",
        transition=Transition.FADE_IN.value
    )

    # Sử dụng hiệu ứng động text cài sẵn
    client.add_text(
        draft.draft_id,
        "Xin chào",
        start=0,
        end=3,
        text_intro=TextAnimation.ZOOM_IN.value
    )
```

### Xử lý lỗi

```python
from skill.scripts.vectcut_client import VectCutClient

try:
    client = VectCutClient("http://localhost:9001")
    draft = client.create_draft()

    if client.add_video(draft.draft_id, "video.mp4"):
        print("Video thêm thành công")
    else:
        print("Thêm video thất bại")

except Exception as e:
    print(f"Lỗi xảy ra: {e}")
finally:
    client.close()
```

---

## Ví dụ các trường hợp

### Trường hợp 1: Tạo video ngắn

```python
from skill.scripts.vectcut_client import create_quick_video, Resolution

# Tạo video ngắn nhanh chóng
video_url = create_quick_video(
    base_url="http://localhost:9001",
    video_url="https://example.com/bg.mp4",
    text_content="Hãy theo dõi kênh của tôi",
    bgm_url="https://example.com/bgm.mp3",
    resolution=Resolution.VERTICAL
)

print(f"Video đã được tạo: {video_url}")
```

### Trường hợp 2: Chuyển đổi text thành video bằng AI

```python
from skill.scripts.vectcut_client import VectCutClient

def text_to_video(text_lines, bg_video, bgm):
    """Chuyển đổi văn bản thành video"""
    with VectCutClient() as client:
        draft = client.create_draft(1080, 1920)

        # Thêm video nền và nhạc
        client.add_video(draft.draft_id, bg_video, volume=0.4)
        client.add_audio(draft.draft_id, bgm, volume=0.3)

        # Thêm text
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
        for i, line in enumerate(text_lines):
            client.add_text(
                draft.draft_id,
                line,
                start=i * 4,
                end=(i + 1) * 4,
                font_size=48,
                font_color=colors[i % len(colors)],
                shadow_enabled=True,
                background_alpha=0.6
            )

        # Lưu
        result = client.save_draft(draft.draft_id)
        return result.draft_url

# Sử dụng
video_url = text_to_video(
    ["Dòng văn bản 1", "Dòng văn bản 2", "Dòng văn bản 3"],
    "bg.mp4",
    "bgm.mp3"
)
```

### Trường hợp 3: Ghép video

```python
from skill.scripts.vectcut_client import VectCutClient, Transition

def create_mashup(video_clips):
    """Tạo ghép video"""
    with VectCutClient() as client:
        draft = client.create_draft(1080, 1920)

        transitions = [
            Transition.FADE_IN.value,
            Transition.WIPE_LEFT.value,
            Transition.WIPE_RIGHT.value
        ]

        current_time = 0
        for i, clip in enumerate(video_clips):
            transition = transitions[i % len(transitions)] if i > 0 else None

            client.add_video(
                draft.draft_id,
                clip["url"],
                start=0,
                end=clip["duration"],
                target_start=current_time,
                transition=transition,
                transition_duration=0.5
            )
            current_time += clip["duration"]

        result = client.save_draft(draft.draft_id)
        return result.draft_url

# Sử dụng
clips = [
    {"url": "clip1.mp4", "duration": 5},
    {"url": "clip2.mp4", "duration": 4},
    {"url": "clip3.mp4", "duration": 6}
]

video_url = create_mashup(clips)
```

### Trường hợp 4: Video có phụ đề

```python
from skill.scripts.vectcut_client import VectCutClient

def add_subtitles_to_video(video_url, srt_url):
    """Thêm phụ đề vào video"""
    with VectCutClient() as client:
        draft = client.create_draft(1920, 1080)

        # Thêm video
        client.add_video(draft.draft_id, video_url)

        # Thêm phụ đề
        client.add_subtitle(
            draft_id=draft.draft_id,
            srt_url=srt_url,
            font_size=36,
            font_color="#FFFFFF",
            stroke_enabled=True,
            stroke_width=4.0,
            background_alpha=0.5
        )

        result = client.save_draft(draft.draft_id)
        return result.draft_url

# Sử dụng
video_url = add_subtitles_to_video("video.mp4", "subtitles.srt")
```

---

## Khắc phục sự cố

### Vấn đề 1: Dịch vụ VectCutAPI không thể khởi động

**Triệu chứng**: Lỗi khi chạy `python capcut_server.py`

**Giải pháp**:

1. Kiểm tra phiên bản Python (cần 3.10+)
   ```bash
   python --version
   ```

2. Cài đặt lại các phụ thuộc
   ```bash
   pip install -r requirements.txt
   ```

3. Kiểm tra cổng đang được sử dụng
   ```bash
   # Windows
   netstat -ano | findstr :9001

   # Linux/macOS
   lsof -i :9001
   ```

### Vấn đề 2: Claude Code không nhận diện Skill

**Triệu chứng**: Claude không tự động tải kỹ năng vectcut-api

**Giải pháp**:

1. Kiểm tra vị trí thư mục kỹ năng
   ```bash
   # Nên ở đường dẫn sau
   ~/.claude/skills/public/vectcut-api/
   # hoặc
   %USERPROFILE%\.claude\skills\public\vectcut-api\
   ```

2. Kiểm tra định dạng SKILL.md
   - Đảm bảo YAML frontmatter đúng
   - Đảm bảo các trường name và description tồn tại

3. Khởi động lại Claude Code

### Vấn đề 3: Yêu cầu API thất bại

**Triệu chứng**: Client trả về lỗi

**Giải pháp**:

1. Kiểm tra dịch vụ VectCutAPI có đang chạy không
   ```bash
   curl http://localhost:9001/
   ```

2. Kiểm tra kết nối mạng
   ```bash
   ping localhost
   ```

3. Xem nhật ký dịch vụ

### Vấn đề 4: File bản nháp không thể nhập vào Jianying/CapCut

**Triệu chứng**: File bản nháp được tạo không hiển thị trong Jianying/CapCut

**Giải pháp**:

1. Xác nhận vị trí thư mục bản nháp Jianying/CapCut:
   - **Windows**: `C:\Users\Tên người dùng\AppData\Local\JianyingPro\User Data\Projects\`
   - **Mac**: `~/Movies/JianyingPro/User Data/Projects/`

2. Sao chép folder `dfd_xxxxx` vào thư mục trên

3. Khởi động lại Jianying/CapCut

---

## Thực hành tốt nhất

### 1. Quản lý Timeline

```python
# Cách tốt: Sử dụng biến để theo dõi thời gian
current_time = 0
duration_per_clip = 5

for clip in clips:
    client.add_video(
        draft.draft_id,
        clip["url"],
        target_start=current_time,
        end=duration_per_clip
    )
    current_time += duration_per_clip

# Tránh: Hardcode thời gian
client.add_video(draft.draft_id, clip1, target_start=0)
client.add_video(draft.draft_id, clip2, target_start=5)
client.add_video(draft.draft_id, clip3, target_start=10)
```

### 2. Xử lý lỗi

```python
# Cách tốt: Xử lý lỗi hoàn chỉnh
try:
    draft = client.create_draft()
    if not client.add_video(draft.draft_id, video_url):
        print(f"Thêm video thất bại: {video_url}")
except Exception as e:
    print(f"Lỗi xảy ra: {e}")
```

### 3. Dọn dẹp tài nguyên

```python
# Cách tốt: Sử dụng context manager
with VectCutClient() as client:
    # Các thao tác...
    pass  # Tự động đóng kết nối

# Tránh: Quên đóng
client = VectCutClient()
# Các thao tác...
# Quên gọi client.close()
```

### 4. Quản lý cấu hình

```python
# Cách tốt: Sử dụng file cấu hình
import json

with open("video_config.json") as f:
    config = json.load(f)

client = VectCutClient(config["api_url"])
draft = client.create_draft(
    width=config["width"],
    height=config["height"]
)
```

### 5. Thao tác hàng loạt

```python
# Cách tốt: Thêm các tài nguyên hàng loạt
texts = [
    {"text": "Tiêu đề", "size": 64, "color": "#FFD700"},
    {"text": "Phụ đề", "size": 48, "color": "#FFFFFF"},
    {"text": "Ghi chú", "size": 36, "color": "#CCCCCC"}
]

for text_config in texts:
    client.add_text(draft.draft_id, **text_config)
```

---

## Kỹ thuật nâng cao

### 1. Sử dụng kiểm tra trước

```python
# Kiểm tra thời lượng media trước khi tạo video
duration = client.get_duration(media_url)
if duration:
    print(f"Thời lượng media: {duration} giây")
else:
    print("Không thể lấy thời lượng media")
```

### 2. Xây dựng tham số động

```python
# Xây dựng tham số động dựa trên điều kiện
video_params = {
    "draft_id": draft.draft_id,
    "video_url": video_url
}

if needs_transition:
    video_params["transition"] = "fade_in"
    video_params["transition_duration"] = 0.8

if needs_volume_adjust:
    video_params["volume"] = 0.5

client.add_video(**video_params)
```

### 3. Tạo hàm có thể tái sử dụng

```python
def create_title_card(client, draft_id, title, subtitle=""):
    """Tạo card tiêu đề"""
    client.add_text(
        draft_id,
        title,
        start=0,
        end=3,
        font_size=64,
        font_color="#FFD700",
        shadow_enabled=True
    )

    if subtitle:
        client.add_text(
            draft_id,
            subtitle,
            start=1,
            end=4,
            font_size=36,
            pos_y=0.1
        )

# Sử dụng
create_title_card(client, draft.draft_id, "Tiêu đề chính", "Tiêu đề phụ")
```

---

## Tài nguyên liên quan

- [VectCutAPI GitHub](https://github.com/nguyenduccanh011/VectCutAPI)
- [Tài liệu tham chiếu API](skill/references/api_reference.md)
- [Ví dụ quy trình](skill/references/workflows.md)
- [Kiến trúc kỹ thuật](ARCHITECTURE.md)
