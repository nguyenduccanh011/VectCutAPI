# 🚀 Quick Start - Tự động hóa VectCutAPI

## ⏱️ 5 phút bắt đầu

### 1️⃣ Chuẩn bị các file cần thiết

Các file đã được tạo sẵn cho bạn:
- ✅ `AUTOMATION_GUIDE.md` - Hướng dẫn chi tiết (bạn đang đọc)
- ✅ `template_processor.py` - Template processor (xử lý template)
- ✅ `template_examples.py` - Ví dụ thực hành

### 2️⃣ Chạy ví dụ đơn giản nhất

```bash
# Chạy tất cả ví dụ (chỉ xem output)
python template_examples.py

# Chạy từng ví dụ cụ thể
python template_examples.py 1    # Basic slideshow
python template_examples.py 2    # Custom template
python template_examples.py 3    # Compare approaches
python template_examples.py 4    # Template anatomy
python template_examples.py 5    # MCP integration
```

### 3️⃣ Tạo slideshow đơn giản của bạn

```python
from template_processor import TemplateProcessor, create_default_slideshow_template
import json

# Step 1: Tạo template (nếu chưa có)
template = create_default_slideshow_template()
with open("template/my-slideshow.json", 'w') as f:
    json.dump(template, f, indent=2)

# Step 2: Chuẩn bị nội dung
content_data = {
    "image_0": "https://...",
    "image_1": "https://...",
    "image_2": "https://...",
}

# Step 3: Render
processor = TemplateProcessor("template/my-slideshow.json")
result = processor.render(content_data)

print(result)
# Output: {
#   "success": true,
#   "draft_id": "dfd_cat_...",
#   "duration": 9.0,
#   "draft_url": "https://..."
# }
```

---

## 📚 Ba cách tiếp cận

### 🟢 **Cách 1: Pattern Template** (Đơn giản nhất)
👉 Nếu bạn thích **code** và muốn **kiểm soát từng chi tiết**

**File**: `pattern/slideshow_template.py`

```python
from pattern.slideshow_template import SlideshowTemplate

result = SlideshowTemplate.create_slideshow(
    image_urls=["url1", "url2", "url3"],
    effects=["zoom_in", "pan_left_right"],
    DURATION_PER_SLIDE=3.0
)
```

✅ **Ưu điểm**: Dễ custom, có logic control  
❌ **Nhược điểm**: Chỉ cho lập trình viên  
⏱️ **Thời gian**: ~15 phút để tạo pattern mới

---

### 🟡 **Cách 2: JSON Template** (Khuyến nghị) ⭐⭐⭐⭐⭐
👉 Nếu bạn muốn **tách biệt layout và nội dung**, **dễ chia sẻ**

**File**: `template_processor.py`

```python
processor = TemplateProcessor("template/slideshow.json")
result = processor.render({
    "image_0": "url1",
    "image_1": "url2",
})
```

✅ **Ưu điểm**: Linh hoạt, dễ share, có thể dùng từ UI  
✅ **Nhược điểm**: Tương đối dễ  
⏱️ **Thời gian**: ~30 phút cho production template  

🎯 **Khuyến nghị cho 80% trường hợp sử dụng**

---

### 🔴 **Cách 3: LLM Parser** (Phức tạp)
👉 Nếu bạn muốn **100% tự động từ lời mô tả**, không care chi phí API

**File**: `llm_parser.py` (cần tạo)

```python
parser = VideoDescriptionParser("schema.json")
plan = parser.parse("Tạo slideshow 5 ảnh với zoom effect")
# Output: {"template": "slideshow", "params": {...}}
```

✅ **Ưu điểm**: Hoàn toàn tự động  
❌ **Nhược điểm**: Phức tạp, tốn API calls  
⏱️ **Thời gian**: ~1 giờ để triển khai

---

## 🎯 Tạo Template JSON của riêng bạn

### Cách 1: Từ file mẫu

```python
from template_processor import create_template_file

# Tạo template 5 slides
create_template_file("my-template", num_slides=5)
# Tạo file: template/my-template-template.json
```

### Cách 2: Tải template có sẵn

```json
{
  "name": "slideshow-deluxe",
  "settings": {
    "canvas": {"width": 1920, "height": 1080},
    "duration_per_slide": 5.0,
    "transition": {"type": "CrossDissolve", "duration": 1.0}
  },
  "tracks": {...},
  "slots": {...}
}
```

### Cách 3: Chỉnh sửa JSON trực tiếp

Các tham số có thể tùy chỉnh:

