# 🔬 Kế Hoạch Reverse-Engineer VectCutAPI

## Mục Tiêu

Bổ sung các hiệu ứng còn thiếu (như `Cross Open`, `Cross Warp`, v.v.) vào thư viện `pyJianYingDraft` để VectCutAPI có thể sử dụng chúng.

---

## 📚 Hiểu Cấu Trúc Hiện Tại

### Các file metadata cần bổ sung (13 files)

| File | Nội dung | Số hiệu ứng hiện có |
|------|----------|---------------------|
| `capcut_transition_meta.py` | Transitions (chuyển cảnh) | ~116 |
| `capcut_animation_meta.py` | Animations Intro/Outro | ~100+ |
| `capcut_effect_meta.py` | Video Scene Effects | ~50+ |
| `capcut_audio_effect_meta.py` | Voice Filters | ~20+ |
| `capcut_text_animation_meta.py` | Text Animations | ~30+ |
| `capcut_mask_meta.py` | Masks | ~9 |
| `animation_meta.py` | JianYing Animations | (tham khảo) |
| `transition_meta.py` | JianYing Transitions | (tham khảo) |
| `filter_meta.py` | Filters | ~50+ |
| `font_meta.py` | Fonts | ~100+ |
| `video_effect_meta.py` | Legacy effects | (tham khảo) |

### Format của mỗi entry:

```python
# Transition
Cross_Open = Transition_meta(
    "Cross Open",           # tên hiển thị (phải khớp CHÍNH XÁC với CapCut)
    False,                  # is_vip: False = miễn phí
    "7xxxxxxxxxxxxxxxxx",   # resource_id: ID để download resource
    "XXXX-XXXX-...",        # effect_id: UUID nhận dạng effect
    "abc123...",            # md5: hash xác thực file download
    0.466666,               # default_duration (giây)
    True                    # is_overlap: có đè lên nhau không
)

# Animation
Fade_In = Animation_meta(
    "Fade In", False,
    0.500,                  # default_duration
    "6xxxxxxxxxxxxxxxxx",   # resource_id (= effect_id cho animation)
    "6xxxxxxxxxxxxxxxxx",   # effect_id
    "abc123..."             # md5
)

# Effect (có params)
Blur = Effect_meta(
    "Blur", False,
    "6xxxxxxxxxxxxxxxxx",   # resource_id
    "15206412",             # effect_id (số nguyên string)
    "abc123...",            # md5
    [Effect_param("effects_adjust_blur", 0.500, 0.000, 1.000)]
)
```

---

## 🛠️ 3 Phương Pháp Reverse Engineer

### ➤ Phương Pháp 1: Draft JSON (DỄ NHẤT - Làm Trước)

**Quy trình:**
1. Mở CapCut PC → Tạo draft mới → Thêm 2 video clip
2. Kéo transition `Cross Open` vào giữa 2 clip
3. Lưu draft (Ctrl+S hoặc thoát)
4. Chạy: `python reverse_engineer.py`
5. Đọc output, lấy `resource_id`, `effect_id`, `md5`
6. Thêm vào `capcut_transition_meta.py`

**Vị trí file draft:**
```
%APPDATA%\CapCut\User Data\Projects\com.lveditor.draft\<draft_name>\draft_content.json
```
hoặc:
```
%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\<draft_name>\draft_content.json
```

**Ví dụ draft_content.json phần transitions:**
```json
{
  "materials": {
    "transitions": [
      {
        "name": "Cross Open",
        "resource_id": "7412345678901234567",
        "effect_id": "A1B2C3D4-1234-5678-ABCD-EF1234567890",
        "md5": "abc123def456abc123def456abc12345",
        "duration": 466666,
        "is_overlap": true,
        "category_name": "Basic"
      }
    ]
  }
}
```

---

### ➤ Phương Pháp 2: CapCut Resource Cache

**Vị trí cache:**
```
%APPDATA%\CapCut\User Data\resource_cache\
%LOCALAPPDATA%\CapCut\User Data\resource_cache\
```

**Cách khai thác:**
1. Áp dụng effect trong CapCut (sẽ tự download)
2. Tìm trong cache file `.json` mô tả effect
3. Đọc `resource_id` và `md5`

---

### ➤ Phương Pháp 3: Network Interception (NÂng Cao)

