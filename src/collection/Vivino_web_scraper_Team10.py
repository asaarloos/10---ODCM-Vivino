#!/usr/bin/env python
# coding: utf-8

# Team Project ODCM - Team 10

## Project 
#This document contains the code  to scrape data from Vivino. The extracted data could be used to analyse the influence of the price of wine on consumer ratings. The Vivino website offers over millions of different wines. The sample we are going to scrape consists of all wines originated in Spain and that are deliverable to the Netherlands. At 05-10-2024, this leaves a sample of 8,079 wines (this number could change over time). Of these wines, the following data will be extracted:
#- **Hyperlink**: The hyperlink of each wine, which includes the unique id of each wine. The unique wine id will later be isolated when cleaning the data.
#- **Brand**: The brand that produces the wine.
#- **Wine**: The name of the specific wine.
#- **Rating**: The rating of the specific wine (0-5).
#- **Price**: The price of the specific wine. When the wine is on discount, the original price will be taken, not the discounted price.
#- **Timestamp**: The timestamp at which the data is extracted. This will be useful in future analyses, so the date and time of extraction can always be found.

### Code
#The code will be run individually for each type of wine: red, white, rose, sparkling, dessert and fortified. After the code of each type is run, a dataset will be created containing all wines of that type. Later, when cleaning the data, each dataset will get identified by adding an extra column with the wine category. Then, all datasets will be merged into one dataset containing all 8,057 wines. This dataset will be further cleaned and after removing duplicate wines, it will producte a final dataset with 7,585 wines.

#We created a makefile to automate this process. When running the makefile, it will first run this webscraping code, creating seperate datasets per type of wine. Then, the datasets will be merged into one csv file, which will then be cleaned and several summary statistics will be calculated and plots will be created. The individual files for each category created by the web scraper will be deleted.

# ### Install the packages & librabies 
# 
# To extract the data, we make use of Beautiful Soup and Selenium. In order to run the code, first install and import the packages below:

# In[15]:


#installing packages
# get_ipython().system('pip3 install selenium')
# get_ipython().system('pip3 install webdriver_manager')
# get_ipython().system('pip3 install beautifulsoup4')

#libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import csv


# ## Red Wines 
# 
# In the cell below the data of the red wines are collected. To ensure that the code doesn't break, we filter the wines to create separate extraction batches, each with their own URL. These urls are then, one by one, fed into the code using a for loop. After scraping, the data will be appended to a csv file named 'red_wine.csv' in the data folder.

# In[5]:


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls = ('https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NFBLrrT181FLtnUNDVIrAEqmp9mWJRZlppYk5qjlF6XYpqQWJ6vlJ1XaFhRlJqeqlZdExwJVJVcWA-nUYjUwCQC3hRy5', # 0-10 euro
      'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1NFDLTaywNTJQS6609fNRS7Z1DQ1SKwDKpqfZliUWZaaWJOao5Rel2KakFier5SdV2hYUZSanqpWXRMcCVSVXFgPp1GI1MAkAya8c6w%3D%3D', # 10-20 euro
      'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1MlDLTaywNTFQS6609fNRS7Z1DQ1SKwDKpqfZliUWZaaWJOao5Rel2KakFier5SdV2hYUZSanqpWXRMcCVSVXFgPp1GI1MAkAyosc7g%3D%3D', # 20-40 euro
      'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1MVDLTaywNTUwUEuutPXzUUu2dQ0NUisASqen2ZYlFmWmliTmqOUXpdimpBYnq-UnVdoWFGUmp6qVl0THAlUlVxYD6dRiNTAJAN31HSE%3D') # 40-500 euro

