"""
🎙️ Test Podcast Video Builder
Tạo video podcast từ template layer-based + script segments

Cấu trúc video:
  Layer 4 (top):    Logo + Play icon (persistent)
  Layer 3:          Title text (dynamic per segment)
  Layer 2:          Script text (dynamic per segment)
  Layer 1:          Dark overlay (persistent, optional)
  Layer 0 (bottom): Background images (slideshow + zoom/pan)
"""

import sys
import os

# Ensure project root in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from video_builder import VideoBuilder, RenderInput, Segment


# ── Sample data ────────────────────────────────────────────────────

LOGO_URL = "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=200&h=200&fit=crop"

SEGMENTS = [
    {
        "text": "Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc và sống mỗi ngày.",
        "title": "AI & Cuộc sống",
        "duration": 4.0,
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080&h=1920&fit=crop",
    },
    {
        "text": "Từ chatbot đến xe tự lái, AI đang hiện diện ở khắp nơi xung quanh chúng ta.",
        "title": "",
        "duration": 4.0,
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1080&h=1920&fit=crop",
    },
    {
        "text": "Nhưng liệu chúng ta đã sẵn sàng cho một tương lai do AI định hình?",
        "title": "",
        "duration": 3.5,
        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1080&h=1920&fit=crop",
    },
    {
        "text": "Hãy cùng khám phá những cơ hội và thách thức phía trước trong tập podcast này.",
        "title": "Cơ hội & Thách thức",
        "duration": 5.0,
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&h=1920&fit=crop",
    },
    {
        "text": "Đăng ký kênh để không bỏ lỡ những tập tiếp theo!",
        "title": "Subscribe!",
        "duration": 3.0,
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&h=1920&fit=crop",
    },
]


def test_preview_template():
    """Test 1: Preview template (không render, không cần server)"""
    print("\n" + "="*60)
    print("🔍 TEST 1: Preview template")
    print("="*60)

    info = VideoBuilder.preview_template("template/podcast-video-v1.json")

    print(f"\n📋 Template: {info['name']}")
    print(f"📺 Canvas: {info['canvas']['width']}×{info['canvas']['height']}")
    print(f"🎚️  Layers: {info['layer_count']}")

    for layer in info["layers"]:
        opt = " (optional)" if layer["optional"] else ""
        print(f"   [{layer['z_index']}] {layer['id']:20s} | {layer['type']:20s}{opt}")
        print(f"       {layer['description']}")

    print(f"\n🎬 Motion presets: {', '.join(info['motion_presets'])}")

    return info


def test_list_templates():
    """Test 2: List available templates"""
    print("\n" + "="*60)
    print("📂 TEST 2: List templates")
    print("="*60)

    templates = VideoBuilder.list_templates("template")

    if templates:
        for t in templates:
            print(f"\n   📄 {t['name']}")
            print(f"      Path: {t['path']}")
            print(f"      Layers: {t['layers']}")
            print(f"      Desc: {t['description'][:80]}...")
    else:
        print("   ❌ No v2 templates found in template/")

    return templates


def test_render_podcast():
    """Test 3: Render podcast video (cần server hoặc local modules)"""
    print("\n" + "="*60)
    print("🎬 TEST 3: Render podcast video")
    print("="*60)

    # Load template
    builder = VideoBuilder("template/podcast-video-v1.json")

    # Build input
    render_input = RenderInput(
        segments=[Segment.from_dict(s) for s in SEGMENTS],
        logo_url=LOGO_URL,
        play_icon_url="",   # Không có play icon
        overlay_url="",     # Không có overlay
    )

    print(f"\n📊 Input:")
    print(f"   Segments: {len(render_input.segments)}")
    total_dur = sum(s.duration for s in render_input.segments)
    print(f"   Total duration: {total_dur:.1f}s")
    print(f"   Logo: {'✓' if render_input.logo_url else '✗'}")

    for i, seg in enumerate(render_input.segments):
        title = f" [{seg.title}]" if seg.title else ""
        print(f"   [{i}] {seg.duration:.1f}s{title}: {seg.text[:50]}...")

    # Render
    print(f"\n🚀 Rendering...")
    result = builder.render(render_input)

    print(f"\n📊 Result:")
    print(f"   Success: {result['success']}")
    if result["success"]:
        print(f"   Draft ID: {result['draft_id']}")
        print(f"   Duration: {result['total_duration']:.1f}s")
        print(f"   Segments: {result['segment_count']}")
        print(f"   Layers: {', '.join(result['layers_rendered'])}")
    else:
        print(f"   Error: {result.get('error')}")

    return result


