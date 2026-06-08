#!/usr/bin/env python3
"""Insert HADS badge into README.md if not already present, then commit + push."""
import os
import subprocess
import sys
from pathlib import Path

BADGE_URL = "https://img.shields.io/badge/docs-HADS%20optimized-4A90E2?style=flat-square&logo=markdown&logoColor=white"
BADGE_LINK = "https://github.com/catcam/hads"
BADGE_MD = f"[![HADS Optimized]({BADGE_URL})]({BADGE_LINK})"
MARKER = "catcam/hads"

readme = Path("README.md")
if not readme.exists():
    print("No README.md found — skipping badge.")
    sys.exit(0)

content = readme.read_text(encoding="utf-8")

if MARKER in content:
    print("HADS badge already present — nothing to do.")
    sys.exit(0)

# Insert badge after the first H1 line (or at the very top if no H1)
lines = content.splitlines(keepends=True)
insert_at = 0
for i, line in enumerate(lines):
    if line.startswith("# "):
        insert_at = i + 1
        break

lines.insert(insert_at, "\n" + BADGE_MD + "\n\n")
readme.write_text("".join(lines), encoding="utf-8")
print(f"Badge inserted at line {insert_at + 1}.")

# Commit and push
repo = os.environ.get("GITHUB_REPOSITORY", "")
token = os.environ.get("GITHUB_TOKEN", "")
actor = os.environ.get("GITHUB_ACTOR", "github-actions")

subprocess.run(["git", "config", "user.name", "HADS Bot"], check=True)
subprocess.run(["git", "config", "user.email", "hads-bot@users.noreply.github.com"], check=True)

if token and repo:
    remote = f"https://x-access-token:{token}@github.com/{repo}.git"
    subprocess.run(["git", "remote", "set-url", "origin", remote], check=True)

subprocess.run(["git", "add", "README.md"], check=True)
result = subprocess.run(["git", "diff", "--cached", "--quiet"])
if result.returncode == 0:
    print("No changes to commit.")
    sys.exit(0)

subprocess.run(["git", "commit", "-m", "docs: add HADS Optimized badge [skip ci]"], check=True)
subprocess.run(["git", "push"], check=True)
print("Badge committed and pushed.")
