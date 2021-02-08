


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Import ChromeDrriver
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

## JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

## D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# First, get a list of all of the hemispheres
# First, get a list of all of the hemispheres
html = browser.html
mars_hemispheres = soup(html, 'html.parser')

mars_images = mars_hemispheres.find_all('div', class_='item')

# Next, loop through those links, click the link, find the sample anchor, return the href
for image in mars_images:
    url = image.find("a")['href']
    browser.visit(base_url+url)
    
    # parse the hemi page
    hemi_item_html = browser.html
    hemi_soup = soup(hemi_item_html, 'html.parser')
    
    # Get the title for Hemisphere
    title = hemi_soup.find('h2', class_ = 'title').text
    
    # Get URL and Jpeg image
    downloads = hemi_soup.find('div', class_ = 'downloads')
    image_url = downloads.find('a')['href']

    # Append hemisphere object to list
    hemisphere_image_urls.append({"title": title, "img_url": image_url})
    
   

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()





