"""Check every external URL in src/resources.py (and content.py's AGENT links).

Usage: python3 execution/check_links.py
Prints status per URL; exits 1 if any fail. A final redirect is reported so the source can be updated.
Note: some government sites block HEAD or non-browser agents, so we GET with a browser UA.
Sites that still refuse scripts are listed in resources.VERIFIED_MANUALLY after checking them by
search/browser; they're reported as "man" instead of failing. Also flag redirects to non-HTML
(one "utilities" URL silently redirected to a .jpg).
"""
import os, sys, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from resources import RESOURCES, NEW_RESIDENT_STEPS, VERIFIED_MANUALLY  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
urls = {u for _, _, items in RESOURCES for _, u, _, _ in items} | {u for _, _, links in NEW_RESIDENT_STEPS for _, u in links}

def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        r = urllib.request.urlopen(req, timeout=25)
        final = r.geturl()
        ctype = r.headers.get("Content-Type", "")
        if "html" not in ctype and not url.endswith(".pdf"):
            return url, f"NOT-HTML ({ctype})", final
        return url, r.status, final if final.rstrip("/") != url.rstrip("/") else ""
    except urllib.error.HTTPError as e:
        return url, e.code, ""
    except Exception as e:
        return url, f"ERR {type(e).__name__}: {str(e)[:60]}", ""

bad = 0
with ThreadPoolExecutor(8) as ex:
    for url, status, final in sorted(ex.map(check, sorted(urls)), key=lambda x: str(x[1])):
        if status != 200 and url in VERIFIED_MANUALLY:
            print(f"man {status} {url}  (blocks scripts; verified manually)"); continue
        ok = status == 200
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {status} {url}" + (f"  -> {final}" if final else ""))
print(f"\n{len(urls) - bad}/{len(urls)} ok")
sys.exit(1 if bad else 0)
