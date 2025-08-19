#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用图书章节分割脚本

功能：
- 输入 txt（优先）或 pdf（尝试自动提取文本）
- 自动识别并按章节/前言/附录等切分为 markdown 文件
- 输出目录可自定义，默认在输入文件同目录创建“书名_章节分割”

用法示例：
  python split_chapters.py -i "/path/to/book.txt"
  python split_chapters.py -i "/path/to/book.pdf" -o "/path/to/output_dir"

注意：
- pdf 需要本地安装 pdfminer.six 才能自动抽取文本；否则请先转换为 txt 再处理
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import List, Tuple


def try_read_text(file_path: str) -> str:
    """以常见编码尝试读取文本文件，返回内容字符串。"""
    encodings = ["utf-8", "utf-16", "utf-16le", "utf-16be", "gb18030", "gbk", "big5", "latin1"]
    last_err = None
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.read()
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue
    raise RuntimeError(f"无法读取文本文件（尝试的编码均失败）：{file_path}，最后错误：{last_err}")


def read_input_content(input_path: str) -> str:
    """读取输入内容。若为 txt 直接读；若为 pdf，尝试使用 pdfminer 提取文本。"""
    ext = os.path.splitext(input_path)[1].lower()
    if ext in {".txt", ".md"}:
        return try_read_text(input_path)

    if ext == ".pdf":
        try:
            # 延迟导入，避免无依赖时报错
            from pdfminer.high_level import extract_text  # type: ignore
        except Exception:
            raise RuntimeError(
                "解析 PDF 需要依赖 pdfminer.six。请先安装：pip install pdfminer.six，"
                "或先将 PDF 转为 txt 后再处理。"
            )
        text = extract_text(input_path)
        if not text or not text.strip():
            raise RuntimeError("PDF 文本抽取为空，请先手动转换为 txt 再处理。")
        return text

    raise RuntimeError(f"不支持的文件类型：{ext}，仅支持 .txt/.md/.pdf")


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def slugify_filename(name: str) -> str:
    """将标题转为安全文件名。"""
    name = re.sub(r"[\s\t\r\n]+", " ", name).strip()
    # 替换不适合文件名的字符
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    # 避免过长
    return name[:120] if len(name) > 120 else name


CHINESE_NUM_MAP = {
    "零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "百": 100, "千": 1000
}


def chinese_numeral_to_int(text: str) -> int | None:
    """尽量将中文数字（十/二十/一百零二等）解析为整数。失败返回 None。"""
    # 简单处理常见到百范围
    try:
        if text.isdigit():
            return int(text)
        total = 0
        unit = 0
        last = 0
        for ch in text:
            if ch in ("十", "百", "千"):
                factor = CHINESE_NUM_MAP[ch]
                if unit == 0:
                    unit = 1
                total += unit * factor
                unit = 0
            else:
                unit = CHINESE_NUM_MAP.get(ch, 0)
                last = unit
        total += unit
        # 处理“十、二十、三十”这种末尾不带个数的
        if total == 0 and last == 0 and any(c in text for c in ("十", "百", "千")):
            # “十” -> 10
            return sum(CHINESE_NUM_MAP.get(c, 0) for c in text if c in ("十", "百", "千"))
        return total or None
    except Exception:  # noqa: BLE001
        return None


def find_headings(content: str) -> List[Tuple[int, str, str]]:
    """
    识别所有章节/前后记/附录类标题。
    返回列表：[(start_index, kind, title_line), ...]
      kind in {chapter, preface, appendix}
    """
    headings: List[Tuple[int, str, str]] = []

    # 章节：第X章/节/回/讲/部分
    chapter_re = re.compile(r"^\s*(第([一二三四五六七八九十百零〇\d]+)[章节回讲部分节])\s*[：:．. ]?\s*(.*)$", re.M)
    # 前言/序
    preface_re = re.compile(r"^\s*(译序|前言|引言|序言|自序|序)\s*$", re.M)
    # 附录/后记等
    appendix_re = re.compile(r"^\s*(后记|编后记|附(?:录|：|:).*)\s*$", re.M)

    for m in chapter_re.finditer(content):
        full = m.group(1).strip()
        title_tail = (m.group(3) or "").strip()
        line = f"{full} {title_tail}".strip()
        headings.append((m.start(), "chapter", line))

    for m in preface_re.finditer(content):
        headings.append((m.start(), "preface", m.group(1).strip()))

    for m in appendix_re.finditer(content):
        headings.append((m.start(), "appendix", m.group(1).strip()))

    # 去重并排序
    headings = sorted(set(headings), key=lambda x: x[0])
    return headings


