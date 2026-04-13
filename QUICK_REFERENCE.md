# 📋 VectCutAPI Automation - Quick Reference

## 🎯 Chọn cách tiếp cận

```
Bạn là lập trình viên?
  ↓ Có → Pattern Template (Cách 1)
  ↓ Không → JSON Template (Cách 2)

Muốn hoàn toàn tự động?
  ↓ Có & không care chi phí → LLM Parser (Cách 3)
  ↓ Không → JSON Template (Cách 2)

Muốn dễ chia sẻ & bảo trì?
  ↓ Có → JSON Template (Cách 2) ⭐ BEST
```

---

## 🟡 Cách 2: JSON Template (Khuyến nghị)

### Đối tượng: Ai nên dùng?
- ✅ Bạn muốn tách biệt layout và nội dung
- ✅ Bạn cần dễ chia sẻ template
- ✅ Bạn chạy video bị lặp lại (slideshow, KOL, tutorial)
- ✅ Bạn muốn non-technical staff dùng được

### Các bước

#### Step 1: Tạo template JSON (lần đầu)

**Cách A: Tự tạo**
```python
# File: create_my_template.py
from template_processor import create_default_slideshow_template
import json

template = create_default_slideshow_template()
# Tùy chỉnh nếu cần
template["settings"]["duration_per_slide"] = 4.0

with open("template/my-slideshow.json", 'w') as f:
    json.dump(template, f, indent=2)

print("✅ Template created at template/my-slideshow.json")
```

**Cách B: Copy từ mẫu**
```bash
cp template/slideshow-template.json template/my-slideshow.json
# Chỉnh sửa file tại thư mục template/
```

#### Step 2: Chuẩn bị nội dung

```python
content_data = {
    "image_0": "https://images.unsplash.com/photo-1506905925346...?w=1280",
    "image_1": "https://images.unsplash.com/photo-1500534314209...?w=1280",
    "image_2": "https://images.unsplash.com/photo-1507525428034...?w=1280",
}
```

#### Step 3: Render

```python
from template_processor import TemplateProcessor

processor = TemplateProcessor("template/my-slideshow.json")
result = processor.render(content_data)

if result["success"]:
    print(f"✨ Video created: {result['draft_id']}")
    print(f"⏱️  Duration: {result['duration']:.1f}s")
else:
    print(f"❌ Error: {result['error']}")
```

---

## 🔴 Cách 1: Pattern Template

### Syntax nhanh

```python
from pattern.slideshow_template import SlideshowTemplate

# Basic
result = SlideshowTemplate.create_slideshow([
    "https://...",
    "https://...",
])

# With custom settings
result = SlideshowTemplate.create_slideshow(
    image_urls=["url1", "url2", "url3"],
    effects=["zoom_in", "pan_left_right"],
    DURATION_PER_SLIDE=4.0,
    TRANSITION_DUR=1.0,
    TRANSITION_TYPE="CrossDissolve"
)
```

---

## 🟢 Cách 3: LLM Parser (Advanced)

### TBD: Sẽ triển khai sau

---

## 🔧 Tùy chỉnh Template

### Tùy chỉnh thường gặp

```json
{
  "name": "slideshow-custom",
  "settings": {
    "canvas": {
      "width": 1920,        // 👈 Độ rộng video
      "height": 1080        // 👈 Độ cao video
    },
    "duration_per_slide": 5.0,    // 👈 Mỗi ảnh dài 5s
    "transition": {
      "type": "CrossDissolve",    // 👈 Kiểu transition
      "duration": 1.0             // 👈 Duration transition 1s
    }
  },
  "tracks": {
    "video": {
      "elements": [
        {
          "type": "image",
          "keyframes": [
            {
              "property_type": "scale_x",
              "at_start": "1.0",    // 👈 Giá trị lúc bắt đầu
              "at_end": "1.3"       // 👈 Giá trị lúc kết thúc (zoom to 1.3x)
            }
          ]
        }
      ]
    }
  },
  "slots": {
    "image_0": {"type": "image"},
    "image_1": {"type": "image"},
    "image_2": {"type": "image"}
    // 👈 Thêm image_3, image_4... cho slot khác
  }
}
```

### Các keyframe property phổ biến

| Property | at_start | at_end | Effect |
|----------|----------|--------|--------|
| `scale_x`, `scale_y` | `"1.0"` | `"1.25"` | Zoom in |
| `scale_x`, `scale_y` | `"1.25"` | `"1.0"` | Zoom out |
| `position_x` | `"-0.1"` | `"0.1"` | Pan left→right |
| `position_x` | `"0.1"` | `"-0.1"` | Pan right→left |
| `position_y` | `"-0.1"` | `"0.1"` | Pan bottom→top |
| `alpha` | `"0"` | `"1"` | Fade in |
| `rotation` | `"0"` | `"360"` | Spin 360° |

