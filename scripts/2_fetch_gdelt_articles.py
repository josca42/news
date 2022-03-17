from news.data import articles
import time

while True:
    articles.fetch_new_articles()
    time.sleep(60)
