# Point First changelog

The version number is shown in the command palette under "About Point First". It steps up with each build; the date is when it was cut.

## 1.11.0 (2026-10-31)

Tab and Shift+Tab, on any line
- Tab moves every line you are on, or have selected, one step right; Shift+Tab one step back. Before, they only worked in lists and tables, and did nothing in a paragraph.
- Prose steps by an em space. Markdown has no paragraph indent: a tab or four spaces at the start of a paragraph make it a code block in a Ghost Markdown card, Obsidian and GitHub. An em space shows as an indent everywhere and stays prose, and Publish keeps it.
- A list item nests by two spaces, as before. Code in a fence steps two spaces. In a quote, the indent goes after the >. Headings, rules and fence lines stay where they are, and in a table Tab still moves between cells.
- On an empty line, Tab starts an indented paragraph. Shift+Tab takes off an em space, a tab or spaces. Each indent is one step to undo. Esc, then Tab, still leaves the page.

The indent trap
- Slips now marks a paragraph that starts with a tab or four spaces, since Markdown reads it as code. Shift+Tab takes the indent out, and Tab puts in an em space. A list's own continuation and code in a fence are left alone.

## 1.10.0 (2026-10-31)

Moving paragraphs
- Alt+Up and Alt+Down move the paragraph the cursor is in past the one before or after it. The blank lines between them stay where they were. A selection moves every paragraph it touches. A heading moves on its own; a code block or a note keeps the blank lines inside it.
- In a list, the item moves past its neighbour at the same depth, its sub-items with it, and a numbered list keeps counting up.
- Pasted words stay pasted when they move, and a move adds nothing to the words typed today. Each move is one step to undo. Forward only keeps paragraphs where they are while drafting.

Typing
- Two hyphens always become an em dash while smart punctuation is on. The separate switch is gone. Revise still marks every em dash, under Tells.
- Superscript and subscript, as Ghost writes them: 29^th^ and H~2~O. On the page they sit above and below the line, but never inside code, a footnote marker or strikethrough. Type ^ round a selection for superscript; ~ makes subscript, and twice, strikethrough. Publish as HTML turns them into real superscript and subscript, and Publish says where the Markdown marks render.

The palette by keyword
- Insert lists everything the page can take: link, note, table, blockquote, code block and section break. Blockquote, code block and section break are new.
- Format lists what wraps your words: bold, italic, strikethrough, highlight, superscript and subscript.
- Stage lists the stages (Stage: Drafting and the rest), Go to the rooms and your notes, and Move the paragraph moves.
- Gone: Two hyphens to em dash; Open Words, which Coach: Words does, with Alt Shift W; and Copy as Markdown, which copied your notes too, where Publish leaves them out. Check folder resources is now Check folder for word lists.
- The shortcuts list (Ctrl ?) adds the paragraph moves, strikethrough, superscript and subscript, code blocks, and --- as a section break.
- Typing in the palette lists only what matches. Before, every essay showed under any word you typed. A command that already starts with its group, such as Insert link, no longer repeats the group beside it.

## 1.9.0 (2026-10-31)

The coach in the order to revise
- Three tabs where there were five: Reader, Voice and Words. Anatomy and Plan are gone, and Lexicon is now part of Reader, so no finding is counted in two places.
- Reader lists every check and every kind of mark in the order Yellowlees Douglas gives for revising, largest units first: coherence (the skim test, threads), continuity (loose pronouns, echoes), clarity (zombie nouns, passive voice, weak verbs, long runways, punctuation load), concision (qualifiers, clutter), cadence (rhythm, flat paragraphs), then a last pass (tells, slips).
- A kind of mark opens to each of its phrases once, strongest first, with its better word and how often it appears. Click a phrase to find it. Click it again for the next place it appears; its count shows which one you are on.
- Show, on a row, puts that check on the page: Skim for the skim test, Runway for long runways, and the kind itself under Marks. Pressed again, it goes back to every mark.
- Each kind of mark has a level, as the other checks do. Something marked always, any slip, or more than four zombie nouns in the zombie pattern needs work. Something marked usually, or many in context, is worth a look.
- Sentence clutter is now Punctuation load: it counts commas, semicolons, colons, brackets and dashes, not cluttered words. Clutter is now the kind of mark for wordy phrases, empty words, throat-clearing, officialese and clichés.
- Echoes and threads are apart. Echoes are marks, under Continuity. Threads, the key terms you carry on purpose, sit with the skim test under Coherence.
- Voice asks whether any of it is yours: personal or impersonal, first person, quoted words, rare words, the abstract-to-vivid gauge and the four questions.
- Each tab keeps its own place as you move between them, and an open row stays open while you type.

