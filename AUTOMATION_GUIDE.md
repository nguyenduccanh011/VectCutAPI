# 🎬 VectCutAPI - Hướng dẫn Tự động hóa & Tạo Template

## 📋 Mục lục
1. [Vấn đề hiện tại](#vấn-đề-hiện-tại)
2. [Giải pháp 1: Pattern Template (Đơn giản)](#giải-pháp-1-pattern-template)
3. [Giải pháp 2: JSON Template (Linh hoạt)](#giải-pháp-2-json-template)
4. [Giải pháp 3: LLM Parser Layer (Tự động hoàn toàn)](#giải-pháp-3-llm-parser-layer)
5. [So sánh & Lựa chọn](#so-sánh--lựa-chọn)

---

## 🚨 Vấn đề hiện tại

Hiện tại MCP yêu cầu:
```
User: "Tạo video slideshow 5 ảnh"
↓
MCP: Cần prompt từng bước
  1. create_draft
  2. add_image (ảnh 1)
  3. add_image (ảnh 2)
  4. add_video_keyframe (zoom effect)
  5. ... (lặp lại với ảnh 3,4,5)
  6. save_draft
↓
User phải mô tả chi tiết từng bước ❌
```

**Mục tiêu**: Từ 1 mô tả → Tự động generate toàn bộ video ✅

---

## ✅ Giải pháp 1: Pattern Template (Đơn giản)

### 📌 Khái niệm
Định nghĩa sẵn "công thức" video, chỉ cần user cung cấp nội dung.

### 🎯 Ưu điểm
- ✅ Đơn giản, dễ thực hiện
- ✅ Tái sử dụng cao (Slideshow, KOL video, Tutorial, v.v.)
- ✅ Không cần LLM phức tạp
- ❌ Chỉ phù hợp các video có cấu trúc cố định

### 📝 Ví dụ: Tạo file `pattern/003-slideshow-template.py`

```python
"""
Template: Slideshow với zoom/pan effects + transitions
Người dùng cung cấp: Danh sách ảnh URL + hiệu ứng tùy chọn
"""
from example import (
    add_image_impl,
    add_video_keyframe_impl,
    save_draft_impl,
)

class SlideshowTemplate:
    """Tùy chỉnh dễ dàng: thay đổi các biến này"""
    DURATION_PER_SLIDE = 3.0      # Mỗi ảnh kéo dài 3s
    TRANSITION_TYPE = "Dissolve"  # Kiểu transition
    TRANSITION_DUR = 0.5          # Độ dài transition
    MOTION_EFFECTS = ["zoom_in", "zoom_out"]  # Danh sách hiệu ứng
    
    @staticmethod
    def apply_zoom_in(draft_id, track_name, clip_start, duration):
        """Zoom In: 1.0 → 1.25"""
        add_video_keyframe_impl(draft_id, track_name, "scale_x", 
                                clip_start + 0.01, "1.0")
        add_video_keyframe_impl(draft_id, track_name, "scale_x", 
                                clip_start + duration - 0.01, "1.25")
        add_video_keyframe_impl(draft_id, track_name, "scale_y", 
                                clip_start + 0.01, "1.0")
        add_video_keyframe_impl(draft_id, track_name, "scale_y", 
                                clip_start + duration - 0.01, "1.25")

    @staticmethod
    def apply_pan_left_right(draft_id, track_name, clip_start, duration):
        """Pan Trái → Phải: -0.08 → 0.08"""
        add_video_keyframe_impl(draft_id, track_name, "position_x", 
                                clip_start + 0.01, "-0.08")
        add_video_keyframe_impl(draft_id, track_name, "position_x", 
                                clip_start + duration - 0.01, "0.08")

    @classmethod
    def create_slideshow(cls, image_urls, effects=None, **kwargs):
        """
        Tạo slideshow tự động
        
        Args:
            image_urls: ["url1", "url2", "url3"]
            effects: ["zoom_in", "pan_left_right", ...] hoặc None (dùng mặc định)
            **kwargs: override DURATION_PER_SLIDE, TRANSITION_TYPE, v.v.
        
        Returns:
            {"success": bool, "draft_id": str, "draft_url": str}
        """
        # Cập nhật settings từ kwargs
        for key in ["DURATION_PER_SLIDE", "TRANSITION_TYPE", "TRANSITION_DUR"]:
            if key in kwargs:
                setattr(cls, key, kwargs[key])
        
        if effects is None:
            effects = cls.MOTION_EFFECTS
        
        draft_id = None
        total = len(image_urls)
        track_name = "video"
        
        print(f"🎬 Tạo slideshow: {total} ảnh, effect: {effects[0]}")
        
        for i, img_url in enumerate(image_urls):
            clip_start = i * cls.DURATION_PER_SLIDE
            clip_end = clip_start + cls.DURATION_PER_SLIDE
            effect = effects[i % len(effects)]
            
            print(f"  [{i+1}/{total}] {effect} | {clip_start:.1f}s")
            
            # Thêm ảnh
            r = add_image_impl(
                image_url=img_url,
                start=clip_start,
                end=clip_end,
                width=1280,
                height=720,
                track_name=track_name,
                draft_id=draft_id,
                transition=cls.TRANSITION_TYPE if i > 0 else None,
                transition_duration=cls.TRANSITION_DUR,
            )
            assert r.get("success"), f"Lỗi thêm ảnh {i+1}"
            draft_id = r["output"]["draft_id"]
            
            # Thêm effect motion
            method_name = f"apply_{effect}"
            if hasattr(cls, method_name):
                getattr(cls, method_name)(draft_id, track_name, clip_start, 
                                         cls.DURATION_PER_SLIDE)
            
            print(f"    ✓ draft_id = {draft_id}")
        
        # Lưu draft
        save_draft_impl(draft_id, "/path/to/capcut/folder")
        
        return {
            "success": True,
            "draft_id": draft_id,
            "draft_url": f"https://www.install-ai-guider.top/draft/downloader?draft_id={draft_id}",
            "total_duration": len(image_urls) * cls.DURATION_PER_SLIDE
        }

if __name__ == "__main__":
    # 🎯 Ví dụ 1: Dùng settings mặc định
    result = SlideshowTemplate.create_slideshow([
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280",
        "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280",
    ])
    print(result)
    
    # 🎯 Ví dụ 2: Tùy chỉnh settings
    result2 = SlideshowTemplate.create_slideshow(
        image_urls=[...],
        effects=["zoom_in", "pan_left_right", "zoom_out"],
        DURATION_PER_SLIDE=4.0,
        TRANSITION_DUR=1.0,
        TRANSITION_TYPE="CrossDissolve"
    )
```

### 🔧 Cách sử dụng Pattern Template qua MCP

Thêm vào `mcp_server.py`:

```python
{
    "name": "create_slideshow_template",
    "description": "Create slideshow with auto effects from image URLs",
    "inputSchema": {
        "type": "object",
        "properties": {
            "image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Array of image URLs"
            },
            "effects": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Mô phỏng effects: ['zoom_in', 'pan_left_right', ...]"
            },
            "duration_per_slide": {"type": "number", "default": 3.0},
            "transition_type": {"type": "string", "default": "Dissolve"}
        },
        "required": ["image_urls"]
    }
}
```

---

## 🎨 Giải pháp 2: JSON Template (Linh hoạt)

### 📌 Khái niệm
Lưu "bản thiết kế" video dưới dạng JSON, sau đó "điền nội dung" vào.

### 🎯 Ưu điểm
- ✅ Rất linh hoạt, dễ mở rộng
- ✅ Tách biệt layout và nội dung
- ✅ Dễ version control & chia sẻ
- ✅ Hỗ trợ nhiều kịch bản

### 📋 Template JSON cấu trúc

Tạo file `template/slideshow-template.json`:

```json
{
  "name": "slideshow-basic",
  "version": "1.0.0",
  "description": "Basic slideshow with zoom/pan effects",
  "settings": {
    "canvas": {"width": 1280, "height": 720},
    "duration_per_slide": 3.0,
    "transition": {
      "type": "Dissolve",
      "duration": 0.5
    }
  },
  "tracks": {
    "video": {
      "type": "video",
      "elements": [
        {
          "type": "image",
          "slot": "image_{{INDEX}}",
          "duration_offset": 0,
          "keyframes": [
            {
              "type": "scale",
              "property_type": "scale_x",
              "at_start": "1.0",
              "at_end": "1.25",
              "description": "Zoom In effect"
            },
            {
              "type": "scale",
              "property_type": "scale_y",
              "at_start": "1.0",
              "at_end": "1.25"
            }
          ]
        }
      ]
    }
  },
  "slots": {
    "image_0": {"type": "image", "placeholder": true},
    "image_1": {"type": "image", "placeholder": true},
    "image_2": {"type": "image", "placeholder": true}
  }
}
```

### 🎯 Template Processor - Chương trình xử lý Template

Tạo file `template_processor.py`:

```python
import json
from typing import Dict, List, Any
from create_draft import get_or_create_draft
from add_image_impl import add_image_impl
from add_video_keyframe_impl import add_video_keyframe_impl
from save_draft_impl import save_draft_impl

class TemplateProcessor:
    """Xử lý JSON template và điền nội dung"""
    
    def __init__(self, template_path: str):
        with open(template_path) as f:
            self.template = json.load(f)
        self.config = self.template.get("settings", {})
    
    def render(self, content_map: Dict[str, Any]) -> str:
        """
        Render template với nội dung thực
        
        Args:
            content_map: {
                "image_0": "https://...",
                "image_1": "https://...",
                ...
            }
        
        Returns:
            draft_id
        """
        draft_id = None
        slot_keys = sorted(self.template["slots"].keys())
        
        for idx, slot_key in enumerate(slot_keys):
            if slot_key not in content_map:
                continue
            
            content = content_map[slot_key]
            clip_start = idx * self.config["duration_per_slide"]
            clip_end = clip_start + self.config["duration_per_slide"]
            
            # Thêm ảnh
            r = add_image_impl(
                image_url=content,
                start=clip_start,
                end=clip_end,
                **self.config["canvas"],
                track_name="video",
                draft_id=draft_id,
                transition=self.config["transition"]["type"] if idx > 0 else None,
                transition_duration=self.config["transition"]["duration"],
            )
            draft_id = r["output"]["draft_id"]
            
            # Thêm keyframes từ template
            for element in self.template["tracks"]["video"]["elements"]:
                for kf in element.get("keyframes", []):
                    add_video_keyframe_impl(
                        draft_id=draft_id,
                        track_name="video",
                        property_type=kf["property_type"],
                        time=clip_start + 0.01,
                        value=kf["at_start"]
                    )
                    add_video_keyframe_impl(
                        draft_id=draft_id,
                        track_name="video",
                        property_type=kf["property_type"],
                        time=clip_end - 0.01,
                        value=kf["at_end"]
                    )
        
        # Lưu draft
        save_draft_impl(draft_id, "/path/to/capcut")
        return draft_id

# 🎯 Ví dụ sử dụng
if __name__ == "__main__":
    processor = TemplateProcessor("template/slideshow-template.json")
    
    draft_id = processor.render({
        "image_0": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
        "image_1": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
        "image_2": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    })
    
    print(f"✅ Draft created: {draft_id}")
```

Thêm MCP tool:
```python
{
    "name": "render_template",
    "description": "Render video from JSON template",
    "inputSchema": {
        "type": "object",
        "properties": {
            "template_name": {"type": "string", "description": "e.g. 'slideshow-template'"},
            "content": {"type": "object", "description": "Content map: {slot: url/value}"}
        },
        "required": ["template_name", "content"]
    }
}
```

---

## 🤖 Giải pháp 3: LLM Parser Layer (Tự động hoàn toàn)

### 📌 Khái niệm
LLM tự động:
1. Parse mô tả từ user
2. Xác định template phù hợp (hoặc patterns)
3. Extract tham số cần thiết
4. Generate MCP calls tự động

### 🎯 Ưu điểm
- ✅ Hoàn toàn tự động từ mô tả
- ✅ Linh hoạt, hỗ trợ nhiều kịch bản
- ❌ Phức tạp hơn, cần LLM API

### 🔧 Cách triển khai

#### 1️⃣ Định nghĩa Schema cho LLM

Tạo file `mcp_template_schema.json`:

```json
{
  "templates": [
    {
      "name": "slideshow",
      "triggers": ["slideshow", "carousel", "image gallery"],
      "required_params": ["images"],
      "optional_params": ["effects", "duration", "transition_type"],
      "instruction": "Create slideshow from images list"
    },
    {
      "name": "kol_video",
      "triggers": ["KOL", "influencer", "product review"],
      "required_params": ["product_name", "script"],
      "optional_params": ["logo", "background_music"]
    },
    {
      "name": "tutorial",
      "triggers": ["tutorial", "how-to", "guide"],
      "required_params": ["steps"],
      "optional_params": ["intro_text", "outro_text"]
    }
  ],
  "effects": [
    {
      "name": "zoom_in",
      "description": "Scale 1.0 → 1.25",
      "params": {}
    },
    {
      "name": "pan_left_right",
      "description": "Move from left to right",
      "params": {}
    }
  ]
}
```

#### 2️⃣ LLM Parser

Tạo file `llm_parser.py`:

```python
import json
import re
from typing import Dict, List, Any
from openai import OpenAI  # hoặc Claude, Gemini, v.v.

class VideoDescriptionParser:
    """Parse mô tả video → Structured plan"""
    
    def __init__(self, template_schema_path: str):
        with open(template_schema_path) as f:
            self.schema = json.load(f)
    
    def parse(self, user_description: str) -> Dict[str, Any]:
        """
        User: "Tạo video slideshow 5 ảnh với zoom effect"
        ↓
        Output: {
            "template": "slideshow",
            "params": {
                "images": ["url1", "url2", ...],
                "effects": ["zoom_in"],
                "duration": 3.0
            }
        }
        """
        
        client = OpenAI()  # hoặc use Claude API
        
        system_prompt = f"""
        Bạn là chuyên gia phân tích mô tả video.
        
        Templates có sẵn:
        {json.dumps(self.schema['templates'], indent=2, ensure_ascii=False)}
        
        Nhiệm vụ:
        1. Xác định template nào phù hợp nhất
        2. Extract tham số từ mô tả
        3. Return JSON structured
        
        Output format:
        {{
            "template": "template_name",
            "params": {{
                "param_name": "value",
                ...
            }},
            "confidence": 0.95,
            "notes": "Any special instructions"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_description}
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        
        # Parse JSON từ response
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        return {"error": "Failed to parse"}

# 🎯 Ví dụ sử dụng
if __name__ == "__main__":
    parser = VideoDescriptionParser("mcp_template_schema.json")
    
    result = parser.parse(
        "Tạo video slideshow từ 5 ảnh du lịch, mỗi ảnh 3 giây, "
        "có zoom in effect, transition dissolve"
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # Output:
    # {
    #   "template": "slideshow",
    #   "params": {
    #     "images": [],  # LLM không thể fetch URL, user cần cung cấp
    #     "effects": ["zoom_in"],
    #     "duration": 3.0,
    #     "transition_type": "Dissolve"
    #   },
    #   "confidence": 0.95
    # }
```

#### 3️⃣ Integration với MCP

Tạo MCP tool mới:

```python
{
    "name": "create_from_description",
    "description": "Auto-create video from natural language description",
    "inputSchema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Video description in natural language"
            },
            "content_data": {
                "type": "object",
                "description": "Actual content (images URLs, text, etc)"
            }
        },
        "required": ["description", "content_data"]
    }
}
```

Thêm vào `mcp_server.py`:

```python
def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    # ... existing code ...
    
    elif tool_name == "create_from_description":
        from llm_parser import VideoDescriptionParser
        from template_processor import TemplateProcessor
        
        parser = VideoDescriptionParser("mcp_template_schema.json")
        plan = parser.parse(arguments["description"])
        
        if "error" in plan:
            return {"success": False, "error": plan["error"]}
        
        template_name = plan["template"]
        processor = TemplateProcessor(f"template/{template_name}-template.json")
        
        # Merge LLM-extracted params với user-provided content
        content_map = arguments.get("content_data", {})
        
        draft_id = processor.render(content_map)
        
        return {
            "success": True,
            "draft_id": draft_id,
            "used_template": template_name,
            "extracted_params": plan["params"]
        }
```

---

## 📊 So sánh & Lựa chọn

| Tiêu chí | Pattern Template | JSON Template | LLM Parser |
|---------|------------------|---------------|-----------|
| **Độ phức tạp** | 🟢 Đơn giản | 🟡 Trung bình | 🔴 Phức tạp |
| **Tự động hóa** | 🟡 Một phần | 🟡 Một phần | 🟢 Hoàn toàn |
| **Tái sử dụng** | 🟡 Giới hạn | 🟢 Cao | 🟢 Cao |
| **Khó custom** | 🟢 Dễ | 🟡 Trung bình | 🟡 Trung bình |
| **Chi phí** | 💰 Free | 💰 Free | 💸 API calls |
| **Tốc độ dev** | 🟢 Nhanh | 🟡 Trung bình | 🔴 Chậm |

### 🎯 Khuyến nghị

| Trường hợp | Giải pháp |
|-----------|----------|
| Video có **cấu trúc cố định** (slideshow, KOL video, v.v.) | **Pattern Template** |
| Muốn **linh hoạt hơn**, cho phép customize layout | **JSON Template** |
| Cần **tự động 100%** từ mô tả, không care chi phí API | **LLM Parser** |
| **Combo tối ưu** (Recommended) | Pattern + JSON Template (không cần LLM) |

---

## 🚀 Bắt đầu ngay

### Step 1: Tạo Pattern Template (15 phút)
```bash
cp pattern/test_slideshow.py pattern/slideshow-template.py
# Tùy chỉnh class SlideshowTemplate
```

### Step 2: Tạo JSON Template (10 phút)
```bash
cp template/draft_info.json template/slideshow-template.json
# Cập nhật slots, keyframes
```

### Step 3: Tạo Template Processor (20 phút)
```python
# Tạo template_processor.py
# Thêm MCP tool: render_template
```

### Step 4 (Optional): LLM Parser
```python
# Tạo llm_parser.py (nếu muốn full auto)
# Thêm MCP tool: create_from_description
```

---

## 📚 Tài liệu tham khảo

- [Pattern Examples](./pattern/)
- [Template Structure](./template/)
- [MCP Server](./mcp_server.py)
- [Test Slideshow](./test_slideshow.py)

---

**Bắt đầu bằng Pattern Template - nó đơn giản nhất và đã bao nhận 80% trường hợp sử dụng!** 🚀
