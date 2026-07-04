#!/usr/bin/env python3
"""Script to update all HTML footer blocks across UnitClaw.cn website."""

import re
import os

BASE_DIR = r"C:\Users\49563\WorkBuddy\20260511211326\UnitClaw.cn"

# --- Templates ---

ROOT_FOOTER = '''<footer class="bg-dark text-gray-400">
    <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
                <div class="flex items-center space-x-3 mb-4">
                    <img src="assets/logos/WwRobot-Logo.png" alt="WW-Robot" class="h-10 w-auto" onerror="this.style.display='none'">
                    <span class="text-2xl font-bold text-white">Unit<span class="text-accent">Claw</span>.cn</span>
                </div>
                <p class="text-sm leading-relaxed mb-4">万物拟态，面向高校的 AI+机器人全栈教育平台</p>
                <p class="text-sm leading-relaxed">总部：广州增城区</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">五大产品阵列</h4>
                <div class="space-y-2 text-sm">
                    <a href="products/robots.html" class="block hover:text-white transition-colors">具身智能机器人</a>
                    <a href="products/openarm.html" class="block hover:text-white transition-colors">OpenArm 开源机械臂</a>
                    <a href="products/dexterous-hand.html" class="block hover:text-purple-400 transition-colors">灵巧手</a>
                    <a href="products/embedded-platform.html" class="block hover:text-white transition-colors">多功能实训平台</a>
                    <a href="products/courses.html" class="block hover:text-white transition-colors">课程智能体</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">四大合作模式</h4>
                <div class="space-y-2 text-sm">
                    <a href="solutions/university-cooperation.html" class="block hover:text-white transition-colors">模式零：品牌共建</a>
                    <a href="solutions/education.html" class="block hover:text-white transition-colors">模式一：AI+机器人实训室</a>
                    <a href="solutions/education.html" class="block hover:text-white transition-colors">模式二：产教研赛用一体化</a>
                    <a href="solutions/education.html" class="block hover:text-white transition-colors">模式三：竞赛定制支持</a>
                    <a href="solutions/education.html" class="block hover:text-white transition-colors">模式四：1+X 认证培训</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">联系我们</h4>
                <div class="space-y-2 text-sm">
                    <a href="contact.html" class="block hover:text-white transition-colors">预约演示</a>
                    <a href="about.html" class="block hover:text-white transition-colors">关于我们</a>
                </div>
            </div>
        </div>
    </div>
    <div class="max-w-7xl mx-auto px-6 py-6 border-t border-gray-800 flex flex-wrap justify-between text-xs text-gray-500">
        <span>&copy; 2026 unitclaw.cn All rights reserved.</span>
        <div class="flex space-x-4">
            <a href="privacy.html" class="hover:text-gray-400">隐私政策</a>
            <a href="disclaimer.html" class="hover:text-gray-400">免责声明</a>
        </div>
    </div>
</footer>'''

# For products/: products links go to same dir, everything else gets ../
PRODUCTS_FOOTER = '''<footer class="bg-dark text-gray-400">
    <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
                <div class="flex items-center space-x-3 mb-4">
                    <img src="../assets/logos/WwRobot-Logo.png" alt="WW-Robot" class="h-10 w-auto" onerror="this.style.display='none'">
                    <span class="text-2xl font-bold text-white">Unit<span class="text-accent">Claw</span>.cn</span>
                </div>
                <p class="text-sm leading-relaxed mb-4">万物拟态，面向高校的 AI+机器人全栈教育平台</p>
                <p class="text-sm leading-relaxed">总部：广州增城区</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">五大产品阵列</h4>
                <div class="space-y-2 text-sm">
                    <a href="robots.html" class="block hover:text-white transition-colors">具身智能机器人</a>
                    <a href="openarm.html" class="block hover:text-white transition-colors">OpenArm 开源机械臂</a>
                    <a href="dexterous-hand.html" class="block hover:text-purple-400 transition-colors">灵巧手</a>
                    <a href="embedded-platform.html" class="block hover:text-white transition-colors">多功能实训平台</a>
                    <a href="courses.html" class="block hover:text-white transition-colors">课程智能体</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">四大合作模式</h4>
                <div class="space-y-2 text-sm">
                    <a href="../solutions/university-cooperation.html" class="block hover:text-white transition-colors">模式零：品牌共建</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式一：AI+机器人实训室</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式二：产教研赛用一体化</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式三：竞赛定制支持</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式四：1+X 认证培训</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">联系我们</h4>
                <div class="space-y-2 text-sm">
                    <a href="../contact.html" class="block hover:text-white transition-colors">预约演示</a>
                    <a href="../about.html" class="block hover:text-white transition-colors">关于我们</a>
                </div>
            </div>
        </div>
    </div>
    <div class="max-w-7xl mx-auto px-6 py-6 border-t border-gray-800 flex flex-wrap justify-between text-xs text-gray-500">
        <span>&copy; 2026 unitclaw.cn All rights reserved.</span>
        <div class="flex space-x-4">
            <a href="../privacy.html" class="hover:text-gray-400">隐私政策</a>
            <a href="../disclaimer.html" class="hover:text-gray-400">免责声明</a>
        </div>
    </div>
</footer>'''

