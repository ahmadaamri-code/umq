exec(open('audio.py').read().split('# --- pad')[0].replace('T=87.0','T=111.0'))
C4,D4,E4,F4,G4,A4,B4=261.63,293.66,329.63,349.23,392.0,440.0,493.88
chords=[(0,8,[130.81,196.0,329.63]),(8,26,[146.83,220.0,349.23]),(26,38,[110.0,164.81,261.63]),(38,57,[130.81,196.0,329.63]),(57,81,[116.54,174.61,293.66]),(81,102,[146.83,220.0,349.23]),(102,111,[130.81,196.0,329.63])]
for a,b,fs in chords:
    n=int((b-a)*SR); tt=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*tt+0.3*k)*(1+0.15*np.sin(2*np.pi*0.2*tt+k)) for k,f in enumerate(fs))/len(fs)
    add(a,s*env(n,1.2,1.2)*0.035)
# q1
sweep(0.6,1.8,220,880,0.08)
for i in range(14): pop(2+i*0.12,0.06)
chime(4.6,[E4*2,G4*2],0.07); chime(5.4,[C4*2,E4*2,G4*2],0.06)
# q2 (8): P moves -> soft sweeps following y; off-line buzz; back chime; conclusion chime
sweep(8.6,10.8,392,523,0.05,'sine'); sweep(10.8,13,523,262,0.05,'sine'); sweep(13,15,262,330,0.05,'sine'); sweep(15,16.4,330,392,0.04,'sine')
buzz(17.6,0.05); chime(22.6,[E4*2,G4*2],0.08); chime(23.4,[C4*2,E4*2,G4*2,C4*4],0.08)
# q3 (26)
bell(26.5,G4,0.07); tick(28.3); bell(29,A4,0.07); chime(32.3,[C4*2,E4*2,G4*2],0.09); bell(35.3,E4*2,0.05)
# q4 (38)
bell(38.6,G4,0.06); chime(39.9,[C4*2,G4*2],0.07); pop(41.3)
for k in range(3): tick(42.4+k*1.1); sweep(42.9+k*1.1,43.4+k*1.1,330*(1.2**k),400*(1.2**k),0.05,'sine')
whoosh(46.9,1.4,0.03); whoosh(48.4,1.2,0.03); whoosh(50.2,0.9,0.03)
sweep(50.9,51.6,300,520,0.04,'sine'); sweep(52.4,53.1,520,250,0.04,'sine'); sweep(53.8,54.4,330,330.1,0.04,'sine')
# q5 (57)
pop(57.8); pop(58.2); sweep(59.4,60.2,500,300,0.05,'sine'); bell(60.2,G4,0.06); bell(62.2,A4,0.06); chime(65,[D4*2,F4*2,A4*2],0.09)
whoosh(68,1.4,0.03); chime(69.2,[A4,D4*2],0.08); bell(70.6,F4*2,0.05)
whoosh(72.6,1.4,0.03); chime(73.8,[F4,A4],0.08); bell(75,D4*2,0.06)
sweep(75.6,79.4,180,150,0.03,'sine')
# q6 (81)
sweep(81.5,83.4,262,392,0.05,'sine'); pop(83.4)
sweep(84.2,89.4,200,600,0.035,'sine'); chime(90,[C4*2,E4*2,G4*2],0.09); bell(91.2,G4*2,0.05)
sweep(93,95.4,600,200,0.03,'sine'); chime(95.6,[D4*2,A4*2],0.08); chime(96.6,[F4*2,A4*2,D4*4],0.08); bell(98,A4,0.06); chime(99.2,[D4*2,F4*2,A4*2,D4*4],0.08)
# q7 (102)
pop(102.6); pop(103.6); chime(104.8,[C4*2,G4*2],0.07); chime(106,[C4,E4,G4,C4*2,E4*2],0.08,0.12)
out*=np.minimum(1,np.minimum(np.arange(N)/(0.3*SR),(N-np.arange(N))/(1.5*SR)))
out=np.tanh(out*1.6)/np.tanh(1.6)*0.85
st=np.stack([out,out],1); pcm=(st*32767).astype(np.int16)
with wave.open('audio2.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('peak',np.abs(out).max())
