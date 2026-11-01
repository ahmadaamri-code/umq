# لقطات ثابتة من جولة «العجلة الدوّارة» للفحص قبل الإخراج
# python stills_ferris.py <outdir> T1 T2 ...   (T بالثواني من بداية الجولة)
import asyncio, os, sys, json
from playwright.async_api import async_playwright
APP=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','apps','ep-trig-ferris','index.html'))
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def main():
    out=sys.argv[1]; ts=[float(x) for x in sys.argv[2:]]; os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS)
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('console',lambda m: print('console:',m.text) if m.type in ('error','warning','assert') else None)
        pg.on('pageerror',lambda e: print('pageerror:',e))
        await pg.goto('file:///'+APP.replace('\\','/')+'?video=1'); await pg.wait_for_function('window.READY===true',timeout=60000)
        print('verify',await pg.evaluate('JSON.stringify(TOUR_INFO)'))
        print('audit',await pg.evaluate('JSON.stringify(audit())'))
        print('checkAll',await pg.evaluate('JSON.stringify(checkAll(0.05))'))
        for T in ts:
            d=await pg.evaluate(f'JSON.stringify(renderAt({T}))'); await pg.wait_for_timeout(60)
            fn=os.path.join(out,f'T{T:06.1f}.png'); await pg.screenshot(path=fn)
            print(fn,d,flush=True)
        await b.close()
asyncio.run(main())
