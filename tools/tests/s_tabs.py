import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Alpha body.', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Beta body.', 'bbbb22'))
    await a.connect()
    b = await c.tab(); await b.wait(800)

    # S10 two tabs, two essays: a reload never pairs one essay's text with another's file
    await a.open('Alpha'); await b.open('Beta')
    await a.type(' A-typed.'); await a.wait(700)        # A's browser copy is newest
    await b.type(' B-typed.'); await b.wait(700)        # now B's is
    await a.type(' A-again.'); await a.wait(700)
    await b.settle(); await a.settle()
    await a.reload(); await a.settle(2500)
    al, be = await a.read('alpha.md'), await a.read('beta.md')
    check('S10 alpha.md holds only Alpha', 'B-typed' not in al and 'Beta body' not in al, al)
    check('S10 beta.md holds only Beta', 'A-typed' not in be and 'A-again' not in be and 'Alpha body' not in be, be)
    check('S10 A reopens its own essay', 'A-again' in await a.ev('editor.value') or 'Alpha' in await a.ev('doctitle.value'), await a.ev('doctitle.value'))

    # S11 two tabs, the same essay: neither silently overwrites the other
    await a.open('Alpha'); await b.open('Alpha')
    await a.type(' From A.'); await a.settle()
    await b.type(' From B.'); await b.settle()
    al = await a.read('alpha.md')
    files = await a.fs('list'); hist = [await a.read(p) for p in files if 'history/' in p]
    keptA = 'From A.' in al or any('From A.' in (t or '') for t in hist)
    keptB = 'From B.' in al or any('From B.' in (t or '') for t in hist) or 'From B.' in await b.ev('editor.value')
    check('S11 A\'s words survive', keptA, al)
    check('S11 B\'s words survive', keptB, al)
    check('S11 B picked up A\'s save, so both are in the file', 'From A.' in al and 'From B.' in al, al)

    # S14 the whole folder disappears (renamed or deleted in Explorer)
    await a.fs('rmdir', '')
    await a.lib(); await a.wait(600)
    txt = await a.ev("document.querySelector('#library').innerText")
    check('S14 a missing folder is named, not shown as empty', 'No essays in' not in txt, txt[:200])

go(suite)
