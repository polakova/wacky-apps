#!/usr/bin/env python3
"""Generate take-home downloads for 111 Wacky Apps.

For each app, produce a SELF-CONTAINED standalone HTML file:
  - shared CSS inlined (so it works opened directly from a phone)
  - the buy-widget <script> removed (no broken relative path / button)
  - the "back" link repointed to the live hub
Then bundle every standalone file + a local index into one .zip.
"""
import json, os, re, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
HUB = "http://138.68.81.78:8111/"
apps = json.load(open(os.path.join(ROOT, "apps.json")))
apps.sort(key=lambda a: a["id"])

css = open(os.path.join(ROOT, "apps", "_shared", "wacky.css"), encoding="utf-8").read()
outdir = os.path.join(ROOT, "download")
os.makedirs(outdir, exist_ok=True)

def standalone(html):
    # inline the shared stylesheet
    html = re.sub(r'<link[^>]+href="\.\./_shared/wacky\.css"[^>]*>',
                  "<style>\n" + css + "\n</style>", html)
    # drop the buy widget script (any path to wacky-buy.js)
    html = re.sub(r'<script[^>]+wacky-buy\.js[^>]*></script>\s*', "", html)
    # repoint the back link to the live hub so it still works offline-ish
    html = html.replace('href="../../"', 'href="%s"' % HUB)
    return html

made = []
for a in apps:
    src = os.path.join(ROOT, "apps", a["slug"], "index.html")
    html = open(src, encoding="utf-8").read()
    out = os.path.join(outdir, a["slug"] + ".html")
    open(out, "w", encoding="utf-8").write(standalone(html))
    made.append(a)

# a tidy local index for the bundle
links = "\n".join(
    f'<a href="{a["slug"]}.html">{a["emoji"]} {a["title"]}</a>' for a in made
)
bundle_index = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>111 Wacky Apps — your copy</title>
<style>body{{font-family:system-ui,sans-serif;background:#fdf6e3;color:#1a1623;margin:0;padding:28px;
background-image:radial-gradient(#1a1623 1px,transparent 1px);background-size:22px 22px}}
h1{{font-size:34px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:20px}}
a{{background:#fff;border:3px solid #1a1623;border-radius:12px;padding:14px;text-decoration:none;color:#1a1623;
font-weight:800;box-shadow:3px 3px 0 #1a1623}}a:hover{{background:#ffd23f}}
p{{font-family:monospace}}</style></head><body>
<h1>🤪 111 Wacky Apps — your copy 💛</h1>
<p>Thank you for supporting the dev's coffee fund! Tap any app. Each file is self-contained —
open it in any browser, or use your browser's “Add to Home Screen” to pin it like an app.</p>
<div class="g">{links}</div></body></html>"""
open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(bundle_index)

zip_path = os.path.join(outdir, "wacky-apps-bundle.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(outdir, "index.html"), "111-wacky-apps/index.html")
    for a in made:
        z.write(os.path.join(outdir, a["slug"] + ".html"), f"111-wacky-apps/{a['slug']}.html")

print(f"Built {len(made)} standalone downloads + bundle zip ({os.path.getsize(zip_path)//1024} KB).")

# ---- offline full-site copy for the all-in-one APK (assets/www) ----
import shutil
allin = os.path.join(outdir, "allinone")
if os.path.exists(allin):
    shutil.rmtree(allin)
os.makedirs(os.path.join(allin, "apps", "_shared"))

def strip_buy(html):
    # drop the buy-widget script tag (online-only; pointless inside a paid offline app)
    return re.sub(r'<script[^>]+wacky-buy\.js[^>]*></script>\s*', "", html)

# hub
hub = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
open(os.path.join(allin, "index.html"), "w", encoding="utf-8").write(strip_buy(hub))
# shared assets (no wacky-buy.js)
shutil.copy(os.path.join(ROOT, "apps", "_shared", "wacky.css"), os.path.join(allin, "apps", "_shared", "wacky.css"))
shutil.copy(os.path.join(ROOT, "apps", "_shared", "apps-list.json"), os.path.join(allin, "apps", "_shared", "apps-list.json"))
# each app page (relative ../_shared/wacky.css + back link ../../ still resolve inside www)
for a in made:
    dst = os.path.join(allin, "apps", a["slug"])
    os.makedirs(dst, exist_ok=True)
    src_html = open(os.path.join(ROOT, "apps", a["slug"], "index.html"), encoding="utf-8").read()
    open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(strip_buy(src_html))

print(f"Built offline all-in-one site at {allin} ({len(made)} apps + hub).")
