import numpy as np, wave
SR=44100; T=87.0; N=int(SR*T); out=np.zeros(N)
def env(n,a,r):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR))
    e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr); return e
def add(t,sig):
    i=int(t*SR); j=min(N,i+len(sig)); out[i:j]+=sig[:j-i]
def tone(t,f,d,vol=0.12,a=0.01,r=None,kind='sine'):
    n=int(d*SR); tt=np.arange(n)/SR; ph=2*np.pi*f*tt
    s=np.sin(ph) if kind=='sine' else (2/np.pi)*np.arcsin(np.sin(ph))
    add(t,s*env(n,a,r if r else d*0.6)*vol)
def bell(t,f,vol=0.12,d=1.4):
    n=int(d*SR); tt=np.arange(n)/SR
    s=(np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*6))*np.exp(-tt*3.2)
    add(t,s*vol*env(n,0.005,0.05))
def chime(t,notes,vol=0.10,gap=0.09):
    for k,f in enumerate(notes): bell(t+k*gap,f,vol)
def sweep(t0,t1,f0,f1,vol=0.10,kind='tri'):
    n=int((t1-t0)*SR); tt=np.linspace(0,1,n); f=f0*(f1/f0)**tt; ph=2*np.pi*np.cumsum(f)/SR
    s=(2/np.pi)*np.arcsin(np.sin(ph)) if kind=='tri' else np.sin(ph)
    add(t0,s*env(n,0.05,0.12)*vol)
def pop(t,vol=0.12):
    n=int(0.09*SR); tt=np.arange(n)/SR; f=900*np.exp(-tt*18)+380; ph=2*np.pi*np.cumsum(f)/SR
    add(t,np.sin(ph)*np.exp(-tt*35)*vol)
def tick(t,vol=0.06):
    n=int(0.03*SR); add(t,np.random.randn(n)*np.exp(-np.arange(n)/SR*180)*vol)
def whoosh(t,d,vol=0.05):
    n=int(d*SR); x=np.random.randn(n); 
    k=np.ones(40)/40; x=np.convolve(x,k,'same'); add(t,x*np.sin(np.linspace(0,np.pi,n))**2*vol*3)
def buzz(t,vol=0.07):
    n=int(0.32*SR); tt=np.arange(n)/SR; s=np.sign(np.sin(2*np.pi*150*tt))*0.5+np.sin(2*np.pi*150*tt)*0.5
    s=np.convolve(s,np.ones(12)/12,'same'); add(t,s*env(n,0.01,0.1)*vol); add(t+0.36,s*env(n,0.01,0.1)*vol*0.8)
def thud(t,vol=0.18):
    n=int(0.35*SR); tt=np.arange(n)/SR; f=110*np.exp(-tt*5)+45; add(t,np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)*vol)
# --- pad (soft chords per scene) ---
C4,D4,E4,F4,G4,A4,B4=261.63,293.66,329.63,349.23,392.0,440.0,493.88
chords=[(0,9,[130.81,196.0,329.63]),(9,24,[146.83,220.0,349.23]),(24,37,[130.81,196.0,329.63]),(37,53,[110.0,164.81,261.63]),(53,65,[146.83,220.0,349.23]),(65,79,[116.54,174.61,293.66]),(79,87,[130.81,196.0,329.63])]
for a,b,fs in chords:
    n=int((b-a)*SR); tt=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*tt+0.3*k)*(1+0.15*np.sin(2*np.pi*0.2*tt+k)) for k,f in enumerate(fs))/len(fs)
    add(a,s*env(n,1.2,1.2)*0.035)
# --- events ---
pop(0.3); sweep(3.8,7.6,130,150,0.025,'sine'); chime(5.7,[C4*2,E4*2]); chime(6.9,[G4,C4*2,E4*2],0.08)
pop(10.5); pop(11.3); sweep(12.0,13.6,220,880,0.10); tick(14.0); sweep(14.0,15.2,300,300*1.06,0.03,'sine'); tick(16.0); sweep(16.0,17.2,330,500,0.04,'sine')
for t,f in [(18.0,E4*2),(19.4,F4*2),(20.8,G4*2)]: bell(t,f,0.07)
chime(22.2,[C4*2,E4*2,G4*2,C4*4],0.09)
for t in [24+2,24+5.4,24+8.6]: whoosh(t,1.6,0.035)
chime(24+10.3,[G4*2,C4*4],0.08)
sweep(37.8,40.0,262,523,0.10); sweep(41.2,43.0,523,262,0.10); sweep(43.8,45.4,392,392.01,0.08)
for t,f in [(46.2,440),(47.4,523.25),(48.6,659.25),(49.8,880)]: tone(t,f,0.5,0.10,0.01,0.35,'tri')
thud(51.0); thud(51.95,0.12)
pop(53.8); pop(54.0); pop(54.6); pop(55.8); buzz(57.6); chime(59.2,[E4*2,G4*2]); chime(61.8,[C4*2,E4*2,G4*2],0.09)
whoosh(67.0,1.6,0.04); chime(68.8,[A4,A4*1.5],0.08); sweep(71.0,73.4,330,494,0.06,'sine'); chime(74.6,[D4*2,F4*2,A4*2],0.09); bell(75.6,D4*4,0.06)
pop(79.6); 
for k in range(4): pop(80.4+k*0.25,0.08)
pop(81.8); pop(82.2); chime(84.6,[C4,E4,G4,C4*2,E4*2],0.08,0.12)
# master fade & limit
out*=np.minimum(1,np.minimum(np.arange(N)/(0.3*SR),(N-np.arange(N))/(1.5*SR)))
out=np.tanh(out*1.6)/np.tanh(1.6)*0.85
st=np.stack([out,out],1); pcm=(st*32767).astype(np.int16)
with wave.open('audio.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('peak',np.abs(out).max())
