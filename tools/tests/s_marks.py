import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY
import json

# The coach in the order to revise, after Yellowlees Douglas: Reader holds every check and every
# kind of mark, from paragraphs down to words, then cadence and a last pass. Voice asks whether
# any of it is yours. Words is the thesaurus, and explains every file Point First reads.
# Lens: Marks shows one kind at a time, live on the page, like Word classes. A click in the coach
# lands the first time, however far down the page.

P1 = ('This is the opening line of the essay. It sets the scene in a very plain way. The report was '
      'written by the committee in a hurry, and it was approved by the board.')
P2 = ('Some people say that readers skim. Research suggests that they arguably read the first sentence '
      'and perhaps decide whether the rest is worth their time. They really do, and it is very clear.')
P3 = ('The implementation of the new policy needs careful consideration. We need to delve into the rich '
      'tapestry of reasons, in order to utilize the end result. It seems that the the first sentence '
      'carries the weight, and that is very much the point.')
P4 = 'The budget fell. The budget rose again. Budget talks went on while the budget sat untouched.'
BODY = '\n\n'.join([P1, P2, P3, P4])

KINDS = ['Loose pronouns', 'Echoes', 'Zombie nouns', 'Passive voice', 'Weak verbs', 'Qualifiers', 'Clutter', 'Tells', 'Slips']
ORDER = ['The skim test', 'Threads', 'Loose pronouns', 'Echoes', 'Zombie nouns', 'Passive voice', 'Weak verbs',
         'Long runways', 'Punctuation load', 'Qualifiers', 'Clutter', 'Flat paragraphs', 'Tells', 'Slips']

