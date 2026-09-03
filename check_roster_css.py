import re

with open('dist/roster/index.html', 'r', encoding='utf-8') as fp:
    c = fp.read()

print('CSS files in dist/roster/index.html:')
for link in re.findall(r'<link[^>]+>', c):
    if 'stylesheet' in link:
        print('LINK:', link)

print('\nInline style tags containing ptMove:')
for style in re.findall(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
    if 'ptMove' in style:
        print('STYLE:', style[:200])
        print('Contains @keyframes ptMoveToLeft:', '@keyframes ptMoveToLeft' in style)

print('\nCheck if @keyframes ptMoveToLeft is anywhere in dist/roster/index.html:')
print('@keyframes ptMoveToLeft in c:', '@keyframes ptMoveToLeft' in c)
