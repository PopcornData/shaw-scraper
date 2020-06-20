# Shaw Scraper

A web scraper built to scrape movie and seat buying data from [Shaw Theatres](https://www.shaw.sg/)' website to understand movie-goers' behaviouristic patterns. The data was used to build intersting visualisations which can be found on the [PopcornData website](https://popcorn-data.herokuapp.com/). More details on how we obtained the data and cleaned it can be found in this [Medium article](https://towardsdatascience.com/popcorn-data-analysing-cinema-seating-patterns-part-1-a0b2a5c2c19a).

## Data Collected 
#### Raw Data  
The complete raw data collected can be found [here](https://drive.google.com/file/d/1K7Vv88SnmWarf6rOre2ijA-Qq7Dv2sNp/view).  

#### Cleaned Data  
The processed data can be found [here](https://docs.google.com/spreadsheets/d/1pLNbwfnrmfpyA7sxtRyB1P6iHuSFyUPEerwW7f3fEWU/edit?usp=sharing).


## Built With
- [Selenium](https://www.selenium.dev/) 
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)



## Getting Started

The scraper was built to run on Heroku. The following instructions are to deploy it on Heroku.

### Prerequisites

- Heroku
  - Account - Create a free account on [Heroku](https://www.heroku.com/)
  - Heroku CLI - Follow these [instructions](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) 
to download and install the Heroku CLI

- MongoDB Atlas account
  - Create a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account 
  - Create a database in MongoDB named "shaw_data" and a collection inside it called "movie_data". You can have different names for the database and collection but you must update the Shaw_scraper.py file accordingly.
  - Add 0.0.0.0/0 (i.e. all addresses) to your MongoDB Atlas [whitelist](https://docs.atlas.mongodb.com/tutorial/whitelist-connection-ip-address/)
  - Get the database [connection string](https://docs.mongodb.com/manual/reference/connection-string/) which is in this format:
  ```
  mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
  ```


### Installation

1. Clone the repo and navigate to the correct folder 
```
git clone https://github.com/PopcornData/shaw-scraper.git
```
2. Open your Heroku CLI and login to Heroku
```
heroku login
```
3. Create a new project on Heroku
```
heroku create <project-name>
```
4. Add the remote
```
heroku git:remote -a <project-name>
```
5. Add the Buildpacks necessary for Selenium ChromeDriver
```
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-python.git

heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver

heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-google-chrome
```
6. Add the PATH variable to the Heroku configuration
```
heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome

heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver

heroku config:set MONGODB_URL=<your-MongoDB-connection-string>
```
7. Deploy to Heroku (Make sure that you navigate to the cloned folder before deploying)
```
git push heroku master
```
8. Run the following command to start the scraper
```
heroku ps:scale clock=1
```

## Usage
The scraper has 2 functions which run separately:
   1. **get_movie_data()** - This function scrapes the movie details from all the theatres for the given day and stores the JSON data in the DB. The data has the folowing format:
   ```
   {
     "theatre":"Nex",
     "hall":"nex Hall 5",
     "movie":"Jumanji: The Next Level",
     "date":"18 Jan 2020",
     "time":"1:00 PM+",
     "session_code":"P00000000000000000200104"
   }
   ```
   2. **get_seat_data()** - This function scrapes the seat details including which seats where bought and the time at which seats where bought for movie sessions. It scrapes data from the previous day so that all the seat data (ticket sales) are updated. It should be run only after running the get_movie_data() function as it updates the JSON in the DB by adding the seat data to it. The updated data has the following format:
   ```
   {
       "theatre":"Nex",
       "hall":"nex Hall 5",
       "movie":"Jumanji: The Next Level",
       "date":"18 Jan 2020",
       "time":"1:00 PM+",
       "session_code":"P00000000000000000200104"
       "seats":[
           {   
             "seat_status":"AV",
             "last_update_time":"2020-01-20 14:34:53.704117",
             "seat_buy_time":"1900-01-01T00:00:00",
             "seat_number":"I15",
             "seat_sold_by":""
           },
           ...,
           {  
             "seat_status":"SO",
             "last_update_time":"2020-01-20 14:34:53.705116",
             "seat_buy_time":"2020-01-18T13:12:34.193",
             "seat_number":"F6",
             "seat_sold_by":""
           }
        ]
  }
   ```
A full sample updated document in the database can be viewed [here](https://gist.github.com/noelmathewisaac/31a9d20a674f6dd8524ed89d65183279)
   
**The functions are scheduled to run daily at the times specified in clock.py. The timings and frequencies of the scraper can be changed by editing the clock.py file.**

## License
Distributed under the MIT License. See ```LICENSE``` for more information.


## Team
* [Noel Mathew Isaac](https://github.com/noelmathewisaac)
* [Vanshiqa Agrawal](https://github.com/vanshiqa)

## Disclaimer
This scraper was made as a project to analyse cinema seat patterns. We are in no way affiliated with [Shaw Theatres](https://www.shaw.sg/) and are not responsible for the accuracy of the data scraped using this scraper. The scraper was developed to scrape data in **Jan 2020** from the website and was functional as of **June 2020**. It may not work as expected as the structure of the website may have changed since.
