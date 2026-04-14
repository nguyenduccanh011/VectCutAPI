# VectCutAPI Workflow Examples

## 1. Basic Video Production

### Vertical Short Videos (TikTok/Douyin)

```python
import requests

BASE_URL = "http://localhost:9001"

# 1. Create vertical draft (1080x1920)
draft = requests.post(f"{BASE_URL}/create_draft", json={
    "width": 1080,
    "height": 1920
}).json()
draft_id = draft["output"]["draft_id"]

# 2. Add background video (fullscreen)
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/background.mp4",
    "start": 0,
    "end": 30,
    "volume": 0.5
})

# 3. Add background music
requests.post(f"{BASE_URL}/add_audio", json={
    "draft_id": draft_id,
    "audio_url": "https://example.com/bgm.mp3",
    "volume": 0.3
})

# 4. Add title text (with animation)
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Exciting Video Title",
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

# 5. Add description text
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "This is video description text",
    "start": 2,
    "end": 30,
    "font_size": 36,
    "font_color": "#FFFFFF",
    "pos_y": -0.3,
    "alignment_h": "center"
})

# 6. Save draft
result = requests.post(f"{BASE_URL}/save_draft", json={
    "draft_id": draft_id
}).json()

print(f"Draft saved: {result['output']['draft_url']}")
```

---

## 2. AI Text-to-Video

### Complete Workflow

```python
import requests

BASE_URL = "http://localhost:9001"

def create_text_to_video(text_content, bg_video_url, bgm_url):
    """
    Convert text content into video
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add background video
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": bg_video_url,
        "volume": 0.4
    })

    # 3. Add background music
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": bgm_url,
        "volume": 0.3
    })

    # 4. Add segmented text (each segment with different color)
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

    # 5. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Usage example
video_url = create_text_to_video(
    text_content="""Welcome to VectCutAPI
This is the second line
This is the third line
Thank you for watching""",
    bg_video_url="https://example.com/bg.mp4",
    bgm_url="https://example.com/bgm.mp3"
)
print(f"Video generated: {video_url}")
```

---

## 3. Video Mashup Workflow

### Multiple Video Clips Combined

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_mashup(video_clips, add_transitions=True):
    """
    Create video mashup
    :param video_clips: List of video clips [{"url": "...", "duration": 5}, ...]
    :param add_transitions: Whether to add transitions
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add video clips
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

    # 3. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Usage example
clips = [
    {"url": "https://example.com/clip1.mp4", "duration": 5},
    {"url": "https://example.com/clip2.mp4", "duration": 4},
    {"url": "https://example.com/clip3.mp4", "duration": 6},
    {"url": "https://example.com/clip4.mp4", "duration": 5}
]

video_url = create_video_mashup(clips)
print(f"Mashup video generated: {video_url}")
```

---

## 4. Video with Subtitles

### SRT Subtitle Import

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_with_subtitles(video_url, srt_url):
    """
    Create video with subtitles
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1920,
        "height": 1080
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add video
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": video_url
    })

    # 3. Add subtitles
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

    # 4. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 5. Keyframe Animation Video

### Image Animation Display

```python
import requests

BASE_URL = "http://localhost:9001"

def create_image_animation(image_url, duration=10):
    """
    Create image display with keyframe animation
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add image (treated as 1-second video)
    requests.post(f"{BASE_URL}/add_image", json={
        "draft_id": draft_id,
        "image_url": image_url,
        "start": 0,
        "end": duration,
        "animation_type": "fade_in"
    })

    # 3. Add keyframe animation
    # Scale: 1.0 -> 1.3 -> 1.0
    # Opacity: 1.0 -> 1.0 -> 0.8
    requests.post(f"{BASE_URL}/add_video_keyframe", json={
        "draft_id": draft_id,
        "track_name": "video_main",
        "property_types": ["scale_x", "scale_y", "alpha"],
        "times": [0, duration/2, duration],
        "values": ["1.0,1.0,1.0", "1.3,1.3,1.0", "1.0,1.0,0.8"]
    })

    # 4. Add description text
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "Beautiful Image Display",
        "start": 1,
        "end": duration - 1,
        "font_size": 52,
        "font_color": "#FFFFFF",
        "shadow_enabled": True,
        "pos_y": 0.35
    })

    # 5. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 6. Product Introduction Video

### Professional Product Showcase

```python
import requests

