import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

TABLE = '| Western Efficacy | Chinese Efficacy |\n|---|:---:|\n| Means / Ends | Conditions / **Consequences** |\n| either \\| or | [source](https://example.com) |'
BODY = 'A paragraph before the table.\n\n' + TABLE + '\n\nA paragraph after the table.'

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'tables.md', ESSAY('Tables', BODY, 'tttt55'))
    await a.connect(); await a.open('Tables')
    kb = a.pg.keyboard
    await a.ev("fx.dim='off';saveFx();setRoom('write')"); await a.wait(200)
    await a.ev("editor.focus();editor.setSelectionRange(0,0)"); await a.wait(300)

    # T1 drawn as a real table while the cursor is elsewhere
    t = await a.ev("(()=>{const w=document.querySelector('#editor .cm-table-wrap');if(!w)return null;return{th:w.querySelectorAll('th').length,td:w.querySelectorAll('td').length,center:w.querySelectorAll('td')[1].style.textAlign,strong:!!w.querySelector('td strong'),link:(w.querySelector('td a')||{}).href||'',pipe:w.querySelectorAll('td')[2].textContent}})()")
    check('T1 a table is drawn as a table', t and t['th'] == 2 and t['td'] == 4, t)
    check('T1 alignment from the dash line', t and t['center'] == 'center', t)
    check('T1 bold and links work in cells', t and t['strong'] and 'example.com' in t['link'], t)
    check('T1 an escaped pipe shows as a pipe', t and t['pipe'].strip() == 'either | or', t)
    await a.pg.screenshot(path='/tmp/table_drawn.png', clip={'x': 250, 'y': 120, 'width': 820, 'height': 360})

    # T2 a click on a cell opens the table with the cursor in that cell
    await a.ev("(()=>{const td=[...document.querySelectorAll('#editor .cm-table-wrap td')][0];const r=td.getBoundingClientRect();window.__pt=[r.left+r.width/2,r.top+r.height/2]})()")
    pt = await a.ev("window.__pt"); await a.pg.mouse.click(pt[0], pt[1]); await a.wait(250)
    pos = await a.ev("editor.selectionStart"); here = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionStart+12)")
    check('T2 click puts the cursor in that cell', here.startswith('Means / Ends'), here)
    check('T2 the table opens to its Markdown', await a.ev("!document.querySelector('#editor .cm-table-wrap')"), '')
    await a.pg.screenshot(path='/tmp/table_open.png', clip={'x': 250, 'y': 120, 'width': 820, 'height': 360})

    # T3 Tab and Shift+Tab move between cells, selecting their words; Tab past the end adds a row
    await kb.press('Tab'); sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('T3 Tab selects the next cell', sel == 'Conditions / **Consequences**', sel)
    await kb.press('Shift+Tab'); sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('T3 Shift+Tab goes back', sel == 'Means / Ends', sel)
    for _ in range(3): await kb.press('Tab')
    await kb.press('Tab'); await kb.type('New cell')
    check('T3 Tab past the last cell adds a row', '\n| New cell  |  |' in await a.ev("editor.value") or '| New cell |' in await a.ev("editor.value"), (await a.ev("editor.value"))[-60:])

    # T4 Enter adds a row; Enter on an empty last row ends the table
    await kb.press('Enter'); await kb.type('Third')
    v = await a.ev("editor.value")
    check('T4 Enter adds a row under this one', '| Third |  |' in v, v[-80:])
    await kb.press('Enter'); await kb.press('Enter')
    v = await a.ev("editor.value")
    check('T4 Enter on an empty last row ends the table', '| Third |  |\n\n' in v and v.count('|  |  |') == 0, v[-90:])
    await kb.type('Written after the table.')
    v = await a.ev("editor.value")
    check('T4 and what follows is its own paragraph', '| Third |  |\n\nWritten after the table.\n\nA paragraph after' in v, v[-120:])

    # T5 Insert table from the palette: blank lines around it, first heading selected
    await a.ev("editor.setSelectionRange(editor.value.indexOf('A paragraph after'),editor.value.indexOf('A paragraph after')+11)")
    await a.ev("(()=>{const i=editor.value.length;editor.setSelectionRange(i,i)})()"); await kb.type(' End.')
    await a.ev("insertTable()"); await kb.type('Claim')
    v = await a.ev("editor.value")
    check('T5 Insert table: blank line before, heading typed in', 'End.\n\n| Claim | Heading |\n|---|---|\n|  |  |' in v, v[-70:])
    await kb.press('Tab'); await kb.type('Evidence'); await kb.press('Tab'); await kb.type('one'); await kb.press('Tab'); await kb.type('two')

    # T6 the file keeps every table exactly as typed
    await a.ev("editor.setSelectionRange(0,0)"); await a.settle()
    disk = await a.read('tables.md') or ''
    check('T6 the file keeps the table as typed', TABLE.split('\n')[0] in disk and '|---|:---:|' in disk and '| Claim | Evidence |' in disk, disk[-160:])
    check('T6 both tables drawn again once the cursor leaves', await a.ev("document.querySelectorAll('#editor .cm-table-wrap').length") == 2, '')

    # T7 counts: words in cells count; pipes, dash lines and bullets do not
    check('T7 bullets are not words', await a.ev("countWords('- one\\n- two\\n---')") == 2, await a.ev("countWords('- one\\n- two\\n---')"))
    n = await a.ev("countWords('| a cat | the dog |\\n|---|---|\\n| one | two |')")
    check('T7 table words count, its marks do not', n == 6, n)
    # Revise reads sentences the skim test's way: a table row is not a sentence, and none runs on
    # into the line after the table.
    k = await a.ev("analyze('| a cat sat | the dog ran |\\n|---|---|\\n| one fish | two fish |\\nNext line here.',mode).sents.map(r=>r.open.join(' '))")
    check('T7 table rows are not sentences, and the line after a table stands alone', k == ['Next line here.'], k)

    # T8 Publish turns tables into HTML tables
    await a.ev("openPublish('html')"); await a.wait(400)
    html = await a.ev("pubData.html")
    check('T8 Publish HTML has the tables', html.count('<table>') == 2, html[:120])
    await a.ev("closePub()")

    # T9 Tab outside a list or table stays in the essay and indents the paragraph by an em space,
    # Shift+Tab takes it back; Esc then Tab leaves the page
    await a.ev("editor.focus();editor.setSelectionRange(5,5)"); await kb.press('Tab')
    check('T9 Tab in a paragraph stays in the essay and indents it', await a.ev("editor.hasFocus") and (await a.ev("editor.value")).startswith('\u2003A paragraph before'), await a.ev("document.activeElement.className"))
    await kb.press('Shift+Tab')
    check('T9 Shift+Tab takes the indent back', (await a.ev("editor.value")).startswith('A paragraph before'), (await a.ev("editor.value"))[:30])
    await kb.press('Escape'); await kb.press('Tab')
    check('T9 Esc then Tab leaves the page', not await a.ev("editor.hasFocus"), '')

    # T10 arrowing down into a table opens it
    await a.ev("editor.focus();editor.setSelectionRange(5,5)")
    for _ in range(3): await kb.press('ArrowDown')
    check('T10 arrow keys open a table they reach', await a.ev("document.querySelectorAll('#editor .cm-table-wrap').length") == 1, await a.ev("editor.selectionStart"))

    # T11 dark theme drawing
    await a.ev("editor.setSelectionRange(0,0);applyTheme('dark')"); await a.wait(300)
    await a.pg.screenshot(path='/tmp/table_dark.png', clip={'x': 250, 'y': 120, 'width': 820, 'height': 360})
    await a.ev("applyTheme('system')")

go(suite)
