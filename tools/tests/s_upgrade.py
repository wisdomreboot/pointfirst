import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY, URL
async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Alpha body.', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Beta body.', 'bbbb22'))
    await a.connect(); await a.open('Beta'); await a.settle()
    mt = await a.fs('mtime', 'beta.md')
    # U1 upgrading from the old separate keys, with unsaved words in the old browser copy
    await a.pg.goto(URL.rsplit('/', 1)[0] + '/CHANGELOG.md')      # leave the app; set up what 1.3 leaves behind
    await a.ev("""(mt)=>{localStorage.removeItem('ww:session');localStorage.setItem('ww:file',JSON.stringify({path:'beta.md',lastModified:mt}));
        localStorage.setItem('ww:draft',JSON.stringify('Beta body. Unsaved from the old version.'));localStorage.setItem('ww:title',JSON.stringify('Beta'));localStorage.setItem('ww:own',JSON.stringify(null));localStorage.setItem('ww:room',JSON.stringify('write'))}""", mt)
    await a.pg.goto(URL); await a.settle(2500)
    be = await a.read('beta.md') or ''
    check('UP1 upgrade: the old browser copy reaches its own essay', 'Unsaved from the old version.' in be, be)
    check('UP1 upgrade: no duplicate essay', sorted(f for f in await a.fs('list') if not f.startswith('.')) == ['alpha.md', 'beta.md'], await a.fs('list'))
    check('UP1 upgrade: old keys cleared, one session key', await a.ev("localStorage.getItem('ww:file')===null&&!!localStorage.getItem('ww:session')"), '')
    # U2 browser restart: permission asks again; nothing forgets which essay was open
    await a.type(' After upgrade.'); await a.settle()
    await a.ev("__fs.perm='prompt'"); await a.pg.reload(); await a.wait(1200)
    check('UP2 restart: Library asks to reconnect', 'reconnect' in (await a.ev("document.querySelector('#library').innerText")).lower(), '')
    await a.ev("document.querySelector('[data-act=reconnect]').click()"); await a.wait(1500)
    check('UP2 after Reconnect, the essay is bound again', await a.ev("cur&&cur.path") == 'beta.md', await a.ev("JSON.stringify(store.get('ww:session',null)&&store.get('ww:session',null).file)"))
    await a.ev("setRoom('write')"); await a.type(' And after restart.'); await a.settle()
    check('UP2 typing after Reconnect saves to the same file, no duplicate', 'And after restart.' in (await a.read('beta.md') or '') and len([f for f in await a.fs('list') if not f.startswith('.')]) == 2, await a.fs('list'))
go(suite)
