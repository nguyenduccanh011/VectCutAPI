# 🎨 Template Development Guide
## Từ ý tưởng đến template sản phẩm

> **Vấn đề**: Làm sao biết font size 24 hay 32, tốc độ animation như thế nào, màu sắc phù hợp không?  
> **Giải pháp**: Xây dựng template từ **draft có sẵn**, rồi **preview & iterate** trước khi finalize

---

## 📋 3 Cách phát triển Template

### 🟢 Cách 1: Từ Draft có sẵn (Khuyến nghị)
**Thích hợp**: Đã có dự án mẫu trong CapCut, muốn reuse

**Workflow**:
```
Tạo draft mẫu in CapCut
        ↓
Export thành template JSON
        ↓
Preview & validate
        ↓
Test render
        ↓
Finalize & share
```

### 🟡 Cách 2: Từ Template mặc định (Nhanh)
**Thích hợp**: Bắt đầu nhanh, không có draft mẫu

**Workflow**:
```
Create default template
        ↓
Customize settings (JSON edit)
        ↓
Preview in code
        ↓
Test render
        ↓
Finalize
```

### 🔴 Cách 3: Hybrid (Tốt nhất)
**Thích hợp**: Kết hợp cả hai

**Workflow**:
```
1. Tạo draft mẫu (CapCut)
  ↓
2. Export → template JSON (draft_to_template.py)
  ↓
3. Customize → template (edit JSON)
  ↓
4. Preview & validate (template_preview.py)
  ↓
5. Test render (template_processor.py)
  ↓
6. Finalize & share
```

---

## 🎬 Chi tiết: Cách 1 - Từ Draft Có Sẵn

### Step 1: Tạo Draft Mẫu (trong CapCut)

**Mục tiêu**: Tạo một dự án demo trong CapCut với tất cả settings bạn muốn

**Làm gì**:
1. Mở CapCut
2. Tạo draft mới
3. Thêm ảnh/video (đủ cho 5-10 item)
4. Adjust effects, transitions, timings
   - Font size (nếu có text)
   - Màu sắc
   - Animation speed
   - Transition type & duration
5. **Lưu draft** → Nhớ tên: e.g., `slideshow-demo-v1`

### Step 2: Export Draft → Template

**Command**:
```bash
# Liệt kê drafts có sẵn
python draft_to_template.py --list

# Export specific draft
python draft_to_template.py --draft "C:\Path\To\CapCut\Draft\slideshow-demo-v1" "my-slideshow" 5
```

**Output**:
```
✅ Template exported: template/my-slideshow.json
   Canvas: 1280x720
   Slots: 5
```

**Điều gì xảy ra**:
- Script đọc `draft_info.json` từ draft folder
- Extract canvas size, fps, transitions
- Convert content items → slots
- Lưu thành template JSON

### Step 3: Preview & Validate Template

**Command**:
```bash
python template_preview.py template/my-slideshow.json
```

**Output kỳ vọng**:
```
📋 TEMPLATE PREVIEW: my-slideshow
==================================================

📺 Canvas:
   Resolution: 1280 × 720
   Aspect Ratio: 1.78:1

⏱️  Timing:
   Duration per slide: 3.0s
   Num slides: 5
   Transition type: Dissolve
   Transition duration: 0.5s
   ➜ Total duration estimate: 19.5s

✨ Effects/Keyframes (4 total):
   1. zoom
      Property: scale_x
      Animated: 1.0 → 1.3
   ...

✅ Validation:
   [✓] Canvas defined
   [✓] Has slots
   [✓] Has tracks
   [✓] Duration set
   [✓] Transition configured
```

### Step 4: Tùy chỉnh Settings (nếu cần)

**Edit `template/my-slideshow.json`**:

```json
{
  "settings": {
    "duration_per_slide": 4.0,  // ← Mỗi ảnh 4s thay vì 3s
    "transition": {
      "type": "CrossDissolve",   // ← Đổi transition
      "duration": 1.0            // ← Transition 1s
    }
  }
}
```

**Sau khi sửa, preview lại**:
```bash
python template_preview.py template/my-slideshow.json
```

### Step 5: Generate Sample Content & Test

