# Hướng Dẫn Các Hiệu Ứng, Chuyển Tiếp & Hoạt Ảnh VectCutAPI

## 📋 Tổng Quan

VectCutAPI cung cấp hàng chục hiệu ứng sẵn có. Để biết có những hiệu ứng nào, bạn cần gọi các **API truy vấn** để lấy danh sách.

---

## 🔍 Cách Lấy Danh Sách Hiệu Ứng

### 1. **Hiệu Ứng Chuyển Tiếp (Transitions)**

Dùng cho video/hình ảnh chuyển từ clip này sang clip khác.

```python
import requests

BASE_URL = "http://localhost:9001"

# Lấy danh sách hiệu ứng chuyển tiếp
response = requests.get(f"{BASE_URL}/get_transition_types")
transitions = response.json()["output"]

print("Danh sách hiệu ứng chuyển tiếp:")
for transition in transitions:
    print(f"  - {transition}")
```

**Một số hiệu ứng phổ biến:**
- `fade_in` - Mờ dần vào
- `fade_out` - Mờ dần ra
- `wipe_left` - Quét từ phải sang trái
- `wipe_right` - Quét từ trái sang phải
- `wipe_up` - Quét từ dưới lên
- `wipe_down` - Quét từ trên xuống
- `slash_left` - Gạch chéo trái
- `slash_right` - Gạch chéo phải
- `scale` - Thu phóng
- `zoom_in` - Phóng to
- `zoom_out` - Thu nhỏ
- `blur` - Mờ
- `pixelate` - Pixelate
- `plus` - Tia sáng
- `rotate` - Xoay

---

### 2. **Hoạt Ảnh Vào Video (Video Intro Animations)**

Hoạt ảnh xuất hiện của video khi bắt đầu phát.

```python
# Lấy danh sách hoạt ảnh vào
response = requests.get(f"{BASE_URL}/get_intro_animation_types")
intro_anims = response.json()["output"]

print("Danh sách hoạt ảnh vào video:")
for anim in intro_anims:
    print(f"  - {anim}")
```

**Ví dụ:**
- `fade_in` - Mờ dần vào
- `scale_up` - Phóng to vào
- `bounce_in` - Nảy vào
- `flip_in` - Lật vào
- `rotate_in` - Xoay vào
- `slide_in_left` - Trượt vào từ trái
- `slide_in_right` - Trượt vào từ phải

---

### 3. **Hoạt Ảnh Ra Video (Video Outro Animations)**

Hoạt ảnh biến mất của video khi kết thúc.

```python
# Lấy danh sách hoạt ảnh ra
response = requests.get(f"{BASE_URL}/get_outro_animation_types")
outro_anims = response.json()["output"]

print("Danh sách hoạt ảnh ra video:")
for anim in outro_anims:
    print(f"  - {anim}")
```

---

### 4. **Hoạt Ảnh Kết Hợp (Combo Animations)**

Kết hợp nhiều hiệu ứng cùng lúc.

```python
# Lấy danh sách hoạt ảnh kết hợp
response = requests.get(f"{BASE_URL}/get_combo_animation_types")
combo_anims = response.json()["output"]

print("Danh sách hoạt ảnh kết hợp:")
for anim in combo_anims:
    print(f"  - {anim}")
```

---

### 5. **Hoạt Ảnh Văn Bản Vào (Text Intro Animations)**

Cách văn bản xuất hiện trên video.

```python
# Lấy danh sách hoạt ảnh vào văn bản
response = requests.get(f"{BASE_URL}/get_text_intro_types")
text_intros = response.json()["output"]

print("Danh sách hoạt ảnh vào văn bản:")
for anim in text_intros:
    print(f"  - {anim}")
```

**Ví dụ:**
- `fade_in` - Mờ dần vào
- `zoom_in` - Phóng to vào
- `slide_in_left` - Trượt từ trái
- `slide_in_right` - Trượt từ phải
- `bounce_in` - Nảy vào
- `flip_in` - Lật vào
- `typewriter` - Gõ máy (từng ký tự)

