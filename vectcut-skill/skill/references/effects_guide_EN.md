# Guide to Effects, Transitions & Animations in VectCutAPI

## 📋 Overview

VectCutAPI provides dozens of built-in effects. To discover what effects are available, you need to call **API query endpoints** to retrieve the list.

---

## 🔍 How to Get Effects List

### 1. **Transition Effects**

Used when transitioning between video/image clips.

```python
import requests

BASE_URL = "http://localhost:9001"

# Get list of transition types
response = requests.get(f"{BASE_URL}/get_transition_types")
transitions = response.json()["output"]

print("Available Transitions:")
for transition in transitions:
    print(f"  - {transition}")
```

**Common Transitions:**
- `fade_in` - Fade in
- `fade_out` - Fade out
- `wipe_left` - Wipe left
- `wipe_right` - Wipe right
- `wipe_up` - Wipe up
- `wipe_down` - Wipe down
- `slash_left` - Slash left
- `slash_right` - Slash right
- `scale` - Scale
- `zoom_in` - Zoom in
- `zoom_out` - Zoom out
- `blur` - Blur
- `pixelate` - Pixelate
- `plus` - Plus (light rays)
- `rotate` - Rotate

---

### 2. **Video Intro Animations**

How the video appears when it starts playing.

```python
# Get list of video intro animations
response = requests.get(f"{BASE_URL}/get_intro_animation_types")
intro_anims = response.json()["output"]

print("Available Video Intro Animations:")
for anim in intro_anims:
    print(f"  - {anim}")
```

**Examples:**
- `fade_in` - Fade in
- `scale_up` - Scale up
- `bounce_in` - Bounce in
- `flip_in` - Flip in
- `rotate_in` - Rotate in
- `slide_in_left` - Slide in from left
- `slide_in_right` - Slide in from right

---

### 3. **Video Outro Animations**

How the video disappears when it ends.

```python
# Get list of video outro animations
response = requests.get(f"{BASE_URL}/get_outro_animation_types")
outro_anims = response.json()["output"]

print("Available Video Outro Animations:")
for anim in outro_anims:
    print(f"  - {anim}")
```

---

### 4. **Combo Animations**

Combinations of multiple effects at once.

```python
# Get list of combo animations
response = requests.get(f"{BASE_URL}/get_combo_animation_types")
combo_anims = response.json()["output"]

print("Available Combo Animations:")
for anim in combo_anims:
    print(f"  - {anim}")
```

---

### 5. **Text Intro Animations**

How text appears on the video.

```python
# Get list of text intro animations
response = requests.get(f"{BASE_URL}/get_text_intro_types")
text_intros = response.json()["output"]

print("Available Text Intro Animations:")
for anim in text_intros:
    print(f"  - {anim}")
```

**Examples:**
- `fade_in` - Fade in
- `zoom_in` - Zoom in
- `slide_in_left` - Slide from left
- `slide_in_right` - Slide from right
- `bounce_in` - Bounce in
- `flip_in` - Flip in
- `typewriter` - Typewriter (character by character)

---

### 6. **Text Outro Animations**

How text disappears from the video.

```python
# Get list of text outro animations
response = requests.get(f"{BASE_URL}/get_text_outro_types")
text_outros = response.json()["output"]

print("Available Text Outro Animations:")
for anim in text_outros:
    print(f"  - {anim}")
```

---

### 7. **Text Loop Animations**

Continuous animations that repeat on text.

```python
# Get list of text loop animations
response = requests.get(f"{BASE_URL}/get_text_loop_anim_types")
text_loops = response.json()["output"]

print("Available Text Loop Animations:")
for anim in text_loops:
    print(f"  - {anim}")
```

**Examples:**
- `blink` - Blinking
- `swing` - Swing
- `bounce` - Bouncing
- `pulse` - Pulsing
- `glow` - Glowing
- `shake` - Shaking

---

### 8. **Mask Types**

Used to reveal/hide portions of video.

```python
# Get list of mask types
response = requests.get(f"{BASE_URL}/get_mask_types")
masks = response.json()["output"]

print("Available Mask Types:")
for mask in masks:
    print(f"  - {mask}")
```

