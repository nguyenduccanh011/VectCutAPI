"""
Script tạo slideshow: nhiều ảnh, mỗi ảnh 3s
Hiệu ứng chuyển động: zoom in, zoom out, pan trái→phải, pan phải→trái, pan trên→dưới
Transition giữa các ảnh: Dissolve
"""
import shutil
import os
from example import (
    add_image_impl,
    add_video_keyframe_impl,
    save_draft_impl,
    CAPCUT_DRAFT_FOLDER,
)

# ── Ảnh mẫu công khai ─────────────────────────────────────────────────────────
IMAGES = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&h=720&fit=crop",  # núi
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1280&h=720&fit=crop",  # rừng
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1280&h=720&fit=crop",  # biển
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1280&h=720&fit=crop",  # đêm
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1280&h=720&fit=crop",  # đồng cỏ
]

DURATION = 3.0          # mỗi ảnh kéo dài 3 giây
TRANSITION_DUR = 0.5    # transition 0.5s giữa các ảnh
W, H = 1280, 720

# Các pattern chuyển động bằng keyframe (scale_x, scale_y, position_x, position_y)
# Mỗi pattern: (tên, list[(property, time_offset_from_start, time_offset_from_end, val_start, val_end)])
MOTION_PATTERNS = [
    # 1. Zoom In: scale 1.0 → 1.25
    ("zoom_in",    [("scale_x", 0, DURATION, "1.0", "1.25"),
                    ("scale_y", 0, DURATION, "1.0", "1.25")]),
    # 2. Zoom Out: scale 1.25 → 1.0
    ("zoom_out",   [("scale_x", 0, DURATION, "1.25", "1.0"),
                    ("scale_y", 0, DURATION, "1.25", "1.0")]),
    # 3. Pan trái → phải (position_x -0.1 → 0.1, scale nhẹ để thấy pan)
    ("pan_left_right", [("scale_x", 0, DURATION, "1.15", "1.15"),
                        ("scale_y", 0, DURATION, "1.15", "1.15"),
                        ("position_x", 0, DURATION, "-0.08", "0.08")]),
    # 4. Pan phải → trái
    ("pan_right_left", [("scale_x", 0, DURATION, "1.15", "1.15"),
                        ("scale_y", 0, DURATION, "1.15", "1.15"),
                        ("position_x", 0, DURATION, "0.08", "-0.08")]),
    # 5. Pan trên → dưới
    ("pan_top_down",   [("scale_x", 0, DURATION, "1.15", "1.15"),
                        ("scale_y", 0, DURATION, "1.15", "1.15"),
                        ("position_y", 0, DURATION, "0.06", "-0.06")]),
]

def apply_motion(draft_id, track_name, pattern, clip_start):
    """Thêm keyframes chuyển động cho 1 ảnh"""
    _, props = pattern
    EPSILON = 0.01  # tránh trùng boundary với clip liền kề
    for prop, t0, t1, v0, v1 in props:
        # keyframe đầu: +epsilon tránh trùng điểm cuối clip trước
        add_video_keyframe_impl(
            draft_id=draft_id,
            track_name=track_name,
            property_type=prop,
            time=clip_start + t0 + EPSILON,
            value=v0,
        )
        # keyframe cuối: -epsilon tránh trùng điểm đầu clip sau
        add_video_keyframe_impl(
            draft_id=draft_id,
            track_name=track_name,
            property_type=prop,
            time=clip_start + t1 - EPSILON,
            value=v1,
        )

def move_to_capcut(draft_id):
    src = os.path.join(os.getcwd(), draft_id)
    dst = os.path.join(CAPCUT_DRAFT_FOLDER, draft_id)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"  → Chuyển sang CapCut: {dst}")
    else:
        print(f"  → Draft đã lưu tại: {dst}")

def main():
    print("=" * 60)
    print(" SLIDESHOW: ghép ảnh + zoom/pan keyframe + transition")
    print("=" * 60)

    draft_id = None
    total = len(IMAGES)
    TRACK_NAME = "video"  # Dùng main track để ảnh xếp tuần tự trên timeline chính

    for i, img_url in enumerate(IMAGES):
        clip_start = i * DURATION
        clip_end   = clip_start + DURATION
        pattern    = MOTION_PATTERNS[i % len(MOTION_PATTERNS)]

        print(f"\n[{i+1}/{total}] Ảnh {i+1} | {pattern[0]} | {clip_start:.1f}s → {clip_end:.1f}s")

        r = add_image_impl(
            image_url=img_url,
            start=clip_start,
            end=clip_end,
            width=W,
            height=H,
            track_name=TRACK_NAME,
            draft_id=draft_id,
            transition="Dissolve" if i > 0 else None,
            transition_duration=TRANSITION_DUR,
        )
        assert r.get("success"), f"Lỗi thêm ảnh {i+1}: {r.get('error')}"
        draft_id = r["output"]["draft_id"]
        print(f"  ✓ draft_id = {draft_id}")

        # Thêm keyframe chuyển động
        apply_motion(draft_id, TRACK_NAME, pattern, clip_start)
        print(f"  ✓ Keyframe '{pattern[0]}' đã áp dụng")

    # Save
    print("\n[Lưu draft...]")
    r_save = save_draft_impl(draft_id, CAPCUT_DRAFT_FOLDER)
    assert r_save.get("success"), f"Lỗi save: {r_save}"
    print(f"  ✓ Saved: {r_save}")

    move_to_capcut(draft_id)

    total_dur = len(IMAGES) * DURATION
    print("\n" + "=" * 60)
    print(f" HOÀN THÀNH! Thời lượng: {total_dur:.0f}s | {len(IMAGES)} ảnh")
    print(f" Mở CapCut, tìm draft: {draft_id}")
    print("=" * 60)

if __name__ == "__main__":
    main()
