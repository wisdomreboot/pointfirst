# Point First changelog

The version number is shown in the command palette under "About Point First". It steps up with each build; the date is when it was cut.

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
