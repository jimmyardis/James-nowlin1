"""Search Wikimedia Commons for free-licensed photos and list candidates.

Usage: python3 commons_search.py "<query>" [limit]
Prints: title | WxH | license | artist | thumb url
"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request

UA = "JamesNowlinSiteBuild/1.0 (jimmy.ardis@gmail.com)"

def search(q, limit=10):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrnamespace": 6, "gsrsearch": q, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1600,
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    # Commons rate-limits bursts (HTTP 429): back off and retry
    for attempt in range(6):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=30))
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 10 * (attempt + 1))
    out = []
    for p in data.get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        artist = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip()
        out.append({
            "title": p["title"], "w": ii["width"], "h": ii["height"],
            "license": m.get("LicenseShortName", {}).get("value", ""),
            "artist": artist[:80], "thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"),
        })
    return out

if __name__ == "__main__":
    for r in search(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10):
        if r["w"] >= 1000 and r["title"].lower().endswith((".jpg", ".jpeg")):
            print(f'{r["title"]} | {r["w"]}x{r["h"]} | {r["license"]} | {r["artist"]} | {r["thumb"]}')
