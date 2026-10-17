# Point First

**A writing desk that coaches and never writes for you.**

Open it at **https://pointfirst.jonathandutoit.com**

## What it is

Point First is one HTML file for writing essays in your own voice. It reads and saves plain Markdown files in a folder you choose, such as your essays folder in Obsidian, and coaches while you write. It never generates, rewrites or suggests prose. It asks. The writer writes.

Everything runs in your browser. There is no server, no account and no cookies. The page counts its own visits (see Page-view count below), and nothing you write is ever sent anywhere. Point First works only in a folder you connect: your essays, their history, Point First's own records and its word lists all live there, so clearing the browser loses nothing. It needs a browser that can open a folder: Chrome or Edge on a computer.

**Three rooms**

- **Library:** your essays, by stage.
- **Write:** the page, and nothing else.
- **Revise:** the lenses, checks and the coach.

**Five coach tabs**

- **Voice:** sentence rhythm, the skim test, zombie nouns, passive voice, and an Abstract-to-Vivid gauge.
- **Lexicon:** words and phrases worth a second look.
- **Words:** meanings and synonyms by sense, offline.
- **Anatomy:** the principles of a clear essay, one per card, each with a test.
- **Plan:** a structure checklist.

**Also included**

- **Ownership tracking:** every character is tagged as written here or not, and a meter shows how much of the draft is yours. The rule: anything not written inside Point First is not yours until you claim it. Pasted text, an essay written in another app, and a change made to an essay outside Point First all count as not yours. Rewrite it, or select it and choose Claim.
- **Find and Replace,** with a map of matches.
- **Version history,** kept before anything replaces text.
- **Safe beside other apps:** edit an essay in Obsidian and Point First shows the new version when you come back, keeping what you had in History. Rename or move an essay and Point First follows it. Delete one and Point First never writes it back unless you choose Put it back. If the folder can't be reached, say a sync drive is offline, nothing is taken as deleted and your words wait in the browser until it returns.
- **Publish** as Markdown or HTML.
- **Notes:** write `%% a note to yourself %%` anywhere, as in Obsidian. Notes stay in the file, sit shaded on the page, and are left out of the word count, the checks, the ownership meter and Publish.
- **Smart punctuation:** `...` becomes `…` and quotes curl as you type, but never inside code or a link's address. Backspace straight after puts back what you typed. Two hyphens can become an em dash if you turn that on.

## Keyboard

Ctrl on Windows and Linux, Cmd on a Mac. Where Obsidian, Ghost, Word and Google Docs agree on a key, Point First uses that key. Shortcuts follow the letter, not the key's position, so they work on Dvorak and other layouts. Ctrl ? lists them all inside the app.

