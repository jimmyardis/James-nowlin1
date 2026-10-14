"""Build the James Nowlin static site into docs/ (served by GitHub Pages).

Usage:
  python3 execution/build_site.py                      # GitHub Pages project URL
  SITE_URL=https://jamesnowlin.com BASE_PATH= python3 execution/build_site.py   # custom domain

Inputs:  src/content.py (all copy), src/assets/ (css, js, web fonts), src/photos/ (area photos,
         credits.json from commons_download.py, headshot.png), src/build-fonts/ (share image)
Outputs: docs/ — every page, optimized images, sitemap.xml, robots.txt, llms.txt, CNAME (if custom).
"""
import datetime, html, json, math, os, shutil, sys, urllib.parse
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from content import AGENT, AREAS, FAQ, SITE_NAME  # noqa: E402

SITE_URL = os.environ.get("SITE_URL", "https://jimmyardis.github.io/james-nowlin1").rstrip("/")
BASE = os.environ.get("BASE_PATH", "/james-nowlin1").rstrip("/")
OUT = os.path.join(ROOT, "docs")
TMP = os.path.join(ROOT, ".tmp")
TODAY = datetime.date.today().isoformat()
AREA_BY_SLUG = {a["slug"]: a for a in AREAS}
PHOTOS = os.path.join(ROOT, "src", "photos")      # area photos + headshot (committed)
FONTS = os.path.join(ROOT, "src", "build-fonts")  # TTFs used only to draw the share image
CREDITS = json.load(open(os.path.join(PHOTOS, "credits.json")))

e = html.escape
def u(path):  # site-relative link
    return f"{BASE}{path}"
def absu(path):
    return f"{SITE_URL}{path}"
def tel():
    return f"tel:{AGENT['phone_e164']}"
def sms(body=""):
    return f"sms:{AGENT['phone_e164']}" + (f"?&body={urllib.parse.quote(body)}" if body else "")

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
def build_images():
    img_out = os.path.join(OUT, "img"); os.makedirs(img_out, exist_ok=True)
    # Headshot (only a 319px original exists — ask James for a larger one)
    hs = Image.open(os.path.join(PHOTOS, "headshot.png")).convert("RGB")
    hs.save(os.path.join(img_out, "james-nowlin.webp"), quality=88)
    hs.save(os.path.join(img_out, "james-nowlin.jpg"), quality=88)
    # Area photos: 1280 + 720 widths, webp + jpg
    for a in AREAS:
        if not a.get("_has_photo"): continue
        src = os.path.join(PHOTOS, a["photo"] + ".jpg")
        im = Image.open(src).convert("RGB")
        a["photo_size"] = im.size
        for w in (1280, 720):
            r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(os.path.join(img_out, f"{a['slug']}-{w}.webp"), quality=80)
            r.save(os.path.join(img_out, f"{a['slug']}-{w}.jpg"), quality=82, optimize=True, progressive=True)
    build_share_image(img_out, hs)