| Tham số | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `duration_per_slide` | Mỗi ảnh dài bao lâu (giây) | `3.0`, `4.0` |
| `transition.type` | Kiểu transition | `"Dissolve"`, `"CrossDissolve"` |
| `transition.duration` | Duration transition (giây) | `0.5`, `1.0` |
| `at_start` / `at_end` | Giá trị keyframe đầu/cuối | `"1.0"`, `"1.25"` |

Ví dụ: Thay đổi zoom duration từ 3s thành 5s

```json
{
  "settings": {
    "duration_per_slide": 5.0  // ← Thay này
  }
}
```

---

## 🔌 Integrate vào MCP Server

### Step 1: Thêm tool definition

Trong `mcp_server.py`, thêm:

```python
{
    "name": "render_slideshow",
    "description": "Create slideshow from template",
    "inputSchema": {
        "type": "object",
        "properties": {
            "template_name": {"type": "string"},
            "images": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["template_name", "images"]
    }
}
```

### Step 2: Thêm handler

Trong `execute_tool()`:

```python
elif tool_name == "render_slideshow":
    from template_processor import TemplateProcessor
    
    template_path = f"template/{arguments['template_name']}-template.json"
    processor = TemplateProcessor(template_path)
    
    # Tạo content map
    content_map = {
        f"image_{i}": url 
        for i, url in enumerate(arguments["images"])
    }
    
    result = processor.render(content_map)
    return {"success": result["success"], "result": result}
```

### Step 3: Sử dụng

```
User: "Create slideshow from 3 images"
↓
Copilot calls: render_slideshow(
    template_name="slideshow-basic",
    images=["url1", "url2", "url3"]
)
↓
Result: {"success": true, "draft_id": "..."}
```

---

## 📊 So sánh kết quả

### Trước (Manual)
```
User prompt → 15-20 MCP calls → Phức tạp, dễ lỗi ❌
```

### Sau (Template)
```
User mô tả → 1 MCP call → Đơn giản, tái sử dụng ✅
```

**Tiết kiệm**: 75% API calls, 80% code, 100% nhẫn nại 😄

---

## 🎬 Danh sách templates có sẵn

Các templates bạn có thể tạo thêm:

| Template | Mục đích | Độ phức tạp |
|----------|---------|-----------|
| `slideshow-basic` | Slideshow đơn giản + zoom | 🟢 Dễ |
| `slideshow-with-text` | Slideshow + text overlay | 🟡 Trung bình |
| `kol-video` | Video KOL/influencer | 🟡 Trung bình |
| `tutorial` | Video hướng dẫn step-by-step | 🟡 Trung bình |
| `carousel-3d` | Carousel effect 3D | 🔴 Khó |
| `montage` | Montage với nhiều effects | 🔴 Khó |

---

## 🐛 Troubleshooting

### ❌ Error: "Template not found"
```
✅ Giải pháp: Chắc chắn file JSON nằm trong folder "template/"
   Ví dụ: template/slideshow-basic-template.json
```

### ❌ Error: "Missing required content for slot"
```
✅ Giải pháp: Cung cấp đủ content cho tất cả slots
   Ví dụ: {"image_0": "url1", "image_1": "url2", "image_2": "url3"}
```

### ❌ Render chậm
```
✅ Giải pháp: Giảm duration_per_slide hoặc số lượng images
   Ví dụ: duration_per_slide: 1.0 (vừa nhanh, vừa đủ hiệu ứng)
```

---

## 📚 Tài liệu tham khảo

- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - Chi tiết 3 cách tiếp cận
- [template_processor.py](template_processor.py) - Source code
- [template_examples.py](template_examples.py) - Ví dụ thực hành
- [test_slideshow.py](test_slideshow.py) - Test slideshow (cách cũ)

---

## 💡 Tips & Tricks

### Tip 1: Tạo template library
```bash
mkdir -p template/library/
# Tạo các template mẫu sử dụng nhiều
# - slideshow-basic.json
# - slideshow-deluxe.json
# - kol-video.json
```

### Tip 2: Version control templates
```bash
# Templates là file JSON, có thể track bằng git
git add template/*.json
git commit -m "Add new slideshow template"
```

### Tip 3: Template validation
```python
# Validate template trước render
processor = TemplateProcessor("template/my-template.json")
processor.validate_content_map(content_data)
# → True/False
```

---

## 🏆 Recap

### ✅ Bạn đã học được:
1. 3 cách tự động hóa video creation
2. Cách tạo JSON template
3. Cách sử dụng TemplateProcessor
4. Cách integrate với MCP

### 🎯 Next steps:
1. ✅ Chạy `python template_examples.py` để xem examples
2. ✅ Tạo template đầu tiên của bạn
3. ✅ Test với `TemplateProcessor.render()`
4. ✅ Integrate vào MCP server
5. ✅ Share templates với team

---

**Happy templating! 🎬🎉**
