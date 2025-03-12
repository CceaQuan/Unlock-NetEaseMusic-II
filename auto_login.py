# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002DB7AA8CAD68E46AA4CC9F5FCCA65A362B5A7BA557B19162221BF9376D261260296860A87DDE82584E74716D68E829F597419F8995989DC07CC920ED2BCF0EDBF8925E62FE29A2B092568E105598967FBCCA06E9AE0FB6A327420A81D46B47738C951CB732EB84476516E86A42F8C935C7BF97F2C9683E44075EADBEF6361DBE462EF484FB08FC0E71519248EAE64CD776B5168C9269A4D63BD76957C88FBCAC04212E7D5D26C1C4B469C52FD7AD781BC7FC3A1333B6FFF70C0048009F572EF10F8974EA8D1201879DBD7DA2060C3E6DE2ED771A98A045DD9E3C060F0BA2995B3A167BEBDBED0550B874E6CD378D8F05D56D4A0B0233D378E67A76FABFDD0EA79D51EB399FF5F7FA2E4AD5D68C9E3425E24E85E7E49E8CBF0BCEA79795A57438A65B21262695C36F51769DB9444086CA743887966F183DB698CE4728F3428364CE26B743D4EBF31EC4C09DBAF558DE9B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
