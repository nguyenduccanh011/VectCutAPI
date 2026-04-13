# 🔗 Template Development Integration Guide
## Cách sử dụng tất cả tools cùng nhau

---

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Template Development                       │
└─────────────────────────────────────────────────────────────┘

1️⃣  DESIGN PHASE (CapCut UI)
    └─ Tạo draft mẫu
    └─ Adjust effects, transitions, timing
    └─ Save draft → e.g., "slideshow-demo-v1"

           ↓

2️⃣  EXTRACT PHASE (draft_to_template.py)
    ┌─────────────────────────────┐
    │ python draft_to_template.py │
    │   --draft <path> <name>     │
    └─────────────────────────────┘
    └─ Export CapCut draft → template JSON
    └─ Output: template/slideshow-demo-v1.json

           ↓

3️⃣  PREVIEW PHASE (template_preview.py)
    ┌──────────────────────────────┐
    │ python template_preview.py   │
    │   <template_path>            │
    └──────────────────────────────┘
    └─ Validate canvas, duration, effects
    └─ Generate sample content
    └─ Analyze template structure

           ↓

4️⃣  CUSTOMIZE PHASE (JSON editing)
    └─ Edit template/slideshow-demo-v1.json
    └─ Adjust duration, transition, effects
    └─ Run preview again

           ↓

5️⃣  TEST PHASE (template_processor.py)
    ┌──────────────────────────────┐
    │ processor.render(content)    │
    └──────────────────────────────┘
    └─ Test with actual content
    └─ Verify result

           ↓

6️⃣  FINALIZE PHASE (version control)
    └─ git commit template/
    └─ Share with team
```

---

## 🎬 Complete Example: Slideshow Template

### Step 1: Design in CapCut

**In CapCut**:
1. Create new project
2. Add 5 images
3. Set each to 3 seconds
4. Add Dissolve transition (0.5s)
5. Add zoom effect on each image
6. Save as "slideshow-demo-v1"

### Step 2: List & Export Draft

```bash
# List available drafts
python draft_to_template.py --list

# Output:
# 📂 Available drafts in C:\Users\...\CapCut\Draft:
#    1. slideshow-demo-v1
#       Path: C:\Users\...\CapCut\Draft\slideshow-demo-v1

# Export
python draft_to_template.py \
  --draft "C:\Users\...\CapCut\Draft\slideshow-demo-v1" \
  "slideshow-v1" \
  5
```

**Output**:
```
✅ Template exported: template/slideshow-v1.json
   Canvas: 1280x720
   Slots: 5
```

### Step 3: Preview Template

```bash
python template_preview.py template/slideshow-v1.json
```

**Output**:
```
📋 TEMPLATE PREVIEW: slideshow-v1
==================================================

📺 Canvas:
   Resolution: 1280 × 720

⏱️  Timing:
   Duration per slide: 3.0s
   Num slides: 5
   Total duration: 19.5s

✨ Effects:
   - Zoom: scale_x (1.0 → 1.25)
   - Zoom: scale_y (1.0 → 1.25)

📁 Slots:
   • image_0
   • image_1
   • image_2
   • image_3
   • image_4

✅ Validation:
   [✓] Canvas defined
   [✓] Has slots
   [✓] Duration set
   [✓] Transition configured
```

### Step 4: Customize (Optional)

Edit `template/slideshow-v1.json`:

```json
{
  "settings": {
    "duration_per_slide": 4.0,    // ← Adjust to 4s
    "transition": {
      "type": "CrossDissolve",    // ← Change transition
      "duration": 1.0
    }
  }
}
```

Preview again:
```bash
python template_preview.py template/slideshow-v1.json
```

### Step 5: Test Render

```python
from template_processor import TemplateProcessor
from template_preview import TemplatePreviewTool

# Load template
preview = TemplatePreviewTool("template/slideshow-v1.json")

# Generate sample content
sample_content = preview.generate_sample_content()

