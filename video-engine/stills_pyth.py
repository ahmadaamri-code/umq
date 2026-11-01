# لقطات ثابتة من تطبيق «جهاز فيثاغورس المائي» للفحص قبل الإخراج
# python stills_pyth.py <outdir> [WxH]   — يصوّر كل ٣٠° من التدوير، وزوايا المثلث ٦٠ و٩٠ و١٢٠ عند ١٨٠°
# python stills_pyth.py <outdir> tour T1 T2 ...  — لقطات من الجولة عند أزمنة T
import asyncio, os, sys, json, pathlib
from playwright.async_api import async_playwright
APP=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','apps','ep-pythagoras','index.html'))
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def main():
    out=sys.argv[1]; os.makedirs(out,exist_ok=True); rest=sys.argv[2:]
    vw,vh=1920,1080
    if rest and 'x' in rest[0]: vw,vh=map(int,rest[0].split('x')); rest=rest[1:]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS)
        pg=await b.new_page(viewport={'width':vw,'height':vh})
        pg.on('console',lambda m: print('console:',m.text) if m.type in ('error','warning','assert') else None)
        pg.on('pageerror',lambda e: print('pageerror:',e))
        await pg.goto(pathlib.Path(APP).as_uri()+'?video=1'); await pg.wait_for_function('window.READY===true',timeout=60000)
        print('verify',await pg.evaluate('JSON.stringify(TOUR_INFO.verify)'))
        print('checkGrid',await pg.evaluate('JSON.stringify(checkGrid())'))
        print('checkAll',await pg.evaluate('JSON.stringify(checkAll(0.05))'))
        if rest and rest[0]=='tour':
            for T in map(float,rest[1:]):
                d=await pg.evaluate(f'JSON.stringify(renderAt({T}))'); await pg.wait_for_timeout(60)
                fn=os.path.join(out,f'T{T:06.1f}.png'); await pg.screenshot(path=fn); print(fn,d,flush=True)
        else:
            shots=[(r,90) for r in range(0,181,30)]+[(180,60),(180,120),(0,120),(90,120),(90,60)]
            for r,g in shots:
                d=await pg.evaluate(f'JSON.stringify(renderState({{rot:{r},g:{g}}}))'); await pg.wait_for_timeout(60)
                fn=os.path.join(out,f'r{r:03d}_g{g}.png'); await pg.screenshot(path=fn); print(fn,d,flush=True)
        await b.close()
asyncio.run(main())
