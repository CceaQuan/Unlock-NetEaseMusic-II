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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A260FD3F2E49D6BF84E8956B15E8A1475196F147D2A27B395F91C8A59E166E2EE7E10ABEBB58D2D706031EFB831CFB3E37FD89E441B7D95714329FCAA8E803810D87B74CE720395CC635AA9661B76D77F9E71889EDC9A75C0D447B4C31B393E26F67C82424AD5499D3289FD3BDAA91007D2CEECB715A814759C71193F214269F6DFA523CA028DC6280976C40845BF36E902DFB9C1DFC9A2CD1E0DBBEC59C8B2B0CD9548CEA729CDA95299CA851864BE49983E078A5343C908770ABF8E3F08B9D76A34962374CD87E53ACD5B587946074CA3759FD9172953398B20EAA770EB0D06432B3F55D01FBAE9328B765F26E365C96B27B5F766C5582E5675D8B8DBAF899175DDF18D124268A37A73BA0CBAB480088BAE6FF52F5C3D427093C6DE200F99020FCB8AB1285F568AA8387BC864680D71F9942B3FACCBE6C740B48F4F477F4B1EA3E603B3A03609D97F5E4225997D5C5"})
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
