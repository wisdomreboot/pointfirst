# Point First

**A writing desk that coaches and never writes for you.**

Open it at **https://pointfirst.jonathandutoit.com**

## What it is

Point First is one HTML file for writing essays in your own voice. It reads and saves plain Markdown files in a folder you choose, such as your essays folder in Obsidian, and coaches while you write. It never generates, rewrites or suggests prose. It asks. The writer writes.

Everything runs in your browser. There is no server, no account and no tracking. Point First works only in a folder you connect: your essays, their history, Point First's own records and its word lists all live there, so clearing the browser loses nothing. It needs a browser that can open a folder: Chrome or Edge on a computer.

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

- **Ownership tracking:** every character is tagged as typed or pasted, and a meter shows how much of the draft is yours.
- **Find and Replace,** with a map of matches.
- **Version history,** kept before anything replaces text.
- **Publish** as Markdown or HTML.

## Word lists

Words, the zombie-noun check, the rare-word check and the concreteness gauge read word lists from your folder. Point First never fetches them. To add them:

1. Download [pointfirst-word-lists.zip](https://github.com/wisdomreboot/pointfirst/releases/latest/download/pointfirst-word-lists.zip) from the latest release (about 15 MB).
2. In Point First, open the Words tab, choose **Add word lists**, and pick the zip.

Point First copies the data lists into `.pointfirst/word-lists` and three editable starter files (lexicon, Anatomy, Plan) to the top level of your folder. Where each list comes from is described in `ABOUT.md` inside the pack.

## Make it yours

The Anatomy cards, the Plan checklist and the lexicon are plain Markdown files. Keep your own `pointfirst-anatomy.md`, `pointfirst-plan.md` or `pointfirst-lexicon.md` at the top level of your folder and Point First uses yours instead of the built-in one. **Make these cards yours** in the Anatomy pane saves the built-in cards there as a starting point. Delete the file to go back.

## Security

Point First runs only code published in this repository and can connect to nothing but its own address; the browser enforces both. See [SECURITY.md](SECURITY.md) for what it can and cannot reach, and how to report a problem.

## Host your own copy

Fork this repository and turn on GitHub Pages, or serve the files from any static host. If you host it elsewhere, change the address in the page's `canonical`, `og:url` and `og:image` tags, and in `robots.txt` and `sitemap.xml`. If you change the inline script in `index.html`, run `python3 tools/csp.py index.html` to refresh the security policy, or the browser will refuse to run it. The `index.html` file also works on its own, opened from disk in Chrome or Edge.

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
