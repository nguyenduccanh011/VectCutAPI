# Các Ví Dụ Quy Trình Làm Việc VectCutAPI

## 1. Sản Xuất Video Cơ Bản

### Video Ngắn Dọc (TikTok/Douyin)

```python
import requests

BASE_URL = "http://localhost:9001"

# 1. Tạo bản nháp dọc (1080x1920)
draft = requests.post(f"{BASE_URL}/create_draft", json={
    "width": 1080,
    "height": 1920
}).json()
draft_id = draft["output"]["draft_id"]

# 2. Thêm video nền (toàn màn hình)
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/background.mp4",
    "start": 0,
    "end": 30,
    "volume": 0.5
})

# 3. Thêm nhạc nền
requests.post(f"{BASE_URL}/add_audio", json={
    "draft_id": draft_id,
    "audio_url": "https://example.com/bgm.mp3",
    "volume": 0.3
})

# 4. Thêm tiêu đề (với hoạt ảnh)
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Tiêu đề Video Hấp Dẫn",
    "start": 0,
    "end": 5,
    "font_size": 64,
    "font_color": "#FFD700",
    "shadow_enabled": True,
    "shadow_color": "#000000",
    "shadow_distance": 10,
    "background_color": "#000000",
    "background_alpha": 0.7,
    "background_round_radius": 20,
    "text_intro": "fade_in",
    "text_outro": "zoom_out"
})

# 5. Thêm text mô tả
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Đây là dòng mô tả video",
    "start": 2,
    "end": 30,
    "font_size": 36,
    "font_color": "#FFFFFF",
    "pos_y": -0.3,
    "alignment_h": "center"
})

# 6. Lưu bản nháp
result = requests.post(f"{BASE_URL}/save_draft", json={
    "draft_id": draft_id
}).json()

print(f"Bản nháp đã lưu: {result['output']['draft_url']}")
```

---

## 2. Video Chuyển Từ Văn Bản AI

### Quy Trình Hoàn Chỉnh

```python
import requests

BASE_URL = "http://localhost:9001"

def create_text_to_video(text_content, bg_video_url, bgm_url):
    """
    Chuyển đổi nội dung văn bản thành video
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm video nền
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": bg_video_url,
        "volume": 0.4
    })

    # 3. Thêm nhạc nền
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": bgm_url,
        "volume": 0.3
    })

    # 4. Thêm text chia đoạn (mỗi đoạn có màu khác nhau)
    segments = text_content.split("\n")
    current_time = 1
    duration_per_segment = 4

    for i, segment in enumerate(segments):
        if not segment.strip():
            continue

        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
        color = colors[i % len(colors)]

        requests.post(f"{BASE_URL}/add_text", json={
            "draft_id": draft_id,
            "text": segment.strip(),
            "start": current_time,
            "end": current_time + duration_per_segment,
            "font_size": 48,
            "font_color": color,
            "shadow_enabled": True,
            "shadow_color": "#000000",
            "shadow_distance": 8,
            "background_color": "#000000",
            "background_alpha": 0.6,
            "background_round_radius": 15,
            "text_intro": "zoom_in",
            "text_outro": "fade_out"
        })

        current_time += duration_per_segment

    # 5. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Ví dụ sử dụng
video_url = create_text_to_video(
    text_content="""Chào mừng đến với VectCutAPI
Đây là dòng thứ hai
Đây là dòng thứ ba
Cảm ơn bạn đã xem""",
    bg_video_url="https://example.com/bg.mp4",
    bgm_url="https://example.com/bgm.mp3"
)
print(f"Video đã tạo: {video_url}")
```

---

## 3. Quy Trình Trộn Video

