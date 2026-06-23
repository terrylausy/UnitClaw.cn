#!/usr/bin/env python3
"""将全站导航栏中'高校合作'改为下拉菜单（教育方案+产教研合作），移除独立'产教研合作'链接"""

import re, os

BASE = r'C:\Users\49563\WorkBuddy\20260511211326\UnitClaw.cn'

# Desktop dropdown HTML for "高校合作" (with sub-items)
# Different prefix for solutions/ directory (local links) vs other directories
def get_gaoxiao_dropdown(prefix_solutions, is_solution_page=False):
    """prefix_solutions: path to solutions/ dir from current file"""
    education_link = prefix_solutions + 'education.html'
    chanjiao_link = prefix_solutions + 'education.html#chanjiao'
    if is_solution_page:
        # In solutions/ directory, links are local (education.html instead of ../solutions/education.html)
        education_link = 'education.html'
        chanjiao_link = 'education.html#chanjiao'
    return f'''<div class="group relative">
                <a href="{education_link}" class="px-4 py-2 text-gray-700 hover:text-gray-900 text-sm font-medium transition-colors">高校合作 <i class="fas fa-chevron-down text-[10px] ml-1"></i></a>
                <div class="absolute top-full left-0 mt-2 w-48 glass rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                    <a href="{education_link}" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-flask mr-2 text-accent text-xs"></i>教育方案</a>
                    <a href="{chanjiao_link}" class="block px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100/50 transition-colors"><i class="fas fa-handshake mr-2 text-warm text-xs"></i>产教研合作</a>
                </div>
            </div>'''

def get_gaoxiao_mobile_items(prefix_solutions, is_solution_page=False):
    """Mobile menu items for 高校合作"""
    education_link = prefix_solutions + 'education.html'
    chanjiao_link = prefix_solutions + 'education.html#chanjiao'
    if is_solution_page:
        education_link = 'education.html'
        chanjiao_link = 'education.html#chanjiao'
    return f'''        <a href="{education_link}" class="block py-3 text-gray-700 font-medium"><i class="fas fa-university mr-2 text-accent text-xs"></i>高校合作</a>
        <a href="{education_link}" class="block py-3 text-gray-700 pl-4"><i class="fas fa-flask mr-2 text-accent text-xs"></i>教育方案</a>
        <a href="{chanjiao_link}" class="block py-3 text-gray-700 pl-4"><i class="fas fa-handshake mr-2 text-warm text-xs"></i>产教研合作</a>'''

# File configurations: (file_path, prefix_to_solutions, is_solution_page)
FILE_CONFIGS = {
    # Root level: solutions/ prefix
    'index.html':      ('solutions/', False),
    'about.html':      ('solutions/', False),
    'courses.html':    ('solutions/', False),
    'contact.html':    ('solutions/', False),
    'news.html':       ('solutions/', False),
    'support.html':    ('solutions/', False),
    'disclaimer.html': ('solutions/', False),
    'privacy.html':    ('solutions/', False),
    # products/ level: ../solutions/
    'products/robots.html':            ('../solutions/', False),
    'products/openarm.html':           ('../solutions/', False),
    'products/embedded-platform.html': ('../solutions/', False),
    'products/courses.html':           ('../solutions/', False),
    'products/dexterous-hand.html':    ('../solutions/', False),
    'products/training-box.html':      ('../solutions/', False),
    # solutions/ level: local links
    'solutions/education.html':              ('../solutions/', True),  # special: is solution page
    'solutions/university-cooperation.html':  ('../solutions/', True),
    # 2-deep: ../../solutions/
    'robots/index.html':  ('../../solutions/', False),
    'robots/mini-pi.html':('../../solutions/', False),
    'robots/mini-hi.html':('../../solutions/', False),
    'robots/pi-plus.html':('../../solutions/', False),
    'courses/index.html': ('../../solutions/', False),
    'download/index.html':('../../solutions/', False),
    'partnerships/university-cooperation.html':('../../solutions/', False),
    'partnerships/hightorque.html':            ('../../solutions/', False),
    'partnerships/suiguangming.html':          ('../../solutions/', False),
    'components/index.html':         ('../../solutions/', False),
    'components/dexterous-hand.html':('../../solutions/', False),
}

MODIFIED_FILES = []

