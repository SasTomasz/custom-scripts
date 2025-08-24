import re
import os

def change_text(filepath, reg_pattern):
    new_lines = []

    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            match = reg_pattern.search(line)
            if match:
                # Replace with [page X]
                page_num = match.group(1)
                new_lines.append(f"[page {page_num}]\n")
            else:
                new_lines.append(line)

    # Create new filename with _modified suffix
    base, ext = os.path.splitext(filepath)
    new_filepath = f"{base}_modified{ext}"

    with open(new_filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    print(f"✅ File saved as: {new_filepath}")

# Regex: capture page number in group(1)
pattern = re.compile(
    r"- Your Highlight on page (\d+) \| Location \d+-\d+ \| Added on .*"
)

# Example usage
change_text(r"C:\Documents\book.txt", pattern)