Marks, one kind at a time
- Lens: Marks has a picker, as Word classes does: All, Pronouns, Echoes, Zombies, Passive, Weak verbs, Qualifiers, Clutter, Tells and Slips. Pick one and every mark of that kind shows on the page, whatever the level. The caption counts them by category and says what to look for. The choice is remembered, and each is in the palette.
- All keeps the level, now in its caption: Always, + Usually or Deep edit, each with the number of marks it shows.
- A mark in context has a thin dashed line as well as its shade, so the three strengths (solid, dotted, dashed) read without colour, on the page and in Reader.
- The concreteness gauge has a neutral track, as the rhythm meter does: no red-to-green ramp.

Finding things
- A click on a finding in the coach lands it in view the first time, however far down the page. Before, a finding far off screen could take two or three clicks: the page scrolled to an estimate of where the line would be, before the line was drawn.

Words and your files
- The files card in Words says what each file is for, your lexicon included, and Start your own saves a starter lexicon to your folder. The resources card that sat under Lexicon is gone.
- The word-list pack's Anatomy and Plan files are skipped quietly when you add the pack. Copies already in your folder stay there untouched, and are never listed as essays.
- Essay records no longer keep Plan ticks, and the README in the hidden folder says so.

## 1.8.0 (2026-10-30)

Rhythm replaces burstiness
- The Voice meter now reads rhythm the way a reader hears it, sentence by sentence. Its number is the share of sentences that change pace from the one before: at least half again as long, or a third shorter. The old number was the spread of every sentence length in the essay, which cannot see order. The same sentences in any order scored the same, and an essay made of flat paragraphs could score 100.
- The track has no colour ramp. A shaded band marks where published prose sits, 55 to 70%. Measured on 17,000 paragraphs of speeches, essays, news and novels, published prose sits near 60%, and shuffling each paragraph's sentences gives the same 60%: good writers vary their sentences, they do not alternate them.
- Every sentence is a bar, grouped by paragraph and wrapping, so a long essay shows all of them (the old row drew the first 160). Height is length, with faint lines at 15 and 25 words, and the bars widen when there are fewer to show. Click a bar to select its sentence. The sentence the cursor is in is drawn in full ink.
- Flat paragraphs, new in Voice: paragraphs whose pace never changes. Choppy: four or more sentences, none over 15 words. Heavy: three or more, none under 25. Even: three or more, all within a few words of each other. They are underlined in the bars, and a click on one in the list selects it. About one published paragraph in eleven is flat, so a few are normal, and a tricolon or parallel sentences repeat their length on purpose.
- The meter no longer calls even rhythm a machine tell.

Counting
- Rhythm, the Sentences count and the average length now read the same sentences as the skim test, so the pane's counts agree. A number counts as a word in a sentence's length, since it is heard. Lists are left out of rhythm, and table rows are not sentences.
- "0.6 million" no longer splits a sentence in Voice, and a sentence that ends on a contraction ("It isn't.") no longer runs into the next one anywhere in the app.

## 1.7.0 (2026-10-29)

The Skim lens
- A new lens, first in the menu: Skim. What a reader who skims takes from the page stays in full ink, and the rest fades. The difference is light and dark, never colour.
- Paragraphs: only the first sentence of each paragraph and list item stays dark. Read them alone, top to bottom. This is the skim test from the Anatomy card, on the page: if they tell the argument, the structure works.
- Sentences: each sentence's first words and its last stay dark, the openings and endings the Voice list shows, in place. A word an ending hands to the next opening is underlined in both.
- The choice between them is remembered, and both are in the palette: Skim: Paragraphs, Skim: Sentences.

The tools stay in reach
- In Revise, the tools above the page (Lens, X-ray, Pasted, Claim, Word, Find, Publish, History) stay pinned to the top as you scroll, with the current lens's picker under them. The lens caption is read once and scrolls away.
- Moving the cursor up the page keeps it clear of the pinned tools.
- The lens picker used to come unpinned a short way down a long essay. It stays now.

