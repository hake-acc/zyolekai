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
    print("Navigating to live production site...")
    driver.get('https://zyolekai.vercel.app/roster')
    time.sleep(3)
    
    # Inject animation inspector
    driver.execute_script("""
      window.__active_animations = [];
      const interval = setInterval(() => {
        const anims = document.getAnimations();
        if (anims.length > 0) {
          anims.forEach(a => {
            const effect = a.effect;
            const target = effect ? (effect.target ? effect.target.tagName : 'unknown') : 'unknown';
            const pseudo = effect ? effect.pseudoElement : null;
            const keyframes = effect ? effect.getKeyframes() : [];
            window.__active_animations.push({
              playState: a.playState,
              pseudo: pseudo,
              target: target,
              keyframesCount: keyframes.length,
              animationName: a.animationName
            });
          });
        }
      }, 50);
      window.__clear_inspector = () => clearInterval(interval);
    """)
    
    btn = driver.find_element(By.CSS_SELECTOR, "a.open-kit-btn")
    print("Clicking Media Kit button...")
    btn.click()
    
    time.sleep(2)
    driver.execute_script("if (window.__clear_inspector) window.__clear_inspector();")
    
    anims = driver.execute_script("return window.__active_animations;")
    print(f"Captured {len(anims)} animation records!")
    for a in anims[:20]:
        print("ANIMATION:", a)

finally:
    driver.quit()
