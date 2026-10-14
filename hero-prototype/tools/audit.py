"""Responsive audit of the site: automated layout checks on many devices + per-section screenshots.

    python audit.py <outdir> [shots]      # 'shots' also saves section screenshots for the key devices
"""
import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

C = "/Applications/motionVFX/Google Chrome.app/Contents/MacOS/Google Chrome"
URL = "http://localhost:8790/?nointro"
OUT = sys.argv[1]
SHOTS = len(sys.argv) > 2
# name, width, height, touch
DEVICES = [
    ("phone-320", 320, 568, True), ("phone-360", 360, 800, True), ("phone-375", 375, 667, True),
    ("phone-390", 390, 844, True), ("phone-430", 430, 932, True), ("phone-land-844", 844, 390, True),
    ("ipad-mini-768", 768, 1024, True), ("ipad-air-820", 820, 1180, True), ("ipad-pro-1024", 1024, 1366, True),
    ("ipad-land-1180", 1180, 820, True), ("ipad-land-1024", 1024, 768, True),
    ("laptop-1280", 1280, 800, False), ("laptop-1366", 1366, 768, False), ("laptop-1440", 1440, 900, False),
    ("desktop-1920", 1920, 1080, False), ("desktop-2560", 2560, 1440, False),
]
KEY = {"phone-320", "phone-390", "ipad-air-820", "ipad-land-1180", "laptop-1366", "desktop-1920", "phone-land-844"}
SECTIONS = ["#top", "section[aria-labelledby=problem-h]", "section[aria-labelledby=jobs-h]",
            "section[aria-labelledby=proof-h]", "#films", "#case", "#index", "section[aria-labelledby=ship-h]",
            "section[aria-labelledby=obj-h]", "#brief", "footer.foot"]

CHECK = r"""
(touch) => {
  const vw = document.documentElement.clientWidth, vh = innerHeight;
  const out = { vw, scrollW: document.documentElement.scrollWidth, overflow: [], tiny: [], tap: [], overlapTop: [] };
  const desc = (el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' "' + (el.textContent || '').trim().slice(0, 30) + '"';
  const clipped = (el) => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const o = getComputedStyle(a); if (/(hidden|clip|auto|scroll)/.test(o.overflowX + o.overflow)) return true; } return false; };
  for (const el of document.querySelectorAll('main *, .nav *, .player *')) {
    if (el.closest('[hidden], .sr-only, .hp, svg, datalist, option')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if ((r.right > vw + 1 || r.left < -1) && !clipped(el) && cs.position !== 'fixed') out.overflow.push(desc(el) + ` [${Math.round(r.left)}..${Math.round(r.right)}]`);
    const ownText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (ownText && parseFloat(cs.fontSize) < 11) out.tiny.push(desc(el) + ' ' + cs.fontSize);
    if (touch && el.matches('a[href], button, input:not([type=checkbox]), textarea') && !el.closest('.wheel') &&
        (r.height < 40 || r.width < 40)) out.tap.push(desc(el) + ` ${Math.round(r.width)}x${Math.round(r.height)}`);
  }
  // hero: nothing over the menu bar, the kicker clear of the menu bar
  const nav = document.querySelector('.nav').getBoundingClientRect(), k = document.querySelector('.kicker').getBoundingClientRect();
  if (k.top < nav.bottom - 2 && getComputedStyle(document.querySelector('.kicker')).display !== 'none') out.overlapTop.push(`kicker ${Math.round(k.top)} < nav ${Math.round(nav.bottom)}`);
  const b = document.querySelector('.brand').getBoundingClientRect(), l = document.querySelector('.links').getBoundingClientRect();
  if (b.right > l.left - 8) out.overlapTop.push(`brand ${Math.round(b.right)} touches links ${Math.round(l.left)}`);
  const dock = document.querySelector('.dock').getBoundingClientRect();
  if (dock.top < k.bottom) out.overlapTop.push(`dock ${Math.round(dock.top)} over kicker ${Math.round(k.bottom)}`);
  out.uniq = (a) => a;
  for (const key of ['overflow', 'tiny', 'tap']) out[key] = [...new Set(out[key])].slice(0, 12);
  return out;
}
"""


async def main():
    os.makedirs(OUT, exist_ok=True)
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=C, headless=True,
                                    args=["--enable-gpu", "--use-angle=metal", "--ignore-gpu-blocklist",
                                          "--autoplay-policy=no-user-gesture-required"])
        for name, w, h, touch in DEVICES:
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if touch else 1,
                                      is_mobile=touch and w < 1100, has_touch=touch)
            pg = await ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL, wait_until="networkidle")
            await pg.wait_for_timeout(2200)
            res = await pg.evaluate(CHECK, touch)
            res.pop("uniq", None)
            res["errors"] = errs[:3]
            report[name] = res
            flag = "OK " if not (res["overflow"] or res["overlapTop"] or res["scrollW"] > res["vw"]) else "!! "
            print(flag + name, f"scrollW {res['scrollW']}/{res['vw']}", "overflow", len(res["overflow"]),
                  "tiny", len(res["tiny"]), "tap", len(res["tap"]), "top", res["overlapTop"], errs[:1])
            if SHOTS and name in KEY:
                for i, sel in enumerate(SECTIONS):
                    el = await pg.query_selector(sel)
                    if not el:
                        continue
                    await pg.evaluate("(s) => document.querySelector(s).scrollIntoView({block: 'start'})", sel)
                    await pg.wait_for_timeout(700)
                    await pg.screenshot(path=f"{OUT}/{name}_{i:02d}.png")
            await ctx.close()
        await b.close()
    json.dump(report, open(f"{OUT}/report.json", "w"), indent=1)

asyncio.run(main())