def build_share_image(img_out, hs):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#1E3A3B")
    d = ImageDraw.Draw(im)
    try:
        big = ImageFont.truetype(os.path.join(FONTS, "Archivo-ExtraBold-Expanded.ttf"), 76)
        try: big.set_variation_by_axes([125, 800])
        except Exception: pass
        med = ImageFont.truetype(os.path.join(FONTS, "SourceSerif4-Regular.ttf"), 36)
        small = ImageFont.truetype(os.path.join(FONTS, "Archivo-Medium.ttf"), 26)
    except OSError:
        big = med = small = ImageFont.load_default()
    face = hs.resize((420, 420), Image.LANCZOS)
    im.paste(face, (W - 420 - 70, (H - 420) // 2))
    d.rectangle([W - 420 - 70 - 14, (H - 420) // 2 + 30, W - 420 - 70 - 8, (H + 420) // 2 - 30], fill="#C6A24E")
    d.text((70, 150), "James Nowlin", font=big, fill="#F2F5F1")
    d.text((70, 260), "Real estate in Columbia, Lexington", font=med, fill="#DCE6E1")
    d.text((70, 306), "and Lake Murray, SC", font=med, fill="#DCE6E1")
    d.text((70, 420), AGENT["phone_display"], font=small, fill="#C6A24E")
    d.text((70, 462), AGENT["brokerage"], font=small, fill="#9DBDBA")
    im.save(os.path.join(img_out, "share.jpg"), quality=88)

def picture(slug, alt, eager=False, sizes="100vw"):
    return (f'<picture><source type="image/webp" srcset="{u(f"/img/{slug}-720.webp")} 720w, {u(f"/img/{slug}-1280.webp")} 1280w" sizes="{sizes}">'
            f'<img src="{u(f"/img/{slug}-1280.jpg")}" srcset="{u(f"/img/{slug}-720.jpg")} 720w, {u(f"/img/{slug}-1280.jpg")} 1280w" sizes="{sizes}" '
            f'alt="{e(alt)}" width="1280" height="{AREA_BY_SLUG[slug]["_h"]}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async"></picture>')

def credit_line(photo_key):
    c = CREDITS[photo_key]
    who = c["artist"] or "Unknown author"
    return f'Photo: <a href="{e(c["page"])}" rel="nofollow noopener">{e(who)}</a>, {e(c["license"])}, via Wikimedia Commons'

# ---------------------------------------------------------------------------
# The Midlands map — the site's signature element. Pins link to area pages.
# Simple equirectangular projection, corrected for latitude.
# ---------------------------------------------------------------------------
LON0, LON1, LAT0, LAT1 = -81.60, -80.88, 33.88, 34.26
KX = math.cos(math.radians(34.07))
MW = 1000
MH = round(MW * (LAT1 - LAT0) / ((LON1 - LON0) * KX))

def P(lon, lat):
    return ((lon - LON0) / (LON1 - LON0) * MW, (LAT1 - lat) / (LAT1 - LAT0) * MH)

def smooth(points, closed=False):
    """Catmull-Rom -> cubic Bezier path through projected points."""
    pts = [P(*p) for p in points]
    if closed: pts = pts[-1:] + pts + pts[:2]
    else: pts = pts[:1] + pts + pts[-1:]
    dpath = f"M{pts[1][0]:.1f},{pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        dpath += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return dpath + (" Z" if closed else "")

LAKE = [  # hand-traced approximation with irregular coves; schematic, not survey-grade
    (-81.212, 34.055), (-81.228, 34.080), (-81.250, 34.088), (-81.268, 34.100), (-81.292, 34.104),
    (-81.305, 34.122), (-81.322, 34.124), (-81.336, 34.140), (-81.352, 34.132), (-81.375, 34.128),
    (-81.398, 34.124), (-81.420, 34.133), (-81.445, 34.122), (-81.475, 34.116), (-81.505, 34.114),
    (-81.535, 34.106), (-81.566, 34.104), (-81.545, 34.094), (-81.515, 34.096), (-81.492, 34.084),
    (-81.468, 34.080), (-81.445, 34.066), (-81.420, 34.066), (-81.398, 34.055), (-81.372, 34.054),
    (-81.352, 34.040), (-81.330, 34.046), (-81.312, 34.032), (-81.292, 34.040), (-81.272, 34.028),
    (-81.252, 34.038), (-81.232, 34.034)]
RIVERS = {
    "Saluda": [(-81.212, 34.050), (-81.165, 34.032), (-81.115, 34.020), (-81.070, 34.006), (-81.050, 34.000)],
    "Upper Saluda": [(-81.566, 34.104), (-81.590, 34.116), (-81.625, 34.130)],
    "Broad": [(-81.175, 34.300), (-81.140, 34.225), (-81.102, 34.135), (-81.072, 34.060), (-81.050, 34.000)],
    "Congaree": [(-81.050, 34.000), (-81.040, 33.962), (-81.002, 33.928), (-80.950, 33.900), (-80.880, 33.868), (-80.840, 33.855)],
}
ROADS = {  # schematic interstates, drawn faintly for orientation
    "I-26": [(-81.62, 34.235), (-81.40, 34.175), (-81.24, 34.115), (-81.12, 34.040), (-81.06, 33.985), (-80.98, 33.900), (-80.92, 33.840)],
    "I-20": [(-81.62, 33.900), (-81.35, 33.955), (-81.15, 33.975), (-81.06, 34.045), (-80.95, 34.070), (-80.86, 34.110)],
    "I-77": [(-80.92, 33.880), (-80.94, 33.960), (-80.965, 34.060), (-80.985, 34.180), (-81.000, 34.290)],
}

def midlands_map(highlight=None, idp="m"):
    out = [f'<svg class="map" viewBox="0 0 {MW} {MH}" role="img" aria-labelledby="{idp}-t {idp}-d" xmlns="http://www.w3.org/2000/svg">',
           f'<title id="{idp}-t">Map of the Columbia, SC area</title>',
           f'<desc id="{idp}-d">The Broad and Saluda rivers meet at Columbia to form the Congaree, with Lake Murray to the west. Pins mark the areas James Nowlin serves; each links to a local guide.</desc>']
    for name, pts in ROADS.items():
        out.append(f'<path class="road" d="{smooth(pts)}"/>')
        lx, ly = P(*pts[1])
        out.append(f'<text class="road-label" x="{lx:.0f}" y="{ly - 8:.0f}">{name}</text>')
    out.append(f'<path class="lake" d="{smooth(LAKE, closed=True)}"/>')
    for name, pts in RIVERS.items():
        out.append(f'<path class="river" d="{smooth(pts)}"/>')
    for name, (lon, lat), rot in [("Broad River", (-81.128, 34.205), 64), ("Congaree River", (-80.985, 33.915), 28), ("Saluda River", (-81.15, 34.042), 18)]:
        x, y = P(lon, lat)
        out.append(f'<text class="river-label" transform="translate({x:.0f},{y:.0f}) rotate({rot})">{name}</text>')
    for a in AREAS:
        x, y = P(*a["pin"])
        on = " is-on" if highlight == a["slug"] else ""
        anchor = a.get("label_anchor", "start")
        label = a.get("map_label", a["name"])
        cur = ' aria-current="page"' if on else ""
        out.append(f'<a class="pin{on}{" pin-lake" if a.get("is_lake") else ""}" href="{u("/areas/" + a["slug"] + "/")}"{cur}>')
        if a.get("is_lake"):
            out.append(f'<text class="lake-label" x="{x:.0f}" y="{y + a["label_dy"]:.0f}" text-anchor="middle">{e(label)}</text>')
        else:
            out.append(f'<circle class="pin-hit" cx="{x:.0f}" cy="{y:.0f}" r="22"/>')
            out.append(f'<circle class="pin-dot" cx="{x:.0f}" cy="{y:.0f}" r="7"/>')
            out.append(f'<text class="pin-label" x="{x + a["label_dx"]:.0f}" y="{y + a["label_dy"]:.0f}" text-anchor="{anchor}">{e(label)}</text>')
        out.append("</a>")
    out.append("</svg>")
    return "".join(out)

# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
def org():
    return {"@type": "RealEstateAgent", "@id": absu("/#brokerage"), "name": AGENT["brokerage"],
            "url": AGENT["brokerage_url"], "telephone": AGENT["office_phone_e164"], "address": office_address()}

def office_address():
    return {"@type": "PostalAddress", "streetAddress": AGENT["office_street"], "addressLocality": AGENT["office_city"],
            "addressRegion": AGENT["office_region"], "postalCode": AGENT["office_zip"], "addressCountry": "US"}

def agent_schema():
    areas = [{"@type": "City" if not a.get("is_lake") else "Place", "name": a["name"] if not a.get("is_lake") else "Lake Murray",
              "containedInPlace": {"@type": "State", "name": "South Carolina"}} for a in AREAS]
    return [
        {"@type": "RealEstateAgent", "@id": absu("/#agent"), "name": AGENT["name"], "url": absu("/"),
         "image": absu("/img/james-nowlin.jpg"), "telephone": AGENT["phone_e164"], "address": office_address(),
         "areaServed": areas, "parentOrganization": {"@id": absu("/#brokerage")},
         "sameAs": [AGENT["facebook"], AGENT["instagram"], "https://jamesnowlin.myrealtyonegroup.com/"],
         "knowsAbout": ["Home buying in South Carolina", "Home selling in South Carolina", "Mortgage financing",
                        "Lake Murray real estate", "Columbia, SC neighborhoods"]},
        {"@type": "Person", "@id": absu("/#james"), "name": AGENT["name"], "jobTitle": AGENT["job_title"],
         "image": absu("/img/james-nowlin.jpg"), "telephone": AGENT["phone_e164"], "url": absu("/about/"),
         "worksFor": {"@id": absu("/#brokerage")},
         "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                           "name": "South Carolina real estate license", "identifier": AGENT["license"],
                           "recognizedBy": {"@type": "GovernmentOrganization", "name": "South Carolina Real Estate Commission"}},
         "sameAs": [AGENT["facebook"], AGENT["instagram"]]},
        org(),
        {"@type": "WebSite", "@id": absu("/#website"), "name": SITE_NAME, "url": absu("/"), "publisher": {"@id": absu("/#agent")}},
    ]

def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absu(p)} for i, (n, p) in enumerate(items)]}

