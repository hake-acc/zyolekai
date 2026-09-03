with open('dist/_astro/ClientRouter.astro_astro_type_script_index_0_lang.CDGfc0hd.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
for var in ['M', 'k', 'd']:
    matches = re.findall(r'\b' + var + r'\s*=\s*["\']([^"\']+)["\']', js)
    print(var, '=', matches)
