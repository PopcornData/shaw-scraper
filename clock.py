from apscheduler.schedulers.blocking import BlockingScheduler
from Shaw_scraper import*
import datetime 
from datetime import datetime, timedelta


sched = BlockingScheduler()

#Repeat job after specified interval
@sched.scheduled_job('interval', seconds=10000)
def print_data():
    print("Have a good day!")

@sched.scheduled_job('cron',hour=1,minute=1, timezone='Asia/Singapore')
def seat_data():
    date=datetime.now()-timedelta(1)
    scr.get_seat_data(date.strftime('%d %b %Y'))

@sched.scheduled_job('cron',hour=8,minute=0, timezone='Asia/Singapore')
def movie_data():
    scr.get_movie_data()    


sched.start()