def faq_schema(qas):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
NAV = [("Areas", "/areas/"), ("Buy", "/buy/"), ("Sell", "/sell/"), ("FAQ", "/faq/"), ("About", "/about/"), ("Contact", "/contact/")]

def crumbs_html(items):
    if len(items) < 2: return ""
    parts = []
    for i, (n, p) in enumerate(items):
        parts.append(f'<li><a href="{u(p)}">{e(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{e(n)}</li>')
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'

def page(path, title, description, body, schema=None, crumbs=None, og_image="/img/share.jpg", nav_key=None):
    graph = agent_schema() + (schema or [])
    if crumbs: graph.append(breadcrumb(crumbs))
    graph.append({"@type": "WebPage", "@id": absu(path), "url": absu(path), "name": title, "description": description,
                  "isPartOf": {"@id": absu("/#website")}, "about": {"@id": absu("/#agent")}, "dateModified": TODAY})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<li><a href="{u(p)}"{" aria-current=\"page\"" if nav_key == p else ""}>{n}</a></li>' for n, p in NAV)
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{absu(path)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{absu(path)}">
<meta property="og:image" content="{absu(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1E3A3B">
<meta name="geo.region" content="US-SC">
<meta name="geo.placename" content="Columbia, South Carolina">
<link rel="icon" href="{u('/favicon.svg')}" type="image/svg+xml">
<link rel="preload" href="{u('/assets/fonts/archivo-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{u('/assets/fonts/sourceserif-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u('/assets/style.css')}?v={TODAY}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-row">
    <a class="brand" href="{u('/')}"><span class="brand-name">James Nowlin</span><span class="brand-sub">Realty ONE Group Reside</span></a>
    <a class="head-call" href="{tel()}"><span class="hc-full">{AGENT['phone_display']}</span><span class="hc-short">Call</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
{crumbs_html(crumbs or [])}
<main id="main">
{body}
</main>
{footer()}
<script src="{u('/assets/site.js')}?v={TODAY}" defer></script>
</body>
</html>
"""

def footer():
    areas = "".join(f'<li><a href="{u("/areas/" + a["slug"] + "/")}">{e(a["name"])}</a></li>' for a in AREAS)
    return f"""<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-who">
      <p class="foot-name">James Nowlin</p>
      <p>Real estate agent, SC license #{AGENT['license']}</p>
      <p><a href="{tel()}">{AGENT['phone_display']}</a> (call or text)</p>
      <p class="foot-social"><a href="{AGENT['facebook']}" rel="noopener">Facebook</a> <a href="{AGENT['instagram']}" rel="noopener">Instagram</a></p>
    </div>
    <div>
      <p class="foot-h">Areas</p>
      <ul class="foot-list">{areas}</ul>
    </div>
    <div>
      <p class="foot-h">Brokerage</p>
      <p><a href="{AGENT['brokerage_url']}" rel="noopener">{AGENT['brokerage']}</a><br>{AGENT['office_street']}<br>{AGENT['office_city']}, {AGENT['office_region']} {AGENT['office_zip']}<br>Office <a href="tel:{AGENT['office_phone_e164']}">{AGENT['office_phone_display']}</a></p>
    </div>
  </div>
  <div class="wrap foot-legal">
    <p><svg class="eho" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 1 10h3v11h16V10h3L12 2zm-5 10h10v2H7v-2zm0 4h10v2H7v-2z"/></svg>Equal Housing Opportunity. James Nowlin is a licensed real estate agent with {AGENT['brokerage']}, which is independently owned and operated. Information on this site is provided for general guidance and is not legal, tax or lending advice.</p>
    <p><a href="{u('/photo-credits/')}">Photo credits</a> <a href="https://jamesnowlin.myrealtyonegroup.com/privacy-policy" rel="noopener">Privacy policy</a></p>
  </div>
</footer>"""

def cta_band(heading="Talk to James", text="Questions about a home, a neighborhood or your next move? Call or text James. He'll get back to you the same day."):
    return f"""<section class="cta-band">
  <div class="wrap cta-inner">
    <h2>{e(heading)}</h2>
    <p>{e(text)}</p>
    <p class="cta-phone"><a href="{tel()}">{AGENT['phone_display']}</a></p>
    <p class="cta-actions"><a class="btn btn-light" href="{tel()}">Call James</a><a class="btn btn-ghost" href="{sms()}">Text James</a></p>
  </div>
</section>"""

def faq_items(qas, level="h3"):
    return "".join(f'<details class="qa"><summary><{level}>{e(q)}</{level}></summary><p>{e(a)}</p></details>' for q, a in qas)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    area_list = "".join(f'<li><a href="{u("/areas/" + a["slug"] + "/")}"><span>{e(a["name"])}</span><span class="county">{e(a.get("list_county", a["county"]))}</span></a></li>' for a in AREAS)
    preview = [FAQ[0][1][0], FAQ[1][1][0], FAQ[3][1][1], FAQ[2][1][0]]
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Columbia-area real estate, with a lender's eye for the details.</h1>
      <p class="lede">James Nowlin is a real estate agent with {AGENT['brokerage']}, helping people buy and sell homes in Columbia, Lexington, Irmo, Chapin and around Lake Murray. He came to real estate from mortgage finance, so your deal is built to close.</p>
      <p class="hero-actions"><a class="btn" href="{tel()}">Call or text {AGENT['phone_display']}</a><a class="btn btn-quiet" href="{AGENT['home_value_url']}" rel="noopener">See what your home is worth</a></p>
    </div>
    <figure class="hero-photo">
      <picture class="hero-frame"><source type="image/webp" srcset="{u('/img/james-nowlin.webp')}"><img src="{u('/img/james-nowlin.jpg')}" alt="James Nowlin, real estate agent in Columbia, SC" width="319" height="319" fetchpriority="high"></picture>
      <figcaption>James Nowlin<br><span>SC license #{AGENT['license']}</span></figcaption>
    </figure>
  </div>
</section>

<section class="map-band" aria-labelledby="where">
  <div class="wrap map-grid">
    <div class="map-copy">
      <h2 id="where">Where James works</h2>
      <p>Three rivers, one big lake and a dozen towns, each with its own taxes, schools and feel. Pick an area for a local guide.</p>
      <ul class="area-list">{area_list}</ul>
    </div>
    <div class="map-wrap">{midlands_map(idp="home-map")}</div>
  </div>
</section>

<section class="split wrap">
  <div>
    <h2>Buying a home</h2>
    <p>From your first showing to the attorney's closing table, James keeps your financing, inspections and due diligence deadlines lined up. Search every MLS listing in the Midlands, then go see the ones worth your Saturday.</p>
    <p class="links"><a href="{u('/buy/')}">How buying works in SC</a><a href="{AGENT['search_url']}" rel="noopener">Search homes for sale</a></p>
  </div>
  <div>
    <h2>Selling a home</h2>
    <p>Pricing comes from recent nearby sales, not wishful thinking. James helps you prepare, handles disclosures and showings, and reads each offer the way a lender will, so you pick the one most likely to close.</p>
    <p class="links"><a href="{u('/sell/')}">How selling works in SC</a><a href="{AGENT['home_value_url']}" rel="noopener">Get a home value estimate</a></p>
  </div>
</section>

<section class="lender wrap" aria-labelledby="lender-h">
  <h2 id="lender-h">Why a mortgage background matters</h2>
  <div class="lender-grid">
    <div><h3>Offers that hold up</h3><p>James knows how underwriters look at income, credit and appraisals, so buyers write offers their loan can actually support.</p></div>
    <div><h3>Fewer surprises at closing</h3><p>He watches the lending timeline alongside the contract dates, and flags trouble early, while there's still time to fix it.</p></div>
    <div><h3>Sellers pick stronger offers</h3><p>The highest price isn't always the best offer. James weighs financing type, contingencies and the buyer's lender before you sign.</p></div>
  </div>
</section>

<section class="faq-preview wrap" aria-labelledby="faq-h">
  <h2 id="faq-h">Common questions</h2>
  {faq_items(preview)}
  <p class="more"><a href="{u('/faq/')}">All questions about buying and selling in SC</a></p>
</section>
{cta_band()}
"""
    return page("/", "James Nowlin | Real Estate Agent in Columbia, Lexington & Lake Murray, SC",
                "James Nowlin helps buyers and sellers in Columbia, Lexington, Irmo, Chapin and Lake Murray, SC. Realty ONE Group Reside agent with a mortgage finance background. Call (803) 949-0229.",
                body, nav_key=None)

def area_figure(a):
    if not a.get("_has_photo"): return ""
    return (f'<figure class="area-photo wrap">{picture(a["slug"], a["photo_alt"], eager=True, sizes="(min-width: 1100px) 1080px, 100vw")}'
            f'<figcaption>{credit_line(a["photo"])}</figcaption></figure>')

def area_page(a):
    path = f"/areas/{a['slug']}/"
    secs = "".join(f'<h2>{e(h)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in a["sections"])
    nearby = "".join(f'<li><a href="{u("/areas/" + s + "/")}">{e(AREA_BY_SLUG[s]["name"])}</a></li>' for s in a["nearby"])
    crumbs = [("Home", "/"), ("Areas", "/areas/"), (a["name"], path)]
    body = f"""
<article class="area">
  <header class="wrap area-head">
    <p class="area-county">{e(a['county'])}</p>
    <h1>{e(a['h1'])}</h1>
    <p class="lede answer">{e(a['answer'])}</p>
  </header>
  {area_figure(a)}
  <div class="wrap area-grid">
    <div class="prose">
      {secs}
      <h2>{e(a['name'])} questions</h2>
      {faq_items(a['faq'])}
    </div>
    <aside class="area-side" aria-label="{e(a['name'])} on the map">
      <div class="side-map">{midlands_map(highlight=a['slug'], idp='side-map')}</div>
      <div class="side-card">
        <p class="side-h">Looking {a.get('prep', 'in')} {e(a['name'])}?</p>
        <p>James can pull current listings, recent sales and tax details for any address.</p>
        <p><a class="btn" href="{tel()}">Call {AGENT['phone_display']}</a></p>
        <p><a class="btn btn-quiet" href="{sms('Hi James, I have a question about ' + a['name'] + '.')}">Text James</a></p>
        <p class="side-link"><a href="{AGENT['search_url']}" rel="noopener">Search homes for sale</a></p>
      </div>
      <div class="side-nearby"><p class="side-h">Nearby</p><ul>{nearby}</ul></div>
    </aside>
  </div>
</article>
{cta_band(f"Buying or selling {a.get('prep', 'in')} {a['name']}?")}
"""
    return path, page(path, a["title"], a["description"], body, schema=[faq_schema(a["faq"]),
        {"@type": "Place", "name": a["name"] if not a.get("is_lake") else "Lake Murray", "containedInPlace": {"@type": "State", "name": "South Carolina"}}],
        crumbs=crumbs, nav_key="/areas/")

def areas_index():
    items = "".join(f"""<li class="area-row"><a href="{u('/areas/' + a['slug'] + '/')}">
      <span class="area-row-name">{e(a['name'])}</span><span class="area-row-county">{e(a['county'])}</span>
      <span class="area-row-text">{e(a['answer'].split('. ')[0])}.</span></a></li>""" for a in AREAS)
    body = f"""
<section class="wrap page-head">
  <h1>Columbia, SC area neighborhoods and towns</h1>
  <p class="lede">The Columbia metro spreads across Richland and Lexington counties and around Lake Murray. County lines, school districts and tax rates shift from one town to the next, so each guide covers what matters before you buy or sell there.</p>
</section>
<section class="wrap areas-layout">
  <div class="map-wrap light">{midlands_map(idp="areas-map")}</div>
  <ul class="area-rows">{items}</ul>
</section>
{cta_band()}
"""
    return page("/areas/", "Columbia, SC Area Guides: Lexington, Irmo, Chapin, Lake Murray & More | James Nowlin",
                "Local guides to the Columbia, SC area: Columbia, Lexington, Irmo, Chapin, Lake Murray, West Columbia and Cayce, Blythewood and Forest Acres. Housing, schools, taxes and commutes.",
                body, crumbs=[("Home", "/"), ("Areas", "/areas/")], nav_key="/areas/",
                schema=[{"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": absu(f"/areas/{a['slug']}/"), "name": a["name"]} for i, a in enumerate(AREAS)]}])

