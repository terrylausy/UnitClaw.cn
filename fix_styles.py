"""Standardize style across all UnitClaw.cn pages to match homepage."""
import re, os

BASE = r'C:\Users\49563\WorkBuddy\20260511211326\UnitClaw.cn'

# Standard Tailwind config (from homepage)
STANDARD_COLORS = {
    'primary': '#ffffff',
    'secondary': '#f1f5f9',
    'accent': '#2563eb',
    'light': '#3b82f6',
    'warm': '#d97706',
    'card': '#ffffff',
    'border': '#e2e8f0',
    'accent2': '#7c3aed',
    'dark': '#0F172A',
    'muted': '#64748B',
}

STANDARD_FONT = {
    'sans': ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
    'display': ['JetBrains Mono', 'monospace'],
}

# Standard CSS classes to add (from homepage)
STANDARD_CSS = """
.bg-grid{background-image:linear-gradient(rgba(37,99,235,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(37,99,235,.04) 1px,transparent 1px);background-size:40px 40px}
.glass{background:rgba(255,255,255,.9);backdrop-filter:blur(16px);border:1px solid rgba(0,0,0,.08)}
.card-hover{transition:all .35s cubic-bezier(.4,0,.2,1)}
.card-hover:hover{transform:translateY(-8px);box-shadow:0 20px 40px rgba(37,99,235,.10)}
.text-gradient{background:linear-gradient(135deg,#2563eb,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-glow{background:radial-gradient(ellipse at 50% 0%,rgba(37,99,235,.06) 0%,transparent 70%)}
.tag{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.75rem;font-weight:600;letter-spacing:.05em}
.tag-robot{background:rgba(37,99,235,.08);color:#2563eb;border:1px solid rgba(37,99,235,.20)}
.tag-course{background:rgba(124,58,237,.08);color:#7c3aed;border:1px solid rgba(124,58,237,.20)}
.tag-claw{background:rgba(217,119,6,.08);color:#d97706;border:1px solid rgba(217,119,6,.20)}
.tag-embedded{background:rgba(5,150,105,.08);color:#059669;border:1px solid rgba(5,150,105,.20)}
"""

files_to_fix = [
    'about.html', 'courses.html', 'contact.html', 'news.html',
    'support.html', 'disclaimer.html', 'privacy.html',
    'products/robots.html', 'products/openarm.html', 'products/embedded-platform.html',
    'products/courses.html', 'products/dexterous-hand.html', 'products/training-box.html',
    'robots/index.html', 'robots/mini-pi.html', 'robots/mini-hi.html', 'robots/pi-plus.html',
    'courses/index.html', 'download/index.html',
    'partnerships/university-cooperation.html', 'partnerships/hightorque.html', 'partnerships/suiguangming.html',
    'components/index.html', 'components/dexterous-hand.html',
]

# Skip files already fully standardized (index.html, solutions/*)
skip = ['index.html', 'solutions/education.html', 'solutions/university-cooperation.html']

for f in files_to_fix:
    if f in skip:
        continue
    fp = os.path.join(BASE, f)
    if not os.path.exists(fp):
        print(f'SKIP (not found): {f}')
        continue
    
    content = open(fp, 'r', encoding='utf-8').read()
    original = content
    
    # 1. Fix Tailwind config - add missing colors and fontFamily
    # Find tailwind.config block
    config_match = re.search(r'tailwind\.config\s*=?\s*\{.*?\}(?:\s*;?\s*</script>)?', content, re.DOTALL)
    if not config_match:
        # Some files use inline config: tailwind.config={...}
        config_match = re.search(r'tailwind\.config\s*=\s*\{[^}]+\}', content)
    
    if config_match:
        config_text = config_match.group()
        
        # Add missing colors
        existing_colors = re.findall(r'(\w+):\s*[\'"]#[\w]+[\'"]', config_text)
        missing_colors = {k: v for k, v in STANDARD_COLORS.items() if k not in existing_colors}
        
        if missing_colors:
            # Find colors section
            colors_match = re.search(r'colors:\s*\{([^}]+)\}', config_text)
            if colors_match:
                colors_block = colors_match.group(1)
                # Add missing colors to existing colors block
                for name, value in missing_colors.items():
                    if name not in colors_block:
                        # Add before closing bracket
                        colors_block += f",\n                        {name}: '{value}'"
                new_config = config_text.replace(colors_match.group(1), colors_block)
            else:
                # No colors section at all - add one
                # Find theme.extend section
                extend_match = re.search(r'extend:\s*\{([^}]*)\}', config_text)
                if extend_match:
                    colors_str = ','.join(f"{k}: '{v}'" for k, v in STANDARD_COLORS.items())
                    new_colors = f"\n                    colors: {{\n                        {colors_str}\n                    }},"
                    new_config = config_text.replace(extend_match.group(0), 
                        f"extend: {{{new_colors}\n                    {extend_match.group(1)}\n                }}")
                else:
                    # Completely rewrite config
                    colors_str = ','.join(f"'{k}': '{v}'" for k, v in STANDARD_COLORS.items())
                    new_config = f'''tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        {colors_str}
                    }},
                    fontFamily: {{
                        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
                        display: ['JetBrains Mono', 'monospace'],
                    }}
                }}
            }}
        }}'''
            
            content = content.replace(config_text, new_config)
        
        # Add fontFamily if missing
        if 'fontFamily' not in content or 'Inter' not in content:
            # Need to add fontFamily to config
            config_match2 = re.search(r'tailwind\.config\s*=?\s*\{.*?\}', content, re.DOTALL)
            if config_match2 and 'fontFamily' not in config_match2.group():
                old_config = config_match2.group()
                # Add fontFamily before closing of extend
                fontFamily_add = ''',
                    fontFamily: {
                        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
                        display: ['JetBrains Mono', 'monospace'],
                    }'''
                # Find the extend section closing
                extend_match = re.search(r'extend:\s*\{.*?\}', old_config, re.DOTALL)
                if extend_match:
                    old_extend = extend_match.group()
                    # Insert fontFamily at end of extend
                    new_extend = old_extend.rstrip() + fontFamily_add
                    if new_extend.endswith('}'):
                        new_extend = new_extend[:-1] + fontFamily_add + '\n                }'
                    new_config = old_config.replace(old_extend, new_extend)
                    content = content.replace(old_config, new_config)
    
    # 2. Add missing CSS classes to <style> block
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match:
        existing_css = style_match.group(1)
        missing_css_classes = []
        for line in STANDARD_CSS.strip().split('\n'):
            class_name = re.match(r'\.(\w+)', line)
            if class_name:
                cls = class_name.group(1)
                if f'.{cls}' not in existing_css:
                    missing_css_classes.append(line)
        
        if missing_css_classes:
            new_css = existing_css.rstrip() + '\n' + '\n'.join(missing_css_classes)
            # Handle <style type="text/tailwindcss"> vs regular <style>
            content = content.replace(style_match.group(1), new_css)
    
    # 3. Fix body class - add min-h-screen and antialiased
    body_match = re.search(r'<body\s+class="([^"]*)"', content)
    if body_match:
        body_classes = body_match.group(1)
        if 'min-h-screen' not in body_classes:
            body_classes += ' min-h-screen'
        if 'antialiased' not in body_classes:
            body_classes += ' antialiased'
        content = content.replace(body_match.group(1), body_classes)
    
    # Only write if changed
    if content != original:
        open(fp, 'w', encoding='utf-8').write(content)
        print(f'FIXED: {f}')
    else:
        print(f'NO CHANGE: {f}')

print('\nAll files processed.')
