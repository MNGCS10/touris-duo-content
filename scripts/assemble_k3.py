#!/usr/bin/env python3
import sys,os,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assemble_lib import build
A="assets/backgrounds/"; V="assets/voice/"; D=json.load(open(V+"durations.json"))
T=[];AU=[];t=0.0
def add(dur,av,sub,style=""):
    global t; T.append((round(t,2),round(t+dur,2),av,sub,style)); t+=dur
add(3.0,"yaaus_puzzled","ยายนั่งใต้ดินได้กี่รอบ<br>ในวันเดียว?","hook")
t_stairs=t
for i in range(10): add(0.5,"yaaus_climbing" if i%2==0 else "yaaus_puzzled",None)     # ฉากขำ 5 วิ
t_train=t
note_start=t
AU.append((V+"K3_card.wav",t)); add(D["K3_card"]+0.3,"nongtour_phone","มีบัตร Climate Card ค่ะยาย")
AU.append((V+"K3_unlimited.wav",t)); add(D["K3_unlimited"]+0.3,"nongtour_phone","ขึ้นรถไฟใต้ดินกับรถเมล์ในโซล<br>ได้ไม่จำกัดจำนวนรอบ")
AU.append((V+"K3_cheaper.wav",t)); add(D["K3_cheaper"]+0.3,"nongtour_phone","3 วันถูกกว่าซื้อรายวันสามครั้ง")
T.append((round(note_start,2),round(t,2),None,"1 วัน 5,000 วอน · 3 วัน 10,000 วอน<br>+ ค่าบัตร 3,000 วอน (ราคา พ.ค. 2026)","note"))
add(2.2,"yaaus_cheer","งั้นยายนั่งให้คุ้มเลย!")          # เสียงยายอัส ยังไม่มี
t_quote=t
add(3.5,"yaaus_cheer","บัตรถูก แต่ถ้าไม่ออกไปเที่ยว<br>ก็ไม่คุ้มหรอกลูก","quote")   # เสียงยายอัส ยังไม่มี
t_cta=t
AU.append((V+"K3_cta.wav",t)); add(D["K3_cta"]+0.5,None,"วางแผนเดินทางเกาหลีกับทัวริสอัส<br><b>ทักไลน์</b>","cta")
tot=round(t,2); print("K3 total",tot)
build("K3",
 {"yaaus_puzzled":"K3_s1_yaaus_puzzled","yaaus_climbing":"K3_s2_yaaus_climbing","nongtour_phone":"K3_s3_nongtour_phone","yaaus_cheer":"K3_s4_yaaus_cheer"},T,
 [(A+"bg_K3_station_entrance.png",3,""),(A+"bg_K3_station_stairs.png",round(t_train-3,2),""),(A+"bg_K3_train.png",round(t_quote-t_train,2),""),
  (A+"bg_K3_station_stairs.png",round(t_cta-t_quote,2),""),(A+"bg_K3_station_entrance.png",round(tot-t_cta,2),",boxblur=14:2,eq=brightness=-0.18")],
 audio=AU)