---

### 6. **Hoạt Ảnh Văn Bản Ra (Text Outro Animations)**

Cách văn bản biến mất trên video.

```python
# Lấy danh sách hoạt ảnh ra văn bản
response = requests.get(f"{BASE_URL}/get_text_outro_types")
text_outros = response.json()["output"]

print("Danh sách hoạt ảnh ra văn bản:")
for anim in text_outros:
    print(f"  - {anim}")
```

---

### 7. **Hoạt Ảnh Lặp Văn Bản (Text Loop Animations)**

Hoạt ảnh lặp lại liên tục cho văn bản.

```python
# Lấy danh sách hoạt ảnh lặp văn bản
response = requests.get(f"{BASE_URL}/get_text_loop_anim_types")
text_loops = response.json()["output"]

print("Danh sách hoạt ảnh lặp văn bản:")
for anim in text_loops:
    print(f"  - {anim}")
```

**Ví dụ:**
- `blink` - Nhấp nháy
- `swing` - Swing
- `bounce` - Nảy
- `pulse` - Xung động
- `glow` - Phát sáng
- `shake` - Rung lắc

---

### 8. **Kiểu Mặt Nạ (Mask Types)**

Dùng để che/lộ từng phần của video.

```python
# Lấy danh sách kiểu mặt nạ
response = requests.get(f"{BASE_URL}/get_mask_types")
masks = response.json()["output"]

print("Danh sách kiểu mặt nạ:")
for mask in masks:
    print(f"  - {mask}")
```

**Ví dụ:**
- `circle` - Tròn
- `rect` - Hình vuông
- `linear` - Tuyến tính
- `radial` - Bức xạ
- `heart` - Trái tim
- `star` - Sao

---

### 9. **Hiệu Ứng Âm Thanh (Audio Effects)**

Hiệu ứng xử lý âm thanh.

```python
# Lấy danh sách hiệu ứng âm thanh
response = requests.get(f"{BASE_URL}/get_audio_effect_types")
audio_effects = response.json()["output"]

print("Danh sách hiệu ứng âm thanh:")
for effect in audio_effects:
    print(f"  - {effect}")
```

**Ví dụ:**
- `reverb` - Vang âm
- `echo` - Tiếng vang
- `distortion` - Méo tiếng
- `pitch_shift` - Thay đổi cao độ
- `speed_up` - Tăng tốc
- `slow_down` - Giảm tốc

---

### 10. **Hiệu Ứng Cảnh Video (Video Scene Effects)**

Hiệu ứng toàn cảnh video.

```python
# Lấy danh sách hiệu ứng cảnh
response = requests.get(f"{BASE_URL}/get_video_scene_effect_types")
scene_effects = response.json()["output"]

print("Danh sách hiệu ứng cảnh video:")
for effect in scene_effects:
    print(f"  - {effect}")
```

**Ví dụ:**
- `grayscale` - Đen trắng
- `vintage` - Cổ điển
- `cool_tone` - Tông lạnh
- `warm_tone` - Tông ấm
- `sepia` - Sepia
- `blur` - Mờ
- `sharpen` - Sắc nét

---

### 11. **Hiệu Ứng Ký Tự Video (Video Character Effects)**

Hiệu ứng đặc biệt cho ký tự/nhân vật.

```python
# Lấy danh sách hiệu ứng ký tự
response = requests.get(f"{BASE_URL}/get_video_character_effect_types")
char_effects = response.json()["output"]

print("Danh sách hiệu ứng ký tự/nhân vật:")
for effect in char_effects:
    print(f"  - {effect}")
```

---

### 12. **Kiểu Phông Chữ (Font Types)**

Danh sách các phông chữ có sẵn.

```python
# Lấy danh sách phông chữ
response = requests.get(f"{BASE_URL}/get_font_types")
fonts = response.json()["output"]

print("Danh sách phông chữ:")
for font in fonts:
    print(f"  - {font}")
```

---

