#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REVERSE ENGINEER TOOL - Đọc draft CapCut để tìm metadata hiệu ứng

CÁCH SỬ DỤNG:
1. Mở CapCut app
2. Tạo draft mới, thêm 1 video
3. Áp dụng hiệu ứng bạn muốn (VD: Cross Open transition)
4. Lưu draft (Ctrl+S hoặc thoát)
5. Chạy script này:  python reverse_engineer.py
6. Script sẽ đọc draft mới nhất và in ra metadata

OUTPUT MẪU:
  Name: Cross Open
  resource_id: 7xxxxxxxxxxxxxxxxx
  effect_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  md5: abc123def456...
  duration: 0.47s

Sau đó thêm vào: pyJianYingDraft/metadata/capcut_transition_meta.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


# ─── Đường dẫn CapCut storage ────────────────────────────────────────────────

CAPCUT_PATHS = [
    # Windows CapCut
    Path(os.environ.get("APPDATA", "")) / "CapCut" / "User Data" / "Projects",
    # Windows CapCut alternative
    Path(os.environ.get("LOCALAPPDATA", "")) / "CapCut" / "User Data" / "Projects",
    # Windows JianYing (剪映)
    Path(os.environ.get("APPDATA", "")) / "JianyingPro" / "User Data" / "Projects",
    Path(os.environ.get("LOCALAPPDATA", "")) / "JianyingPro" / "User Data" / "Projects",
    # Android CapCut (nếu được mount)
    Path("/sdcard/Movies/CapCut/Projects"),
    Path("/sdcard/DCIM/CapCut/Projects"),
]


def find_capcut_projects():
    """Tìm thư mục projects của CapCut"""
    found = []
    for path in CAPCUT_PATHS:
        if path.exists():
            found.append(path)
    return found


def find_latest_draft(project_dir: Path):
    """Tìm draft mới nhất trong thư mục projects"""
    draft_files = []

    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file == "draft_content.json":
                full_path = Path(root) / file
                mtime = full_path.stat().st_mtime
                draft_files.append((mtime, full_path))

    if not draft_files:
        return None

    draft_files.sort(reverse=True)
    return draft_files[0][1]


def extract_transitions(draft_json: dict) -> list:
    """Trích xuất transitions từ draft JSON"""
    results = []

    materials = draft_json.get("materials", {})
    transitions = materials.get("transitions", [])

    for t in transitions:
        entry = {
            "type": "transition",
            "name": t.get("name", ""),
            "resource_id": t.get("resource_id", ""),
            "effect_id": t.get("effect_id", t.get("id", "")),
            "md5": "",
            "duration": t.get("duration", 466666) / 1e6,
            "is_overlap": t.get("is_overlap", False),
            "raw": t
        }

        # md5 thường nằm trong extra_material_refs hoặc sub_type
        if "extra_material_refs" in t:
            entry["extra_refs"] = t["extra_material_refs"]

        results.append(entry)

    return results


def extract_animations(draft_json: dict) -> list:
    """Trích xuất video animations từ draft JSON"""
    results = []

    materials = draft_json.get("materials", {})
    animations = materials.get("video_effects", []) + materials.get("animations", [])

    for a in animations:
        entry = {
            "type": "animation",
            "name": a.get("name", ""),
            "resource_id": a.get("resource_id", ""),
            "effect_id": a.get("id", ""),
            "category": a.get("category_name", ""),
            "raw": a
        }
        results.append(entry)

    return results


def extract_effects(draft_json: dict) -> list:
    """Trích xuất video effects từ draft JSON"""
    results = []

    materials = draft_json.get("materials", {})
    effects = materials.get("video_effects", [])

    for e in effects:
        entry = {
            "type": "effect",
            "name": e.get("name", ""),
            "resource_id": e.get("resource_id", ""),
            "effect_id": e.get("id", ""),
            "params": e.get("params", {}),
            "raw": e
        }
        results.append(entry)

    return results


def extract_text_animations(draft_json: dict) -> list:
    """Trích xuất text animations từ draft JSON"""
    results = []

    materials = draft_json.get("materials", {})
    texts = materials.get("texts", [])

    for t in texts:
        # Text intro
        if "text_effect" in t:
            effect = t["text_effect"]
            entry = {
                "type": "text_animation",
                "name": effect.get("name", ""),
                "resource_id": effect.get("resource_id", ""),
                "effect_id": effect.get("effect_id", ""),
                "category": "intro" if "intro" in str(effect).lower() else "outro",
                "raw": effect
            }
            results.append(entry)

        # Animation animations
        for anim_key in ["animations"]:
            if anim_key in t:
                for anim in t[anim_key]:
                    entry = {
                        "type": "text_animation",
                        "name": anim.get("name", ""),
                        "resource_id": anim.get("resource_id", ""),
                        "effect_id": anim.get("id", ""),
                        "raw": anim
                    }
                    results.append(entry)

    return results


def extract_stickers(draft_json: dict) -> list:
    """Trích xuất stickers từ draft JSON"""
    results = []

    materials = draft_json.get("materials", {})
    stickers = materials.get("stickers", [])

    for s in stickers:
        entry = {
            "type": "sticker",
            "name": s.get("name", ""),
            "sticker_id": s.get("sticker_id", ""),
            "resource_id": s.get("resource_id", ""),
            "raw": s
        }
        results.append(entry)

    return results


