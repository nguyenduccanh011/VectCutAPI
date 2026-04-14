# Tài Liệu Kiến Trúc Kỹ Thuật VectCutAPI Skill

## Tổng Quan

Tài liệu này trình bày chi tiết về kiến trúc kỹ thuật, nguyên tắc thiết kế và chi tiết thực hiện của VectCutAPI Skill.

---

## Kiến Trúc Dự Án

### Sơ Đồ Kiến Trúc Tổng Quan

```
┌─────────────────────────────────────────────────────────────────┐
│                         Claude Code                              │
│                   (Công cụ CLI của Anthropic)                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Hệ Thống Skill                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Skill vectcut-api                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   SKILL.md   │  │  scripts/    │  │ references/  │   │  │
│  │  │ (Tài liệu)   │  │ (Mã thực thi) │  │ (Tài liệu)  │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      VectCutAPI                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  HTTP API Server (capcut_server.py)                      │  │
│  │  Cổng: 9001                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  pyJianYingDraft (Thư viện lõi quản lý bản nháp)        │  │
│  │  - Quản lý bản nháp                                       │  │
│  │  - Hoạt động trên track                                   │  │
│  │  - Xử lý đoạn phim                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CapCut / JianYing                               │
│                 (Ứng dụng chỉnh sửa video)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Thiết Kế Cấu Trúc Skill

### Quy Chuẩn Claude Code Skill của Anthropic

Dự án này tuân thủ chặt chẽ quy chuẩn Skill chính thức của Anthropic:

#### 1. Tệp Bắt Buộc

```
skill/
├── SKILL.md              # Bắt buộc - Tài liệu chính của kỹ năng
└── [Thư mục tài nguyên]  # Tùy chọn - scripts/, references/, assets/
```

#### 2. Định Dạng SKILL.md

SKILL.md sử dụng YAML frontmatter để định nghĩa metadata:

```markdown
---
name: vectcut-api
description: VectCutAPI is a powerful cloud-based video editing API...
---

# Nội dung kỹ năng...
```

**Giải Thích Các Trường Metadata:**
- `name`: Định danh kỹ năng (được sử dụng để kích hoạt kỹ năng)
- `description`: Mô tả kỹ năng (Claude dùng để xác định khi nào sử dụng kỹ năng này)

#### 3. Thiết Kế Tiết Lộ Dần Dần

Để tối ưu hóa việc sử dụng token, sử dụng hệ thống tải ba cấp:

| Cấp | Nội Dung | Giới Hạn Kích Thước | Thời Điểm Tải |
|------|------|----------|----------|
| **Metadata** | name + description | ~100 tokens | Luôn tải |
| **Phần thân SKILL.md** | Hướng dẫn sử dụng cốt lõi | <5k tokens | Khi kích hoạt kỹ năng |
| **Tài Nguyên Đi Kèm** | scripts/references/assets | Không giới hạn | Tải theo yêu cầu |

---

## Thiết Kế Client Python

### Nguyên Tắc Thiết Kế

1. **Tính Đơn Giản** - Cung cấp giao diện API trực quan
2. **An Toàn Kiểu** - Sử dụng dataclasses và Enum
3. **Quản Lý Tài Nguyên** - Hỗ trợ context manager
4. **Xử Lý Lỗi** - Cơ chế xử lý lỗi thống nhất

### Cấu Trúc Lớp

```python
# Lớp dữ liệu
@dataclass
class DraftInfo:
    """Thông tin bản nháp"""
    draft_id: str
    draft_folder: Optional[str] = None
    draft_url: Optional[str] = None

@dataclass
class ApiResult:
    """Kết quả phản hồi API"""
    success: bool
    output: Dict[str, Any]
    error: Optional[str] = None

# Lớp liệt kê
class Resolution(Enum):
    """Cài đặt độ phân giải video phổ biến"""
    VERTICAL = (1080, 1920)
    HORIZONTAL = (1920, 1080)
    SQUARE = (1080, 1080)

