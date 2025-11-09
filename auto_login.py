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

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00253F3940749DB8A6E47121C8C24509BADD9B79C55E5A40B7ECEDD2EF627FE65C7EF8E44925C32395BB4F8EF47784535F8521D9647CCA082EE0098EE60B5EC730D80F21BFFF4A8F4DEB6D077929AB67C5DCF77C94A98E82209252F5B8EBA450B2613A93E4612DCF160442668E00C9E15BAB8C53312A4527F5286E78687B759C172C3A81ADA0A3238603FDFF475E4549ECB477F5C582D3C490D488385A533C46884F43627348CB1D98F7B8F7E9A884F155BECD5F74269420A0C61B9B5F76E906974135D10634D8EBC4E5AABAADB1E931C022902FCD1E9820B669D335C9A8FAC6B3F25D73614660557D6CD664639103E20890B9C5D9B9F52914BE5827003819970F8BA2360E0764C03894942F726947B14CBE08402D2DF831AAB77E938B7F9C1E79FDA9237E488A630B86C3AB5FCE990984E5B3BDED249F722CC90C8861988263A915B9CD6EAC46820BBD6EEBFCF854E51C0DF8A3B197708B938614C731516C20778C12B27BDFB9791FF6C76599FBACCEC51281ED9DD9BF4F060950F2084B5CFAAA78966D65927EEECEF73991B7AE11507B28EDA395AC0A9B8899515851A30F1194"})
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
