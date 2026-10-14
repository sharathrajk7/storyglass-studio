"""Build the production site from the prototype: a proper index.html (head tags in <head>) plus assets.

    python3 build.py [--base-url https://storyglass.example]
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "hero-prototype")
OUT = os.path.join(HERE, "public")
base = sys.argv[sys.argv.index("--base-url") + 1].rstrip("/") if "--base-url" in sys.argv else ""

page = open(os.path.join(SRC, "page.html"), encoding="utf-8").read()
head, body, rest = [], [], page.splitlines(keepends=True)
i = 0
while i < len(rest) and re.match(r"\s*<(title|meta|link)\b", rest[i]):
    head.append(rest[i]); i += 1
body = "".join(rest[i:])
head = "".join(head)
if base:  # link previews need absolute URLs
    head = head.replace('content="media/brand/og.jpg"', f'content="{base}/media/brand/og.jpg"')
    head += f'<meta property="og:url" content="{base}/">\n<link rel="canonical" href="{base}/">\n'
head += '<meta property="og:type" content="website">\n<meta name="theme-color" content="#030405">\n'

html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
for f in ("films.json", "favicon.ico"):
    shutil.copy2(os.path.join(SRC, f), OUT)
shutil.copytree(os.path.join(SRC, "media"), os.path.join(OUT, "media"))
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n")
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print(f"built public/ ({size / 1e6:.1f} MB){' for ' + base if base else ''}")
