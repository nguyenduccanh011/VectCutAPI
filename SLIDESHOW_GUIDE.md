# 🎬 Image Slideshow Creator - VectCut API

Tạo video slideshow ghép 3 ảnh từ internet bằng VectCut API.

## 📋 Yêu Cầu

- VectCut API Server đang chạy (`capcut_server.py` trên port 9001)
- Python 3.10+
- Kết nối internet

## 🚀 Cách Sử Dụng

### 1. **Simple - Slideshow Demo (Khuyến Nghị)**

Tạo slideshow 3 ảnh từ internet tự động:

```bash
python create_slideshow_advanced.py
```

**Kết quả:**
- Tạo 3 ảnh sequence (3 giây mỗi ảnh)
- Thêm hiệu ứng zoom-in/zoom-out
- Thêm tiêu đề cho mỗi ảnh
- Tạo URL preview

**Output:**
```
📺 Preview URL: https://cc-vectcut-preview.oss-accelerate.aliyuncs.com/...
```

### 2. **Custom Images**

Tạo slideshow với ảnh tùy chỉnh:

```bash
python create_slideshow_advanced.py --custom \
  "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80" \
  "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=1920&q=80" \
  "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?w=1920&q=80"
```

### 3. **Basic Script**

Tạo slideshow cơ bản:

```bash
python create_image_slideshow.py
```

## 📸 Nguồn Ảnh Miễn Phí

Có thể sử dụng ảnh từ các nguồn sau:

### Unsplash (Miễn phí, không cần credit)
```
https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80
https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=1920&q=80
https://images.unsplash.com/photo-1495567720989-cebdbdd97913?w=1920&q=80
```

### Pixabay
```
https://pixabay.com/images/... (thêm /download tại cuối)
```

### Pexels
```
https://www.pexels.com/...
```

## 🎨 Tùy Chỉnh

### Thay Đổi Kích Thước

```python
slideshow = ImageSlideshow(width=1080, height=1920)  # Dọc màn hình
slideshow = ImageSlideshow(width=1920, height=1080)  # Ngang (mặc định)
slideshow = ImageSlideshow(width=1080, height=1080)  # Vuông
```

### Thay Đổi Thời Lượng Ảnh

```python
slideshow.add_image(
    image_url="https://...",
    duration=5.0,  # 5 giây cho mỗi ảnh
    transition="slide_left"  # Chuyển cảnh
)
```

### Loại Hiệu Ứng Chuyển Cảnh

```
fade_in
slide_left
slide_right
slide_up
slide_down
zoom_in
zoom_out
```

## 🔍 Troubleshooting

### ❌ "Cannot connect to VectCut API server"

**Giải pháp:**
```bash
# Kiểm tra server có chạy không
python capcut_server.py

# Hoặc chạy MCP server
python mcp_server.py
```

### ❌ Image không load được

**Kiểm tra:**
- URL ảnh có hợp lệ không
- Ảnh có public access không
- Có internet connection không

### ❌ "Draft saved but no URL"

**Giải pháp:**
- Đảm bảo `config.json` được cấu hình đúng
- Kiểm tra VectCut API token/key

## 💡 Workflow Chi Tiết

```
1. Create Draft (1920x1080)
   ↓
2. Add Image 1 (0-3s) với zoom_in animation
   ├─ Add Title
   ↓
3. Add Image 2 (3-6s) với zoom_in animation
   ├─ Add Title
   ↓
4. Add Image 3 (6-9s) với zoom_in animation
   ├─ Add Title
   ↓
5. Save Draft → Get Preview URL
   ↓
6. Open URL → View/Edit/Export
```

## 🎯 Ví Dụ Output

```
=======================================================================
🎬 Create Image Slideshow - Simple Demo
=======================================================================
📹 Creating video draft: 1920x1080...
✅ Draft created: 2024-04-14_abc123xyz

🖼️  Adding image: https://images.unsplash.com/photo-1506... (duration: 3.0s)
📝 Adding text: '🏔️ Mountain View'
✅ Image added (0.0s - 3.0s)

🖼️  Adding image: https://images.unsplash.com/photo-1505... (duration: 3.0s)
📝 Adding text: '🌊 Ocean Wave'
✅ Image added (3.0s - 6.0s)

🖼️  Adding image: https://images.unsplash.com/photo-1495... (duration: 3.0s)
📝 Adding text: '🌅 Sunset'
✅ Image added (6.0s - 9.0s)

💾 Saving draft...
✅ Draft saved successfully!

=======================================================================
✨ SUCCESS! Slideshow Created
=======================================================================
📺 Preview URL: https://cc-vectcut-preview.oss-accelerate.aliyuncs.com/draft...
⏱️  Total Duration: 9.0 seconds

💡 Tips:
  • Click the preview URL to view in browser
  • Use CapCut to make further edits if needed
  • Export as video when satisfied
```

## 📚 Thêm Thông Tin

- Xem `AUTOMATION_GUIDE.md` để biết chi tiết hơn
- Xem `MCP_Documentation_English.md` hoặc `MCP_文档_中文.md`
- Xem skill VectCut API: `vectcut-skill/`

## 🎬 Bước Tiếp Theo

1. **Xem Preview**: Bấm vào URL preview để xem slideshow
2. **Chỉnh Sửa**: Import vào CapCut để chỉnh sửa thêm
3. **Export**: Xuất thành video MP4/MOV khi hoàn tất

---

**Tạo bởi VectCut API** | **Powered by CapCut/JianYing**
