#!/usr/bin/env python3
"""Fail if CJK characters are found in English-only files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# Focus on English-first core paths only.
TARGET_FILES = [
    "README.md",
    "mcp_server.py",
    "capcut_server.py",
    "add_audio_track.py",
    "downloader.py",
    "add_text_impl.py",
    "examples/example_capcut_effect.py",
    "pattern/001-words.py",
    "vectcut-skill/skill/scripts/vectcut_client.py",
    "locales/en.json",
    "locales/vi.json",
]

ALLOWED_CJK_SNIPPETS = [
    "MCP_文档_中文.md",
    "思源黑体",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checked = 0
    findings: list[str] = []

    for relative_path in TARGET_FILES:
        file_path = root / relative_path
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(root)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        checked += 1
        for index, line in enumerate(content.splitlines(), start=1):
            if any(snippet in line for snippet in ALLOWED_CJK_SNIPPETS):
                continue
            if CJK_RE.search(line):
                findings.append(f"{rel.as_posix()}:{index}: {line.strip()}")

    if findings:
        print("Found CJK text in English-only files:")
        for item in findings[:200]:
            print(item)
        if len(findings) > 200:
            print(f"... and {len(findings) - 200} more")
        return 1

    print(f"OK: checked {checked} files, no CJK text found in English-only scope.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
