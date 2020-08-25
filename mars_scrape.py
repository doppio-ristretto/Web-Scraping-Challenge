import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser




def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)




def scrape():
    browser=init_browser()
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')





    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text




    
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)





    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)





    browser.click_link_by_partial_text('more info')





    html = browser.html
    image_soup = bs(html, 'html.parser')




    
    
    featured_image_half = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://jpl.nasa.gov" + featured_image_half





    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)





    html=browser.html
    table = pd.read_html(facts_url)
    mars_facts = table[2]





    mars_facts.columns = ['Description','Value']



    mars_facts.set_index('Description')




    mars_table = mars_facts.to_html()
    mars_table.replace('\n', '')




    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)





    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    pic_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'


    for item in items: 

        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        pic_urls.append({"title" : title, "img_url" : img_url})
    

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": str(mars_table),
        "pic_urls": pic_urls
    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()



