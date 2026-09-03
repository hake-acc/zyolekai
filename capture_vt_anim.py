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
    time.sleep(1)
    driver.get('http://127.0.0.1:4329/roster')
    time.sleep(2)
    
    driver.execute_script("""
      window.__anim_events = [];
      const handler = (e) => {
        window.__anim_events.push({
          type: e.type,
          animName: e.animationName,
          pseudo: e.pseudoElement,
          target: e.target ? e.target.nodeName : null,
          time: performance.now()
        });
      };
      window.addEventListener('animationstart', handler, true);
      window.addEventListener('animationend', handler, true);
    """)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    btn.click()
    time.sleep(2)
    
    events = driver.execute_script("return window.__anim_events;")
    print(f"Captured {len(events)} animation events:")
    for ev in events:
        if 'ptZoom' in ev['animName'] or 'ptScale' in ev['animName'] or 'ptMove' in ev['animName']:
            print(ev)

finally:
    driver.quit()
