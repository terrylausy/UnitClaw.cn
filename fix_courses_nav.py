#!/usr/bin/env python3
"""将全站导航栏中的'课程'链接改为下拉菜单（四大课程体系），与产品下拉菜单风格一致"""

import re, os

BASE = r'C:\Users\49563\WorkBuddy\20260511211326\UnitClaw.cn'

# 定义不同目录前缀下的课程下拉菜单HTML（桌面端）
def get_courses_dropdown(prefix_root, prefix_products):
    """生成课程下拉菜单HTML
    prefix_root: 到根目录的前缀（如 '' 或 '../' 或 '../../'）
    prefix_products: 到products目录的前缀（如 'products/' 或 '../products/' 或 '../../products/'）
    注意：courses.html在根目录，所以链接用 prefix_root + 'courses.html#xxx'
    """
    courses_link = prefix_root + 'courses.html'
    return f'''<div class="group relative">
                <a href="{courses_link}" class="px-4 py-2 text-gray-700 hover:text-gray-900 text-sm font-medium transition-colors">课程 <i class="fas fa-chevron-down text-[10px] ml-1"></i></a>
                <div class="absolute top-full left-0 mt-2 w-56 glass rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                    <a href="{courses_link}#ai-courses" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-microchip mr-2 text-emerald-500 text-xs"></i>AI实训箱课程</a>
                    <a href="{courses_link}#openarm-courses" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-industry mr-2 text-orange-500 text-xs"></i>OpenArm 机械臂课程</a>
                    <a href="{courses_link}#robot-courses" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-robot mr-2 text-accent text-xs"></i>具身智能机器人课程</a>
                    <a href="{courses_link}#dexterous-hand-courses" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-hand-sparkles mr-2 text-purple-500 text-xs"></i>灵巧手课程</a>
                </div>
            </div>'''

def get_courses_mobile_items(prefix_root):
    """生成手机端课程子项"""
    courses_link = prefix_root + 'courses.html'
    return f'''        <a href="{courses_link}#ai-courses" class="block py-3 text-gray-700 pl-4"><i class="fas fa-microchip mr-2 text-emerald-500 text-xs"></i>AI实训箱课程</a>
        <a href="{courses_link}#openarm-courses" class="block py-3 text-gray-700 pl-4"><i class="fas fa-industry mr-2 text-orange-500 text-xs"></i>OpenArm 机械臂课程</a>
        <a href="{courses_link}#robot-courses" class="block py-3 text-gray-700 pl-4"><i class="fas fa-robot mr-2 text-accent text-xs"></i>具身智能机器人课程</a>
        <a href="{courses_link}#dexterous-hand-courses" class="block py-3 text-gray-700 pl-4"><i class="fas fa-hand-sparkles mr-2 text-purple-500 text-xs"></i>灵巧手课程</a>'''

# 每个文件的前缀配置
FILE_CONFIGS = {
    # 根目录文件：无前缀
    'about.html':        ('', 'products/'),
    'courses.html':      ('', 'products/'),
    'contact.html':      ('', 'products/'),
    'news.html':         ('', 'products/'),
    'support.html':      ('', 'products/'),
    'disclaimer.html':   ('', 'products/'),
    'privacy.html':      ('', 'products/'),
    'index.html':        ('', 'products/'),
    # products/ 目录：../ 到根目录，本地产品无前缀
    'products/robots.html':            ('../', '../products/'),
    'products/openarm.html':           ('../', '../products/'),
    'products/embedded-platform.html': ('../', '../products/'),
    'products/courses.html':           ('../', '../products/'),
    'products/dexterous-hand.html':    ('../', '../products/'),
    'products/training-box.html':      ('../', '../products/'),
    # solutions/ 目录：../ 到根目录
    'solutions/education.html':              ('../', '../products/'),
    'solutions/university-cooperation.html': ('../', '../products/'),
    # robots/ 目录：../../ 到根目录
    'robots/index.html':  ('../../', '../../products/'),
    'robots/mini-pi.html':('../../', '../../products/'),
    'robots/mini-hi.html':('../../', '../../products/'),
    'robots/pi-plus.html':('../../', '../../products/'),
    # courses/ 目录：../../ 到根目录
    'courses/index.html': ('../../', '../../products/'),
    # download/ 目录：../../ 到根目录
    'download/index.html':('../../', '../../products/'),
    # partnerships/ 目录：../../ 到根目录
    'partnerships/university-cooperation.html':('../../', '../../products/'),
    'partnerships/hightorque.html':            ('../../', '../../products/'),
    'partnerships/suiguangming.html':          ('../../', '../../products/'),
    # components/ 目录：../../ 到根目录
    'components/index.html':         ('../../', '../../products/'),
    'components/dexterous-hand.html':('../../', '../../products/'),
}

