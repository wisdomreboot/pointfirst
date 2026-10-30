import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY
import json

# Writing moves. Alt+Up and Alt+Down move the paragraph the cursor is in, or a list item with its
# sub-items, and pasted words stay pasted when they move. Two hyphens become an em dash whenever
# smart punctuation is on. ^Superscript^ and ~subscript~ show on the page and in Publish. The
# palette works by keyword: Go to, Insert, Format, Move, Stage. An essay file ends on a line
# break, so the page does too.

BODY = 'First paragraph here.\n\nSecond paragraph here.\n\nThird paragraph here.'

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'edit.md', ESSAY('Edit', BODY, 'edit01'))
    await a.connect(); await a.open('Edit'); await a.settle()
    await a.ev("setRoom('revise')"); await a.wait(400)
    kb = a.pg.keyboard
    put = lambda body: a.ev("(t)=>{editor.value=t;prevValue=t;flags=new Array(t.length).fill(0);onInput()}", body)
    caret = lambda needle, k=0: a.ev("([n,k])=>{editor.focus();const i=editor.value.indexOf(n)+k;editor.setSelectionRange(i,i)}", [needle, k])

    # E1 Alt+Up moves the paragraph above the one before; the spacing stays; the cursor goes with it
    await caret('Second', 3)
    await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E1 Alt+Up moves the paragraph above the one before', v == 'Second paragraph here.\n\nFirst paragraph here.\n\nThird paragraph here.\n', v)
    check('E1 the cursor moves with it', await a.ev("editor.selectionStart") == 3, await a.ev("editor.selectionStart"))
    await kb.press('Alt+ArrowUp'); await a.wait(100)
    check('E1 at the top, nothing moves', await a.ev("editor.value") == v, '')
    await kb.press('Alt+ArrowDown'); await kb.press('Alt+ArrowDown'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E1 Alt+Down twice takes it to the end', v == 'First paragraph here.\n\nThird paragraph here.\n\nSecond paragraph here.\n', v)
    await kb.press('Control+z'); await a.wait(150)
    check('E1 each move is one step to undo', await a.ev("editor.value") == 'First paragraph here.\n\nSecond paragraph here.\n\nThird paragraph here.\n', await a.ev("editor.value"))

    # E2 pasted words stay pasted when they move, and a move is not typing
    await put('Typed one.\n\nTyped two.')
    await a.ev("(()=>{const t=editor.value;ED.view.dispatch({changes:{from:t.length,insert:'\\n\\nPasted in from elsewhere.'},userEvent:'input.paste'})})()"); await a.wait(200)
    before = await a.ev("(()=>{const i=editor.value.indexOf('Pasted');return flags.slice(i,i+25).join('')})()")
    check('E2 a paste is marked pasted', before == '1' * 25, before)
    log0 = await a.ev("wlog[dayKey(new Date())]||0")
    await caret('Pasted', 2); await kb.press('Alt+ArrowUp'); await kb.press('Alt+ArrowUp'); await a.wait(200)
    v = await a.ev("editor.value")
    check('E2 the pasted paragraph moved to the top', v == 'Pasted in from elsewhere.\n\nTyped one.\n\nTyped two.', v)
    marks = await a.ev("[flags.slice(0,25).join(''),flags.slice(27,37).join('')]")
    check('E2 it is still pasted, and the typed ones still typed', marks == ['1' * 25, '0' * 10], marks)
    check('E2 a move adds nothing to the words typed today', (await a.ev("wlog[dayKey(new Date())]||0")) == log0, '')

    # E3 a selection moves every paragraph it touches
    await put('One.\n\nTwo.\n\nThree.\n\nFour.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.indexOf('wo'),editor.value.indexOf('hre'))")
    await kb.press('Alt+ArrowDown'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E3 two selected paragraphs move together', v == 'One.\n\nFour.\n\nTwo.\n\nThree.', v)
    sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('E3 the selection goes with them', sel == 'wo.\n\nT', sel)

    # E4 a heading is a paragraph of its own; a code block keeps its blank lines
    await put('## Part one\nOpening line.\n\n```\ncode\n\nmore\n```\n\nClosing line.')
    await caret('Closing'); await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E4 a code block with a blank line inside moves whole', v == '## Part one\nOpening line.\n\nClosing line.\n\n```\ncode\n\nmore\n```', v)
    await caret('Opening'); await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E4 a paragraph moves past a heading on its own', v.startswith('Opening line.\n## Part one\n'), v[:40])

    # E5 in a list, the item moves past its neighbour with its sub-items; a numbered list keeps counting
    await put('- apples\n- pears\n  - green\n  - ripe\n- plums')
    await caret('pears'); await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E5 a list item moves up with its sub-items', v == '- pears\n  - green\n  - ripe\n- apples\n- plums', v)
    await caret('ripe'); await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E5 a sub-item moves among its own', v == '- pears\n  - ripe\n  - green\n- apples\n- plums', v)
    await kb.press('Alt+ArrowUp'); await a.wait(100)
    check('E5 and stops at the top of them', await a.ev("editor.value") == v, '')
    await put('1. First step\n2. Second step\n3. Third step')
    await caret('Third'); await kb.press('Alt+ArrowUp'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E5 a numbered list keeps counting up', v == '1. First step\n2. Third step\n3. Second step', v)

    # E6 Forward only: paragraphs stay put while drafting
    await put('Alpha.\n\nBeta.')
    await a.ev("fx.fwd=true;saveFx();setRoom('write')"); await a.wait(400)
    await caret('Beta'); await kb.press('Alt+ArrowUp'); await a.wait(200)
    check('E6 Forward only blocks a move', await a.ev("editor.value") == 'Alpha.\n\nBeta.', await a.ev("editor.value"))
    msg = await a.ev("$('#wmsg').textContent")
    check('E6 and says why', 'Move them in Revise' in msg, msg)
    await a.ev("fx.fwd=false;saveFx();setRoom('revise')"); await a.wait(400)

    # E7 two hyphens become an em dash while smart punctuation is on; there is no separate switch
    await put('Start.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
    await kb.type(' A pause--then more.'); await a.wait(200)
    check('E7 two hyphens become an em dash', (await a.ev("editor.value")).endswith('A pause—then more.'), await a.ev("editor.value"))
    names = await a.ev("paletteCommands().map(x=>x.label)")
    check('E7 the palette has no em dash switch', not any('hyphen' in n.lower() or 'em dash' in n.lower() for n in names), [n for n in names if 'dash' in n.lower()])
    await a.ev("setSmart('on',false)"); await kb.type(' Then--this.'); await a.wait(200)
    check('E7 with smart punctuation off, two hyphens stay two', (await a.ev("editor.value")).endswith('Then--this.'), (await a.ev("editor.value"))[-20:])
    await a.ev("setSmart('on',true)")
    await put('Text.\n\n'); await a.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
    await kb.type('---'); await a.wait(150)
    check('E7 hyphens at the start of a line stay a rule', (await a.ev("editor.value")).endswith('\n---'), await a.ev("editor.value"))
    keys = await a.ev("shortcutGroups().flatMap(g=>g.rows).filter(r=>r.d==='Em dash').map(r=>r.n).join('')")
    check('E7 the shortcuts list says it is always on', 'Becomes —' in keys and 'turn it on' not in keys, keys)

    # E8 superscript and subscript on the page: not in code, not a footnote, not strikethrough
    await put('The 29^th^ of May. Water is H~2~O. A note[^1] here. Struck ~~out~~ text. Code `x^2^ y~3~` stays.\n\n[^1]: The note.')
    await caret('Struck'); await a.wait(200)
    sup = await a.ev("[...document.querySelectorAll('#editor .cm-sup')].map(x=>x.textContent)")
    sub = await a.ev("[...document.querySelectorAll('#editor .cm-sub')].map(x=>x.textContent)")
    check('E8 ^th^ is superscript, H~2~O subscript, and nothing else', sup == ['^th^'] and sub == ['~2~'], (sup, sub))
    hid = await a.ev("(()=>{const s=document.querySelector('#editor .cm-sup');return [...s.querySelectorAll('.cm-hide')].map(x=>x.textContent)})()")
    check('E8 away from the cursor, its marks step back', hid == ['^', '^'], hid)
    look = await a.ev("(()=>{const s=document.querySelector('#editor .cm-sup'),c=getComputedStyle(s);return [c.position,parseFloat(c.top)<0,parseFloat(c.fontSize)<parseFloat(getComputedStyle(s.parentElement).fontSize)]})()")
    check('E8 it sits above the line, smaller, without stretching it', look == ['relative', True, True], look)
    strike = await a.ev("[...document.querySelectorAll('#editor .cm-strike')].map(x=>x.textContent)")
    check('E8 ~~out~~ is still strikethrough', strike == ['~~out~~'], strike)

    # E9 typed ^ wraps a selection; Format: Subscript wraps and unwraps
    await put('Mass is mc2 here.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.indexOf('2'),editor.value.indexOf('2')+1)")
    await kb.type('^'); await a.wait(150)
    check('E9 typing ^ round a selection makes it superscript', (await a.ev("editor.value")) == 'Mass is mc^2^ here.', await a.ev("editor.value"))
    await put('Water is H2O.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.indexOf('2'),editor.value.indexOf('2')+1)")
    await a.ev("paletteCommands().find(x=>x.label==='Format: Subscript').run()"); await a.wait(150)
    check('E9 Format: Subscript wraps the selection', (await a.ev("editor.value")) == 'Water is H~2~O.', await a.ev("editor.value"))
    await a.ev("paletteCommands().find(x=>x.label==='Format: Subscript').run()"); await a.wait(150)
    check('E9 and run again, takes it off', (await a.ev("editor.value")) == 'Water is H2O.', await a.ev("editor.value"))
    await put('A ~~struck~~ word.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.indexOf('struck'),editor.value.indexOf('struck')+6)")
    await a.ev("paletteCommands().find(x=>x.label==='Format: Strikethrough').run()"); await a.wait(150)
    check('E9 Format: Strikethrough on struck words takes the strike off', (await a.ev("editor.value")) == 'A struck word.', await a.ev("editor.value"))

    # E10 Publish: real superscript and subscript in HTML, and a word on where they render
    await put('The 29^th^ of May, and H~2~O, and a note[^1].\n\n[^1]: The note.')
    html = await a.ev("buildPub().html")
    check('E10 HTML has real superscript and subscript', '29<sup>th</sup>' in html and 'H<sub>2</sub>O' in html, html[:200])
    check('E10 a footnote stays a footnote link', 'href="#fn-1"' in html, html[:300])
    await a.ev("openPublish('md')"); await a.wait(300)
    note = await a.ev("$('#pub').textContent")
    check('E10 Publish says where ^ and ~ render', '2 superscript or subscript marks stay as ^ ^ or ~ ~' in note and 'Substack does not' in note, note[:400])
    await a.ev("$('#pubClose').click()"); await a.wait(200)

    # E11 the palette by keyword
    names = await a.ev("paletteCommands().map(x=>x.label)")
    fam = lambda k: [n for n in names if n.startswith(k)]
    check('E11 Insert lists every insert', fam('Insert ') == ['Insert link', 'Insert note', 'Insert table', 'Insert blockquote', 'Insert code block', 'Insert section break'], fam('Insert '))
    check('E11 Format lists every format', fam('Format: ') == ['Format: Bold', 'Format: Italic', 'Format: Strikethrough', 'Format: Highlight', 'Format: Superscript', 'Format: Subscript'], fam('Format: '))
    check('E11 Stage lists every stage', fam('Stage: ') == ['Stage: Idea', 'Stage: Drafting', 'Stage: Revising', 'Stage: Ready', 'Stage: Published', 'Stage: Archived'], fam('Stage: '))
    check('E11 Go to lists the rooms and the notes', fam('Go to ') == ['Go to Library', 'Go to Write', 'Go to Revise', 'Go to a note'], fam('Go to '))
    check('E11 Move lists the paragraph moves', fam('Move ') == ['Move paragraph up', 'Move paragraph down'], fam('Move '))
    gone = [n for n in names if n in ('Copy as Markdown', 'Open Words', 'Add a note', 'Bold', 'Link', 'Library') or n.startswith('Move to ') or n.startswith('Two hyphens')]
    check('E11 the old names are gone', gone == [], gone)
    hint = await a.ev("JSON.stringify(Object.fromEntries(paletteCommands().filter(x=>['Coach: Words','Insert link','Format: Bold','Move paragraph up'].includes(x.label)).map(x=>[x.label,x.keys])))")
    hint = json.loads(hint)
    check('E11 each keeps its shortcut', hint.get('Coach: Words', '').endswith('W') and hint.get('Insert link', '').endswith('K') and hint.get('Format: Bold', '').endswith('B') and '↑' in hint.get('Move paragraph up', ''), hint)
    await a.ev("openPal('cmd')"); await a.ev("$('#palIn').value='insert';renderPal()"); await a.wait(200)
    shown = await a.ev("[...document.querySelectorAll('#palList .pi .pl')].map(x=>x.textContent)")
    check('E11 typing insert lists the inserts, and nothing that does not match', shown == ['Insert link', 'Insert note', 'Insert table', 'Insert blockquote', 'Insert code block', 'Insert section break'], shown)
    grp = await a.ev("[...document.querySelectorAll('#palList .pi .pg')].map(x=>x.textContent)")
    check('E11 an Insert command does not repeat its group beside it', all(g == '' for g in grp), grp)
    await a.ev("closePal()")
    await a.lib(); lib = await a.ev("paletteCommands().map(x=>x.label)")
    check('E11 in the Library, nothing to insert or format', not any(n.startswith(('Insert ', 'Format: ', 'Move ')) for n in lib), [n for n in lib if n.startswith(('Insert', 'Format', 'Move'))])
    await a.open('Edit'); await a.ev("setRoom('revise')"); await a.wait(300)

    # E12 Insert blockquote turns a paragraph into a quote and back, and keeps pasted words pasted
    await put('Before.\n\nQuote this line\nand this one.\n\nAfter.')
    await a.ev("(()=>{const i=editor.value.indexOf('and this');for(let k=i;k<i+8;k++)flags[k]=1})()")
    await caret('this line'); await a.ev("insertQuote()"); await a.wait(150)
    v = await a.ev("editor.value")
    check('E12 the paragraph becomes a quote', v == 'Before.\n\n> Quote this line\n> and this one.\n\nAfter.', v)
    f = await a.ev("(()=>{const i=editor.value.indexOf('and this');return flags.slice(i,i+8).join('')})()")
    check('E12 pasted words in it stay pasted', f == '1' * 8, f)
    await a.ev("insertQuote()"); await a.wait(150)
    check('E12 run again, it is a paragraph again', (await a.ev("editor.value")) == 'Before.\n\nQuote this line\nand this one.\n\nAfter.', await a.ev("editor.value"))

    # E13 Insert code block: around the selected lines, or an empty one to type into
    await put('Intro.\n\nlet x = 1;\nlet y = 2;\n\nOutro.')
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.indexOf('let x'),editor.value.indexOf('2;')+2)")
    await a.ev("insertCode()"); await a.wait(150)
    v = await a.ev("editor.value")
    check('E13 the selected lines go inside a fence', v == 'Intro.\n\n```\nlet x = 1;\nlet y = 2;\n```\n\nOutro.', v)
    await put('Intro.')
    await caret('Intro', 3); await a.ev("insertCode()"); await kb.type('code'); await a.wait(150)
    v = await a.ev("editor.value")
    check('E13 with nothing selected, an empty block after the paragraph, cursor inside', v == 'Intro.\n\n```\ncode\n```', v)

    # E14 Insert section break: after the paragraph, a blank line either side
    await put('Part one ends.\n\nPart two begins.')
    await caret('ends'); await a.ev("insertBreak()"); await a.wait(150)
    v = await a.ev("editor.value")
    check('E14 a section break goes after the paragraph', v == 'Part one ends.\n\n* * *\n\nPart two begins.', v)
    check('E14 the cursor waits after it', await a.ev("editor.selectionStart") == len('Part one ends.\n\n* * *'), await a.ev("editor.selectionStart"))

    # E15 the shortcuts list names the new moves and marks
    rows = await a.ev("shortcutGroups().flatMap(g=>g.rows).map(r=>r.d)")
    check('E15 the shortcuts list has the moves, strikethrough, superscript and code blocks',
          all(x in rows for x in ['Move a paragraph up', 'Move a paragraph down', 'Strikethrough', 'Superscript, subscript', 'Code block', 'Insert or format anything, by name']), rows)

go(suite)