**Command**:
```python
from template_preview import TemplatePreviewTool
from template_processor import TemplateProcessor

# Step 1: Preview
preview = TemplatePreviewTool("template/my-slideshow.json")
preview.print_preview()

# Step 2: Generate sample content
sample_content = preview.generate_sample_content()
print("Sample content URLs:", sample_content)

# Step 3: Test render
processor = TemplateProcessor("template/my-slideshow.json")
result = processor.render(sample_content)

if result["success"]:
    print(f"✨ Test render successful!")
    print(f"   Duration: {result['duration']}s")
    print(f"   Draft ID: {result['draft_id']}")
else:
    print(f"❌ Error: {result['error']}")
```

### Step 6: Finalize & Share

**Checklist**:
- [ ] Preview chạy ok
- [ ] Test render ok (without saving)
- [ ] Tất cả settings hợp lý
- [ ] Có document/README

**Commit template**:
```bash
# Lưu template vào git
git add template/my-slideshow.json
git add template/my-slideshow-INFO.md
git commit -m "Add slideshow template with 5 slots and zoom effect"

# Share: Push to repo hoặc gửi JSON file cho team
```

---

## 🔧 Chi tiết: Cách 2 - Từ Template Mặc định (Nhanh)

### Step 1: Create & Preview

```python
from template_processor import create_default_slideshow_template
from template_preview import TemplatePreviewTool
import json

# Create
template = create_default_slideshow_template()

# Customize (optional)
template["settings"]["duration_per_slide"] = 5.0
template["settings"]["transition"]["duration"] = 1.0

# Save
template_path = "template/my-slideshow-v2.json"
with open(template_path, 'w') as f:
    json.dump(template, f, indent=2)

# Preview
preview = TemplatePreviewTool(template_path)
preview.print_preview()
```

### Step 2: Test Render Immediately

```python
from template_processor import TemplateProcessor

processor = TemplateProcessor(template_path)
sample_content = {
    "image_0": "https://images.unsplash.com/photo-1...",
    "image_1": "https://images.unsplash.com/photo-2...",
    "image_2": "https://images.unsplash.com/photo-3...",
}

result = processor.render(sample_content)
```

---

## 📊 Bảng so sánh: Draft-based vs Template-based

| Tiêu chí | Cách 1: Draft-based | Cách 2: Template-based |
|---------|-----------------|-------------------|
| **Setup time** | 🟢 5-10 phút | 🟡 15-30 phút |
| **Trial & error** | 🟢 Dễ (CapCut UI) | 🟡 JSON editing |
| **Accuracy** | 🟢 100% (từ UI) | 🟡 Cần test |
| **Iteration** | 🟡 2. Quay lại CapCut | 🟢 Sửa JSON + preview |
| **Tốc độ iteration** | 🔴 Chậm | 🟢 Nhanh |
| **Phù hợp không-dev** | 🟢 Có | 🟡 Không rõ |

**Kết luận**: Cách 1 (Draft-based) tốt cho initial setup, sau đó dùng Cách 2 để iterate nhanh

---

## 🎯 Common Adjustments

### Tùy chỉnh Duration
```json
"duration_per_slide": 3.0  // Giây

// Ảnh hưởng: Mỗi ảnh dài bao lâu
// Recommend: 
//   - Slideshow: 3-4s
//   - Tutorial: 2-3s
//   - Story: 4-5s
```

### Tùy chỉnh Transition
```json
"transition": {
  "type": "Dissolve",        // Dissolve, CrossDissolve, Fade, v.v.
  "duration": 0.5            // Giây
}

// Recommend:
//   - Smooth: Dissolve (0.5s)
//   - Dynamic: CrossDissolve (1s)
//   - Minimal: Fade (0.3s)
```

### Thêm Effects  
```json
"keyframes": [
  {
    "property_type": "scale_x",
    "at_start": "1.0",
    "at_end": "1.25"    // Zoom 1.0→1.25
  },
  {
    "property_type": "position_x",
    "at_start": "-0.1",
    "at_end": "0.1"     // Pan from left to right
  }
]

// Recommend:
//   - Video: zoom + slight pan
//   - Product: zoom in + rotate
//   - Story: zoom + fade
```

---

## ⚠️ Common Issues

### ❌ Issue 1: "Template not found"
**Solution**: Chắc chắn file ở trong `template/` folder

### ❌ Issue 2: "Missing required slot"
**Solution**: Cung cấp content cho tất cả slots, hoặc giảm num_slots