def steps_html(steps):
    return '<ol class="steps">' + "".join(f"<li><h2>{e(h)}</h2><p>{e(p)}</p></li>" for h, p in steps) + "</ol>"

BUY_STEPS = [
    ("Get pre-approved", "Talk to a lender before you tour. A pre-approval tells you what you can borrow and makes your offers credible. James can recommend local lenders and help you understand the numbers, from rate to closing costs."),
    ("Sign a buyer agreement", "Before touring together, you and James sign a written agreement that spells out his services and how he's paid. Compensation is negotiable, and he'll walk you through every line."),
    ("Find the right home", "Set up a search across every MLS listing in the Midlands. James checks each home's county, tax rate and school assignment so you compare true monthly costs."),
    ("Make an offer", "James writes the offer on South Carolina's standard contract forms, with a due diligence period, fee and earnest money set to fit the home and the competition."),
    ("Use your due diligence period", "Schedule the home inspection, termite letter, survey and insurance quote right away. If something isn't right, you can negotiate or walk away during this period."),
    ("Appraisal and loan approval", "Your lender orders the appraisal and finishes underwriting. James tracks these deadlines alongside the contract dates."),
    ("Close with an attorney", "South Carolina requires an attorney to handle the closing. You'll do a final walk-through, sign the documents and get your keys."),
    ("Apply for the 4% assessment", "Right after closing, apply with your county assessor for the 4% legal residence rate on your primary home. It can cut your property tax bill significantly, and it isn't automatic."),
]
SELL_STEPS = [
    ("Price it from real sales", "James prepares a comparative market analysis from recent nearby sales and adjusts for your home's condition and updates. Start with the online estimate if you just want a ballpark."),
    ("Prepare the home", "Small fixes, a deep clean and clearing clutter usually return more than they cost. James will tell you what's worth doing and what to skip."),
    ("Complete your disclosures", "Most SC sellers fill out the Residential Property Condition Disclosure Statement. Being thorough now prevents problems later in the deal."),
    ("Market and show it", "Professional photos, an MLS listing that reaches every agent in the region, and showings scheduled around your life."),
    ("Choose the strongest offer", "James compares price alongside financing type, due diligence terms, the buyer's lender and closing date, so you know which offer is most likely to close."),
    ("Get through due diligence", "Expect an inspection and possibly repair requests. James negotiates on your behalf and keeps the deal on schedule."),
    ("Close", "The closing attorney handles the payoff of your mortgage, the deed and the disbursement of your proceeds."),
]

