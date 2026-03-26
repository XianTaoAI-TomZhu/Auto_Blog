import random
import asyncio
from playwright.async_api import Page
from config import Config


class BlogVisitor:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        self.success_count = 0
        self.fail_count = 0
        self._lock = asyncio.Lock()

    async def visit_page(self, url: str) -> bool:
        page = None
        try:
            page = await self.browser_manager.new_page()
            
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            if response and response.ok:
                await self._simulate_reading(page)
                async with self._lock:
                    self.success_count += 1
                print(f"[+] 成功访问: {url}")
                return True
            else:
                async with self._lock:
                    self.fail_count += 1
                print(f"[-] 访问失败: {url}, 状态码: {response.status if response else 'N/A'}")
                return False
                
        except Exception as e:
            async with self._lock:
                self.fail_count += 1
            print(f"[-] 访问出错: {url}, 错误: {str(e)}")
            return False
        finally:
            if page:
                await page.close()

    async def _simulate_reading(self, page: Page):
        stay_time = random.randint(Config.MIN_STAY_TIME, Config.MAX_STAY_TIME)
        
        await page.mouse.wheel(0, random.randint(100, 300))
        await asyncio.sleep(random.uniform(1, 2))
        
        steps = stay_time // 3
        for _ in range(steps):
            scroll_amount = random.randint(200, 500)
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(2, 4))
        
        await page.mouse.wheel(0, -random.randint(100, 200))
        await asyncio.sleep(random.uniform(0.5, 1))

    async def visit_multiple(self, url: str, count: int):
        print(f"\n开始访问任务: URL={url}, 次数={count}\n")
        
        for i in range(count):
            print(f"进度: {i+1}/{count}")
            await self.visit_page(url)
            
            if i < count - 1:
                delay = random.randint(Config.MIN_DELAY, Config.MAX_DELAY)
                print(f"等待 {delay} 秒后继续...")
                await asyncio.sleep(delay)
        
        await self.print_stats()

    async def visit_urls_concurrent(self, urls: list, count: int = 1):
        print(f"\n开始并发访问任务: URL数量={len(urls)}, 访问次数={count}, 并发数={Config.CONCURRENCY}\n")

        async def visit_with_semaphore(url):
            async with asyncio.Semaphore(Config.CONCURRENCY):
                await self.visit_page(url)

        for i in range(count):
            if count > 1:
                print(f"\n--- 第 {i+1}/{count} 轮访问 ---")
            tasks = [visit_with_semaphore(url) for url in urls]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            if i < count - 1:
                delay = random.randint(Config.MIN_DELAY, Config.MAX_DELAY)
                print(f"等待 {delay} 秒后继续下一轮...")
                await asyncio.sleep(delay)

        await self.print_stats()

    async def print_stats(self):
        print("\n" + "="*50)
        print(f"访问统计:")
        print(f"  成功: {self.success_count}")
        print(f"  失败: {self.fail_count}")
        print(f"  总计: {self.success_count + self.fail_count}")
        print("="*50 + "\n")
