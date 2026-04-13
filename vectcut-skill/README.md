# VectCutAPI Skill cho Claude Code

<div align="center">

**[English](README_EN.md)** | **Tiếng Việt**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-purple.svg)](https://claude.com/claude-code)
[![VectCutAPI](https://img.shields.io/badge/VectCutAPI-1.5k%2B%20Stars-orange.svg)](https://github.com/nguyenduccanh011/VectCutAPI)

Cho phép AI thực hiện chỉnh sửa video chuyên nghiệp thông qua VectCutAPI

[Bắt đầu nhanh](#bắt-đầu-nhanh) • [Tính năng](#tính-năng) • [Ví dụ sử dụng](#ví-dụ-sử-dụng) • [Tài liệu API](#tài-liệu-api)

</div>

---

## Giới thiệu dự án

**VectCutAPI Skill** là kỹ năng chỉnh sửa video chuyên nghiệp được đóng gói cho [Claude Code](https://claude.com/claude-code), dựa trên dự án mạnh mẽ [VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI).

Thông qua kỹ năng này, Claude AI có thể gọi trực tiếp tất cả các chức năng của VectCutAPI để thực hiện:
- Tự động tạo dự án bản nháp video
- Thêm tài nguyên video, âm thanh, hình ảnh
- Thêm văn bản, phụ đề, hiệu ứng
- Áp dụng chuyển cảnh và hoạt ăn chuyển động
- Xử lý video hàng loạt
- Quy trình tạo video do AI điều khiển

### Ưu điểm cốt lõi

- **Tích hợp liền mạch** - Claude Code tự động nhận diện và tải kỹ năng
- **Đóng gói hoàn chỉnh** - Hỗ trợ tất cả 35+ giao diện HTTP và 11 công cụ MCP của VectCutAPI
- **Client Python** - Cung cấp API Python được đóng gói thanh lịch
- **Ví dụ phong phú** - Bao gồm 8+ mã ví dụ quy trình công việc phổ biến
- **Hỗ trợ giao thức kép** - Hỗ trợ cả giao thức HTTP REST và MCP

---

## Lời cảm ơn và Tuyên bố

Dự án này được đóng gói và mở rộng dựa trên các dự án mã nguồn mở sau:

### Dự án phụ thuộc cốt lõi

| Dự án | Tác giả | Giấy phép | Mô tả |
|------|--------|---------|------|
| [VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI) | [@nguyenduccanh011](https://github.com/nguyenduccanh011) | Apache 2.0 | API chỉnh sửa video trên đám mây mạnh mẽ, cung cấp kiểm soát lập trình cho Jianying/CapCut |
| [Claude Code](https://claude.com/claude-code) | Anthropic | - | Công cụ CLI chính thức của Anthropic, hỗ trợ mở rộng kỹ năng tùy chỉnh |
| [skill-creator](https://github.com/anthropics/claude-code-skills) | Anthropic | - | Hướng dẫn và công cụ tạo kỹ năng Claude Code |

### Cảm ơn đặc biệt

- **@nguyenduccanh011** - Cảm ơn đã fork và duy trì dự án VectCutAPI tuyệt vời này, lấp đầy khoảng cách giữa các tài liệu được tạo bởi AI và chỉnh sửa video chuyên nghiệp
- **Anthropic** - Cảm ơn đã cung cấp Claude Code và hệ thống kỹ năng, cho phép AI tích hợp liền mạch các công cụ chuyên nghiệp

### Tuyên bố

Dự án này chỉ tồn tại như một kỹ năng đi kèm với VectCutAPI, nhằm cung cấp cho người dùng Claude Code một cách tích hợp thuận tiện. Các chức năng chỉnh sửa video cốt lõi hoàn toàn phụ thuộc vào dự án VectCutAPI gốc.

---

## Tính năng

### Chức năng chỉnh sửa video được hỗ trợ

| Mô-đun chức năng | Mô tả |
|---------|------|
| **Quản lý bản nháp** | Tạo, lưu, truy vấn tệp bản nháp Jianying/CapCut |
| **Xử lý video** | Nhập video đa định dạng, cắt, chuyển cảnh, hiệu ứng, mặt nạ |
| **Chỉnh sửa âm thanh** | Các track âm thanh, kiểm soát âm lượng, xử lý hiệu ứng âm thanh |
| **Xử lý hình ảnh** | Nhập hình ảnh, hoạt ăn, mặt nạ, bộ lọc |
| **Chỉnh sửa văn bản** | Văn bản đa kiểu dáng, bóng, nền, hoạt ăn |
| **Hệ thống phụ đề** | Nhập phụ đề SRT, cài đặt kiểu dáng, đồng bộ hóa thời gian |
| **Công cụ hiệu ứng** | Hiệu ứng hình ảnh, bộ lọc, hoạt ăn chuyển cảnh |
| **Hệ thống nhãn dán** | Tài sản nhãn dán, kiểm soát vị trí, hiệu ứng hoạt ăn |
| **Khung hình chính** | Hoạt ăn thuộc tính, kiểm soát dòng thời gian, hàm giảm tốc |
| **Phân tích phương tiện** | Lấy thời lượng video, phát hiện định dạng |

### Tài nguyên có sẵn trong Skill

- **SKILL.md** - Hướng dẫn sử dụng kỹ năng hoàn chỉnh
- **Client Python** - `vectcut_client.py` cung cấp API được đóng gói thanh lịch
- **Tài liệu tiếp cận** - Tài liệu giao diện chi tiết và mô tả tham số
- **Ví dụ quy trình** - Mã hoàn chỉnh cho 8+ trường hợp sản xuất video phổ biến

---

## Bắt đầu nhanh

### Yêu cầu hệ thống

- Python 3.10+
- Claude Code (CLI chính thức của Anthropic)
- Jianying hoặc CapCut International Version
- FFmpeg (tùy chọn)

### 1. Cài đặt VectCutAPI

```bash
# Clone dự án VectCutAPI
git clone https://github.com/nguyenduccanh011/VectCutAPI.git
cd VectCutAPI

# Cài đặt các phụ thuộc
pip install -r requirements.txt      # Phụ thuộc cơ bản cho HTTP API
pip install -r requirements-mcp.txt  # Hỗ trợ giao thức MCP (tùy chọn)

# Tệp cấu hình
cp config.json.example config.json
# Chỉnh sửa config.json nếu cần thiết

# Khởi động dịch vụ
python capcut_server.py  # Máy chủ API HTTP (cổng mặc định: 9001)
```

### 2. Cài đặt Skill

```bash
# Clone dự án này
git clone https://github.com/HUNSETO1413/vectcut-skill.git
cd vectcut-skill

# Sao chép tệp skill vào thư mục kỹ năng Claude Code
# Windows:
copy skill\* %USERPROFILE%\.claude\skills\public\vectcut-api\ /E

# Linux/macOS:
cp -r skill/* ~/.claude/skills/public/vectcut-api/
```

### 3. Xác minh cài đặt

Nhập vào Claude Code:

```
Tôi cần tạo một bản nháp video 1080x1920
```

Claude sẽ tự động tải kỹ năng vectcut-api và gọi các chức năng liên quan.

---

## Ví dụ sử dụng

### Sản xuất video cơ bản

```python
from skill.scripts.vectcut_client import VectCutClient

# Tạo client
client = VectCutClient("http://localhost:9001")

# Tạo bản nháp
draft = client.create_draft(width=1080, height=1920)

# Thêm video nền
client.add_video(
    draft.draft_id,
    "https://example.com/background.mp4",
    volume=0.6
)

# Thêm tiêu đề văn bản
client.add_text(
    draft.draft_id,
    "Chào mừng bạn đến với VectCutAPI",
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

### Quy trình chuyển đổi văn bản thành video bằng AI

```python
import requests

BASE_URL = "http://localhost:9001"

# 1. Tạo bản nháp
draft = requests.post(f"{BASE_URL}/create_draft", json={
    "width": 1080,
    "height": 1920
}).json()
draft_id = draft["output"]["draft_id"]

# 2. Thêm video nền
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/bg.mp4",
    "volume": 0.4
})

# 3. Thêm văn bản theo đoạn
segments = ["Đoạn text thứ nhất", "Đoạn text thứ hai", "Đoạn text thứ ba"]
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

for i, (segment, color) in enumerate(zip(segments, colors)):
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": segment,
        "start": i * 4,
        "end": (i + 1) * 4,
        "font_size": 48,
        "font_color": color,
        "shadow_enabled": True
    })

# 4. Lưu bản nháp
result = requests.post(f"{BASE_URL}/save_draft", json={
    "draft_id": draft_id
}).json()

print(f"Video đã được tạo: {result['output']['draft_url']}")
```

Chi tiết hơn xem [workflows.md](skill/references/workflows.md).

---

## Kiến trúc kỹ thuật

### Cấu trúc Skill

```
vectcut-skill/
├── skill/                       # Claude Code Skill
│   ├── SKILL.md                 # Tài liệu chính của kỹ năng
│   ├── scripts/                 # Script có thể thực thi
│   │   └── vectcut_client.py   # Đóng gói client Python
│   ├── references/              # Tài liệu tham chiếu
│   │   ├── api_reference.md    # Tham chiếu giao diện API
│   │   └── workflows.md        # Ví dụ quy trình
│   └── assets/                  # Tệp tài sản
│       └── examples/            # Mã ví dụ
├── docs/                        # Tài liệu dự án
│   ├── ARCHITECTURE.md          # Mô tả kiến trúc kỹ thuật
│   ├── INSTALLATION.md          # Hướng dẫn cài đặt
│   └── USAGE.md                 # Hướng dẫn sử dụng
├── LICENSE                      # Giấy phép MIT
└── README.md                    # Mô tả dự án
```

### Công nghệ đóng gói

Dự án này sử dụng các công nghệ sau để đóng gói:

1. **Hệ thống Claude Code Skill**
   - Tuân thủ thông số kỹ năng chính thức của Anthropic
   - Sử dụng YAML frontmatter để định nghĩa siêu dữ liệu kỹ năng
   - Áp dụng nguyên tắc lộ trình tiến bộ

2. **Đóng gói client Python**
   - Sử dụng dataclasses để định nghĩa cấu trúc dữ liệu
   - Sử dụng loại Enum để định nghĩa giá trị cài sẵn
   - Hỗ trợ trình quản lý bối cảnh
   - Xử lý lỗi hoàn chỉnh

3. **Tổ chức tài liệu**
   - SKILL.md: Hướng dẫn sử dụng cốt lõi
   - references/: Tài liệu tham chiếu chi tiết
   - scripts/: Mã có thể thực thi

---

## Tài liệu API

### API cốt lõi

| API | Chức năng |
|-----|------|
| `create_draft()` | Tạo bản nháp video |
| `save_draft()` | Lưu bản nháp và tạo URL |
| `add_video()` | Thêm track video |
| `add_audio()` | Thêm track âm thanh |
| `add_image()` | Thêm tài sản hình ảnh |
| `add_text()` | Thêm phần tử văn bản |
| `add_subtitle()` | Thêm phụ đề SRT |
| `add_effect()` | Thêm hiệu ứng video |
| `add_sticker()` | Thêm nhãn dán |
| `add_video_keyframe()` | Thêm hoạt ăn khung hình chính |

Xem tài liệu API đầy đủ tại [api_reference.md](skill/references/api_reference.md).

---

## Ví dụ quy trình

Dự án bao gồm các ví dụ quy trình hoàn chỉnh sau:

1. **Sản xuất video cơ bản** - Quy trình sản xuất video ngắn dọc
2. **Chuyển đổi văn bản thành video bằng AI** - Tự động chuyển đổi nội dung văn bản thành video
3. **Ghép video** - Ghép nối đa đoạn video và chuyển cảnh
4. **Video có phụ đề** - Nhập phụ đề SRT
5. **Hoạt ăn khung hình chính** - Hiển thị hoạt ăn hình ảnh
6. **Video giới thiệu sản phẩm** - Giới thiệu sản phẩm chuyên nghiệp
7. **Hiệu ứng chia đôi màn hình** - So sánh chia đôi trái phải
8. **Trình chiếu ảnh** - Slide ảnh

Xem thêm [workflows.md](skill/references/workflows.md).

---

## Các dự án liên quan

- [VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI) - API chỉnh sửa video cốt lõi
- [pyJianYingDraft](https://github.com/nguyenduccanh011/pyJianYingDraft) - Thư viện Python bản nháp Jianying
- [Claude Code Skills](https://github.com/anthropics/claude-code-skills) - Bộ sưu tập kỹ năng chính thức

---

## Giấy phép

Dự án này được phân phối dưới [Giấy phép MIT](LICENSE).

**Lưu ý**: Thư viện cốt lõi VectCutAPI được đóng gói bởi dự án này được phân phối dưới giấy phép Apache 2.0.

---

## Hướng dẫn đóng góp

Chúng tôi hoan nghênh các đóng góp mã! Vui lòng tuân theo quy trình sau:

1. Fork dự án
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`)
3. Commit những thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push tới nhánh (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

### Hướng dẫn đóng góp

- Thêm ví dụ quy trình mới
- Tối ưu hóa client Python
- Cải thiện tài liệu
- Sửa lỗi

---

## Thông tin liên hệ

### Thông tin tác giả

**Tác giả dự án**: HUNSETO1413

- **Trang chủ dự án**: [GitHub Repository](https://github.com/HUNSETO1413/vectcut-skill)
- **Phản hồi vấn đề**: [Issues](https://github.com/HUNSETO1413/vectcut-skill/issues)
- **Dự án VectCutAPI gốc**: [nguyenduccanh011/VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI)

### Liên hệ WeChat

Quét mã để thêm WeChat của tác giả, trao đổi các vấn đề kỹ thuật:

<div align="center">

![WeChat tác giả](Mark微信.png)

**WeChat ID**: `399187854`

</div>

---

## Nhật ký cập nhật

### v1.0.0 (2025-01-25)

Phát hành phiên bản ban đầu

- ✅ Đóng gói Skill VectCutAPI hoàn chỉnh
- ✅ Thư viện client Python
- ✅ 8+ ví dụ quy trình
- ✅ Tài liệu tham chiếu API hoàn chỉnh
- ✅ Hỗ trợ tất cả các chức năng VectCutAPI

---

## Định dạng sao

Nếu dự án này hữu ích cho bạn, vui lòng cấp một sao ⭐️

Đồng thời hoan nghênh cấp sao cho dự án gốc [VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI) 🌟

---

<div align="center">

**Được tạo với ❤️ bởi HUNSETO1413**

Dựa trên [VectCutAPI](https://github.com/nguyenduccanh011/VectCutAPI) của [@nguyenduccanh011](https://github.com/nguyenduccanh011)

WeChat: **399187854**

</div>
