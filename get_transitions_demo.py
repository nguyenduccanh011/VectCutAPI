#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VectCutAPI - Danh Sách Hiệu Ứng Chuyển Tiếp (Demo)

Khi server không chạy, script này sẽ hiển thị danh sách hiệu ứng tư dữ liệu mẫu.
"""

import json

# Dữ liệu mẫu các hiệu ứng chuyển tiếp
TRANSITIONS_DEMO = [
    "fade_in",
    "fade_out",
    "wipe_left",
    "wipe_right",
    "wipe_up",
    "wipe_down",
    "slash_left",
    "slash_right",
    "scale",
    "zoom_in",
    "zoom_out",
    "blur",
    "pixelate",
    "plus",
    "rotate",
    "circle_open",
    "circle_close",
    "diamond",
    "wedge",
    "push_left",
    "push_right",
    "push_up",
    "push_down",
    "morph"
]

TEXT_INTROS_DEMO = [
    "fade_in",
    "zoom_in",
    "slide_in_left",
    "slide_in_right",
    "slide_in_top",
    "slide_in_bottom",
    "bounce_in",
    "flip_in",
    "rotate_in",
    "typewriter",
    "scale_up",
    "spin_in"
]

TEXT_OUTROS_DEMO = [
    "fade_out",
    "zoom_out",
    "slide_out_left",
    "slide_out_right",
    "slide_out_top",
    "slide_out_bottom",
    "bounce_out",
    "flip_out",
    "rotate_out",
    "scale_down",
    "spin_out"
]

VIDEO_INTROS_DEMO = [
    "fade_in",
    "scale_up",
    "bounce_in",
    "flip_in",
    "rotate_in",
    "slide_in_left",
    "slide_in_right",
    "slide_in_top",
    "slide_in_bottom",
    "zoom_in"
]

VIDEO_OUTROS_DEMO = [
    "fade_out",
    "scale_down",
    "bounce_out",
    "flip_out",
    "rotate_out",
    "slide_out_left",
    "slide_out_right",
    "slide_out_top",
    "slide_out_bottom",
    "zoom_out"
]

MASKS_DEMO = [
    "circle",
    "rect",
    "linear",
    "radial",
    "heart",
    "star",
    "diamond",
    "rounded_rect",
    "triangle",
    "hexagon"
]

TEXT_LOOPS_DEMO = [
    "blink",
    "swing",
    "bounce",
    "pulse",
    "glow",
    "shake",
    "wave",
    "rotate",
    "scale",
    "skew"
]

def display_transitions_comparison():
    """Hiển thị danh sách chuyển tiếp với so sánh"""
    
    print("=" * 70)
    print("🎬 VECTCUTAPI - DANH SÁCH HIỆU ỨNG CHUYỂN TIẾP (TRANSITIONS)")
    print("=" * 70)
    
    transitions = TRANSITIONS_DEMO
    
    print(f"\n✅ Tổng cộng: {len(transitions)} hiệu ứng chuyển tiếp\n")
    
    # Phân loại theo kiểu
    categories = {
        "Mờ": [t for t in transitions if "fade" in t.lower() or "blur" in t.lower()],
        "Quét": [t for t in transitions if "wipe" in t.lower() or "slash" in t.lower() or "push" in t.lower()],
        "Thu Phóng": [t for t in transitions if "zoom" in t.lower() or "scale" in t.lower()],
        "Hình Tròn": [t for t in transitions if "circle" in t.lower() or "diamond" in t.lower() or "plus" in t.lower()],
        "Xoay": [t for t in transitions if "rotate" in t.lower() or "spin" in t.lower()],
        "Khác": [t for t in transitions if not any(
            x in t.lower() for x in ["fade", "blur", "wipe", "slash", "push", "zoom", "scale", "circle", "diamond", "plus", "rotate", "spin"]
        )]
    }
    
    # Hiển thị từng danh mục
    for category, items in categories.items():
        if items:
            print(f"\n📊 {category} ({len(items)} loại):")
            print("-" * 70)
            for i, item in enumerate(items, 1):
                print(f"  {i:2d}. {item:<25}")
    
    # Hiển thị bảng so sánh chi tiết
    print("\n" + "=" * 70)
    print("📋 BẢNG SO SÁNH CHI TIẾT - TRANSITIONS")
    print("=" * 70)
    
    comparison_data = {
        "fade_in": {
            "description": "Mờ dần vào từ từ",
            "use_case": "Bắt đầu video nhẹ nhàng",
            "duration": "0.5-1.0s"
        },
        "fade_out": {
            "description": "Mờ dần ra từ từ",
            "use_case": "Kết thúc video nhẹ nhàng",
            "duration": "0.5-1.0s"
        },
        "wipe_left": {
            "description": "Quét từ phải sang trái",
            "use_case": "Chuyển clip nhanh chóng",
            "duration": "0.3-0.5s"
        },
        "wipe_right": {
            "description": "Quét từ trái sang phải",
            "use_case": "Chuyển clip nhanh chóng",
            "duration": "0.3-0.5s"
        },
        "wipe_up": {
            "description": "Quét từ dưới lên",
            "use_case": "Chuyển clip nhanh chóng",
            "duration": "0.3-0.5s"
        },
        "wipe_down": {
            "description": "Quét từ trên xuống",
            "use_case": "Chuyển clip nhanh chóng",
            "duration": "0.3-0.5s"
        },
        "zoom_in": {
            "description": "Phóng to vào",
            "use_case": "Focus vào chi tiết, tăng hưng phấn",
            "duration": "0.4-0.8s"
        },
        "zoom_out": {
            "description": "Thu nhỏ ra",
            "use_case": "Rút lui, tạo khoảng cách",
            "duration": "0.4-0.8s"
        },
        "blur": {
            "description": "Mờ nhòe",
            "use_case": "Hiệu ứng mất tiêu điểm",
            "duration": "0.3-0.6s"
        },
        "pixelate": {
            "description": "Pixelate (khối vuông)",
            "use_case": "Hiệu ứng cố định, che lấp",
            "duration": "0.3-0.6s"
        },
        "rotate": {
            "description": "Xoay",
            "use_case": "Transition năng động, thu hút",
            "duration": "0.5-0.8s"
        },
        "circle_open": {
            "description": "Hình tròn mở",
            "use_case": "Reveal hiệu ứng từ tâm",
            "duration": "0.4-0.7s"
        },
        "circle_close": {
            "description": "Hình tròn đóng",
            "use_case": "Hide hiệu ứng tới tâm",
            "duration": "0.4-0.7s"
        }
    }
    
    print(f"\n{'Tên Hiệu Ứng':<18} | {'Mô Tả':<28} | {'Trường Hợp Sử Dụng':<25} | {'Thời Gian':<12}")
    print("-" * 100)
    
    for name, info in comparison_data.items():
        print(f"{name:<18} | {info['description']:<28} | {info['use_case']:<25} | {info['duration']:<12}")


def display_text_animations():
    """Hiển thị hoạt ảnh văn bản"""
    
    print("\n" + "=" * 70)
    print("📝 HOẠT ẢNH VĂN BẢN (TEXT ANIMATIONS)")
    print("=" * 70)
    
    print(f"\n🔹 Hoạt ảnh VÀO (Intro) - {len(TEXT_INTROS_DEMO)} loại:")
    print("-" * 70)
    for i, anim in enumerate(TEXT_INTROS_DEMO, 1):
        print(f"  {i:2d}. {anim:<30}", end="")
        if i % 2 == 0:
            print()
    if len(TEXT_INTROS_DEMO) % 2 != 0:
        print()
    
    print(f"\n🔹 Hoạt ảnh RA (Outro) - {len(TEXT_OUTROS_DEMO)} loại:")
    print("-" * 70)
    for i, anim in enumerate(TEXT_OUTROS_DEMO, 1):
        print(f"  {i:2d}. {anim:<30}", end="")
        if i % 2 == 0:
            print()
    if len(TEXT_OUTROS_DEMO) % 2 != 0:
        print()


def display_masks():
    """Hiển thị mặt nạ"""
    
    print("\n" + "=" * 70)
    print("🎭 KIỂU MẶT NẠ (MASK TYPES)")
    print("=" * 70)
    
    print(f"\n✅ Tổng cộng: {len(MASKS_DEMO)} loại mặt nạ\n")
    
    for i, mask in enumerate(MASKS_DEMO, 1):
        print(f"  {i:2d}. {mask:<20}", end="")
        if i % 3 == 0:
            print()
    if len(MASKS_DEMO) % 3 != 0:
        print()


def display_text_loops():
    """Hiển thị hoạt ảnh lặp văn bản"""
    
    print("\n" + "=" * 70)
    print("🔁 HOẠT ẢNH LẶP VĂN BẢN (TEXT LOOP ANIMATIONS)")
    print("=" * 70)
    
    print(f"\n✅ Tổng cộng: {len(TEXT_LOOPS_DEMO)} loại hoạt ảnh lặp\n")
    
    loop_descriptions = {
        "blink": "Nhấp nháy",
        "swing": "Swing (đung đưa)",
        "bounce": "Nảy",
        "pulse": "Xung động (size thay đổi)",
        "glow": "Phát sáng",
        "shake": "Rung lắc",
        "wave": "Sóng",
        "rotate": "Xoay",
        "scale": "Phóng to/thu nhỏ",
        "skew": "Nghiêng"
    }
    
    for i, loop in enumerate(TEXT_LOOPS_DEMO, 1):
        description = loop_descriptions.get(loop, "")
        print(f"  {i:2d}. {loop:<20} - {description}")


def display_summary():
    """Hiển thị bảng tóm tắt tất cả loại hiệu ứng"""
    
    print("\n" + "=" * 70)
    print("📊 BẢNG TÓMS VĂT TẤT CẢ LOẠI HIỆU ỨNG")
    print("=" * 70)
    
    all_effects = {
        "🔄 Hiệu Ứng Chuyển Tiếp (Transitions)": len(TRANSITIONS_DEMO),
        "📝 Hoạt Ảnh Vào Văn Bản": len(TEXT_INTROS_DEMO),
        "📝 Hoạt Ảnh Ra Văn Bản": len(TEXT_OUTROS_DEMO),
        "📹 Hoạt Ảnh Vào Video": len(VIDEO_INTROS_DEMO),
        "📹 Hoạt Ảnh Ra Video": len(VIDEO_OUTROS_DEMO),
        "🎭 Kiểu Mặt Nạ": len(MASKS_DEMO),
        "🔁 Hoạt Ảnh Lặp Văn Bản": len(TEXT_LOOPS_DEMO)
    }
    
    total = sum(all_effects.values())
    
    print(f"\n{'Loại Hiệu Ứng':<45} | {'Số Lượng':<10}")
    print("-" * 60)
    
    for category, count in all_effects.items():
        print(f"{category:<45} | {count:<10}")
    
    print("-" * 60)
    print(f"{'TỔNG CỘNG':<45} | {total:<10}")


def export_to_json():
    """Xuất danh sách vào file JSON"""
    
    data = {
        "transitions": TRANSITIONS_DEMO,
        "text_intros": TEXT_INTROS_DEMO,
        "text_outros": TEXT_OUTROS_DEMO,
        "video_intros": VIDEO_INTROS_DEMO,
        "video_outros": VIDEO_OUTROS_DEMO,
        "masks": MASKS_DEMO,
        "text_loops": TEXT_LOOPS_DEMO
    }
    
    filename = "vectcut_transitions.json"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Đã xuất ra file: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Lỗi xuất file: {str(e)}")
        return None


def main():
    """Chương trình chính"""
    
    print("\n🎬 VECTCUTAPI - DANH SÁCH HIỆU ỨNG & CHO VD THẾ")
    print("=" * 70)
    print("\n💡 Lưu ý: Đây là dữ liệu mẫu. Để lấy danh sách thực tế,")
    print("   hãy khởi động VectCutAPI server tại http://localhost:9001\n")
    
    # Hiển thị các danh sách
    display_transitions_comparison()
    display_text_animations()
    display_masks()
    display_text_loops()
    display_summary()
    
    # Xuất JSON
    json_file = export_to_json()
    
    print("\n" + "=" * 70)
    print("✅ Hoàn tất!")
    print("=" * 70)
    
    # Hướng dẫn sử dụng
    print("\n📖 HƯỚNG DẪN SỬ DỤNG TRONG CODE:")
    print("-" * 70)
    print("""
# 1. Sử dụng transition khi thêm video
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "transition": "fade_in",           # ⬅️ Chọn từ danh sách trên
    "transition_duration": 0.8
})

# 2. Sử dụng hoạt ảnh văn bản
requests.post(f"{BASE_URL}/add_text", json={
    "draft_id": draft_id,
    "text": "Văn bản có hoạt ảnh",
    "text_intro": "zoom_in",           # ⬅️ Hoạt ảnh vào
    "text_outro": "fade_out"           # ⬅️ Hoạt ảnh ra
})

# 3. Sử dụng mặt nạ
requests.post(f"{BASE_URL}/add_video", json={
    "draft_id": draft_id,
    "video_url": "https://example.com/video.mp4",
    "mask_type": "circle",             # ⬅️ Chọn từ danh sách trên
    "mask_feather": 0.2
})
    """)


if __name__ == "__main__":
    main()