def write_section(out_dir: str, kind: str, title: str, body: str, chapter_idx_hint: int | None = None, book_name: str = "") -> None:
    """将一个分段写为 markdown 文件。"""
    os.makedirs(out_dir, exist_ok=True)

    header = f"# {title}\n\n"

    # 文件名策略：书名_章节_章节标题
    filename: str
    if kind == "chapter":
        # 提取中文/数字编号
        m = re.match(r"第([一二三四五六七八九十百零〇\d]+)([章节回讲部分节])\s*(.*)", title)
        if m:
            num_str = m.group(1)
            arabic = chinese_numeral_to_int(num_str)
            suffix = m.group(3).strip()
            if arabic is not None:
                if "章" in m.group(2):
                    base = f"{book_name}_第{arabic}章_{suffix or '未命名'}"
                else:
                    base = f"{book_name}_第{arabic}{m.group(2)}_{suffix or '未命名'}"
            else:
                base = f"{book_name}_{m.group(0)}"
        else:
            base = f"{book_name}_{title}"
        filename = slugify_filename(base) + ".md"
    elif kind == "preface":
        filename = slugify_filename(f"{book_name}_{title}") + ".md"  # 如：书名_译序.md / 书名_前言.md
    else:
        # appendix
        filename = slugify_filename(f"{book_name}_{title}") + ".md"  # 如：书名_后记.md / 书名_附录_*.md

    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + body.strip() + "\n")


def split_to_sections(content: str) -> List[Tuple[str, str, str]]:
    """
    根据标题切分内容。
    返回[(kind, title, body)]
    """
    headings = find_headings(content)
    if not headings:
        # 找不到标题，整体作为一个文件
        return [("chapter", "全文", content)]

    sections: List[Tuple[str, str, str]] = []
    positions = headings + [(len(content), "end", "END")]  # 末尾哨兵

    for idx in range(len(headings)):
        start_pos, kind, title = positions[idx]
        end_pos = positions[idx + 1][0]
        body = content[start_pos:end_pos]

        # 去掉标题行本身
        body_lines = body.splitlines()
        if body_lines:
            # 删除首行标题
            body_lines = body_lines[1:]
        body = "\n".join(line.rstrip() for line in body_lines)

        sections.append((kind, title, body))

    # 可能存在正文前的无标题内容，将其作为“前言_及其他.md”
    first_start = headings[0][0]
    pre_body = content[:first_start].strip()
    if pre_body:
        sections.insert(0, ("preface", "前言_及其他", pre_body))

    return sections


def derive_output_dir(input_path: str, out_dir: str | None) -> str:
    if out_dir:
        return out_dir
    base_dir = os.path.dirname(os.path.abspath(input_path))
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(base_dir, f"{base_name}_章节分割")


def main() -> None:
    parser = argparse.ArgumentParser(description="按章节切分 txt/pdf 并输出为 markdown 文件。")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径（txt/pdf）")
    parser.add_argument("-o", "--outdir", default=None, help="输出目录（默认：与输入同目录，书名_章节分割）")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_dir = derive_output_dir(input_path, args.outdir)
    ensure_dir(output_dir)

    # 提取书名（去掉扩展名和路径）
    book_name = os.path.splitext(os.path.basename(input_path))[0]

    try:
        content = read_input_content(input_path)
    except Exception as e:  # noqa: BLE001
        print(f"[错误] 读取输入失败：{e}")
        sys.exit(1)

    sections = split_to_sections(content)
    for idx, (kind, title, body) in enumerate(sections, start=1):
        write_section(output_dir, kind, title, body, chapter_idx_hint=idx, book_name=book_name)

    print(f"完成：共输出 {len(sections)} 个文件 -> {output_dir}")


if __name__ == "__main__":
    main()


