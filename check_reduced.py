from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)
try:
    driver.get('https://zyolekai.vercel.app')
    reduced = driver.execute_script("return window.matchMedia('(prefers-reduced-motion: reduce)').matches;")
    print("prefers-reduced-motion is:", reduced)
finally:
    driver.quit()
