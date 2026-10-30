#!/usr/bin/env python3
"""Point First check: the page boots cleanly under its own security policy, and the
page-view counter is the published GoatCounter file, counts once on a real address,
never counts locally, and never sends anything from after the # in the address.

    pip install playwright && python3 -m playwright install chromium
    python3 tools/check.py            # checks the copy in this repository
    python3 tools/check.py path/to/site

Exit code 0 means every check passed.
"""
import base64, functools, hashlib, http.server, json, os, re, socket, socketserver, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, ".."))
PAGE = os.path.join(SITE, "index.html")

# GoatCounter's published integrity hash for https://gc.zgo.at/count.v5.js (goatcounter.com/help/countjs-versions).
GC_V5 = "sha384-atnOLvQb9t+jTSipvd75X2yginT4PjVbqDdlJAmxMm+wYElFmeR6EmLP5bYeoRVQ"
GC_ENDPOINT = "https://pointfirst.goatcounter.com/count"
GC_LOCAL = "goatcounter: not counting because of: "

results = []
def expect(name, got, want, why):
    try:
        ok = bool(want(got)) if callable(want) else got == want
    except Exception:
        ok = False
    results.append((name, ok, got, "(condition)" if callable(want) else want, why))

# ---------- the file itself ----------
html = open(PAGE, encoding="utf-8").read()
srcs = re.findall(r'<script\b[^>]*\bsrc\s*=\s*["\']([^"\']+)', html, re.I)
expect("every script is part of this site", [s for s in srcs if re.match(r"^(?:[a-z]+:)?//", s, re.I) or not os.path.isfile(os.path.join(SITE, s))], [],
       "the security policy runs only this site's code: put a library inside index.html (or beside it), never link it from another site")
blocks = re.findall(r'<script\b[^>]*\bdata-goatcounter="([^"]*)"[^>]*>(.*?)</script>', html, re.S | re.I)
expect("one page-view counter, pointing at Point First's dashboard", [b[0] for b in blocks], [GC_ENDPOINT], "exactly one counter, with this site's own address")
if blocks:
    digest = "sha384-" + base64.b64encode(hashlib.sha384(blocks[0][1].encode("utf-8")).digest()).decode()
    expect("the counter is GoatCounter's published count.v5.js, unchanged", digest, GC_V5, "only the published, pinned file may run here")

# ---------- in a browser ----------
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright is missing. Run: pip install playwright && python3 -m playwright install chromium")

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
s = socket.socket(); s.bind(("127.0.0.1", 0)); PORT = s.getsockname()[1]; s.close()
socketserver.ThreadingTCPServer.allow_reuse_address = True
httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), functools.partial(Quiet, directory=SITE))
threading.Thread(target=httpd.serve_forever, daemon=True).start()

def problems_of(page, sink, counted):
    def note(m):
        if m.text.startswith(GC_LOCAL): counted["skipped"] = m.text[len(GC_LOCAL):]
        elif m.type == "error" or "Content Security Policy" in m.text: sink.append(m.text)
    page.on("console", note)
    page.on("pageerror", lambda e: sink.append(str(e)))
    page.on("dialog", lambda d: d.dismiss())

with sync_playwright() as p:
    # 1. A local address, the real policy on: boots cleanly, sends no count.
    b = p.chromium.launch(); ctx = b.new_context(); pg = ctx.new_page()
    errs, counted, sent = [], {}, []
    problems_of(pg, errs, counted)
    pg.on("request", lambda r: sent.append(r.url) if "goatcounter.com" in r.url else None)
    pg.goto("http://127.0.0.1:%d/index.html" % PORT); pg.wait_for_load_state("load"); pg.wait_for_timeout(1500)
    expect("boots cleanly under the security policy", errs, [], "no error and no policy refusal on load")
    expect("no page view is counted from a local address", [counted.get("skipped"), sent], ["localhost", []], "test runs and local copies must never reach the live count")
    ctx.close(); b.close()

    # 2. Opened straight from disk: still one file that runs, and nothing counted.
    b = p.chromium.launch(); ctx = b.new_context(); pg = ctx.new_page()
    errs, counted = [], {}
    problems_of(pg, errs, counted)
    pg.goto("file://" + PAGE); pg.wait_for_load_state("load"); pg.wait_for_timeout(1200)
    expect("runs from disk without errors, uncounted", [errs, counted.get("skipped")], [[], "localfile"], "the downloaded file needs nothing else and counts nothing")
    ctx.close(); b.close()

    # 3. A real-looking address, the real policy on. The counter is intercepted, so nothing
    #    reaches the live dashboard. One count goes out, with nothing from after the #.
    b = p.chromium.launch(args=["--host-resolver-rules=MAP pointfirst.test 127.0.0.1"])
    ctx = b.new_context(); pg = ctx.new_page()
    errs, counted, sent = [], {}, []
    problems_of(pg, errs, counted)
    def stub(route):
        sent.append(route.request.url); route.fulfill(status=204, body="")
    pg.route(re.compile(r"^https://pointfirst\.goatcounter\.com/"), stub)
    pg.goto("http://pointfirst.test:%d/index.html#private-part-must-not-leave" % PORT); pg.wait_for_load_state("load")
    # Wait with Playwright, not time.sleep: the sync API only hands a request to the stub while
    # one of its own calls is running, so a count sent a moment after load would go unseen.
    for _ in range(40):
        if sent: break
        pg.wait_for_timeout(250)
    pg.wait_for_timeout(500)
    expect("a page view is counted once on a real address", len(sent), 1, "the counter runs under the policy and sends one count per page load")
    expect("the count never carries the address after #", [u for u in sent if "private-part" in u or "%23" in u or "#" in u], [], "nothing after # may leave the page")
    expect("the counter causes no errors or policy refusals", errs, [], "the counter must run cleanly with the policy on")
    ctx.close(); b.close()

httpd.shutdown()
failed = [r for r in results if not r[1]]
for name, ok, got, want, why in results:
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else "\n      expected %s, got %s  (%s)" % (json.dumps(want), json.dumps(got)[:400], why)))
print("\n%d of %d checks passed." % (len(results) - len(failed), len(results)))
sys.exit(1 if failed else 0)
