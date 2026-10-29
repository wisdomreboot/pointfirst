import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

# The Skim lens: what a reader who skims takes from the page stays in full ink, the rest fades.
# Paragraphs: the first sentence of each paragraph and list item. Sentences: each sentence's
# first words and its last, with a word an ending hands to the next opening underlined in both.
# And the Revise tools: they stay pinned above the page as it scrolls; the lens caption does not.

P1 = 'Most writers think a long sentence is the problem. It isn\'t. The problem is how long the reader waits before anything happens.'
P2 = 'A sentence starts to mean something when its subject meets its verb. Everything before that meeting is held in the reader\'s head.'
P3 = 'Readers skim. They read the first sentence of a paragraph and decide whether the rest is worth their time.'
LIST = '- A list item that makes one point and stops there.\n- A second item that adds a reason the reader can use.'
P4 = 'When the chain breaks, the reader has to jump. A jump costs attention.'
FILL = ' '.join(['The essay goes on here so that the page is long enough to scroll a good way down.'] * 6)

BODY = '\n\n'.join([P1, P2, '## What the skim shows', P3, LIST, P4] + [FILL] * 8)

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'skim.md', ESSAY('Skim', BODY, 'skim01'))
    await a.connect()
    await a.open('Skim'); await a.settle()
    await a.ev("setRoom('revise')"); await a.wait(500)

    # S1 the lens menu: Skim first
    labels = await a.ev("[...document.querySelectorAll('#lensMenu [data-lens] b')].map(b=>b.textContent)")
    check('S1 the lens menu offers Skim first', labels[:1] == ['Skim'] and labels[1:] == ['Marks', 'Word classes', 'Runway', 'Plain'], labels)
    await a.ev("skimMode='para';store.set('ww:skim','para');setLens('skim')"); await a.wait(500)
    check('S1 the lens button names it', (await a.ev("$('#lensBtn').textContent")) == 'Lens: Skim', await a.ev("$('#lensBtn').textContent"))
    pills = await a.ev("[...document.querySelectorAll('#lenspick [data-skim]')].map(b=>b.textContent+':'+b.getAttribute('aria-pressed'))")
    check('S1 the picker offers Paragraphs and Sentences, Paragraphs first', pills == ['Paragraphs:true', 'Sentences:false'], pills)

    # S2 Paragraphs: the first sentence of each paragraph and list item stays dark, nothing else
    kept = await a.ev("[...document.querySelectorAll('#editor .sk')].map(x=>x.textContent)")
    check('S2 each paragraph keeps its first sentence', 'Most writers think a long sentence is the problem.' in kept and
          'A sentence starts to mean something when its subject meets its verb.' in kept and 'Readers skim.' in kept and
          'When the chain breaks, the reader has to jump.' in kept, kept[:6])
    check('S2 each list item keeps its first sentence', 'A list item that makes one point and stops there.' in kept and
          'A second item that adds a reason the reader can use.' in kept, kept[:8])
    check('S2 a later sentence fades', not any(k.startswith("It isn't") or k.startswith('Everything before') or k.startswith('They read') for k in kept), kept[:8])
    ink = await a.ev("(()=>{const a=c=>{const m=c.match(/\\/\\s*([\\d.]+)\\)|rgba\\([^)]*,\\s*([\\d.]+)\\)/);return m?parseFloat(m[1]||m[2]):1};const k=document.querySelector('#editor .sk'),line=k.closest('.cm-line');return [a(getComputedStyle(k).color),a(getComputedStyle(line).color)]})()")
    check('S2 what stays keeps full ink and the rest fades: light and dark, not hue', ink[0] == 1 and ink[1] < 0.5, ink)
    cap = await a.ev("$('#lensbar').textContent")
    check('S2 the caption counts paragraphs and says what to read for', cap.startswith('13 paragraphs.') and 'tell the argument' in cap, cap[:120])

    # S3 Sentences: openings and endings, and the word an ending hands to the next opening
    await a.ev("document.querySelector('#lenspick [data-skim=sent]').click()"); await a.wait(500)
    check('S3 the choice is remembered', (await a.ev("store.get('ww:skim')")) == 'sent', await a.ev("store.get('ww:skim')"))
    kept = await a.ev("[...document.querySelectorAll('#editor .sk')].map(x=>x.textContent)")
    check('S3 a long sentence keeps its first words', any(k.startswith('A sentence starts to mean') for k in kept), kept[:10])
    check('S3 and its last words, not its middle', any(k.endswith('meets its verb.') for k in kept) and not any('something when its subject' in k for k in kept), kept[:10])
    links = await a.ev("[...document.querySelectorAll('#editor .sk-link')].map(x=>x.textContent)")
    check('S3 a word an ending shares with the next opening is underlined in both', links.count('problem.') + links.count('problem') >= 2, links)
    cap = await a.ev("$('#lensbar').textContent")
    check('S3 the caption counts sentences', cap.split('.')[0].endswith('sentences') and 'underlined in both' in cap, cap[:120])

    # S4 a reload keeps the lens and the choice
    await a.reload(); await a.ev("setRoom('revise')"); await a.wait(600)
    check('S4 the lens and the choice survive a reload', (await a.ev("$('#lensBtn').textContent")) == 'Lens: Skim' and
          (await a.ev("document.querySelector('#lenspick [data-skim=sent]').getAttribute('aria-pressed')")) == 'true',
          await a.ev("$('#lensBtn').textContent"))

    # S5 the palette reaches both
    names = await a.ev("paletteCommands().map(x=>x.label)")
    check('S5 the palette offers Skim: Paragraphs and Skim: Sentences', 'Skim: Paragraphs' in names and 'Skim: Sentences' in names and 'Lens: Skim' in names,
          [x for x in names if 'Skim' in x])

    # S6 the tools stay pinned above the page as it scrolls; the caption scrolls away
    await a.ev("setLens('syntax')"); await a.wait(400)
    await a.ev("document.querySelector('.editor-wrap').scrollTop=900"); await a.wait(400)
    pos = await a.ev("""(()=>{const w=document.querySelector('.editor-wrap').getBoundingClientRect(),r=$('#rtools').getBoundingClientRect(),
      p=$('#lenspick').getBoundingClientRect(),c=$('#lensbar').getBoundingClientRect();return {wrap:w.top,tools:r.top,toolsBottom:r.bottom,pick:p.top,pickH:p.height,cap:c.bottom}})()""")
    check('S6 the tools stay at the top of the page area', pos['wrap'] <= pos['tools'] <= pos['wrap'] + 16, pos)
    check('S6 the lens picker stays under them', pos['pickH'] > 0 and pos['pick'] >= pos['toolsBottom'] - 1 and pos['pick'] < pos['wrap'] + 120, pos)
    check('S6 the caption has scrolled away', pos['cap'] < pos['wrap'], pos)
    clicked = await a.ev("(()=>{const r=$('#lensBtn').getBoundingClientRect();const el=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return !!el&&!!el.closest('#lensBtn')})()")
    check('S6 the lens button can be clicked while pinned', clicked, clicked)

    # S7 the caret keeps clear of the pinned tools
    await a.ev("editor.focus()"); await a.wait(100)
    await a.ev("""(()=>{const w=document.querySelector('.editor-wrap'),top=$('#rhead').getBoundingClientRect().bottom;
      const lines=[...document.querySelectorAll('#editor .cm-line')];const l=lines.find(x=>x.getBoundingClientRect().top>top+2);
      const pos=ED.view.posAtDOM(l);editor.setSelectionRange(pos,pos)})()""")
    for _ in range(3):
        await a.pg.keyboard.press('ArrowUp'); await a.wait(120)
    gap = await a.ev("(()=>{const r=ED.view.coordsAtPos(ED.view.state.selection.main.head);return r.top-$('#rhead').getBoundingClientRect().bottom})()")
    check('S7 moving up the page keeps the caret below the pinned tools', gap >= 0, gap)

    # S8 Write has no tools to pin
    await a.ev("setRoom('write')"); await a.wait(400)
    shown = await a.ev("getComputedStyle($('#rhead')).display")
    check('S8 Write shows no pinned tools', shown == 'none', shown)
    await a.ev("setRoom('revise')"); await a.wait(300)

go(suite)
