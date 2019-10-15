
#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#Site Navigation
def init_browser():
    executable_path = {"executable_path": "C:\\Users\\taiwo\\Downloads\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
# Defining scrape & dictionary
def scrape():
    browser = init_browser()
    listings = {}
    listings["mars_news"] = mars_news()
    listings["mars_image"] = marsImage()
    listings["mars_weather"] = marsWeather()
    listings["mars_facts"] = marsFacts()
    listings["mars_hemisphere"] = marsHem()
    return listings


# # NASA Mars News
def mars_news():
   news_url = "https://mars.nasa.gov/news/"
   browser.visit(news_url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   news = soup.find("div", class_="list_text")
   news_date = news.find("div", class_="list_date").text
   news_paragraph = news.find("div", class_="article_teaser_body").text
   news_title = news.find("div", class_="content_title").text

   mars_news = [news_title, news_paragraph]
   return mars_news



# # JPL Mars Space Images - Featured Image
def marsImage():
   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   image = (link.get('data-fancybox-href'))
   featured_image_url = "https://www.jpl.nasa.gov" + image
   return featured_image_url


# # Mars Weather
def marsWeather():
   url = "https://twitter.com/marswxreport?lang=en"
   browser.visit(url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   mars_weather = soup.find("div",{"class":"js-tweet-text-container"})
   mars_weather = mars_weather.text.strip()
   mars_weather
   return mars_weather

# # Mars Facts
def marsFacts():
   import pandas as pd
   from IPython.display import HTML
   facts_url = "https://space-facts.com/mars/"
   browser.visit(facts_url)
   mars_data = pd.read_html(facts_url)
   mars_data = pd.DataFrame(mars_data[0])
   mars_data.columns = ["Mars-Earth Comparison", "Mars", "Earth"]
   mars_data = mars_data.set_index("Mars-Earth Comparison")
   mars_facts = mars_data.to_html(index = True, header =True)
   return mars_facts

# # Mars Hemispheres
def marsHem():
   import time
   hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   browser.visit(hemispheres_url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   mars_hemisphere = []
   products = soup.find("div", class_ = "result-list" )
   hemispheres = products.find_all("div", class_="item")
   for hemisphere in hemispheres:
       title = hemisphere.find("h3").text
       title = title.replace("Enhanced", "")
       end_link = hemisphere.find("a")["href"]
       image_link = "https://astrogeology.usgs.gov/" + end_link
       browser.visit(image_link)
       html = browser.html
       soup=BeautifulSoup(html, "html.parser")
       downloads = soup.find("div", class_="downloads")
       image_url = downloads.find("a")["href"]
       dictionary = {"title": title, "img_url": image_url}
       mars_hemisphere.append(dictionary)
   return mars_hemisphere