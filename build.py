#!/usr/bin/env python3
"""Build the 111 Wacky Apps hub index.html from apps.json."""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
apps = json.load(open(os.path.join(ROOT, "apps.json")))
apps.sort(key=lambda a: a["id"])

cats = []
for a in apps:
    if a["cat"] not in cats:
        cats.append(a["cat"])

cards = []
for a in apps:
    cards.append(
        f'<a class="appcard" href="apps/{a["slug"]}/" data-cat="{html.escape(a["cat"])}" '
        f'data-search="{html.escape((a["title"]+" "+a["blurb"]+" "+a["cat"]).lower())}">'
        f'<span class="num">{a["id"]:03d}</span>'
        f'<span class="emoji">{a["emoji"]}</span>'
        f'<span class="t">{html.escape(a["title"])}</span>'
        f'<span class="b">{html.escape(a["blurb"])}</span>'
        f'<span class="tag">{html.escape(a["cat"])}</span>'
        f'</a>'
    )

cat_btns = '<button class="catbtn active" data-cat="*">All ✺</button>' + "".join(
    f'<button class="catbtn" data-cat="{html.escape(c)}">{html.escape(c)}</button>' for c in cats
)

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>111 Wacky Apps</title>
<meta name="description" content="111 unique, useless, wonderful little web toys. Old-internet soul, modern polish.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤪</text></svg>">
<link rel="stylesheet" href="apps/_shared/wacky.css">
<style>
body{{background-image:radial-gradient(var(--ink) 1px,transparent 1px);background-size:24px 24px}}
.hero{{text-align:center;padding:44px 18px 14px}}
.logo{{font-weight:900;line-height:.92;font-size:clamp(46px,12vw,120px);
  letter-spacing:-2px;text-shadow:var(--shadow)}}
.logo .one{{color:var(--pink)}} .logo .two{{color:var(--purple)}} .logo .three{{color:var(--blue)}}
.logo .word{{display:block;color:var(--ink)}}
.tagline{{font-family:var(--mono);font-weight:700;margin-top:10px;font-size:clamp(14px,3vw,20px)}}
.marquee{{overflow:hidden;white-space:nowrap;background:var(--ink);color:var(--yellow);
  font-family:var(--mono);padding:8px 0;border-top:4px solid var(--pink);border-bottom:4px solid var(--cyan);margin-top:18px}}
.marquee span{{display:inline-block;padding-left:100%;animation:scroll 22s linear infinite}}
@keyframes scroll{{to{{transform:translateX(-100%)}}}}
.controls{{max-width:1100px;margin:22px auto 0;padding:0 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center}}
#search{{flex:1;min-width:220px;max-width:420px}}
.cats{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:1100px;margin:14px auto 0;padding:0 18px}}
.catbtn{{font-family:var(--mono);font-weight:700;font-size:13px;cursor:pointer;background:#fff;
  border:3px solid var(--ink);border-radius:999px;padding:6px 14px;box-shadow:var(--shadow-sm)}}
.catbtn.active{{background:var(--purple);color:#fff}}
.grid{{max-width:1100px;margin:22px auto 60px;padding:0 18px;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.appcard{{position:relative;display:flex;flex-direction:column;gap:6px;text-decoration:none;color:var(--ink);
  background:#fff;border:4px solid var(--ink);border-radius:16px;box-shadow:var(--shadow-sm);
  padding:16px;transition:transform .08s,box-shadow .08s,background .15s;min-height:150px}}
.appcard:hover{{transform:translate(-3px,-3px);box-shadow:var(--shadow);background:var(--yellow)}}
.appcard .num{{position:absolute;top:10px;right:12px;font-family:var(--mono);font-size:12px;opacity:.45}}
.appcard .emoji{{font-size:38px}}
.appcard .t{{font-weight:900;font-size:19px;line-height:1}}
.appcard .b{{font-size:13px;opacity:.75;flex:1}}
.appcard .tag{{align-self:flex-start;font-family:var(--mono);font-size:11px;background:var(--ink);color:#fff;
  padding:2px 8px;border-radius:999px}}
.appcard.hide{{display:none}}
footer{{text-align:center;padding:30px 18px 60px;font-family:var(--mono);font-size:13px;opacity:.7}}
.counter{{display:inline-block;background:var(--ink);color:var(--cyan);font-family:var(--mono);
  padding:4px 10px;border-radius:6px;letter-spacing:3px;border:2px solid var(--cyan)}}
#noresult{{text-align:center;font-family:var(--mono);padding:30px;display:none}}
.lucky{{background:var(--pink);color:#fff}}
</style>
</head>
<body>
<div class="hero">
  <div class="logo"><span class="one">1</span><span class="two">1</span><span class="three">1</span>
    <span class="word">WACKY APPS</span></div>
  <div class="tagline">★ {len(apps)} tiny web toys · zero point · maximum fun ★</div>
</div>
<div class="marquee"><span>✦ welcome to the world wide weird ✦ no logins ✦ no ads ✦ no reason ✦ pop some bubbles ✦ pet a cat ✦ generate a band ✦ flip a coin ✦ best viewed with a smile ✦ made with love &amp; nonsense ✦</span></div>

<div class="controls">
  <input id="search" type="text" placeholder="🔎 search the wackiness...">
  <button class="btn lucky" id="lucky">🎲 I'm Feeling Wacky</button>
</div>
<div class="cats">{cat_btns}</div>

<div class="grid" id="grid">
{chr(10).join(cards)}
</div>
<div id="noresult">🦗 ...nothing here. even the crickets left.</div>

<footer>
  you are visitor <span class="counter" id="hits">000000</span><br>
  © 1996–∞ · 111 Wacky Apps · <span class="blink">●</span> handcrafted, one folder at a time
</footer>

<script>
const grid=document.getElementById('grid');
const cards=[...document.querySelectorAll('.appcard')];
const search=document.getElementById('search');
const noresult=document.getElementById('noresult');
let cat='*';
function apply(){{
  const q=search.value.trim().toLowerCase();
  let shown=0;
  cards.forEach(c=>{{
    const okCat = cat==='*'||c.dataset.cat===cat;
    const okQ = !q||c.dataset.search.includes(q);
    const show=okCat&&okQ;
    c.classList.toggle('hide',!show);
    if(show)shown++;
  }});
  noresult.style.display=shown?'none':'block';
}}
search.addEventListener('input',apply);
document.querySelectorAll('.catbtn').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelectorAll('.catbtn').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');cat=b.dataset.cat;apply();
}}));
document.getElementById('lucky').addEventListener('click',()=>{{
  const vis=cards.filter(c=>!c.classList.contains('hide'));
  if(vis.length)location.href=vis[Math.floor(Math.random()*vis.length)].href;
}});
// retro hit counter (purely local, purely silly)
let n=parseInt(localStorage.getItem('wacky_hits')||'13337',10)+1;
localStorage.setItem('wacky_hits',n);
document.getElementById('hits').textContent=String(n).padStart(6,'0');
</script>
</body>
</html>
"""

open(os.path.join(ROOT, "index.html"), "w").write(PAGE)

# lightweight app list for the buy-widget picker
applist = [{"slug": a["slug"], "title": a["title"], "emoji": a["emoji"]} for a in apps]
open(os.path.join(ROOT, "apps", "_shared", "apps-list.json"), "w").write(json.dumps(applist, ensure_ascii=False))

print(f"Built hub with {len(apps)} apps across {len(cats)} categories. Wrote apps-list.json.")
