from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #windows work-around for chromedriver.exe 'e' error
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


    #get headline image
    sleep(1)
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')
    imgs = img_soup.find(class_ = "carousel_item")['style']
    featured_image = imgs.split("'")[1]
    img_base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = img_base_url + featured_image

    mars_data.update( {'featured_image_url' : featured_image_url} )

    #get the Mars Facts and nothing but the facts
    sleep(1)
    facts_url = 'https://space-facts.com/mars/'
    facts_url_tables = pd.read_html(facts_url)
    mars_facts_df = facts_url_tables[0]
    mars_facts_df.columns = ['Label', 'Value']
    mars_facts_df.set_index('Label', inplace=True)
    html_table = mars_facts_df.to_html()

    mars_data.update( {'html_table' : html_table} )

    #get Mars Hemisphere images
    sleep(1)
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")
    hemi_links = hemi_soup.find_all("div", class_ = "item")

    hemi_img_urls = []

    for link in hemi_links:
        #dictionary to hold the name/link pairs
        hemi_dict = {}
        #name is in the h3 text
        img_name = link.find("h3").text
        #link is in each desctiption, a href
        img_link = link.find("div", class_ = "description").a["href"]
        #add the base url
        link_base = "https://astrogeology.usgs.gov"
        visit_link = link_base + img_link
    
        #visit the link
        browser.visit(visit_link)
        #don't go too fast
        time.sleep(5)
    
        #parse the html
        indv_hemi_html = browser.html
        indv_hemi_soup = bs(indv_hemi_html, 'html.parser')
    
        #grab the full image link from wide-image src
        indv_hemi_url = indv_hemi_soup.find("img", class_ = "wide-image")["src"]
    
        #add to dictionary as hemi_img_name, hemi_img_url
        hemi_dict['hemi_img_name'] = img_name
        hemi_dict['hemi_img_url'] = link_base + indv_hemi_url
        #put dictionary into hemi_img_urls
        hemi_img_urls.append(hemi_dict)
        browser.back()

    mars_data.update( {'hemi_img_urls': hemi_img_urls} )

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

