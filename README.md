# Shaw Scraper
A web scraper built to scrape movie and seat buying data from [Shaw Theatres](https://www.shaw.sg/)' website to understand movie-goers' behaviouristic patterns.  

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
  - Create a free MongoDB account 
  - Create a database in MongoDB named "shaw_data" and a collection inside it called "movie_data". You can have different names for the database and collection but you must update the Shaw_scraper.py file accordingly.
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
3. Add the Buildpacks necessary for Selenium ChromeDriver
```
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-python.git

heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver

heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-google-chrome
```
4. Add the PATH variable to the Heroku configuration
```
heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome

heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver

heroku config:set MONGODB_URL=<your_MongoDB_connection_string>
```
5. Deploy to Heroku (Make sure that you navigate to the cloned folder before deploying)
```
git push heroku master
```
6. Run the following command to start the scraper
```
heroku ps:scale clock=1
```

## Usage
- The scraper has 2 functions for obtaining movie data and seat data. 
- The data will be stored in JSON format in the MongoDB database and will be scraped at the times specified in clock.py. Edit clock.py to chnage the scrape times.




## Team
* [Noel Mathew Isaac](https://github.com/noelmathewisaac)
* [Vanshiqa Agrawal](https://github.com/vanshiqa)

## Disclaimer
This scraper was made as a project to analyse cinema seat patterns. We are in no way affiliated with [Shaw Theatres](https://www.shaw.sg/) and are not responsible for the accuracy of the data scraped using this scraper. The scraper was developed to scrape data in Jan 2020 from the website and may not work as expected as the structure of the website may have changed since.