### Kết Hợp Nhiều Đoạn Video

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_mashup(video_clips, add_transitions=True):
    """
    Tạo video trộn
    :param video_clips: Danh sách clip video [{"url": "...", "duration": 5}, ...]
    :param add_transitions: Có thêm hiệu ứng chuyển tiếp không
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm các clip video
    current_time = 0
    transitions = ["fade_in", "wipe_left", "wipe_right", "wipe_up", "wipe_down"]

    for i, clip in enumerate(video_clips):
        transition = transitions[i % len(transitions)] if add_transitions and i > 0 else None

        requests.post(f"{BASE_URL}/add_video", json={
            "draft_id": draft_id,
            "video_url": clip["url"],
            "start": 0,
            "end": clip["duration"],
            "target_start": current_time,
            "transition": transition,
            "transition_duration": 0.5,
            "volume": 1.0
        })

        current_time += clip["duration"]

    # 3. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Ví dụ sử dụng
clips = [
    {"url": "https://example.com/clip1.mp4", "duration": 5},
    {"url": "https://example.com/clip2.mp4", "duration": 4},
    {"url": "https://example.com/clip3.mp4", "duration": 6},
    {"url": "https://example.com/clip4.mp4", "duration": 5}
]

video_url = create_video_mashup(clips)
print(f"Video trộn đã tạo: {video_url}")
```

---

## 4. Video Có Phụ Đề

### Nhập Phụ Đề SRT

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_with_subtitles(video_url, srt_url):
    """
    Tạo video có phụ đề
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1920,
        "height": 1080
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm video
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": video_url
    })

    # 3. Thêm phụ đề
    requests.post(f"{BASE_URL}/add_subtitle", json={
        "draft_id": draft_id,
        "srt_url": srt_url,
        "font_size": 36,
        "font_color": "#FFFFFF",
        "stroke_enabled": True,
        "stroke_color": "#000000",
        "stroke_width": 4.0,
        "background_alpha": 0.5,
        "pos_y": -0.35
    })

    # 4. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 5. Video Hoạt Ảnh Keyframe

### Hiển Thị Hoạt Ảnh Hình Ảnh

```python
import requests

BASE_URL = "http://localhost:9001"

def create_image_animation(image_url, duration=10):
    """
    Tạo hiển thị hình ảnh với hoạt ảnh keyframe
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm hình ảnh (được xử lý như video 1 giây)
    requests.post(f"{BASE_URL}/add_image", json={
        "draft_id": draft_id,
        "image_url": image_url,
        "start": 0,
        "end": duration,
        "animation_type": "fade_in"
    })

    # 3. Thêm hoạt ảnh keyframe
    # Tỷ lệ: 1.0 -> 1.3 -> 1.0
    # Độ mờ: 1.0 -> 1.0 -> 0.8
    requests.post(f"{BASE_URL}/add_video_keyframe", json={
        "draft_id": draft_id,
        "track_name": "video_main",
        "property_types": ["scale_x", "scale_y", "alpha"],
        "times": [0, duration/2, duration],
        "values": ["1.0,1.0,1.0", "1.3,1.3,1.0", "1.0,1.0,0.8"]
    })

    # 4. Thêm text mô tả
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "Hiển Thị Hình Ảnh Đẹp",
        "start": 1,
        "end": duration - 1,
        "font_size": 52,
        "font_color": "#FFFFFF",
        "shadow_enabled": True,
        "pos_y": 0.35
    })

    # 5. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 6. Video Giới Thiệu Sản Phẩm

### Trình Bày Sản Phẩm Chuyên Nghiệp

```python
import requests

BASE_URL = "http://localhost:9001"

def create_product_video(product_info):
    """
    Tạo video giới thiệu sản phẩm
    :param product_info: Từ điển thông tin sản phẩm
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm video demo sản phẩm
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": product_info["demo_video"],
        "transition": "fade_in",
        "transition_duration": 1.0,
        "volume": 0.5
    })

    # 3. Thêm nhạc nền
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": product_info["bgm"],
        "volume": 0.3
    })

    # 4. Thêm tiêu đề tên sản phẩm
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": product_info["name"],
        "start": 0,
        "end": 4,
        "font_size": 72,
        "font_color": "#FFD700",
        "shadow_enabled": True,
        "shadow_color": "#000000",
        "shadow_distance": 15,
        "background_color": "#1E1E1E",
        "background_alpha": 0.8,
        "background_round_radius": 30,
        "text_intro": "zoom_in",
        "alignment_h": "center",
        "pos_y": 0.3
    })

    # 5. Thêm danh sách tính năng sản phẩm
    features = product_info.get("features", [])
    for i, feature in enumerate(features):
        start_time = 3 + i * 3
        requests.post(f"{BASE_URL}/add_text", json={
            "draft_id": draft_id,
            "text": f"• {feature}",
            "start": start_time,
            "end": start_time + 4,
            "font_size": 40,
            "font_color": "#FFFFFF",
            "background_alpha": 0.6,
            "alignment_h": "left",
            "pos_x": -0.35,
            "pos_y": 0.1 + i * 0.1
        })

    # 6. Thêm thông tin giá/mua hàng
    if "price" in product_info:
        requests.post(f"{BASE_URL}/add_text", json={
            "draft_id": draft_id,
            "text": f"${product_info['price']}",
            "start": len(features) * 3 + 2,
            "end": len(features) * 3 + 6,
            "font_size": 56,
            "font_color": "#FF4444",
            "shadow_enabled": True,
            "background_color": "#FFFFFF",
            "background_alpha": 0.9,
            "background_round_radius": 25,
            "alignment_h": "center",
            "pos_y": -0.3
        })

    # 7. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Ví dụ sử dụng
product = {
    "name": "Đồng Hồ Thông Minh Pro",
    "demo_video": "https://example.com/product_demo.mp4",
    "bgm": "https://example.com/upbeat.mp3",
    "features": [
        "Giám Sát Nhịp Tim 24/7",
        "Chống Nước 50m",
        "Thời Lượng Pin 14 Ngày",
        "100+ Chế Độ Thể Thao"
    ],
    "price": "299"
}

video_url = create_product_video(product)
print(f"Video sản phẩm đã tạo: {video_url}")
```

---

## 7. Video Đa Rãnh Phức Tạp

### Hiệu Ứng Chia Màn Hình

```python
import requests

BASE_URL = "http://localhost:9001"

def create_split_screen_video(left_video, right_video, duration=10):
    """
    Tạo video chia màn hình
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1920,
        "height": 1080
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm video bên trái (co lại và dịch trái)
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": left_video,
        "start": 0,
        "end": duration,
        "scale_x": 0.7,
        "scale_y": 0.7,
        "transform_x": -0.25
    })

    # 3. Thêm video bên phải (co lại và dịch phải)
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": right_video,
        "start": 0,
        "end": duration,
        "scale_x": 0.7,
        "scale_y": 0.7,
        "transform_x": 0.25
    })

    # 4. Thêm đường chia
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "|",
        "start": 0,
        "end": duration,
        "font_size": 100,
        "font_color": "#FFFFFF"
    })

    # 5. Thêm tiêu đề
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "So Sánh",
        "start": 0,
        "end": 3,
        "font_size": 48,
        "font_color": "#FFD700",
        "background_alpha": 0.7,
        "pos_y": -0.4
    })

    # 6. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 8. Video Vòng Quay Hình Ảnh

