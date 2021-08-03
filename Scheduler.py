from schedule import every, repeat, run_pending
import time

@repeat(every(10).seconds)
def job():
    print("I am a scheduled job")

while True:
    run_pending()
    time.sleep(1)