# For solutions/: solutions links go to same dir, everything else gets ../
SOLUTIONS_FOOTER = '''<footer class="bg-dark text-gray-400">
    <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
                <div class="flex items-center space-x-3 mb-4">
                    <img src="../assets/logos/WwRobot-Logo.png" alt="WW-Robot" class="h-10 w-auto" onerror="this.style.display='none'">
                    <span class="text-2xl font-bold text-white">Unit<span class="text-accent">Claw</span>.cn</span>
                </div>
                <p class="text-sm leading-relaxed mb-4">万物拟态，面向高校的 AI+机器人全栈教育平台</p>
                <p class="text-sm leading-relaxed">总部：广州增城区</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">五大产品阵列</h4>
                <div class="space-y-2 text-sm">
                    <a href="../products/robots.html" class="block hover:text-white transition-colors">具身智能机器人</a>
                    <a href="../products/openarm.html" class="block hover:text-white transition-colors">OpenArm 开源机械臂</a>
                    <a href="../products/dexterous-hand.html" class="block hover:text-purple-400 transition-colors">灵巧手</a>
                    <a href="../products/embedded-platform.html" class="block hover:text-white transition-colors">多功能实训平台</a>
                    <a href="../products/courses.html" class="block hover:text-white transition-colors">课程智能体</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">四大合作模式</h4>
                <div class="space-y-2 text-sm">
                    <a href="university-cooperation.html" class="block hover:text-white transition-colors">模式零：品牌共建</a>
                    <a href="education.html" class="block hover:text-white transition-colors">模式一：AI+机器人实训室</a>
                    <a href="education.html" class="block hover:text-white transition-colors">模式二：产教研赛用一体化</a>
                    <a href="education.html" class="block hover:text-white transition-colors">模式三：竞赛定制支持</a>
                    <a href="education.html" class="block hover:text-white transition-colors">模式四：1+X 认证培训</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">联系我们</h4>
                <div class="space-y-2 text-sm">
                    <a href="../contact.html" class="block hover:text-white transition-colors">预约演示</a>
                    <a href="../about.html" class="block hover:text-white transition-colors">关于我们</a>
                </div>
            </div>
        </div>
    </div>
    <div class="max-w-7xl mx-auto px-6 py-6 border-t border-gray-800 flex flex-wrap justify-between text-xs text-gray-500">
        <span>&copy; 2026 unitclaw.cn All rights reserved.</span>
        <div class="flex space-x-4">
            <a href="../privacy.html" class="hover:text-gray-400">隐私政策</a>
            <a href="../disclaimer.html" class="hover:text-gray-400">免责声明</a>
        </div>
    </div>
</footer>'''

# For all other subdirectories (robots/, courses/, download/, partnerships/, components/):
# ALL relative paths get ../ prefix
SUBDIR_FOOTER = '''<footer class="bg-dark text-gray-400">
    <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
                <div class="flex items-center space-x-3 mb-4">
                    <img src="../assets/logos/WwRobot-Logo.png" alt="WW-Robot" class="h-10 w-auto" onerror="this.style.display='none'">
                    <span class="text-2xl font-bold text-white">Unit<span class="text-accent">Claw</span>.cn</span>
                </div>
                <p class="text-sm leading-relaxed mb-4">万物拟态，面向高校的 AI+机器人全栈教育平台</p>
                <p class="text-sm leading-relaxed">总部：广州增城区</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">五大产品阵列</h4>
                <div class="space-y-2 text-sm">
                    <a href="../products/robots.html" class="block hover:text-white transition-colors">具身智能机器人</a>
                    <a href="../products/openarm.html" class="block hover:text-white transition-colors">OpenArm 开源机械臂</a>
                    <a href="../products/dexterous-hand.html" class="block hover:text-purple-400 transition-colors">灵巧手</a>
                    <a href="../products/embedded-platform.html" class="block hover:text-white transition-colors">多功能实训平台</a>
                    <a href="../products/courses.html" class="block hover:text-white transition-colors">课程智能体</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">四大合作模式</h4>
                <div class="space-y-2 text-sm">
                    <a href="../solutions/university-cooperation.html" class="block hover:text-white transition-colors">模式零：品牌共建</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式一：AI+机器人实训室</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式二：产教研赛用一体化</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式三：竞赛定制支持</a>
                    <a href="../solutions/education.html" class="block hover:text-white transition-colors">模式四：1+X 认证培训</a>
                </div>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">联系我们</h4>
                <div class="space-y-2 text-sm">
                    <a href="../contact.html" class="block hover:text-white transition-colors">预约演示</a>
                    <a href="../about.html" class="block hover:text-white transition-colors">关于我们</a>
                </div>
            </div>
        </div>
    </div>
    <div class="max-w-7xl mx-auto px-6 py-6 border-t border-gray-800 flex flex-wrap justify-between text-xs text-gray-500">
        <span>&copy; 2026 unitclaw.cn All rights reserved.</span>
        <div class="flex space-x-4">
            <a href="../privacy.html" class="hover:text-gray-400">隐私政策</a>
            <a href="../disclaimer.html" class="hover:text-gray-400">免责声明</a>
        </div>
    </div>
</footer>'''


