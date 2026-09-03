from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import os

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,900')

driver = webdriver.Edge(options=options)
try:
    print("Opening live homepage...")
    driver.get('https://zyolekai.vercel.app/')
    time.sleep(3)
    
    # Click Talent Roster in navbar
    roster_link = driver.find_element(By.CSS_SELECTOR, "nav a[href='/roster']")
    print("Clicking Talent Roster link...")
    roster_link.click()
    
    os.makedirs('nav_frames', exist_ok=True)
    # Capture 10 frames spaced by 60ms
    for i in range(10):
        time.sleep(0.06)
        driver.save_screenshot(f'nav_frames/slide_frame_{i}_{i*60}ms.png')
    
    print("Captured slide frames!")
    
    # Now wait for page to settle
    time.sleep(1)
    # Find Media Kit button on Roster page
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    print("Clicking Media Kit button...")
    btn.click()
    
    os.makedirs('zoom_frames', exist_ok=True)
    for i in range(10):
        time.sleep(0.06)
        driver.save_screenshot(f'zoom_frames/zoom_frame_{i}_{i*60}ms.png')
        
    print("Captured zoom frames!")

finally:
    driver.quit()
