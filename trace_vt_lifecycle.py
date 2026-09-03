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
    driver.get('https://zyolekai.vercel.app/roster')
    time.sleep(3)
    
    driver.execute_script("""
      window.__debug_events = [];
      const log = (msg, extra) => window.__debug_events.push({ time: performance.now(), msg, extra });
      
      document.addEventListener('click', (e) => {
        const a = e.target.closest('a');
        log('click-listener', {
          targetTag: e.target.tagName,
          isA: !!a,
          href: a ? a.getAttribute('href') : null,
          currentDataTransition: document.documentElement.getAttribute('data-transition')
        });
      }, true);
      
      document.addEventListener('astro:before-preparation', (e) => {
        log('before-preparation', {
          from: e.from ? e.from.pathname : null,
          to: e.to ? e.to.pathname : null,
          direction: e.direction,
          currentDataTransition: document.documentElement.getAttribute('data-transition')
        });
      });
      
      document.addEventListener('astro:before-swap', (e) => {
        log('before-swap', {
          currentDataTransition: document.documentElement.getAttribute('data-transition'),
          newDocDataTransition: e.newDocument ? e.newDocument.documentElement.getAttribute('data-transition') : null
        });
      });
    """)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    print("Found button href:", btn.get_attribute("href"))
    btn.click()
    time.sleep(2)
    
    events = driver.execute_script("return window.__debug_events;")
    for ev in events:
        print(ev)

finally:
    driver.quit()
