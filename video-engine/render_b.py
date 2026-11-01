import asyncio, os, subprocess, json, sys, pathlib
PAGE=sys.argv[1]; OUT=sys.argv[2]
from playwright.async_api import async_playwright
FPS=30
URL=pathlib.Path(PAGE).resolve().as_uri()
# WebGL برمجي في Chromium بلا واجهة (للحلقات ثلاثية الأبعاد)، وiframe محلي يحمل التطبيق
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def scene(b, i, start, dur):
    pg=await b.new_page(viewport={'width':1920,'height':1080})
    await pg.goto(URL); await pg.wait_for_function('window.READY===true',timeout=120000)
    tmp=OUT+f'/s{i}.tmp.mp4'
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
    n=int(round(dur*FPS))
    for f in range(n):
        await pg.evaluate(f'draw({start+f/FPS})')
        ff.stdin.write(await pg.screenshot(type='jpeg',quality=92))
    ff.stdin.close(); rc=ff.wait()
    if rc==0: os.replace(tmp,OUT+f'/s{i}.mp4')
    await pg.close(); print('scene',i,'rc',rc,flush=True)
async def main():
    os.makedirs(OUT,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS)
        pg=await b.new_page(); await pg.goto(URL); await pg.wait_for_function('window.READY===true',timeout=120000)
        meta=json.loads(await pg.evaluate('JSON.stringify(META)')); await pg.close()
        sem=asyncio.Semaphore(4)
        async def run(i):
            async with sem: await scene(b,i,meta['START'][i],meta['DUR'][i])
        await asyncio.gather(*[run(i) for i in range(len(meta['DUR']))])
        await b.close()
asyncio.run(main())