def find_footer_range(content):
    """Find start and end position of <footer>...</footer> block.
    Returns (start_idx, end_idx) or None."""
    # Find <footer opening tag
    start_match = re.search(r'<footer\b', content)
    if not start_match:
        return None
    
    start_idx = start_match.start()
    
    # Start searching after the opening tag with depth=1
    depth = 1
    pos = start_match.end()
    
    while pos < len(content):
        next_open = content.find('<footer', pos)
        next_close = content.find('</footer>', pos)
        
        if next_close == -1:
            return None  # No closing tag found
        
        if next_open != -1 and next_open < next_close:
            # Nested <footer opening (shouldn't happen but handle it)
            depth += 1
            pos = next_open + len('<footer')
        else:
            depth -= 1
            if depth == 0:
                # Found matching close
                end_idx = next_close + len('</footer>')
                return (start_idx, end_idx)
            pos = next_close + len('</footer>')
    
    return None


def update_file(filepath, new_footer):
    """Replace footer block in a single HTML file."""
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    footer_range = find_footer_range(content)
    if not footer_range:
        print(f"  ERROR: No footer found in {filepath}")
        return False
    
    start, end = footer_range
    new_content = content[:start] + new_footer + content[end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    # --- Root directory files ---
    root_files = [
        "about.html",
        "courses.html",
        "contact.html",
        "news.html",
        "support.html",
        "disclaimer.html",
        "privacy.html",
    ]
    
    # --- products/ directory files ---
    products_files = [
        "products/robots.html",
        "products/openarm.html",
        "products/embedded-platform.html",
        "products/courses.html",
        "products/dexterous-hand.html",
        "products/training-box.html",
    ]
    
    # --- solutions/ directory files ---
    solutions_files = [
        "solutions/education.html",
        "solutions/university-cooperation.html",
    ]
    
    # --- robots/ directory files ---
    robots_files = [
        "robots/index.html",
        "robots/mini-pi.html",
        "robots/mini-hi.html",
        "robots/pi-plus.html",
    ]
    
    # --- Other subdirectory files ---
    other_subdir_files = [
        "courses/index.html",
        "download/index.html",
        "partnerships/university-cooperation.html",
        "partnerships/hightorque.html",
        "partnerships/suiguangming.html",
        "components/dexterous-hand.html",
        "components/index.html",
    ]
    
    # Process each group
    all_results = []
    
    print("=" * 60)
    print("=== 处理根目录文件 (7个) ===")
    print("=" * 60)
    for f in root_files:
        path = os.path.join(BASE_DIR, f)
        ok = update_file(path, ROOT_FOOTER)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {f}")
        all_results.append((f, ok))
    
    print()
    print("=" * 60)
    print("=== 处理 products/ 目录文件 (6个) ===")
    print("=" * 60)
    for f in products_files:
        path = os.path.join(BASE_DIR, f)
        ok = update_file(path, PRODUCTS_FOOTER)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {f}")
        all_results.append((f, ok))
    
    print()
    print("=" * 60)
    print("=== 处理 solutions/ 目录文件 (2个) ===")
    print("=" * 60)
    for f in solutions_files:
        path = os.path.join(BASE_DIR, f)
        ok = update_file(path, SOLUTIONS_FOOTER)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {f}")
        all_results.append((f, ok))
    
    print()
    print("=" * 60)
    print("=== 处理 robots/ 目录文件 (4个) ===")
    print("=" * 60)
    for f in robots_files:
        path = os.path.join(BASE_DIR, f)
        ok = update_file(path, SUBDIR_FOOTER)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {f}")
        all_results.append((f, ok))
    
    print()
    print("=" * 60)
    print("=== 处理其他子目录文件 (7个) ===")
    print("=" * 60)
    for f in other_subdir_files:
        path = os.path.join(BASE_DIR, f)
        ok = update_file(path, SUBDIR_FOOTER)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {f}")
        all_results.append((f, ok))
    
    # Summary
    print()
    print("=" * 60)
    print("=== 处理完成 ===")
    print("=" * 60)
    ok_count = sum(1 for _, ok in all_results if ok)
    fail_count = sum(1 for _, ok in all_results if not ok)
    print(f"  成功: {ok_count} 个文件")
    print(f"  失败: {fail_count} 个文件")
    print(f"  总计: {len(all_results)} 个文件")


if __name__ == "__main__":
    main()
