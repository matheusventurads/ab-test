import time
import numpy as np
from selenium import webdriver

driver = webdriver.Firefox()

driver.get('http://127.0.01:5001/home')

clicks = 10000
for click in range(clicks):
    if np.random.choice(np.arange(0, 2), p=[0.65, 0.35]) == 1:
        driver.find_element('name', 'yescheckbox').click()
        driver.find_element('id', 'yesbtn').click()
        time.sleep(2)
    else:
        driver.find_element('name', 'nocheckbox').click()
        driver.find_element('id', 'nobtn').click()
        time.sleep(2)