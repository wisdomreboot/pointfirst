# Security

## What Point First can reach

- **Your folder.** Only the one you pick, and only while Point First is open in a tab. You can revoke it at any time in the browser's site settings. The folder is not on the internet: there is no address anyone can connect to.
- **Browser storage** for this one address holds settings and the link to your folder. No other website can read it.
- **Nothing leaves your computer.** The page's security policy allows connections only to Point First's own address, and the browser enforces that, not the app. Word lists are files you add; Point First never fetches them. The only outside request is for the page's fonts.

## What protects it

- **Only this repository's code runs.** The Content-Security-Policy lets the browser run scripts from this site and the one inline script whose fingerprint it lists, and nothing else.
- **Files from the folder are treated as untrusted.** Essays, starter files, word lists and Point First's own records are escaped before display and checked before use. Links in Publish keep only web, mail and in-page addresses. A word-list zip is refused if it would unpack to more than any list needs.

## What it can't protect

- **Your device.** Your essays are plain Markdown files, as safe as your computer. Use a login password and disk encryption (FileVault on a Mac, BitLocker on Windows).
- **Browser extensions** with permission to read every site can read Point First too. Install few.

## For the owner of a copy

Whoever controls the repository controls the code every user runs. Turn on two-factor sign-in for GitHub, for the DNS provider that points the address at GitHub, and for the domain registrar. Don't merge a pull request you haven't read line by line. After editing the inline script in `index.html`, run `python3 tools/csp.py index.html` to refresh its fingerprint.

## Reporting a problem

Use GitHub's private vulnerability reporting on this repository (the **Security** tab, **Report a vulnerability**). Please don't open a public issue for a security problem. This is a personal project with no support promise, but security reports will be read.
