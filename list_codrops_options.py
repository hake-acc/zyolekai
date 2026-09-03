from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')

driver = webdriver.Edge(options=options)
try:
    driver.get('https://tympanus.net/Development/PageTransitions/')
    time.sleep(2)
    
    # Get all animations listed in the menu
    options_text = driver.execute_script("""
      const menu = document.querySelectorAll('#dl-menu ul li a');
      return Array.from(menu).map((a, i) => `${i+1}: ${a.textContent.trim()}`);
    """)
    print("Codrops animations count:", len(options_text))
    for opt in options_text[:20]:
        print(opt)

finally:
    driver.quit()
