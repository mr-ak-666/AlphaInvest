import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import json

class IndiaStockNewsCollector:
    """Fetch real-time news affecting BSE/NSE Indian stock markets"""
    
    def __init__(self):
        self.sources = {
            'moneycontrol': 'https://www.moneycontrol.com/rss/latestnews.xml',
            'economic_times': 'https://economictimes.indiatimes.com/rssfeedstopstories.cms',
            'business_standard': 'https://www.business-standard.com/rss/home_page_top_stories.rss',
            'livemint': 'https://www.livemint.com/rss/markets',
            'ndtv_profit': 'https://www.ndtvprofit.com/rss/news',
            'reuters_india': 'https://www.reuters.com/places/india',
        }
    
    def fetch_news(self, limit_per_source: int = 20) -> List[Dict]:
        """Fetch all news from Indian financial sources"""
        all_news = []
        
        for source, url in self.sources.items():
            try:
                news_items = self._fetch_rss(url, source, limit_per_source)
                all_news.extend(news_items)
            except Exception as e:
                print(f"Error fetching {source}: {e}")
        
        # Sort by time
        all_news.sort(key=lambda x: x['published'], reverse=True)
        return self._remove_duplicates(all_news)
    
    def _fetch_rss(self, url: str, source: str, limit: int) -> List[Dict]:
        """Fetch RSS feed"""
        feed = feedparser.parse(url)
        news_items = []
        
        for entry in feed.entries[:limit]:
            published = datetime.now()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            
            description = ''
            if hasattr(entry, 'summary'):
                description = self._clean_html(entry.summary)
            elif hasattr(entry, 'description'):
                description = self._clean_html(entry.description)
            
            news_items.append({
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', '#'),
                'description': description[:500],
                'published': published,
                'source': source.upper().replace('_', ' ')
            })
        
        return news_items
    
    def _clean_html(self, html_text: str) -> str:
        """Remove HTML tags"""
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text().strip()
    
    def _remove_duplicates(self, news_list: List[Dict]) -> List[Dict]:
        """Remove duplicate news"""
        seen = set()
        unique = []
        
        for news in news_list:
            title_key = news['title'][:50].lower()
            if title_key not in seen:
                seen.add(title_key)
                unique.append(news)
        
        return unique