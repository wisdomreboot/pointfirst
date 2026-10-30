#!/usr/bin/env python3
"""Point First's behaviour tests: files, folders, tabs, rooms and writing.

Each suite drives the real index.html in headless Chromium against a simulated folder
(fsmock.js) that can be edited, renamed, deleted, taken offline or made to refuse writes,
the way Obsidian, a sync app or a second tab can. They check that nothing you write is
ever lost or overwritten, that Point First never gets stuck, and that writing stays smooth.

    pip install playwright && python3 -m playwright install chromium
    python3 tools/tests/run_all.py            # every suite
    python3 tools/tests/run_all.py s_files    # one suite

Exit code 0 means every check passed. Run it before every release.
"""
import functools, http.server, os, socket, socketserver, subprocess, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
SUITES = ['s_files', 's_tabs', 's_tabs2', 's_more', 's_ui', 's_write', 's_upgrade', 's_hist', 's_tables', 's_revise', 's_runway', 's_skim', 's_rhythm', 's_marks']

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
socketserver.ThreadingTCPServer.allow_reuse_address = True
httpd = socketserver.ThreadingTCPServer(('127.0.0.1', port), functools.partial(Quiet, directory=SITE))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
env = dict(os.environ, PF_URL='http://localhost:%d/index.html' % port)

failed = []
for name in (sys.argv[1:] or SUITES):
    r = subprocess.run([sys.executable, os.path.join(HERE, name + '.py')], env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    passed = out.count('\nPASS') + out.startswith('PASS')
    bad = [l for l in out.splitlines() if l.startswith('FAIL') or 'Traceback' in l]
    print('%-10s %3d passed%s' % (name, passed, ('   FAILED: ' + '; '.join(bad[:3])) if bad else ''))
    if bad: failed.append(name)
httpd.shutdown()
print('\nAll suites passed.' if not failed else '\nFailed: ' + ', '.join(failed))
sys.exit(1 if failed else 0)
