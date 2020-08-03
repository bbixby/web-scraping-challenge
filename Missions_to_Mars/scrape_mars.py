from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Nasa Mars News
    news_url = 'https://mars.nasa.gov/mars2020/news/'
    # Scrape page into Soup
    news_response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'html'
    news_soup = bs(news_response.text, "html.parser")
    #define news_title and news_p to render
    news_title = news_soup.find("div", class_='listTextLabel').find('h2', class_='alt01').text.strip()
    news_p = news_soup.find("div", class_='listTextLabel').find('p').text.strip()
    # Store data in the mars_data dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p
     }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

