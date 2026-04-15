#!/usr/bin/env python3
"""
Manual Test MCP Tools - Test các tính năng vừa thêm
Run: python manual_test_mcp.py
"""

import json
import subprocess
import sys
import time
import os

def run_tool(tool_name, tool_input):
    """Gọi MCP tool thông qua test_mcp_client.py"""
    # Sử dụng test file có sẵn
    cmd = f"""python -c "
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
from test_mcp_client import call_mcp_tool

result = call_mcp_tool('{tool_name}', {json.dumps(tool_input)})
print(json.dumps(result, indent=2, ensure_ascii=False))
" """
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None


def test_list_templates():
    """Test 1: list_templates - xem templates có sẵn"""
    print("\n" + "="*80)
    print("TEST 1: list_templates - Liệt kê templates")
    print("="*80)
    
    result = run_tool("list_templates", {"preview": True})
    if result and "templates" in result:
        templates = result["templates"]
        print(f"\n✅ Found {len(templates)} template(s)")
        for t in templates:
            print(f"  📄 {t['name']:25s} | {t.get('description', '?')[:50]}")
        return True
    else:
        print("❌ Failed to list templates")
        return False


def test_analyze_draft():
    """Test 2: analyze_draft - phân tích draft CapCut"""
    print("\n" + "="*80)
    print("TEST 2: analyze_draft - Phân tích draft")
    print("="*80)
    
    # Tìm path đến draft thật hoặc dùng mock
    draft_folder = "C:/Users/DUC CANH PC/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft"
    if not os.path.exists(draft_folder):
        # Dùng template folder có draft_info.json
        draft_folder = "./template"
        print(f"⚠️  CapCut draft folder không tìm thấy, dùng template folder: {draft_folder}")
    
    print(f"📂 Analyzing: {draft_folder}")
    
    result = run_tool("analyze_draft", {"draft_path": draft_folder})
    if result and "tracks" in result:
        tracks = result["tracks"]
        print(f"\n✅ Analyzed {len(tracks)} track(s)")
        for i, track in enumerate(tracks):
            print(f"\n  [{i}] {track.get('name', 'unknown'):25s}")
            print(f"      Type: {track.get('track_type', '?'):10s} | Segments: {track.get('segment_count', 0)}")
            print(f"      Position: x={track.get('transform_x', 0):.4f}, y={track.get('transform_y', 0):.4f}")
            print(f"      Scale: x={track.get('scale_x', 1):.4f}, y={track.get('scale_y', 1):.4f}")
            print(f"      🤖 Suggest: {track.get('suggested_role', 'unknown')}")
        return True
    else:
        print("❌ Failed to analyze draft")
        return False


def test_export_draft_template():
    """Test 3: export_draft_template - export draft thành template"""
    print("\n" + "="*80)
    print("TEST 3: export_draft_template - Export draft → template")
    print("="*80)
    
    draft_folder = "./template"  # Mock draft
    
    # Bước 1: Tag tracks
    track_roles = {
        "0": "background",      # nếu có
        "1": "logo",            # nếu có
        "2": "script_text",     # nếu có
    }
    
    print(f"📂 Draft: {draft_folder}")
    print(f"🏷️  Track roles:")
    for idx, role in track_roles.items():
        print(f"   Track {idx} → {role}")
    
    result = run_tool("export_draft_template", {
        "draft_path": draft_folder,
        "template_name": "manual-test-podcast",
        "track_roles": track_roles,
        "auto_tag": True,  # Auto-detect nếu không match
    })
    
    if result and "template" in result:
        template = result["template"]
        print(f"\n✅ Template exported successfully")
        print(f"   Name: {template.get('name', '?')}")
        print(f"   Version: {template.get('version', '?')}")
        print(f"   Layers: {len(template.get('layers', []))}")
        
        for layer in template.get("layers", []):
            opt = " (optional)" if layer.get("optional") else ""
            print(f"     • {layer['id']:20s} | {layer['type']:15s}{opt}")
        
        print(f"\n   📁 Saved to: template/manual-test-podcast.json")
        return True
    else:
        print("❌ Failed to export template")
        print(f"Response: {result}")
        return False