# Test render
processor = TemplateProcessor("template/slideshow-v1.json")
result = processor.render(sample_content)

# Check result
if result["success"]:
    print(f"✨ Success!")
    print(f"   Draft ID: {result['draft_id']}")
    print(f"   Duration: {result['duration']}s")
else:
    print(f"❌ Error: {result['error']}")
```

### Step 6: Commit to Git

```bash
# Check status
git status

# Add template
git add template/slideshow-v1.json

# Optional: Add documentation
git add template/slideshow-v1-INFO.md

# Commit
git commit -m "Add slideshow template v1 with zoom effect"

# Tag
git tag "template-slideshow-v1"

# Push
git push origin main
```

---

## 🛠️ API Reference

### Tool 1: draft_to_template.py

```python
from draft_to_template import DraftToTemplateConverter

# Convert draft to template
converter = DraftToTemplateConverter("path/to/draft")

# Print summary
converter.print_summary()

# Convert
template = converter.to_template("my-template", num_slots=5)

# Save
output_file = converter.save_template("template/", "my-template", 5)

# Cleanup (if from zip)
converter.cleanup()
```

**Command line**:
```bash
# Export draft
python draft_to_template.py --draft "path/to/draft" "template-name" 5

# List drafts
python draft_to_template.py --list
```

---

### Tool 2: template_preview.py

```python
from template_preview import TemplatePreviewTool

# Load template
preview = TemplatePreviewTool("template/my-template.json")

# Get summary
summary = preview.get_summary()

# Preview (print)
preview.print_preview()

# Detailed keyframes
preview.print_detailed_keyframes()

# Generate sample content
sample_content = preview.generate_sample_content()

# Analyze template ↔ content
preview.print_content_analysis(content_data)

# Export info
preview.export_template_info("template/my-template-INFO.md")
```

**Command line**:
```bash
# Basic preview
python template_preview.py template/my-template.json

# Detailed preview
python template_preview.py template/my-template.json --detailed

# Compare with content
python template_preview.py template/my-template.json content.json
```

---

### Tool 3: template_processor.py

```python
from template_processor import TemplateProcessor

# Load template
processor = TemplateProcessor("template/my-template.json")

# Render
result = processor.render({
    "image_0": "https://...",
    "image_1": "https://...",
    ...
})

# Check result
if result["success"]:
    print(result["draft_id"])
    print(result["duration"])
```

---

## 📋 Checklists

### Template Creation Checklist

- [ ] **Design**: Created and tested draft in CapCut
- [ ] **Extract**: Exported draft to template JSON
- [ ] **Preview**: Ran template_preview.py successfully
- [ ] **Validate**: All validation checks passed ✓
- [ ] **Customize**: Made necessary adjustments (optional)
- [ ] **Test**: Test render successful with sample content
- [ ] **Document**: Created README/info file
- [ ] **Version Control**: Committed to git
- [ ] **Share**: Shared template with team (optional)

### Template Update Checklist

- [ ] **Edit**: Modified template JSON
- [ ] **Preview**: Re-previewed after changes
- [ ] **Test**: Test render again
- [ ] **Validate**: All tests pass
- [ ] **Version**: Updated version number in JSON
- [ ] **Commit**: Committed changes with message
- [ ] **Tag**: Tagged if major change

---

## 🎓 Examples

### Example 1: Simple workflow

```bash
# 1. Export
python draft_to_template.py --draft "path/to/draft" "slideshow" 3

# 2. Preview
python template_preview.py template/slideshow.json

# 3. Test
python -c "
from template_processor import TemplateProcessor
processor = TemplateProcessor('template/slideshow.json')
content = {
    'image_0': 'https://...',
    'image_1': 'https://...',
    'image_2': 'https://...',
}
result = processor.render(content)
print(f'✨ Success: {result[\"draft_id\"]}')" 
```

### Example 2: Complete Python script

```python
#!/usr/bin/env python3
"""
Complete template development workflow
"""

