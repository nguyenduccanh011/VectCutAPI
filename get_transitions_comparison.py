#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VectCutAPI - Lấy danh sách hiệu ứng chuyển tiếp (Transitions)
"""

import requests
import json
from typing import List, Dict

BASE_URL = "http://localhost:9001"

def get_transitions() -> List[str]:
    """Lấy danh sách tất cả hiệu ứng chuyển tiếp"""
    try:
        response = requests.get(f"{BASE_URL}/get_transition_types", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("output", [])
            else:
                print(f"❌ Lỗi API: {data.get('error')}")
                return []
        else:
            print(f"❌ Lỗi kết nối: HTTP {response.status_code}")
            return []
    
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối tới server!")
        print(f"   Đảm bảo VectCutAPI server đang chạy tại {BASE_URL}")
        return []
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return []


def get_all_effects() -> Dict[str, List[str]]:
    """Lấy tất cả loại hiệu ứng"""
    
    endpoints = {
        "🔄 Hiệu Ứng Chuyển Tiếp (Transitions)": "/get_transition_types",
        "📹 Hoạt Ảnh Vào Video (Intro)": "/get_intro_animation_types",
        "📹 Hoạt Ảnh Ra Video (Outro)": "/get_outro_animation_types",
        "✨ Hoạt Ảnh Kết Hợp (Combo)": "/get_combo_animation_types",
        "📝 Hoạt Ảnh Vào Văn Bản": "/get_text_intro_types",
        "📝 Hoạt Ảnh Ra Văn Bản": "/get_text_outro_types",
        "📝 Hoạt Ảnh Lặp Văn Bản": "/get_text_loop_anim_types",
        "🎭 Kiểu Mặt Nạ (Masks)": "/get_mask_types",
        "🔊 Hiệu Ứng Âm Thanh": "/get_audio_effect_types",
        "🎬 Hiệu Ứng Cảnh": "/get_video_scene_effect_types",
        "👤 Hiệu Ứng Ký Tự": "/get_video_character_effect_types",
        "🔤 Phông Chữ": "/get_font_types"
    }
    
    results = {}
    
    for category, endpoint in endpoints.items():
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    results[category] = data.get("output", [])
        except:
            results[category] = []
    
    return results


def display_transitions_comparison():
    """Hiển thị danh sách chuyển tiếp với so sánh"""
    
    print("=" * 70)
    print("🎬 VECTCUTAPI - DANH SÁCH HIỆU ỨNG CHUYỂN TIẾP (TRANSITIONS)")
    print("=" * 70)
    
    transitions = get_transitions()
    
    if not transitions:
        print("❌ Không thể lấy danh sách hiệu ứng")
        return
    
    print(f"\n✅ Tổng cộng: {len(transitions)} hiệu ứng chuyển tiếp\n")
    
    # Phân loại theo kiểu
    categories = {
        "Mờ": [t for t in transitions if "fade" in t.lower() or "blur" in t.lower()],
        "Quét": [t for t in transitions if "wipe" in t.lower() or "slash" in t.lower()],
        "Thu Phóng": [t for t in transitions if "zoom" in t.lower() or "scale" in t.lower()],
        "Xoay": [t for t in transitions if "rotate" in t.lower()],
        "Khác": [t for t in transitions if not any(
            x in t.lower() for x in ["fade", "blur", "wipe", "slash", "zoom", "scale", "rotate"]
        )]
    }
    
    # Hiển thị từng danh mục
    for category, items in categories.items():
        if items:
            print(f"\n📊 {category} ({len(items)} loại):")
            print("-" * 70)
            for i, item in enumerate(items, 1):
                print(f"  {i:2d}. {item}")
    
    # Hiển thị bảng so sánh
    print("\n" + "=" * 70)
    print("📋 BẢNG SO SÁNH CỤ THỂ")
    print("=" * 70)
    
    comparison_data = {
        "fade_in": "Mờ dần vào từ từ",
        "fade_out": "Mờ dần ra từ từ",
        "wipe_left": "Quét từ phải sang trái",
        "wipe_right": "Quét từ trái sang phải",
        "wipe_up": "Quét từ dưới lên",
        "wipe_down": "Quét từ trên xuống",
        "zoom_in": "Phóng to vào",
        "zoom_out": "Thu nhỏ ra",
        "scale": "Tỷ lệ thu phóng",
        "rotate": "Xoay",
        "blur": "Mờ nhòe",
        "pixelate": "Pixelate (khối vuông)",
        "slash_left": "Gạch chéo trái",
        "slash_right": "Gạch chéo phải",
        "plus": "Tia sáng (+)"
    }
    
    print("\n🎯 Các hiệu ứng phổ biến:\n")
    print(f"{'Tên Hiệu Ứng':<20} | {'Mô Tả':<45} | {'Có Sẵn':<10}")
    print("-" * 80)
    
    for name, description in comparison_data.items():
        available = "✅ Có" if name in transitions else "❌ Không"
        print(f"{name:<20} | {description:<45} | {available:<10}")


def display_all_effects_table():
    """Hiển thị bảng tất cả loại hiệu ứng"""
    
    print("\n" + "=" * 70)
    print("📊 BẢNG TỔNG QUAN TẤT CẢ HIỆU ỨNG")
    print("=" * 70)
    
    all_effects = get_all_effects()
    
    print(f"\n{'Loại Hiệu Ứng':<45} | {'Số Lượng':<10} | {'Status':<10}")
    print("-" * 70)
    
    for category, effects in all_effects.items():
        count = len(effects)
        status = "✅" if count > 0 else "❌"
        print(f"{category:<45} | {count:<10} | {status:<10}")


def save_transitions_to_json():
    """Lưu danh sách transitions vào file JSON"""
    
    transitions = get_transitions()
    all_effects = get_all_effects()
    
    data = {
        "timestamp": "2026-04-14",
        "server": BASE_URL,
        "transitions": {
            "count": len(transitions),
            "list": transitions
        },
        "all_effects": {
            category: {"count": len(items), "list": items}
            for category, items in all_effects.items()
        }
    }
    
    filename = "vectcut_effects_list.json"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Đã lưu vào: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Lỗi lưu file: {str(e)}")
        return None


def main():
    """Chương trình chính"""
    
    print("\n🚀 Đang kết nối VectCutAPI...\n")
    
    # Hiển thị danh sách chuyển tiếp
    display_transitions_comparison()
    
    # Hiển thị bảng tất cả hiệu ứng
    display_all_effects_table()
    
    # Lưu vào JSON
    json_file = save_transitions_to_json()
    
    print("\n" + "=" * 70)
    print("✅ Hoàn tất!")
    print("=" * 70)


if __name__ == "__main__":
    main()