## 1.6.1 (2026-10-29)

The runway, hardened
- A shade now means what it says. The runway is shown only when every word before the verb is accounted for. A sentence that could be read two ways stays plain, in the lens and in Long runways: a wrong shade misleads, a missing one only goes unseen.
- Measured on 68,000 sentences of real prose (news, essays, speeches, science writing, fiction), each with its main verb found by a full parser, and every shade that disagreed with the parser checked by hand: in 1.6.0, about 7 shades in 10 were right, and some 700 fine sentences were shaded as long. Now 99.8% are right, and 3 are. About half of all long runways are shaded, as before.
- On prose it had never seen, before any fix for that prose, 94% to 98% of shades were right. Expect about one wrong shade in twenty-five on new writing. About half of those fall on a sentence that really is long, with the shade ending early or late.
- It reads more of what essays do: an opening clause or phrase, a subject with a clause inside it, asides in commas, brackets or dashes, a verb phrase as the subject, "what this means is", "we all know", "the question arises", "according to".
- It knows more words that can only be verbs ("depends", "arises", "went") and never takes them for nouns, and more nouns that look like verbs ("high-end sets", "fresh produce", "the four delegates").
- A sentence the runway cannot read stays plain, and the rest of the draft still reads.

Words and sentences
- Two hyphens between words are a dash ("revenues--something" is two words), and so is a hyphen with a space either side. "21st" and "1990s" are one word each.
- "cannot", "after", "ain't" and the "-wise" words are tagged right; "precise", "expertise" and a few others are not taken for verbs.
- A sentence no longer splits after "Gov.", "Lt.", "Jr.", "Ave." and other abbreviations, after "No." before a number, inside a number like "2.5", or before a word that starts in lower case. A closing quote or bracket after a full stop stays with its sentence.

## 1.6.0 (2026-10-28)

The runway replaces the reading grade
- The Difficulty lens, the Hard sentences check and the grade in the Library are gone. They scored sentences with Flesch-Kincaid, which counts syllables and words, so they measured length, not how hard a sentence is to read. Two 32-word sentences, one a sixth grader reads with ease and one most readers need twice, both scored 15.0.
- In their place: the Runway lens, and Long runways in Voice. A runway is the words a reader holds before the main verb arrives: an opening phrase, the subject, anything wedged between subject and verb. Until subject and verb meet, nothing in the sentence has happened.
- The lens shades the runway itself, not the whole sentence. It shades a runway of 12 words or more, or from 6 when the subject is itself a verb phrase ("Seeing the accident from the window…"). 20 and up is underlined too.
- Long runways lists the longest, then the sentences whose subject is a verb phrase. Click one to select its runway in the draft.
- Questions, fragments, headings, notes and code have no runway. Neither does a sentence whose verb the tagger can't find: no answer is better than a wrong one.
- A lens left on Difficulty opens on Runway.

The skim test, finished
- Each line now shows a sentence's first words and its last. Read down the left for the thread. Read each ending into the next opening to see whether the next sentence starts where the last one ended. Read the endings alone for what a reader keeps.
- A word an ending shares with the next opening is underlined in both. A blank line starts a new group; a heading, code or a table breaks the chain.
- Click a line to select its sentence in the draft.
- Tables, notes and code are not sentences here.

## 1.5.0 (2026-10-18)

Tables
- A table in an essay now shows as a table: a quiet grid with the heading row on a faint band, columns aligned by the colons in its dash line, and bold, links and code working inside cells. Move the cursor into it, or click a cell, and it opens to its Markdown for editing, the same way bold opens to its stars. Move on and it becomes a table again.
- Tab goes to the next cell and selects what is in it; Shift+Tab goes back. Tab past the last cell adds a row. Enter adds a row under the one you are in. Enter on an empty last row ends the table, with a blank line after it, the way an empty list item ends a list.
- Insert table, in the palette, starts a blank two-column table with blank lines around it, the first heading selected.
- Arrow keys stop at a table instead of passing over it.
- The file keeps every table exactly as typed. Point First never re-spaces one, so a table moves between Point First, Obsidian, Ghost and Backchat unchanged. Publish already made real HTML tables.
- The shortcuts list has a Tables group.

