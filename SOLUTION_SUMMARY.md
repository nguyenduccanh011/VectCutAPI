# 🎯 Solution: Template Development & Preview

## 📌 Vấn đề gốc

> **User đặt ra**: Làm sao biết font size 24 hay 32, tốc độ animation như thế nào, màu sắc phù hợp không, mà không phải bịa ra con số?  
> **Và**: Nếu có sẵn dự án mẫu hay template draft, có thể convert thành template để tái sử dụng hay share không?

---

## ✅ Giải pháp

Tôi tạo cho bạn **5 tools & guides** để giải quyết vấn đề này:

### 1️⃣ **template_preview.py** - Preview template (không render)
🎯 **Mục đích**: Xem trước template settings trước khi commit
- Validate canvas, duration, effects
- Generate sample content automatically
- Analyze template ↔ content matching
- **Thời gian chạy**: < 1 giây

**Sử dụng**:
```bash
# Preview
python template_preview.py template/my-slideshow.json

# With detailed keyframes
python template_preview.py template/my-slideshow.json --detailed

# Compare with content
python template_preview.py template/my-slideshow.json content.json
```

### 2️⃣ **draft_to_template.py** - Export draft → template JSON
🎯 **Mục đích**: Chuyển existing draft (từ CapCut) thành template tái sử dụng
- List tất cả available drafts
- Extract canvas, transitions, effects
- Convert content → slots
- **Thời gian**: < 2 giây

**Sử dụng**:
```bash
# List drafts
python draft_to_template.py --list

# Export
python draft_to_template.py --draft "path/to/draft" "template-name" 5
```

### 3️⃣ **template_processor.py** - Render template (có sẵn)
🎯 **Mục đích**: Render video từ template
- Load template JSON
- Merge với content data
- Generate CapCut draft
- **Thời gian**: Tùy số ảnh/video

**Sử dụng**:
```python
processor = TemplateProcessor("template/my-slideshow.json")
result = processor.render({
    "image_0": "url1",
    "image_1": "url2",
    ...
})
```

### 4️⃣ **TEMPLATE_DEVELOPMENT_GUIDE.md** - Hướng dẫn development workflow
🎯 **Nội dung**:
- Chi tiết 3 cách phát triển template
- Step-by-step workflow từ design đến finalize
- Common adjustments (duration, transition, effects)
- Tips & best practices

### 5️⃣ **TEMPLATE_INTEGRATION_GUIDE.md** - Cách dùng tất cả tools cùng nhau
🎯 **Nội dung**:
- Complete workflow diagram
- Full example (end-to-end)
- API reference cho từng tool
- Troubleshooting guide

---

## 🎬 Workflow: Draft → Template → Reuse

```
┌────────────────────────────┐
│ 1. Design (CapCut UI)      │ ← Tạo draft, adjust settings
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ 2. Extract                 │ → python draft_to_template.py
│    (draft_to_template.py)  │
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ 3. Preview                 │ → python template_preview.py
│    (template_preview.py)   │   (check canvas, duration, effects)
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ 4. Customize (JSON edit)   │ ← Edit settings nếu cần
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ 5. Test Render             │ → TemplateProcessor.render()
│    (template_processor.py) │   (test with sample content)
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ 6. Finalize & Share        │ ← git commit, chia sẻ team
└────────────────────────────┘
```

---

## 🎓 3 Use Cases

### Use Case 1: Từ Draft Có Sẵn (Recommended ⭐⭐⭐⭐⭐)

**Scenario**: Bạn đã tạo một slideshow chuẩn trong CapCut, muốn reuse

**Workflow**:
```bash
# 1. Export
python draft_to_template.py --draft "C:\Path\To\CapCut\Draft\my-slideshow" "slideshow" 5

# 2. Preview
python template_preview.py template/slideshow.json

# 3. Test
python -c "
from template_processor import TemplateProcessor
processor = TemplateProcessor('template/slideshow.json')
result = processor.render({
    'image_0': 'url1',
    'image_1': 'url2',
    ...
})
"
```

**Ưu điểm**:
- ✅ Settings từ thực tế (không bịa)
- ✅ Nhanh (chỉ cần export)
- ✅ Chính xác (từ UI)

**Thời gian**: 5-10 phút

---

### Use Case 2: Customize Existing Template

**Scenario**: Có template rồi, muốn change duration, transition, v.v.

**Workflow**:
```python
# 1. Load & preview current
python template_preview.py template/slideshow-v1.json

# 2. Edit template/slideshow-v1.json
# (Change duration_per_slide: 3.0 → 4.0)

# 3. Preview again
python template_preview.py template/slideshow-v1.json

# 4. Test render
processor = TemplateProcessor("template/slideshow-v1.json")
result = processor.render(sample_content)
```

**Ưu điểm**:
- ✅ Iteration nhanh (không cần back to CapCut)
- ✅ Version control (track changes)
- ✅ Easy rollback

**Thời gian**: 10-15 phút

---

### Use Case 3: Tạo Template Mới từ Scratch

**Scenario**: Không có draft mẫu, tạo template hoàn toàn mới

**Workflow**:
```python
# 1. Create default
from template_processor import create_default_slideshow_template
template = create_default_slideshow_template()
# Customize...
with open("template/my-template.json", 'w') as f:
    json.dump(template, f)

# 2. Preview
python template_preview.py template/my-template.json

# 3. Test
processor = TemplateProcessor("template/my-template.json")
result = processor.render(sample_content)
```

