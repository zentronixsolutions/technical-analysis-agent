import yfinance as yf
from pyshorteners import Shortener

shortener = Shortener()

def get_news(symbol):
  news = {}
  ticker = yf.Ticker(symbol.replace("\n", ""))
  news_items = ticker.news
  for item in news_items[:5]:
    title = item['content']["title"]
    # short_url = shortener.tinyurl.short(item['content']["canonicalUrl"]["url"])
    news[title] = item['content']["canonicalUrl"]["url"]
  return news