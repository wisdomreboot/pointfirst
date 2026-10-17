# Test harness v2: a shared simulated folder (fsmock2.js), several tabs, reloads.
import asyncio, json, sys
from playwright.async_api import async_playwright

import os
URL = os.environ.get('PF_URL', 'http://localhost:8765/index.html')
MOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fsmock.js')
FAILS = []

def check(name, ok, detail=''):
    print(('PASS  ' if ok else 'FAIL  ') + name + ('' if ok else '   <-- ' + str(detail)))
    if not ok: FAILS.append(name)

class Tab:
    def __init__(self, pg, errs):
        self.pg, self.errs = pg, errs
    async def ev(self, js, arg=None):
        return await (self.pg.evaluate(js, arg) if arg is not None else self.pg.evaluate(js))
    async def wait(self, ms=300): await self.pg.wait_for_timeout(ms)
    async def fs(self, method, *args): return await self.ev("([m,a])=>__fs[m](...a)", [method, list(args)])
    async def read(self, path): return await self.fs('read', path)
    async def connect(self): await self.ev("pickFolder()"); await self.wait(700)
    async def lib(self): await self.ev("setRoom('library')"); await self.wait(700)
    async def rows(self): return await self.ev("[...document.querySelectorAll('.lrow .lr-t')].map(x=>x.textContent)")
    async def groups(self): return await self.ev("[...document.querySelectorAll('.lgroup')].map(g=>g.querySelector('h2').firstChild.textContent+': '+[...g.querySelectorAll('.lr-t')].map(x=>x.textContent).join(','))")
    async def open(self, title):
        await self.lib()
        ok = await self.ev("(t)=>{const r=[...document.querySelectorAll('.lrow')].find(x=>x.querySelector('.lr-t').textContent===t);if(!r)return false;r.querySelector('[data-act=open]').click();return true}", title)
        await self.wait(800); return ok
    async def type(self, text, at_end=True):
        if at_end: await self.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
        await self.pg.keyboard.type(text)
    async def settle(self, ms=1800): await self.wait(ms)   # past the 1.2s autosave
    async def info(self): return await self.ev("document.querySelector('#fileinfo').innerText")
    async def toast(self): return await self.ev("document.querySelector('#toast').textContent")
    async def reload(self): await self.pg.reload(); await self.wait(1300)
    async def focus_back(self):   # the writer comes back to the tab
        await self.ev("window.dispatchEvent(new Event('focus'));document.dispatchEvent(new Event('visibilitychange'))"); await self.wait(600)

class Ctx:
    def __init__(self, ctx): self.ctx = ctx; self.tabs = []
    async def tab(self):
        pg = await self.ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)
        await pg.goto(URL); await pg.wait_for_timeout(1000)
        t = Tab(pg, errs); self.tabs.append(t); return t

async def _run(fn, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': w, 'height': h})
        await ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=URL.rsplit('/', 1)[0])
        await ctx.add_init_script(path=MOCK)
        c = Ctx(ctx)
        try: await fn(c)
        finally:
            errs = [e for t in c.tabs for e in t.errs]
            check('no script errors', not errs, errs[:5])
            await b.close()

def go(fn, w=1300, h=900):
    asyncio.run(_run(fn, w, h))
    if FAILS: print('\n%d FAILED: %s' % (len(FAILS), ', '.join(FAILS)))
    else: print('\nall passed')

ESSAY = lambda title, body, id='', status='drafting': ('---\n' + (f'pointfirst-id: {id}\n' if id else '') + f'status: {status}\n---\n# {title}\n\n{body}\n')
