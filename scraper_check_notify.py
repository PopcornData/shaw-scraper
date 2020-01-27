import telegram
from telegram.ext import *
import pymongo
from datetime import datetime
from pytz import timezone
import threading


updater = Updater(token='653101517:AAFhv9tYNvOibm-rzb5pR-X107I4LCbANbo')
dispatcher = updater.dispatcher   
j = updater.job_queue
dash="-"*38
sgp = timezone('Asia/Singapore')



def check_scraper():

    client = pymongo.MongoClient("mongodb+srv://Mathew:scraper1234@cluster0-dgi6j.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('shaw_data')

    mycol = db["movie_data"]
    date=datetime.now(sgp)
    date=date.strftime('%d %b %Y')
    mydoc = mycol.find({'date': date})#16th, 23rd and 25th have problems
    res=[]
    for doc in mydoc:
        res.append(doc)
    check=[]
    not_done=[]
    print(len(res))
    for i,r in enumerate(res):
      try:
        check.append(len(r['seats']))
      except:
        not_done.append(i)
    print(len(check))
    return len(res),len(check)
        

def sendmsg(bot,update):
    res=check_scraper()
    text='Total: {}, Scraped: {}'.format(res[0], res[1])   
    bot.send_message(chat_id=490133039,text=text,parse_mode="HTML",disable_web_page_preview=False)

def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    threading.Thread(target=shutdown).start()

    

        
def main():

        
        job1 = j.run_repeating(sendmsg, interval=60, first=5) 
        job2 = j.run_repeating(stop, interval=20, first=20) 
        # handler = MessageHandler(Filters.video | Filters.photo | Filters.document, sendmsg)
        # dispatcher.add_handler(handler)
        updater.start_polling()
        updater.idle()
          

