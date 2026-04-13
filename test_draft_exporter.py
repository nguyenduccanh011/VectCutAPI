"""Test Draft Exporter - kiểm tra export CapCut draft → template"""

import json
import os
import tempfile
import shutil
from draft_exporter import DraftExporter, LAYER_ROLES


def create_mock_draft(tmp_dir: str) -> str:
    """Tạo mock draft_info.json giống cấu trúc CapCut thật"""
    draft_path = os.path.join(tmp_dir, "test_draft")
    os.makedirs(draft_path, exist_ok=True)

    # Mock canvas 1080x1920
    draft_info = {
        "canvas_config": {"width": 1080, "height": 1920},
        "materials": {
            "videos": [
                # Background images (5 segments)
                {"id": "mat_bg_1", "path": "/photos/bg1.jpg", "type": "photo"},
                {"id": "mat_bg_2", "path": "/photos/bg2.jpg", "type": "photo"},
                {"id": "mat_bg_3", "path": "/photos/bg3.jpg", "type": "photo"},
                {"id": "mat_bg_4", "path": "/photos/bg4.jpg", "type": "photo"},
                {"id": "mat_bg_5", "path": "/photos/bg5.jpg", "type": "photo"},
                # Logo (1 segment)
                {"id": "mat_logo", "path": "/photos/logo.png", "type": "photo"},
                # Play icon
                {"id": "mat_play", "path": "/photos/play_icon.png", "type": "photo"},
                # Overlay
                {"id": "mat_overlay", "path": "/photos/dark_overlay.png", "type": "photo"},
            ],
            "texts": [
                {
                    "id": "mat_text_1",
                    "content": json.dumps({
                        "text": "Segment 1 text here...",
                        "styles": [{
                            "range": [0, 22],
                            "size": 7.0,
                            "fill": {"content": {"solid": {"color": [1.0, 1.0, 1.0]}}},
                            "font": {"id": "Roboto-Bold"},
                            "stroke": {
                                "content": {"solid": {"color": [0, 0, 0], "alpha": 1.0}},
                                "width": 0.08
                            },
                            "shadow": {
                                "color": {"solid": {"color": [0, 0, 0], "alpha": 0.6}},
                                "distance": 4.0,
                                "angle": -45.0,
                                "smoothing": 0.12
                            }
                        }]
                    }),
                },
                {
                    "id": "mat_text_2",
                    "content": json.dumps({
                        "text": "Segment 2 text here...",
                        "styles": [{
                            "range": [0, 22],
                            "size": 7.0,
                            "fill": {"content": {"solid": {"color": [1.0, 1.0, 0.8]}}},
                            "font": {"id": "Roboto-Bold"},
                        }]
                    }),
                },
                {
                    "id": "mat_text_3",
                    "content": json.dumps({
                        "text": "Segment 3 text here...",
                        "styles": [{
                            "range": [0, 22],
                            "size": 7.0,
                            "fill": {"content": {"solid": {"color": [1.0, 1.0, 1.0]}}},
                            "font": {"id": "Roboto-Bold"},
                        }]
                    }),
                },
            ],
            "audios": [],
            "stickers": [],
            "speeds": [],
            "material_animations": [],
            "effects": [],
            "transitions": [],
            "canvases": [],
            "masks": [],
        },
        "tracks": [
            # Track 0: Background images (5 segments, dynamic)
            {
                "id": "track_bg", "name": "bg_track", "type": "video",
                "segments": [
                    {
                        "material_id": f"mat_bg_{i+1}",
                        "target_timerange": {"start": i * 5000000, "duration": 5000000},
                        "clip": {"alpha": 1.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}, "rotation": 0.0},
                        "extra_material_refs": [],
                    }
                    for i in range(5)
                ],
            },
            # Track 1: Dark overlay (1 segment, persistent)
            {
                "id": "track_overlay", "name": "overlay_track", "type": "video",
                "segments": [
                    {
                        "material_id": "mat_overlay",
                        "target_timerange": {"start": 0, "duration": 25000000},
                        "clip": {"alpha": 0.5, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}, "rotation": 0.0},
                        "extra_material_refs": [],
                    }
                ],
            },
            # Track 2: Script text (3 segments, dynamic)
            {
                "id": "track_text", "name": "text_track", "type": "text",
                "segments": [
                    {
                        "material_id": f"mat_text_{i+1}",
                        "target_timerange": {"start": i * 8000000, "duration": 8000000},
                        "clip": {"alpha": 1.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.3}, "rotation": 0.0},
                        "extra_material_refs": [],
                    }
                    for i in range(3)
                ],
            },
            # Track 3: Logo (1 segment, small, persistent)
            {
                "id": "track_logo", "name": "logo_track", "type": "video",
                "segments": [
                    {
                        "material_id": "mat_logo",
                        "target_timerange": {"start": 0, "duration": 25000000},
                        "clip": {"alpha": 1.0, "scale": {"x": 0.12, "y": 0.12}, "transform": {"x": -0.4, "y": -0.45}, "rotation": 0.0},
                        "extra_material_refs": [],
                    }
                ],
            },
            # Track 4: Play icon (1 segment, small, persistent)
            {
                "id": "track_play", "name": "play_track", "type": "video",
                "segments": [
                    {
                        "material_id": "mat_play",
                        "target_timerange": {"start": 0, "duration": 25000000},
                        "clip": {"alpha": 0.8, "scale": {"x": 0.15, "y": 0.15}, "transform": {"x": 0.0, "y": 0.0}, "rotation": 0.0},
                        "extra_material_refs": [],
                    }
                ],
            },
        ],
    }

    with open(os.path.join(draft_path, "draft_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_info, f, indent=2)

    return draft_path


def test_analyze():
    """Test 1: Analyze draft"""
    print("\n" + "="*60)
    print("TEST 1: Analyze Draft")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        exporter = DraftExporter(draft_path)
        tracks = exporter.analyze()

        assert len(tracks) == 5, f"Expected 5 tracks, got {len(tracks)}"
        assert tracks[0].name == "bg_track"
        assert tracks[0].segment_count == 5
        assert tracks[0].track_type == "video"
        assert tracks[1].name == "overlay_track"
        assert tracks[1].segment_count == 1
        assert tracks[2].name == "text_track"
        assert tracks[2].track_type == "text"
        assert tracks[2].segment_count == 3
        assert tracks[3].name == "logo_track"
        assert tracks[3].scale_x == 0.12
        assert tracks[3].transform_x == -0.4

        exporter.print_analysis()
        print("\nTEST 1 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_auto_tag():
    """Test 2: Auto tag by track name convention"""
    print("\n" + "="*60)
    print("TEST 2: Auto Tag")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        exporter = DraftExporter(draft_path)
        exporter.analyze()

        tagged = exporter.auto_tag()
        print(f"\nAuto-tagged {tagged} tracks")

        assert tagged == 5, f"Expected 5 auto-tagged, got {tagged}"
        assert exporter.tracks[0].role == "background"
        assert exporter.tracks[1].role == "overlay"
        assert exporter.tracks[2].role == "script_text"
        assert exporter.tracks[3].role == "logo"
        assert exporter.tracks[4].role == "play_icon"

        print("TEST 2 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_manual_tag():
    """Test 3: Manual tag by index and name"""
    print("\n" + "="*60)
    print("TEST 3: Manual Tag")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        exporter = DraftExporter(draft_path)
        exporter.analyze()

        exporter.tag_track("0", "background")
        exporter.tag_track("overlay_track", "overlay")
        exporter.tag_track("2", "script_text")
        exporter.tag_track("logo_track", "logo")
        exporter.tag_track("4", "play_icon")

        assert exporter.tracks[0].role == "background"
        assert exporter.tracks[1].role == "overlay"
        assert exporter.tracks[2].role == "script_text"
        assert exporter.tracks[3].role == "logo"
        assert exporter.tracks[4].role == "play_icon"

        print("TEST 3 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_suggest_role():
    """Test 4: Role suggestion heuristics"""
    print("\n" + "="*60)
    print("TEST 4: Suggest Role")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        exporter = DraftExporter(draft_path)
        exporter.analyze()

        suggestions = [exporter._suggest_role(t) for t in exporter.tracks]
        print(f"  Suggestions: {suggestions}")

        assert suggestions[0] == "background"     # 5 video segments
        assert suggestions[1] == "overlay"         # 1 video segment, full scale
        assert suggestions[2] == "script_text"     # 3 text segments
        assert suggestions[3] == "logo"            # 1 video, scale 0.12
        assert suggestions[4] == "logo"            # 1 video, scale 0.15 (small → logo heuristic)

        print("TEST 4 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_export_template():
    """Test 5: Full export flow"""
    print("\n" + "="*60)
    print("TEST 5: Export Template")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        output_dir = os.path.join(tmp_dir, "template_output")

        exporter = DraftExporter(draft_path)
        exporter.analyze()
        exporter.auto_tag()

        template = exporter.export_template("test-podcast", output_dir=output_dir)

        # Verify template structure
        assert template["name"] == "test-podcast"
        assert template["version"] == "2.0.0"
        assert template["canvas"]["width"] == 1080
        assert template["canvas"]["height"] == 1920

        layers = template["layers"]
        assert len(layers) == 5

        # Check layers
        layer_ids = [l["id"] for l in layers]
        assert "background" in layer_ids
        assert "overlay" in layer_ids
        assert "script_text" in layer_ids
        assert "logo" in layer_ids
        assert "play_icon" in layer_ids

        # Check background layer
        bg = next(l for l in layers if l["id"] == "background")
        assert bg["type"] == "dynamic_image"
        assert "transition" in bg
        assert "motion" in bg

        # Check logo layer
        logo = next(l for l in layers if l["id"] == "logo")
        assert logo["type"] == "persistent_image"
        assert logo["style"]["scale_x"] == 0.12
        assert logo["style"]["transform_x"] == -0.4

        # Check text layer
        text = next(l for l in layers if l["id"] == "script_text")
        assert text["type"] == "dynamic_text"
        assert text["style"]["font_size"] == 7.0
        assert text["style"]["font_color"] == "#FFFFFF"
        assert text["style"]["transform_y"] == 0.3
        assert text["style"]["border_width"] == 0.08

        # Check shadow extracted
        assert text["style"]["shadow_enabled"] == True
        assert text["style"]["shadow_distance"] == 4.0

        # Verify file was saved
        output_path = os.path.join(output_dir, "test-podcast.json")
        assert os.path.exists(output_path)

        # Reload and verify
        with open(output_path, encoding="utf-8") as f:
            saved = json.load(f)
        assert saved == template

        # Print template
        print(json.dumps(template, indent=2))

        print("\nTEST 5 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_text_style_extraction():
    """Test 6: Detailed text style extraction"""
    print("\n" + "="*60)
    print("TEST 6: Text Style Extraction")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        exporter = DraftExporter(draft_path)
        tracks = exporter.analyze()

        text_track = tracks[2]  # text_track
        assert text_track.font_size == 7.0
        assert text_track.font_color == "#FFFFFF"
        assert text_track.font == "Roboto-Bold"

        print(f"  Font: {text_track.font}")
        print(f"  Size: {text_track.font_size}")
        print(f"  Color: {text_track.font_color}")
        print(f"  Position: ({text_track.transform_x}, {text_track.transform_y})")

        print("TEST 6 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


def test_no_content_in_template():
    """Test 7: Verify template does NOT contain content URLs or text"""
    print("\n" + "="*60)
    print("TEST 7: No Content in Template")
    print("="*60)

    tmp_dir = tempfile.mkdtemp()
    try:
        draft_path = create_mock_draft(tmp_dir)
        output_dir = os.path.join(tmp_dir, "template_output")

        exporter = DraftExporter(draft_path)
        exporter.analyze()
        exporter.auto_tag()

        template = exporter.export_template("test-no-content", output_dir=output_dir)

        template_str = json.dumps(template)

        # Template MUST NOT contain content
        assert "/photos/" not in template_str, "Template should not contain file paths!"
        assert "Segment 1" not in template_str, "Template should not contain text content!"
        assert "bg1.jpg" not in template_str, "Template should not contain image filenames!"
        assert "mat_bg_1" not in template_str, "Template should not contain material IDs!"

        # Template SHOULD contain style values
        assert "7.0" in template_str, "Template should contain font_size"
        assert "#FFFFFF" in template_str, "Template should contain font_color"
        assert "0.12" in template_str, "Template should contain logo scale"

        print("  No content URLs or text found in template")
        print("  Style values present")
        print("TEST 7 PASSED")
    finally:
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    test_analyze()
    test_auto_tag()
    test_manual_tag()
    test_suggest_role()
    test_export_template()
    test_text_style_extraction()
    test_no_content_in_template()

    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)
