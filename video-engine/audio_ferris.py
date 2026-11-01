# صوت حلقة «العجلة الدوّارة» مولَّد بالكود على الخط الزمني نفسه للفيديو.
# يقرأ META وTIMELINE (ارتفاع الراكب كل 0.01 s، والتشغيل، ولحظات النقر والكشف) من صفحة الفيديو نفسها.
# python audio_ferris.py ep-trig-ferris.html out.wav
import asyncio, sys, pathlib, json, wave
import numpy as np
from playwright.async_api import async_playwright
SR=44100
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def fetch(page):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS); pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto(pathlib.Path(page).resolve().as_uri()); await pg.wait_for_function('window.READY===true',timeout=120000)
        meta=json.loads(await pg.evaluate('JSON.stringify(META)')); tl=json.loads(await pg.evaluate('JSON.stringify(TIMELINE)'))
        await b.close(); return meta,tl
def bell(f,d,vol):
    t=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*5))*np.exp(-t*2.2)*vol
def pad(fs,d,vol):
    t=np.arange(int(d*SR))/SR; s=sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs); e=np.minimum(1,np.minimum(t/0.8,(d-t)/0.8)); return s*e*vol
def place(buf,t,sig): i=int(t*SR); j=min(len(buf),i+len(sig)); buf[i:j]+=sig[:j-i]
def sting(d,notes,start=0.6):  # كما في audio_b.py: مقدمة وخاتمة الهوية
    b=np.zeros(int(d*SR)); place(b,0,pad([130.81,196,329.63,392],d,0.05))
    t=np.arange(int(0.9*SR))/SR; sw=np.sin(2*np.pi*np.cumsum(220*(4**(t/0.9)))/SR)*np.sin(np.pi*t/0.9)**2*0.05; place(b,start,sw)
    for k,f in enumerate(notes): place(b,start+0.9+k*0.13,bell(f,2.2,0.09))
    return b
def click(vol=0.10):
    t=np.arange(int(0.05*SR))/SR; rng=np.random.default_rng(3)
    return (np.sin(2*np.pi*1650*t)*np.exp(-t*140)+rng.standard_normal(len(t))*np.exp(-t*300)*0.25)*vol
def main():
    page,out=sys.argv[1],sys.argv[2]
    meta,tl=asyncio.run(fetch(page))
    total=meta['TOTAL']; c0=meta['CORE0']; L=meta['TOUR_LEN']; dur0=meta['DUR'][0]; durE=meta['DUR'][-1]
    x=np.zeros(int(total*SR)+SR)
    place(x,0,sting(dur0,[523.25,659.25,783.99,1046.5]))
    # خلفية هادئة طوال المشاهد
    n=int(L*SR); t=np.arange(n)/SR
    bg=sum(np.sin(2*np.pi*f*t) for f in (130.81,164.81,196.0,246.94))/4*0.028*(1+0.25*np.sin(2*np.pi*t/9))
    bg*=np.minimum(1,np.minimum(t/1.5,(L-t)/1.5)); place(x,c0,bg)
    # نغمة الراكب: ترتفع وتنخفض مع h(t)
    h=np.array(tl['h']); pl=np.array(tl['playing'],float); ts=np.arange(len(h))/100.0
    hs=np.interp(t,ts,h); ps=np.interp(t,ts,pl)
    k=int(0.25*SR); cs=np.concatenate([[0],np.cumsum(ps)])                         # تشغيل/إيقاف ناعم: متوسط متحرك بالمجموع التراكمي
    i=np.arange(n); lo=np.clip(i-k//2,0,n); hi=np.clip(i+k//2,0,n); env=(cs[hi]-cs[lo])/np.maximum(1,hi-lo)
    f=196.0*2**(np.clip(hs,0,62)/24.0)                                            # h = 0 → 196 Hz، h = 42 → ≈ 657 Hz
    ph=2*np.pi*np.cumsum(f)/SR
    tone=(np.sin(ph)+0.22*np.sin(2*ph)+0.08*np.sin(3*ph))*0.055*env*(196/f)**0.35
    tone*=np.minimum(1,(L-t)/1.2).clip(0,1); place(x,c0,tone)
    for tc in tl['clicks']: place(x,c0+tc,click())
    if tl['reveal']>=0:
        for i,fq in enumerate([659.25,783.99,1046.5]): place(x,c0+tl['reveal']+0.05+i*0.11,bell(fq,1.8,0.075))
    o=sting(durE,[392,523.25,659.25,783.99,1046.5],0.2); o*=np.minimum(1,(len(o)-np.arange(len(o)))/(1.2*SR)); place(x,c0+L,o)
    x=x[:int(total*SR)]; x=x/max(1e-9,np.max(np.abs(x)))*0.89
    pcm=(np.stack([x,x],1)*32767).astype(np.int16)
    with wave.open(out,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(out,round(len(x)/SR,2),'s; h range',float(h.min()),float(h.max()),'; f range',round(float(f.min())),round(float(f.max())),'Hz; clicks',len(tl['clicks']))
main()
