#!/usr/bin/env python3
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assemble_lib import build
A="assets/backgrounds/"
# 3-8s: "ฉากขำ" ยายอัสเดินวนขึ้นลงบันได = สลับสองท่าเร็วๆ (puzzled <-> climbing)
flip=[(3+0.5*i,3.5+0.5*i,"yaaus_climbing" if i%2==0 else "yaaus_puzzled",None,"") for i in range(10)]
build("K3",
 {"yaaus_puzzled":"K3_s1_yaaus_puzzled","yaaus_climbing":"K3_s2_yaaus_climbing","nongtour_phone":"K3_s3_nongtour_phone","yaaus_cheer":"K3_s4_yaaus_cheer"},
 [(0,3,"yaaus_puzzled","ยายนั่งใต้ดินได้กี่รอบ<br>ในวันเดียว?","hook"),*flip,
  (8,11.5,"nongtour_phone","มีบัตร Climate Card ค่ะยาย",""),
  (8,15,None,"1 วัน 5,000 วอน · 3 วัน 10,000 วอน<br>+ ค่าบัตร 3,000 วอน (ราคา พ.ค. 2026)","note"),
  (11.5,15,"nongtour_phone","ขึ้นรถไฟใต้ดินกับรถเมล์ในโซล<br>ได้ไม่จำกัดจำนวนรอบ",""),
  (15,17,"nongtour_phone","3 วันถูกกว่าซื้อรายวันสามครั้ง",""),
  (17,19,"yaaus_cheer","งั้นยายนั่งให้คุ้มเลย!",""),
  (19,22,"yaaus_cheer","บัตรถูก แต่ถ้าไม่ออกไปเที่ยว<br>ก็ไม่คุ้มหรอกลูก","quote"),
  (22,24,None,"วางแผนเดินทางเกาหลีกับทัวริสอัส<br><b>ทักไลน์</b>","cta")],
 [(A+"bg_K3_station_entrance.png",3,""),(A+"bg_K3_station_stairs.png",5,""),(A+"bg_K3_train.png",11,""),
  (A+"bg_K3_station_stairs.png",3,""),(A+"bg_K3_station_entrance.png",2,",boxblur=14:2,eq=brightness=-0.18")])
