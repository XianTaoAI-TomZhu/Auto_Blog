import argparse
import sys
from config import Config
from browser_manager import BrowserManager
from blog_visitor import BlogVisitor


def main():
    parser = argparse.ArgumentParser(description="稀土掘金博客访问量自动化工具")
    parser.add_argument("--url", "-u", type=str, default=Config.DEFAULT_URL, help="要访问的博客文章URL")
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
    print(f"目标URL: {args.url}")
    print(f"访问次数: {args.count}")
    print(f"浏览器模式: {'无头模式' if Config.HEADLESS else '可视化模式'}")
    print("="*50 + "\n")
    
    try:
        with BrowserManager() as browser_manager:
            visitor = BlogVisitor(browser_manager)
            visitor.visit_multiple(args.url, args.count)
            
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
