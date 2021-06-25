#!/usr/bin/env python
# coding: utf-8

# In[11]:


from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
from sys import platform
import pandas as pd
import numpy as np

options = Options()
if platform == "win32":
	options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# In[32]:


delay = 5

driver = webdriver.Chrome(ChromeDriverManager().install())
print('Once your browser opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')
input("Press ENTER after login into Whatsapp Web and your chats are visiable	.")
df = pd.read_csv("whatsapp_send.csv").dropna()
df['Number'] = df['Number'].apply(np.int64)

for index, row in df.iterrows():
    number = str(row['Number'])
    if number == "":
        continue
    if len(number) == 10:
        number = '91'+number	
    print('{}/{} => Sending message to {}.'.format((index+1), df.shape[0], number))
    try:
        url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + row['Message']
        sent = False
        for i in range(3):
            if not sent:
                driver.get(url)
                try:
                    click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME , '_1E0Oz')))
                except Exception as e:
                    print(f"Something went wrong..\n Failed to send message to: {number}, retry ({i+1}/3)")
                    print("Make sure your phone and computer is connected to the internet.")
                    print("If there is an alert, please dismiss it.")
                    input("Press enter to continue")
                else:
                    sleep(1)
                    click_btn.click()
                    sent=True
                    sleep(3)
                    print('Message sent to: ' + number)
    except Exception as e:
        print('Failed to send message to ' + number + str(e))


# In[30]:




