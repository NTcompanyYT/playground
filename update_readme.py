#!/usr/bin/env python3
import os
import re

README_FILE = "README.md"
START_MARKER = "<!-- PROJECTS_TABLE -->"
END_MARKER = "<!-- /PROJECTS_TABLE -->"

def get_project_info(folder):
    """Extract name and description from a project folder's README."""
    readme_path = os.path.join(folder, "README.md")
    if not os.path.isfile(readme_path):
        return None
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    name = None
    desc = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and name is None:
            name = stripped[2:].strip()
            continue
        if name is not None and stripped and desc is None:
            desc = stripped
            break
    if not name:
        return None
    return name, desc or "*(no description)*"

def generate_table():
    projects = []
    for entry in sorted(os.listdir(".")):
        if not os.path.isdir(entry) or entry.startswith(".") or entry.startswith("_"):
            continue
        info = get_project_info(entry)
        if info:
            name, desc = info
            link = f"[{name}](./{entry}/)"
            projects.append((link, desc))
    if not projects:
        return "| No projects added yet. | Add a folder with a README.md! |\n"
    table = "| Project | Description |\n|--------|-------------|\n"
    for link, desc in projects:
        table += f"| {link} | {desc} |\n"
    return table

def update_readme():
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    new_table = generate_table()
    pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
    replacement = f"{START_MARKER}\n{new_table}\n{END_MARKER}"
    new_content, count = pattern.subn(replacement, content)
    if count == 0:
        print("Markers not found in README. Add <!-- PROJECTS_TABLE --> and <!-- /PROJECTS_TABLE --> in your README.")
        exit(1)
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README table updated!")

if __name__ == "__main__":
    update_readme()
