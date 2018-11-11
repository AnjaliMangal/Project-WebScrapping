#!/usr/bin/env python
# import all dependencies 
from bs4  import BeautifulSoup
from splinter import Browser
#import requests
import pymongo
import pandas as pd
import time 

## Big scrape function    

def scrape_data():
    print("*************** Execution started ******************************") 
    #getting browser initiated 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False) 
    
    ## 1 NASA Mars news and Title 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    soup =BeautifulSoup(browser.html,'html.parser')
    # collect the latest News Title and Paragraph
    news_title= soup.find('div',class_='content_title').text
    print(news_title)
    news_p = soup.find("div", class_='article_teaser_body').text
    print(news_p)

    #  2 JPL Mars Space Image 
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.find_by_id("full_image").click()
    ## need to wait a bit
    time.sleep(5)
    soup =BeautifulSoup(browser.html,'html.parser')
    image_name = soup.find('img',class_='fancybox-image')['src']
    print(image_name)
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url+image_name
    print(featured_image_url)


    ##  3 Mars Weather from twitter
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    ## need to wait a bit
    time.sleep(2)
    soup =BeautifulSoup(browser.html,'html.parser')
    mars_weather = soup.find('p',class_='TweetTextSize').text
    print(mars_weather)
    
     
    ### 4 Mars Facts
    mars_fact_url ='http://space-facts.com/mars/'
    tables = pd.read_html(mars_fact_url)
    print(tables)
    df_facts = tables[0]
    print(df_facts)
    df_facts.columns  = ['facts','values']
    df_facts.set_index('facts',inplace=True)
    # Converting to html
    facts_html = "".join(df_facts.to_html().split("\n"))


    ####  5 Mars Hemispheres Info
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    time.sleep(2)
    soup =BeautifulSoup(browser.html,'html.parser')
    hemispeher_images_list = []
    results = soup.find_all('a',class_='itemLink product-item')
    for result in results:       
        dict ={}
        if(result.find('h3')):
            title = result.find('h3').text
            print(title)
            img_url = "https://astrogeology.usgs.gov" + result['href']
            browser.visit(img_url)
            time.sleep(2)
            img_link = browser.find_by_text('Sample')['href']
            print(img_link)
            browser.back()
            dict= {
            'title': title,
            'img_url': img_link    
            } 
        else :
            continue    
        hemispeher_images_list.append(dict)
    print("Final list of dict")    
    print(hemispeher_images_list)
    browser.quit()

    ## Prepare a final dictionary of all Mars scraped data 
    mars_data ={
        'news_title': news_title,
        'news_p': news_p,
        'mars_image': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': facts_html ,
        'mars_hemi_data' : hemispeher_images_list
    }
    print("*************** This is  final Mars scraped data *****************")
    print(mars_data)
    return mars_data
    

print("*************** Execution started ******************************")    
#data = scrape_data()    
print("*************** This is  final Mars scraped data *****************")
#print(data)






