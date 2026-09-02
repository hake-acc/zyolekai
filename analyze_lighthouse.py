import json, os

report_name = 'lighthouse_report_webp.json' if os.path.exists('lighthouse_report_webp.json') else 'lighthouse_report.json'
print("Report analyzed:", report_name)
with open(report_name, 'r', encoding='utf-8') as f:
    data = json.load(f)

cats = data.get('categories', {})
print("=" * 40)
print("       CURRENT LIGHTHOUSE SCORES       ")
print("=" * 40)
for k, v in cats.items():
    title = v.get('title')
    score = int(v.get('score', 0) * 100)
    print(f"• {title:<20}: {score:>3} / 100")

print("\n" + "=" * 40)
print("      AREAS FOR LIGHTHOUSE OPTIMIZATION      ")
print("=" * 40)
audits = data.get('audits', {})

# Sort low scores first
failed_audits = []
for k, v in audits.items():
    score = v.get('score')
    if score is not None and score < 1:
        failed_audits.append((score, v.get('title'), v.get('displayValue', ''), k))

failed_audits.sort(key=lambda x: x[0])

for score, title, displayVal, k in failed_audits:
    disp = f" ({displayVal})" if displayVal else ""
    print(f"[{score*100:02.0f}/100] {title}{disp}  (id: {k})")

print("\nSpecific Performance Metrics:")
for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
    if m in audits:
        am = audits[m]
        print(f"• {am.get('title')}: {am.get('displayValue')} (score: {int(am.get('score', 0)*100)})")
