#!/usr/bin/env python3
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assemble_lib import build
A="assets/backgrounds/"
build("K2",
 {"yaaus_amazed":"K2_s1_yaaus_amazed_test","yaaus_whisper":"K2_s2_yaaus_whisper","nongtour_shh":"K2_s3_nongtour_shh"},
 [(0,3,"yaaus_amazed","ที่นี่ ไม่ใช่ฉากถ่ายหนัง","hook"),(3,5,"yaaus_amazed",None,""),(5,7,"nongtour_shh","ชู่ว์ค่ะยาย",""),
  (7,10,"nongtour_shh","ที่นี่คือย่านที่คนอยู่จริง",""),(10,13,"nongtour_shh","นักท่องเที่ยวเข้าโซนพิเศษได้แค่<br>10:00–17:00",""),
  (13,15.5,"nongtour_shh","เดินเบา ๆ ถ่ายรูปเสร็จแล้วไป",""),(15.5,18,"nongtour_shh","ฝ่าฝืนอาจโดนปรับนะ",""),
  (18,22,"yaaus_whisper","ที่เที่ยวของเรา…<br>คือบ้านของเขา","quote"),(22,24,None,"อยากไปเกาหลีแบบรู้กฎ<br><b>ทักไลน์ทัวริสอัส</b>","cta")],
 [(A+"bg_K2_alley.png",18,""),(A+"bg_K2_house_door.png",4,""),(A+"bg_K2_alley.png",2,",boxblur=14:2,eq=brightness=-0.18")])
