from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)
try:
    driver.get('https://zyolekai.vercel.app/roster')
    time.sleep(2)
    
    # Intercept document.startViewTransition and check computed style of pseudo elements inside the transition
    styles = driver.execute_script("""
      return new Promise((resolve) => {
        const orig = document.startViewTransition;
        document.startViewTransition = function(cb) {
          const vt = orig.call(document, cb);
          vt.ready.then(() => {
            const oldStyle = window.getComputedStyle(document.documentElement, '::view-transition-old(main-content)');
            const newStyle = window.getComputedStyle(document.documentElement, '::view-transition-new(main-content)');
            const rootOldStyle = window.getComputedStyle(document.documentElement, '::view-transition-old(root)');
            const rootNewStyle = window.getComputedStyle(document.documentElement, '::view-transition-new(root)');
            resolve({
              oldAnim: oldStyle.animationName,
              oldDuration: oldStyle.animationDuration,
              oldTiming: oldStyle.animationTimingFunction,
              newAnim: newStyle.animationName,
              newDuration: newStyle.animationDuration,
              newTiming: newStyle.animationTimingFunction,
              rootOldAnim: rootOldStyle.animationName,
              rootNewAnim: rootNewStyle.animationName,
            });
          });
          return vt;
        };
        
        // Trigger navigation
        const btn = document.querySelector('nav a[href=\"/sponsorships\"]');
        btn.click();
      });
    """)
    print("PROD VIEW TRANSITION COMPUTED STYLES:")
    print(styles)

finally:
    driver.quit()
