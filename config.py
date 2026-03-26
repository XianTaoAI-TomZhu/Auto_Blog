import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEFAULT_URL = os.getenv("DEFAULT_URL", "https://juejin.cn/post/7618196523335221291")

    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

    MIN_DELAY = int(os.getenv("MIN_DELAY", "5"))
    MAX_DELAY = int(os.getenv("MAX_DELAY", "15"))

    MIN_STAY_TIME = int(os.getenv("MIN_STAY_TIME", "10"))
    MAX_STAY_TIME = int(os.getenv("MAX_STAY_TIME", "30"))

    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")

    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1280"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "720"))

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    ]