# Open a csv file to store the data in
with open('../../data/red_wine.csv', mode='w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)

      # Write the header row
      writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

for url in urls:
      driver.get(url)
      driver.maximize_window()

      # Optional: Adding some wait time for the page to fully load if needed
      driver.implicitly_wait(20)

      # Create a function to click away the cookies
      try:
            accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
            accept_cookies_button.click()
            print("Cookies accepted.")
      except Exception as e:
            print("Cookie acceptance button not found or could not be clicked:")

      # Infinite scroll to load more content
      scroll_pause_time = 2 # Adjust if necessary
      last_height = driver.execute_script("return document.body.scrollHeight")

      while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
            # Wait for the new page to load
            time.sleep(scroll_pause_time)
    
            # Calculate new scroll height and compare with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                  time.sleep(scroll_pause_time) # Wait for the potentially new content to load
                  new_height = driver.execute_script("return document.body.scrollHeight") # Try scroling once more
                  if new_height == last_height:
                        break  # Stop if we've reached the end of the page
            last_height = new_height

      # Get the final page source after all content is loaded
      page_source = driver.page_source

      # Parse the page source with BeautifulSoup
      soup = BeautifulSoup(page_source, 'html.parser')

      # Create empty lists to store the data
      hyperlink = []
      brands = []
      wines = []
      ratings = []
      reviews = []
      prices = []
      timestamp = []

      # Find all wine entries on the page
      wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

      for entry in wine_entries:

            # Extract hyperlink
            link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
            if link_tag and link_tag.has_attr('href'):
                  hyperlink.append(link_tag['href'])

            # Extract brand
            brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
            if brand:
                  brands.append(brand.get_text(strip=True))

            # Extract wine name
            wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
            if wine:
                  wines.append(wine.get_text(strip=True))

            # Extract rating
            rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
            if rating:
                  ratings.append(rating.get_text(strip=True))
            # Extract review count
            review = entry.find(class_='vivinoRating_caption__xL84P')
            if review:
                  # Get only the first part so the word 'beoordelingen' is not scraped
                  review_text = review.get_text(strip=True)
                  review_count = review_text.split()[0]
                  reviews.append(review_count)
            
            # Check for the presence of the discount first
            discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
            if discount_price_div:
                  # If discount exist, get the original price
                  discount_price_text = discount_price_div.get_text(strip=True)
                  price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
                  prices.append(price_only)  # Append only the discount price to the list
    
            else:  
                  # Extract currency & price if present in the addToCartButton
                  price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
                  if price_divs:  # If primary price class exists
                        for price_div in price_divs:
                              currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                              price = price_div.find_all('div')[1]  # Assuming price is in the second div
                              full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                              prices.append(full_price)  # Save the full price
                  else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
                        alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
                        if alt_price_div:
                              alt_price_text = alt_price_div.get_text(strip=True)
                              price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                              prices.append(price_only)  # Append only the price to the list
            
            # Extract timestamp
            timestamps = time.time()
            timestamp.append(timestamps)

            # Wait for 2 seconds to not overload the server
            time.sleep(2)

      # Open a csv file to store the data in
      with open('../../data/red_wine.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the data rows
            for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink,brands, wines, ratings, reviews, prices, timestamp):
                  writer.writerow([
                        hyperlink,
                        brand,
                        wine,
                        rating,
                        reviews,
                        price,
                        timestamp 
                  ])
      
      print("Data saved to 'red_wine.csv' successfully.")


# ## White Wines
# 
# In the cell below the data of the white wines are collected. To ensure that the code doesn't break, we filter the wines to create separate extraction batches, each with their own URL. These urls are then, one by one, fed into the code using a for loop. After scraping, the data will be appended to a csv file named 'white_wine.csv' in the data folder.

# In[6]:


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls = ('https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1MlBLrrT181FLtnUNDVIrAEqmp9mWJRZlppYk5qjlF6XYJhYnq-UnVdoWFGUmp6qVl0TH2hoBNRUD6dRiNTAJAJlRHFM%3D', # 0-20 euro
        'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1MlDLTaywNTUwUEuutPXzUUu2dQ0NUisASqen2ZYlFmWmliTmqOUXpdgmFier5SdV2hYUZSanqpWXRMfaGgE1FQPp1GI1MAkAvnccuA%3D%3D') # 20-500 euro

# Open a csv file to store the data in
with open('../../data/white_wine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

for url in urls:
    driver.get(url)
    driver.maximize_window()

    # Optional: Adding some wait time for the page to fully load if needed
    driver.implicitly_wait(20)

    # Create a function to click away the cookies
    try:
        accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
        accept_cookies_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("Cookie acceptance button not found or could not be clicked:")

    # Infinite scroll to load more content
    scroll_pause_time = 2 # Adjust if necessary
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait for the new page to load
        time.sleep(scroll_pause_time)
    
        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(scroll_pause_time) # Wait for the potentially new content to load
            new_height = driver.execute_script("return document.body.scrollHeight") # Try scroling once more
            if new_height == last_height:
                break  # Stop if we've reached the end of the page
        last_height = new_height

    # Get the final page source after all content is loaded
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Create empty lists to store the data
    hyperlink = []
    brands = []
    wines = []
    ratings = []
    reviews = []
    prices = []
    timestamp = []

    # Find all wine entries on the page
    wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

    for entry in wine_entries:

        # Extract hyperlink
        link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
        if link_tag and link_tag.has_attr('href'):
            hyperlink.append(link_tag['href'])

        # Extract brand
        brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
        if brand:
            brands.append(brand.get_text(strip=True))

        # Extract wine name
        wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
        if wine:
            wines.append(wine.get_text(strip=True))

        # Extract rating
        rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
        if rating:
            ratings.append(rating.get_text(strip=True))
        # Extract review count
        review = entry.find(class_='vivinoRating_caption__xL84P')
        if review:
            # Get only the first part so the word 'beoordelingen' is not scraped
            review_text = review.get_text(strip=True)
            review_count = review_text.split()[0]
            reviews.append(review_count)
            
        # Check for the presence of the discount first
        discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
        if discount_price_div:
            # If discount exist, get the original price
            discount_price_text = discount_price_div.get_text(strip=True)
            price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
            prices.append(price_only)  # Append only the discount price to the list
    
        else:  
            # Extract currency & price if present in the addToCartButton
            price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
            if price_divs:  # If primary price class exists
                for price_div in price_divs:
                    currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                    price = price_div.find_all('div')[1]  # Assuming price is in the second div
                    full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                    prices.append(full_price)  # Save the full price
            else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
                alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
                if alt_price_div:
                    alt_price_text = alt_price_div.get_text(strip=True)
                    price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                    prices.append(price_only)  # Append only the price to the list
            
        # Extract timestamp
        timestamps = time.time()
        timestamp.append(timestamps)
        
        # Wait for 2 seconds to not overload the server
        time.sleep(2)

    # Open a csv file to store the data in
    with open('../../data/white_wine.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the data rows
        for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink,brands, wines, ratings, reviews, prices, timestamp):
            writer.writerow([
                hyperlink,
                brand,
                wine,
                rating,
                reviews,
                price,
                timestamp 
            ])
      
    print("Data saved to 'white_wine.csv' successfully.")


# ## Rose Wines
# 
# In the cell below we are collecting the data of the rose wines. Since the number of rose wines is limited, it is not necessary to seperate the wines into seperate urls. Therefore, the code is only run once to extract the full set of rose wines. After scraping, the data will be appended to a csv file named 'rose_wine.csv' in the data folder.
# In[7]:

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Opening the 'Vivino' website
url = 'https://www.vivino.com/explore?e=eJwdi70KgCAABt_mmw1q_Ma2aAiaIsLMQkgNtb-3T1ruhuNsYAFrHAWsfFgJAfWybaBY9x2OXLeVlwxGJ7nDh4WLjgp-fhlkMm6Lk_KnS7jTMLLMd8zWET8_0d4gXQ%3D%3D'
driver.get(url)
driver.maximize_window()

# Optional: Adding some wait time for the page to fully load if needed
driver.implicitly_wait(20)  # 20 seconds 

 # Create a function to click away the cookies
try:
    accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookies_button.click()
    print("Cookies accepted.")
except Exception as e:
    print("Cookie acceptance button not found or could not be clicked:")

# Infinite scroll to load more content
scroll_pause_time = 2  # Adjust if necessary
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for the new page to load
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(scroll_pause_time)  # Wait for the potentially new content to load
        break  # Stop if we've reached the end of the page
    last_height = new_height

# Get the final page source after all content is loaded
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Create empty lists to store the data
hyperlink = []
brands = []
wines = []
ratings = []
reviews = []
prices = []
timestamp = []

# Find all wine entries on the page
wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

for entry in wine_entries:

    link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
    if link_tag and link_tag.has_attr('href'):
        hyperlink.append(link_tag['href'])

    # Extract brand
    brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
    if brand:
        brands.append(brand.get_text(strip=True))

    # Extract wine name
    wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
    if wine:
        wines.append(wine.get_text(strip=True))

    # Extract rating
    rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
    if rating:
        ratings.append(rating.get_text(strip=True))
    
    # Extract review count
    review = entry.find(class_='vivinoRating_caption__xL84P')
    if review:
       # Get only the first part so the word 'beoordelingen' is not scraped
        review_text = review.get_text(strip=True)
        review_count = review_text.split()[0]
        reviews.append(review_count)

    # Check for the presence of the discount first
    discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
    if discount_price_div:
        # If discount exist, get the original price
        discount_price_text = discount_price_div.get_text(strip=True)
        price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
        prices.append(price_only)  # Append only the discount price to the list
    
    else:  
        # Extract currency & price if present in the addToCartButton
        price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
        if price_divs:  # If primary price class exists
            for price_div in price_divs:
                currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                price = price_div.find_all('div')[1]  # Assuming price is in the second div
                full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                prices.append(full_price)  # Save the full price
        else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
            alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
            if alt_price_div:
                alt_price_text = alt_price_div.get_text(strip=True)
                price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                prices.append(price_only)  # Append only the price to the list
                
    timestamps = time.time()
    timestamp.append(timestamps)

    # Wait for 2 seconds to not overload the server
    time.sleep(2)

# Open csv file to store the data
with open('../../data/rose_wine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

    # Write the data rows
    for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink, brands, wines, ratings, reviews, prices, timestamp):
        writer.writerow([
            hyperlink,
            brand,
            wine,
            rating,
            reviews,
            price,
            timestamp
        ])

print("Data saved to 'rose_wine.csv' successfully.")


# ## Sparkling Wines
# 
# In the cell below we are collecting the data of the sparkling wines. Since the number of sparkling wines is limited, it is not necessary to seperate the wines into seperate urls. Therefore, the code is only run once with the full set of sparkling wines. After scraping, the data will be appended to a csv file named 'sparkling_wine.csv' in the data folder.

# In[8]:


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Opening the 'Vivino' website
url = 'https://www.vivino.com/explore?e=eJwdi70KgCAABt_mm41o_Ma2aAiaIsLMQkgNtb-3T1ruhuNsYAFrHAWsfFgJAfWybaBY9x2OXLeVlwxGJ7nDh4WLjgp-fhlkMm6Lk_KnS7jTMLLMd8zWET8_0c4gXA%3D%3D'
driver.get(url)
driver.maximize_window()

# Optional: Adding some wait time for the page to fully load if needed
driver.implicitly_wait(20)  # 20 seconds 

 # Create a function to click away the cookies
try:
    accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookies_button.click()
    print("Cookies accepted.")
except Exception as e:
    print("Cookie acceptance button not found or could not be clicked:")

# Infinite scroll to load more content
scroll_pause_time = 2  # Adjust if necessary
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for the new page to load
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(scroll_pause_time)  # Wait for the potentially new content to load
        break  # Stop if we've reached the end of the page
    last_height = new_height

# Get the final page source after all content is loaded
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Create empty lists to store the data
hyperlink = []
brands = []
wines = []
ratings = []
reviews = []
prices = []
timestamp = []

# Find all wine entries on the page
wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

for entry in wine_entries:

    link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
    if link_tag and link_tag.has_attr('href'):
        hyperlink.append(link_tag['href'])

    # Extract brand
    brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
    if brand:
        brands.append(brand.get_text(strip=True))

    # Extract wine name
    wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
    if wine:
        wines.append(wine.get_text(strip=True))

    # Extract rating
    rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
    if rating:
        ratings.append(rating.get_text(strip=True))
    
    # Extract review count
    review = entry.find(class_='vivinoRating_caption__xL84P')
    if review:
       # Get only the first part so the word 'beoordelingen' is not scraped
        review_text = review.get_text(strip=True)
        review_count = review_text.split()[0]
        reviews.append(review_count)

    # Check for the presence of the discount first
    discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
    if discount_price_div:
        # If discount exist, get the original price
        discount_price_text = discount_price_div.get_text(strip=True)
        price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
        prices.append(price_only)  # Append only the discount price to the list
    
    else:  
        # Extract currency & price if present in the addToCartButton
        price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
        if price_divs:  # If primary price class exists
            for price_div in price_divs:
                currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                price = price_div.find_all('div')[1]  # Assuming price is in the second div
                full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                prices.append(full_price)  # Save the full price
        else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
            alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
            if alt_price_div:
                alt_price_text = alt_price_div.get_text(strip=True)
                price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                prices.append(price_only)  # Append only the price to the list
                
    timestamps = time.time()
    timestamp.append(timestamps)

    # Wait for 2 seconds to not overload the server
    time.sleep(2)

# Open csv file to store the data
with open('../../data/sparkling_wine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

    # Write the data rows
    for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink, brands, wines, ratings, reviews, prices, timestamp):
        writer.writerow([
            hyperlink,
            brand,
            wine,
            rating,
            reviews,
            price,
            timestamp
        ])

print("Data saved to 'sparkling_wine.csv' successfully.")


# ## Dessert Wines
# 
# In the cell below we are collecting the data of the dessert wines. Since the number of dessert wines is limited, it is not necessary to seperate the wines into seperate urls. Therefore, the code is only run once with the full set of dessert wines. After scraping, the data will be appended to a csv file named 'dessert_wine.csv' in the data folder.

# In[31]:


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Opening the 'Vivino' website
url = 'https://www.vivino.com/explore?e=eJwdi70KgCAABt_mm22Ipm9si4agKSLMLITUUPt7-6TlbjjOBhawxlHAyoelEFAv2waKdd_hyHVbeclgdJI7fFi46Kjg55dBJuO2OCl_uoQ7DSOrfMdsHfHzA9IOIGA%3D'
driver.get(url)
driver.maximize_window()

# Optional: Adding some wait time for the page to fully load if needed
driver.implicitly_wait(20)  # 20 seconds 

 # Create a function to click away the cookies
try:
    accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookies_button.click()
    print("Cookies accepted.")
except Exception as e:
    print("Cookie acceptance button not found or could not be clicked:")

# Infinite scroll to load more content
scroll_pause_time = 2  # Adjust if necessary
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for the new page to load
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(scroll_pause_time)  # Wait for the potentially new content to load
        break  # Stop if we've reached the end of the page
    last_height = new_height

# Get the final page source after all content is loaded
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Create empty lists to store the data
hyperlink = []
brands = []
wines = []
ratings = []
reviews = []
prices = []
timestamp = []

# Find all wine entries on the page
wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

for entry in wine_entries:

    link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
    if link_tag and link_tag.has_attr('href'):
        hyperlink.append(link_tag['href'])

    # Extract brand
    brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
    if brand:
        brands.append(brand.get_text(strip=True))

    # Extract wine name
    wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
    if wine:
        wines.append(wine.get_text(strip=True))

    # Extract rating
    rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
    if rating:
        ratings.append(rating.get_text(strip=True))
    
    # Extract review count
    review = entry.find(class_='vivinoRating_caption__xL84P')
    if review:
       # Get only the first part so the word 'beoordelingen' is not scraped
        review_text = review.get_text(strip=True)
        review_count = review_text.split()[0]
        reviews.append(review_count)

    # Check for the presence of the discount first
    discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
    if discount_price_div:
        # If discount exist, get the original price
        discount_price_text = discount_price_div.get_text(strip=True)
        price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
        prices.append(price_only)  # Append only the discount price to the list
    
    else:  
        # Extract currency & price if present in the addToCartButton
        price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
        if price_divs:  # If primary price class exists
            for price_div in price_divs:
                currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                price = price_div.find_all('div')[1]  # Assuming price is in the second div
                full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                prices.append(full_price)  # Save the full price
        else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
            alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
            if alt_price_div:
                alt_price_text = alt_price_div.get_text(strip=True)
                price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                prices.append(price_only)  # Append only the price to the list
                
    timestamps = time.time()
    timestamp.append(timestamps)

    # Wait for 2 seconds to not overload the server
    time.sleep(2)

# Open csv file to store the data
with open('../../data/dessert_wine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

    # Write the data rows
    for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink, brands, wines, ratings, reviews, prices, timestamp):
        writer.writerow([
            hyperlink,
            brand,
            wine,
            rating,
            reviews,
            price,
            timestamp
        ])

print("Data saved to 'dessert_wine.csv' successfully.")


# ## Fortified Wines
# 
# In the cell below we are collecting the data of the fortified wines. Since the number of fortified wines is limited, it is not necessary to seperate the wines into seperate urls. Therefore, the code is only run once with the full set of fortified wines. After scraping, the data will be appended to a csv file named 'fortified_wine.csv' in the data folder.

# In[10]:


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Opening the 'Vivino' website
url = 'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NTBQS6609fNRS7Z1DQ1SKwDKpqfZliUWZaaWJOao5Rel2CYWJ6vlJ1XaFhRlJqeqlZdEx9oamQB1FQMZqcVqYBIAxtccug%3D%3D'
driver.get(url)
driver.maximize_window()

# Optional: Adding some wait time for the page to fully load if needed
driver.implicitly_wait(20)  # 20 seconds 

 # Create a function to click away the cookies
try:
    accept_cookies_button = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookies_button.click()
    print("Cookies accepted.")
except Exception as e:
    print("Cookie acceptance button not found or could not be clicked:")

# Infinite scroll to load more content
scroll_pause_time = 2  # Adjust if necessary
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for the new page to load
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(scroll_pause_time)  # Wait for the potentially new content to load
        break  # Stop if we've reached the end of the page
    last_height = new_height

# Get the final page source after all content is loaded
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Create empty lists to store the data
hyperlink = []
brands = []
wines = []
ratings = []
reviews = []
prices = []
timestamp = []

# Find all wine entries on the page
wine_entries = soup.find_all(class_='card__card--2R5Wh wineCard__wineCardContent--3cwZt')

for entry in wine_entries:

    link_tag = entry.find('a', class_='wineCard__cardLink--3F_uB')
    if link_tag and link_tag.has_attr('href'):
        hyperlink.append(link_tag['href'])

    # Extract brand
    brand = entry.find(class_='wineInfoVintage__truncate--3QAtw')
    if brand:
        brands.append(brand.get_text(strip=True))

    # Extract wine name
    wine = entry.find(class_='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw') 
    if wine:
        wines.append(wine.get_text(strip=True))

    # Extract rating
    rating = entry.find(class_='vivinoRating_averageValue__uDdPM')
    if rating:
        ratings.append(rating.get_text(strip=True))
    
    # Extract review count
    review = entry.find(class_='vivinoRating_caption__xL84P')
    if review:
       # Get only the first part so the word 'beoordelingen' is not scraped
        review_text = review.get_text(strip=True)
        review_count = review_text.split()[0]
        reviews.append(review_count)

    # Check for the presence of the discount first
    discount_price_div = entry.find(class_='price_strike__mOVjZ addToCart__subText--1pvFt')
    if discount_price_div:
        # If discount exist, get the original price
        discount_price_text = discount_price_div.get_text(strip=True)
        price_only = discount_price_text.split()[-1]  # Get the last part (currency + price)
        prices.append(price_only)  # Append only the discount price to the list
    
    else:  
        # Extract currency & price if present in the addToCartButton
        price_divs = entry.find_all(class_='addToCartButton__price--qJdh4')
        if price_divs:  # If primary price class exists
            for price_div in price_divs:
                currency = price_div.find('div', class_='addToCartButton__currency--2CTNX')
                price = price_div.find_all('div')[1]  # Assuming price is in the second div
                full_price = f"{currency.get_text(strip=True) if currency else ''}{price.get_text(strip=True) if price else ''}"
                prices.append(full_price)  # Save the full price
        else:  # If not present, extract price from alternative class (online verkrijgbaar vanaf...)
            alt_price_div = entry.find(class_='addToCart__subText--1pvFt addToCart__ppcPrice--ydrd5')
            if alt_price_div:
                alt_price_text = alt_price_div.get_text(strip=True)
                price_only = alt_price_text.split()[-1]  # Get the last part (currency + price)
                prices.append(price_only)  # Append only the price to the list
                
    timestamps = time.time()
    timestamp.append(timestamps)

    # Wait for 2 seconds to not overload the server
    time.sleep(2)

# Open csv file to store the data
with open('../../data/fortified_wine.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['hyperlink','Brand', 'Wine', 'Rating', 'Reviews', 'Price','Timestamp'])

    # Write the data rows
    for hyperlink,brand, wine, rating, reviews, price, timestamp in zip(hyperlink, brands, wines, ratings, reviews, prices, timestamp):
        writer.writerow([
            hyperlink,
            brand,
            wine,
            rating,
            reviews,
            price,
            timestamp
        ])

print("Data saved to 'fortified_wine.csv' successfully.")