Counting
- List bullets and lines of dashes no longer count as words. A table's words count; its pipes and dash line do not. In Revise, each table row reads as its own sentence instead of running on into the next.

Writing
- Tab in a paragraph now does nothing, instead of moving the cursor out of the essay. In a list it still indents. Esc then Tab leaves the page, for anyone using the keyboard to move around.

## 1.4.0 (2026-10-17)

Your files, with other apps around
- Point First and Obsidian (or a sync app, or a second Point First tab) can now share an essay without stepping on each other. When you come back to Point First, it looks at the open essay's file. Changed in another app while you had nothing unsaved here: the new version loads where you left off, and what you had goes to History. Changed while you had unsaved words: you choose which to keep, as before. Nothing is overwritten.
- Rename or move an essay in Obsidian while it is open, or while Point First is closed, and Point First follows it by its id. Before, it carried on under the old name and could make a second copy.
- Delete an essay outside Point First while it is open, and Point First says so and never writes it back on its own. Your words are kept, on the page and in its History. Put it back restores it in place, with its history still linked. Close it lets it go.
- A folder that can't be reached (moved, renamed, or a sync drive such as pCloud offline) is named as such. Nothing is ever taken as deleted while the folder itself is out of reach. Your words stay in the browser, and Try again picks up where you were once the folder is back.
- A sync app that touches a file's timestamp without changing its words no longer shows as a change made outside.
- With Point First open in two tabs, a reload could pair one essay's unsaved words with the other essay's file and write them into it. The browser's copy of your draft and the record of which essay it belongs to are now kept together, so that can't happen. When another tab saves the essay you have open, the new version appears at once. The first time a second tab opens, a note says so.
- A save that fails (a sync lock, a full disk) is tried again a few times, further apart each time. The word beside the essay in the top bar now says where your words are: saved means saved in your folder, never only in this browser. It says "not saved", "paused", "needs a choice", "not in folder" or "kept here" when that is the truth.
- History never thins its safety versions: those kept before a disk version loads, before an overwrite or a restore, during a conflict, and around a delete made outside.
- Fewer writes into a synced folder: the daily word count goes to the folder at most once a minute, and when you leave the tab, instead of after every pause.

Fixed
- Library: showing archived essays, then deleting the last one outside Point First, left the Library stuck in an empty archived view until a refresh. The Library button now always leads back to every essay, and the archived view closes itself when nothing is archived.
- Library: right after archiving an essay from its row, it reappeared under Not staged by its file name. It now leaves the list at once.
- A new essay's file was named the moment you paused while typing its title, so a pause halfway gave "Half a.md". The file is named once the title is finished, or once the essay has 25 words.
- Lists: Enter on an empty item now leaves a blank line before the next paragraph, so Markdown keeps that paragraph out of the list. An empty nested item steps out one level first. Enter just after the bullet of an item with words no longer removes the bullet.
- Typing with an input method (Japanese, Chinese, Korean, or accents made with dead keys): Enter that confirms a word no longer starts a list item, leaves the title, opens an essay from Find an essay, or runs Find. Arrow keys that choose a word no longer jump to the title.
- Switching rooms closes whatever was open over the old one: Find, the palette, the shortcuts list, History, Publish, the file list.
- The version shown in the app had stayed at 1.1.2 since the page-view change. It now matches this changelog.

## 1.3.0 (2026-10-17)

Counts read prose only
- Web addresses no longer count as words, and no longer count for or against the ownership meter. `[these words](https://…)` counts as "these words". An essay full of sources reads as yours when the prose is. The Library's % yours, word counts and reading grade follow the same rule.

