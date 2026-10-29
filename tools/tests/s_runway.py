import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

# The runway is shown only when every word before the verb is accounted for. Each case marks
# the main verb in [brackets] and says what the lens must do with the sentence:
#   short   the verb is found, and the runway is too short to shade
#   long    the verb is found, and 12 to 19 words come before it
#   very    the verb is found, and 20 or more words come before it
#   verbal  the subject is a verb phrase of 6 words or more
#   doubt   the sentence reads two ways, so the runway stays plain
#   quiet   whatever is found, nothing is shaded
#   none    no runway at all: a question, a headline, a fragment
# A wrong shade is a lie; a missing one only goes unseen. So "quiet" and "doubt" are as
# much a pass as "long".

CASES = [
    ("Writers [cut] what the reader does not need.", "short"),
    ("The draft [was] too long by a third.", "short"),
    ("Most readers [skim] the first paragraph and then decide.", "short"),
    ("The committee that reviewed the proposals from the three regional offices last spring [approved] the plan in June.", "long"),
    ("A writer who has spent twenty years editing other people's prose for a living [knows] where sentences break.", "long"),
    ("The argument that a short sentence is always clearer than a long one, which most style guides repeat without evidence of any kind, [falls] apart on the first page of any good novel.", "very"),
    ("When the editor finally returned the manuscript with notes on every page, the author [rewrote] the opening.", "long"),
    ("After the war, the town [rebuilt] its library.", "short"),
    ("In the second half of the nineteenth century, long before anyone had heard of the telephone, the mail [arrived] twice a day.", "long"),
    ("Seeing the accident from the upstairs window [changed] how she drove.", "verbal"),
    ("To finish a draft before the outline is settled [is] to build a house without a plan.", "verbal"),
    ("Rising prices across the whole of the country hurt families on fixed incomes.", "quiet"),
    ("To keep the reader with you a writer [needs] short openings.", "short"),
    ("The essay, which had been rejected by four magazines in a single year, [won] the prize.", "long"),
    ("My grandmother, a teacher for forty years in the same small village school, [read] every word I wrote.", "long"),
    ("The first draft (written in a single night, as most first drafts are) [needed] a week of repair.", "long"),
    ("The best editors -- and there are fewer of them every year -- [ask] what the writer meant before they cut.", "short"),
    ("The trouble with most long sentences, she argues, is not their length but their order.", "doubt"),
    ("In nearly every essay that reaches the final round of the competition, the judges say, the opening paragraph carries more weight than the rest.", "doubt"),
    ("Why does the verb arrive so late in this sentence?", "none"),
    ("[Read] the sentence aloud before you decide.", "short"),
    ("The arguments she makes in the second chapter of her book about the origins of writing rest on a single study.", "doubt"),
    ("If the subject is long and the verb is buried at the end of the sentence, the reader [loses] the thread.", "long"),
    ("Because the subject runs on for a full line and a half the reader forgets what it was.", "doubt"),
    ("The evidence from three separate studies of reading speed in adults and children strongly undercuts the claim.", "quiet"),
    ("The new tax plan for small family businesses in the three northern states [cuts] their rates by half.", "long"),
    ("Sales of the new edition [rose] by half in the first three months.", "short"),
    ("Moody's [said] the outlook for the region had darkened.", "short"),
    ("This [suggests] that the reader never needed the second paragraph at all.", "short"),
    ("What matters [is] the order of the words, not their number.", "short"),
    ("Had the editor read the whole draft before the meeting on Friday, she [would] have cut the second half.", "long"),
    ("As the evidence piled up over the course of the long winter, the committee [changed] its mind.", "long"),
    ("As a result, the company [lost] its best writers.", "short"),
    ("The Long Road Home From The War", "none"),
    ("Two failed attempts at the summit in a single season [ended] his career.", "short"),
    ("The complaint filed by the tenants of the building on the corner of Fifth and Main last week was dismissed.", "doubt"),
    ("Writing, he argues, is thinking on paper.", "quiet"),
    ("Being born to wealthy parents bound to not let you fail [can] prove to be a hefty handicap.", "verbal"),
    ("Nothing in the sentence happens until the subject meets its verb.", "quiet"),
    ("The pages that the students who joined the course in its second year wrote by hand [were] lost in the fire.", "long"),
    ("Every sentence we write in a hurry needs a second look.", "quiet"),
    ("People who read the draft aloud to someone else before sending it out catch more of their own mistakes.", "quiet"),
    ("Although the first version of the essay ran to nine thousand words and three appendices, the second [ran] to four.", "long"),
    ("Although tired, the editor [finished] the last chapter that night.", "short"),
    ("While in Rome, she [wrote] most of the second book.", "short"),
    ("The writers whose drafts were returned with the most notes in the first round of reviews [improved] the most.", "long"),
    ("Those who, because of the deadline and the pressure of the coming election, rushed the final edit [regretted] it.", "long"),
    ("The difference between a writer who revises and one who does not [shows] in every paragraph.", "long"),
    ("Interest in the long sentence, once the pride of every serious nineteenth-century novelist, [has] faded.", "long"),
    ("Under the old rules of the house, every manuscript that came in through the front door [went] to the senior editor first.", "long"),
    ("Under the old rules every manuscript went straight to the senior editor.", "quiet"),
    ("The idea that readers want simple sentences [is] wrong.", "short"),
    ("The idea that readers who are given simple sentences with short subjects understand them faster [is] older than the research.", "long"),
    ("Clear prose, according to the editors who have spent their careers on it, [is] mostly a matter of order.", "long"),
    ("Nobody who has tried to cut a long subject down to a single noun phrase [thinks] the job is easy.", "long"),
    ("Short subjects with their verbs close behind them make for quick reading.", "quiet"),
    ("To read a sentence whose subject runs on for twenty words before the verb arrives [is] to hold your breath.", "long"),
    ("Holding the whole subject in mind while waiting for the verb [tires] the reader.", "verbal"),
    ("Engineering students in the final year of the course [are] given a long reading list.", "short"),
    ("The first three pages of the report, the ones that every board member is guaranteed to read, [carry] the whole argument.", "long"),
    ("Every one of the forty sentences in the opening chapter of the novel [begins] with its subject.", "long"),
    ("\"Cut the first paragraph,\" the editor said.", "quiet"),
    ("The phrase \"in order to\" adds nothing that \"to\" does not already say.", "quiet"),
    ("A sentence with no verb at all, just a long list of nouns and adjectives and the odd adverb.", "quiet"),
    ("The horse raced past the barn fell.", "quiet"),
    ("The old man the boats.", "quiet"),
    ("In 1990 sales of the paper edition in the northern territories rose by a third.", "quiet"),
    ("If, in drafting the letter for the third time, you notice the same clumsy opening, you [have] found the sentence to cut.", "long"),
    ("Since nobody in the room had read the report from beginning to end, the vote [went] the wrong way.", "long"),
    ("The report, published in March after two years of delay and three changes of editor, [said] nothing new.", "long"),
    ("Most of the readers who wrote in after the first issue appeared asked for shorter articles.", "quiet"),
    ("None of the changes the editor made to the third chapter in the final week before printing [survived] the review.", "quiet"),
    ("Each of the forty writers who took part in the study of revision habits [kept] a diary.", "long"),
    ("The more the subject grows, the longer the reader waits.", "quiet"),
    ("Readers of long sentences, especially those whose subjects run for more than a line, lose track.", "quiet"),
    ("Wherever the main verb falls late in a sentence that carries a heavy load of clauses, the reader [slows] down.", "long"),
    ("Only when the subject has finally been introduced and the verb has arrived does the sentence begin to mean something.", "quiet"),
    ("Writers who learned to write in school where long sentences earned praise [find] the habit hard to break.", "long"),
    ("She cut it.", "none"),
    ("Done well, the long sentence [rewards] the reader.", "short"),
    ("Written in a single afternoon and never revised, the opening chapter [carries] the marks of haste on every page.", "short"),
    ("The teacher [takes] hold of the problem before the class has even noticed it.", "short"),
    ("Adolescence in general [appears] to have been a hard time for the poets of that century.", "short"),
    ("We all [know] that the second draft is where the real work begins.", "short"),
    ("What this means [is] that the reader holds the subject for longer than we think.", "short"),
    ("Vast new growth and change [are] the two certainties of the coming decade.", "short"),
    ("The four other grower delegates all [represented] the same interests in the debate.", "short"),
    ("These [receive] chemical fuel through a circulatory system and turn it into motion.", "short"),
    ("Why, it [looks] as though the reader had given up before the second page.", "short"),
    ("According to the three editors who read the first draft of the essay last spring, the opening [runs] far too long.", "long"),
    ("The fact that the essay has for the first time introduced a real counterargument [is] a step forward.", "long"),
    ("A man and a woman meet and something clicks.", "quiet"),
    ("Our national goal for the coming years - full employment - [requires] that we act now.", "short"),
    ("The simple but frustrating problem of matching what we spend to what we earn--something every family does--[has] caused trouble for years.", "long"),
    ("Assuming the weather holds through the weekend, the whole family [will] walk to the lake.", "short"),
    ("\"If this patient is awake, why can't she move?\" asks the doctor in charge.", "none"),
    ("Those that combine the old work of the family and the school in a single building [hold] the most promise.", "long"),
    ("Enterprises of the highest importance to our well-being [unite] us.", "short"),
    ("The quest for excellence in the 21st century [begins] in the schoolroom.", "short"),
    ("Our working men and women, instead of being forced to beg for help once they are old, [should] start saving now.", "long"),
    ("The trust the people have placed in us constrains every choice we make.", "quiet"),
    ("Every writer who drafts in the morning to beat the noise of the day and loses the thread by noon [learns] to keep notes.", "very"),
    ("If love reflects the nature of the person, as the poets say, then the writers of that age [were] right to dwell on it.", "long"),
    ("The research also sheds more light on how we remember what we read.", "quiet"),
    ("In hunter-gatherer societies, that maturity [was] probably reached in the late teens, he says.", "short"),
    ("Nellie [ain't] near strong enough to have done it alone.", "short"),
    ("The research [shows], i.e. the numbers show, that long subjects slow readers down.", "short"),
]

