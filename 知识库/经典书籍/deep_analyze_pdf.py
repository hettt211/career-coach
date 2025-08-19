#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析PDF结构，仔细查看目录和章节格式
"""

from pdfminer.high_level import extract_text
import re

def deep_analyze_pdf():
    # 输入文件
    input_file = "100+思维模型合集 (模型思维) (Z-Library).pdf"
    
    print("正在提取PDF文本...")
    content = extract_text(input_file)
    print(f"PDF文本提取成功，长度: {len(content)} 字符")
    
    # 查找目录部分
    print("\n=== 查找目录部分 ===")
    toc_match = re.search(r'目\s*录', content)
    if toc_match:
        toc_start = toc_match.start()
        print(f"目录开始位置: {toc_start}")
        
        # 获取目录后的更多内容进行分析
        after_toc = content[toc_start:toc_start+2000]
        print("目录内容（前2000字符）:")
        print("=" * 50)
        print(after_toc)
        print("=" * 50)
        
        # 查找目录中的章节行
        print("\n=== 分析目录中的章节行 ===")
        lines = after_toc.split('\n')
        chapter_lines = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            # 查找以数字开头的行
            if re.match(r'^\d{2}\s+', line_stripped):
                chapter_lines.append((i, line_stripped))
                print(f"行 {i}: {line_stripped}")
        
        print(f"\n找到 {len(chapter_lines)} 个可能的章节行")
        
        # 分析第一个章节的格式
        if chapter_lines:
            first_chapter = chapter_lines[0]
            print(f"\n第一个章节行: {first_chapter[1]}")
            
            # 尝试解析这个章节
            match = re.match(r'(\d{2})\s+(.+?)(?:\.{3,}|\s+\d+|\s*$)', first_chapter[1])
            if match:
                num = match.group(1)
                title = match.group(2).strip()
                print(f"解析结果: 编号={num}, 标题={title}")
            else:
                print("无法解析章节格式")
    
    # 查找正文中的章节标题
    print("\n=== 查找正文中的章节标题 ===")
    
    # 尝试不同的模式
    patterns = [
        r'(\d{2})\s+([^—\n\r\.]+)—([^\.\n\r]+)',  # 01 标题—副标题
        r'(\d{2})\s+([^—\n\r\.]+):([^\.\n\r]+)',  # 01 标题:副标题
        r'(\d{2})\s+([^—\n\r\.]+)',               # 01 标题
    ]
    
    for i, pattern in enumerate(patterns):
        matches = list(re.finditer(pattern, content))
        print(f"模式{i+1}: 找到 {len(matches)} 个匹配")
        
        # 显示前5个匹配
        for j, match in enumerate(matches[:5]):
            print(f"  {j+1}. {match.group(0)}")
        
        if matches:
            # 分析编号分布
            numbers = [int(m.group(1)) for m in matches]
            numbers.sort()
            print(f"  编号范围: {min(numbers)} - {max(numbers)}")
            print(f"  编号列表: {numbers[:10]}{'...' if len(numbers) > 10 else ''}")
    
    # 查找正文中第一个真正的章节
    print("\n=== 查找正文中第一个真正的章节 ===")
    
    # 假设真正的章节在目录之后，且格式更规范
    if toc_match:
        # 在目录后查找第一个看起来像章节的内容
        after_toc_content = content[toc_match.end():]
        
        # 查找第一个以数字开头的行
        lines = after_toc_content.split('\n')
        for i, line in enumerate(lines[:100]):  # 检查前100行
            line_stripped = line.strip()
            if re.match(r'^\d{2}\s+', line_stripped):
                print(f"目录后第{i+1}行可能是章节: {line_stripped}")
                break
        
        # 查找第一个包含"思维模型"的行
        thinking_model_match = re.search(r'\d{2}\s+思维模型', after_toc_content)
        if thinking_model_match:
            print(f"找到思维模型章节: {thinking_model_match.group(0)}")
            print(f"位置: {toc_match.end() + thinking_model_match.start()}")

if __name__ == "__main__":
    deep_analyze_pdf()
