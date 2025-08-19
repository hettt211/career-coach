#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
思维模型合集章节分割脚本
专门处理"100+思维模型合集"这种编号格式的章节
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
    
    # 首先尝试用pdfminer提取文本
    try:
        from pdfminer.high_level import extract_text
        print("正在提取PDF文本...")
        content = extract_text(input_file)
        print(f"PDF文本提取成功，长度: {len(content)} 字符")
    except Exception as e:
        print(f"PDF文本提取失败: {e}")
        return
    
    # 定义章节模式 - 匹配 "01 模型思维——牛人顶级思维法" 这种格式
    chapter_pattern = r'(\d{2})\s+([^—\n]+)—([^\n]+)'
    
    # 找到所有章节
    chapters = []
    for match in re.finditer(chapter_pattern, content):
        chapter_num = int(match.group(1))
        chapter_title = match.group(2).strip()
        chapter_subtitle = match.group(3).strip()
        full_title = f"{chapter_title}—{chapter_subtitle}"
        start_pos = match.start()
        chapters.append((chapter_num, full_title, start_pos))
    
    # 按章节号排序
    chapters.sort(key=lambda x: x[0])
    
    print(f"找到 {len(chapters)} 个思维模型章节")
    
    # 处理每个章节
    for i, (chapter_num, chapter_title, start_pos) in enumerate(chapters):
        # 确定章节结束位置
        if i + 1 < len(chapters):
            end_pos = chapters[i + 1][2]
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
    # 查找目录前的内容
    toc_match = re.search(r'目\s*录', content)
    if toc_match:
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
    
    for chapter_num, chapter_title, _ in chapters:
        safe_title = re.sub(r'[^\w\s—]', '', chapter_title).strip()
        safe_title = re.sub(r'\s+', '_', safe_title)
        filename = f"100+思维模型合集_第{chapter_num:02d}章_{safe_title}.md"
        readme_content += f"- [第{chapter_num:02d}章 {chapter_title}]({filename})\n"
    
    readme_content += "\n## 说明\n本书按思维模型章节分割为独立的markdown文件，便于学习和参考。每个章节都包含完整的模型内容，并保持了原文的格式和结构。"
    
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"已创建: README.md")
    print(f"\n完成！共输出 {len(chapters) + 1} 个文件 -> {output_dir}")

if __name__ == "__main__":
    split_thinking_models()