MODIFIED_FILES = []

for filepath, (prefix_root, prefix_products) in FILE_CONFIGS.items():
    fullpath = os.path.join(BASE, filepath)
    if not os.path.exists(fullpath):
        print(f'SKIP (not found): {filepath}')
        continue
    
    content = open(fullpath, 'r', encoding='utf-8').read()
    original = content
    
    # === 1. Desktop: Replace standalone "课程" link with dropdown ===
    # Pattern: standalone <a href="Xcourses.html" ...>课程</a>
    # Need to handle various formats:
    # Format A: <a href="courses.html" class="...">课程</a>  (root level)
    # Format B: <a href="../courses.html" class="...">课程</a>  (1-deep)
    # Format C: <a href="../../courses.html" class="...">课程</a>  (2-deep)
    # Also need to handle: active state version (text-accent font-semibold border-b-2 border-accent)
    
    # Generate the correct replacement
    dropdown = get_courses_dropdown(prefix_root, prefix_products)
    courses_link = prefix_root + 'courses.html'
    
    # Pattern 1: Simple "课程" link (various href formats pointing to courses.html)
    # Match: <a href="[prefix]courses.html" class="px-4 py-2 ...">课程</a>
    # The href can be: courses.html, ../courses.html, ../../courses.html
    pattern1 = r'<a\s+href="[^"]*courses\.html"\s+class="px-4\s+py-2[^>]*>课程</a>'
    
    # Need to check if the nav already has a dropdown for 课程
    if '课程 <i class="fas fa-chevron-down' in content:
        # Already has dropdown - check if it needs updating
        # Find existing dropdown and replace with new one
        existing_dropdown_pattern = r'<div\s+class="group\s+relative">\s*<a\s+href="[^"]*courses\.html"[^>]*>课程\s+<i\s+class="fas\s+fa-chevron-down[^"]*"[^>]*></i></a>\s*<div\s+class="absolute[^>]*>.*?</div>\s*</div>'
        match = re.search(existing_dropdown_pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(), dropdown)
            print(f'UPDATED existing dropdown: {filepath}')
        else:
            print(f'HAS chevron but no matching dropdown pattern: {filepath}')
    else:
        # Replace standalone link with dropdown
        matches = list(re.finditer(pattern1, content))
        if matches:
            # Replace each match with the dropdown
            for m in matches:
                # Check if this is in the desktop nav (hidden lg:flex section)
                # We need context to distinguish desktop from mobile
                content = content.replace(m.group(), dropdown)
            print(f'REPLACED standalone link: {filepath}')
        else:
            print(f'NO 课程 link found: {filepath}')
    
    # === 2. Mobile: Replace standalone "课程" link with header + sub-items ===
    # Pattern in mobile menu: <a href="[prefix]courses.html" class="block py-3 ...">课程</a>
    mobile_courses_link_pattern = r'<a\s+href="[^"]*courses\.html"\s+class="block\s+py-3[^>]*>[^<]*课程[^<]*</a>'
    
    mobile_items = get_courses_mobile_items(prefix_root)
    # For mobile, replace the single link with: header link + sub-items
    mobile_replacement = f'''        <a href="{courses_link}" class="block py-3 text-gray-700 font-medium"><i class="fas fa-book-open mr-2 text-accent2 text-xs"></i>课程</a>
{mobile_items}'''
    
    mobile_matches = list(re.finditer(mobile_courses_link_pattern, content))
    if mobile_matches:
        for m in mobile_matches:
            content = content.replace(m.group(), mobile_replacement)
        print(f'UPDATED mobile menu: {filepath}')
    
    # Write back if changed
    if content != original:
        open(fullpath, 'w', encoding='utf-8').write(content)
        MODIFIED_FILES.append(filepath)
    else:
        print(f'NO CHANGE: {filepath}')

print(f'\n=== Summary ===')
print(f'Modified {len(MODIFIED_FILES)} files:')
for f in MODIFIED_FILES:
    print(f'  {f}')
