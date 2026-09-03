from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,900')

driver = webdriver.Edge(options=options)
try:
    print("Navigating to live roster page...")
    driver.get('https://zyolekai.vercel.app/roster')
    time.sleep(3)
    
    # Scroll down so cards are visible
    driver.execute_script("window.scrollTo(0, 400);")
    time.sleep(1)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    print("Clicking View Media Kit button...")
    btn.click()
    
    # Capture mid-transition frames during the 600ms animation
    time.sleep(0.18)
    driver.save_screenshot('live_zoom_180ms.png')
    time.sleep(0.18)
    driver.save_screenshot('live_zoom_360ms.png')
    time.sleep(0.3)
    driver.save_screenshot('live_zoom_final.png')
    print("Captured mid-transition frames successfully!")

finally:
    driver.quit()
