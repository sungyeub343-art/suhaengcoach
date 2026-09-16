from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
OLD_NAME = ("수행" + "코치").encode()
BRAND_PREFIX = "더세이브 ".encode()
NEW_NAME = BRAND_PREFIX + OLD_NAME
LEGACY_NAME_PATTERN = re.compile(rb"(?<!" + re.escape(BRAND_PREFIX) + rb")" + OLD_NAME)
TEXT_SUFFIXES = {".css", ".html", ".js", ".ps1", ".py", ".svg"}
EXCLUDED_PARTS = {".git", ".vscode", "__pycache__"}


updated_files = 0
updated_occurrences = 0
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
        continue

    content = path.read_bytes()
    occurrence_count = len(LEGACY_NAME_PATTERN.findall(content))
    if occurrence_count == 0:
        continue

    path.write_bytes(LEGACY_NAME_PATTERN.sub(NEW_NAME, content))
    updated_files += 1
    updated_occurrences += occurrence_count

print(f"Updated {updated_occurrences} brand references across {updated_files} files.")