Keys everyone already knows
- Replace: Ctrl H on Windows and Linux, Cmd Option F on a Mac (Cmd H hides the app there), as in Obsidian, Word and Google Docs. Find opens with the cursor in Replace.
- Next and previous match: Ctrl or Cmd + G and F3, with Shift for back, as well as Enter in the Find box.
- Library: Ctrl or Cmd + F finds an essay. Down goes from the find box to the list, Up and Down move between essays, Enter opens one. N starts a new essay. (Ctrl N can't be used: Chrome keeps it for a new window.)
- Title and page: Enter or Down in the title goes to the start of the page. Up on the page's first line goes back to the title.
- The shortcuts list, the palette and the README show all of these.

Fixed
- Leaving an essay written outside Point First (by New essay, or by opening another) could do nothing the first time. Point First tried to keep a closing version in History, which needed to write an id into the file first. An essay Point First has never saved now keeps no closing version: its file is already that version, and opening or leaving it never writes to it.

## 1.2.0 (2026-10-17)

Links, the way Obsidian and Ghost make them
- Ctrl or Cmd + K makes a link. Selected words become `[words]()` with the cursor ready for the address. A selected address becomes `[](address)` with the cursor where the words go. With nothing selected you get `[]()`.
- Paste a web address over selected words and they become a link. Only the address counts as pasted; the words keep their marks.
- Typing `[` over a selection wraps it as a link too, beside `*`, `_`, `` ` `` and `~`.
- An essay with no title takes its suggested file name from the first line's words, without link addresses or notes.
- The palette moves to Ctrl or Cmd + P, Obsidian's palette key. Ctrl O still opens an essay by name, as Obsidian's quick switcher does.

## 1.1.2 (2026-10-17)

Page-view count
- Point First counts its visits through GoatCounter, which uses no cookies and stores nothing on your device. Each page open sends the page address (never anything after #), the referring site, the page title and the screen size. Nothing you write is sent. It skips your own computer's addresses and the file opened from disk, and #toggle-goatcounter at the end of the address switches it off in that browser. The README and SECURITY.md now say so, in place of "no tracking".
- The first attempt linked GoatCounter's script from its server. The page's security policy refuses that, so nothing was counted, and opened from disk the link broke. The counter is now GoatCounter's pinned version 5, unchanged, inside index.html, and the policy allows the count to reach pointfirst.goatcounter.com and nowhere else.
- A check, tools/check.py, now runs on every pull request: the page boots cleanly under its policy, the counter is still the published file, a real page load sends one count with nothing from after #, and local or from-disk copies send none.

## 1.1.1 (2026-10-16)

Shortcuts
- Ctrl or Cmd + ? opens a list of every shortcut: formatting, Markdown you can type, lists, smart punctuation, editing, Find, Words and moving around. Press ? on its own when you are not typing in the page. It is in the palette too, as Keyboard shortcuts.
- Type in the box at the top to narrow it: "bold" shows bold.
- Mac shows ⌘ and ⌥, Windows and Linux show Ctrl and Alt.
- The palette now has Bold, Italic and Open an essay, and takes its key hints from the same list, so the two always agree.

## 1.1.0 (2026-10-16)

A page that shows structure, not syntax
- The page is now a real Markdown editor. Headings are set in the display face at their own sizes, bold is bold, italic is italic, a link reads as its words, quotes carry a rule, lists keep their shape when a line wraps, and `* * *` sits as a centred break.
- Markdown marks show only where the cursor is. Move into a bold word and its stars appear; move on and they step back. A heading's hashes show while the cursor is on its line. A link's address shows while the cursor is in the link.
- The file is unchanged: still plain Markdown, character for character, so Obsidian, GitHub and Ghost read it exactly as before.
- Ctrl or Cmd + B and I make the selection bold or italic, or undo it if it already is. With nothing selected, they open an empty pair with the cursor inside. They follow the letter, so Dvorak works.
- Everything else carries over: the lenses, X-ray, the Pasted view and Claim, notes, Find and Replace, the word popover, dimming, typewriter scrolling, forward only, smart punctuation and list continuation.
- Typing is faster on long essays.
- The editor is CodeMirror 6, built into the file so Point First still works offline. `tools/codemirror/build.sh` rebuilds it.

## 1.0.9 (2026-10-12)

Not yours until you claim it
- One rule for the ownership meter: anything not written inside Point First is not yours until you claim it. Until now, text that arrived from outside without a paste counted as typed.
- A change made to an essay in another app (Obsidian, a sync, an AI tool) now counts as not yours. The parts you wrote here keep their marks; only what changed is tinted.
- An essay Point First has never saved, such as one written in Obsidian, opens as 0% yours. Opening it still never writes to it.
- Text that comes back from a version in History, or from the disk copy after a clash, counts the same way: what differs from your current draft is not yours until you claim it.
- To claim, select the text and choose Claim (Ctrl or Cmd + A first for the whole essay), or rewrite it.
- Every saved essay now keeps its record in `.pointfirst/records`, so outside changes can always be told apart from your own writing. Essays saved by earlier versions, which kept no record when fully typed, are trusted as yours the first time you open them and get a record then.
- The Library's "% yours" reads the same way, so an essay edited elsewhere shows it there too.

## 1.0.8 (2026-10-11)

Notes
- Write `%% a note to yourself %%` anywhere in a draft, the same syntax Obsidian uses for comments. Ctrl or Cmd + / opens a note at the cursor, turns a selection into one, or, inside a note, removes its markers and keeps the words.
- Notes sit on a faint band in lighter text, so they read as asides without relying on colour.
- The coach treats notes as absent: they don't count as words, never trigger a check, and don't touch the ownership meter. Publish already left them out.
- An "N notes" link beside the word count in Revise lists them; pick one to jump to it. The palette has Add a note and Go to a note.

Section breaks that survive Obsidian
- A line of dashes straight under text is a heading in Obsidian, Ghost and GitHub, not a break. Publish now shows it the same way, and the Lexicon flags it as a Heading trap with the fix: a blank line above the dashes, or `* * *`.

Smart punctuation
- As you type, `...` becomes `…`, straight quotes curl the right way, and apostrophes turn into ’. Never inside inline or fenced code, a link's address, a web address or an HTML tag. Backspace straight after a change puts back what you typed.
- Two hyphens can become an em dash. It starts off, since the Lexicon questions em dashes; turn it on in the palette if you want it. `---` on a line of its own always stays as typed.
- Smart punctuation itself can be turned off in the palette. Both settings travel with the folder.
- The checks read curly apostrophes and the ellipsis character the same as their plain forms, so "it’s" matches the lexicon like "it's", and … ends a sentence like ... does.

Keyboard
- Alt+W now follows the letter W on every layout. On a Mac it used to depend on where the W key sits on a QWERTY keyboard, so it missed on Dvorak; Option+W, which a Mac types as ∑, now counts as W.
- The README lists every shortcut.

## 1.0.7 (2026-10-11)

A security pass. Nothing changes in how Point First looks or works.
- The browser now runs only Point First's own code. The page's security policy names the one inline script by its fingerprint, so code slipped into the page some other way is refused. Point First could already connect to nothing but its own address; that stays.
- Links and images in Publish keep only web, mail and in-page addresses. An essay file carrying a `javascript:` link, for example from a shared folder, now gets a harmless `#` instead.
- Publish formatting can no longer reach inside a link's address, so a crafted address can't break out of it.
- Adding word lists refuses a zip that would unpack to more than any word list needs, so a malformed or hostile zip can't fill the folder or freeze the tab.
- Point First's own records and settings files are checked before use. A damaged or crafted file is ignored instead of hanging the Library or breaking a view.

## 1.0.6 (2026-10-10)

- The Wisdom Reboot mark sits beside the name in the top bar and opens jonathandutoit.com in a new tab, so a link never pulls you away from a draft.
- The Library and the welcome page say who made Point First.
- The W mark is now the favicon and home-screen icon, and the page carries a proper description, share image and search details for when the link is shared or found.
- The Anatomy and Plan files no longer show up in the Library as if they were essays. Only the lexicon was being left out before.

## 1.0.5 (2026-10-10)

Folder first, all the way
- Point First now works only in a connected folder. The folder is the source and the truth, so "Write without a folder" is gone. Write and Revise open once a folder is connected or reconnected.
- A browser that cannot open folders (Safari, Firefox, phones) gets a plain page explaining why, and naming Chrome and Edge.

Word lists the writer brings
- Point First no longer downloads word lists from the site. Download the word-list pack once from the latest GitHub release, then choose **Add word lists** in the Words tab and pick the zip. Point First copies each file into your folder: data lists to `.pointfirst/word-lists`, the starter Markdown files to the top level. It never overwrites a starter you already have.
- Single files work too. A list saved under another name is recognised by its contents and filed under its proper name.

A new Anatomy
- Fourteen cards, rewritten short and plain: one principle per card, in a few lines, with a test to run on your own draft. Each card names its source: Williams, Gopen, Halliday, Fish, Graff and Birkenstein, and Hayakawa.
- **Make these cards yours** saves the built-in cards to `pointfirst-anatomy.md` in your folder, ready to edit. The Plan pane offers the same for `pointfirst-plan.md`. Your file then replaces the built-in; delete it to go back.
- The Plan checklist uses the same plain words as the cards.

## 1.0.4 (2026-10-10)

- The one-click word-list download finishes cleanly. The manifest listed `ABOUT.md` at an older size, so the download saved every list and then stopped with "ABOUT.md arrived incomplete". The sizes now match, and the size check applies only to the data lists, so editing a text file can't break the download again.
- The page now declares itself a standard HTML document, so browsers render it in standards mode rather than quirks mode. Nothing looks different; it just stops depending on browser guesswork.

## 1.0.3 (2026-10-08)

- Publish, Copy HTML, now copies real HTML. Paste into a rich editor like Ghost or Substack and the formatting holds; paste into a plain field or a Ghost HTML card and you get the HTML source, the same `<p>` and `<table>` the Download .html gives. Before, the plain side carried Markdown, so some destinations pasted Markdown from a button called Copy HTML.
- Tables become real tables in HTML. A Markdown pipe table, with or without alignment colons, converts to a `<table>` in the HTML output, the preview and the downloaded file. Markdown output keeps the pipe table as written.

## 1.0.2 (2026-10-08)

- The concrete-detail gauge in Voice now measures real word concreteness, not a count of numbers and capitals. It averages the concreteness of your content words against a 40,000-word human-rated list (Brysbaert et al. 2014), names the most abstract words in your draft so you can act, and labels the ends Abstract and Vivid. A built-in set of common words makes it work offline; the full list ships in the bundle. The gauge measures the words; whether a detail is yours is still the four questions beside it.

## 1.0.1 (2026-10-08)

- Find and Replace is now a button in the Revise toolbar, not only a shortcut, so it does not depend on a key that moves under Dvorak.
- The "You" tab is folded into Voice: the concrete-detail gauge and the four personality questions now sit under Voice, and ownership stays in the top bar and the Pasted lens. Five tabs, not six.
- The version number shows in the Library header, so you can always tell which build you are running.

## 1.0.0 (2026-10-08)

Folder and content
- Anatomy and Plan are no longer locked in the app. Drop `pointfirst-anatomy.md` or `pointfirst-plan.md` in your folder to use your own; delete to return to the built-in. Both are in the resource bundle.
- The one-click download now places editable files (lexicon, anatomy, plan) at the folder top level, and data lists in `.pointfirst/word-lists`. It never overwrites a file you have edited.
- The `.pointfirst` back room is organised: `history/`, `records/`, `word-lists/`, with a README it writes itself.
- Each essay carries a `pointfirst-id` in its frontmatter, so renaming or moving it in Obsidian keeps its history and ownership.

Writing
- Select a word and press `*` `_` `` ` `` `~` to wrap it; press again to double (bold, strikethrough). Selected spaces stay outside the markers.
- Lists continue on Enter and exit on an empty item. Tab and Shift+Tab indent inside a list.
- Selecting a word shows an options chip (Synonyms, In Words). In Words peeks over the page while writing and closes when you click back.
- Alt+W and the other shortcuts match the key you press, so Dvorak and other layouts work.

Revision
- Find and Replace (Ctrl/Cmd+F): live highlight of every match, a map of their positions down the right edge, match case, whole word, and regular expressions. Replacements go in as typed edits, so ownership and undo hold.
- Versions are now numbered (1.0.0), shown under "About Point First".

Publish
- Publish is now Markdown or HTML, with copy and download for each. Markdown is your text unchanged; HTML is the converted version.

Fixes
- Conflicts never lose your text: your version is always kept in History first.
- Plan ticks and voice mode are written before you leave an essay, so a fast switch keeps them.
- A frontmatter change reports the real save result, not a blind success.
- An invalid folder word list no longer wipes a working one.
- Loading a word list by hand files each one by its real kind, and repairs a frequency list that an older build stored as the thesaurus.
- The options chip hides reliably on click-away and Escape.

## Earlier

Point First began as a single-file writing coach: three rooms (Library, Write, Revise), the lenses (Marks, Word classes, Difficulty, Plain), the coach panes (Voice, You, Lexicon, Anatomy, Plan), pasted-versus-typed ownership, the offline Words thesaurus, folder-first durability with History, and the five themes.
