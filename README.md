# Shaw Scraper
A web scraper built to scrape movie and seat buying data from [Shaw Theatres](https://www.shaw.sg/)' website to understand movie-goers' behaviouristic patterns.  


<!-- GETTING STARTED -->
## Getting Started

The scraper was built to run on Heroku. The following instructions are to deploy it to heroku.

### Prerequisites

- Heroku
  - Account - Create a free account on [Heroku](https://www.heroku.com/)
  - Heroku CLI - Follow these [instructions](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) 
to download and install the heroku CLI

- MongoDB Atlas account
  Create a free MongoDB account and get the connection string which is in this format
  ```
  mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
  ```


### Installation

1. Clone the repo and navigate to it 
```
https://github.com/PopcornData/shaw-scraper.git
```
2. Open your Heroku CLI and login to Heroku
```
heroku login
```
3. Create a new project
```
heroku create <project-name>
```
3. Add the Buildpacks necessary for Selenium ChromeDriver
```
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
```
4. Add the PATH variable to the Heroku configuration
```
heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome
heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver
heroku config:set MONGODB_URL = <your_MongoDB_connection_string>
```
5. Deploy to Heroku(Make sure that you navigate to the cloned folder)
```
git push heroku master
```


## Built With
- [Selenium](https://www.selenium.dev/) 
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
&nbsp;

## Team
* [Noel Mathew Isaac](https://github.com/noelmathewisaac)
* [Vanshiqa Agrawal](https://github.com/vanshiqa)

## Disclaimer
This scraper was made as a project to analyse cinema seat patterns. We are in no way affiliated with [Shaw Theatres](https://www.shaw.sg/) and are not responsible for the accuracy of the data scraped using this scraper. The scraper was developed to scrape data in Jan 2020 from the website and may not work as expected as the structure of the website may have changed since.
