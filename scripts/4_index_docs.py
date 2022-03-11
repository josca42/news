from news.doc.index import index_docs
import time

while True:
    index_docs()
    time.sleep(60)
