# 职场课程内容爬虫

自动爬取职场相关课程信息的Python脚本，支持多分类爬取、详情页内容提取和AI分析数据格式化。

## 功能特性

- ✅ **多分类爬取**: 支持7个职场分类的课程爬取
- ✅ **详情页提取**: 自动进入课程详情页获取亮点和内容
- ✅ **智能滚动**: 处理动态加载的课程内容列表
- ✅ **多格式输出**: 支持CSV、JSON和AI分析摘要格式
- ✅ **错误处理**: 完善的错误重试和日志记录
- ✅ **配置化**: 支持配置文件自定义爬取参数

## 支持的分类

1. 说话沟通
2. 情绪管理
3. 时间管理
4. 目标管理
5. 职业技能
6. 领导力
7. 人脉社交

## 安装依赖

### 方法1: 自动安装
```bash
python3 install_requirements.py
```

### 方法2: 手动安装
```bash
# 安装Python依赖
pip install selenium pandas requests beautifulsoup4 lxml

# 安装ChromeDriver (macOS)
brew install chromedriver

# 安装ChromeDriver (Ubuntu/Debian)
sudo apt-get install chromium-chromedriver
```

## 使用方法

### 基础使用
```bash
# 使用默认配置运行
python3 advanced_course_scraper.py
```

### 自定义配置
1. 编辑 `scraper_config.json` 文件
2. 运行脚本

```bash
python3 advanced_course_scraper.py
```

## 配置说明

### scraper_config.json 配置项

```json
{
  "scraper_settings": {
    "headless": false,           // 是否无头模式运行
    "max_courses_per_category": 20,  // 每个分类最多爬取课程数
    "delay_between_requests": 1,     // 请求间隔(秒)
    "delay_between_categories": 2,   // 分类间隔(秒)
    "page_load_timeout": 10,         // 页面加载超时(秒)
    "scroll_pause_time": 2           // 滚动暂停时间(秒)
  },
  "categories": [...],          // 要爬取的分类列表
  "output": {
    "csv_enabled": true,        // 是否输出CSV
    "json_enabled": true,       // 是否输出JSON
    "summary_enabled": true,    // 是否生成AI摘要
    "output_directory": "./output"  // 输出目录
  }
}
```

## 输出文件

脚本运行完成后会在 `output` 目录生成以下文件：

1. **courses_data_YYYYMMDD_HHMMSS.csv** - CSV格式的课程数据
2. **courses_data_YYYYMMDD_HHMMSS.json** - JSON格式的课程数据
3. **courses_summary_for_ai_YYYYMMDD_HHMMSS.txt** - AI分析专用摘要
4. **failed_courses_YYYYMMDD_HHMMSS.json** - 失败的课程记录(如有)
5. **scraper_YYYYMMDD_HHMMSS.log** - 运行日志

## 数据字段说明

### 基础信息
- `category`: 课程分类
- `title`: 课程标题
- `subtitle`: 课程副标题
- `type`: 课程类型
- `play_count`: 学习人数
- `track_count`: 课程讲数
- `url`: 详情页链接

### 详情信息
- `highlights`: 课程亮点
- `content`: 课程内容列表
- `scraped_at`: 爬取时间
- `detail_scraped_at`: 详情爬取时间

## AI分析建议

使用生成的 `courses_summary_for_ai_*.txt` 文件进行AI分析，可以关注以下方面：

### 1. 内容共性分析
- 各分类课程的核心主题
- 高频出现的关键词
- 课程结构的共同特点

### 2. 趋势分析
- 不同分类的课程数量分布
- 学习人数的分布特征
- 课程长度的特点

### 3. 质量评估
- 课程亮点的表达方式
- 内容组织的逻辑性
- 实用性和可操作性

## 故障排除

### 常见问题

1. **ChromeDriver错误**
   ```bash
   # 检查Chrome版本
   google-chrome --version
   # 下载对应版本的ChromeDriver
   # https://chromedriver.chromium.org/
   ```

2. **macOS安全问题**: "无法打开chromedriver，因为Apple无法检查其是否包含恶意软件"
   ```bash
   # 方法1: 自动修复（推荐）
   python3 fix_chromedriver_mac.py
   
   # 方法2: 手动修复
   xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
   
   # 方法3: 重新安装
   brew uninstall chromedriver
   brew install chromedriver
   ```

2. **页面加载失败**
   - 检查网络连接
   - 增加 `page_load_timeout` 配置
   - 关闭 `headless` 模式查看浏览器状态

3. **元素定位失败**
   - 网站可能更新了页面结构
   - 查看日志文件了解具体错误
   - 需要更新选择器配置

### 调试模式

设置 `headless: false` 可以看到浏览器运行过程，便于调试。

## 注意事项

1. **遵守网站使用条款**: 请确保爬取行为符合目标网站的使用条款
2. **合理控制频率**: 避免过于频繁的请求对服务器造成压力
3. **数据使用规范**: 爬取的数据仅供学习和研究使用
4. **及时更新**: 网站结构变化时需要更新选择器配置

## 技术栈

- **Python 3.7+**
- **Selenium**: 浏览器自动化
- **Pandas**: 数据处理
- **Requests**: HTTP请求
- **ChromeDriver**: Chrome浏览器驱动

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 支持基础课程信息爬取
- 支持详情页内容提取
- 支持多格式数据输出

---

如有问题或建议，欢迎提交Issue或Pull Request。
