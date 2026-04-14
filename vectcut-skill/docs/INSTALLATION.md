# Hướng Dẫn Cài Đặt

Tài liệu này cung cấp hướng dẫn cài đặt chi tiết cho VectCutAPI Skill.

---

## Mục Lục

1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt VectCutAPI](#cài-đặt-vectcutapi)
3. [Cài Đặt Skill](#cài-đặt-skill)
4. [Xác Minh Cài Đặt](#xác-minh-cài-đặt)
5. [Gỡ Cài Đặt](#gỡ-cài-đặt)

---

## Yêu Cầu Hệ Thống

### Các Thành Phần Bắt Buộc

| Thành Phần | Phiên Bản Tối Thiểu | Phiên Bản Được Đề Xuất | Liên Kết Tải |
|------|----------|----------|----------|
| Python | 3.10 | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Claude Code | Mới Nhất | Mới Nhất | [claude.com](https://claude.com/claude-code) |
| JianYing/CapCut | Mới Nhất | Mới Nhất | [capcut.com](https://www.capcut.com/) |

### Các Thành Phần Tùy Chọn

| Thành Phần | Mục Đích | Liên Kết Tải |
|------|------|----------|
| FFmpeg | Xử Lý Video | [ffmpeg.org](https://ffmpeg.org/download.html) |
| Git | Kiểm Soát Phiên Bản | [git-scm.com](https://git-scm.com/downloads) |

### Hỗ Trợ Hệ Điều Hành

- **Windows**: Windows 10/11 (Được Đề Xuất)
- **macOS**: macOS 11+ (Big Sur hoặc Cao Hơn)
- **Linux**: Ubuntu 20.04+, Debian 11+, CentOS 8+

---

## Cài Đặt VectCutAPI

VectCutAPI là dịch vụ cốt lõi mà kỹ năng này phụ thuộc vào.

### Cài Đặt Windows

#### Bước 1: Cài Đặt Python

1. Truy cập [python.org](https://www.python.org/downloads/)
2. Tải xuống Python 3.10 hoặc cao hơn
3. Chạy trình cài đặt, **Hãy Chắc Chắn Đánh Dấu "Add Python to PATH"**
4. Xác Minh Cài Đặt:
   ```cmd
   python --version
   ```

#### Bước 2: Nhân Bản Dự Án

```cmd
# Sử Dụng Git (Được Đề Xuất)
git clone https://github.com/sun-guannan/VectCutAPI.git
cd VectCutAPI

# Hoặc Tải Trực Tiếp ZIP
# https://github.com/sun-guannan/VectCutAPI/archive/refs/heads/main.zip
```

#### Bước 3: Tạo Môi Trường Ảo

```cmd
# Tạo Môi Trường Ảo
python -m venv venv-vectcut

# Kích Hoạt Môi Trường Ảo
venv-vectcut\Scripts\activate

# Xác Minh Kích Hoạt (Tiền Tố Dòng Lệnh Sẽ Hiển Thị (venv-vectcut))
```

#### Bước 4: Cài Đặt Phụ Thuộc

```cmd
# Nâng Cấp pip
python -m pip install --upgrade pip

# Cài Đặt Phụ Thuộc Cơ Bản
pip install -r requirements.txt

# Cài Đặt Hỗ Trợ MCP (Tùy Chọn)
pip install -r requirements-mcp.txt
```

#### Bước 5: Cấu Hình

```cmd
# Sao Chép Tệp Cấu Hình
copy config.json.example config.json

# Chỉnh Sửa Cấu Hình Bằng Notepad
notepad config.json
```

Sửa Đổi Các Loại Cấu Hình Khi Cần Thiết:

```json
{
  "is_capcut_env": true,
  "draft_domain": "https://www.capcutapi.top",
  "port": 9001,
  "preview_router": "/draft/downloader",
  "is_upload_draft": false
}
```

#### Bước 6: Khởi Động Dịch Vụ

```cmd
# Khởi Động HTTP API Server
python capcut_server.py

# Dịch Vụ Sẽ Khởi Động Tại http://localhost:9001
```

### Cài Đặt macOS/Linux

#### Bước 1: Cài Đặt Python

**macOS:**
```bash
# Sử Dụng Homebrew (Được Đề Xuất)
brew install python@3.11

# Hoặc Tải Gói Cài Đặt Từ Trang Web Chính Thức
# https://www.python.org/downloads/
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**CentOS/RHEL:**
```bash
sudo yum install python311 python311-pip
```

#### Bước 2: Nhân Bản Dự Án

```bash
git clone https://github.com/sun-guannan/VectCutAPI.git
cd VectCutAPI
```

#### Bước 3: Tạo Môi Trường Ảo

```bash
# Tạo Môi Trường Ảo
python3 -m venv venv-vectcut

# Kích Hoạt Môi Trường Ảo
source venv-vectcut/bin/activate
```

#### Bước 4: Cài Đặt Phụ Thuộc

```bash
# Nâng Cấp pip
python -m pip install --upgrade pip

# Cài Đặt Phụ Thuộc Cơ Bản
pip install -r requirements.txt

# Cài Đặt Hỗ Trợ MCP (Tùy Chọn)
pip install -r requirements-mcp.txt
```

#### Bước 5: Cấu Hình

```bash
# Sao Chép Tệp Cấu Hình
cp config.json.example config.json

# Chỉnh Sửa Cấu Hình
nano config.json  # Hoặc Sử Dụng vim, Trình Chỉnh Sửa Khác
```

#### Bước 6: Khởi Động Dịch Vụ

```bash
# Khởi Động HTTP API Server
python capcut_server.py

# Dịch Vụ Sẽ Khởi Động Tại http://localhost:9001
```

---

## Cài Đặt Skill

### Cài Đặt Windows

#### Phương Pháp 1: Sử Dụng Git (Được Đề Xuất)

```powershell
# Nhân Bản Dự Án
git clone https://github.com/your-username/vectcut-skill.git
cd vectcut-skill

# Sao Chép Tệp Skill
Copy-Item -Path "skill\*" -Destination "$env:USERPROFILE\.claude\skills\public\vectcut-api\" -Recurse -Force
```

#### Phương Pháp 2: Sao Chép Thủ Công

1. Tải Tệp ZIP Của Dự Án
2. Giải Nén Vào Thư Mục Bất Kỳ
3. Sao Chép Nội Dung Thư Mục `skill` Vào:
   ```
   C:\Users\Tên Người Dùng Của Bạn\.claude\skills\public\vectcut-api\
   ```

#### Phương Pháp 3: Sử Dụng CMD

```cmd
xcopy "skill\*" "%USERPROFILE%\.claude\skills\public\vectcut-api\" /E /I /Y
```

### Cài Đặt macOS/Linux

```bash
# Nhân Bản Dự Án
git clone https://github.com/your-username/vectcut-skill.git
cd vectcut-skill

# Sao Chép Tệp Skill
cp -r skill/* ~/.claude/skills/public/vectcut-api/

# Hoặc Tạo Liên Kết Tượng Trưng (Được Đề Xuất)
ln -s $(pwd)/skill ~/.claude/skills/public/vectcut-api
```

---

## Xác Minh Cài Đặt

### 1. Xác Minh Dịch Vụ VectCutAPI

```bash
# Sử Dụng curl
curl http://localhost:9001/

# Hoặc Sử Dụng Trình Duyệt Để Truy Cập
# http://localhost:9001/
```

Bạn Sẽ Thấy Trang Tài Liệu API.

### 2. Xác Minh Tệp Skill

```bash
# Windows
dir %USERPROFILE%\.claude\skills\public\vectcut-api

# Linux/macOS
ls -la ~/.claude/skills/public/vectcut-api
```

Bạn Sẽ Thấy Các Tệp Sau:
```
SKILL.md
scripts/
  └── vectcut_client.py
references/
  ├── api_reference.md
  └── workflows.md
assets/
  └── examples/
```

### 3. Xác Minh Tích Hợp Claude Code

1. Khởi Động Claude Code
2. Nhập Lệnh Kiểm Tra:
   ```
   Sử Dụng vectcut-api skill để tạo bản nháp video
   ```
3. Claude Sẽ Tự Động Xác Định Và Tải Kỹ Năng

### 4. Chạy Kịch Bản Kiểm Tra

Tạo Tệp Kiểm Tra `test_installation.py`:

```python
from skill.scripts.vectcut_client import VectCutClient

def test_installation():
    """Kiểm Tra Xem Cài Đặt Có Thành Công Hay Không"""
    print("Kiểm Tra Kết Nối VectCutAPI...")

    try:
        # Tạo Máy Khách
        client = VectCutClient("http://localhost:9001")

        # Kiểm Tra Tạo Bản Nháp
        draft = client.create_draft(width=1080, height=1920)
        print(f"✓ Bản Nháp Tạo Thành Công: {draft.draft_id}")

        # Kiểm Tra Lưu Bản Nháp
        result = client.save_draft(draft.draft_id)
        print(f"✓ Bản Nháp Lưu Thành Công: {result.draft_url}")

        print("\n✅ Xác Minh Cài Đặt Thành Công!")
        return True

    except Exception as e:
        print(f"\n❌ Xác Minh Cài Đặt Thất Bại: {e}")
        return False

if __name__ == "__main__":
    test_installation()
```

Chạy Kiểm Tra:
```bash
python test_installation.py
```

---

## Gỡ Cài Đặt

### Gỡ Cài Đặt Windows

#### Gỡ Cài Đặt Skill

```cmd
# Xóa Thư Mục Skill
rmdir /s /q %USERPROFILE%\.claude\skills\public\vectcut-api
```

#### Gỡ Cài Đặt VectCutAPI

```cmd
# Dừng Dịch Vụ (Ctrl+C)

# Kích Hoạt Môi Trường Ảo
venv-vectcut\Scripts\activate

# Gỡ Cài Đặt Phụ Thuộc
pip freeze | xargs pip uninstall -y

# Thoát Môi Trường Ảo
deactivate

# Xóa Thư Mục Dự Án
rmdir /s /q VectCutAPI
```

### Gỡ Cài Đặt macOS/Linux

#### Gỡ Cài Đặt Skill

```bash
# Xóa Thư Mục Skill
rm -rf ~/.claude/skills/public/vectcut-api
```

#### Gỡ Cài Đặt VectCutAPI

```bash
# Dừng Dịch Vụ (Ctrl+C)

# Kích Hoạt Môi Trường Ảo
source venv-vectcut/bin/activate

# Gỡ Cài Đặt Phụ Thuộc
pip freeze | xargs pip uninstall -y

# Thoát Môi Trường Ảo
deactivate

# Xóa Thư Mục Dự Án
rm -rf VectCutAPI
```

---

## Các Câu Hỏi Thường Gặp

### Q1: Phiên Bản Python Không Tương Thích

**Vấn Đề**: `Python version error`

**Giải Pháp**:
```bash
# Kiểm Tra Phiên Bản Python
python --version

# Nếu Phiên Bản Dưới 3.10, Vui Lòng Nâng Cấp Python
```

### Q2: Cổng 9001 Bị Chiếm Dụng

**Vấn Đề**: `Port 9001 already in use`

**Giải Pháp**:
```bash
# Windows - Tìm Quy Trình Chiếm Cổng
netstat -ano | findstr :9001

# Chấm Dứt Quy Trình (Sử Dụng PID)
taskkill /PID <PID> /F

# Hoặc Sửa Đổi Cổng Trong config.json
```

### Q3: Cài Đặt Phụ Thuộc Pip Thất Bại

**Vấn Đề**: `pip install failed`

**Giải Pháp**:
```bash
# Nâng Cấp pip
python -m pip install --upgrade pip

# Sử Dụng Nguồn Gương Trong Nước
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: Claude Code Không Thể Tìm Thấy Skill

**Vấn Đề**: `Skill not found`

**Giải Pháp**:
1. Kiểm Tra Đường Dẫn Thư Mục Skill Có Chính Xác Không
2. Xác Nhận Tệp SKILL.md Tồn Tại Và Định Dạng Chính Xác
3. Khởi Động Lại Claude Code

### Q5: Kích Hoạt Môi Trường Ảo Thất Bại

**Vấn Đề**: `venv activation failed`

**Giải Pháp**:
```bash
# Windows - Chạy PowerShell Với Quyền Quản Trị Viên
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Kích Hoạt Lại
venv-vectcut\Scripts\Activate.ps1
```

---

## Bước Tiếp Theo

Sau Khi Cài Đặt Xong, Bạn Nên Xem Qua:

1. [Hướng Dẫn Sử Dụng](USAGE.md) - Học Cách Sử Dụng
2. [Ví Dụ Workflow](skill/references/workflows.md) - Xem Các Trường Hợp Thực Tế
3. [Tham Khảo API](skill/references/api_reference.md) - Tìm Hiểu API Đầy Đủ

---

## Nhận Trợ Giúp

Nếu Gặp Vấn Đề:

1. Xem Phần [Khắc Phục Sự Cố](USAGE.md#khắc-phục-sự-cố)
2. Tìm Kiếm [Issues](https://github.com/your-username/vectcut-skill/issues)
3. Tạo Issue Mới
4. Liên Hệ Dự Án Gốc [VectCutAPI](https://github.com/sun-guannan/VectCutAPI)
