from news.doc.add import add_articles2docArray
import time

while True:
    add_articles2docArray(load_images=True)
    time.sleep(60)
