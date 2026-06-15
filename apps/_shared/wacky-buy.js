/* ============================================================
   111 WACKY APPS — "keep this app" / tip widget
   One script, auto-injected into every app page + the hub.
   Floating button -> modal -> Stripe Payment Link -> /thanks/.
   Soft gate: the apps are free online; paying is a coffee tip
   that unlocks a take-home download. Source is public by nature.
   ============================================================ */
(function () {
  // ----- CONFIG: paste your two Stripe Payment Links below -----
  const WACKY_PAY = {
    single: "https://buy.stripe.com/00w5kF9R4fJr9241Xs4wM00",   // €1 "single Wacky App"
    bundle: "https://buy.stripe.com/bJe3cxd3gcxf924atY4wM01",   // €5 "all 111 Wacky Apps"
    priceSingle: "€1",
    priceBundle: "€5",
  };
  // Set BOTH Payment Links' "after payment" redirect to:  <site>/thanks/
  // -------------------------------------------------------------

  const SELF = document.currentScript;
  if (!SELF) return;
  const ROOT = new URL("../../", SELF.src).href;        // site root, e.g. http://.../
  const LIST_URL = new URL("apps-list.json", SELF.src).href;
  const THANKS = ROOT + "thanks/";

  // which app are we on? (/apps/<slug>/)
  const m = location.pathname.match(/\/apps\/([^/]+)\/?/);
  const curSlug = m ? m[1] : null;

  let APPS = [];           // [{slug,title,emoji}]
  let target = curSlug;    // currently selected single-app target

  // ---------- styles ----------
  const css = `
  .wb-fab{position:fixed;right:16px;bottom:16px;z-index:9000;font-family:var(--mono),monospace;
    font-weight:800;font-size:15px;cursor:pointer;background:var(--pink,#ff5da2);color:#fff;
    border:3px solid var(--ink,#1a1623);border-radius:14px;padding:10px 16px;
    box-shadow:4px 4px 0 var(--ink,#1a1623);transition:transform .06s}
  .wb-fab:hover{background:var(--purple,#7b2ff7)}
  .wb-fab:active{transform:translate(3px,3px);box-shadow:none}
  .wb-overlay{position:fixed;inset:0;z-index:9001;background:rgba(26,22,35,.72);
    display:none;align-items:center;justify-content:center;padding:18px}
  .wb-overlay.open{display:flex}
  .wb-modal{background:#fff;color:var(--ink,#1a1623);border:4px solid var(--ink,#1a1623);
    border-radius:20px;box-shadow:8px 8px 0 var(--ink,#1a1623);max-width:440px;width:100%;
    padding:22px;font-family:var(--sans,system-ui),sans-serif;max-height:90vh;overflow:auto}
  .wb-modal h2{margin:.1em 0 .3em;font-size:24px}
  .wb-modal p{font-size:14px;line-height:1.45;margin:.5em 0}
  .wb-this{background:var(--yellow,#ffd23f);border:3px solid var(--ink,#1a1623);border-radius:12px;
    padding:12px;margin:12px 0;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .wb-this .em{font-size:30px}
  .wb-this .nm{font-weight:900;font-size:17px;flex:1;min-width:120px}
  .wb-btn{font-family:var(--mono),monospace;font-weight:800;font-size:16px;cursor:pointer;
    border:3px solid var(--ink,#1a1623);border-radius:12px;padding:11px 16px;
    box-shadow:3px 3px 0 var(--ink,#1a1623);transition:transform .06s}
  .wb-btn:active{transform:translate(3px,3px);box-shadow:none}
  .wb-btn.go{background:var(--cyan,#16e0bd);color:var(--ink,#1a1623);width:100%;margin-top:4px}
  .wb-btn.bundle{background:var(--purple,#7b2ff7);color:#fff;width:100%}
  .wb-pick{width:100%;margin:6px 0 2px}
  .wb-or{text-align:center;font-family:var(--mono),monospace;opacity:.55;margin:14px 0 8px;font-weight:700}
  .wb-bundle{background:#fff;border:3px dashed var(--ink,#1a1623);border-radius:12px;padding:12px;margin-top:2px}
  .wb-fine{font-size:11.5px;opacity:.65;margin-top:14px;line-height:1.4}
  .wb-x{float:right;cursor:pointer;font-weight:900;font-size:22px;line-height:1;border:none;background:none;color:var(--ink,#1a1623)}
  .wb-warn{background:#ffe0e6;border:2px solid #c0392b;color:#8a1f12;border-radius:10px;padding:8px 10px;font-size:12.5px;margin-top:8px;display:none}
  `;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  // ---------- floating button ----------
  const fab = document.createElement("button");
  fab.className = "wb-fab";
  fab.textContent = curSlug ? "💾 Keep this app" : "💛 Get the apps";
  document.body.appendChild(fab);

  // ---------- modal ----------
  const ov = document.createElement("div");
  ov.className = "wb-overlay";
  ov.innerHTML = `
    <div class="wb-modal" role="dialog" aria-modal="true">
      <button class="wb-x" aria-label="close">×</button>
      <h2>☕ Take it with you</h2>
      <p>Every app here is <b>free in your browser, forever</b>. If one made you smile,
         you can grab a copy to keep on your phone — for the price of a sip of coffee.
         It goes straight to caffeinating the developer and funding more late-night nonsense. 💛</p>
      <div class="wb-this" data-this style="display:none">
        <span class="em"></span>
        <span class="nm"></span>
      </div>
      <button class="wb-btn go" data-go>Get this app — ${WACKY_PAY.priceSingle}</button>
      <label style="display:block;font-size:12.5px;font-weight:700;margin-top:12px">…or pick a different one:</label>
      <select class="wb-pick" data-pick><option value="">— choose an app —</option></select>
      <div class="wb-or">— or —</div>
      <div class="wb-bundle">
        <div style="font-weight:900;font-size:16px">🎁 The whole arcade</div>
        <p style="margin:.3em 0 .6em">All <b>111 apps</b> as one tidy download. ${WACKY_PAY.priceBundle} — cheaper than 5 singles, and you'll never be bored again.</p>
        <button class="wb-btn bundle" data-bundle>Get all 111 — ${WACKY_PAY.priceBundle}</button>
      </div>
      <div class="wb-warn" data-warn>⚠️ Payment links aren't set up yet. (Owner: paste your Stripe links into <code>apps/_shared/wacky-buy.js</code>.)</div>
      <p class="wb-fine">Paid downloads are a thank-you tip — the apps stay free online. After paying you'll be redirected back and your download starts automatically. 📱 <b>Android</b> gets a real installable app (.apk); <b>iPhone &amp; desktop</b> get the self-contained web file (use “Add to Home Screen” to pin it like an app).</p>
    </div>`;
  document.body.appendChild(ov);

  const elThis = ov.querySelector("[data-this]");
  const elGo = ov.querySelector("[data-go]");
  const elPick = ov.querySelector("[data-pick]");
  const elBundle = ov.querySelector("[data-bundle]");
  const elWarn = ov.querySelector("[data-warn]");

  function setTarget(slug) {
    target = slug || null;
    const a = APPS.find(x => x.slug === target);
    if (a) {
      elThis.style.display = "flex";
      elThis.querySelector(".em").textContent = a.emoji;
      elThis.querySelector(".nm").textContent = a.title;
      elGo.textContent = `Get “${a.title}” — ${WACKY_PAY.priceSingle}`;
      elGo.style.display = "block";
      elPick.value = a.slug;
    } else {
      elThis.style.display = "none";
      elGo.style.display = "none";
    }
  }

  function buy(link, code) {
    if (!link) { elWarn.style.display = "block"; return; }
    try { localStorage.setItem("wacky_buy", code); } catch (e) {}
    location.href = link;
  }

  fab.addEventListener("click", () => {
    ov.classList.add("open");
    if (!APPS.length) loadList();
  });
  ov.addEventListener("click", e => { if (e.target === ov) ov.classList.remove("open"); });
  ov.querySelector(".wb-x").addEventListener("click", () => ov.classList.remove("open"));
  document.addEventListener("keydown", e => { if (e.key === "Escape") ov.classList.remove("open"); });

  elPick.addEventListener("change", () => setTarget(elPick.value));
  elGo.addEventListener("click", () => { if (target) buy(WACKY_PAY.single, target); });
  elBundle.addEventListener("click", () => buy(WACKY_PAY.bundle, "__bundle__"));

  function loadList() {
    fetch(LIST_URL).then(r => r.json()).then(list => {
      APPS = list;
      elPick.innerHTML = '<option value="">— choose an app —</option>' +
        list.map(a => `<option value="${a.slug}">${a.emoji} ${a.title}</option>`).join("");
      if (curSlug) setTarget(curSlug);
    }).catch(() => {});
  }
})();
