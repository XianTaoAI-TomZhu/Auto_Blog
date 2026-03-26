import random
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config import Config


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright[Config.BROWSER_TYPE].launch(
            headless=Config.HEADLESS,
            args=['--disable-blink-features=AutomationControlled']
        )
        return self

    def create_context(self, user_agent: str = None):
        viewport = {'width': Config.VIEWPORT_WIDTH, 'height': Config.VIEWPORT_HEIGHT}
        
        context_options = {
            'viewport': viewport,
            'locale': 'zh-CN',
            'timezone_id': 'Asia/Shanghai',
        }
        
        if user_agent:
            context_options['user_agent'] = user_agent
        
        self.context = self.browser.new_context(**context_options)
        self.context.set_default_timeout(30000)
        return self.context

    def new_page(self) -> Page:
        if not self.context:
            user_agent = random.choice(Config.USER_AGENTS)
            self.create_context(user_agent)
        return self.context.new_page()

    def close(self):
        if self.context:
            self.context.close()
            self.context = None
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