def buy():
    qas = FAQ[0][1]
    body = f"""
<section class="wrap page-head">
  <h1>How buying a home works in South Carolina</h1>
  <p class="lede answer">Buying a home in South Carolina usually takes 30 to 45 days from accepted offer to closing. You'll get pre-approved, sign a buyer agreement, make an offer with a due diligence period, inspect the home, and close with a licensed attorney, then apply for the 4% primary residence tax rate.</p>
</section>
<section class="wrap guide">{steps_html(BUY_STEPS)}</section>
<section class="wrap faq-preview"><h2>Buyer questions</h2>{faq_items(qas)}</section>
{cta_band("Ready to start looking?")}
"""
    return page("/buy/", "How to Buy a Home in Columbia, SC: Step-by-Step Guide | James Nowlin",
                "A step-by-step guide to buying a home in South Carolina: pre-approval, buyer agreements, due diligence, attorney closings and the 4% tax rate, from Columbia-area agent James Nowlin.",
                body, schema=[faq_schema(qas)], crumbs=[("Home", "/"), ("Buy", "/buy/")], nav_key="/buy/")

def sell():
    qas = FAQ[2][1] + [FAQ[1][1][2]]
    body = f"""
<section class="wrap page-head">
  <h1>How selling a home works in South Carolina</h1>
  <p class="lede answer">Selling a home in South Carolina starts with pricing from recent nearby sales and completing the state's property disclosure form. Then you market the home, choose the offer most likely to close, get through the buyer's due diligence period, and close with an attorney who pays off your loan and sends your proceeds.</p>
  <p><a class="btn" href="{AGENT['home_value_url']}" rel="noopener">See what your home is worth</a></p>
</section>
<section class="wrap guide">{steps_html(SELL_STEPS)}</section>
<section class="wrap faq-preview"><h2>Seller questions</h2>{faq_items(qas)}</section>
{cta_band("Thinking about selling?")}
"""
    return page("/sell/", "How to Sell a Home in Columbia, SC: Seller's Guide | James Nowlin",
                "What selling a home in South Carolina involves: pricing, disclosures, offers, due diligence, closing costs and the deed recording fee, from Columbia-area agent James Nowlin.",
                body, schema=[faq_schema(qas)], crumbs=[("Home", "/"), ("Sell", "/sell/")], nav_key="/sell/")