def test_render_template():
    """Test 4: render_template - render video từ template"""
    print("\n" + "="*80)
    print("TEST 4: render_template - Render video")
    print("="*80)
    
    template_name = "podcast-video-v1"  # Default template có sẵn
    
    print(f"📄 Template: {template_name}")
    print(f"\nPreparing segments...")
    
    segments = [
        {
            "text": "Artificial Intelligence thay đổi thế giới",
            "duration": 4.0,
            "image_url": "https://via.placeholder.com/1080x1920/FF6B6B/FFFFFF?text=AI+Today",
        },
        {
            "text": "Từ chatbots đến AGI - chúng ta đi đâu?",
            "duration": 4.5,
            "image_url": "https://via.placeholder.com/1080x1920/4ECDC4/FFFFFF?text=AGI+Future",
        },
        {
            "text": "Nhưng bạn sẽ làm gì khi AI thế chỗ mình?",
            "duration": 3.5,
            "image_url": "https://via.placeholder.com/1080x1920/45B7D1/FFFFFF?text=What+Now",
        },
    ]
    
    for i, seg in enumerate(segments):
        print(f"  [{i}] {seg['text'][:50]:50s} | {seg['duration']}s")
    
    result = run_tool("render_template", {
        "template_name": template_name,
        "segments": segments,
        "logo_url": "https://via.placeholder.com/200x200/FFFFFF/000000?text=LOGO",
        "play_icon_url": "https://via.placeholder.com/100x100/FF0000/FFFFFF?text=▶",
    })
    
    if result and "draft_id" in result:
        print(f"\n✅ Video rendered successfully!")
        print(f"   Draft ID: {result['draft_id']}")
        print(f"   Canvas: {result.get('canvas_config', {})}")
        print(f"   Duration: {result.get('total_duration_sec', 0):.1f}s")
        print(f"   Tracks created: {result.get('tracks_created', 0)}")
        print(f"   Total segments: {result.get('total_segments', 0)}")
        
        if "save_path" in result:
            print(f"   📁 Path: {result['save_path']}")
        
        return True
    else:
        print("❌ Failed to render template")
        print(f"Response: {result}")
        return False


def test_workflow():
    """Test 5: Full workflow - analyze → export → render"""
    print("\n" + "="*80)
    print("TEST 5: Full Workflow - Analyze → Export → Render")
    print("="*80)
    
    print("""
    Workflow:
    1️⃣  User: "Hãy export draft này thành template"
         ↓
    2️⃣  AI: analyze_draft → xem tracks, gợi ý role
         ↓
    3️⃣  User/AI: export_draft_template → save template
         ↓
    4️⃣  User: "Tạo video podcast với template"
         ↓
    5️⃣  AI: render_template → video tạo xong!
    """)
    
    print("\n🔄 Simulating workflow...")
    
    # Bước 1: Analyze
    print("\n[Step 1] Analyzing draft...", end="", flush=True)
    result1 = run_tool("analyze_draft", {"draft_path": "./template"})
    print(" ✓")
    
    # Bước 2: Export
    print("[Step 2] Exporting template...", end="", flush=True)
    track_roles = {}
    if result1 and "tracks" in result1:
        for i, t in enumerate(result1["tracks"][:3]):  # Tag first 3 tracks
            role_guess = t.get("suggested_role", "skip")
            if role_guess != "skip":
                track_roles[str(i)] = role_guess
    
    result2 = run_tool("export_draft_template", {
        "draft_path": "./template",
        "template_name": "workflow-test",
        "track_roles": track_roles,
        "auto_tag": True,
    })
    print(" ✓")
    
    # Bước 3: Render
    print("[Step 3] Rendering video...", end="", flush=True)
    segments = [
        {"text": "Segment 1", "duration": 3.0, "image_url": "https://via.placeholder.com/1080x1920"},
        {"text": "Segment 2", "duration": 3.0, "image_url": "https://via.placeholder.com/1080x1920"},
    ]
    result3 = run_tool("render_template", {
        "template_name": "podcast-video-v1",
        "segments": segments,
    })
    print(" ✓")
    
    if result1 and result2 and result3:
        print("\n✅ Full workflow completed successfully!")
        return True
    else:
        print("\n❌ Workflow failed")
        return False


def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║         Manual Test MCP Tools - Video Template & Export Features           ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    
    tests = [
        ("list_templates", test_list_templates),
        ("analyze_draft", test_analyze_draft),
        ("export_draft_template", test_export_draft_template),
        ("render_template", test_render_template),
        ("full workflow", test_workflow),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            print(f"❌ Exception in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print(f"📊 Results: {passed}/{len(tests)} passed, {failed} failed")
    print("="*80)


if __name__ == "__main__":
    main()
