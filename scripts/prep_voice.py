#!/usr/bin/env python3
"""Map raw AI Studio downloads (time-ordered) to named lines, trim silence, write assets/voice/*.wav + durations.json"""
import wave, json, os, numpy as np, re, glob
RAW="assets/voice/raw"; OUT="assets/voice"
def key(f):
    m=re.match(r'(\d+)_(\d+)PM(?:_(\d+))?\.wav',os.path.basename(f)); return (int(m[1]),int(m[2]),int(m[3] or 0))
files=sorted(glob.glob(f"{RAW}/*.wav"),key=key)
names=[None,"K2_shh","K2_yai_thinee","K2_rule","K2_soft","K2_fine","K2_cta","K3_card","K3_unlimited","K3_cheaper","K3_cta"]  # first file = Veda test, discarded
assert len(files)==len(names),(len(files),len(names))
dur={}
for f,n in zip(files,names):
    if not n: continue
    w=wave.open(f); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768; w.close()
    win=int(sr*0.02); r=np.sqrt(np.convolve(x*x,np.ones(win)/win,'same')); act=np.where(r>0.01)[0]
    a=max(0,act[0]-int(sr*0.08)); b=min(len(x),act[-1]+int(sr*0.15)); y=(x[a:b]*32767).astype(np.int16)
    o=wave.open(f"{OUT}/{n}.wav","wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
    dur[n]=round(len(y)/sr,2); print(n,round(len(x)/sr,2),"->",dur[n])
json.dump(dur,open(f"{OUT}/durations.json","w"),indent=1)