**Ưu điểm**:
- ✅ Nhanh (không cần CapCut)
- ✅ Đơn giản (JSON-only)

**Hạn chế**:
- ❌ Cần test nhiều lần

**Thời gian**: 15-20 phút

---

## 📊 Before & After

### ❌ Before (Manual)
```
User: "Làm sao biết font size 24 hay 32?"
Dev: "Cứ tạo 10 draft test với size khác nhau"
Day: "Thử thử... 28px vẫn chưa phù hợp"
Week: "Cuối cùng match được nhưng quên settings"
```

### ✅ After (Template + Preview)
```
Dev: "Tạo 1 draft chuẩn"
Dev: "python draft_to_template.py" → template.json
Dev: "python template_preview.py" → xem settings
Dev: "Nếu cần adjust → edit JSON → preview lại"
Hour: "✨ Template sẵn sàng, reuse vĩnh viễn"
```

---

## 🎯 Key Features

### Feature 1: Template Preview (không render)
- ✅ Xem canvas, duration, effects
- ✅ Generate sample content automatically
- ✅ Validate structure
- ✅ **Tốc độ**: < 1 giây
- ✅ **Chi phí**: 0 API calls

### Feature 2: Draft Export
- ✅ Extract từ existing CapCut draft
- ✅ Auto-detect canvas, transitions
- ✅ Convert content → slots
- ✅ **Tốc độ**: < 2 giây

### Feature 3: Template Iteration
- ✅ Edit JSON → preview lại
- ✅ No need to go back to CapCut
- ✅ Version control changes
- ✅ Quick rollback

---

## 📚 Files Created

| File | Mục đích | Điểm mạnh |
|------|---------|----------|
| **template_preview.py** | Preview template | Fast, no API calls |
| **draft_to_template.py** | Export draft | Exact settings from UI |
| **TEMPLATE_DEVELOPMENT_GUIDE.md** | Step-by-step guide | Comprehensive |
| **TEMPLATE_INTEGRATION_GUIDE.md** | Tool integration | Complete examples |
| **...existing files** | Template processor | Production-ready |

---

## 🚀 Quick Start

### 5 Phút: Từ Draft sang Template

```bash
# 1. List & export (30 secs)
python draft_to_template.py --list
python draft_to_template.py --draft "path/to/draft" "my-slideshow" 5

# 2. Preview (30 secs)
python template_preview.py template/my-slideshow.json

# 3. Done! (in code)
from template_processor import TemplateProcessor
processor = TemplateProcessor("template/my-slideshow.json")
# Use to render
```

---

## 💡 Why This Solution is Better

| Tiêu chí | Before | After |
|---------|--------|-------|
| **Cách biết settings** | Bịa ra con số | Từ actual draft |
| **Tốc độ preview** | Manual testing (slow) | Auto (< 1s) |
| **Tái sử dụng** | Copy-paste mess | Clean JSON files |
| **Iteration** | Back to CapCut | Edit & preview |
| **Version control** | Khó tracking | git-friendly JSON |
| **Team sharing** | Không rõ | JSON file share |

---

## 📖 Learning Path

### Beginner (10 phút)
1. Đọc: [START_HERE.md](START_HERE.md)
2. Chạy: `python template_preview.py template/example.json`

### Intermediate (30 phút)
1. Đọc: [TEMPLATE_DEVELOPMENT_GUIDE.md](TEMPLATE_DEVELOPMENT_GUIDE.md)
2. Thực hành: Export một draft của bạn
3. Preview & customize

### Advanced (1 giờ)
1. Đọc: [TEMPLATE_INTEGRATION_GUIDE.md](TEMPLATE_INTEGRATION_GUIDE.md)
2. Tạo template workflow cho team
3. Setup version control

---

## 🎓 Examples

### Example 1: Quick export & preview
```bash
python draft_to_template.py --draft "/path/to/draft" "slideshow" 3
python template_preview.py template/slideshow.json
```

### Example 2: Full workflow in Python
```python
from draft_to_template import DraftToTemplateConverter
from template_preview import TemplatePreviewTool
from template_processor import TemplateProcessor

# Step 1: Export
converter = DraftToTemplateConverter("path/to/draft")
converter.print_summary()
converter.save_template("template/", "slideshow")

# Step 2: Preview
preview = TemplatePreviewTool("template/slideshow.json")
preview.print_preview()
sample = preview.generate_sample_content()

# Step 3: Test render
processor = TemplateProcessor("template/slideshow.json")
result = processor.render(sample)
print(f"✨ {result['draft_id']}")
```

---

## 🎯 Summary

**Vấn đề**: Làm sao biết settings (font, color, speed) phù hợp?  
**Giải pháp**: Export từ draft UICapCut → template JSON → preview code → iterate  
**Lợi ích**: Exact settings + fast iteration + version control + team sharing  
**Thời gian**: 5-15 phút per template, reuse forever  

---

**Ready to start? 🚀**

Next steps:
1. Read [TEMPLATE_DEVELOPMENT_GUIDE.md](TEMPLATE_DEVELOPMENT_GUIDE.md)
2. Create a test draft in CapCut
3. Run `python draft_to_template.py --draft "path" "test" 3`
4. Run `python template_preview.py template/test.json`
5. Share template with team!

Happy template building! 🎨✨