def faq_page():
    groups = "".join(f'<section class="faq-group"><h2>{e(g)}</h2>{faq_items(qas)}</section>' for g, qas in FAQ)
    allq = [qa for _, qas in FAQ for qa in qas]
    body = f"""
<section class="wrap page-head">
  <h1>Buying and selling a home in the Columbia, SC area: common questions</h1>
  <p class="lede">Straight answers about South Carolina real estate, from attorney closings and due diligence to property taxes and disclosures. Have a question that isn't here? Call or text James at <a href="{tel()}">{AGENT['phone_display']}</a>.</p>
</section>
<div class="wrap faq-page">{groups}</div>
{cta_band()}
"""
    return page("/faq/", "South Carolina Home Buying & Selling FAQ | James Nowlin, Columbia SC",
                "Answers to common questions about buying and selling a home in Columbia, SC: attorney closings, due diligence, property taxes, the 4% rate, disclosures and closing costs.",
                body, schema=[faq_schema(allq)], crumbs=[("Home", "/"), ("FAQ", "/faq/")], nav_key="/faq/")

def about():
    body = f"""
<section class="wrap about">
  <div class="about-grid">
    <figure class="about-photo"><picture><source type="image/webp" srcset="{u('/img/james-nowlin.webp')}"><img src="{u('/img/james-nowlin.jpg')}" alt="James Nowlin" width="319" height="319"></picture></figure>
    <div class="prose">
      <h1>About James Nowlin</h1>
      <p class="lede answer">James Nowlin is a real estate agent with {AGENT['brokerage']} in Lexington, SC, serving buyers and sellers across the Columbia metro area. Before real estate, he worked in mortgage finance.</p>
      <p>That lending background shapes how he works. James knows what underwriters look for, how appraisals can move a deal, and where closings tend to stall, so he plans for those moments from the first conversation instead of reacting to them at the end.</p>
      <p>He takes a personal approach. Every client gets direct access to James by phone or text, clear answers in plain language, and a plan built around their timeline, whether that's a first home, a move to the lake or selling a house they've had for decades.</p>
      <h2>Credentials</h2>
      <ul>
        <li>South Carolina real estate license #{AGENT['license']}</li>
        <li>{AGENT['brokerage']}, {AGENT['office_street']}, {AGENT['office_city']}, {AGENT['office_region']} {AGENT['office_zip']}</li>
        <li>Background in mortgage finance</li>
      </ul>
      <p><a class="btn" href="{tel()}">Call or text {AGENT['phone_display']}</a></p>
    </div>
  </div>
</section>
"""
    return page("/about/", "About James Nowlin | Columbia, SC Real Estate Agent",
                "Meet James Nowlin, a Realty ONE Group Reside real estate agent in Lexington, SC with a mortgage finance background, serving buyers and sellers across the Columbia area.",
                body, crumbs=[("Home", "/"), ("About", "/about/")], nav_key="/about/")

