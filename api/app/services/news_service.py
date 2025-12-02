import os
import json
import time
from datetime import datetime
import requests
from app.config import settings
from app.core.logger import logger

class NewsService:
    def __init__(self):
        self.api_key = settings.data_sources.news_api_key
        self.base_path = "data/news"
        self.retry_attempts = 3
        self.retry_delay = 3
        self.request_delay = 1

    def fetch_news(self, symbol: str) -> list:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={self.api_key}"
        for attempt in range(1, self.retry_attempts + 1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    time.sleep(self.request_delay)
                    return response.json().get("articles", [])
                else:
                    logger.warning(f"Failed to fetch news for {symbol}: HTTP {response.status_code}")
            except Exception as e:
                logger.error(f"Error fetching news for {symbol}, attempt {attempt}/{self.retry_attempts}: {e}")
                if attempt < self.retry_attempts:
                    time.sleep(self.retry_delay)
        return []

    def save_news(self, symbol: str, articles: list):
        if not articles:
            logger.warning(f"No news to save for {symbol}.")
            return
        today = datetime.now()
        path = os.path.join(self.base_path, str(today.year), str(today.month), str(today.day))
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{symbol}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        logger.info(f"Saved news for {symbol} to {file_path}")

    def fetch_and_save(self, symbols: list):
        for symbol in symbols:
            articles = self.fetch_news(symbol)
            self.save_news(symbol, articles)
