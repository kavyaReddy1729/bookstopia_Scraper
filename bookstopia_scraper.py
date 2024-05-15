#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import random
from bs4 import BeautifulSoup
import pandas as pd    
import json
import time


# In[2]:


input_file_path = "/Users/kavyareddy/Downloads/input_list.xlsx"
input_df2 = pd.read_excel(input_file_path)
urls_list = input_df2['ISBN13'].to_list()[:]


# In[3]:


out_ls = []
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
]

chrome_options = Options()
chrome_options.add_argument("--headless")  # Setting Chrome options to run headless
chrome_options.add_argument("--disable-gpu")  # This option is often recommended to avoid unnecessary use of GPU
chrome_options.add_argument("--window-size=1920x1080") 
def get_book_details(id_):
    try:
        url = f"https://www.booktopia.com.au/ebook/{id_}.html"
        
        driver.get(url)
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        print("here", "total_height",total_height)
        for i in range(1, total_height, 4):
            driver.execute_script("window.scrollTo(0, {});".format(i))
        page_source = driver.page_source
        if "Access to this page has been denied" in page_source:
            time.sleep(10)
            return
        soup = BeautifulSoup(str(page_source), 'html.parser')
        title = soup.find("div", class_= "MuiBox-root mui-style-1ebnygn").find("h1").get_text(strip = True)
        author = soup.find("p", class_= "MuiTypography-root MuiTypography-body1 mui-style-snzs7y").span.get_text(strip = True)
        author_url = soup.find("p", class_= "MuiTypography-root MuiTypography-body1 mui-style-snzs7y").a["href"]
        book_type_date = soup.find("div", class_= "MuiBox-root mui-style-1ebnygn").find("p", class_= "MuiTypography-root MuiTypography-body1 mui-style-tgrox").get_text(strip = True)
        book_type = book_type_date.split("|")[0]
        published_date = book_type_date.split("|")[1]
        det_ls = soup.find("div", id = "pdp-tabpanel-details").find_all("p", class_= "MuiTypography-root MuiTypography-body1 mui-style-tgrox")

        prod_det_dict = {}
        for item in det_ls:
            key_val = item.get_text().split(":")
            prod_det_dict[key_val[0]] = " ".join(key_val[1:])
        isbn_10 = prod_det_dict['ISBN-10']
        try:
            pages = prod_det_dict['Number of Pages']
        except:
            pages = ''
        try:
            Publisher = prod_det_dict['Publisher']
        except:
            Publisher = ''
        price_ele = soup.find("div", class_= "MuiStack-root mui-style-j7qwjs")
        try:
            original_price = price_ele.find("span", class_= "strike").get_text()
        except:
            original_price = ""
        try:
            price_ele_ = soup.find("div", class_= "MuiStack-root BuyBox_center-price__fXF15 mui-style-j7qwjs")
            disc_price= price_ele_.find("p", class_=  "MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox").get_text()
        except:
            disc_price= soup.find("p", class_= "MuiTypography-root MuiTypography-h1 Prices_sale-price__WVEfw mui-style-1ngtbwk").get_text()

        media = {
            "id_": str(id_),
            "url": url,
            "title": title,
            "author": author,
            "author_url": author_url,
            "book_type": book_type,
            "published_date": published_date,
            "isbn_10": isbn_10,
            "pages": pages,
            "original_price": original_price,
            "disc_price": disc_price,
            "prod_det_dict": prod_det_dict
        }
        out_ls.append(media)
        
    except Exception as e:
        print("exception!!!!!", e)
        return
        
for url in urls_list[:]:
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=chrome_options)
    action = webdriver.ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    get_book_details(url)
    time.sleep(5)
    driver.quit()
raw_df = pd.DataFrame(out_ls)
raw_df.to_csv(f"bookstopia_data.csv")


# In[ ]:




