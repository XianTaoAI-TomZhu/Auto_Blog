# 稀土掘金博客访问量自动化工具

## 项目概述

通过浏览器自动化技术（Playwright）自动访问稀土掘金博客文章，增加页面访问量。

## 环境确认

- 操作系统: Windows
- Python版本: 3.13+
- 浏览器自动化库: Playwright

## 文件结构

```
Auto_Blog/
├── config.py           # 配置文件
├── browser_manager.py  # 浏览器管理
├── blog_visitor.py    # 访问逻辑
├── blog_fetcher.py     # 用户文章获取
├── main.py            # 主程序
├── urls.json          # URL配置文件
├── requirements.txt   # 依赖
└── README.md          # 使用说明
```

## 依赖库

- playwright - 浏览器自动化
- python-dotenv - 环境变量管理

## 安装

```bash
pip install -r requirements.txt
playwright install
```

## 使用方式

### 1. 访问单个URL

```bash
# 访问指定URL 1次
python main.py --url "https://juejin.cn/post/xxx"

# 访问指定URL 10次
python main.py -u "https://juejin.cn/post/xxx" --count 10
```

### 2. 使用配置文件批量访问

编辑 `urls.json` 文件：

```json
{
    "urls": [
        "https://juejin.cn/post/7618196523335221291",
        "https://juejin.cn/post/7619093505763901455",
        "https://juejin.cn/post/7619006433164312576"
    ]
}
```

运行：

```bash
# 使用配置文件访问所有URL（默认3并发）
python main.py --file urls.json

# 使用配置文件，每个URL访问2次
python main.py -f urls.json -c 2
```

### 3. 通过用户获取文章并访问

```bash
# 通过用户ID访问
python main.py --user "用户ID"

# 通过用户主页URL访问
python main.py -g "https://juejin.cn/user/xxxxxx"

# 访问用户所有文章2次
python main.py -g "用户ID" -c 2
```

### 4. 浏览器模式

```bash
# 无头模式（默认）
python main.py -u "URL" --headless

# 显示浏览器窗口
python main.py -u "URL" --visible
```

## 功能特性

- ✅ 使用 Playwright 进行浏览器自动化
- ✅ 模拟真实用户阅读行为（滚动页面、随机停留时间）
- ✅ 随机 User-Agent 防止被检测
- ✅ 支持自定义访问间隔（5-15秒）
- ✅ 支持无头/可视化模式
- ✅ 访问统计功能
- ✅ 支持配置文件批量访问多个URL
- ✅ 默认3并发访问（不可修改）
- ✅ 支持通过用户获取所有文章并访问

## 并发说明

- 并发数默认为 **3**，不可修改
- 并发访问时会自动控制同时进行的浏览器数量
- 配置文件模式和多URL模式均支持并发访问
