from news.data import articles
import time

while True:
    articles.fetch_remaining()
    time.sleep(5 * 60)