Dùng [mitmproxy](https://mitmproxy.org/) để bắt request khi CapCut download effect:

```bash
pip install mitmproxy
mitmproxy --port 8080
```

Khi CapCut download `Cross Open`, bạn sẽ thấy URL dạng:
```
https://p16-capcut-va.ibyteimg.com/obj/capcut-ad-resource/<resource_id>
```

---

## 📋 Checklist Từng Loại Hiệu Ứng

### 1. Transitions (chuyển cảnh)

**Ưu tiên cao** - các transition phổ biến chưa có:
- [ ] Cross Open
- [ ] Cross Warp  
- [ ] Cross Blur
- [ ] Film Roll
- [ ] Pixelate

**Cách test:**
```python
from pyJianYingDraft.metadata.capcut_transition_meta import CapCut_Transition_type

# Sau khi thêm
print(CapCut_Transition_type.Cross_Open.value.name)  # → "Cross Open"
```

---

### 2. Animations (intro/outro)

**File:** `capcut_animation_meta.py`  
Classes: `CapCut_Intro_type`, `CapCut_Outro_type`, `CapCut_Loop_type`

**Quy trình:**
1. Thêm video → chọn Animation → chọn Intro tab → áp dụng effect mới
2. Lưu draft → chạy `reverse_engineer.py`
3. Thêm vào class tương ứng

---

### 3. Video Effects

**File:** `capcut_effect_meta.py`  
Classes: `CapCut_Video_scene_effect_type`, `CapCut_Video_character_effect_type`

**Đặc biệt:** Effect có adjustable params, cần lấy thêm:
```json
{
  "params": {
    "effects_adjust_blur": { "default": 0.5, "min": 0.0, "max": 1.0 }
  }
}
```

---

### 4. Text Animations

**File:** `capcut_text_animation_meta.py`

**Quy trình:**
1. Thêm text → vào Animation tab → áp dụng text animation
2. Draft JSON sẽ có trong `materials.texts[].animations`

---

### 5. Sticker Animations

**Lưu ý:** Stickers có ID riêng, không phải `resource_id` thông thường

---

## 🔧 Script Hỗ Trợ

### `reverse_engineer.py` (đã tạo)
```bash
# Tự động tìm draft mới nhất
python reverse_engineer.py

# Chỉ định file draft cụ thể
python reverse_engineer.py "C:\Users\...\draft_content.json"
```

Output:
- In ra tất cả hiệu ứng tìm thấy với metadata
- Tạo `discovered_effects.json` - toàn bộ data raw
- Tạo `new_effects_code.py` - code Python sẵn để copy vào metadata files

---

## 📌 Ví Dụ Thêm Cross Open

Sau khi chạy `reverse_engineer.py` và lấy được IDs:

**Mở file:** `pyJianYingDraft/metadata/capcut_transition_meta.py`

**Tìm class `CapCut_Transition_type` và thêm:**
```python
class CapCut_Transition_type(Effect_enum):
    """CapCut自带的转场效果"""

    # ... existing entries ...
    
    # THÊM VÀO ĐÂY (sắp xếp alpha):
    Cross_Open   = Transition_meta("Cross Open", False, "7xxx", "UUID-xxx", "md5xxx", 0.466666, True)
    Cross_Warp   = Transition_meta("Cross Warp", False, "7xxx", "UUID-xxx", "md5xxx", 0.533333, True)
```

**Test ngay:**
```python
from pyJianYingDraft.metadata.capcut_transition_meta import CapCut_Transition_type
t = CapCut_Transition_type.Cross_Open
print(t.value)  # Transition_meta(name='Cross Open', ...)
```

---

## 🚀 Thứ Tự Ưu Tiên

| Priority | Loại | Lý Do |
|----------|------|-------|
| ⭐⭐⭐ | Transitions | Phổ biến nhất, dễ extract |
| ⭐⭐⭐ | Video Effects | Được dùng nhiều |
| ⭐⭐ | Animations | Đã có nhiều, cần bổ sung |
| ⭐⭐ | Text Animations | Quan trọng cho content |
| ⭐ | Audio Effects | Ít dùng hơn |
| ⭐ | Stickers | Format khác nhau |

---

## 💡 Tips Quan Trọng

1. **Mỗi lần chỉ thêm 1 effect** → Dễ xác định ID nào thuộc effect nào
2. **Đặt tên enum theo tên hiển thị**: `"Cross Open"` → `Cross_Open`
3. **Không dùng tên giống nhau** trong cùng class (Python sẽ override)
4. **VIP effects** (`is_vip=True`) sẽ cần subscription để dùng
5. **md5 có thể trống `""`** trong draft JSON nếu chưa download xong

---

## 📞 Hỏi Khi Gặp Vấn Đề

1. **Draft không có transitions field** → CapCut chưa lưu, thử thoát hẳn app
2. **resource_id trống** → Effect cần download, áp dụng xong chờ download xong
3. **md5 trống** → Chưa download xong, chờ CapCut tải effect về
4. **Script không tìm thấy draft** → Nhập đường dẫn thủ công:
   ```
   python reverse_engineer.py "%APPDATA%\CapCut\User Data\Projects\com.lveditor.draft\<tên_dự_án>\draft_content.json"
   ```
