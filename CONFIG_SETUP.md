# 🔧 Hướng dẫn cấu hình CapCut Draft Folder

## 📍 Vấn đề

Khi clone dự án trên máy khác, đường dẫn CapCut/JianYing draft folder thường khác nhau tùy theo:
- Tên người dùng Windows/macOS
- Vị trí cài đặt CapCut

**Giải pháp:** Thay vì hardcode, đường dẫn được lưu trong `config.json`.

---

## ✅ Cách cấu hình (chỉ cần làm 1 lần)

### Bước 1: Tìm đường dẫn draft folder của bạn

**Windows - CapCut:**
```
C:\Users\<YourUsername>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft
```

**Windows - JianYing Pro:**
```
C:\Users\<YourUsername>\AppData\Local\ByteDance\JianyingPro\User Data\Projects\com.lveditor.draft
```

**macOS - CapCut:**
```
/Users/<YourUsername>/Movies/CapCut/User Data/Projects/com.lveditor.draft
```

**macOS - JianYing Pro:**
```
/Users/<YourUsername>/Movies/JianyingPro/User Data/Projects/com.lveditor.draft
```

### Bước 2: Sửa file `config.json`

Mở `config.json` và thêm dòng `"draft_folder"`:

```json
{
  "is_capcut_env": true,
  "draft_domain": "https://www.capcutapi.top",
  "port": 9001,
  "preview_router": "/draft/downloader",
  "is_upload_draft": false,
  "draft_folder": "C:/Users/<YourUsername>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft"
}
```

**⚠️ Lưu ý:** 
- Windows: Dùng forward slash `/` (không backslash `\`)
- Thay `<YourUsername>` bằng tên user thực của bạn
- Dùng đúng cách từ Bước 1 tùy hệ điều hành

### Bước 3: Xác minh đường dẫn

Mở terminal và kiểm tra:

**Windows:**
```powershell
Test-Path "C:/Users/<YourUsername>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft"
```

**macOS/Linux:**
```bash
test -d "/Users/<YourUsername>/Movies/CapCut/User Data/Projects/com.lveditor.draft" && echo "exists"
```

---

## 📦 Cấu trúc tự động tìm đường dẫn

Khi bạn chạy script:

1. **example.py** import từ `settings/local.py`
2. **settings/local.py** đọc từ `config.json`
3. Nếu không tìm thấy `draft_folder` trong `config.json` → dùng giá trị default (fallback)

```python
CAPCUT_DRAFT_FOLDER = DRAFT_FOLDER or "C:/Users/DUC CANH PC/..."
```

---

## 🎯 Kiểm tra setup đã đúng

Chạy test script:

```bash
python test_flow.py
python test_slideshow.py
```

Nếu draft được lưu vào CapCut folder → cấu hình đúng ✅

---

## ❓ Thường gặp

### Q: Làm sao biết tên user của mình?

**Windows:**
```powershell
$env:USERNAME
```

**macOS/Linux:**
```bash
whoami
```

### Q: Draft vẫn nằm ở project folder, không vào CapCut?

→ Đường dẫn trong `config.json` không đúng. Kiểm tra lại Bước 1-2.

### Q: Có thể để trống `draft_folder` không?

Có, script sẽ dùng default. Nhưng nếu default không khớp username của bạn → draft sẽ không vào CapCut.

---

## 📝 Environment variable (tùy chọn)

Nếu muốn dùng environment variable thay vì config.json:

```bash
set CAPCUT_DRAFT_FOLDER="C:/Users.../com.lveditor.draft"  # Windows
export CAPCUT_DRAFT_FOLDER="/Users.../com.lveditor.draft"  # macOS
```

Sau đó sửa `settings/local.py`:
```python
DRAFT_FOLDER = os.getenv("CAPCUT_DRAFT_FOLDER") or local_config.get("draft_folder")
```