# Every case in one call: the page's own tagger, splitter and runway, the way Revise runs them.
RUN = """(cases) => {
  const LONG = 12, VERY = 20, VERBAL = 6;
  const level = (x) => !x || x.doubt ? 0 : x.n >= VERY ? 2 : (x.n >= LONG || (x.verbal && x.n >= VERBAL)) ? 1 : 0;
  return cases.map(([raw, want]) => {
    const m = /\\[([^\\]]+)\\]/.exec(raw);
    const s = raw.replace(/\\[([^\\]]+)\\]/, '$1');
    const toks = WS.tagTokens(WS.tokenizeLine(s), s);
    const seg = WS.wsSentences(s)[0];
    const st = toks.filter(t => t.from >= seg.from && t.to <= seg.to);
    const res = st.length >= 4 ? WS.findRunway(st, s) : null;
    const wantN = m ? toks.filter(t => t.from < m.index).length : null;
    const lv = level(res);
    let ok;
    switch (want) {
      case 'short': ok = !!res && res.n === wantN && lv === 0; break;
      case 'long': ok = !!res && res.n === wantN && lv === 1; break;
      case 'very': ok = !!res && res.n === wantN && lv === 2; break;
      case 'verbal': ok = !!res && res.n === wantN && lv === 1 && res.verbal; break;
      case 'doubt': ok = !!res && res.doubt; break;
      case 'quiet': ok = lv === 0; break;
      case 'none': ok = res === null; break;
    }
    return [ok, res ? `n=${res.n} ${res.verb.w}${res.doubt ? ' doubt' : ''}${res.verbal ? ' verbal' : ''}` : 'null'];
  });
}"""

