# لقطات ثابتة من صفحة فيديو تستعمل draw(T) — للفحص قبل الإخراج الكامل
# python video_stills.py <page.html> <outdir> T1 T2 ...
import asyncio, os, sys, pathlib, json
from playwright.async_api import async_playwright
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def main():
    page,out=sys.argv[1],sys.argv[2]; ts=[float(x) for x in sys.argv[3:]]; os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS); pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror',lambda e: print('pageerror:',e))
        await pg.goto(pathlib.Path(page).resolve().as_uri()); await pg.wait_for_function('window.READY===true',timeout=120000)
        print('META',await pg.evaluate('JSON.stringify(META)'))
        for T in ts:
            si=await pg.evaluate(f'draw({T})'); fn=os.path.join(out,f'V{T:06.1f}.png'); await pg.screenshot(path=fn); print(fn,'scene',si,flush=True)
        await b.close()
asyncio.run(main())
