from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from user_agent_rotation import *
import time as tm
import traceback
import datetime
from datetime import datetime
import pytz
from pytz import timezone 
from bs4 import BeautifulSoup
import random
import json
import requests
import pymongo
import os

MONGODB_URI=os.environ.get("MONGODB_URI")

client = pymongo.MongoClient(MONGODB_URI,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True,
                     retryWrites=False)

db = client.get_default_database()
mycol = db["movie_data"]

class shaw_scraper():
    
    def __init__(self):
        # Create a headless browser  
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("window-size=1920,1080")
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self.chrome_options)
        self.base_url="https://www.shaw.sg/theatre/location/"
        
    def get_movie_data(self):
        
        theatres={
        "Lido":"0100",
        "Jewel":"1000",
        "Paya_Lebar":"1100",
        "Waterway_Point": "0900",
        "Nex":"0700",
        "Seletar": "0800",
        "Jcube":"0200",
        "Lot_One":"0400",
        "Balestiar":"0300"
        }

        errors=[]
        sgp = timezone('Asia/Singapore')
        date=datetime.now(sgp)
        dt=date.strftime('%d %b %Y')
        
        
        for theatre,code in theatres.items():
            try:
                print(theatre)
                self.browser.get(self.base_url + code)
                tm.sleep(3)
                all_dates=self.browser.find_elements_by_class_name("owl-item")
                # right_button=self.browser.find_element_by_class_name("time-nav-btn-right")
                for i in range(0,2000,5):
                    tm.sleep(0.005)
                    self.browser.execute_script("window.scrollTo({},{});".format(str(i),str(i+1)))
                try:
                    tm.sleep(2)
                    ActionChains(self.browser).move_to_element(all_dates[0]).click().perform()
                    tm.sleep(2)
                    page=BeautifulSoup(self.browser.page_source, "html.parser")
                    movie_date=dt
                    print(theatre,movie_date)
                    all_movies=page.find("div",{"class":"detail-location"})
                    all_movies=all_movies.find_all("div",{"class":"movies_item-movie"})

                    for movie in all_movies:
                        #Movie Title
                        movie_title=movie.find("div",{"class":"title"}).text
                        print(movie_title)

                        #Hall, timing and session code
                        movie_times=movie.find_all("div",{"class":"showtimes-block"})

                        for time in movie_times:
                            mycol.update_one( { 
                                 'theatre' : theatre,
                                 'hall': time.a["data-balloon"].split("\n")[0],
                                 'movie':movie_title,
                                 'date':movie_date,
                                 'session_code': time.a["href"][16:]}, 
                                {'$set' : {'time': time.a.text} }, 
                                upsert = True 
                                )
                            print({ 
                                 'theatre' : theatre,
                                 'hall': time.a["data-balloon"].split("\n")[0],
                                 'movie':movie_title,
                                 'date':movie_date,
                                 'time': time.a.text,
                                 'session_code': time.a["href"][16:]})

                except Exception:
                    traceback.print_exc() 
                    # errors.append([theatre,movie_title,movie_date,time.a.text])


            except Exception:
                traceback.print_exc()            

        self.browser.quit()
        print('Finished scraping movie details for {}'.format(dt))
        print('Errors:\n', errors)

    def get_seat_data(self, date):
        movie_data = mycol.find({"date": date})
        sgp = timezone('Asia/Singapore')
        errors=[]
        try:
            for movie in movie_data:
                print(movie['hall'], movie['movie'],movie['time'],'done\n')
                all_seats=[]
                try:
                    headers=rheaders.rand_headers()
                except:
                    headers=rheaders.back_up_headers()
                req_seat_data=requests.get('https://www.shaw.sg/api/SeatingStatuses?recordcode={}'.format(movie['session_code']),headers=headers)
                val=(random.randint(0, 100))
                tm.sleep(0.2 + (val/100 * (0.3)))
                req_seat_data=req_seat_data.json()
                for seat in (req_seat_data['Items']):
                    if(seat['element_category_code']=='SEAT'):
                        seat_data={}
                        seat_data['seat_number']=seat['element_seat_name']
                        seat_data['seat_status']=seat['element_status_code']
                        seat_data['seat_buy_time']=seat['element_updated_on']
                        seat_data['seat_sold_by']=seat['element_updated_by']
                        seat_data['last_update_time']=str(datetime.now(sgp))
                        all_seats.append(seat_data)
                all_seats=sorted(all_seats, key = lambda k: k['seat_buy_time'])        
                mycol.update_one({ 
                                 'theatre' : movie['theatre'],
                                 'hall': movie['hall'],
                                 'session_code': movie['session_code']
                                 },
                    {'$set':{'seats':all_seats}}, 
                    upsert = True 
                    )
        except Exception:
            traceback.print_exc() 
            errors.append([movie['hall'],movie['date'], movie['movie'],movie['time']])      
        print('Finished scraping seat details')
        print('Errors:\n', errors)

            
            
scr=shaw_scraper()


