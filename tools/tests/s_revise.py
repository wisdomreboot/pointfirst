import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

# The runway: words a reader holds before the main verb. The skim test: each sentence's
# first words and last words, with a word shared across the break underlined.

A = ('Helicopter parents can prevent their children from developing grit, the ability to try and not '
     'give up when things get hard, but, without grit, children may struggle with challenges later in life.')
B = ('Being born to wealthy parents bound to not let you fail can prove to be a hefty handicap when you '
     'consider how anxious parents sheltering children can prevent them from developing grit.')
LONG = ('Robert E. Simanek, who was awarded the Medal of Honor for saving his fellow Marines from grievous '
        'injuries or death by falling on a live grenade hurled by Chinese Communist troops during a battle in '
        'the Korean War, died on Monday in West Bloomfield.')
MID = 'Following initial breakthroughs, the development of proto-cuneiform into such a system proceeded apace for two thousand years.'
SKIM1 = 'The grade counts syllables and words, so what it measures is length, not structure.'
SKIM2 = 'Structure is what a reader holds in his head while he waits for the verb.'
SKIM3 = 'Questions like this one stay plain?'
SKIM4 = 'The verb arrives at last and the sentence starts to mean something.'

BODY = '\n\n'.join([A + ' ' + B, LONG + ' ' + MID, SKIM1 + ' ' + SKIM2, '## A heading', SKIM3 + ' ' + SKIM4])

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'runway.md', ESSAY('Runway', BODY, 'rrrr11'))
    await a.connect()
    await a.open('Runway'); await a.settle()
    await a.ev("setRoom('revise')"); await a.wait(600)

    # R1 the runway separates the pair a syllable count could not
    S = await a.ev("JSON.stringify(proseRun(editor.value).sents.map(x=>({rw:x.rw,verbal:x.verbal,label:x.label,s:x.s,e:x.e,rwEnd:x.rwEnd})))")
    import json; S = json.loads(S)
    by = lambda start: next((x for x in S if x['label'].startswith(start)), None)
    ra, rb, rl, rm = by('Helicopter'), by('Being born'), by('Robert E'), by('Following initial')
    check('R1 Douglas pair: A lands its verb at word 3', ra and ra['rw'] == 2, ra)
    check('R1 Douglas pair: B holds eleven words, a verb phrase as subject', rb and rb['rw'] == 11 and rb['verbal'], rb)
    check('R1 a long subject with a clause set off by commas runs to the main verb', rl and rl['rw'] >= 30 and not rl['verbal'], rl)
    check('R1 an opening phrase counts: "Following…, the development … proceeded"', rm and rm['rw'] == 11, rm)
    q = by('Questions like')
    check('R1 a question has no runway', q and q['rw'] is None, q)
    text = await a.ev('editor.value')
    check('R1 the runway ends where the verb starts', rl and text[rl['s']:rl['rwEnd']].endswith('Korean War') and text[rl['rwEnd']:].lstrip(', ').startswith('died'), text[rl['s']:rl['rwEnd']][-30:] if rl else '')

    # R2 the lens: Runway replaces Difficulty, and shades only the held words
    labels = await a.ev("[...document.querySelectorAll('#lensMenu [data-lens] b')].map(b=>b.textContent)")
    check('R2 lens menu: Runway, no Difficulty', 'Runway' in labels and 'Difficulty' not in labels, labels)
    await a.ev("setLens('runway')"); await a.wait(500)
    marks = await a.ev("[...document.querySelectorAll('#editor mark.rw-h,#editor mark.rw-v')].map(m=>m.className+'|'+m.textContent)")
    joined = ' '.join(marks)
    check('R2 the long runway is shaded and underlined', any(m.startswith('rw-v|') and 'Simanek' in m for m in marks), marks)
    check('R2 a verb phrase as subject is shaded', any(m.startswith('rw-h|') and 'Being born' in m for m in marks), marks)
    check('R2 the verb itself is not shaded', 'died' not in joined and 'can prove' not in joined, marks)
    check('R2 a short runway is left plain', 'Helicopter' not in joined, marks)
    cap = await a.ev("$('#lensbar').textContent")
    check('R2 the caption says what a runway is and counts them', 'holds before the verb' in cap and '1 very long' in cap, cap)
    check('R2 the lens button names it', (await a.ev("$('#lensBtn').textContent")) == 'Lens: Runway', await a.ev("$('#lensBtn').textContent"))

    # R3 Voice: Long runways replaces Hard sentences
    names = await a.ev("[...document.querySelectorAll('#voiceChecks .check-name')].map(x=>x.textContent)")
    check('R3 Long runways is listed, Hard sentences is gone', 'Long runways' in names and 'Hard sentences' not in names, names)
    chips = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Long runways');return [...c.querySelectorAll('.hit')].map(h=>h.textContent)})()")
    check('R3 its chips name the longest first, with the count', chips and chips[0].startswith('Robert E Simanek') and chips[0].rstrip().split(' ')[-1].isdigit(), chips)
    check('R3 a verb phrase as subject has its own chip, and is not called long', any(x == 'Being born to wealthy parents bound…' for x in chips) and not any(x.startswith('Being born') and x.rstrip().split(' ')[-1].isdigit() for x in chips), chips)
    await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Long runways');c.querySelector('.hit').click()})()")
    await a.wait(300)
    sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('R3 a chip selects the runway in the draft', sel.startswith('Robert E. Simanek') and sel.endswith('Korean War'), sel[-40:])

    # R4 the skim test: openings and endings, shared words underlined, headings break the chain
    rows = await a.ev("[...document.querySelectorAll('#voiceChecks .skim .op')].map(r=>({t:r.textContent,u:[...r.querySelectorAll('u')].map(u=>u.textContent),p:r.classList.contains('para')}))")
    check('R4 one line per sentence', len(rows) == 8, [r['t'][:30] for r in rows])
    r1 = next((r for r in rows if r['t'].startswith('The grade')), None)
    r2 = next((r for r in rows if r['t'].startswith('Structure is')), None)
    check('R4 a line shows the opening and the ending', r1 and 'The grade counts syllables and' in r1['t'] and r1['t'].rstrip().endswith('length, not structure.'), r1)
    check('R4 a word an ending shares with the next opening is underlined in both', r1 and r2 and any('structure' in u for u in r1['u']) and any(u.startswith('Structure') for u in r2['u']), (r1, r2))
    r3 = next((r for r in rows if r['t'].startswith('Questions')), None)
    r4 = next((r for r in rows if r['t'].startswith('The verb arrives')), None)
    check('R4 across a heading nothing is linked', r3 and not r3['u'], r3)
    check('R4 a short sentence shows once, without a gap', r3 and '…' not in r3['t'], r3)
    check('R4 paragraphs sit apart', r3 and r3['p'] and r2 and not r2['p'], rows)
    count = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='The skim test');return c.querySelector('.check-count').textContent})()")
    check('R4 the count is sentences', count == '8 sentences', count)
    await a.ev("document.querySelectorAll('#voiceChecks .skim .op')[5].click()"); await a.wait(300)
    sel = await a.ev("editor.value.slice(editor.selectionStart,editor.selectionEnd)")
    check('R4 a click on a line selects that sentence', sel == 'Structure is what a reader holds in his head while he waits for the verb.', sel)

    # R5 the Library shows no reading grade
    await a.lib()
    row = await a.ev("document.querySelector('.lrow').textContent")
    check('R5 Library rows carry no grade', 'grade' not in row.lower(), row)

    # R6 a lens saved as Difficulty comes back as Runway
    await a.ev("store.set('ww:lens','grade')"); await a.reload()
    await a.ev("setRoom('revise')"); await a.wait(400)
    check('R6 an old Difficulty setting opens as Runway', (await a.ev("$('#lensBtn').textContent")) == 'Lens: Runway', await a.ev("$('#lensBtn').textContent"))

    # R7 lists, quotes, tables, notes and code: the skim test reads prose only, and so does the lens
    await a.fs('write', 'edge.md', ESSAY('Edge', EDGE, 'eeee22'))
    await a.lib(); await a.open('Edge'); await a.settle()
    await a.ev("setRoom('revise')"); await a.ev("setLens('runway')"); await a.wait(500)
    rows = await a.ev("[...document.querySelectorAll('#voiceChecks .skim .op')].map(r=>r.textContent)")
    check('R7 a list marker is not part of an opening', any(r.startswith('A list item') for r in rows), rows)
    check('R7 a quote marker is not part of an opening', any(r.startswith('A quoted paragraph') for r in rows), rows)
    check('R7 notes, code and table rows are not sentences', not any(('note' in r.lower()) or ('compiler' in r) or ('cell' in r) for r in rows), rows)
    check('R7 an abbreviation does not split a sentence', any(r.startswith('Dr. Smith said') for r in rows), rows)
    marks = await a.ev("[...document.querySelectorAll('#editor mark.rw-h,#editor mark.rw-v')].map(m=>m.textContent)")
    check('R7 the lens leaves notes and code alone', not any(('note' in m.lower()) or ('compiler' in m) for m in marks), marks)

EDGE = '\n\n'.join([
    'First line of prose that sets the scene for the reader. The reader keeps going.',
    '- A list item that has a sentence in it. Another sentence in the same item.\n- Second item, short.',
    '> A quoted paragraph says something about quotes. Quotes are other voices.',
    '| Column | Other |\n|---|---|\n| a cell with words | another cell |',
    '%% The note that the writer left in the margin of the draft for the morning after the long night stays out of the count. %%',
    '```\nwhen the compiler that the team built in the long cold winter of the last decade finally runs it fails.\n```',
    'Dr. Smith said it was fine.'])

go(suite)