---

## 📊 Bảng so sánh chi tiết

| Tiêu chí | Pattern | JSON | LLM |
|---------|---------|------|-----|
| **Code lines** | 5-10 | 3-5 | 2-3 |
| **Khó tạo** | Dễ | Trung bình | Khó |
| **Khó custom** | Dễ | Trung bình | Khó |
| **Tái sử dụng** | Cao | Rất cao | Cao |
| **Dễ share** | Không | Có (JSON) | Không |
| **Thích hợp** | Dev | Production | Advanced |
| **Chi phí** | Free | Free | $$ (API) |

---

## 🎯 Use case & Khuyến nghị

### Slideshow video
✅ **Khuyến nghị**: JSON Template
```
Lý do: Cấu trúc cố định, tái sử dụng cao
```

### KOL/Influencer video
✅ **Khuyến nghị**: JSON Template
```
Lý do: Template layout cố định, chỉ thay nội dung
```

### Explainer/Tutorial video
✅ **Khuyến nghị**: Pattern Template
```
Lý do: Logic phức tạp, animation tùy chỉnh
```

### Event playlist
✅ **Khuyến nghị**: LLM Parser
```
Lý do: Đầu vào không chuẩn, cần parse
```

---

## 🐛 Common Issues & Solutions

### ❌ Issue 1: "Template not found: template/my-template.json"

**Nguyên nhân**: File template không ở đúng vị trí

**Giải pháp**:
```bash
# Kiểm tra file tồn tại
ls template/my-template.json

# Hoặc dùng Python
from pathlib import Path
print(Path("template/my-template.json").exists())

# Tạo file nếu chưa có
python template_examples.py 1
```

### ❌ Issue 2: "Missing required content for slot: image_0"

**Nguyên nhân**: Thiếu content cho slot nào đó

**Giải pháp**:
```python
# Template có 3 slots (image_0, image_1, image_2)
# Nhưng chỉ cung cấp 2 content

content_data = {
    "image_0": "url1",
    "image_1": "url2",
    # ❌ Thiếu image_2
}

# ✅ Fix: Cung cấp đủ
content_data = {
    "image_0": "url1",
    "image_1": "url2",
    "image_2": "url3",
}
```

### ❌ Issue 3: Render quá chậm

**Nguyên nhân**: Video quá dài, effect quá phức tạp

**Giải pháp**:
```json
{
  "settings": {
    "duration_per_slide": 1.0  // ← Giảm từ 3.0 xuống 1.0
  }
}
```

### ❌ Issue 4: Template JSON hỏng

**Nguyên nhân**: JSON syntax error

**Giải pháp**:
```python
import json

try:
    with open("template/my-template.json") as f:
        template = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ JSON Error: {e}")
    # Fix: Dùng online JSON validator
    # https://jsonlint.com/
```

---

## 💻 Lệnh hữu ích

```bash
# Chạy tất cả examples
python template_examples.py

# Chạy example cụ thể
python template_examples.py 1  # Basic slideshow
python template_examples.py 2  # Custom template

# Validate JSON template
python -m json.tool template/my-template.json

# Copy template mẫu
cp template/slideshow-template.json template/my-custom.json

# Kiểm tra template structure
python -c "import json; print(json.dumps(json.load(open('template/my-template.json')), indent=2)[:500])"
```

---

## 📚 Files tham khảo

| File | Mục đích |
|------|---------|
| `AUTOMATION_GUIDE.md` | Hướng dẫn chi tiết 3 cách |
| `QUICKSTART_TEMPLATES.md` | Quick start guide |
| `template_processor.py` | **Core file - xử lý template** |
| `template_examples.py` | Ví dụ thực hành |
| `pattern/slideshow_template.py` | Pattern template example |
| `template/*.json` | Template definitions |

---

## 🚀 Next Steps

### 1️⃣ Bắt đầu (5 phút)
```bash
python template_examples.py 2
```

### 2️⃣ Tạo template của bạn (10 phút)
```python
from template_processor import create_default_slideshow_template
import json

template = create_default_slideshow_template()
with open("template/my-template.json", 'w') as f:
    json.dump(template, f, indent=2)
```

### 3️⃣ Render slideshow (5 phút)
```python
from template_processor import TemplateProcessor

processor = TemplateProcessor("template/my-template.json")
result = processor.render({"image_0": "url1", "image_1": "url2"})
```

### 4️⃣ Integrate MCP (30 phút)
```python
# Thêm tool vào mcp_server.py
# (xem QUICKSTART_TEMPLATES.md)
```

---

## 🎓 Learning Path

**Beginner** → JSON Template → **Intermediate** → Pattern Template → **Advanced** → LLM Parser

---

**Happy creating! 🎬✨**
