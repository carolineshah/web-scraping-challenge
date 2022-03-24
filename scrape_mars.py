from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # scrape the Mars News Site and collect the latest News Title and Paragraph Text
    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # visit featured space image site
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # find the image url for the current Featured Mars Image
    relative_image_url = soup.find('img', class_='headerimage')["src"]
    featured_image_url = url + relative_image_url

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    mars_table = pd.read_html('https://galaxyfacts-mars.com', header=0)
    mars_df = mars_table[0]
    mars_html = mars_df.to_html()

    # Visit the astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # create list of dictionaries for url and img info
    hemisphere_image_urls = []
    image_infos = soup.find_all('div', class_='item')
    for image in image_infos:
        title = image.h3.text
        rel_image_url = image.find('img', class_='thumb')['src']
        image_url = url + rel_image_url
        hemisphere_dict = {"title": title, "img_url": image_url}
        hemisphere_image_urls.append(hemisphere_dict)

    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": featured_image_url,
        "mars_html": mars_html,
        "hemisphere_list_dict": hemisphere_image_urls
    }
    # Close the browser
    browser.quit()

    return(mars_dict)

