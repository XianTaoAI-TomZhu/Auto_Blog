import random
import time
from playwright.sync_api import Page
from config import Config
from browser_manager import BrowserManager


class BlogVisitor:
    def __init__(self, browser_manager: BrowserManager):
        self.browser_manager = browser_manager
        self.success_count = 0
        self.fail_count = 0

    def visit_page(self, url: str) -> bool:
        page = None
        try:
            page = self.browser_manager.new_page()
            
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            if response and response.ok:
                self._simulate_reading(page)
                self.success_count += 1
                print(f"[+] 成功访问: {url}")
                return True
            else:
                self.fail_count += 1
                print(f"[-] 访问失败: {url}, 状态码: {response.status if response else 'N/A'}")
                return False
                
        except Exception as e:
            self.fail_count += 1
            print(f"[-] 访问出错: {url}, 错误: {str(e)}")
            return False
        finally:
            if page:
                page.close()

    def _simulate_reading(self, page: Page):
        stay_time = random.randint(Config.MIN_STAY_TIME, Config.MAX_STAY_TIME)
        
        page.mouse.wheel(0, random.randint(100, 300))
        time.sleep(random.uniform(1, 2))
        
        steps = stay_time // 3
        for _ in range(steps):
            scroll_amount = random.randint(200, 500)
            page.mouse.wheel(0, scroll_amount)
            time.sleep(random.uniform(2, 4))
        
        page.mouse.wheel(0, -random.randint(100, 200))
        time.sleep(random.uniform(0.5, 1))

    def visit_multiple(self, url: str, count: int):
        print(f"\n开始访问任务: URL={url}, 次数={count}\n")
        
        for i in range(count):
            print(f"进度: {i+1}/{count}")
            self.visit_page(url)
            
            if i < count - 1:
                delay = random.randint(Config.MIN_DELAY, Config.MAX_DELAY)
                print(f"等待 {delay} 秒后继续...")
                time.sleep(delay)
        
        self.print_stats()

    def print_stats(self):
        print("\n" + "="*50)
        print(f"访问统计:")
        print(f"  成功: {self.success_count}")
        print(f"  失败: {self.fail_count}")
        print(f"  总计: {self.success_count + self.fail_count}")
        print("="*50 + "\n")