## 💻 Ví Dụ Thực Tế: Lấy Tất Cả Hiệu Ứng

Tạo script Python để lấy và xem tất cả loại hiệu ứng:

```python
import requests

BASE_URL = "http://localhost:9001"

def get_all_effect_types():
    """Lấy tất cả loại hiệu ứng sẵn có"""
    
    effects_map = {
        "Chuyển tiếp (Transitions)": "/get_transition_types",
        "Hoạt ảnh vào video": "/get_intro_animation_types",
        "Hoạt ảnh ra video": "/get_outro_animation_types",
        "Hoạt ảnh kết hợp": "/get_combo_animation_types",
        "Hoạt ảnh vào văn bản": "/get_text_intro_types",
        "Hoạt ảnh ra văn bản": "/get_text_outro_types",
        "Hoạt ảnh lặp văn bản": "/get_text_loop_anim_types",
        "Kiểu mặt nạ": "/get_mask_types",
        "Hiệu ứng âm thanh": "/get_audio_effect_types",
        "Hiệu ứng cảnh": "/get_video_scene_effect_types",
        "Hiệu ứng ký tự": "/get_video_character_effect_types",
        "Phông chữ": "/get_font_types"
    }
    
    for category, endpoint in effects_map.items():
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            data = response.json()
            
            if data["success"]:
                items = data["output"]
                print(f"\n{'='*50}")
                print(f"📌 {category}")
                print(f"{'='*50}")
                print(f"Tổng cộng: {len(items)} loại")
                print("\nDanh sách:")
                
                # Hiển thị 10 cái đầu tiên, sau đó "..."
                for i, item in enumerate(items[:10]):
                    print(f"  • {item}")
                
                if len(items) > 10:
                    print(f"  ... và {len(items) - 10} loại khác")
            else:
                print(f"\n❌ Lỗi khi lấy {category}: {data['error']}")
        
        except Exception as e:
            print(f"\n❌ Exception khi lấy {category}: {str(e)}")

if __name__ == "__main__":
    print("🎬 Lấy toàn bộ danh sách hiệu ứng từ VectCutAPI...")
    get_all_effect_types()
```

**Một số ví dụ chạy:**

```
==================================================
📌 Chuyển tiếp (Transitions)
==================================================
Tổng cộng: 24 loại

Danh sách:
  • fade_in
  • fade_out
  • wipe_left
  • wipe_right
  • scale_up
  • rotate
  • zoom_in
  • blur
  • pixelate
  • plus
  ... và 14 loại khác
```

---

## 🎯 Cách Sử Dụng Hiệu Ứng Trong Code

### Ví dụ 1: Dùng Chuyển Tiếp

```python
import requests

BASE_URL = "http://localhost:9001"
draft_id = "draft_123"

# 1. Lấy danh sách chuyển tiếp
response = requests.get(f"{BASE_URL}/get_transition_types")
transitions = response.json()["output"]

# 2. Chọn một chuyển tiếp (ví dụ chuyển tiếp thứ hai)
chosen_transition = transitions[1]  # "fade_out" (hoặc hiệu ứng khác)

# 3. Dùng nó khi thêm video
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "transition": chosen_transition,
    "transition_duration": 0.8
})
```

### Ví dụ 2: Dùng Hoạt Ảnh Văn Bản

```python
# 1. Lấy danh sách hoạt ảnh vào
response = requests.get(f"{BASE_URL}/get_text_intro_types")
text_intros = response.json()["output"]

# 2. Chọn hoạt ảnh "zoom_in"
intro = "zoom_in"  # hoặc chọn từ danh sách: text_intros[2]

# 3. Lấy hoạt ảnh ra
response = requests.get(f"{BASE_URL}/get_text_outro_types")
text_outros = response.json()["output"]
outro = "fade_out"

# 4. Dùng trong add_text
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Văn bản với hoạt ảnh",
    "start": 0,
    "end": 5,
    "text_intro": intro,
    "text_outro": outro
})
```

