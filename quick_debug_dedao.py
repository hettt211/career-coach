#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速调试得到APP导航问题
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def quick_debug():
    """快速调试得到APP页面"""
    print("🔍 快速调试得到APP...")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # 访问首页
        print("1️⃣ 访问首页...")
        driver.get("https://www.dedao.cn/")
        time.sleep(3)
        
        print(f"页面标题: {driver.title}")
        
        # 查找所有包含"职场"的链接
        print("\n2️⃣ 查找职场相关链接...")
        workplace_links = driver.find_elements(By.XPATH, "//a[contains(@href, '职场') or contains(text(), '职场')]")
        
        print(f"找到 {len(workplace_links)} 个职场相关链接:")
        for i, link in enumerate(workplace_links[:5], 1):
            href = link.get_attribute("href")
            text = link.text.strip()
            print(f"  {i}. {text} -> {href}")
        
        # 如果找到职场链接，直接访问
        if workplace_links:
            print(f"\n3️⃣ 直接访问第一个职场链接...")
            target_url = workplace_links[0].get_attribute("href")
            driver.get(target_url)
            time.sleep(3)
            
            print(f"职场页面标题: {driver.title}")
            print(f"职场页面URL: {driver.current_url}")
            
            # 分析职场页面的课程结构
            print("\n4️⃣ 分析课程结构...")
            
            # 尝试多种课程选择器
            course_selectors = [
                "a[href*='course']",
                "a[href*='product']", 
                "[class*='course']",
                "[class*='product']",
                "[class*='card']",
                "h3", "h4"
            ]
            
            for selector in course_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"  选择器 '{selector}': {len(elements)} 个元素")
                    
                    # 显示前3个元素的文本
                    for i, elem in enumerate(elements[:3], 1):
                        try:
                            text = elem.text.strip()[:50]
                            href = elem.get_attribute("href") or "无链接"
                            if text:
                                print(f"    {i}. {text}... -> {href[:50]}...")
                        except:
                            continue
        
        # 保存页面源码片段用于分析
        with open("dedao_page_sample.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source[:5000])  # 保存前5000字符
        print("\n📄 页面源码片段已保存到 dedao_page_sample.html")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    quick_debug()
