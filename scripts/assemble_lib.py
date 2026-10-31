#!/usr/bin/env python3
"""Shared assembler: illustrated bg + character circle + Thai subtitles. Silent (voice added later)."""
import subprocess, os, json, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
FPS=30; W,H=1080,1920; D=420

def avatar(src,out):
    im=Image.open(src).convert("RGB"); a=np.asarray(im).astype(int)
    bg=a[5:25,5:25].reshape(-1,3).mean(0); m=(np.abs(a-bg).sum(2)>45)
    ys,xs=np.where(m); x0,x1,y0=xs.min(),xs.max(),ys.min()
    cx=(x0+x1)//2; side=int((x1-x0)*1.25)
    # head-and-shoulders crop starting just above the head
    top=max(0,y0-int(side*0.06)); left=max(0,min(im.width-side,cx-side//2)); 
    crop=im.crop((left,top,left+side,top+side)).resize((D,D),Image.LANCZOS)
    mask=Image.new("L",(D*4,D*4),0); ImageDraw.Draw(mask).ellipse((0,0,D*4-1,D*4-1),fill=255); mask=mask.resize((D,D),Image.LANCZOS)
    ring=Image.new("RGBA",(D+24,D+24),(0,0,0,0)); d=ImageDraw.Draw(ring)
    d.ellipse((0,0,D+23,D+23),fill=(255,255,255,255)); ring.paste(crop,(12,12),mask)
    sh=Image.new("RGBA",(D+24,D+24),(0,0,0,0)); ring.save(out)

CSS="""@font-face{font-family:P;font-weight:700;src:url(../../assets/fonts/prompt-thai-700-normal.woff2)}
@font-face{font-family:P;font-weight:700;src:url(../../assets/fonts/prompt-latin-700-normal.woff2);unicode-range:U+0000-00FF}
html,body{margin:0;background:transparent}body{width:1080px;height:1920px;position:relative;font-family:P,sans-serif;font-weight:700}
.t{position:absolute;left:60px;right:60px;text-align:center;color:#fff;line-height:1.35;text-shadow:0 4px 14px rgba(0,0,0,.65)}
.t span{display:inline-block;background:rgba(20,20,30,.55);padding:18px 38px;border-radius:34px}
.n .t{bottom:760px;font-size:62px}.hook .t{top:300px;font-size:88px}.quote .t{bottom:760px;font-size:68px}
.cta .t{top:760px;font-size:78px}.cta b{color:#ffd9ec}.note .t{top:300px;font-size:50px}.note .t span{background:rgba(255,255,255,.82);color:#2a2a3a;text-shadow:none}"""

def build(name, chars, T, segs, audio=None):
    """chars {key: shot}, T [(start,end,avatar|None,subtitle|None,style)], segs [(bg_path,dur,extra_vf)]"""
    B=f"build/{name}"; os.makedirs(B,exist_ok=True)
    for k,v in chars.items(): avatar(f"assets/characters/{v}.png",f"{B}/av_{k}.png")
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={"width":W,"height":H})
        for i,(s,e,av,txt,st) in enumerate(T):
            if not txt: continue
            open(f"{B}/s{i}.html","w").write(f"<style>{CSS}</style><body class='{st or 'n'}'><div class='t'><span>{txt}</span></div></body>")
            pg.goto(f"file://{ROOT}/{B}/s{i}.html"); pg.wait_for_timeout(250); pg.screenshot(path=f"{B}/s{i}.png",omit_background=True)
        br.close()
    lst=[]
    for j,(bg,dur,extra) in enumerate(segs):
        n=int(dur*FPS)
        vf=f"scale=-2:3840,crop=2160:3840,zoompan=z='1+0.09*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}{extra},format=yuv420p"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",bg,"-vf",vf,"-t",str(dur),f"{B}/seg{j}.mp4"],check=True); lst.append(f"file seg{j}.mp4")
    open(f"{B}/list.txt","w").write("\n".join(lst)+"\n")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i",f"{B}/list.txt","-c","copy",f"{B}/bg.mp4"],check=True)
    inputs=["-i",f"{B}/bg.mp4"]; flt=[]; last="0:v"; idx=1; x=(W-(D+24))//2; y=1250
    for i,(s,e,av,txt,st) in enumerate(T):
        if av:
            inputs+=["-i",f"{B}/av_{av}.png"]; flt.append(f"[{last}][{idx}:v]overlay={x}:{y}:enable='between(t,{s},{e})'[v{idx}]"); last=f"v{idx}"; idx+=1
        if txt:
            inputs+=["-i",f"{B}/s{i}.png"]; flt.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{s},{e})'[v{idx}]"); last=f"v{idx}"; idx+=1
    os.makedirs("out",exist_ok=True); tot=sum(d for _,d,_ in segs)
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(flt),"-map",f"[{last}]","-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-t",str(tot),f"out/{name}_draft_silent.mp4"],check=True)
    print("ok",f"out/{name}_draft_silent.mp4")
    if audio:
        ins=[];fl=[]
        for i,(f,st) in enumerate(audio):
            ins+=["-i",f]; ms=int(st*1000); fl.append(f"[{i+1}:a]adelay={ms}|{ms},volume=1.0[a{i}]")
        mix="".join(f"[a{i}]" for i in range(len(audio)))+f"amix=inputs={len(audio)}:normalize=0:duration=longest,apad,atrim=0:{tot}[aout]"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"out/{name}_draft_silent.mp4",*ins,"-filter_complex",";".join(fl)+";"+mix,"-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","160k","-shortest",f"out/{name}_draft_voice.mp4"],check=True)
        print("ok",f"out/{name}_draft_voice.mp4")
