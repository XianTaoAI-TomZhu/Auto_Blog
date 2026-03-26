import random
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config import Config


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright[Config.BROWSER_TYPE].launch(
            headless=Config.HEADLESS,
            args=['--disable-blink-features=AutomationControlled']
        )
        return self

    async def create_context(self, user_agent: str = None):
        viewport = {'width': Config.VIEWPORT_WIDTH, 'height': Config.VIEWPORT_HEIGHT}
        
        context_options = {
            'viewport': viewport,
            'locale': 'zh-CN',
            'timezone_id': 'Asia/Shanghai',
        }
        
        if user_agent:
            context_options['user_agent'] = user_agent
        
        self.context = await self.browser.new_context(**context_options)
        self.context.set_default_timeout(30000)
        return self.context

    async def new_page(self) -> Page:
        if not self.context:
            user_agent = random.choice(Config.USER_AGENTS)
            await self.create_context(user_agent)
        return await self.context.new_page()

    async def close(self):
        if self.context:
            await self.context.close()
            self.context = None
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
