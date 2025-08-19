#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyPDF2
import sys
import os

def extract_pdf_text(pdf_path):
    """提取PDF文本内容"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"正在处理: {pdf_path}")
            print(f"总页数: {len(pdf_reader.pages)}")
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += f"\n--- 第{page_num + 1}页 ---\n"
                        text += page_text
                        text += "\n"
                except Exception as e:
                    print(f"处理第{page_num + 1}页时出错: {e}")
                    continue
            
            return text
    except Exception as e:
        print(f"处理PDF文件时出错: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("用法: python3 extract_pdf.py <pdf文件路径>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"文件不存在: {pdf_path}")
        sys.exit(1)
    
    # 提取文本
    text = extract_pdf_text(pdf_path)
    
    if text:
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}.txt"
        
        # 保存到文本文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"文本已提取到: {output_path}")
        print(f"提取的文本长度: {len(text)} 字符")
        
        # 显示前500个字符作为预览
        print("\n--- 内容预览 ---")
        print(text[:500])
        if len(text) > 500:
            print("...")
    else:
        print("无法提取文本内容")

if __name__ == "__main__":
    main()
