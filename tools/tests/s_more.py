import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Alpha body.', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Beta body.', 'bbbb22'))
    await a.fs('write', 'gamma.md', ESSAY('Gamma', 'Gamma body.', 'cccc33'))
    await a.connect()

    # D1 deleted outside: the choice, and both ways out work
    await a.open('Beta'); await a.fs('del', 'beta.md'); await a.focus_back()
    info = await a.info()
    check('D1 a delete outside is named, with Put it back', 'deleted outside' in info and 'PUT IT BACK' in info.upper(), info)
    check('D1 save word says so', (await a.ev("$('#save').textContent")) == 'not in folder', await a.ev("$('#save').textContent"))
    await a.type(' After the delete.'); await a.settle()
    check('D1 typing does not bring the file back', await a.read('beta.md') is None, await a.fs('list'))
    await a.ev("$('#fiBack').click()"); await a.wait(900)
    back = await a.read('beta.md') or ''
    check('D1 Put it back restores it in place, id and words', 'bbbb22' in back and 'After the delete.' in back, back)
    await a.fs('del', 'beta.md'); await a.focus_back(); await a.ev("$('#fiLetGo').click()"); await a.wait(900)
    check('D1 Close it leaves it deleted and goes to the Library', await a.read('beta.md') is None and await a.ev('room') == 'library', await a.ev('room'))
    hist = [p for p in await a.fs('list') if 'history/' in p and 'bbbb22' in p]
    texts = [await a.read(p) for p in hist]
    check('D1 its words are in History', any('After the delete.' in (t or '') for t in texts), hist)

    # D2 the sync drive goes offline mid-session: nothing is taken as deleted, nothing lost
    await a.open('Alpha')
    snapshot_fs = await a.ev("localStorage.getItem('__mockfs')")
    await a.fs('rmdir', '')                                   # every file and the folder vanish at once
    await a.type(' Written while offline.'); await a.settle(2500)
    info = await a.info()
    check('D2 offline folder is named, not a delete', "reach" in info.lower() and 'deleted' not in info.lower(), info)
    check('D2 save word: kept here', (await a.ev("$('#save').textContent")) == 'kept here', await a.ev("$('#save').textContent"))
    await a.ev("(s)=>localStorage.setItem('__mockfs',s)", snapshot_fs)   # the drive comes back
    await a.ev("$('#fiRetry').click()"); await a.wait(2500)
    al = await a.read('alpha.md') or ''
    check('D2 back online, the words written offline are saved', 'Written while offline.' in al, al)

    # D3 renamed in Obsidian while Point First was closed: found again on reload
    await a.type(' Before closing.'); await a.settle()
    await a.ev("__fs.failWrites=true"); await a.type(' Unsaved at close.'); await a.wait(700)
    await a.pg.reload(); await a.ev("__fs.failWrites=false")
    await a.fs('mv', 'alpha.md', 'Essays 2026/Alpha (final).md')
    await a.pg.reload(); await a.settle(2500)
    moved = await a.read('Essays 2026/Alpha (final).md') or ''
    check('D3 reload follows a rename made while closed', 'Unsaved at close.' in moved and await a.read('alpha.md') is None, (await a.info(), moved[-60:]))

    # D4 archive: row leaves at once, and the archived view never strands you
    await a.lib()
    await a.ev("(()=>{const r=[...document.querySelectorAll('.lrow')].find(x=>x.querySelector('.lr-t').textContent==='Gamma');r.querySelector('[data-act=stage]').click()})()")
    await a.wait(200); await a.ev("document.querySelector('#smenu [data-act=archive]').click()"); await a.wait(800)
    g = await a.groups()
    check('D4 an archived essay leaves the list at once', not any('Gamma' in x or 'gamma' in x for x in g), g)
    await a.ev("document.querySelector('[data-act=archived]').click()"); await a.wait(300)
    check('D4 archived view lists it', await a.rows() == ['Gamma'], await a.rows())
    await a.fs('del', 'gamma.md')
    await a.ev("document.querySelector('.room[data-room=library]').click()"); await a.wait(900)
    rows = await a.rows()
    check('D4 after deleting the last archived essay, Library click shows the Library', len(rows) >= 1 and not await a.ev('libArchived'), rows)

    # D5 a pause halfway through a new title does not name the file after half a title
    await a.ev("newEssay()"); await a.wait(600)
    await a.pg.keyboard.type('Half a'); await a.wait(1800); await a.pg.keyboard.type(' title, then the rest')
    await a.pg.keyboard.press('Enter'); await a.pg.keyboard.type('First words of the body.'); await a.settle(2500)
    names = [f for f in await a.fs('list') if not f.startswith('.')]
    check('D5 file is named after the whole title', 'Half a title, then the rest.md' in names and 'Half a.md' not in names, names)

    # D6 fewer writes: the daily count goes to the folder at most once a minute
    await a.ev("window.__wt=0;const W=FileSystemWritableFileStream;(()=>{})()")
    before = await a.fs('mtime', '.pointfirst/words-typed.json')
    for i in range(4):
        await a.type(' some more words here and there'); await a.wait(2600)
    after = await a.fs('mtime', '.pointfirst/words-typed.json')
    check('D6 typing in bursts does not rewrite the word count each time', before == after or before is None, (before, after))
    await a.ev("document.dispatchEvent(new Event('visibilitychange'))")   # still visible: no flush
    await a.ev("Object.defineProperty(document,'visibilityState',{get:()=>'hidden',configurable:true});document.dispatchEvent(new Event('visibilitychange'));delete document.visibilityState")
    await a.wait(600)
    check('D6 leaving the tab writes the count', await a.fs('mtime', '.pointfirst/words-typed.json') != after, '')

    # D7 History never thins its safety versions
    kept = await a.ev("""(async()=>{const d=await linked('history',idOf(cur.fm),true,cur.path);const old=Date.now()-3*864e5;
        for(let i=0;i<50;i++){const h=await d.getFileHandle(stampOf(old+i*60e3)+' editing.md',{create:true});const w=await h.createWritable();await w.write('v'+i);await w.close()}
        const h=await d.getFileHandle(stampOf(old+30*60e3+5e3)+' disk-before-overwrite.md',{create:true});const w=await h.createWritable();await w.write('safety');await w.close();
        await thinSnaps(d);const L=await snapsIn(d);return{n:L.length,safe:L.some(s=>s.why==='disk-before-overwrite')}})()""")
    check('D7 thinning keeps safety versions', kept['safe'] and kept['n'] < 52, kept)

    # D8 a second tab is noticed and named once
    b = await c.tab(); await b.wait(1200)
    check('D8 a second tab is noticed', 'another tab' in (await a.toast()).lower() or 'another tab' in (await b.toast()).lower(), (await a.toast(), await b.toast()))

    # D9 the drive is offline when Point First starts: named, and Try again brings it back
    snap = await b.ev("localStorage.getItem('__mockfs')")
    await b.fs('rmdir', ''); await b.ev("setRoom('library')"); await b.reload(); await b.wait(800)
    txt = await b.ev("document.querySelector('#library').innerText")
    check('D9 offline at start: "Can’t find", not an empty Library', 'find' in txt.lower() and 'No essays' not in txt, txt[:160])
    await b.ev("(s)=>localStorage.setItem('__mockfs',s)", snap)
    await b.ev("document.querySelector('[data-act=retryfolder]').click()"); await b.wait(1500)
    check('D9 Try again lists the essays', len(await b.rows()) >= 1, await b.ev("document.querySelector('#library').innerText.slice(0,160)"))

go(suite)