PAINTED = "[...new Set([...document.querySelectorAll('#editor mark[data-i]')].map(m=>+m.dataset.i))]"

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'marks.md', ESSAY('Marks', BODY, 'mark01'))
    await a.connect()
    await a.open('Marks'); await a.settle()
    await a.ev("setRoom('revise')"); await a.ev("setLens('marks')"); await a.wait(600)

    # M1 three tabs: Reader, Voice, Words. Lexicon, Anatomy and Plan are gone, from the palette too
    tabs = await a.ev("[...document.querySelectorAll('.coach .tab')].map(t=>t.textContent)")
    check('M1 the coach has three tabs: Reader, Voice, Words', tabs == ['Reader', 'Voice', 'Words'], tabs)
    gone = await a.ev("['tab-lex','pane-lex','tab-anat','pane-anat','tab-struct','pane-struct'].filter(id=>document.getElementById(id))")
    check('M1 Lexicon, Anatomy and Plan leave no pane behind', gone == [], gone)
    names = await a.ev("paletteCommands().map(x=>x.label)")
    coach = [n for n in names if n.startswith('Coach: ')]
    check('M1 the palette opens Reader, Voice and Words, and nothing else', coach == ['Coach: Reader', 'Coach: Voice', 'Coach: Words'], coach)

    # M2 Reader runs in Douglas's order: paragraphs first, words last, then cadence and a last pass
    heads = await a.ev("[...document.querySelectorAll('#readChecks .phase-h')].map(h=>h.firstChild.textContent.trim())")
    check('M2 Reader is in the order to revise', heads == ['Coherence', 'Continuity', 'Clarity', 'Concision', 'Cadence', 'Last pass'], heads)
    rows = await a.ev("[...document.querySelectorAll('#readChecks .check-name')].map(x=>x.textContent)")
    check('M2 every check and every kind of mark, each in its stage', rows == ORDER, rows)
    card = await a.ev("(()=>{const r=$('#rhythmCard');return !!r&&r.closest('.vsec').querySelector('.phase-h').firstChild.textContent.trim()})()")
    check('M2 the rhythm card leads Cadence', card == 'Cadence', card)

    # M3 nothing is counted twice: Voice keeps only whether it is yours
    voice = await a.ev("[...document.querySelectorAll('#voiceChecks .check-name')].map(x=>x.textContent)")
    check('M3 Voice checks the writer and their words, no marks', voice == ['The writer (should be absent)', 'Quoted words'], voice)
    check('M3 no check appears in both panes', not (set(voice) & set(rows)), set(voice) & set(rows))
    every = await a.ev("[...document.querySelectorAll('.coach .check-name')].map(x=>x.textContent)")
    check('M3 punctuation is Punctuation load, never Sentence clutter', 'Punctuation load' in every and 'Sentence clutter' not in every, every)
    ask = await a.ev("$('#pane-voice .pane-h').textContent")
    check('M3 Voice asks whether any of it is yours', ask == 'Is any of this yours?', ask)

    # M4 Lens: Marks offers its kinds, in the same order, on one line at a desktop width
    pills = await a.ev("[...document.querySelectorAll('#lenspick [data-mark]')].map(b=>b.textContent)")
    check('M4 the Marks picker offers All, then each kind in Reader\'s order', pills == ['All', 'Pronouns', 'Echoes', 'Zombies', 'Passive', 'Weak verbs', 'Qualifiers', 'Clutter', 'Tells', 'Slips'], pills)
    tops = await a.ev("[...new Set([...document.querySelectorAll('#lenspick [data-mark]')].map(b=>Math.round(b.getBoundingClientRect().top)))].length")
    check('M4 the picker fits one line beside the page', tops == 1, tops)
    fam = await a.ev("JSON.stringify(Object.fromEntries(Object.keys(MFAM).filter(k=>k!=='all').map(k=>[k,MFAM[k][3]])))")
    check('M4 each pill is a Reader row', list(json.loads(fam).values()) == KINDS, fam)
    marks = [n for n in names if n.startswith('Marks: ')]
    check('M4 the palette reaches every kind', marks == ['Marks: ' + p for p in pills], marks)
    await a.ev("paletteCommands().find(x=>x.label==='Marks: Zombies').run()"); await a.wait(300)
    check('M4 and puts it on the page', (await a.ev("[lens,markFam]")) == ['marks', 'zom'], await a.ev("[lens,markFam]"))
    await a.ev("setMarkFam('all')"); await a.wait(200)

    # M5 one kind: every one of it on the page, at every level, and nothing else
    await a.ev("setLevel('always')"); await a.ev("setMarkFam('pas')"); await a.wait(400)
    shown = await a.ev(PAINTED)
    want = await a.ev("hits.map((h,i)=>MFAM.pas[2].includes(h.cat)?i:-1).filter(i=>i>=0)")
    check('M5 Passive paints every passive, though they are in context and the level is Always', len(want) == 2 and sorted(shown) == want, (shown, want))
    words = await a.ev("[...new Set([...document.querySelectorAll('#editor mark[data-i]')].map(m=>m.textContent))]")
    check('M5 the passives are the ones written', words == ['was written', 'was approved'], words)
    cap = await a.ev("$('#lensbar').textContent")
    check('M5 the caption counts them and says what to look for', cap.startswith('2 passives.') and 'name them' in cap, cap[:90])
    pressed = await a.ev("[...document.querySelectorAll('#lenspick [aria-pressed=true]')].map(b=>b.textContent)")
    check('M5 its pill is pressed', pressed == ['Passive'], pressed)
    await a.ev("setMarkFam('qual')"); await a.wait(300)
    cap = await a.ev("$('#lensbar').textContent")
    check('M5 a mixed kind counts by category', cap.startswith('3 intensifiers') or ('intensifiers' in cap.split('.')[0] and 'hedges' in cap.split('.')[0]), cap[:90])
    style = await a.ev("(()=>{const m=[...document.querySelectorAll('#editor mark[data-s=c]')][0];return m?getComputedStyle(m).textDecorationStyle:null})()")
    check('M5 a mark in context has a dashed line, so strength reads without colour', style == 'dashed', style)
    await a.ev("setMarkFam('zom')"); await a.wait(300)
    cap = await a.ev("$('#lensbar').textContent")
    check('M5 without nominalizations.txt, Zombies says only the lexicon\'s are marked', 'nominalizations.txt' in cap, cap[-140:])

    # M6 All keeps the level, in its caption, with what each level would show
    await a.ev("setMarkFam('all')"); await a.wait(300)
    lv = await a.ev("[...document.querySelectorAll('#lensbar [data-sev]')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    counts = await a.ev("[hits.filter(h=>h.sev==='a').length,hits.filter(h=>h.sev!=='c').length,hits.length]")
    check('M6 the level buttons carry what each shows', lv == ['Always %d' % counts[0], '+ Usually %d' % counts[1], 'Deep edit %d' % counts[2]], (lv, counts))
    shown = await a.ev(PAINTED)
    check('M6 at Always, only marks that are always worth a look', len(shown) == counts[0] and counts[0] > 0, (len(shown), counts))
    await a.ev("document.querySelector('#lensbar [data-sev=all]').click()"); await a.wait(300)
    shown = await a.ev(PAINTED)
    check('M6 Deep edit shows them all, and is remembered', len(shown) == counts[2] and (await a.ev("store.get('ww:sev')")) == 'all', (len(shown), counts))

    # M7 the kind is remembered between visits
    await a.ev("setMarkFam('echo')"); await a.reload(); await a.ev("setRoom('revise')"); await a.wait(600)
    pressed = await a.ev("[...document.querySelectorAll('#lenspick [aria-pressed=true]')].map(b=>b.textContent)")
    check('M7 the chosen kind survives a reload', pressed == ['Echoes'] and (await a.ev("store.get('ww:mark')")) == 'echo', pressed)
    await a.ev("setMarkFam('all')"); await a.wait(300)

    # M8 Show in Reader puts a row on the page; pressed again, it goes back to every mark
    def row(name): return "[...document.querySelectorAll('#readChecks .check')].find(x=>x.querySelector('.check-name').textContent==='%s')" % name
    await a.ev("(()=>{%s.querySelector('.show').click()})()" % row('Passive voice')); await a.wait(300)
    st = await a.ev("[lens,markFam,%s.querySelector('.show').textContent]" % row('Passive voice'))
    check('M8 Show on Passive voice puts the passives on the page', st == ['marks', 'pas', 'On page'], st)
    pressed = await a.ev("[...document.querySelectorAll('#lenspick [aria-pressed=true]')].map(b=>b.textContent)")
    check('M8 and the picker agrees', pressed == ['Passive'], pressed)
    await a.ev("(()=>{%s.querySelector('.show').click()})()" % row('Passive voice')); await a.wait(300)
    st = await a.ev("[lens,markFam,%s.querySelector('.show').textContent]" % row('Passive voice'))
    check('M8 pressed again, it goes back to every mark', st == ['marks', 'all', 'Show'], st)
    await a.ev("(()=>{%s.querySelector('.show').click()})()" % row('The skim test')); await a.wait(300)
    check('M8 Show on the skim test puts the Skim lens on', (await a.ev("lens")) == 'skim', await a.ev("lens"))
    await a.ev("(()=>{%s.querySelector('.show').click()})()" % row('Long runways')); await a.wait(300)
    st = await a.ev("[lens,%s.querySelector('.show').textContent,%s.querySelector('.show').textContent]" % (row('Long runways'), row('The skim test')))
    check('M8 Show on Long runways puts the Runway lens on, and only it is pressed', st == ['runway', 'On page', 'Show'], st)
    none = await a.ev("(()=>{const r=%s;return [r.querySelector('.check-count').textContent,!!r.querySelector('.show')]})()" % row('Slips'))
    check('M8 a kind with nothing in the draft offers no Show', none[1] is False or none[0] != '0', none)

    # M9 a phrase finds its first place, then the next, round to the first again
    await a.ev("setLens('off')"); await a.wait(300)
    await a.ev("(()=>{const r=%s;r.querySelector('.check-row').click()})()" % row('Qualifiers')); await a.wait(200)
    at = []
    for _ in range(4):
        await a.ev("(()=>{const x=[...document.querySelectorAll('#readChecks .lex-item')].find(e=>e.querySelector('.ph').textContent==='very');x.click()})()"); await a.wait(250)
        at.append(await a.ev("editor.selectionStart"))
    want = await a.ev("(()=>{const v=editor.value,o=[];let i=-1;while((i=v.indexOf('very',i+1))>=0)o.push(i);return o})()")
    check('M9 three clicks find the three places, the fourth comes round', len(want) == 3 and at == want + want[:1], (at, want))
    badge = await a.ev("[...document.querySelectorAll('#readChecks .lex-item')].find(e=>e.querySelector('.ph').textContent==='very').querySelector('.n').textContent")
    check('M9 the count says which one is found', badge == '1 of 3', badge)
    strong = await a.ev("[...document.querySelectorAll('#readChecks .lex-item .ph')].map(p=>p.className)")
    check('M9 each phrase is underlined as on the page', all(c in ('ph ka', 'ph ku', 'ph kc') for c in strong) and strong, strong[:6])

    # M10 an open row stays open while the writer types
    await a.ev("editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length)")
    await a.pg.keyboard.type(' More.'); await a.wait(700)
    open_ = await a.ev("%s.querySelector('.check-row').getAttribute('aria-expanded')" % row('Qualifiers'))
    check('M10 Qualifiers stays open through a repaint', open_ == 'true', open_)

    # M11 levels: a slip needs work; a few in context are fine; many are worth a look
    lv = await a.ev("Object.fromEntries([...document.querySelectorAll('#readChecks .check')].map(x=>[x.querySelector('.check-name').textContent,x.querySelector('.pip').className.replace('pip ','')]))")
    check('M11 a doubled word is a slip that needs work', lv.get('Slips') == 'crit', lv)
    check('M11 two passives in context are fine', lv.get('Passive voice') == 'ok', lv)

    # M12 each tab keeps its own place
    await a.ev("$('.panes').scrollTop=600"); await a.ev("$('#tab-voice').click()"); await a.wait(200)
    top = await a.ev("$('.panes').scrollTop")
    check('M12 Voice opens at its top, not at Reader\'s place', top == 0, top)
    await a.ev("$('#tab-read').click()"); await a.wait(200)
    top = await a.ev("$('.panes').scrollTop")
    check('M12 Reader opens where it was left', abs(top - 600) < 2, top)

    # M13 the first click lands, however far down the page
    far = '\n\n'.join(['Paragraph %d of the long essay says one plain thing about the work and stops there.' % i for i in range(160)]
                      + ['At the very end the essay will utilize one word that is never needed.'])
    await a.fs('write', 'far.md', ESSAY('Far', far, 'far001'))
    await a.lib(); await a.open('Far'); await a.settle()
    await a.ev("setRoom('revise')"); await a.ev("setLens('off')"); await a.wait(500)
    await a.ev("$('.editor-wrap').scrollTop=0;editor.setSelectionRange(0,0)"); await a.wait(300)
    await a.ev("(()=>{const r=%s;r.querySelector('.check-row').click()})()" % row('Clutter')); await a.wait(200)
    await a.ev("[...document.querySelectorAll('#readChecks .lex-item')].find(e=>e.querySelector('.ph').textContent==='utilize').click()"); await a.wait(700)
    seen = await a.ev("""(()=>{const s=editor.selectionStart,r=ED.view.coordsAtPos(s),w=$('.editor-wrap').getBoundingClientRect(),h=$('#rhead').getBoundingClientRect();
      return {sel:editor.value.slice(s,editor.selectionEnd),on:!!r&&r.top>=h.bottom&&r.bottom<=w.bottom}})()""")
    check('M13 a phrase two hundred lines down is on screen after one click', seen['sel'] == 'utilize' and seen['on'], seen)
    await a.ev("setLens('marks');setMarkFam('clut')"); await a.ev("$('.editor-wrap').scrollTop=0"); await a.wait(400)
    await a.ev("[...document.querySelectorAll('#readChecks .lex-item')].find(e=>e.querySelector('.ph').textContent==='utilize').click()"); await a.wait(700)
    seen = await a.ev("""(()=>{const f=document.querySelector('#editor mark.flash');if(!f)return null;const r=f.getBoundingClientRect(),w=$('.editor-wrap').getBoundingClientRect(),h=$('#rhead').getBoundingClientRect();return {t:f.textContent,on:r.top>=h.bottom&&r.bottom<=w.bottom}})()""")
    check('M13 with its kind on the page, it is flashed in place, on screen', seen is not None and seen['t'] == 'utilize' and seen['on'], seen)
    await a.ev("setMarkFam('all')")

    # M14 the retired Anatomy and Plan files are not essays, and records keep no Plan ticks
    await a.fs('write', 'pointfirst-anatomy.md', '# Anatomy of a clear essay\n\n### Point first\n\nA card.\n')
    await a.fs('write', 'pointfirst-plan.md', '## Introduction\n\n- Hook | A line\n')
    await a.lib()
    titles = await a.rows()
    check('M14 the Library lists neither old file', not any('Anatomy' in t or 'Plan' in t or 'pointfirst' in t for t in titles), titles)
    await a.open('Marks'); await a.ev("setRoom('revise')"); await a.wait(300)
    await a.ev("$('#mPersonal').click()"); await a.settle(2600)
    recs = [p for p in (await a.fs('list')) if p.startswith('.pointfirst/records/') and p.endswith('mark01.json')]
    rec = json.loads(await a.read(recs[0])) if recs else {}
    check('M14 a record keeps the voice mode and no Plan ticks', rec.get('mode') == 'personal' and 'plan' not in rec and 'Plan' not in rec.get('note', ''), (recs, rec.get('mode'), rec.get('note')))
    await a.ev("$('#mImpersonal').click()"); await a.wait(300)

    # M15 Words explains every file, the lexicon too, and starts your own when there is none
    await a.ev("$('#tab-words').click()"); await a.wait(500)
    card = await a.ev("$('#wLocal').textContent")
    check('M15 the files card names pointfirst-lexicon.md and what it is for', 'pointfirst-lexicon.md' in card and 'marked under Tells' in card, card[-260:])
    check('M15 and what each word list adds', 'rare-word check in Voice' in card and 'for Reader and Lens: Marks' in card, card[:400])
    await a.ev("document.querySelector('#wLocal [data-starter=lex]').click()"); await a.wait(1200)
    txt = await a.read('pointfirst-lexicon.md')
    check('M15 Start your own writes the lexicon to the folder', txt.startswith('# Point First lexicon'), txt[:40])
    check('M15 and Point First reads it at once', await a.ev("!!R.lex"), '')

go(suite)
