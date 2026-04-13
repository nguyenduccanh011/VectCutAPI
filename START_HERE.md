# 🚀 START HERE - Tự động hóa VectCutAPI

> **Bạn đang ở đây**: Tìm hiểu cách tự động tạo video từ mô tả  
> **Mục tiêu**: Để MCP tạo video 100% tự động, không cần manual prompt từng bước

---

## 🎯 Vấn đề

**Hiện tại:**
```
User: "Tạo slideshow 3 ảnh"
↓
MCP: Cần 10+ bước manual
  1. create_draft
  2. add_image (ảnh 1)
  3. add_video_keyframe (effect 1)
  4. ... (lặp lại)
  10. save_draft
↓
⏰ Mất thời gian, dễ lỗi ❌
```

**Mục tiêu:**
```
User: "Tạo slideshow 3 ảnh"
↓
MCP: Tự động xử lý (1 bước)
  → render_template(template, content)
↓
✨ Nhanh, đơn giản, tái sử dụng ✅
```

---

## 📋 3 Cách giải quyết

Tôi đã tạo **3 lựa chọn** cho bạn:

### 🟢 **Cách 1: JSON Template** (Khuyến nghị hàng đầu)
- **Thích hợp**: 80% trường hợp
- **Độ khó**: Dễ (1-2 giờ setup)
- **Ưu điểm**: 
  - ✅ Dễ tạo, dễ chia sẻ (là file JSON)
  - ✅ Non-technical staff dùng được
  - ✅ Free (0 API cost)
  - ✅ Tái sử dụng cao
- **Nhược điểm**: Chỉ cho cấu trúc video cố định

### 🟡 **Cách 2: Pattern Template**
- **Thích hợp**: Video logic phức tạp
- **Độ khó**: Trung bình (1-2 giờ)
- **Ưu điểm**: 
  - ✅ Kiểm soát toàn bộ logic
  - ✅ Hỗ trợ animation phức tạp
- **Nhược điểm**: Chỉ cho lập trình viên

### 🔴 **Cách 3: LLM Parser** (Advanced)
- **Thích hợp**: Tự động 100% từ mô tả
- **Độ khó**: Khó (2-3 giờ)
- **Ưu điểm**: Hoàn toàn tự động
- **Nhược điểm**: $$ API cost, phức tạp

---

## 🎬 Bắt đầu từ đây (Cách 1: JSON Template)

### Step 1: Kiểm tra files (1 phút)

```bash
# Tất cả files đã tạo sẵn cho bạn:
ls -la
  • AUTOMATION_GUIDE.md          ← Hướng dẫn chi tiết
  • template_processor.py        ← 👑 File quan trọng
  • template_examples.py         ← Ví dụ
  • QUICKSTART_TEMPLATES.md      ← Quick start
  • QUICK_REFERENCE.md           ← Cheat sheet
```

### Step 2: Chạy demo (2 phút)

```bash
# Chạy ví dụ 2 (tạo slideshow custom)
python template_examples.py 2
```

**Output kỳ vọng:**
```
🎬 Rendering template: slideshow-5images-pan
...
✅ Kết quả:
   Success: true
   Draft ID: dfd_cat_...
   Duration: 20.0s (5 ảnh × 4s)
   Draft URL: https://...
```

### Step 3: Tạo template đầu tiên (5 phút)

Tạo file `my_first_template.py`:

```python
from template_processor import TemplateProcessor, create_default_slideshow_template
import json
import os

# Step 1: Tạo template mặc định
template = create_default_slideshow_template()

# Step 2: Tùy chỉnh nếu cần (optional)
template["settings"]["duration_per_slide"] = 4.0
template["settings"]["transition"]["duration"] = 1.0

# Step 3: Lưu template
os.makedirs("template", exist_ok=True)
template_path = "template/my-slideshow.json"
with open(template_path, 'w') as f:
    json.dump(template, f, indent=2)

print(f"✅ Template tạo thành công: {template_path}")

# Step 4: Load và test render
processor = TemplateProcessor(template_path)

content_data = {
    "image_0": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720",
    "image_1": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720",
    "image_2": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720",
}

result = processor.render(content_data)

if result["success"]:
    print(f"✨ Video tạo thành công!")
    print(f"   Draft ID: {result['draft_id']}")
    print(f"   Duration: {result['duration']:.1f}s")
else:
    print(f"❌ Error: {result['error']}")
```

Chạy nó:
```bash
python my_first_template.py
```

### Step 4: Tùy chỉnh template (5 phút)

Chỉnh sửa `template/my-slideshow.json`:

```json
{
  "settings": {
    "canvas": {"width": 1920, "height": 1080},    // 👈 Độ phân giải
    "duration_per_slide": 5.0,                     // 👈 Mỗi ảnh 5s
    "transition": {
      "type": "CrossDissolve",                     // 👈 Kiểu chuyển tiếp
      "duration": 1.0                              // 👈 Transition 1s
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
              "at_start": "1.0",
              "at_end": "1.3"                       // 👈 Zoom từ 1.0x → 1.3x
            }
          ]
        }
      ]
    }
  }
}
```

Sau đó render lại:
```bash
python my_first_template.py
```

### Step 5: Integrate MCP (10 phút) - Optional

Thêm vào `mcp_server.py`:

