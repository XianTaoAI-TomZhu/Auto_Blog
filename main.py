import argparse
import sys
import asyncio
from config import Config
from browser_manager import BrowserManager
from blog_visitor import BlogVisitor
from blog_fetcher import BlogFetcher


async def main():
    parser = argparse.ArgumentParser(description="稀土掘金博客访问量自动化工具")
    parser.add_argument("--url", "-u", type=str, default=None, help="要访问的博客文章URL")
    parser.add_argument("--file", "-f", type=str, default=None, help="URL配置文件路径 (JSON格式)")
    parser.add_argument("--user", "-g", type=str, default=None, help="稀土掘金用户ID或主页URL")
    parser.add_argument("--count", "-c", type=int, default=1, help="访问次数")
    parser.add_argument("--headless", action="store_true", help="无头模式运行浏览器")
    parser.add_argument("--visible", action="store_true", help="显示浏览器窗口")
    
    args = parser.parse_args()
    
    if args.headless:
        Config.HEADLESS = True
    elif args.visible:
        Config.HEADLESS = False
    
    print("="*50)
    print("稀土掘金博客访问量自动化工具")
    print("="*50)
    
    try:
        async with BrowserManager() as browser_manager:
            visitor = BlogVisitor(browser_manager)
            
            if args.user:
                fetcher = BlogFetcher(browser_manager)
                print(f"用户: {args.user}")
                print(f"访问次数: {args.count}")
                print(f"并发数: {Config.CONCURRENCY}")
                print("="*50 + "\n")
                
                urls = await fetcher.get_user_articles(args.user)
                
                if urls:
                    print(f"\n开始访问用户文章...")
                    await visitor.visit_urls_concurrent(urls, args.count)
                else:
                    print("未能获取到用户文章")
                    sys.exit(1)
                    
            elif args.file:
                urls = Config.load_urls_from_file(args.file)
                print(f"配置文件: {args.file}")
                print(f"URL数量: {len(urls)}")
                print(f"访问次数: {args.count}")
                print(f"并发数: {Config.CONCURRENCY}")
                print("="*50 + "\n")
                await visitor.visit_urls_concurrent(urls, args.count)
            elif args.url:
                print(f"目标URL: {args.url}")
                print(f"访问次数: {args.count}")
                print(f"浏览器模式: {'无头模式' if Config.HEADLESS else '可视化模式'}")
                print("="*50 + "\n")
                await visitor.visit_multiple(args.url, args.count)
            else:
                parser.print_help()
                print("\n请提供 --url, --file 或 --user 参数")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