### ❌ Issue 3: "JSON syntax error"
**Solution**: Validate JSON trước (jsonlint.com hoặc VSCode)

### ❌ Issue 4: Draft export không có keyframes
**Solution**: Draft của bạn có keyframes không? Check trong CapCut trước

---

## 📚 Tools & Commands

### Template Preview (xem trước, không render)
```bash
python template_preview.py template/my-slideshow.json
```

### Draft to Template (export from CapCut draft)
```bash
python draft_to_template.py --draft "path/to/draft" "template-name" 5
```

### Template Processor (render actual video)
```bash
python template_processor.py
```

### Validate JSON
```bash
python -m json.tool template/my-slideshow.json > /dev/null && echo "✅ Valid"
```

---

## 🚀 Workflow Checklist

### Phase 1: Design (CapCut)
- [ ] Tạo draft mẫu
- [ ] Adjust tất cả settings (effects, transitions, timing)
- [ ] Save draft

### Phase 2: Extract (Code)
- [ ] Export draft → template JSON
- [ ] Review extracted settings
- [ ] Customize nếu cần

### Phase 3: Validate (Code)
- [ ] Preview template (check canvas, duration, effects)
- [ ] Generate sample content
- [ ] Analyze template ↔ content matching

### Phase 4: Test (Code)
- [ ] Test render (không save)
- [ ] Check output looks correct
- [ ] Adjust template nếu cần

### Phase 5: Finalize (version control)
- [ ] Commit template
- [ ] Write README/documentation
- [ ] Share with team

---

## 💡 Tips & Best Practices

### Tip 1: Version control templates
```bash
git init
git add template/*.json
git commit -m "Initial templates"
git tag v1.0
```

### Tip 2: Template naming convention
```
template/{purpose}-{version}.json
template/slideshow-v1.json
template/kol-video-v2.json
template/tutorial-v1.json
```

### Tip 3: Speed up iteration
```python
# Instead of:
#   1. Edit JSON
#   2. Save
#   3. Run script
#   4. Check result

# Do this:
#   1. Load JSON in-memory
#   2. Edit dictionary
#   3. Preview
#   4. Save only if good
```

Example:
```python
import json
from template_preview import TemplatePreviewTool

with open("template/my-template.json") as f:
    template = json.load(f)

# Iterate
for duration in [2.0, 3.0, 4.0, 5.0]:
    template["settings"]["duration_per_slide"] = duration
    preview = TemplatePreviewTool(template)  # Load from dict
    print(f"Duration {duration}s → Estimated total: {preview.get_summary()['total_duration_estimate']:.1f}s")

# Save best version
with open("template/my-template.json", 'w') as f:
    json.dump(template, f, indent=2)
```

### Tip 4: Document template usage
```markdown
# Slideshow Template

## Purpose
Slideshow with zoom effect for product showcase

## Settings
- Duration: 3s per image
- Transition: Dissolve (0.5s)
- Effects: Zoom in (1.0 → 1.25)

## Slots
- image_0 to image_4 (5 images)

## Recommended content
- Product images (square or similar aspect ratio)
- Resolution: 1280x720+

## Example
```python
processor = TemplateProcessor("template/slideshow-v1.json")
result = processor.render({
    "image_0": "url1",
    "image_1": "url2",
    "image_2": "url3",
    "image_3": "url4",
    "image_4": "url5",
})
```
```

---

## 📞 Still confused?

### Q: Mình phải chỉnh sửa file JSON thì có khó không?
**A**: Không! JSON rất đơn giản. Dùng VSCode với extension "JSON" là ok

### Q: Phải có CapCut để dev template không?
**A**: Không bắt buộc. Có thể tạo từ template mặc định, nhưng có CapCut sẽ dễ hơn (visual feedback)

### Q: Template mình có thể dùng bao lâu?
**A**: Vĩnh viễn! Anh có thể lưu version control, reuse sau vài năm

### Q: Có thể chia sẻ template không?
**A**: Có! Template là file JSON, commit git hoặc email cho team

### Q: Preview và test render khác nhau gì?
**A**: 
- Preview: Chỉ xem settings, không gọi API add_image, v.v.
- Test render: Thực sự gọi MCP tools, tạo draft

---

**Ready to create templates? Let's go! 🚀**
