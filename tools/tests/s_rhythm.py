import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

# Rhythm: the share of sentences that change pace from the one before, every sentence as a bar grouped
# by paragraph, and the paragraphs whose pace never changes (choppy, heavy, even). It reads the skim
# test's sentences, so the counts agree, and it sees order: the same sentences in another order read
# differently, which the old spread-of-lengths score could not.

FILL = ('river stone light field morning window letter garden silver winter harbour candle orchard '
        'ladder meadow lantern pebble thunder valley feather').split()

def sent(n, k=0):
    """A sentence of exactly n words, no word twice in a row."""
    if n == 1: return 'Stop.'
    words = ['The'] + [FILL[(k + i) % len(FILL)] for i in range(n - 2)] + ['ended.']
    return ' '.join(words)

def para(*lens):
    return ' '.join(sent(n, i * 3) for i, n in enumerate(lens))

CHOPPY = 'The meeting ran long. Nobody had read the report. The chair asked for a summary. Three people spoke at once. Nobody listened.'
TRICOLON = 'We tried. We failed. We learned.'
EVEN = para(11, 10, 12)
HEAVY = para(27, 30, 26)
VARIED = para(6, 24, 9, 31)
NUMBERS = 'Revenue rose by 2.5 per cent in 2024, to 0.6 million. It isn\'t much. Nobody on the board of the second office expected the figure to move at all this year.'
LIST = '- One point here.\n- Another point here.\n- A third point.'

