"""Serve docs/ locally under the GitHub Pages base path and screenshot pages.

Usage: python3 execution/screenshot.py [path ...]   (default: a standard set)
Writes .tmp/shots/<name>-desktop.png and -mobile.png, and prints console errors.
"""
import http.server, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE_PATH", "/james-nowlin1")
serve = os.path.join(ROOT, ".tmp", "serve"); os.makedirs(serve, exist_ok=True)
link = os.path.join(serve, BASE.strip("/") or "site")
if not os.path.islink(link): os.symlink(os.path.join(ROOT, "docs"), link)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = lambda *a, **k: Quiet(*a, directory=serve, **k)
srv = socketserver.TCPServer(("127.0.0.1", 0), Handler); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
paths = sys.argv[1:] or ["/", "/areas/", "/areas/lake-murray-sc/", "/buy/", "/contact/"]
out = os.path.join(ROOT, ".tmp", "shots"); os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, vp in [("desktop", {"width": 1366, "height": 900}), ("mobile", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp, device_scale_factor=1)
        errs = []; pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: errs.append("FAILED " + r.url))
        for path in paths:
            pg.goto(f"http://127.0.0.1:{port}{BASE}{path}", wait_until="networkidle")
            name = path.strip("/").replace("/", "_") or "home"
            pg.screenshot(path=f"{out}/{name}-{label}.png", full_page=True)
            w = pg.evaluate("document.documentElement.scrollWidth")
            print(f"{label} {path} scrollWidth={w}" + (" OVERFLOW" if w > vp["width"] else ""))
        for x in errs: print("  ERR", x)
    b.close()
srv.shutdown()
