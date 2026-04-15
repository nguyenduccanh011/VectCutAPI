"""
Script kiểm tra flow: video + image overlay + audio + text
"""
import shutil
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.example import (
    add_video_impl,
    add_image_impl,
    add_audio_track,
    add_text_impl,
    save_draft_impl,
    CAPCUT_DRAFT_FOLDER,
)

# ── Tài nguyên mẫu công khai ──────────────────────────────────────────────────
VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4"
IMAGE_URL = "https://www.w3schools.com/css/img_5terre.jpg"
AUDIO_URL = "https://www.w3schools.com/html/horse.mp3"

def move_to_capcut(draft_id):
    src = os.path.join(os.getcwd(), draft_id)
    dst = os.path.join(CAPCUT_DRAFT_FOLDER, draft_id)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"  → Đã chuyển draft sang CapCut: {dst}")
    else:
        print(f"  → Draft đã được lưu trực tiếp vào: {dst}")

def main():
    print("=" * 55)
    print(" TEST FLOW: video + image + audio + text")
    print("=" * 55)

    # 1. Thêm video nền (3 giây)
    print("\n[1/4] Thêm video nền...")
    r1 = add_video_impl(
        video_url=VIDEO_URL,
        start=0, end=3,
        target_start=0,
        width=1280, height=720,
    )
    assert r1.get("success"), f"Lỗi video: {r1}"
    draft_id = r1["output"]["draft_id"]
    print(f"  ✓ draft_id = {draft_id}")

    # 2. Thêm ảnh overlay (giây 0→3)
    print("\n[2/4] Thêm ảnh overlay...")
    r2 = add_image_impl(
        image_url=IMAGE_URL,
        start=0, end=3,
        draft_id=draft_id,
        track_name="image_overlay",
        scale_x=0.35, scale_y=0.35,
        transform_x=-0.6, transform_y=-0.7,
    )
    assert r2.get("success"), f"Lỗi image: {r2}"
    print(f"  ✓ Ảnh đã thêm vào draft {r2['output']['draft_id']}")

    # 3. Thêm audio (3 giây đầu)
    print("\n[3/4] Thêm audio...")
    r3 = add_audio_track(
        audio_url=AUDIO_URL,
        start=0, end=3,
        target_start=0,
        volume=0.8,
        draft_id=draft_id,
    )
    assert r3.get("success"), f"Lỗi audio: {r3}"
    print(f"  ✓ Audio đã thêm")

    # 4. Thêm text tiêu đề
    print("\n[4/4] Thêm text...")
    r4 = add_text_impl(
        text="Test VectCutAPI",
        start=0, end=3,
        font="Poppins_Bold",
        font_color="#FFFFFF",
        font_size=10.0,
        track_name="title_text",
        draft_id=draft_id,
        transform_y=0.75,
        shadow_enabled=True,
        shadow_color="#000000",
        shadow_alpha=0.8,
    )
    assert r4.get("success"), f"Lỗi text: {r4}"
    print(f"  ✓ Text đã thêm")

    # 5. Save draft
    print("\n[Lưu draft]")
    r5 = save_draft_impl(draft_id, CAPCUT_DRAFT_FOLDER)
    assert r5.get("success"), f"Lỗi save: {r5}"
    print(f"  ✓ Saved: {r5}")

    # 6. Chuyển draft sang CapCut nếu cần
    move_to_capcut(draft_id)

    print("\n" + "=" * 55)
    print(f" HOÀN THÀNH! Mở CapCut, tìm draft: {draft_id}")
    print("=" * 55)

if __name__ == "__main__":
    main()
