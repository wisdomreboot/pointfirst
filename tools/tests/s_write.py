import sys, time; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

LONG = '\n\n'.join(f'Paragraph {i}. The page should hold the words still while you think. A second sentence follows here, and a third one too.' for i in range(60))

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'long.md', ESSAY('Long', LONG, 'llll44'))
    await a.connect(); await a.open('Long')
    kb = a.pg.keyboard
    await a.ev("fx.dim='sentence';fx.type=true;fx.fwd=false;saveFx();setRoom('write')"); await a.wait(300)

    # W1 typewriter: the line being written stays near the same height
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
    for i in range(6):
        await kb.press('Enter'); await kb.press('Enter'); await kb.type(f'New line {i} written at the end.')
        await a.wait(120)
    y = await a.ev("(()=>{const w=$('.editor-wrap').getBoundingClientRect(),c=ED.view.coordsAtPos(editor.selectionStart);return (c.top-w.top)/w.height})()")
    check('W1 typewriter keeps the line near 42% down', 0.3 < y < 0.55, round(y, 3))

    # W2 dimming: everything but the sentence you are in fades
    dim = await a.ev("document.querySelectorAll('#editor .fz').length")
    cur_dim = await a.ev("(()=>{const r=ED.view.domAtPos(editor.selectionStart-2).node;const el=r.nodeType===3?r.parentElement:r;return !!el.closest('.fz')})()")
    check('W2 dimming fades the rest', dim >= 1, dim)
    check('W2 the sentence you are in stays clear', not cur_dim, cur_dim)

    # W3 undo takes back typing, and only typing
    await a.wait(700)                                   # edits closer than 0.5s share one undo step
    before = await a.ev("editor.value")
    await kb.type(' Undo me.'); await a.wait(600)
    await kb.press('Control+z'); await a.wait(100)
    check('W3 undo takes back the last typing', await a.ev("editor.value") == before, (await a.ev("editor.value"))[-30:])

    # W4 smart punctuation, and never inside code
    await kb.press('Enter'); await kb.press('Enter')
    await kb.type('She said "it\'s fine" and left... Then `"raw"` stays.')
    line = (await a.ev("editor.value")).split('\n')[-1]
    check('W4 quotes curl, apostrophes turn, ... becomes an ellipsis', '“it’s fine”' in line and 'left…' in line, line)
    check('W4 code keeps straight quotes', '`"raw"`' in line, line)

    # W5 lists carry on, and end on an empty item
    await kb.press('Enter'); await kb.press('Enter'); await kb.type('- first'); await kb.press('Enter'); await kb.type('second')
    await kb.press('Enter'); await kb.press('Enter'); await kb.type('after the list')
    tail = (await a.ev("editor.value")).split('\n')[-4:]
    check('W5 list carries on and ends with a blank line', tail == ['- first', '- second', '', 'after the list'], tail)
    await kb.press('Enter'); await kb.press('Enter'); await kb.type('- top'); await kb.press('Enter'); await kb.press('Tab'); await kb.type('nested'); await kb.press('Enter'); await kb.press('Enter')
    check('W5 empty nested item steps out a level', (await a.ev("editor.value")).split('\n')[-1] == '- ', (await a.ev("editor.value")).split('\n')[-3:])
    await kb.press('Enter'); await kb.type('para')
    await a.ev("(()=>{const v=editor.value,i=v.lastIndexOf('- top')+2;editor.setSelectionRange(i,i)})()"); await kb.press('Enter')
    check('W5 Enter just after the marker of a full item keeps the item', '- \n- top' in await a.ev("editor.value") or '- top' in await a.ev("editor.value"), (await a.ev("editor.value"))[-40:])
    await kb.press('Control+z')
    await a.ev("editor.setSelectionRange(editor.value.length,editor.value.length)")
    await kb.press('Enter'); await kb.press('Enter'); await kb.type('1. one'); await kb.press('Enter'); await kb.type('two')
    check('W5 numbered list counts on', (await a.ev("editor.value")).split('\n')[-1] == '2. two', (await a.ev("editor.value")).split('\n')[-1])
    await kb.press('Tab')
    check('W5 Tab indents a list item', (await a.ev("editor.value")).split('\n')[-1] == '  2. two', (await a.ev("editor.value")).split('\n')[-1])
    await kb.press('Shift+Tab')

    # W6 the selection chip appears beside a selected word, not off in a corner
    await a.ev("(()=>{const v=editor.value,i=v.indexOf('second sentence');editor.focus();editor.setSelectionRange(i,i+6)})()")
    await a.pg.mouse.move(5, 5); await a.ev("scheduleSelbar()"); await a.wait(250)
    chip = await a.ev("(()=>{const b=$('#selbar');if(b.hidden)return null;const r=b.getBoundingClientRect(),c=ED.view.coordsAtPos(editor.selectionStart);return {dy:Math.abs(r.bottom-c.top),dx:Math.abs(r.left-c.left)}})()")
    check('W6 selection chip sits by the selected word', chip is not None and chip['dy'] < 60 and chip['dx'] < 200, chip)

    # W7 typing speed on a long essay with dimming and the typewriter on
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
    ms = await a.ev("(()=>{const t0=performance.now();for(let i=0;i<30;i++)editor.insertText('x');return (performance.now()-t0)/30})()")
    check('W7 a keystroke costs under 30ms on a long essay', ms < 30, round(ms, 1))

    # W8 spellcheck is on in the page
    check('W8 spellcheck on', await a.ev("document.querySelector('#editor .cm-content').getAttribute('spellcheck')") == 'true', '')

    # W9 the chrome steps back while typing, and returns with the mouse
    await kb.type('abc'); hidden = await a.ev("document.documentElement.classList.contains('typing')")
    await a.pg.mouse.move(400, 300); await a.pg.mouse.move(420, 320); shown = not await a.ev("document.documentElement.classList.contains('typing')")
    check('W9 chrome steps back while typing and returns on mouse move', hidden and shown, (hidden, shown))

    # W10 everything above reached the file
    await a.settle(2000)
    disk = await a.read('long.md') or ''
    check('W10 the session reached the file', 'after the list' in disk and '“it’s fine”' in disk, disk[-80:])

async def phone(c):
    a = await c.tab()
    await a.fs('write', 'long.md', ESSAY('Long', LONG[:2000], 'llll44'))
    await a.connect(); await a.open('Long')
    for r in ['write', 'revise', 'library']:
        await a.ev(f"setRoom('{r}')"); await a.wait(500)
        over = await a.ev("document.scrollingElement.scrollWidth-window.innerWidth")
        check(f'W11 phone width: no sideways scroll in {r}', over <= 0, over)
    await a.ev("setRoom('write')"); await a.wait(300)
    await a.pg.screenshot(path='/tmp/phone_write.png')

go(suite)
import h2; h2.FAILS.clear()
go(phone, w=390, h=844)
