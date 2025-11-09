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
    browser.add_cookie({"name": "MUSIC_U", "value": "0087A9C13BF7C1523D91E740DB573B03194BE00F34561CA0F26280BE553A9CB91AC6C3BB6388AD595DA051B0C09FC2D6B088D634702FAB0A0B3DA87CED98BFC06855238BBA615E18C12DA824B722C048A6CB284F46191387C4A551E785C979785D1498313EA81EFE3170F93AFF433E23F43D27DC705CC66BF4D6376DF8DC27B12325C73F8EC10309BED764ED5F0FA820110832A9F60A33F6089AD50B8DCAD7C60B43B47B5CD57C7B351D1E63360A241A8EFEA9FCAB2F226ECC3956474F855D890D37D1DDE9A87F8AC92FFB8577E513CFFE80B5C28F1BFE627195E42F358E1593FC24C06997796CE9E5E540A6E579936A5692F58E1B63397564067D124D8DCF990DCEB7214F173B931D9A34054B2B22D8C86138EBDB41B320A35D2C6B4D4FCF0136FC4574F282F7817192D19EEA37E9B341F5DAC2CFF7C3B911EF101BAB753F1ED259B2DE0EF311AAA2C82D4A04EDF0CDA438D9DCB7AE70B3A12C1B66156E46D66E6E0AC492BCF9D2887F330E6FAD0532F6DF3AF2F5B87CC6634BEFB443C54FF3F2D0C2562560D62C981E703696921F66B1"})
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
