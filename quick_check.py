import re, subprocess, os

html_path = r'C:\Users\Khalifa Aliyu\desktop\web-wedding-invitation\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_js = scripts[-1]
temp_js = r'C:\Users\Khalifa Aliyu\desktop\web-wedding-invitation\temp_check.js'
with open(temp_js, 'w', encoding='utf-8') as f:
    f.write(main_js)

res = subprocess.run(['node', '--check', temp_js], capture_output=True, text=True)
if os.path.exists(temp_js):
    os.remove(temp_js)

if res.returncode == 0:
    print('PASS: JavaScript syntax check passed with node --check!')
else:
    print('FAIL: JavaScript syntax error:\n', res.stderr)

direct_ids = set(re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', main_js))
html_ids = set(re.findall(r'id=[\'"]([^\'"]+)[\'"]', content))

missing_direct = [i for i in direct_ids if i not in html_ids]
print(f'Total direct getElementById checks: {len(direct_ids)}')
if missing_direct:
    print('WARNING: Missing IDs in HTML:', missing_direct)
else:
    print('PASS: All getElementById referenced IDs exist in HTML!')

gsap_ids = set(re.findall(r'[\'"]#([a-zA-Z0-9_-]+)[\'"]', main_js))
missing_gsap = [i for i in gsap_ids if i not in html_ids]
print(f'Total GSAP #id checks: {len(gsap_ids)}')
if missing_gsap:
    print('WARNING: Missing GSAP #id targets in HTML:', missing_gsap)
else:
    print('PASS: All GSAP #id targets exist in HTML!')
