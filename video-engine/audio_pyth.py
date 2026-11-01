# صوت حلقة «جهاز فيثاغورس المائي» مولَّد بالكود على الخط الزمني نفسه للفيديو.
# يقرأ META وTIMELINE من صفحة الفيديو: سرعة التدفق (سم³/ث من التدوير وحده) كل 0.01 ث، ولحظات «تمام»، ولحظات النقر.
# خرير ماء ناعم: ضجيج مُرشَّح + فقاعات، كلاهما يتبع سرعة التدفق. ونغمة «تمام» عند امتلاء المربعين تماماً.
# python audio_pyth.py ep-pythagoras.html out.wav
import asyncio, sys, pathlib, json, wave
import numpy as np
from playwright.async_api import async_playwright
SR=44100
ARGS=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']
async def fetch(page):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=ARGS); pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto(pathlib.Path(page).resolve().as_uri()); await pg.wait_for_function('window.READY===true',timeout=300000)
        meta=json.loads(await pg.evaluate('JSON.stringify(META)')); tl=json.loads(await pg.evaluate('JSON.stringify(TIMELINE)'))
        await b.close(); return meta,tl
def bell(f,d,vol):
    t=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*5))*np.exp(-t*2.2)*vol
def pad(fs,d,vol):
    t=np.arange(int(d*SR))/SR; s=sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs); e=np.minimum(1,np.minimum(t/0.8,(d-t)/0.8)); return s*e*vol
def place(buf,t,sig): i=int(t*SR); j=min(len(buf),i+len(sig)); buf[i:j]+=sig[:j-i]
def sting(d,notes,start=0.6):  # مقدمة وخاتمة الهوية (كما في الحلقات السابقة)
    b=np.zeros(int(d*SR)); place(b,0,pad([130.81,196,329.63,392],d,0.05))
    t=np.arange(int(0.9*SR))/SR; sw=np.sin(2*np.pi*np.cumsum(220*(4**(t/0.9)))/SR)*np.sin(np.pi*t/0.9)**2*0.05; place(b,start,sw)
    for k,f in enumerate(notes): place(b,start+0.9+k*0.13,bell(f,2.2,0.09))
    return b
def click(vol=0.10):
    t=np.arange(int(0.05*SR))/SR; rng=np.random.default_rng(3)
    return (np.sin(2*np.pi*1650*t)*np.exp(-t*140)+rng.standard_normal(len(t))*np.exp(-t*300)*0.25)*vol
def onepole(x,fc):  # مرشّح تمرير منخفض بسيط
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); s=0.0
    for i in range(len(x)): s=a*s+(1-a)*x[i]; y[i]=s
    return y
def lp(x,fc):  # أسرع: مرشّح IIR متتابع بالمتجهات عبر scipy إن وُجد
    try:
        from scipy.signal import lfilter
        a=np.exp(-2*np.pi*fc/SR); return lfilter([1-a],[1,-a],x)
    except ImportError: return onepole(x,fc)
def bubble(f0,d,vol):  # فقاعة: نغمة قصيرة يرتفع ترددها بسرعة وتخمد
    t=np.arange(int(d*SR))/SR; f=f0*(1+2.2*t/d); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*(6/d))*np.sin(np.pi*np.minimum(1,t/0.004)/2)*vol
def main():
    page,out=sys.argv[1],sys.argv[2]
    meta,tl=asyncio.run(fetch(page))
    total=meta['TOTAL']; c0=meta['CORE0']; L=meta['TOUR_LEN']; dur0=meta['DUR'][0]; durE=meta['DUR'][-1]
    x=np.zeros(int(total*SR)+SR)
    place(x,0,sting(dur0,[523.25,659.25,783.99,1046.5]))
    n=int(L*SR); t=np.arange(n)/SR
    bg=sum(np.sin(2*np.pi*f*t) for f in (130.81,164.81,196.0,246.94))/4*0.022*(1+0.25*np.sin(2*np.pi*t/9))
    bg*=np.minimum(1,np.minimum(t/1.5,(L-t)/1.5)); place(x,c0,bg)
    # شدة التدفق: سرعة انتقال الماء بين الأحواض، منعَّمة ومطبَّعة
    fl=np.array(tl['flow'],float); ts=np.arange(len(fl))/100.0
    k=25; fl=np.convolve(fl,np.ones(k)/k,mode='same')                       # تنعيم ربع ثانية
    peak=max(1e-9,np.percentile(fl[fl>1],80) if (fl>1).any() else 1)
    env=np.clip(fl/peak,0,1.3); envS=np.interp(t,ts,env)
    rng=np.random.default_rng(7)
    noise=rng.standard_normal(n)
    hiss=lp(noise,1800)-lp(noise,350)                                       # نطاق خرير الماء
    rumble=lp(noise,220)
    am=1+0.35*lp(rng.standard_normal(n),6)                                   # تموّج بطيء طبيعي
    water=(hiss*0.55+rumble*0.9)*am*np.power(envS,0.4)*0.24
    place(x,c0,water)
    # فقاعات: معدلها يتبع التدفق (حتى ~٢٢ فقاعة/ث)
    rate=22*env; tt=0.0
    while tt<L:
        r=float(np.interp(tt,ts,rate))
        if r<0.3: tt+=0.05; continue
        tt+=rng.exponential(1/r)
        if tt>=L: break
        place(x,c0+tt,bubble(rng.uniform(380,1100),rng.uniform(0.025,0.07),0.065*min(1,float(np.interp(tt,ts,env)))))
    for tc in tl['clicks']: place(x,c0+tc,click())
    # نغمة «تمام»: عند كل لحظة يصير فيها المربعان ممتلئين تماماً (حافة صاعدة)
    tm=np.array(tl['tamam']); edges=[i/100.0 for i in range(1,len(tm)) if tm[i] and not tm[i-1]]
    for te in edges:
        for i,fq in enumerate([783.99,987.77,1174.66,1567.98]): place(x,c0+te+0.04+i*0.09,bell(fq,2.0,0.08))
    o=sting(durE,[392,523.25,659.25,783.99,1046.5],0.2); o*=np.minimum(1,(len(o)-np.arange(len(o)))/(1.2*SR)); place(x,c0+L,o)
    x=x[:int(total*SR)]; x=x/max(1e-9,np.max(np.abs(x)))*0.89
    pcm=(np.stack([x,x],1)*32767).astype(np.int16)
    with wave.open(out,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(out,round(len(x)/SR,2),'s; flow peak',round(float(peak)),'cm3/s; tamam at',[round(c0+e,2) for e in edges],'; clicks',len(tl['clicks']))
main()
