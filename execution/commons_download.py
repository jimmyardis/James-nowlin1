"""Download chosen Wikimedia Commons files (1280px — a standard pre-rendered size; non-standard widths get throttled hard) and record credits.

Usage: python3 commons_download.py picks.json outdir
picks.json: {"slug": "File:Title.jpg", ...}
Writes outdir/<slug>.jpg and outdir/credits.json (title, artist, license, page url).

Notes (learned): Commons returns HTTP 429 on bursts. Metadata for all titles is
fetched in ONE API call; images are fetched one at a time with a pause and long
backoff. Re-running skips files already downloaded (resumable).
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
UA = "JamesNowlinSiteBuild/1.0 (jimmy.ardis@gmail.com)"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(8):
        try:
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 7: raise
            wait = int(e.headers.get("Retry-After") or 0) or 20 * (attempt + 1)
            print(f"  429, waiting {wait}s", flush=True); time.sleep(wait)

picks = json.load(open(sys.argv[1])); out = sys.argv[2]
cpath = f"{out}/credits.json"
credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
def have_file(s):
    f = f"{out}/{s}.jpg"
    return os.path.exists(f) and os.path.getsize(f) > 0
# work on anything missing its image OR its credit line (credits are required for CC BY-SA)
todo = {s: t for s, t in picks.items() if not have_file(s) or s not in credits}
if todo:
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "|".join(todo.values()),
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1280})
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]
    norm = {n["from"]: n["to"] for n in data.get("normalized", [])}
    by_title = {p["title"]: p for p in data["pages"].values()}
    for slug, title in todo.items():
        page = by_title.get(norm.get(title, title))
        if not page or "imageinfo" not in page:
            print("MISSING", slug, title); continue
        ii = page["imageinfo"][0]; m = ii["extmetadata"]
        if not have_file(slug):
            img = get(ii["thumburl"])  # fetch fully BEFORE creating the file, so resume never skips a partial
            open(f"{out}/{slug}.jpg", "wb").write(img)
        credits[slug] = {"title": page["title"].replace("File:", ""),
            "artist": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip(),
            "license": m.get("LicenseShortName", {}).get("value", ""), "page": ii["descriptionurl"]}
        json.dump(credits, open(cpath, "w"), indent=2)
        print("ok", slug, credits[slug]["license"], flush=True); time.sleep(5)