for filepath, (prefix_sol, is_sol) in FILE_CONFIGS.items():
    fullpath = os.path.join(BASE, filepath)
    if not os.path.exists(fullpath):
        print(f'SKIP: {filepath}')
        continue
    
    content = open(fullpath, 'r', encoding='utf-8').read()
    original = content
    
    dropdown = get_gaoxiao_dropdown(prefix_sol, is_sol)
    mobile_items = get_gaoxiao_mobile_items(prefix_sol, is_sol)
    
    # === 1. Desktop: Replace standalone "高校合作" link with dropdown ===
    # Pattern: <a href="Xeducation.html" ...>高校合作</a> (standalone, not already dropdown)
    # Also need to remove the standalone "产教研合作" link that comes after
    
    # Check if already has 高校合作 dropdown
    if '高校合作 <i class="fas fa-chevron-down' in content:
        print(f'ALREADY HAS DROPDOWN: {filepath}')
    else:
        # Replace standalone 高校合作 link with dropdown
        # Various formats of the 高校合作 link:
        # Format A (root): <a href="solutions/education.html" class="...">高校合作</a>
        # Format B (products): <a href="../solutions/education.html" class="...">高校合作</a>
        # Format C (solutions local): <a href="education.html" class="...">高校合作</a>
        # Format D (2-deep): <a href="../../solutions/education.html" class="...">高校合作</a>
        
        pattern_gaoxiao = r'<a\s+href="[^"]*education\.html"[^>]*class="px-4\s+py-2[^"]*"[^>]*>[^<]*高校合作[^<]*</a>'
        matches = list(re.finditer(pattern_gaoxiao, content, re.DOTALL))
        for m in matches:
            # Check if this is in the desktop nav area (not mobile)
            # We'll just replace all standalone 高校合作 links with dropdown
            content = content.replace(m.group(), dropdown)
            print(f'REPLACED 高校合作 link: {filepath}')
        
        # If no matches found with that pattern, try broader pattern
        if not matches:
            pattern_gaoxiao2 = r'<a\s+href="[^"]*education\.html"[^>]*>.*?高校合作.*?</a>'
            matches2 = list(re.finditer(pattern_gaoxiao2, content, re.DOTALL))
            for m in matches2:
                content = content.replace(m.group(), dropdown)
                print(f'REPLACED 高校合作 (broad): {filepath}')
    
    # === 2. Desktop: Remove standalone "产教研合作" link ===
    # Pattern: <a href="Xuniversity-cooperation.html" or "Xeducation.html#chanjiao" ...>产教研合作</a>
    pattern_chanjiao = r'<a\s+href="[^"]*university-cooperation\.html"[^>]*class="px-4\s+py-2[^"]*"[^>]*>[^<]*产教研合作[^<]*</a>'
    matches_c = list(re.finditer(pattern_chanjiao, content, re.DOTALL))
    for m in matches_c:
        content = content.replace(m.group(), '')
        print(f'REMOVED 产教研合作 standalone: {filepath}')
    
    # === 3. Mobile: Replace standalone 高校合作/产教研合作 with grouped items ===
    # Find mobile menu entries for 高校合作 and 产教研合作
    pattern_gaoxiao_mobile = r'<a\s+href="[^"]*education\.html"[^>]*class="block\s+py-3[^"]*"[^>]*>[^<]*高校合作[^<]*</a>'
    pattern_chanjiao_mobile = r'<a\s+href="[^"]*university-cooperation\.html"[^>]*class="block\s+py-3[^"]*"[^>]*>[^<]*产教研合作[^<]*</a>'
    
    # Also handle text-accent variants
    pattern_gaoxiao_mobile2 = r'<a\s+href="[^"]*education\.html"[^>]*class="block\s+py-3\s+text-accent[^"]*"[^>]*>[^<]*高校合作[^<]*</a>'
    pattern_chanjiao_mobile2 = r'<a\s+href="[^"]*university-cooperation\.html"[^>]*class="block\s+py-3\s+text-accent[^"]*"[^>]*>[^<]*产教研合作[^<]*</a>'
    
    # Replace standalone 高校合作 mobile link
    # Then replace standalone 产教研合作 mobile link
    # We need to find both and replace them together
    
    m_gx = list(re.finditer(pattern_gaoxiao_mobile + '|' + pattern_gaoxiao_mobile2, content, re.DOTALL))
    m_ch = list(re.finditer(pattern_chanjiao_mobile + '|' + pattern_chanjiao_mobile2, content, re.DOTALL))
    
    if m_gx or m_ch:
        # Replace 高校合作 with the grouped items (header + sub-items)
        for m in m_gx:
            # Check if this is not already a grouped header
            if 'fa-university' not in m.group():
                content = content.replace(m.group(), mobile_items)
        
        # Remove standalone 产教研合作 mobile link (already included in grouped items)
        for m in m_ch:
            content = content.replace(m.group(), '')
        
        print(f'UPDATED mobile: {filepath}')
    
    # Write back if changed
    if content != original:
        open(fullpath, 'w', encoding='utf-8').write(content)
        MODIFIED_FILES.append(filepath)
    else:
        print(f'NO CHANGE: {filepath}')

print(f'\n=== Modified {len(MODIFIED_FILES)} files ===')
for f in MODIFIED_FILES:
    print(f'  {f}')
