import time
import numpy as np
from selenium import webdriver

driver = webdriver.Firefox()

driver.get('http://127.0.01:5000/home')

clicks = 10000
for click in range(clicks):
    button_color = driver.find_element('name', 'yescheckbox').get_attribute('value')

    if button_color == 'blue':
        if np.random.choice(np.arange(0, 2), p=[0.70, 0.30]) == 1:
            driver.find_element('name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            time.sleep(2)
        else:
            driver.find_element('name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            time.sleep(1)
    else:
        if np.random.choice(np.arange(0, 2), p=[0.65, 0.35]) == 1:
            driver.find_element('name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            time.sleep(2)
        else:
            driver.find_element('name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            time.sleep(1)
