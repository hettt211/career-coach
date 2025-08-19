#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析PDF文本结构，找到真正的章节模式
"""

from pdfminer.high_level import extract_text
import re

def analyze_pdf():
    # 输入文件
    input_file = "100+思维模型合集 (模型思维) (Z-Library).pdf"
    
    print("正在提取PDF文本...")
    content = extract_text(input_file)
    print(f"PDF文本提取成功，长度: {len(content)} 字符")
    
    # 查找所有可能的章节标题模式
    print("\n=== 查找章节标题模式 ===")
    
    # 模式1: "01 模型思维——牛人顶级思维法"
    pattern1 = r'(\d{2})\s+([^—\n]+)—([^\n]+)'
    matches1 = list(re.finditer(pattern1, content))
    print(f"模式1 (数字+标题—副标题): 找到 {len(matches1)} 个匹配")
    
    # 显示前10个匹配
    for i, match in enumerate(matches1[:10]):
        print(f"  {i+1}. {match.group(0)}")
    
    # 模式2: "第X章" 格式
    pattern2 = r'第(\d+)章\s*([^\n]+)'
    matches2 = list(re.finditer(pattern2, content))
    print(f"\n模式2 (第X章): 找到 {len(matches2)} 个匹配")
    
    # 显示前10个匹配
    for i, match in enumerate(matches2[:10]):
        print(f"  {i+1}. {match.group(0)}")
    
    # 模式3: 查找目录部分
    print("\n=== 查找目录部分 ===")
    toc_match = re.search(r'目\s*录', content)
    if toc_match:
        toc_start = toc_match.start()
        # 获取目录后的1000个字符
        toc_content = content[toc_start:toc_start+1000]
        print("目录内容:")
        print(toc_content)
    
    # 分析章节编号的分布
    print("\n=== 分析章节编号分布 ===")
    chapter_numbers = []
    for match in matches1:
        num = int(match.group(1))
        chapter_numbers.append(num)
    
    chapter_numbers.sort()
    print(f"章节编号: {chapter_numbers}")
    
    # 检查是否有连续的编号
    continuous_chapters = []
    for i in range(len(chapter_numbers)-1):
        if chapter_numbers[i+1] - chapter_numbers[i] == 1:
            continuous_chapters.append((chapter_numbers[i], chapter_numbers[i+1]))
    
    print(f"连续章节: {continuous_chapters}")
    
    # 查找真正的章节开始位置
    print("\n=== 查找真正的章节开始位置 ===")
    # 假设真正的章节在目录之后，且编号连续
    if toc_match:
        after_toc = content[toc_match.end():]
        # 在目录后查找第一个章节
        first_chapter = re.search(pattern1, after_toc)
        if first_chapter:
            print(f"目录后第一个章节: {first_chapter.group(0)}")
            print(f"位置: {toc_match.end() + first_chapter.start()}")

if __name__ == "__main__":
    analyze_pdf()