### Trình Chiếu Ảnh

```python
import requests

BASE_URL = "http://localhost:9001"

def create_image_slideshow(image_urls, image_duration=3, transition="fade_in"):
    """
    Tạo video vòng quay hình ảnh
    :param image_urls: Danh sách URL hình ảnh
    :param image_duration: Thời gian hiển thị mỗi hình ảnh
    :param transition: Hiệu ứng chuyển tiếp
    """
    # 1. Tạo bản nháp
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Thêm hình ảnh tuần tự
    current_time = 0
    for i, image_url in enumerate(image_urls):
        requests.post(f"{BASE_URL}/add_image", json={
            "draft_id": draft_id,
            "image_url": image_url,
            "start": current_time,
            "end": current_time + image_duration,
            "transition": transition if i > 0 else None,
            "transition_duration": 0.5
        })
        current_time += image_duration

    # 3. Thêm nhạc nền
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": "https://example.com/slideshow_bgm.mp3",
        "volume": 0.4
    })

    # 4. Lưu bản nháp
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Ví dụ sử dụng
images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg"
]

video_url = create_image_slideshow(images)
print(f"Video vòng quay đã tạo: {video_url}")
```

---

## Các Thực Tiễn Tốt Nhất

### 1. Quản Lý Dòng Thời Gian

```python
# Sử dụng biến để theo dõi thời gian hiện tại, tránh trùng lặp
current_time = 0
current_time += 5  # Cập nhật sau khi thêm mỗi phần tử media
```

### 2. Xử Lý Lỗi

```python
def safe_add_video(draft_id, video_url, **kwargs):
    try:
        response = requests.post(f"{BASE_URL}/add_video", json={
            "draft_id": draft_id,
            "video_url": video_url,
            **kwargs
        })
        result = response.json()
        if not result.get("success"):
            print(f"Lỗi: {result.get('error')}")
            return False
        return True
    except Exception as e:
        print(f"Ngoại lệ: {e}")
        return False
```

### 3. Kiểm Tra Tài Nguyên Trước

```python
# Kiểm tra độ dài media trước khi tạo video
duration_response = requests.post(f"{BASE_URL}/get_duration", json={
    "media_url": video_url
})
duration = duration_response.json()["output"]["duration"]
```

### 4. Thao Tác Hàng Loạt

```python
# Đối với các thao tác tương tự lớn, sử dụng vòng lặp và cấu hình
text_configs = [
    {"text": "Tiêu Đề", "font_size": 64, "color": "#FFD700"},
    {"text": "Phụ Đề", "font_size": 48, "color": "#FFFFFF"},
    {"text": "Mô Tả", "font_size": 36, "color": "#CCCCCC"}
]

for config in text_configs:
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        **config
    })
```
