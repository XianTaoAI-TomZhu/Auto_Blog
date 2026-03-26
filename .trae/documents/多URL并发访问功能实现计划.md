# 多URL并发访问功能实现计划

## 需求分析

1. **新增配置文件存储URL地址** - 支持存储多个URL
2. **终端能同时访问配置文件中所有URL** - 读取配置文件并访问所有URL
3. **增加并发机制** - 默认3并发且不能修改
4. **新增用户文章获取功能** - 通过用户ID或主页获取用户所有文章并访问

## 实现步骤

### 1. 创建URL配置文件 `urls.json`
- 创建 `urls.json` 文件，格式如下：
```json
{
    "urls": [
        "https://juejin.cn/post/7618196523335221291",
        "https://juejin.cn/post/xxx",
        ...
    ]
}
```

### 2. 修改 config.py
- 添加 `URLS_FILE` 配置项，指向 `urls.json`
- 添加 `CONCURRENCY` 配置项，默认值为 3（不可修改）
- 添加 `load_urls_from_file()` 方法用于读取URL列表

### 3. 修改 blog_visitor.py
- 添加 `visit_urls_concurrent()` 方法
- 使用 Python `asyncio.Semaphore` 实现并发访问
- 每个协程独立使用浏览器页面访问URL

### 4. 修改 main.py
- 添加 `--file` / `-f` 参数，用于指定URL配置文件
- 添加 `--user` / `-g` 参数，用于指定稀土掘金用户
- 当使用 `--file` 参数时，读取配置文件中的所有URL并并发访问
- 添加相应的使用提示

### 5. 新增 blog_fetcher.py
- 创建用户文章获取模块
- 支持通过用户ID或用户主页URL获取用户所有文章
- 优先尝试API获取，失败时使用页面抓取

## 文件修改清单

| 文件 | 修改内容 |
|------|----------|
| `urls.json` | 新增，存储多个URL |
| `config.py` | 添加URL配置文件路径、并发数配置、加载方法 |
| `blog_visitor.py` | 添加并发访问方法，使用asyncio实现 |
| `browser_manager.py` | 改为异步API |
| `main.py` | 添加 --file 和 --user 参数支持 |
| `blog_fetcher.py` | 新增，用户文章获取模块 |

## 使用方式

```bash
# 使用配置文件访问（并发3个URL）
python main.py --file urls.json

# 使用配置文件，每个URL访问2次
python main.py -f urls.json -c 2

# 单独访问单个URL（保持原有功能）
python main.py --url "https://juejin.cn/post/xxx" --count 10

# 通过用户ID访问用户所有文章
python main.py --user "用户ID"

# 通过用户主页URL访问
python main.py -g "https://juejin.cn/user/xxxxxx"

# 访问用户所有文章2次
python main.py -g "用户ID" -c 2
```

## 技术说明

- 由于Playwright同步API不支持多线程，改用异步API (`async_playwright`)
- 使用 `asyncio.Semaphore` 控制并发数为3
- 用户文章获取优先调用稀土掘金API，失败时降级为页面抓取
