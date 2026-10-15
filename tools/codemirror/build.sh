#!/bin/sh
# Rebuilds the CodeMirror bundle inside index.html.
# Needs Node and npm. Run from anywhere:  sh tools/codemirror/build.sh
# Steps: install the pinned packages, bundle entry.js, put the bundle into the
# first <script> of index.html (the one headed "CodeMirror 6"), refresh the CSP hashes.
set -e
here=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$here/../.." && pwd)
cd "$here"
npm install --no-audit --no-fund --silent
npx esbuild entry.js --bundle --minify --legal-comments=none --format=iife --global-name=CM --outfile=cm.min.js
python3 - "$root/index.html" "$here/cm.min.js" <<'PY'
import re, sys
page, bundle = sys.argv[1], sys.argv[2]
js = open(bundle, encoding='utf-8').read().strip()
# An HTML comment opener inside a script can confuse the HTML parser. Escape it.
js = js.replace('<!--', '<\\!--')
if '</script' in js.lower():
    sys.exit('The bundle contains </script and cannot be inlined.')
html = open(page, encoding='utf-8').read()
m = re.search(r'(<script>\n/\* CodeMirror 6,.*?\*/\n)(.*?)(\n</script>)', html, re.S)
if not m:
    sys.exit('Could not find the CodeMirror script block in ' + page)
html = html[:m.start(2)] + js + html[m.end(2):]
open(page, 'w', encoding='utf-8').write(html)
print('Bundle updated:', len(js), 'bytes')
PY
rm -f cm.min.js
python3 "$root/tools/csp.py" "$root/index.html"
