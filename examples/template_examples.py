"""
🎬 Ví dụ thực hành: Template-Based Slideshow
Tạo slideshow từ template JSON một cách tự động
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from template_processor import TemplateProcessor, create_default_slideshow_template
import json

def example_1_basic_slideshow():
    """
    🎯 Ví dụ 1: Tạo slideshow cơ bản từ template
    """
    print("\n" + "="*70)
    print("📝 Ví dụ 1: Tạo slideshow cơ bản từ template JSON")
    print("="*70)
    
    # Step 1: Tạo template file
    template_dict = create_default_slideshow_template()
    template_path = "template/example-slideshow-1.json"
    
    print(f"\n1️⃣  Tạo template file: {template_path}")
    os.makedirs("template", exist_ok=True)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template_dict, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Template created")
    
    # Step 2: Chuẩn bị nội dung
    content_data = {
        "image_0": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop",
        "image_1": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720&fit=crop",
        "image_2": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720&fit=crop",
    }
    
    print(f"\n2️⃣  Chuẩn bị nội dung:")
    for slot, url in content_data.items():
        print(f"   • {slot}: {url[:50]}...")
    
    # Step 3: Render
    print(f"\n3️⃣  Render template:")
    processor = TemplateProcessor(template_path)
    result = processor.render(content_data)
    
    print(f"\n✨ Kết quả:")
    print(f"   Success: {result['success']}")
    if result['success']:
        print(f"   Draft ID: {result['draft_id']}")
        print(f"   Duration: {result['duration']:.1f}s")
        print(f"   Slots used: {result['slots_used']}")
        print(f"   Draft URL: {result['draft_url']}")
    else:
        print(f"   Error: {result['error']}")
    
    return result


def example_2_custom_template():
    """
    🎯 Ví dụ 2: Tạo template tùy chỉnh (5 ảnh với pan effect)
    """
    print("\n" + "="*70)
    print("📝 Ví dụ 2: Template tùy chỉnh (5 ảnh + Pan effect)")
    print("="*70)
    
    # Tạo template tùy chỉnh
    custom_template = {
        "name": "slideshow-5images-pan",
        "version": "1.0.0",
        "description": "Slideshow with 5 images and pan left-right effect",
        "settings": {
            "canvas": {"width": 1280, "height": 720},
            "duration_per_slide": 4.0,  # 4 giây per slide
            "transition": {
                "type": "CrossDissolve",
                "duration": 1.0  # 1 giây transition
            }
        },
        "tracks": {
            "video": {
                "type": "video",
                "elements": [
                    {
                        "type": "image",
                        "description": "Image with pan effect",
                        "keyframes": [
                            {
                                "type": "pan",
                                "property_type": "position_x",
                                "at_start": "-0.08",
                                "at_end": "0.08",
                                "description": "Pan từ trái sang phải"
                            },
                            {
                                "type": "scale",
                                "property_type": "scale_x",
                                "at_start": "1.15",
                                "at_end": "1.15",
                                "description": "Slight zoom"
                            },
                            {
                                "type": "scale",
                                "property_type": "scale_y",
                                "at_start": "1.15",
                                "at_end": "1.15"
                            }
                        ]
                    }
                ]
            }
        },
        "slots": {
            f"image_{i}": {"type": "image", "required": True}
            for i in range(5)
        }
    }
    
    template_path = "template/example-slideshow-2-pan.json"
    
    print(f"\n1️⃣  Tạo template với pan effect: {template_path}")
    os.makedirs("template", exist_ok=True)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(custom_template, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Template created")
    
    # Chuẩn bị 5 ảnh
    content_data = {
        f"image_{i}": f"https://images.unsplash.com/photo-{1506905925346+i}-21bda4d32df4?w=1280&h=720&fit=crop"
        for i in range(5)
    }
    
    # Fix URLs thực tế
    content_data = {
        "image_0": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop",
        "image_1": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720&fit=crop",
        "image_2": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720&fit=crop",
        "image_3": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1280&h=720&fit=crop",
        "image_4": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1280&h=720&fit=crop",
    }
    
    print(f"\n2️⃣  Chuẩn bị 5 ảnh")
    
    print(f"\n3️⃣  Render template:")
    processor = TemplateProcessor(template_path)
    result = processor.render(content_data)
    
    print(f"\n✨ Kết quả:")
    print(f"   Success: {result['success']}")
    if result['success']:
        print(f"   Draft ID: {result['draft_id']}")
        print(f"   Duration: {result['duration']:.1f}s (5 × 4s)")
        print(f"   Slots used: {result['slots_used']}")
    else:
        print(f"   Error: {result['error']}")
    
    return result


def example_3_compare_approaches():
    """
    🎯 Ví dụ 3: So sánh 3 cách tạo slideshow
    """
    print("\n" + "="*70)
    print("📊 Ví dụ 3: So sánh 3 cách tiếp cận")
    print("="*70)
    
    # 1. Manual approach (cũ)
    print(f"\n❌ Approach 1: Manual MCP calls")
    print(f"""
    User phải viết prompt:
    "add_image 1 at 0s, add_video_keyframe zoom, add_image 2 at 3s, ..."
    
    👎 Cần 15-20 API calls
    👎 Khó bảo trì
    👎 Dễ lỗi nếu quên bước
    """)
    
    # 2. Pattern approach
    print(f"\n🟡 Approach 2: Pattern Template")
    print(f"""
    from pattern.slideshow_template import SlideshowTemplate
    
    result = SlideshowTemplate.create_slideshow(
        image_urls=[...],
        effects=["zoom_in", "pan_left_right"],
        DURATION_PER_SLIDE=3.0
    )
    
    ✅ 5 lines code
    ✅ Structured
    ❌ Programmers only, không flexible lắm
    """)
    
    # 3. JSON Template approach
    print(f"\n🟢 Approach 3: JSON Template (Khuyến nghị)")
    print(f"""
    content_data = {{
        "image_0": "url1",
        "image_1": "url2",
        "image_2": "url3"
    }}
    
    processor = TemplateProcessor("template/slideshow.json")
    result = processor.render(content_data)
    
    ✅ 3 lines code
    ✅ Template có thể tạo từ UI
    ✅ Non-technical người cũng có thể dùng
    ✅ Dễ đọc, dễ share
    """)
    
    print(f"\n📊 Bảng so sánh:")
    print(f"""
    ┌────────────────┬──────────┬────────────┬──────────────┐
    │ Tiêu chí       │ Manual   │ Pattern    │ JSON Template│
    ├────────────────┼──────────┼────────────┼──────────────┤
    │ Code lines     │ 20+      │ 5-10       │ 3-5          │
    │ Tái sử dụng    │ Không    │ Có         │ Cao          │
    │ Dễ custom      │ Khó      │ Trung bình │ Dễ           │
    │ Dễ share       │ Không    │ Không      │ Có (JSON)    │
    │ Cho non-coder  │ Không    │ Không      │ Có           │
    │ Thích hợp      │ Demo     │ Lập trình  │ Production   │
    └────────────────┴──────────┴────────────┴──────────────┘
    """)


def example_4_template_anatomy():
    """
    🎯 Ví dụ 4: Giải thích cấu trúc template JSON
    """
    print("\n" + "="*70)
    print("🔍 Ví dụ 4: Giải thích cấu trúc template JSON")
    print("="*70)
    
    template = create_default_slideshow_template()
    
    print(f"\n📋 Cấu trúc template:")
    print(f"""
    {{
      "name": "slideshow-basic",           ← Template name (để tìm kiếm)
      "version": "1.0.0",                  ← Phiên bản
      "description": "...",                ← Mô tả
      
      "settings": {{
        "canvas": {{                       ← Video resolution
          "width": 1280,
          "height": 720
        }},
        "duration_per_slide": 3.0,         ← Mỗi ảnh dài 3s
        "transition": {{                   ← Transition giữa ảnh
          "type": "Dissolve",
          "duration": 0.5
        }}
      }},
      
      "tracks": {{                         ← Các tracks (video, audio, v.v.)
        "video": {{
          "type": "video",
          "elements": [
            {{
              "type": "image",
              "keyframes": [
                {{
                  "type": "zoom",
                  "property_type": "scale_x",
                  "at_start": "1.0",       ← Giá trị lúc bắt đầu
                  "at_end": "1.25"         ← Giá trị lúc kết thúc
                }},
                ...
              ]
            }}
          ]
        }}
      }},
      
      "slots": {{                          ← Placeholder cho nội dung
        "image_0": {{"type": "image"}},
        "image_1": {{"type": "image"}},
        "image_2": {{"type": "image"}}
      }}
    }}
    """)
    
    print(f"\n🎯 Cách tùy chỉnh template:")
    print(f"""
    1. Thay đổi duration:
       "duration_per_slide": 4.0  ← Từ 3s thành 4s
    
    2. Thay đổi transition:
       "type": "CrossDissolve"  ← Từ Dissolve thành CrossDissolve
       "duration": 1.0          ← Từ 0.5s thành 1s
    
    3. Thêm effect:
       Thêm keyframe mới vào "elements[0]["keyframes"]"
    
    4. Thêm slots:
       "image_3": {{"type": "image"}},  ← Cho 4 ảnh
       "image_4": {{"type": "image"}}
    """)


def example_5_mcp_integration():
    """
    🎯 Ví dụ 5: Cách integrate vào MCP server
    """
    print("\n" + "="*70)
    print("🔌 Ví dụ 5: Cách integrate với MCP server")
    print("="*70)
    
    print(f"""
    # Thêm tool này vào mcp_server.py:
    
    {{
        "name": "render_template",
        "description": "Create video from template + content data",
        "inputSchema": {{
            "type": "object",
            "properties": {{
                "template_name": {{
                    "type": "string",
                    "description": "e.g., 'slideshow-basic'"
                }},
                "content": {{
                    "type": "object",
                    "description": "Content data: {{'image_0': 'url', ...}}"
                }},
                "draft_folder": {{
                    "type": "string",
                    "description": "Path to CapCut draft folder (optional)"
                }}
            }},
            "required": ["template_name", "content"]
        }}
    }}
    
    # Thêm handler trong execute_tool():
    
    elif tool_name == "render_template":
        from template_processor import TemplateProcessor
        
        template_name = arguments["template_name"]
        template_path = f"template/{{template_name}}-template.json"
        
        processor = TemplateProcessor(template_path)
        result = processor.render(
            arguments["content"],
            arguments.get("draft_folder")
        )
        return {{"success": result["success"], "result": result}}
    
    # Cách sử dụng qua Claude/Copilot:
    
    User: "Create slideshow from these 3 images"
    ↓
    Call: render_template(
        template_name="slideshow-basic",
        content={{
            "image_0": "url1",
            "image_1": "url2",
            "image_2": "url3"
        }}
    )
    ↓
    Response: {{
        "success": true,
        "draft_id": "dfd_cat_...",
        "duration": 9.0,
        "slots_used": 3
    }}
    """)


if __name__ == "__main__":
    import sys
    
    # Chạy examples
    examples = {
        "1": ("Example 1: Basic slideshow", example_1_basic_slideshow),
        "2": ("Example 2: Custom template", example_2_custom_template),
        "3": ("Example 3: Compare approaches", example_3_compare_approaches),
        "4": ("Example 4: Template anatomy", example_4_template_anatomy),
        "5": ("Example 5: MCP integration", example_5_mcp_integration),
    }
    
    print("\n🎬 VectCutAPI Template Examples")
    print("="*70)
    print("\nAvailable examples:")
    for key, (desc, _) in examples.items():
        print(f"  {key}. {desc}")
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num in examples:
            examples[example_num][1]()
        else:
            print(f"❌ Example {example_num} not found")
    else:
        # Run all
        for key in sorted(examples.keys()):
            examples[key][1]()
    
    print("\n" + "="*70)
    print("✅ Examples completed!")
    print("="*70)