| Keys | Does |
|---|---|
| Ctrl P | Command palette: every command and every essay |
| Ctrl O | Open an essay by name |
| Ctrl S | Save (Point First also saves as you write) |
| Ctrl ? | Every shortcut, in one list |
| Ctrl B, Ctrl I | Bold, italic; press again to take it off |
| Ctrl K | Link: selected words become `[words]()`, ready for the address |
| Paste an address over selected words | Link them |
| Ctrl / | Add a note, turn the selection into one, or remove a note's markers |
| Ctrl F | Find (in the Library, find an essay) |
| Ctrl H, or Cmd Option F on a Mac | Replace |
| Enter, Ctrl G or F3 | Next match; add Shift for the previous one |
| Ctrl Z, Ctrl Y or Ctrl Shift Z | Undo, redo |
| Alt 1, 2, 3 | Library, Write, Revise |
| N | New essay, in the Library |
| Up, Down | Move between essays in the Library |
| Enter in the title | Go to the page; Up on the page's first line goes back |
| Alt W | Look up the word at the cursor |
| Alt Shift W | Open the Words tab |
| `*` `_` `~` `` ` `` or `[` with text selected | Wrap the selection; `[` makes it a link |
| Enter in a list | Continue the list; on an empty item, end it |
| Tab, Shift Tab in a list | Indent, outdent |
| Esc | Close whatever is open |

Ctrl N can't be used for a new essay: Chrome keeps it for a new window.

## Section breaks

Use `* * *` on its own line, or `---` with a blank line above it. A line of dashes straight under text turns that text into a heading in Obsidian, Ghost and GitHub; Point First shows it the same way and flags it in the Lexicon.

## Word lists

Words, the zombie-noun check, the rare-word check and the concreteness gauge read word lists from your folder. Point First never fetches them. To add them:

1. Download [pointfirst-word-lists.zip](https://github.com/wisdomreboot/pointfirst/releases/latest/download/pointfirst-word-lists.zip) from the latest release (about 15 MB).
2. In Point First, open the Words tab, choose **Add word lists**, and pick the zip.

Point First copies the data lists into `.pointfirst/word-lists` and three editable starter files (lexicon, Anatomy, Plan) to the top level of your folder. Where each list comes from is described in `ABOUT.md` inside the pack.

## Make it yours

The Anatomy cards, the Plan checklist and the lexicon are plain Markdown files. Keep your own `pointfirst-anatomy.md`, `pointfirst-plan.md` or `pointfirst-lexicon.md` at the top level of your folder and Point First uses yours instead of the built-in one. **Make these cards yours** in the Anatomy pane saves the built-in cards there as a starting point. Delete the file to go back.

## Security

Point First runs only code published in this repository and can connect to nothing but its own address; the browser enforces both. See [SECURITY.md](SECURITY.md) for what it can and cannot reach, and how to report a problem.

## Page-view count

Each time the page opens, it tells [GoatCounter](https://www.goatcounter.com), a cookie-free counting service, that it was opened. It sends the page address (never anything after `#`), the site you came from, the page title and your screen size. Nothing you write, nothing about your folder and none of your settings is sent, and nothing is stored on your device to recognise you. GoatCounter receives your IP address and browser name with the request, as every website does; it says it holds them only in memory, for up to 8 hours, to tell one visit from the next, and never writes them to disk.

The count does not run on your own computer's addresses or when the file is opened from disk, and you can switch it off in any browser by opening the page once with `#toggle-goatcounter` at the end of its address. The counter is GoatCounter's published `count.v5.js` (ISC licence), kept unchanged inside `index.html`; `tools/check.py` confirms it still matches the published file.

## Host your own copy

Fork this repository and turn on GitHub Pages, or serve the files from any static host. If you host it elsewhere, change the address in the page's `canonical`, `og:url` and `og:image` tags, and in `robots.txt` and `sitemap.xml`. If you change the inline script in `index.html`, run `python3 tools/csp.py index.html` to refresh the security policy, or the browser will refuse to run it. The `index.html` file also works on its own, opened from disk in Chrome or Edge. Change or remove the `data-goatcounter` address in `index.html` and in its security policy, or your visitors are counted on mine.

Before releasing a change, run `python3 tools/tests/run_all.py`. It drives the real page in a headless browser against a simulated folder that can be edited, renamed, deleted, taken offline or made to refuse writes, and checks that nothing written is lost or overwritten, that the app never gets stuck, and that writing stays smooth.

## The deal

I built Point First for my own writing and share it as is. There is no support, no roadmap and no promise of anything. Keep your folder backed up. Issues and suggestions may be read, and may not be answered.

I write at [jonathandutoit.com](https://jonathandutoit.com).

## Licence and credits

**The code** is MIT licensed; see [LICENSE](LICENSE).

**The word lists** in the release pack keep their own terms:

- WordNet 3.0 is © Princeton University, under the WordNet licence reproduced in the pack's `ABOUT.md`.
- Moby Thesaurus II, by Grady Ward, is in the public domain.
- `frequency.txt` is derived from wordfreq by Robyn Speer and is licensed CC BY-SA 4.0.
- `concreteness.txt` holds the concreteness ratings of Brysbaert, Warriner and Kuperman (2014).
- `nominalizations.txt` is built from WordNet's derivational links.

**The Anatomy** distils principles from Joseph M. Williams (*Style: Lessons in Clarity and Grace*), George D. Gopen (*Expectations*), M. A. K. Halliday (*An Introduction to Functional Grammar*), Stanley Fish (*Is There a Text in This Class?*), Gerald Graff and Cathy Birkenstein (*They Say, I Say*) and S. I. Hayakawa (*Language in Thought and Action*), written in my own words. I first met many of them through the Writer Science YouTube channel, which brings these books together.