class Transition(Enum):
    """Loại hiệu ứng chuyển cảnh"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"

# Lớp client chính
class VectCutClient:
    """Client Python VectCutAPI"""

    def __init__(self, base_url: str, timeout: int = 120)
    def create_draft(...) -> DraftInfo
    def save_draft(...) -> DraftInfo
    def add_video(...) -> bool
    def add_audio(...) -> bool
    def add_text(...) -> bool
    # ... Thêm các phương thức khác

    def __enter__(self)
    def __exit__(self, exc_type, exc_val, exc_tb)
```

### Mẫu Thiết Kế Phương Thức

#### 1. Phương Thức Tạo

```python
def create_draft(self, width: int = 1080, height: int = 1920) -> DraftInfo:
    """
    Tạo bản nháp mới

    Args:
        width: Chiều rộng video
        height: Chiều cao video

    Returns:
        DraftInfo: Đối tượng thông tin bản nháp

    Raises:
        Exception: Bắt ra ngoại lệ khi tạo thất bại
    """
```

#### 2. Phương Thức Hoạt Động

```python
def add_video(self,
             draft_id: str,
             video_url: str,
             start: float = 0,
             # ... Thêm tham số
             **kwargs) -> bool:
    """
    Thêm track video

    Args:
        draft_id: ID bản nháp
        video_url: URL video
        ...

    Returns:
        bool: Liệu hoạt động có thành công hay không
    """
```

#### 3. Phương Thức Truy Vấn

```python
def get_duration(self, media_url: str) -> Optional[float]:
    """
    Lấy thời lượng của tệp media

    Args:
        media_url: URL media

    Returns:
        Optional[float]: Thời lượng (giây), trả về None nếu thất bại
    """
```

---

## Cấu Trúc Tổ Chức Tài Liệu

### 1. SKILL.md (Tài Liệu Chính)

**Tổ Chức Nội Dung:**
- Tổng Quan - Giới thiệu về kỹ năng
- Yêu Cầu Hệ Thống - Các yêu cầu hệ thống
- Bắt Đầu Nhanh - Khởi động nhanh
- Workflow - Quy trình công việc tiêu chuẩn
- Giao Diện API - Danh sách giao diện API
- Ví Dụ Sử Dụng - Các ví dụ sử dụng
- Tích Hợp MCP - Tích hợp giao thức MCP
- Tham Số - Giải thích tham số

**Nguyên Tắc Thiết Kế:**
- Giữ dưới 500 dòng
- Chỉ bao gồm quy trình cốt lõi và thông tin cần thiết
- Đặt nội dung chi tiết vào references/

### 2. references/ (Tài Liệu Tham Khảo)

**api_reference.md** - Tham Khảo API Đầy Đủ
- Mô tả chi tiết tất cả các endpoint HTTP
- Định dạng tham số yêu cầu và phản hồi
- Giải thích xử lý lỗi
- Loại tham số và giá trị mặc định

**workflows.md** - Ví Dụ Workflow
- Mã hoàn chỉnh cho 8+ kịch bản phổ biến
- Mỗi ví dụ bao gồm chú thích chi tiết
- Giải thích các thực hành tốt nhất

### 3. scripts/ (Mã Thực Thi)

**vectcut_client.py** - Client Python
- Có thể nhập trực tiếp và sử dụng
- Có thể chạy như một script độc lập
- Bao gồm type annotation đầy đủ

---

## Quan Hệ Ánh Xạ API

### Ánh Xạ HTTP API → Phương Thức Client

| HTTP API | Phương Thức Client | Mô Tả |
|----------|-----------|------|
| POST /create_draft | `create_draft()` | Tạo bản nháp |
| POST /save_draft | `save_draft()` | Lưu bản nháp |
| POST /add_video | `add_video()` | Thêm video |
| POST /add_audio | `add_audio()` | Thêm âm thanh |
| POST /add_image | `add_image()` | Thêm hình ảnh |
| POST /add_text | `add_text()` | Thêm văn bản |
| POST /add_subtitle | `add_subtitle()` | Thêm phụ đề |
| POST /add_sticker | `add_sticker()` | Thêm sticker |
| POST /add_effect | `add_effect()` | Thêm hiệu ứng |
| POST /add_video_keyframe | `add_video_keyframe()` | Thêm keyframe |
| POST /get_duration | `get_duration()` | Lấy thời lượng |
| GET /get_*_types | `get_*_types()` | Lấy danh sách loại |

---

## Thiết Kế Luồng Dữ Liệu

### Luồng Dữ Liệu Tạo Video

```
Yêu Cầu Người Dùng
    │
    ▼
Claude Phân Tích Ý Định
    │
    ▼
Tải Skill vectcut-api
    │
    ▼
Gọi Client Python
    │
    ▼
┌─────────────────────────────────────────┐
│ Gọi Phương Thức VectCutClient           │
│  ┌───────────────────────────────────┐ │
│  │ 1. create_draft()                 │ │
│  │ 2. add_video()                    │ │
│  │ 3. add_audio()                    │ │
│  │ 4. add_text()                     │ │
│  │ 5. save_draft()                   │ │
│  └───────────────────────────────────┘ │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Yêu Cầu HTTP (Thư viện requests)       │
│  POST http://localhost:9001/...        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ VectCutAPI Server                       │
│  Flask HTTP Server                      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ pyJianYingDraft                         │
│  Tạo tệp bản nháp JianYing             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Tệp Bản Nháp (dfd_xxxxx/)               │
│  - draft_content.json                   │
│  - material_*.json                      │
└─────────────────────────────────────────┘
```

---

## Cơ Chế Xử Lý Lỗi

### 1. Xử Lý Phản Hồi API

```python
def _post(self, endpoint: str, **kwargs) -> ApiResult:
    """Gửi yêu cầu POST"""
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
```

### 2. Xử Lý Lỗi Ở Mức Phương Thức

```python
def create_draft(self, ...) -> DraftInfo:
    result = self._post("/create_draft", ...)
    if result.success:
        return DraftInfo(...)
    raise Exception(f"Tạo bản nháp thất bại: {result.error}")
```

---

## Thiết Kế Khả Năng Mở Rộng

### 1. Mở Rộng Giá Trị Cài Đặt

Dễ dàng thêm các cài đặt mới thông qua lớp Enum:

```python
class Resolution(Enum):
    VERTICAL = (1080, 1920)
    HORIZONTAL = (1920, 1080)
    SQUARE = (1080, 1080)
    # Thêm mới
    WIDE = (1920, 1200)
```

### 2. Tham Số Tùy Chỉnh

Tất cả các phương thức hỗ trợ truyền tham số bổ sung thông qua `**kwargs`:

```python
client.add_video(draft_id, video_url, custom_param="value")
```

### 3. Tái Sử Dụng Workflow

Mã ví dụ có thể được sử dụng như template để tái sử dụng nhanh chóng:

```python
# Sao chép template từ workflows.md
# Sửa đổi tham số để sử dụng
```

---

## Tối Ưu Hóa Hiệu Suất

### 1. Tái Sử Dụng Kết Nối

```python
self.session = requests.Session()  # Tái sử dụng kết nối TCP
```

### 2. Tải Theo Yêu Cầu

- Giữ SKILL.md gọn nhẹ
- Tải tài liệu chi tiết theo yêu cầu vào references/

### 3. Hỗ Trợ Bất Đồng Bộ (Trong Tương Lai)

Có thể mở rộng hỗ trợ yêu cầu bất đồng bộ:

```python
async def add_video_async(self, ...):
    async with aiohttp.ClientSession() as session:
        ...
```

---

## Xem Xét Bảo Mật

### 1. Xác Thực URL

Client không xác thực URL, được áp dụng bởi phía máy chủ VectCutAPI

### 2. Kiểm Soát Timeout

Timeout mặc định 120 giây, ngăn chặn bị block lâu dài

### 3. Quản Lý Tài Nguyên

Hỗ trợ context manager đảm bảo giải phóng tài nguyên:

```python
with VectCutClient() as client:
    # Tự động đóng kết nối
    ...
```

---

## Chiến Lược Kiểm Thử

### 1. Kiểm Thử Đơn Vị (Lên Kế Hoạch)

```python
def test_create_draft():
    client = VectCutClient()
    draft = client.create_draft()
    assert draft.draft_id is not None
```

### 2. Kiểm Thử Tích Hợp (Lên Kế Hoạch)

```python
def test_full_workflow():
    # Kiểm thử quy trình tạo video hoàn chỉnh
    ...
```

---

## Quan Hệ Phụ Thuộc

```
vectcut-skill
    │
    ├── Python 3.10+
    │
    ├── requests (Thư viện HTTP)
    │
    ├── dataclasses (Thư viện chuẩn Python)
    │
    ├── typing (Thư viện chuẩn Python)
    │
    └── VectCutAPI (Phụ thuộc bên ngoài)
            │
            ├── Flask
            ├── pyJianYingDraft
            └── JianYing/CapCut
```

---

## Kế Hoạch Tương Lai

### Mục Tiêu Ngắn Hạn

- [ ] Thêm kiểm thử đơn vị
- [ ] Thêm nhiều ví dụ workflow
- [ ] Hỗ trợ yêu cầu bất đồng bộ
- [ ] Thêm công cụ CLI

### Mục Tiêu Dài Hạn

- [ ] Hỗ trợ nhiều nền tảng video khác
- [ ] Giao diện Web UI
- [ ] Giải pháp triển khai trên cloud
- [ ] 插件系统

---

## 贡献指南

欢迎贡献代码！请遵循以下原则：

1. 保持 SKILL.md 简洁 (<500 行)
2. 详细内容放入 references/
3. 添加完整的类型注解
4. 编写清晰的文档字符串
5. 遵循 PEP 8 代码风格

---

## 参考资料

- [Claude Code Skills Documentation](https://github.com/anthropics/claude-code-skills)
- [VectCutAPI Documentation](https://github.com/sun-guannan/VectCutAPI)
- [Python Requests Documentation](https://docs.python-requests.org/)
