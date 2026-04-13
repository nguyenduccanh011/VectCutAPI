#!/usr/bin/env python3
"""
Tạo slideshow đơn giản: 2 ảnh, mỗi ảnh 3 giây, transition Dissolve
"""
import shutil
import os
from example import (
    add_image_impl,
    save_draft_impl,
    CAPCUT_DRAFT_FOLDER,
)

# Ảnh từ Unsplash
IMAGES = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
]

DURATION = 3.0          # Mỗi ảnh 3 giây
TRANSITION_DUR = 0.5    # Transition 0.5 giây
W, H = 1080, 720       # Độ phân giải

def move_to_capcut(draft_id):
    """Chuyển draft sang thư mục CapCut"""
    src = os.path.join(os.getcwd(), draft_id)
    dst = os.path.join(CAPCUT_DRAFT_FOLDER, draft_id)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"  → Chuyển sang CapCut: {dst}")
    else:
        print(f"  → Draft đã lưu tại: {dst}")

def main():
    print("=" * 60)
    print(" SLIDESHOW: 2 ảnh + Dissolve transition")
    print("=" * 60)

    draft_id = None
    total = len(IMAGES)
    TRACK_NAME = "main"

    for i, img_url in enumerate(IMAGES):
        clip_start = i * DURATION
        clip_end = clip_start + DURATION

        print(f"\n[{i+1}/{total}] Ảnh {i+1}: {clip_start:.1f}s → {clip_end:.1f}s")

        # Transition Dissolve cho ảnh thứ 2 trở đi
        r = add_image_impl(
            image_url=img_url,
            start=clip_start,
            end=clip_end,
            width=W,
            height=H,
            track_name=TRACK_NAME,
            draft_id=draft_id,
            transition="Dissolve" if i > 0 else None,
            transition_duration=TRANSITION_DUR if i > 0 else None,
        )
        
        if not r.get("success"):
            print(f"  ✗ Lỗi: {r.get('error')}")
            return
            
        draft_id = r["output"]["draft_id"]
        print(f"  ✓ Thêm thành công | draft_id = {draft_id}")

    # Lưu draft
    print("\n[Lưu draft...]")
    r_save = save_draft_impl(draft_id, CAPCUT_DRAFT_FOLDER)
    if not r_save.get("success"):
        print(f"  ✗ Lỗi save: {r_save}")
        return
        
    print(f"  ✓ Lưu thành công")

    move_to_capcut(draft_id)

    total_dur = len(IMAGES) * DURATION
    print("\n" + "=" * 60)
    print(f" ✓ HOÀN THÀNH!")
    print(f" Thời lượng: {total_dur:.0f}s | {len(IMAGES)} ảnh")
    print(f" Draft ID: {draft_id}")
    print(f" Mở CapCut để xem kết quả")
    print("=" * 60)

if __name__ == "__main__":
    main()