### Ví dụ 3: Dùng Mặt Nạ

```python
# 1. Lấy danh sách mặt nạ
response = requests.get(f"{BASE_URL}/get_mask_types")
masks = response.json()["output"]

# 2. Chọn mặt nạ "circle"
mask = "circle"

# 3. Dùng khi thêm video
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "mask_type": mask,
    "mask_center_x": 0.5,  # Tâm X
    "mask_center_y": 0.5,  # Tâm Y
    "mask_size": 1.0,      # Kích thước
    "mask_feather": 0.2    # Độ mềm mịn viền
})
```

---

## 📝 Bảng Tóm Tắt Các Endpoint

| Endpoint | Mục Đích | Dùng Cho |
|----------|---------|----------|
| `GET /get_transition_types` | Danh sách chuyển tiếp | `transition` parameter |
| `GET /get_intro_animation_types` | Hoạt ảnh vào video | Video/Image |
| `GET /get_outro_animation_types` | Hoạt ảnh ra video | Video/Image |
| `GET /get_text_intro_types` | Hoạt ảnh vào văn bản | `text_intro` parameter |
| `GET /get_text_outro_types` | Hoạt ảnh ra văn bản | `text_outro` parameter |
| `GET /get_text_loop_anim_types` | Hoạt ảnh lặp văn bản | Lặp liên tục |
| `GET /get_mask_types` | Kiểu mặt nạ | `mask_type` parameter |
| `GET /get_audio_effect_types` | Hiệu ứng âm thanh | `effect_type` audio |
| `GET /get_video_scene_effect_types` | Hiệu ứng cảnh | `effect_type` video |
| `GET /get_video_character_effect_types` | Hiệu ứng ký tự | `effect_type` video |
| `GET /get_font_types` | Danh sách phông chữ | `font` parameter |

---

## 🎬 Ví Dụ Hoàn Chỉnh: Video Với Nhiều Hiệu Ứng

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_with_effects():
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]
    
    # 2. Lấy danh sách hiệu ứng
    transitions = requests.get(f"{BASE_URL}/get_transition_types").json()["output"]
    text_intros = requests.get(f"{BASE_URL}/get_text_intro_types").json()["output"]
    text_outros = requests.get(f"{BASE_URL}/get_text_outro_types").json()["output"]
    
    # 3. Thêm video với chuyển tiếp
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": "https://example.com/video.mp4",
        "transition": transitions[0],  # Dùng chuyển tiếp đầu tiên
        "transition_duration": 0.5
    })
    
    # 4. Thêm text với hoạt ảnh
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "Video với hiệu ứng đẹp!",
        "start": 0,
        "end": 5,
        "text_intro": text_intros[2],   # Hoạt ảnh vào thứ 3
        "text_outro": text_outros[1],   # Hoạt ảnh ra thứ 2
        "font_size": 48,
        "font_color": "#FFD700"
    })
    
    # 5. Lưu
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()
    
    print(f"✅ Video tạo thành công: {result['output']['draft_url']}")
    print(f"Dùng hiệu ứng chuyển tiếp: {transitions[0]}")
    print(f"Dùng hoạt ảnh vào: {text_intros[2]}")
    print(f"Dùng hoạt ảnh ra: {text_outros[1]}")

if __name__ == "__main__":
    create_video_with_effects()
```

---

## 💡 Lưu Ý Quan Trọng

1. **Gọi API trước** để lấy danh sách - Không phải hardcode tên hiệu ứng
2. **Kiểm tra response** - Đảm bảo `success: true` trước khi dùng dữ liệu
3. **Tên hiệu ứng phân biệt chữ hoa/thường** - VD: `fade_in` (không phải `Fade_In`)
4. **Một số hiệu ứng có tham số** - VD: `mask_feather`, `transition_duration`
5. **Không phải tất cả hiệu ứng dùng được cho mọi loại** - VD: Text animation không dùng cho video

---

Giờ bạn đã biết cách lấy và sử dụng tất cả hiệu ứng! 🎉