from draft_to_template import DraftToTemplateConverter, draft_to_template_workflow
from template_preview import TemplatePreviewTool
from template_processor import TemplateProcessor
import json

# Step 1: Convert draft to template
print("Step 1: Convert draft to template")
draft_path = "path/to/capcut/draft/slideshow-demo"
template_name = "slideshow-v1"
num_slots = 5

converter = DraftToTemplateConverter(draft_path)
converter.print_summary()
template = converter.to_template(template_name, num_slots)
template_path = converter.save_template("template", template_name)
converter.cleanup()

# Step 2: Preview template
print("\nStep 2: Preview template")
preview = TemplatePreviewTool(template_path)
preview.print_preview()
preview.print_detailed_keyframes()

# Step 3: Generate sample & test
print("\nStep 3: Test render")
sample_content = preview.generate_sample_content()
preview.print_content_analysis(sample_content)

processor = TemplateProcessor(template_path)
result = processor.render(sample_content)

if result["success"]:
    print(f"\n✨ Template created successfully!")
    print(f"   Draft ID: {result['draft_id']}")
    print(f"   Duration: {result['duration']}s")
    print(f"   Template: {template_path}")
else:
    print(f"\n❌ Error: {result['error']}")

# Step 4: Export info
print("\nStep 4: Export info")
preview.export_template_info(f"{template_path}.INFO.md")

print("\n✅ Complete!")
```

---

## 🚀 Tips for Team Collaboration

### Share Templates

```bash
# Create templates directory structure
templates/
├── slideshow-v1/
│   ├── template.json
│   ├── README.md
│   └── examples.json
├── kol-video-v1/
│   └── ...

# Version templates
git tag "templates/slideshow-v1"
git push origin --tags

# Team member clones
git clone <repo>
cd templates
ls  # See all available templates
```

### Template Registry (Optional)

Create `templates/REGISTRY.md`:

```markdown
# Template Registry

## Slideshow v1
- **Name**: slideshow-v1
- **Purpose**: Image slideshow with zoom effect
- **Slots**: 5 images
- **Duration**: 3s per image
- **Creator**: @alice
- **Created**: 2024-04-13
- **Status**: Production

## KOL Video v1
- **Name**: kol-video-v1
- **Purpose**: Product showcase video
- **Slots**: 2 videos + 3 images
- **Duration**: Custom
- **Creator**: @bob
- **Created**: 2024-04-12
- **Status**: Testing
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Draft not found"
```
Error: Draft not found: path/to/draft

Solution:
1. Check path is correct
2. Ensure draft is in CapCut folder
3. Use --list flag to find drafts:
   python draft_to_template.py --list
```

### Issue 2: "JSON parsing error"
```
Error: JSON parsing error in template

Solution:
1. Validate JSON:
   python -m json.tool template/my-template.json
2. Use VSCode with JSON extension
3. Check for trailing commas in JSON
```

### Issue 3: "Missing slots in content"
```
Error: Missing required content for slot: image_2

Solution:
1. Check template slots:
   python template_preview.py template/my-template.json
2. Provide content for all slots
3. Or reduce num_slots when converting
```

### Issue 4: "Preview works but render fails"
```
Error: Render failed - add_image_impl error

Solution:
1. Check image URLs are valid
2. Check network connection
3. Check CapCut server is running
4. Check draft folder permissions
```

---

## 📚 Summary

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **draft_to_template** | Extract from CapCut | Draft path | Template JSON |
| **template_preview** | Validate & analyze | Template JSON | Preview report |
| **template_processor** | Render video | Template + content | Draft ZIP |

**Workflow: Draft → Extract → Preview → Test → Finalize → Share**

---

**Ready to develop templates? 🚀**

Next: [TEMPLATE_DEVELOPMENT_GUIDE.md](TEMPLATE_DEVELOPMENT_GUIDE.md)