BASE_URL = "http://localhost:9001"

def create_product_video(product_info):
    """
    Create product introduction video
    :param product_info: Product information dictionary
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add product demo video
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": product_info["demo_video"],
        "transition": "fade_in",
        "transition_duration": 1.0,
        "volume": 0.5
    })

    # 3. Add background music
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": product_info["bgm"],
        "volume": 0.3
    })

    # 4. Add product name title
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

    # 5. Add product features list
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

    # 6. Add price/purchase information
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

    # 7. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Usage example
product = {
    "name": "Smart Watch Pro",
    "demo_video": "https://example.com/product_demo.mp4",
    "bgm": "https://example.com/upbeat.mp3",
    "features": [
        "24/7 Heart Rate Monitor",
        "50m Water Resistant",
        "14-Day Battery Life",
        "100+ Sports Modes"
    ],
    "price": "299"
}

video_url = create_product_video(product)
print(f"Product video generated: {video_url}")
```

---

## 7. Complex Multi-Track Video

### Split-Screen Effect

```python
import requests

BASE_URL = "http://localhost:9001"

def create_split_screen_video(left_video, right_video, duration=10):
    """
    Create split-screen video
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1920,
        "height": 1080
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add left video (scaled and shifted left)
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": left_video,
        "start": 0,
        "end": duration,
        "scale_x": 0.7,
        "scale_y": 0.7,
        "transform_x": -0.25
    })

    # 3. Add right video (scaled and shifted right)
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": right_video,
        "start": 0,
        "end": duration,
        "scale_x": 0.7,
        "scale_y": 0.7,
        "transform_x": 0.25
    })

    # 4. Add divider line
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "|",
        "start": 0,
        "end": duration,
        "font_size": 100,
        "font_color": "#FFFFFF"
    })

    # 5. Add title
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "Comparison",
        "start": 0,
        "end": 3,
        "font_size": 48,
        "font_color": "#FFD700",
        "background_alpha": 0.7,
        "pos_y": -0.4
    })

    # 6. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]
```

---

## 8. Image Carousel Video

### Photo Slideshow

```python
import requests

BASE_URL = "http://localhost:9001"

def create_image_slideshow(image_urls, image_duration=3, transition="fade_in"):
    """
    Create image carousel video
    :param image_urls: List of image URLs
    :param image_duration: Display duration per image
    :param transition: Transition effect
    """
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]

    # 2. Add images sequentially
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

    # 3. Add background music
    requests.post(f"{BASE_URL}/add_audio", json={
        "draft_id": draft_id,
        "audio_url": "https://example.com/slideshow_bgm.mp3",
        "volume": 0.4
    })

    # 4. Save draft
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()

    return result["output"]["draft_url"]

# Usage example
images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg"
]

video_url = create_image_slideshow(images)
print(f"Carousel video generated: {video_url}")
```

---

## Best Practices

### 1. Timeline Management

```python
# Use variables to track current time, avoid overlaps
current_time = 0
current_time += 5  # Update after adding each media element
```

### 2. Error Handling

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
            print(f"Error: {result.get('error')}")
            return False
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False
```

### 3. Resource Pre-Check

```python
# Check media duration before creating video
duration_response = requests.post(f"{BASE_URL}/get_duration", json={
    "media_url": video_url
})
duration = duration_response.json()["output"]["duration"]
```

### 4. Batch Operations

```python
# For large similar operations, use loops and configurations
text_configs = [
    {"text": "Title", "font_size": 64, "color": "#FFD700"},
    {"text": "Subtitle", "font_size": 48, "color": "#FFFFFF"},
    {"text": "Description", "font_size": 36, "color": "#CCCCCC"}
]

for config in text_configs:
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        **config
    })
```
