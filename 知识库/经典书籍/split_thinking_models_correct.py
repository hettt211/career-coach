#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
思维模型合集章节分割脚本 - 正确版
基于深度分析结果，正确识别和处理章节
"""

import os
import re

def split_thinking_models():
    # 输入文件
    input_file = "100+思维模型合集 (模型思维) (Z-Library).pdf"
    
    # 输出目录
    output_dir = "100+思维模型合集_章节分割"
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # 提取PDF文本
    try:
        from pdfminer.high_level import extract_text
        print("正在提取PDF文本...")
        content = extract_text(input_file)
        print(f"PDF文本提取成功，长度: {len(content)} 字符")
    except Exception as e:
        print(f"PDF文本提取失败: {e}")
        return
    
    # 查找目录部分
    toc_match = re.search(r'目\s*录', content)
    if not toc_match:
        print("未找到目录，无法确定章节结构")
        return
    
    print(f"找到目录，位置: {toc_match.start()}")
    
    # 从目录中提取章节信息
    toc_content = content[toc_match.start():toc_match.start()+3000]  # 获取目录内容
    lines = toc_content.split('\n')
    
    # 解析目录中的章节
    chapters = []
    for line in lines:
        line_stripped = line.strip()
        # 匹配格式: "01 模型思维——牛人顶级思维法................................................................6"
        match = re.match(r'(\d{2})\s+(.+?)(?:\.{3,}|\s+\d+|\s*$)', line_stripped)
        if match:
            chapter_num = int(match.group(1))
            chapter_title = match.group(2).strip()
            chapters.append((chapter_num, chapter_title))
    
    # 按章节号排序
    chapters.sort(key=lambda x: x[0])
    
    print(f"从目录中识别到 {len(chapters)} 个章节")
    
    # 显示前10个章节
    for i, (num, title) in enumerate(chapters[:10]):
        print(f"  {i+1}. {num:02d} {title}")
    
    if len(chapters) > 10:
        print(f"  ... 还有 {len(chapters) - 10} 个章节")
    
    # 查找正文中对应的章节位置
    print("\n正在查找正文中的章节位置...")
    
    # 在正文中查找每个章节
    chapter_positions = []
    for chapter_num, chapter_title in chapters:
        # 构建搜索模式
        # 处理标题中的特殊字符
        search_title = re.escape(chapter_title)
        search_title = search_title.replace('\\—', '—')  # 保留破折号
        
        # 查找章节标题
        pattern = rf'{chapter_num:02d}\s+{search_title}'
        match = re.search(pattern, content)
        
        if match:
            start_pos = match.start()
            chapter_positions.append((chapter_num, chapter_title, start_pos))
            print(f"  找到第{chapter_num:02d}章: {chapter_title} (位置: {start_pos})")
        else:
            print(f"  未找到第{chapter_num:02d}章: {chapter_title}")
    
    # 按位置排序
    chapter_positions.sort(key=lambda x: x[2])
    
    print(f"\n成功定位 {len(chapter_positions)} 个章节")
    
    # 处理每个章节
    for i, (chapter_num, chapter_title, start_pos) in enumerate(chapter_positions):
        # 确定章节结束位置
        if i + 1 < len(chapter_positions):
            end_pos = chapter_positions[i + 1][2]
        else:
            end_pos = len(content)
        
        # 提取章节内容
        chapter_content = content[start_pos:end_pos]
        
        # 找到章节标题的结束位置
        lines = chapter_content.split('\n')
        title_end = 0
        
        # 查找标题行
        for j, line in enumerate(lines):
            line_stripped = line.strip()
            if re.search(rf'{chapter_num:02d}\s+', line_stripped):
                title_end = j + 1
                break
        
        # 提取标题后的内容
        if title_end < len(lines):
            body_lines = lines[title_end:]
            # 去除开头的空行
            while body_lines and not body_lines[0].strip():
                body_lines = body_lines[1:]
            body = '\n'.join(line.rstrip() for line in body_lines)
        else:
            body = ""
        
        # 创建文件名
        safe_title = re.sub(r'[^\w\s—]', '', chapter_title).strip()
        safe_title = re.sub(r'\s+', '_', safe_title)
        filename = f"100+思维模型合集_第{chapter_num:02d}章_{safe_title}.md"
        
        # 写入文件
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 100+思维模型合集 第{chapter_num:02d}章 {chapter_title}\n\n")
            f.write(body)
        
        print(f"已创建: {filename} (内容长度: {len(body)} 字符)")
    
    # 处理前言或介绍部分
    intro_start = 0
    intro_end = toc_match.start()
    intro_content = content[intro_start:intro_end].strip()
    
    if intro_content:
        with open(os.path.join(output_dir, "100+思维模型合集_前言.md"), 'w', encoding='utf-8') as f:
            f.write("# 100+思维模型合集 前言\n\n")
            f.write(intro_content)
        print(f"已创建: 100+思维模型合集_前言.md (内容长度: {len(intro_content)} 字符)")
    
    # 创建README文件
    readme_content = """# 100+思维模型合集 - 章节分割

## 书籍信息
- **书名**: 100+思维模型合集
- **作者**: 模型思维
- **类型**: 思维模型工具书

## 章节结构

### 思维模型章节
"""
    
    for chapter_num, chapter_title in chapters:
        safe_title = re.sub(r'[^\w\s—]', '', chapter_title).strip()
        safe_title = re.sub(r'\s+', '_', safe_title)
        filename = f"100+思维模型合集_第{chapter_num:02d}章_{safe_title}.md"
        readme_content += f"- [第{chapter_num:02d}章 {chapter_title}]({filename})\n"
    
    readme_content += "\n## 说明\n本书按思维模型章节分割为独立的markdown文件，便于学习和参考。每个章节都包含完整的模型内容，并保持了原文的格式和结构。"
    
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"已创建: README.md")
    print(f"\n完成！共输出 {len(chapter_positions) + 1} 个文件 -> {output_dir}")

if __name__ == "__main__":
    split_thinking_models()
