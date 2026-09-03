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
    time.sleep(2)
    
    # Check if startViewTransition is called
    driver.execute_script("""
      window.__vt_called = false;
      window.__vt_error = null;
      const orig = document.startViewTransition;
      if (orig) {
        document.startViewTransition = function(cb) {
          window.__vt_called = true;
          try {
            return orig.call(document, cb);
          } catch(e) {
            window.__vt_error = e.toString();
            throw e;
          }
        };
      }
    """)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    btn.click()
    time.sleep(2)
    
    vt_called = driver.execute_script("return window.__vt_called;")
    vt_error = driver.execute_script("return window.__vt_error;")
    print("startViewTransition was called:", vt_called)
    print("startViewTransition error:", vt_error)
    print("Current URL:", driver.current_url)

finally:
    driver.quit()
