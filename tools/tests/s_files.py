import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'First essay body.', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Second essay body.', 'bbbb22'))
    await a.fs('write', 'notes/gamma.md', '# Gamma\n\nWritten in Obsidian, never saved by Point First.\n')
    await a.connect()

    # S1 boot into the Library lists the essays
    await a.lib(); await a.reload()
    rows = await a.rows()
    check('S1 reload into Library lists essays', len(rows) == 3, rows)

    # S2 typing saves to the file
    await a.open('Alpha'); await a.type(' Typed here.'); await a.settle()
    check('S2 typing reaches the file', 'Typed here.' in (await a.read('alpha.md') or ''), await a.read('alpha.md'))

    # S3 edited outside, nothing unsaved here, writer comes back: page shows the disk text
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Rewritten in Obsidian.', 'aaaa11'))
    await a.focus_back()
    check('S3 outside edit loads when you come back', 'Rewritten in Obsidian.' in await a.ev('editor.value'), await a.ev('editor.value'))

    # S4 edited outside while unsaved typing here: nothing overwritten, both kept
    await a.ev("loadDiskVersion()"); await a.wait(500)
    await a.type(' Mine A.')
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Theirs B.', 'aaaa11'))
    await a.settle()
    disk = await a.read('alpha.md')
    check('S4 outside edit is never overwritten silently', 'Theirs B.' in disk and 'Mine A.' not in disk, disk)
    check('S4 conflict is shown', 'changed on disk' in await a.info(), await a.info())
    await a.ev("document.querySelector('#fiKeep').click()"); await a.wait(800)
    disk = await a.read('alpha.md')
    hist = [p for p in await a.fs('list') if p.startswith('.pointfirst/history/')]
    texts = [await a.read(p) for p in hist]
    check('S4 overwrite keeps mine on disk', 'Mine A.' in disk, disk)
    check('S4 overwrite keeps theirs in History', any('Theirs B.' in (t or '') for t in texts), hist)

    # S5 a sync client touches the timestamp only: no false conflict
    await a.fs('touch', 'alpha.md'); await a.type(' After touch.'); await a.settle()
    check('S5 timestamp-only change is not a conflict', 'After touch.' in (await a.read('alpha.md') or ''), await a.info())
    if 'changed on disk' in await a.info(): await a.ev("document.querySelector('#fiKeep').click()"); await a.wait(600)

    # S6 renamed or moved in Obsidian while open: follows it, no duplicate
    await a.fs('mv', 'alpha.md', 'archive/Alpha renamed.md')
    await a.type(' After move.'); await a.settle()
    files = await a.fs('list')
    moved = await a.read('archive/Alpha renamed.md') or ''
    check('S6 move: writing follows the essay', 'After move.' in moved, files)
    check('S6 move: no duplicate left behind', 'alpha.md' not in files and not any(f.startswith('Alpha') for f in files), files)

    # S7 deleted outside while open: not brought back on its own, text not lost
    await a.open('Beta'); await a.type(' Beta words.'); await a.settle()
    await a.fs('del', 'beta.md')
    await a.type(' Typed after delete.'); await a.settle()
    await a.open('Gamma')
    files = await a.fs('list')
    check('S7 deleted essay is not recreated without asking', not any('Beta' in f or f == 'beta.md' for f in files if not f.startswith('.')), files)
    hist_texts = [await a.read(p) for p in files if p.startswith('.pointfirst/history/')]
    check('S7 text typed after the delete is kept in History', any('Typed after delete.' in (t or '') for t in hist_texts), [p for p in files if 'history' in p])

    # S8 permission lost while writing: text kept, reconnect saves it
    await a.open('Gamma'); await a.fs('__setperm', 'prompt') if False else None
    await a.ev("__fs.perm='prompt'"); await a.type(' Words while paused.'); await a.settle()
    check('S8 paused permission shows Reconnect', 'permission' in (await a.info()).lower(), await a.info())
    await a.ev("__fs.perm='prompt'"); await a.ev("document.querySelector('#fiReconnect')&&document.querySelector('#fiReconnect').click()"); await a.wait(400)
    await a.type(' And after.'); await a.settle()
    g = await a.read('notes/gamma.md') or ''
    check('S8 after reconnect, everything typed is saved', 'Words while paused.' in g and 'And after.' in g, g)

    # S9 writes failing (disk full, sync lock): text kept, saved once writes work
    await a.ev("__fs.failWrites=true"); await a.type(' During failure.'); await a.settle()
    await a.ev("__fs.failWrites=false"); await a.type(' Recovered.'); await a.settle()
    g = await a.read('notes/gamma.md') or ''
    check('S9 failed writes lose nothing', 'During failure.' in g and 'Recovered.' in g, g)

    # S12 reload within a second of typing: nothing lost
    await a.type(' Quick before reload.'); await a.wait(700); await a.reload(); await a.settle()
    g = await a.read('notes/gamma.md') or ''
    check('S12 reload right after typing loses nothing', 'Quick before reload.' in g, g)

    # S13 changed outside while Point First was closed: disk loads, mine kept
    await a.type(' Unsaved at close.'); await a.wait(700)
    await a.fs('write', 'notes/gamma.md', '---\n' + 'status: drafting\n---\n# Gamma\n\nChanged while closed.\n')
    await a.reload(); await a.settle()
    check('S13 page shows the disk version after reload', 'Changed while closed.' in await a.ev('editor.value'), await a.ev('editor.value'))
    files = await a.fs('list')
    hist_texts = [await a.read(p) for p in files if p.startswith('.pointfirst/history/')]
    check('S13 your unsaved words are kept in History', any('Unsaved at close.' in (t or '') for t in hist_texts), '')

go(suite)
