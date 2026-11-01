import numpy as np, wave, sys
SR=44100
def load(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32767.0; return a
def bell(f,d,vol):
    t=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*5))*np.exp(-t*2.2)*vol
def pad(fs,d,vol):
    t=np.arange(int(d*SR))/SR; s=sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs); e=np.minimum(1,np.minimum(t/0.8,(d-t)/0.8)); return s*e*vol
def place(buf,t,sig): i=int(t*SR); j=min(len(buf),i+len(sig)); buf[i:j]+=sig[:j-i]
def sting(d,notes,start=0.6):
    b=np.zeros(int(d*SR)); place(b,0,pad([130.81,196,329.63,392],d,0.05))
    t=np.arange(int(0.9*SR))/SR; sw=np.sin(2*np.pi*np.cumsum(220*(4**(t/0.9)))/SR)*np.sin(np.pi*t/0.9)**2*0.05; place(b,start,sw)
    for k,f in enumerate(notes): place(b,start+0.9+k*0.13,bell(f,2.2,0.09))
    return b
for src,dst in [('audio.wav','audio_b1.wav'),('audio2.wav','audio_b2.wav')]:
    core=load(src)
    intro=sting(3.6,[523.25,659.25,783.99,1046.5]); outro=sting(4.5,[392,523.25,659.25,783.99,1046.5],0.2)
    outro*=np.minimum(1,(len(outro)-np.arange(len(outro)))/(1.2*SR))
    x=np.concatenate([intro,core,outro]); x=np.clip(x,-0.98,0.98)
    pcm=(np.stack([x,x],1)*32767).astype(np.int16)
    with wave.open(dst,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(dst,len(x)/SR)