```python
{
    "name": "render_template",
    "description": "Create video from JSON template",
    "inputSchema": {
        "type": "object",
        "properties": {
            "template_name": {"type": "string", "description": "e.g., 'my-slideshow'"},
            "content": {"type": "object", "description": "e.g., {'image_0': 'url1', ...}"}
        },
        "required": ["template_name", "content"]
    }
}
```

Thêm handler:
```python
elif tool_name == "render_template":
    from template_processor import TemplateProcessor
    
    template_path = f"template/{arguments['template_name']}.json"
    processor = TemplateProcessor(template_path)
    result = processor.render(arguments["content"])
    
    return {"success": result["success"], "result": result}
```

Giờ có thể dùng:
```
User (via Claude): "Create slideshow from these 3 images"
↓
Claude calls: render_template(
    template_name="my-slideshow",
    content={"image_0": "url1", "image_1": "url2", "image_2": "url3"}
)
↓
Result: {"success": true, "draft_id": "..."}
```

---

## 📚 Tài liệu tham khảo

| File | Mục đích | Bắt đầu lúc nào |
|------|---------|-----------------|
| **QUICKSTART_TEMPLATES.md** | 5 phút quick start | Bây giờ |
| **AUTOMATION_GUIDE.md** | Chi tiết 3 cách | Sau khi chạy xong step 2 |
| **template_processor.py** | Source code | Khi muốn hiểu chi tiết |
| **template_examples.py** | Ví dụ 5 trường hợp | Step 2 của guide |
| **QUICK_REFERENCE.md** | Cheat sheet | Khi cần lookup nhanh |

---

## 🎯 Keyframe Properties (để tùy chỉnh effect)

Các properties có thể dùng cho keyframe:

```json
{
  "keyframes": [
    {
      "property_type": "scale_x",      // Zoom X (1.0 = bình thường, 1.25 = zoom)
      "at_start": "1.0",
      "at_end": "1.25"
    },
    {
      "property_type": "position_x",   // Pan left-right (-0.1 = trái, 0.1 = phải)
      "at_start": "-0.1",
      "at_end": "0.1"
    },
    {
      "property_type": "alpha",        // Fade (0 = mờ, 1 = rõ)
      "at_start": "0",
      "at_end": "1"
    },
    {
      "property_type": "rotation",     // Xoay (độ: 0-360)
      "at_start": "0",
      "at_end": "360"
    }
  ]
}
```

---

## ❓ FAQ

### Q: Tôi cần bao lâu để bắt đầu?
**A**: 5-10 phút nếu dùng template mặc định

### Q: Có thể dùng cho video nào?
**A**: 
- ✅ Slideshow
- ✅ KOL/Influencer video (template layout cố định)
- ✅ Tutorial (bước-bước video)
- ❌ Live action video phức tạp

### Q: Tôi có thể chia sẻ template không?
**A**: ✅ Có! File JSON có thể commit git, chia sẻ team

### Q: Có thể thêm âm thanh/text không?
**A**: ✅ Có! Mở rộng template để thêm audio, text tracks

### Q: Có thể chỉnh effect sau khi render không?
**A**: ✅ Có! Draft được lưu CapCut, bạn edit tiếp

### Q: Chi phí là bao nhiêu?
**A**: **Hoàn toàn FREE** (Cách 1 & 2). Chỉ có Cách 3 tốn API cost

---

## 🐛 Nếu gặp lỗi

```
❌ Error: "Template not found"
→ Kiểm tra file ở trong folder "template/"

❌ Error: "Missing required content"
→ Cung cấp content cho tất cả slots

❌ Render chậm
→ Giảm duration_per_slide: 1.0 thay vì 3.0

🩹 Nhận trong TROUBLESHOOTING ở QUICK_REFERENCE.md
```

---

## 📊 So sánh trước/sau

### ❌ Trước (Manual)
```python
# User phải:
add_image_impl(...)  # Step 1
add_video_keyframe_impl(...)  # Step 2
add_image_impl(...)  # Step 3
...  # 15+ steps

# Code: ~50 dòng
# Thời gian: 30 phút setup
# Tái sử dụng: Không (script khác nhau mỗi lần)
```

### ✅ Sau (Template)
```python
# User chỉ cần:
processor = TemplateProcessor("template/slideshow.json")
result = processor.render({"image_0": "url1", ...})

# Code: 2 dòng
# Thời gian: 5 phút setup
# Tái sử dụng: Cao (1 template dùng 100 videos)
```

---

## 🏁 Checklist hoàn thành

- [ ] Đọc file này (5 phút)
- [ ] Chạy `python template_examples.py 2` (2 phút)
- [ ] Tạo template đầu tiên (`my_first_template.py`) (5 phút)
- [ ] Tùy chỉnh template JSON (5 phút)
- [ ] Integrate MCP (optional, 10 phút)
- [ ] Chia sẻ template với team (git commit)

**Tổng thời gian: 30 phút - 1 giờ** ⏱️

---

## 🎉 Kết quả

Sau hoàn thành, bạn sẽ có:
- ✅ 1 template JSON sẵn sàng tái sử dụng
- ✅ Biết cách tạo template mới
- ✅ Có thể render video tự động
- ✅ MCP có thể gọi `render_template` thay vì 15 calls manual
- ✅ Team có thể share & reuse templates

---

**Bây giờ, hãy chạy Step 2**: 

```bash
python template_examples.py 2
```

**Hoặc đọc hướng dẫn chi tiết**: [QUICKSTART_TEMPLATES.md](QUICKSTART_TEMPLATES.md)

Happy creating! 🎬✨
