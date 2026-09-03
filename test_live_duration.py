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
    print("Testing on live production URL https://zyolekai.vercel.app/roster...")
    driver.get('https://zyolekai.vercel.app/roster')
    time.sleep(3)
    
    driver.execute_script("""
      window.__anim_events = [];
      const handler = (e) => {
        window.__anim_events.push({
          type: e.type,
          animName: e.animationName,
          pseudo: e.pseudoElement,
          rootDataTransition: document.documentElement.getAttribute('data-transition'),
          target: e.target ? e.target.nodeName : null,
          time: performance.now()
        });
      };
      window.addEventListener('animationstart', handler, true);
      window.addEventListener('animationend', handler, true);
    """)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    print("Clicking Media Kit button on live site...")
    btn.click()
    time.sleep(2)
    
    events = driver.execute_script("return window.__anim_events;")
    print(f"Captured {len(events)} animation events:")
    for ev in events:
        if 'ptZoom' in ev['animName'] or 'ptScale' in ev['animName'] or 'ptMove' in ev['animName']:
            print(ev)

finally:
    driver.quit()
