import os

templates_dir = '/Users/kekio/Desktop/url-shortener-django/shortener/templates'

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Fix split block title tag
            # Case 1: {% block title\n%}
            new_content = content.replace('{% block title\n%}', '{% block title %}')
            # Case 2: {% block title \n%}
            new_content = new_content.replace('{% block title \n%}', '{% block title %}')
            # Case 3: split across lines with content
            if '{% block title' in new_content and '%}' not in new_content.split('{% block title')[1].split('\n')[0]:
                 # It's split. Let's find the closing %}
                 parts = new_content.split('{% block title')
                 fixed_parts = [parts[0]]
                 for part in parts[1:]:
                     if part.strip().startswith('\n%}') or part.strip().startswith('%}'):
                         fixed_parts.append(' ' + part.lstrip('\n').lstrip(' '))
                     else:
                         # More complex split? Just join the first newline
                         fixed_parts.append(' %}' + part.lstrip().lstrip('%}'))
                 # Actually, simpler:
                 # Just find "{% block title\n" and replace with "{% block title %}\n" if the next line starts with "%}"
                 pass

            # Let's use a more robust regex-like replacement for the specific known issue
            import re
            # Matches "{% block title" followed by optional whitespace and a newline, then optional whitespace and "%}"
            new_content = re.sub(r'\{%\s*block\s+title\s*\n\s*%\}', r'{% block title %}', content)
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Fixed {filepath}")
            else:
                # Try another pattern: "{% block title" at end of line, then " %}" at start of next
                new_content = re.sub(r'\{%\s*block\s+title\s*\n%\}', r'{% block title %}', content)
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Fixed (pattern 2) {filepath}")
