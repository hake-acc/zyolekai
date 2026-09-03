from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(options=options)
try:
    print("Measuring performance on live site https://zyolekai.vercel.app ...")
    driver.get('https://zyolekai.vercel.app')
    time.sleep(4)
    
    perf_data = driver.execute_script("""
      const nav = performance.getEntriesByType('navigation')[0] || {};
      const paint = performance.getEntriesByType('paint') || [];
      const resources = performance.getEntriesByType('resource') || [];
      
      const fcp = paint.find(p => p.name === 'first-contentful-paint');
      
      // Categorize resources
      let totalBytes = 0;
      const byType = {};
      const largestResources = resources
        .map(r => ({
          name: r.name.split('/').pop() || r.name,
          fullUrl: r.name,
          initiatorType: r.initiatorType,
          transferSize: r.transferSize || 0,
          decodedBodySize: r.decodedBodySize || 0,
          duration: Math.round(r.duration)
        }))
        .sort((a, b) => b.transferSize - a.transferSize);
        
      resources.forEach(r => {
        const size = r.transferSize || 0;
        totalBytes += size;
        const type = r.initiatorType || 'other';
        byType[type] = (byType[type] || 0) + size;
      });
      
      return {
        dns: Math.round(nav.domainLookupEnd - nav.domainLookupStart),
        connect: Math.round(nav.connectEnd - nav.connectStart),
        ttfb: Math.round(nav.responseStart - nav.requestStart),
        domInteractive: Math.round(nav.domInteractive),
        domComplete: Math.round(nav.domComplete),
        loadEventEnd: Math.round(nav.loadEventEnd),
        fcp: fcp ? Math.round(fcp.startTime) : null,
        totalResources: resources.length,
        totalTransferKb: Math.round(totalBytes / 1024),
        byTypeKb: Object.fromEntries(Object.entries(byType).map(([k, v]) => [k, Math.round(v / 1024)])),
        largestResources: largestResources.slice(0, 10)
      };
    """)
    
    print("\n=== PERFORMANCE TIMINGS ===")
    print(f"TTFB: {perf_data['ttfb']}ms")
    print(f"FCP: {perf_data['fcp']}ms")
    print(f"DOM Interactive: {perf_data['domInteractive']}ms")
    print(f"DOM Complete: {perf_data['domComplete']}ms")
    print(f"Load Event End: {perf_data['loadEventEnd']}ms")
    print(f"Total Resources: {perf_data['totalResources']}")
    print(f"Total Transferred: {perf_data['totalTransferKb']} KB")
    print(f"By Type: {perf_data['byTypeKb']}")
    
    print("\n=== TOP 10 LARGEST RESOURCES ===")
    for r in perf_data['largestResources']:
        print(f"{r['transferSize']/1024:.1f} KB | {r['duration']}ms | [{r['initiatorType']}] {r['name']}")

finally:
    driver.quit()