def contact():
    opts = "".join(f'<option>{e(a["name"])}</option>' for a in AREAS)
    body = f"""
<section class="wrap contact">
  <h1>Contact James Nowlin</h1>
  <p class="lede">The fastest way to reach James is a call or text to <a href="{tel()}">{AGENT['phone_display']}</a>.</p>
  <div class="contact-grid">
    <form class="msg" id="msg" novalidate>
      <h2>Send James a text</h2>
      <p class="hint">Fill this in and your phone's messaging app opens with the text ready to send.</p>
      <label for="m-name">Your name</label><input id="m-name" name="name" autocomplete="name" required>
      <label for="m-goal">I'm looking to</label>
      <select id="m-goal" name="goal"><option>buy a home</option><option>sell a home</option><option>buy and sell</option><option>ask a question</option></select>
      <label for="m-area">Area</label><select id="m-area" name="area"><option>Not sure yet</option>{opts}</select>
      <label for="m-note">Anything else? (optional)</label><textarea id="m-note" name="note" rows="3"></textarea>
      <p class="form-error" id="m-err" role="alert" hidden>Add your name so James knows who's texting.</p>
      <button class="btn" type="submit" data-phone="{AGENT['phone_e164']}">Open text message</button>
      <p class="hint">On a computer? Call <a href="{tel()}">{AGENT['phone_display']}</a> or use the <a href="{AGENT['rog_contact_url']}" rel="noopener">email form</a>.</p>
    </form>
    <div class="contact-side">
      <h2>Office</h2>
      <p>{AGENT['brokerage']}<br>{AGENT['office_street']}<br>{AGENT['office_city']}, {AGENT['office_region']} {AGENT['office_zip']}<br>Office <a href="tel:{AGENT['office_phone_e164']}">{AGENT['office_phone_display']}</a></p>
      <h2>Tools</h2>
      <ul class="plain"><li><a href="{AGENT['home_value_url']}" rel="noopener">Home value estimate</a></li><li><a href="{AGENT['search_url']}" rel="noopener">Search homes for sale</a></li><li><a href="{AGENT['app_url']}" rel="noopener">Get James's ONE app</a></li></ul>
      <h2>Follow</h2>
      <ul class="plain"><li><a href="{AGENT['facebook']}" rel="noopener">Facebook</a></li><li><a href="{AGENT['instagram']}" rel="noopener">Instagram</a></li></ul>
    </div>
  </div>
</section>
"""
    return page("/contact/", "Contact James Nowlin | Real Estate Agent, Columbia & Lexington SC",
                "Call or text James Nowlin at (803) 949-0229. Realty ONE Group Reside, 5300-B Sunset Blvd., Lexington, SC 29072.",
                body, crumbs=[("Home", "/"), ("Contact", "/contact/")], nav_key="/contact/",
                schema=[{"@type": "ContactPage", "url": absu("/contact/"), "about": {"@id": absu("/#agent")}}])

