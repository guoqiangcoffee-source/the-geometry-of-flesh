#!/usr/bin/env python3
"""
合并 book/ 目录下所有 markdown 章节到 BOOK.md
使用: py scripts/build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
BOOK_DIR = ROOT / "book"
OUTPUT = ROOT / "BOOK.md"

TITLE = "肉身的几何"
SUBTITLE = "一名外科医生的物理学笔记"
EN_TITLE = "The Geometry of Flesh: A Surgeon's Notes on Physics"
AUTHOR = "Guoqiang"
YEAR = "2026"

VOLUMES = [
    ("卷一 · 形", "Form —— 静态的几何", range(1, 5)),
    ("卷二 · 流", "Flow —— 流动的几何", range(5, 9)),
    ("卷三 · 信", "Signal —— 信息的几何", range(9, 13)),
    ("卷四 · 度", "Scale —— 尺度的几何", range(13, 17)),
    ("卷五 · 限", "Limits —— 几何之外", range(17, 22)),
]


def find_chapter(chapters, num):
    prefix = f"{num:02d}-"
    for f in chapters:
        if f.stem.startswith(prefix):
            return f
    return None


def extract_title(filepath):
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()
    return filepath.stem


def read_chapter(filepath):
    return filepath.read_text(encoding="utf-8")


def main():
    files = sorted(BOOK_DIR.glob("*.md"))
    preface = [f for f in files if f.stem.startswith("00-")]
    chapters = [f for f in files if f.stem[:2].isdigit() and not f.stem.startswith("00-")]
    appendices = [f for f in files if f.stem.startswith("appendix-")]

    out = []
    out.append(f"# {TITLE}\n")
    out.append(f"## *{SUBTITLE}*\n")
    out.append(f"### *{EN_TITLE}*\n\n")
    out.append(f"<p align='right'><i>{AUTHOR} · {YEAR}</i></p>\n\n")
    out.append("---\n\n")

    out.append("## 目录 / *Contents*\n\n")
    if preface:
        out.append("- 序 / *Preface*\n")

    for vol_zh, vol_en, ch_range in VOLUMES:
        out.append(f"\n### {vol_zh} · *{vol_en}*\n")
        for ch_num in ch_range:
            ch_file = find_chapter(chapters, ch_num)
            if ch_file:
                ch_title = extract_title(ch_file)
                out.append(f"- {ch_title}\n")

    if appendices:
        out.append(f"\n### 附录 / *Appendix*\n")
        for app in appendices:
            app_title = extract_title(app)
            out.append(f"- {app_title}\n")

    out.append("\n---\n\n")

    for f in preface:
        out.append(read_chapter(f))
        out.append("\n---\n\n")

    for vol_zh, vol_en, ch_range in VOLUMES:
        out.append(f"\n# {vol_zh}\n## *{vol_en}*\n\n---\n\n")
        for ch_num in ch_range:
            ch_file = find_chapter(chapters, ch_num)
            if ch_file:
                out.append(read_chapter(ch_file))
                out.append("\n---\n\n")

    if appendices:
        out.append("\n# 附录 / *Appendix*\n\n---\n\n")
        for f in appendices:
            out.append(read_chapter(f))
            out.append("\n---\n\n")

    OUTPUT.write_text("".join(out), encoding="utf-8")
    print(f"[OK] 合并 {len(chapters)} 章 + {len(appendices)} 附录 -> {OUTPUT}")


if __name__ == "__main__":
    main()