SURE = 'The committee that reviewed the proposals from the three regional offices last spring approved the plan in June.'
TWOWAYS = 'The arguments she makes in the second chapter of her book about the origins of writing rest on a single study.'

async def suite(c):
    a = await c.tab()

    # RW1 every case, read the way Revise reads it
    got = await a.ev(RUN, CASES)
    for (raw, want), (ok, res) in zip(CASES, got):
        check('RW1 %-6s %s' % (want, raw.replace('[', '').replace(']', '')[:70]), ok, res)

    # RW2 the words themselves: a dash typed as two hyphens parts two words; "21st" is one
    toks = await a.ev("['revenues--something', 'the 21st century', 'the 1990s', 'well-known'].map(s => WS.tokenizeLine(s).map(t => t.w))")
    check('RW2 two hyphens between words are a dash', toks[0] == ['revenues', 'something'], toks[0])
    check('RW2 an ordinal is one word', toks[1] == ['the', '21st', 'century'], toks[1])
    check('RW2 a decade is one word', toks[2] == ['the', '1990s'], toks[2])
    check('RW2 one hyphen still joins a word', toks[3] == ['well-known'], toks[3])

    # RW3 a sentence that reads two ways stays plain in the lens and out of Voice
    await a.fs('write', 'twoways.md', ESSAY('Two ways', SURE + ' ' + TWOWAYS, 'rw0001'))
    await a.connect()
    await a.open('Two ways'); await a.settle()
    await a.ev("setRoom('revise')"); await a.wait(500)
    S = await a.ev("proseRun(editor.value).sents.map(x => ({label: x.label, rw: x.rw, doubt: x.doubt}))")
    sure = next((x for x in S if x['label'].startswith('The committee')), None)
    two = next((x for x in S if x['label'].startswith('The arguments')), None)
    check('RW3 the sure sentence has a long runway', sure and sure['rw'] == 13 and not sure['doubt'], sure)
    check('RW3 the other reads two ways', two and two['doubt'], two)
    await a.ev("setLens('runway')"); await a.wait(500)
    marks = await a.ev("[...document.querySelectorAll('#editor mark.rw-h,#editor mark.rw-v')].map(m=>m.textContent)")
    check('RW3 the lens shades the sure runway', any(m.startswith('The committee') for m in marks), marks)
    check('RW3 the lens leaves the doubtful one plain', not any('arguments she makes' in m for m in marks), marks)
    chips = await a.ev("(()=>{const c=[...document.querySelectorAll('#voiceChecks .check')].find(x=>x.querySelector('.check-name').textContent==='Long runways');return c?[...c.querySelectorAll('.hit')].map(h=>h.textContent):[]})()")
    check('RW3 Long runways lists the sure one', any(x.startswith('The committee') for x in chips), chips)
    check('RW3 Long runways leaves out the doubtful one', not any(x.startswith('The arguments') for x in chips), chips)

    # RW4 a sentence the runway cannot read leaves the rest of the draft readable
    # (a text of its own: proseRun keeps the last draft it read)
    r = await a.ev("(()=>{const f=WS.findRunway;WS.findRunway=()=>{throw new Error('unreadable')};try{const P=proseRun(editor.value+'\\n\\nA third sentence for this check alone.');return {n:P.sents.length,plain:P.sents.every(x=>x.rw===null)}}finally{WS.findRunway=f}})()")
    check('RW4 a runway that fails leaves its sentence plain, and the draft still reads', r['n'] == 3 and r['plain'], r)

    # RW5 speed: a long draft reads at once
    ms = await a.ev("""(()=>{const w='the writer who revised the long opening of the essay twice before sending it to the editor finally cut the second paragraph because nobody needed it'.split(' ');
      let s='';for(let i=0;i<400;i++){const k=(i*7)%w.length;s+=w.slice(k).concat(w.slice(0,k)).join(' ')+'. '}
      const t=performance.now();proseRun(s);return performance.now()-t})()""")
    check('RW5 400 long sentences read in under a second', ms < 1000, ms)

go(suite)
