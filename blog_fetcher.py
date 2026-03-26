import re
import asyncio
import random
import urllib.request
import json
from playwright.async_api import Page
from config import Config


class BlogFetcher:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager

    async def get_user_articles(self, user_url: str) -> list:
        user_id = self._extract_user_id(user_url)
        
        if not user_id:
            print(f"无法提取用户ID: {user_url}")
            return []
        
        print(f"正在获取用户文章列表, 用户ID: {user_id}")
        
        articles = await self._fetch_articles_from_api(user_id)
        
        if articles:
            print(f"共获取到 {len(articles)} 篇文章")
        else:
            print("API获取失败，尝试页面抓取...")
            articles = await self._fetch_articles_from_page(user_url)
        
        return articles
    
    async def _fetch_articles_from_api(self, user_id: str) -> list:
        articles = []
        cursor = "0"
        
        try:
            for page_num in range(10):
                url = f"https://api.juejin.cn/content_api/v1/article/list_by_user?user_id={user_id}&cursor={cursor}&category_id="
                
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    if data.get('data') and data['data'].get('article_list'):
                        article_list = data['data']['article_list']
                        if not article_list:
                            break
                            
                        for article in article_list:
                            article_url = f"https://juejin.cn/post/{article.get('article_id', '')}"
                            if article_url not in articles:
                                articles.append(article_url)
                        
                        cursor = data['data'].get('cursor', '')
                        if not cursor:
                            break
                            
                        print(f"API获取到 {len(articles)} 篇文章...")
                    else:
                        break
                    
        except Exception as e:
            print(f"API获取失败: {str(e)}")
            
        return articles
    
    async def _fetch_articles_from_page(self, user_url: str) -> list:
        page = None
        articles = []
        
        try:
            user_url = self._normalize_user_url_to_home(user_url)
            print(f"正在从页面获取用户文章: {user_url}")

            page = await self.browser_manager.new_page()
            
            await page.goto(user_url, wait_until="networkidle", timeout=30000)
            
            await asyncio.sleep(5)
            
            title = await page.title()
            print(f"页面标题: {title}")
            
            content = await page.content()
            print(f"页面内容长度: {len(content)}")
            
            if '暂无内容' in content or '没有' in content:
                print("用户主页没有内容")
                
            print("\n正在尝试查找文章链接...")
            
            post_links = await page.query_selector_all('[href*="/post/"]')
            print(f"找到 {len(post_links)} 个文章链接")
            
            for link in post_links:
                try:
                    href = await link.get_attribute('href')
                    if href:
                        if href.startswith('/'):
                            href = 'https://juejin.cn' + href
                        if href not in articles:
                            articles.append(href)
                except:
                    continue

            print(f"页面获取到 {len(articles)} 篇文章")
            
            if articles:
                print("前5个链接:", articles[:5])
            
        except Exception as e:
            print(f"页面获取失败: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            if page:
                await page.close()
                
        return articles

    def _normalize_user_url_to_home(self, user_url: str) -> str:
        user_url = user_url.strip()

        if not user_url.startswith('http'):
            if 'juejin.cn' not in user_url:
                user_url = f"https://juejin.cn/user/{user_url}"
            else:
                user_url = f"https://juejin.cn/{user_url}"
        
        user_url = user_url.rstrip('/')
        
        if user_url.endswith('/posts'):
            user_url = user_url[:-6]

        match = re.search(r'juejin\.cn/(?:user/)?(\w+)', user_url)
        if match:
            user_id = match.group(1)
            return f"https://juejin.cn/user/{user_id}"

        return user_url

    def _extract_user_id(self, user_url: str) -> str:
        user_url = user_url.strip()
        
        if user_url.isdigit():
            return user_url
            
        match = re.search(r'juejin\.cn/(?:user/)?(\w+)', user_url)
        if match:
            return match.group(1)
        return None

    def _normalize_user_url(self, user_url: str) -> str:
        user_url = user_url.strip()

        if not user_url.startswith('http'):
            if 'juejin.cn' not in user_url:
                user_url = f"https://juejin.cn/user/{user_url}/posts"
            else:
                user_url = f"https://juejin.cn/{user_url}/posts"
        
        if 'juejin.cn/user/' in user_url and '/posts' not in user_url:
            user_url = user_url.rstrip('/') + '/posts'

        match = re.search(r'juejin\.cn/(?:user/)?(\w+)', user_url)
        if match:
            user_id = match.group(1)
            return f"https://juejin.cn/user/{user_id}/posts"

        return user_url