def test_render_from_dict():
    """Test 4: Render từ dict (giống cách MCP gọi)"""
    print("\n" + "="*60)
    print("🔌 TEST 4: Render từ dict (MCP format)")
    print("="*60)

    # Đây là format mà MCP tool sẽ nhận
    mcp_arguments = {
        "template_name": "podcast-video-v1",
        "segments": SEGMENTS,
        "logo_url": LOGO_URL,
        "play_icon_url": "",
        "overlay_url": "",
    }

    template_path = os.path.join("template", f"{mcp_arguments['template_name']}.json")
    builder = VideoBuilder(template_path)
    render_input = RenderInput.from_dict(mcp_arguments)

    result = builder.render(render_input)

    print(f"\n📊 Result: {'✅' if result['success'] else '❌'}")
    if result["success"]:
        print(f"   Draft ID: {result['draft_id']}")
        print(f"   Duration: {result['total_duration']:.1f}s")

    return result


def test_custom_template():
    """Test 5: Tạo template custom on-the-fly"""
    print("\n" + "="*60)
    print("✏️  TEST 5: Custom template")
    print("="*60)

    import json

    # Clone template và sửa settings
    with open("template/podcast-video-v1.json", encoding="utf-8") as f:
        custom = json.load(f)

    # Đổi tên
    custom["name"] = "podcast-dark-mode"

    # Đổi text style: font lớn hơn, nền tối
    for layer in custom["layers"]:
        if layer["id"] == "script_text":
            layer["style"]["font_size"] = 10.0
            layer["style"]["font_color"] = "#00FF88"
            layer["style"]["background_alpha"] = 0.6
            layer["style"]["background_round_radius"] = 0.1
            layer["style"]["transform_y"] = 0.4

        if layer["id"] == "title_text":
            layer["style"]["font_size"] = 14.0
            layer["style"]["font_color"] = "#FF6600"

    # Đổi motion presets: chỉ zoom
    for layer in custom["layers"]:
        if layer["id"] == "background":
            layer["motion"]["presets"] = ["zoom_in", "zoom_out"]

    # Save custom template
    os.makedirs("template", exist_ok=True)
    with open("template/podcast-dark-mode.json", "w", encoding="utf-8") as f:
        json.dump(custom, f, indent=2, ensure_ascii=False)

    print("   ✅ Custom template created: template/podcast-dark-mode.json")
    print("   Changes:")
    print("     - Script text: font_size=10, color=#00FF88, bg_alpha=0.6")
    print("     - Title text: font_size=14, color=#FF6600")
    print("     - Motion: zoom only (no pan)")

    # Preview
    info = VideoBuilder.preview_template("template/podcast-dark-mode.json")
    print(f"\n   📋 {info['name']}: {info['layer_count']} layers")
    print(f"       Motion: {', '.join(info['motion_presets'])}")


if __name__ == "__main__":
    import sys

    tests = {
        "1": ("Preview template", test_preview_template),
        "2": ("List templates", test_list_templates),
        "3": ("Render podcast video", test_render_podcast),
        "4": ("Render from dict (MCP)", test_render_from_dict),
        "5": ("Custom template", test_custom_template),
    }

    print("🎙️ Podcast Video Builder Tests")
    print("="*60)

    if len(sys.argv) > 1:
        test_num = sys.argv[1]
        if test_num in tests:
            tests[test_num][1]()
        else:
            print(f"❌ Test {test_num} not found")
    else:
        # Chạy test 1, 2, 5 (không cần server)
        print("Running tests that don't require server...")
        test_preview_template()
        test_list_templates()
        test_custom_template()

        print("\n" + "="*60)
        print("ℹ️  To run render tests (need server running):")
        print("   python test_podcast_video.py 3   # Render podcast")
        print("   python test_podcast_video.py 4   # MCP format")

    print("\n" + "="*60)
    print("✅ Tests completed!")
