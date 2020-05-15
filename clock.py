from apscheduler.schedulers.blocking import BlockingScheduler
from Shaw_scraper import*
import datetime 
from datetime import datetime, timedelta


sched = BlockingScheduler()
sgp = timezone('Asia/Singapore')

@sched.scheduled_job('cron',hour=10,minute=0, timezone='Asia/Singapore')
def seat_data():
    date=datetime.now(sgp)-timedelta(1)
    scr.get_seat_data(date.strftime('%d %b %Y'))

@sched.scheduled_job('cron',hour=22,minute=11, timezone='Asia/Singapore')
def movie_data():
    scr.get_movie_data()    



sched.start()