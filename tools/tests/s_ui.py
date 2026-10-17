import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from h2 import go, check, ESSAY

OPEN_THINGS = "JSON.stringify({pal:!$('#pal').hidden,keys:!$('#keys').hidden,hist:!$('#hist').hidden,pub:!$('#pub').hidden,find:!$('#findbar').hidden,lens:!$('#lensMenu').hidden,smenu:!$('#smenu').hidden,files:!$('#files').hidden,qpop:!$('#qpop').hidden})"

async def suite(c):
    a = await c.tab()
    await a.fs('write', 'alpha.md', ESSAY('Alpha', 'Alpha body. It is very important to note this.\n\n- one\n- two', 'aaaa11'))
    await a.fs('write', 'beta.md', ESSAY('Beta', 'Beta body.', 'bbbb22'))
    await a.connect(); await a.open('Alpha')
    kb = a.pg.keyboard
    async def nothing_open(label):
        st = await a.ev(OPEN_THINGS)
        check(label, '"true"' not in st and 'true' not in st, st)

    # every overlay closes with Escape
    for name, opener in [('palette', "openPal('cmd')"), ('shortcuts', 'openKeys()'), ('history', 'openHistory()'),
                         ('publish', 'openPublish()'), ('find', 'openFind()'), ('files', 'openFiles()')]:
        await a.ev("setRoom('revise')"); await a.wait(200)
        await a.ev(opener); await a.wait(500)
        await kb.press('Escape'); await a.wait(250)
        await nothing_open(f'U1 Escape closes {name}')

    # menus close with Escape and with a click elsewhere
    await a.ev("setRoom('revise')"); await a.wait(200)
    await a.ev("$('#lensBtn').click()"); await a.wait(150); await kb.press('Escape'); await a.wait(150)
    await nothing_open('U2 Escape closes the lens menu')
    await a.ev("$('#docid').click()"); await a.wait(200); await kb.press('Escape'); await a.wait(150)
    await nothing_open('U2 Escape closes the stage menu')
    await a.ev("$('#docid').click()"); await a.wait(200); await a.pg.mouse.click(600, 600); await a.wait(200)
    await nothing_open('U2 a click elsewhere closes the stage menu')

    # switching rooms with something open never leaves a panel floating over the wrong room
    for name, opener in [('find', 'openFind()'), ('palette', "openPal('cmd')"), ('shortcuts', 'openKeys()'), ('history', 'openHistory()')]:
        await a.ev("setRoom('revise')"); await a.wait(200); await a.ev(opener); await a.wait(400)
        await kb.press('Alt+1'); await a.wait(600)
        st = await a.ev(OPEN_THINGS)
        check(f'U3 Alt+1 with {name} open lands in a clean Library', await a.ev('room') == 'library' and 'true' not in st, st)
        await kb.press('Escape'); await a.wait(150)

    # rooms always come back to a working page
    await a.open('Alpha')
    for k in ['Alt+3', 'Alt+2', 'Alt+1', 'Alt+2']:
        await kb.press(k); await a.wait(500)
    check('U4 after hopping rooms, Write has the page focused', await a.ev('room') == 'write' and await a.ev('editor.hasFocus'), await a.ev('room'))
    await kb.type(' still typing'); await a.wait(200)
    check('U4 and typing lands in the essay', (await a.ev('editor.value')).endswith('still typing'), (await a.ev('editor.value'))[-40:])

    # input methods: Enter that commits a composition is not a list Enter, a title Enter or a Library Enter
    v0 = await a.ev("editor.value")
    await a.ev("(()=>{const v=editor.value,i=v.indexOf('- two')+5;editor.focus();editor.setSelectionRange(i,i)})()")
    await a.ev("""(()=>{const t=document.querySelector('#editor .cm-content');t.dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true,data:''}));t.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:229,isComposing:true,bubbles:true,cancelable:true}));t.dispatchEvent(new CompositionEvent('compositionend',{bubbles:true,data:''}))})()""")
    await a.wait(150)
    check('U5 composing Enter in a list does not start a new item', '- two\n- ' not in await a.ev("editor.value"), (await a.ev("editor.value"))[-30:])
    await a.ev("doctitle.focus()")
    await a.ev("""doctitle.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:229,isComposing:true,bubbles:true,cancelable:true}))""")
    check('U5 composing Enter in the title stays in the title', await a.ev("document.activeElement===doctitle"), await a.ev("document.activeElement.id"))
    await a.ev("setRoom('library')"); await a.wait(500); await a.ev("$('#libFind').focus();$('#libFind').value='bet';libQ='bet';paintLibrary()"); await a.wait(200)
    await a.ev("""$('#libFind').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:229,isComposing:true,bubbles:true,cancelable:true}))"""); await a.wait(500)
    check('U5 composing Enter in Find an essay does not open one', await a.ev('room') == 'library', await a.ev('room'))
    await a.ev("$('#libFind').value='';libQ='';paintLibrary()")

    # the Library's own keys never fire while typing in its search box
    await a.ev("$('#libFind').focus()"); await kb.type('n'); await a.wait(400)
    check('U6 typing n in Find an essay types n', await a.ev("room") == 'library' and await a.ev("$('#libFind').value") == 'n', await a.ev("$('#libFind').value"))

go(suite)
