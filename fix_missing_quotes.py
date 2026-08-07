import glob
import re

html_files = glob.glob("*.html")

total_fixes = 0

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    new_content = content

    # Fix pattern 1: src="images/path alt="... -> src="images/path" alt="..."
    new_content, c1 = re.subn(
        r'src=["\'](images/[^\s"\'<>]+)\s+alt=',
        r'src="\1" alt=',
        new_content
    )

    # Fix pattern 2: src="images/path\n alt="... -> src="images/path"\n alt="..."
    new_content, c2 = re.subn(
        r'src=["\'](images/[^\s"\'<>]+)[\r\n]+\s*alt=',
        r'src="\1"\n                    alt=',
        new_content
    )

    # Fix pattern 3: any src="images/... where quote was omitted before class or other attr
    new_content, c3 = re.subn(
        r'src=["\'](images/[^\s"\'<>]+)\s+(class=|id=|style=|width=|height=)',
        r'src="\1" \2',
        new_content
    )

    # Fix pattern 4: any src="images/path\n where line ends without closing quote
    new_content, c4 = re.subn(
        r'src=["\'](images/[^\s"\'<>]+)\s*[\r\n]+',
        r'src="\1"\n',
        new_content
    )

    count = c1 + c2 + c3 + c4
    total_fixes += count

    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed missing image quotes in: {filepath} ({count} fixes)")

print(f"Total missing quote fixes: {total_fixes}")
