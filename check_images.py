import os
import glob
import re

html_files = glob.glob("*.html")

print("Checking all src attributes and background URLs in HTML files...")

missing_count = 0
found_count = 0

broken_links = []

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    sources = re.findall(r'src=["\']([^"\']+)["\']', content) + re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content)
    
    for src in sources:
        if src.startswith("http") or src.startswith("//") or src.startswith("data:") or src.startswith("https:"):
            continue
        
        clean_src = src.split('?')[0].split('#')[0]
        local_path = clean_src.replace('/', os.sep)
        
        if not os.path.exists(local_path):
            broken_links.append((filepath, src, local_path))
            missing_count += 1
        else:
            found_count += 1

print(f"\n--- BROKEN LINKS FOUND ({missing_count}) ---")
for file, src, path in broken_links:
    print(f"File: {file} | Src: {src}")

print(f"\nSummary: {found_count} valid image links, {missing_count} BROKEN image links.")
