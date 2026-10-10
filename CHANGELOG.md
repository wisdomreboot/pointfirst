# Point First changelog

The version number is shown in the command palette under "About Point First". It steps up with each build; the date is when it was cut.

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
