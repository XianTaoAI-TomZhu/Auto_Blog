import os
import json
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

    CONCURRENCY = 3

    URLS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "urls.json")

    @classmethod
    def load_urls_from_file(cls, file_path: str = None) -> list:
        if file_path is None:
            file_path = cls.URLS_FILE

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"URL配置文件不存在: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        urls = data.get('urls', [])
        if not urls:
            raise ValueError("URL配置文件为空或格式错误")

        return urls
