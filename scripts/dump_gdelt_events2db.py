from news.data import gdelt
import schedule, time


def job():
    gdelt.add_latest_events2db(english=True)
    gdelt.add_latest_events2db(english=False)


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(5)