BODY = '\n\n'.join([VARIED, CHOPPY, TRICOLON, '## Second part', EVEN, HEAVY, LIST, NUMBERS])

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'rhythm.md', ESSAY('Rhythm', BODY, 'rhy001'))
    await a.connect()
    await a.open('Rhythm'); await a.settle()
    await a.ev("setRoom('revise')"); await a.wait(600)

    # RH1 the card says what it measures, and its track carries no colour ramp
    lab = await a.ev("$('#voiceGauge .gauge-top .lab').textContent")
    check('RH1 the card is Rhythm: sentences that change pace', lab == 'Rhythm: sentences that change pace', lab)
    track = await a.ev("(()=>{const t=$('#voiceGauge .track');const b=t.querySelector('.band');return {bg:getComputedStyle(t).backgroundImage,left:b.style.left,width:b.style.width}})()")
    check('RH1 a neutral track: no red-to-green ramp', track['bg'] == 'none', track)
    check('RH1 the band where published prose sits is shaded, 55 to 70%', track['left'] == '55%' and track['width'] == '15%', track)
    ends = await a.ev("$('#voiceGauge .track-ends').textContent")
    check('RH1 the band is named', 'Published prose' in ends, ends)

    # RH2 the bars: one per sentence, grouped by paragraph; lists left out, a heading starts afresh
    R = await a.ev("JSON.stringify(analyze(editor.value,mode).rh.paras.map(p=>({lens:p.rows.map(r=>r.len),flat:p.flat,sec:p.sec})))")
    import json; R = json.loads(R)
    lens = [p['lens'] for p in R]
    check('RH2 each paragraph is a group, in order', lens[0] == [6, 24, 9, 31] and lens[1] == [4, 5, 6, 5, 2] and lens[2] == [2, 2, 2], lens)
    check('RH2 a list is not prose rhythm', not any(l == [3, 3, 3] or l == [3] for l in lens), lens)
    check('RH2 a heading starts a new section', [p['sec'] for p in R] == [False, False, False, True, False, False], [p['sec'] for p in R])
    check('RH2 numbers are words a reader hears, and "2.5", "0.6" and "isn\'t." do not split a sentence', lens[-1] == [11, 3, 17], lens[-1])
    groups = await a.ev("[...document.querySelectorAll('#voiceGauge .rhy .rp')].map(g=>g.querySelectorAll('i').length)")
    check('RH2 the card draws every sentence, grouped by paragraph', groups == [len(l) for l in lens], groups)
    check('RH2 a section break is drawn between groups', (await a.ev("document.querySelectorAll('#voiceGauge .rhy .rsec').length")) == 1, '')
    hs = await a.ev("[...document.querySelectorAll('#voiceGauge .rhy .rp')][0].querySelectorAll('i')[3].style.height")
    check('RH2 a bar\'s height is its length', hs == '37px', hs)

    # RH3 flat paragraphs: choppy, heavy and even are named; a tricolon and a varied paragraph are not
    flat = [p['flat'] for p in R]
    check('RH3 four or more sentences, none over 15 words: choppy', flat[1] == 'choppy', flat)
    check('RH3 three or more, all within a few words of each other: even', flat[3] == 'even', flat)
    check('RH3 three or more, none under 25 words: heavy', flat[4] == 'heavy', flat)
    check('RH3 a tricolon of three short sentences is not flat', flat[2] == '', flat)
    check('RH3 a paragraph that changes pace is not flat', flat[0] == '' and flat[5] == '', flat)
    under = await a.ev("[...document.querySelectorAll('#voiceGauge .rhy .rp')].map(g=>g.classList.contains('flat'))")
    check('RH3 flat paragraphs are underlined in the bars', under == [bool(f) for f in flat], under)
    line = await a.ev("getComputedStyle(document.querySelector('#voiceGauge .rp.flat')).borderBottomStyle+' '+getComputedStyle(document.querySelector('#voiceGauge .rp:not(.flat)')).borderBottomColor")
    check('RH3 the underline is a line, not a colour', line.startswith('solid') and 'rgba(0, 0, 0, 0)' in line, line)
    note = await a.ev("$('#voiceGauge .gauge-note').textContent")
    check('RH3 the note counts them', '3 flat paragraphs' in note, note)
    cnt = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Flat paragraphs');return c.querySelector('.check-count').textContent})()")
    check('RH3 the Flat paragraphs check counts paragraphs of three sentences or more', cnt == '3 of 6', cnt)
    labs = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Flat paragraphs');return [...c.querySelectorAll('.hitlab')].map(x=>x.textContent)})()")
    check('RH3 its chips are grouped by kind', labs == ['Choppy', 'Heavy', 'Even'], labs)
    await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Flat paragraphs');c.querySelector('.check-row').click();c.querySelector('.hit').click()})()")
    await a.wait(300)
    sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('RH3 a chip selects the whole paragraph', sel == CHOPPY, sel[:60])

    # RH4 the number is the share of sentences that change pace, and it sees order
    pace = await a.ev("JSON.stringify((({pace,pairs,turns})=>({pace,pairs,turns}))(analyze(editor.value,mode).rh))")
    pace = json.loads(pace)
    # pairs run across paragraph breaks within a section; the list breaks the chain
    # section one: 6 24 9 31 | 4 5 6 5 2 | 2 2 2, five turns in eleven; section two: 11 10 12 | 27 30 26,
    # one in five; after the list: 11 3 17, two in two. Eight in eighteen.
    check('RH4 pace counts the sentences that change length by half or more', pace['pairs'] == 18 and pace['turns'] == 8 and pace['pace'] == 44, pace)
    val = await a.ev("$('#voiceGauge .gauge-top .val').textContent")
    check('RH4 the card shows it', val == '44%', val)
    band = await a.ev("$('#voiceGauge .gauge-note b').textContent")
    check('RH4 under 45%: flat', band == 'Flat.', band)
    alt = await a.ev("analyze(%s,mode).rh.pace" % json.dumps(para(6, 24, 6, 24)))
    srt = await a.ev("analyze(%s,mode).rh.pace" % json.dumps(para(6, 6, 24, 24)))
    check('RH4 the same sentences in another order read differently', alt == 100 and srt == 33, (alt, srt))
    few = await a.ev("rhythmCard(analyze('One short line here. And another one.',mode).rh)")
    check('RH4 too few sentences: no needle, no number', '–' in few and 'needle' not in few and 'Too short to read' in few, few[:200])

    # RH5 the counts agree: the Sentences tile and the skim test read the same sentences
    tile = await a.ev("$('#m-sent').textContent")
    skim = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='The skim test');return c.querySelector('.check-count').textContent})()")
    check('RH5 the Sentences tile matches the skim test', skim == tile + ' sentences', (tile, skim))

    # RH6 a bar finds its sentence, and the caret's sentence is drawn in full ink
    await a.ev("document.querySelectorAll('#voiceGauge .rhy .rp')[0].querySelectorAll('i')[1].click()"); await a.wait(300)
    sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('RH6 a click on a bar selects its sentence', sel == sent(24, 3), sel[:60])
    await a.ev("editor.setSelectionRange(editor.value.indexOf('Nobody had read'),editor.value.indexOf('Nobody had read'))"); await a.wait(200)
    cur = await a.ev("(()=>{const g=[...document.querySelectorAll('#voiceGauge .rhy .rp')];return g.map(x=>[...x.querySelectorAll('i')].findIndex(i=>i.classList.contains('cur')))})()")
    check('RH6 the caret\'s sentence is marked among the bars', cur[1] == 1 and sum(1 for x in cur if x >= 0) == 1, cur)

    # RH7 a long draft: every sentence shows, the bars narrow, and it stays quick
    big = '\n\n'.join(para(*[(5, 18, 9, 27, 12, 33)[(i + j) % 6] for j in range(5)]) for i in range(60))
    t = await a.ev("(t)=>{const s=performance.now();const h=rhythmCard(analyze(t,mode).rh);return [performance.now()-s,(h.match(/<i /g)||[]).length,/rhy w3/.test(h)]}", big)
    check('RH7 300 sentences: every one drawn, narrower bars', t[1] == 300 and t[2], t)
    check('RH7 and the whole pane\'s numbers come back in under half a second', t[0] < 500, t[0])

go(suite)
