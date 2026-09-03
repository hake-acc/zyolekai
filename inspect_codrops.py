from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(options=options)
try:
    print("Fetching Codrops PageTransitions...")
    driver.get('https://tympanus.net/Development/PageTransitions/')
    time.sleep(3)
    
    # Inspect Codrops DOM structure and CSS
    html = driver.execute_script("""
      return {
        mainId: document.getElementById('pt-main') ? document.getElementById('pt-main').outerHTML.slice(0, 500) : 'not found',
        pages: Array.from(document.querySelectorAll('.pt-page')).map(p => ({
          className: p.className,
          style: p.style.cssText
        })),
        cssClasses: Array.from(document.styleSheets).flatMap(s => {
          try {
            return Array.from(s.cssRules).map(r => r.cssText).filter(c => c.includes('moveToLeft') || c.includes('moveFromRight') || c.includes('scaleDown') || c.includes('zoomIn') || c.includes('.pt-page'));
          } catch(e) { return []; }
        })
      };
    """)
    print("Codrops pt-main container:")
    print(html['mainId'])
    print("\nCodrops CSS Rules count:", len(html['cssClasses']))
    for r in html['cssClasses'][:15]:
        print("  RULE:", r[:140])

finally:
    driver.quit()
