from pathlib import Path
marker = 'class="section keyword-guide"'
updated_count = 0
total_with_marker = 0
files_exactly_once = 0
failed_files = []

for path in Path("regions").rglob("*.html"):
    html = path.read_text(encoding="utf-8", errors="ignore")
    count = html.count(marker)
    if count > 0:
        total_with_marker += 1
        if count == 1:
            files_exactly_once += 1
        else:
            failed_files.append((str(path), count))

print("Total HTML files with marker:", total_with_marker)
print("Files with marker exactly once:", files_exactly_once)
if failed_files:
    print("Files with multiple markers:", failed_files)

seoul = Path("regions/seoul-district.html")
ansan = Path("regions/ansan.html")
print("seoul-district.html exists:", seoul.exists())
if seoul.exists():
    print("seoul-district.html contains marker:", marker in seoul.read_text(encoding="utf-8", errors="ignore"))
print("ansan.html exists:", ansan.exists())
if ansan.exists():
    print("ansan.html contains marker:", marker in ansan.read_text(encoding="utf-8", errors="ignore"))