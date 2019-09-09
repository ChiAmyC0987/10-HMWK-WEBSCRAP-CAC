#!/usr/bin/env python
# coding: utf-8

# ## Step 1 - Scraping
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# * Create a Jupyter Notebook file called `mission_to_mars.ipynb` and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

# In[1]:


# Dependencies
import pymongo
import datetime
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd


# In[2]:


# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


# Declare the database
db = client.nasa_db

# Declare the collection
collection = db.nasa_db


# ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."

# In[4]:


# Splinter access browser and Chrome opens web site
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[5]:


# Open NASA Mars website
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[8]:


# Examine the results using chrome dev tools; then determine elements with title and article info
html = browser.html
soup = bs(html, 'html.parser')


# In[9]:


# Scrapping begines here with Beautiful Soup

# results are returned as an iterable list 
results = soup.find_all('li', class_='slide')

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        news_t = result.find('div', class_='content_title')
        news_title = news_t.text.strip()
        
        news_p1 = result.find('div', class_='article_teaser_body')
        news_p = news_p1.text.strip()

        post = {
    'title': 'news_title',
    'teaser': 'news_p',
} 

# Run only if title, paragraph are avilable
        if (news_title and news_p):
            # Print results
            print('-------------')
            print('title: ', news_title)
            print('article: ', news_p)
      
        collection.insert_one(post) # put information into mongodb.  article = record and collection = table

    except Exception as e:
        print(e)
        
# Click the 'article title' button on each page
try:
    browser.click_link_by_partial_text('article_title')   
except:
    print('-------------')
    print("Scraping Complete")        


# 
# ### JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# * Make sure to find the image url to the full size `.jpg` image.
# 
# * Make sure to save a complete url string for this image.
# 
# ```python
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# ```

# In[10]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[11]:


# Capture the new html from the new page
img_html = browser.html

# Create and feed a new scraper the new html
img_scraper = bs(img_html, 'html.parser')


# In[12]:


# Go to next image page by clicking on the "full image" button
full_img = img_scraper.find('a', {'class': 'button fancybox'})
full_img


# In[13]:


# Click the 'FULL IMAGE' button
browser.click_link_by_partial_text('FULL IMAGE')


# In[14]:


# Click the 'more info' button
browser.click_link_by_partial_text('more info')


# In[15]:


# Scrape the image from the img element
mars_html = browser.html

mars_scraper = bs(mars_html, 'html.parser')

mars_img = mars_scraper.find('img', {'class': 'main_image'})
mars_img


# In[16]:


featured_image_url = mars_img.get('src')
print("https://www.jpl.nasa.gov",featured_image_url)


# 
# ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

# In[17]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[18]:


# Examine the results, then determine element that contains sought info
html = browser.html
# response = requests.get(url)
# soup = bs(response.text, 'lxml')
soup = bs(html, 'html.parser')


# In[19]:


results = soup.find_all('p', class_='TweetTextSize')


# In[20]:


# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        report = result.text.strip()
        print('weather report: ', report)
        print('---------------')
     
        post = {
    'weather report': 'report',
} 

# Run only if title, paragraph are avilable
        if (report):
            # Print results
            print('-------------')
            print('weather report: ', report)
    
        collection.insert_one(post) # put information into mongodb.  article = record and collection = table

    except Exception as e:
        print(e)


# ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.
# 

# In[21]:


url = 'https://space-facts.com/mars/'


# In[22]:


# Used class example 09-panda scraping
tables = pd.read_html(url)
tables


# In[23]:


# table first element
df = tables[0]
df.columns = ['Comparision', 'Mars', 'Earth']
df


# In[24]:


# table second element
df = tables[1]
df.columns = ['Fun Facts', 'Mars']
df


# ### Mars Hemispheres
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# ```
# 
# - - -
# 

# In[26]:


url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_usgs)


# In[27]:


#  following code was borrowed from TA example


# In[28]:


# Scrap 4 images
urls = [
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
    'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
]

# create empty dictionary to collect images
image_data = []


# In[27]:


# for loop through m_urls list and perform some web scraping logic for each link
for url in urls:
    print(url)

    # create empty dictionary
    album = {}
    
    # click link
    browser.visit(url)
    
    # Scrape the image from the img element
    m_html = browser.html
    m_scraper = bs(m_html, 'html.parser')
    
    # scrape the title and image url
    m_title = m_scraper.find('h2', {'class': 'title'}).get_text()
    
    # add title to album
    album['title'] = m_title
  
    # add image to album
    image_data.append(album)
    
    # repeat scraping and extracting steps for image src ------------need to create my code 
    # jpl_image_url = jpl_image.get('src')
    # jpl_image_url

    # go back a page in the browser
    browser.back()


# In[28]:


image_data


# In[29]:


# close brower and start step 2
browser.quit()


# ## Step 2 - MongoDB and Flask Application
# 
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# 
#   * Store the return value in Mongo as a Python dictionary.
# 
# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.
# 
# ![final_app_part1.png](Images/final_app_part1.png)
# ![final_app_part2.png](Images/final_app_part2.png)
# 
# - - -

# In[ ]:





# ## Step 3 - Submission
# 
# To submit your work to BootCampSpot, create a new GitHub repository and upload the following:
# 
# 1. The Jupyter Notebook containing the scraping code used.
# 
# 2. Screenshots of your final application.
# 
# 3. Submit the link to your new repository to BootCampSpot.
