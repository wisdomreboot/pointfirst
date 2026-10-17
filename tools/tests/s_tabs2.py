import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY
async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Alpha body.', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Beta body.', 'bbbb22'))
    await a.connect()
    b = await c.tab(); await b.wait(800)
    await a.open('Alpha'); await b.open('Beta'); await a.settle(); await b.settle()
    await b.type(' B-typed.'); await b.wait(1000)      # B's save lands at 1.2s
    await a.type(' A-late.'); await a.wait(650)        # A's browser copy stored, A's save not yet
    print('stored file:', await a.ev("JSON.stringify(store.get('ww:file',null))"), '| draft starts:', (await a.ev("store.get('ww:draft','')"))[:20])
    await a.ev('__fs.failWrites=true')          # the closing tab's last write does not finish
    await a.pg.reload(); await a.ev('__fs.failWrites=false'); await a.settle(3000)
    al, be = await a.read('alpha.md'), await a.read('beta.md')
    check('S10b beta.md never receives Alpha\'s text', 'Alpha body' not in be and 'A-late' not in be, be)
    check('S10b A-late is not lost', 'A-late' in al or 'A-late' in await a.ev('editor.value'), al)
go(suite)
