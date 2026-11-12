#!/usr/bin/env python3
"""Submit every URL in sitemap.xml to IndexNow (Bing, Yandex, Seznam, Naver...).

Run after each deploy:  python3 scripts/indexnow.py
The key file /92df07167f3a1127f9208ef0e9ebefe3.txt must be live on the site first.
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "hiragana-chart.com"
KEY = "92df07167f3a1127f9208ef0e9ebefe3"

with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
    urls = re.findall(r"<loc>([^<]+)</loc>", f.read())

body = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
    "urlList": urls,
}).encode("utf-8")
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as res:
    print("IndexNow:", res.status, "for", len(urls), "URLs")  # 200 or 202 means accepted