**Examples:**
- `circle` - Circle
- `rect` - Rectangle
- `linear` - Linear
- `radial` - Radial
- `heart` - Heart
- `star` - Star

---

### 9. **Audio Effects**

Effects for audio processing.

```python
# Get list of audio effects
response = requests.get(f"{BASE_URL}/get_audio_effect_types")
audio_effects = response.json()["output"]

print("Available Audio Effects:")
for effect in audio_effects:
    print(f"  - {effect}")
```

**Examples:**
- `reverb` - Reverb
- `echo` - Echo
- `distortion` - Distortion
- `pitch_shift` - Pitch shift
- `speed_up` - Speed up
- `slow_down` - Slow down

---

### 10. **Video Scene Effects**

Full-frame video effects.

```python
# Get list of video scene effects
response = requests.get(f"{BASE_URL}/get_video_scene_effect_types")
scene_effects = response.json()["output"]

print("Available Video Scene Effects:")
for effect in scene_effects:
    print(f"  - {effect}")
```

**Examples:**
- `grayscale` - Grayscale
- `vintage` - Vintage
- `cool_tone` - Cool tone
- `warm_tone` - Warm tone
- `sepia` - Sepia
- `blur` - Blur
- `sharpen` - Sharpen

---

### 11. **Video Character Effects**

Special effects for characters/people in video.

```python
# Get list of video character effects
response = requests.get(f"{BASE_URL}/get_video_character_effect_types")
char_effects = response.json()["output"]

print("Available Video Character Effects:")
for effect in char_effects:
    print(f"  - {effect}")
```

---

### 12. **Font Types**

Available fonts for text elements.

```python
# Get list of font types
response = requests.get(f"{BASE_URL}/get_font_types")
fonts = response.json()["output"]

print("Available Fonts:")
for font in fonts:
    print(f"  - {font}")
```

---

## 💻 Practical Example: Get All Effects

Create a Python script to fetch and display all available effects:

```python
import requests

BASE_URL = "http://localhost:9001"

def get_all_effect_types():
    """Fetch all available effect types"""
    
    effects_map = {
        "Transitions": "/get_transition_types",
        "Video Intro Animations": "/get_intro_animation_types",
        "Video Outro Animations": "/get_outro_animation_types",
        "Combo Animations": "/get_combo_animation_types",
        "Text Intro Animations": "/get_text_intro_types",
        "Text Outro Animations": "/get_text_outro_types",
        "Text Loop Animations": "/get_text_loop_anim_types",
        "Mask Types": "/get_mask_types",
        "Audio Effects": "/get_audio_effect_types",
        "Video Scene Effects": "/get_video_scene_effect_types",
        "Video Character Effects": "/get_video_character_effect_types",
        "Fonts": "/get_font_types"
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
                print(f"Total: {len(items)} types")
                print("\nList:")
                
                # Show first 10, then "..."
                for i, item in enumerate(items[:10]):
                    print(f"  • {item}")
                
                if len(items) > 10:
                    print(f"  ... and {len(items) - 10} more")
            else:
                print(f"\n❌ Error fetching {category}: {data['error']}")
        
        except Exception as e:
            print(f"\n❌ Exception fetching {category}: {str(e)}")

if __name__ == "__main__":
    print("🎬 Fetching all available effects from VectCutAPI...")
    get_all_effect_types()
```

**Example Output:**

```
==================================================
📌 Transitions
==================================================
Total: 24 types

List:
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
  ... and 14 more
```

---

## 🎯 Using Effects in Code

### Example 1: Using Transitions

```python
import requests

BASE_URL = "http://localhost:9001"
draft_id = "draft_123"

# 1. Get list of transitions
response = requests.get(f"{BASE_URL}/get_transition_types")
transitions = response.json()["output"]

# 2. Pick a transition (e.g., second one)
chosen_transition = transitions[1]  # "fade_out" (or similar)

# 3. Use it when adding video
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "transition": chosen_transition,
    "transition_duration": 0.8
})
```

### Example 2: Using Text Animations

