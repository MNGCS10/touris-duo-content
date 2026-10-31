#!/usr/bin/env python3
import sys,os,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assemble_lib import build
A="assets/backgrounds/"; V="assets/voice/"; D=json.load(open(V+"durations.json"))
T=[];AU=[];t=0.0
def add(dur,av,sub,style=""): 
    global t; T.append((round(t,2),round(t+dur,2),av,sub,style)); t+=dur
# hook (no voice): ยายอัสตาโตดีใจ + ซับ
add(2.8,"yaaus_amazed","ที่นี่ ไม่ใช่ฉากถ่ายหนัง","hook")
# ชู่ว์ -> เว้น 1 วิ -> ยาย ที่นี่...
AU.append((V+"K2_shh.wav",t)); add(D["K2_shh"],"nongtour_shh","ชู่ว์")
add(1.0,"nongtour_shh",None)
AU.append((V+"K2_yai_thinee.wav",t)); add(D["K2_yai_thinee"]+0.35,"nongtour_shh","ยาย ที่นี่คือย่านที่คนอยู่จริง")
AU.append((V+"K2_rule.wav",t)); add(D["K2_rule"]+0.3,"nongtour_shh","นักท่องเที่ยวเข้าโซนพิเศษได้แค่<br>10:00–17:00")
AU.append((V+"K2_soft.wav",t)); add(D["K2_soft"]+0.25,"nongtour_shh","เดินเบาๆ ถ่ายรูปเสร็จแล้วไป")
AU.append((V+"K2_fine.wav",t)); add(D["K2_fine"]+0.3,"nongtour_shh","ฝ่าฝืน อาจโดนปรับนะ")
t_quote=t
add(4.0,"yaaus_whisper","ที่เที่ยวของเรา…<br>คือบ้านของเขา","quote")   # เสียงยายอัส ยังไม่มี
t_cta=t
AU.append((V+"K2_cta.wav",t)); add(D["K2_cta"]+0.5,None,"อยากไปเกาหลีแบบรู้กฎ<br><b>ทักไลน์ทัวริสอัส</b>","cta")
tot=round(t,2); print("K2 total",tot)
build("K2",
 {"yaaus_amazed":"K2_s1_yaaus_amazed_test","yaaus_whisper":"K2_s2_yaaus_whisper","nongtour_shh":"K2_s3_nongtour_shh"},T,
 [(A+"bg_K2_alley.png",round(t_quote,2),""),(A+"bg_K2_house_door.png",round(t_cta-t_quote,2),""),(A+"bg_K2_alley.png",round(tot-t_cta,2),",boxblur=14:2,eq=brightness=-0.18")],
 audio=AU)