def credits_page():
    rows = "".join(f'<li>{e(a["name"])}: <a href="{e(CREDITS[a["photo"]]["page"])}" rel="nofollow noopener">{e(CREDITS[a["photo"]]["title"])}</a> by {e(CREDITS[a["photo"]]["artist"] or "Unknown author")}, {e(CREDITS[a["photo"]]["license"])}</li>' for a in AREAS if a.get("_has_photo"))
    body = f"""<section class="wrap prose page-head"><h1>Photo credits</h1>
<p>Area photographs come from Wikimedia Commons and are used under the licenses shown. They have been resized for the web.</p><ul>{rows}</ul></section>"""
    return page("/photo-credits/", "Photo Credits | James Nowlin Real Estate", "Credits and licenses for photographs used on this site.", body,
                crumbs=[("Home", "/"), ("Photo credits", "/photo-credits/")])

def not_found():
    body = f"""<section class="wrap page-head"><h1>That page isn't here</h1>
<p class="lede">The link may be old or mistyped. Try an <a href="{u('/areas/')}">area guide</a>, the <a href="{u('/faq/')}">FAQ</a>, or call James at <a href="{tel()}">{AGENT['phone_display']}</a>.</p></section>"""
    return page("/404.html", "Page not found | James Nowlin Real Estate", "This page could not be found.", body)

# ---------------------------------------------------------------------------
def write(path, content):
    fp = os.path.join(OUT, path.lstrip("/"))
    if fp.endswith("/"): fp += "index.html"
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "src", "assets"), os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(ROOT, "src", "favicon.svg"), os.path.join(OUT, "favicon.svg"))
    for a in AREAS:  # photo must exist AND have a credit line (CC BY-SA); otherwise the page builds without it
        f = os.path.join(PHOTOS, a["photo"] + ".jpg")
        a["_has_photo"] = os.path.exists(f) and os.path.getsize(f) > 0 and a["photo"] in CREDITS
        if a["_has_photo"]:
            im = Image.open(f); a["_h"] = round(im.height * 1280 / im.width)
        else:
            print(f"WARNING: no usable photo for {a['slug']} ({a['photo']}) — built without it")
    build_images()

    pages = {"/": home(), "/areas/": areas_index(), "/buy/": buy(), "/sell/": sell(), "/faq/": faq_page(),
             "/about/": about(), "/contact/": contact(), "/photo-credits/": credits_page()}
    for a in AREAS:
        p, h = area_page(a); pages[p] = h
    for p, h in pages.items(): write(p, h)
    write("/404.html", not_found())

    prio = {"/": "1.0", "/areas/": "0.9", "/buy/": "0.8", "/sell/": "0.8", "/faq/": "0.8"}
    sm = "".join(f"<url><loc>{absu(p)}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.7' if p.startswith('/areas/') else '0.5')}</priority></url>"
                 for p in pages)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {absu('/sitemap.xml')}\n")
    write("/llms.txt", llms_txt())
    write("/.nojekyll", "")
    if not BASE:  # custom domain
        write("/CNAME", SITE_URL.split("://", 1)[1] + "\n")
    print(f"Built {len(pages) + 1} pages into {OUT} for {SITE_URL}")

def llms_txt():
    lines = [f"# {SITE_NAME}", "",
             f"> James Nowlin is a South Carolina real estate agent (license #{AGENT['license']}) with {AGENT['brokerage']}, "
             f"{AGENT['office_street']}, {AGENT['office_city']}, SC {AGENT['office_zip']}. He helps people buy and sell homes in the "
             f"Columbia, SC metro area and has a background in mortgage finance. Phone (call or text): {AGENT['phone_display']}.", "",
             "## Areas served"]
    lines += [f"- [{a['name']}]({absu('/areas/' + a['slug'] + '/')}): {a['answer']}" for a in AREAS]
    lines += ["", "## Guides",
              f"- [How buying a home works in South Carolina]({absu('/buy/')})",
              f"- [How selling a home works in South Carolina]({absu('/sell/')})",
              f"- [Frequently asked questions]({absu('/faq/')})",
              f"- [About James Nowlin]({absu('/about/')})",
              f"- [Contact]({absu('/contact/')})", "",
              "## Key facts",
              "- South Carolina requires a licensed attorney to conduct real estate closings.",
              "- Primary residences are assessed at 4% for property tax (6% otherwise); owners must apply with the county assessor.",
              "- Most SC sellers must complete the Residential Property Condition Disclosure Statement.",
              f"- Home search: {AGENT['search_url']}",
              f"- Home value estimate: {AGENT['home_value_url']}"]
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    main()