```python
# 1. Get list of text intro animations
response = requests.get(f"{BASE_URL}/get_text_intro_types")
text_intros = response.json()["output"]

# 2. Pick "zoom_in"
intro = "zoom_in"  # or choose from list: text_intros[2]

# 3. Get text outro animations
response = requests.get(f"{BASE_URL}/get_text_outro_types")
text_outros = response.json()["output"]
outro = "fade_out"

# 4. Use in add_text
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Animated Text",
    "start": 0,
    "end": 5,
    "text_intro": intro,
    "text_outro": outro
})
```

### Example 3: Using Masks

```python
# 1. Get list of mask types
response = requests.get(f"{BASE_URL}/get_mask_types")
masks = response.json()["output"]

# 2. Pick "circle" mask
mask = "circle"

# 3. Use when adding video
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "mask_type": mask,
    "mask_center_x": 0.5,  # Center X
    "mask_center_y": 0.5,  # Center Y
    "mask_size": 1.0,      # Size
    "mask_feather": 0.2    # Edge softness
})
```

---

## 📝 Endpoint Reference Table

| Endpoint | Purpose | Used For |
|----------|---------|----------|
| `GET /get_transition_types` | Transition list | `transition` parameter |
| `GET /get_intro_animation_types` | Video intro animations | Video/Image intro |
| `GET /get_outro_animation_types` | Video outro animations | Video/Image outro |
| `GET /get_text_intro_types` | Text entrance effects | `text_intro` parameter |
| `GET /get_text_outro_types` | Text exit effects | `text_outro` parameter |
| `GET /get_text_loop_anim_types` | Text loop animations | Continuous loop |
| `GET /get_mask_types` | Mask shapes | `mask_type` parameter |
| `GET /get_audio_effect_types` | Audio effects | `effect_type` for audio |
| `GET /get_video_scene_effect_types` | Scene effects | `effect_type` for video |
| `GET /get_video_character_effect_types` | Character effects | `effect_type` for video |
| `GET /get_font_types` | Font list | `font` parameter |

---

## 🎬 Complete Example: Video with Multiple Effects

```python
import requests

BASE_URL = "http://localhost:9001"

def create_video_with_effects():
    # 1. Create draft
    draft = requests.post(f"{BASE_URL}/create_draft", json={
        "width": 1080,
        "height": 1920
    }).json()
    draft_id = draft["output"]["draft_id"]
    
    # 2. Get effect lists
    transitions = requests.get(f"{BASE_URL}/get_transition_types").json()["output"]
    text_intros = requests.get(f"{BASE_URL}/get_text_intro_types").json()["output"]
    text_outros = requests.get(f"{BASE_URL}/get_text_outro_types").json()["output"]
    
    # 3. Add video with transition
    requests.post(f"{BASE_URL}/add_video", json={
        "draft_id": draft_id,
        "video_url": "https://example.com/video.mp4",
        "transition": transitions[0],  # Use first transition
        "transition_duration": 0.5
    })
    
    # 4. Add text with animations
    requests.post(f"{BASE_URL}/add_text", json={
        "draft_id": draft_id,
        "text": "Beautiful Video with Effects!",
        "start": 0,
        "end": 5,
        "text_intro": text_intros[2],   # 3rd intro animation
        "text_outro": text_outros[1],   # 2nd outro animation
        "font_size": 48,
        "font_color": "#FFD700"
    })
    
    # 5. Save
    result = requests.post(f"{BASE_URL}/save_draft", json={
        "draft_id": draft_id
    }).json()
    
    print(f"✅ Video created: {result['output']['draft_url']}")
    print(f"Used transition: {transitions[0]}")
    print(f"Used intro animation: {text_intros[2]}")
    print(f"Used outro animation: {text_outros[1]}")

if __name__ == "__main__":
    create_video_with_effects()
```

---

## 💡 Important Notes

1. **Always call API first** - Don't hardcode effect names
2. **Check response** - Ensure `success: true` before using data
3. **Case-sensitive** - Effect names use lowercase with underscores (e.g., `fade_in` not `Fade_In`)
4. **Some effects have parameters** - E.g., `mask_feather`, `transition_duration`
5. **Not all effects work everywhere** - E.g., text animations don't work for videos
6. **Response format** - Always structured as: `{"success": true, "output": [...]}`

---

Now you know how to discover and use all effects! 🎉