def scan_all_effects(draft_json: dict) -> dict:
    """Quét tất cả hiệu ứng trong draft - cách tổng quát"""

    found = {
        "transitions": [],
        "animations": [],
        "effects": [],
        "stickers": [],
        "text_animations": [],
        "unknown": []
    }

    def recurse(obj, path=""):
        if isinstance(obj, dict):
            name = obj.get("name", "")
            rid = obj.get("resource_id", "")
            eid = obj.get("effect_id", obj.get("id", ""))
            md5 = obj.get("md5", "")

            # Transition
            if "is_overlap" in obj and rid:
                found["transitions"].append({
                    "path": path,
                    "name": name,
                    "resource_id": rid,
                    "effect_id": eid,
                    "md5": md5,
                    "duration": obj.get("duration", 0) / 1e6,
                    "is_overlap": obj.get("is_overlap", False)
                })

            for key, val in obj.items():
                recurse(val, f"{path}.{key}")

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                recurse(item, f"{path}[{i}]")

    recurse(draft_json)
    return found


def generate_python_code(results: dict) -> str:
    """Tạo code Python để thêm vào metadata files"""

    lines = []

    if results["transitions"]:
        lines.append("# ─── THÊM VÀO: pyJianYingDraft/metadata/capcut_transition_meta.py ─────")
        lines.append("")
        seen = set()
        for t in results["transitions"]:
            name = t["name"]
            if not name or name in seen:
                continue
            seen.add(name)

            enum_name = name.replace(" ", "_").replace("-", "_").replace("&", "And")
            lines.append(f'    {enum_name:<20} = Transition_meta("{name}", False, "{t["resource_id"]}", "{t["effect_id"]}", "{t["md5"]}", {t["duration"]:.6f}, {t["is_overlap"]})')
            lines.append(f'    """Tên: {name} | Duration: {t["duration"]:.2f}s"""')
        lines.append("")

    return "\n".join(lines)


def analyze_draft_file(draft_path: Path):
    """Phân tích file draft và in kết quả"""

    print(f"\n📂 Đang đọc: {draft_path}")
    print(f"   Thời gian sửa đổi: {datetime.fromtimestamp(draft_path.stat().st_mtime)}\n")

    with open(draft_path, encoding="utf-8") as f:
        draft_json = json.load(f)

    # Quét tất cả hiệu ứng
    print("🔍 Quét toàn bộ data...")
    all_found = scan_all_effects(draft_json)

    # In kết quả transitions
    if all_found["transitions"]:
        print(f"\n{'='*60}")
        print(f"🔄 TRANSITIONS TÌM THẤY: {len(all_found['transitions'])}")
        print(f"{'='*60}")
        for t in all_found["transitions"]:
            name = t['name'] or "(không tên)"
            print(f"\n  📌 {name}")
            print(f"     resource_id : {t['resource_id']}")
            print(f"     effect_id   : {t['effect_id']}")
            print(f"     md5         : {t['md5'] or '(trống)'}")
            print(f"     duration    : {t['duration']:.3f}s")
            print(f"     is_overlap  : {t['is_overlap']}")
    else:
        print("  ℹ️  Không tìm thấy transitions trong draft này")
        print("  💡 Thử áp dụng một transition trong CapCut rồi lưu lại")

    # Lưu kết quả vào JSON
    output_file = Path("discovered_effects.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_found, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n✅ Đã lưu toàn bộ data vào: {output_file}")

    # Tạo code Python
    code = generate_python_code(all_found)
    if code.strip():
        code_file = Path("new_effects_code.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write("# Code tự động tạo - thêm vào metadata files\n\n")
            f.write(code)
        print(f"🐍 Code Python được tạo tại: {code_file}")

    return all_found


def manual_mode():
    """Chế độ thủ công - nhập đường dẫn file draft"""
    print("\n📖 CHẾ ĐỘ THỦ CÔNG")
    print("Nhập đường dẫn tới file draft_content.json:")
    path = input("  > ").strip().strip('"')

    if os.path.exists(path):
        analyze_draft_file(Path(path))
    else:
        print(f"❌ File không tồn tại: {path}")


def main():
    print("=" * 60)
    print("🔬 VECTCUTAPI - REVERSE ENGINEER TOOL")
    print("=" * 60)

    # Tìm CapCut projects
    project_dirs = find_capcut_projects()

    if not project_dirs:
        print("\n⚠️  Không tìm thấy thư mục CapCut tự động")
        print("\nCác đường dẫn đã kiểm tra:")
        for p in CAPCUT_PATHS:
            print(f"  - {p}")

        print("\n💡 HƯỚNG DẪN THỦ CÔNG:")
        print("   1. Mở CapCut → tạo draft → thêm hiệu ứng → lưu")
        print("   2. Tìm file draft_content.json:")
        print("      Windows: %APPDATA%\\CapCut\\User Data\\Projects\\")
        print("      hoặc:    %LOCALAPPDATA%\\CapCut\\User Data\\Projects\\")
        print("   3. Chạy lại với: python reverse_engineer.py <đường_dẫn>")

        if len(sys.argv) > 1:
            analyze_draft_file(Path(sys.argv[1]))
        else:
            manual_mode()
        return

    # Tự động tìm draft mới nhất
    print(f"\n✅ Tìm thấy CapCut tại: {project_dirs[0]}")

    latest = find_latest_draft(project_dirs[0])
    if not latest:
        print("❌ Không tìm thấy file draft nào")
        return

    print(f"📄 Draft mới nhất: {latest}")
    analyze_draft_file(latest)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_draft_file(Path(sys.argv[1]))
    else:
        main()
