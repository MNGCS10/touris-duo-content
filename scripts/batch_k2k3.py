import subprocess, concurrent.futures as cf, sys
R="https://raw.githubusercontent.com/MNGCS10/tmp-ref/main/"
YA=("Using the reference sheet, draw ONLY the character 'ยายอัส' (elderly grandma traveler: short gray hair, pink patterned short-sleeve shirt, black cropped pants, pink sneakers, pink cardigan) exactly matching the reference's face, hair, outfit and 3D Pixar-style chibi render. ")
NT=("Using the reference sheet, draw ONLY the character 'น้องทัวร์' (young pro travel guide: black bob hair, black glasses, black sweater with the 'Touris US' print, black pants, black star sneakers) exactly matching the reference's face, hair, outfit and 3D Pixar-style chibi render. ")
TAIL=" Full body, plain flat light-grey background, soft studio lighting. No other characters, no panels, no labels, no question marks, no speech bubbles, no watermark."
ya=lambda p:(YA+p+TAIL+" No text anywhere.", R+"yaaus-sheet.jpg")
nt=lambda p:(NT+p+TAIL+" No text except the sweater print.", R+"nongtour-sheet.jpg")
chars={
 "K2_s2_yaaus_whisper":ya("Pose: leaning slightly forward, one hand cupped beside her mouth as if whispering a secret, sly playful grin, eyes looking sideways at the viewer."),
 "K2_s3_nongtour_shh":nt("Pose: index finger of one hand held up against his lips in a 'shh' gesture, eyebrows raised, calm knowing smile, other hand in pocket."),
 "K3_s1_yaaus_puzzled":ya("Pose: one finger on her chin, head tilted, puzzled thoughtful face with one eyebrow raised, other arm across her body."),
 "K3_s2_yaaus_climbing":ya("Pose: walking up mid-stride, one knee raised as if stepping up a stair, leaning slightly forward, slightly out of breath but cheerful, one hand on her thigh."),
 "K3_s3_nongtour_phone":nt("Pose: smiling warmly at the viewer, holding a smartphone in one hand and pointing at its screen with the other, friendly helpful guide look."),
 "K3_s4_yaaus_cheer":ya("Pose: both arms raised high in joy, eyes closed, big laughing open-mouth smile, one foot slightly lifted."),
}
bgs={
 "bg_K2_alley":"Soft illustrated storybook painting (gouache and watercolor, warm morning light) of a narrow sloping stone alley in Bukchon Hanok Village, Seoul, traditional hanok houses with grey tiled roofs and wooden doors on both sides, the alley leads gently downhill with a soft hint of distant city. Calm empty composition, lower third quiet and uncluttered. No people, no text, no signs, no letters.",
 "bg_K2_closed_gate":"Soft illustrated storybook painting (gouache and watercolor, soft daylight) of a large traditional Korean wooden palace gate tightly closed, stone base, tiled roof eaves above, empty stone plaza in front. Calm composition, lower third quiet and uncluttered. No people, no text, no signs, no letters.",
 "bg_K3_station_entrance":"Soft illustrated storybook painting (gouache and watercolor, daylight) of a Seoul subway station entrance, staircase descending underground between metal railings with a glass canopy, a warm glowing lamp, city street around. Calm composition, lower third quiet and uncluttered. No people, no text, no signs, no letters.",
 "bg_K3_train":"Soft illustrated storybook painting (gouache and watercolor) of the empty interior of a modern Seoul subway carriage, rows of seats, handrails and straps, windows showing blurred city lights, soft glow. Calm composition, lower third quiet and uncluttered. No people, no text, no signs, no letters.",
 "bg_K3_station_stairs":"Soft illustrated storybook painting (gouache and watercolor) of a wide station staircase going up out of an underground station toward bright daylight at the top, clean tiled walls, handrail. Calm composition, lower third quiet and uncluttered. No people, no text, no signs, no letters.",
}
jobs=[]
for n,(p,ref) in chars.items():
    jobs.append(["python3","scripts/kie_gen.py",p,f"assets/characters/{n}.png","--ref",ref,"--ratio","2:3"])
for n,p in bgs.items():
    jobs.append(["python3","scripts/kie_gen.py",p,f"assets/backgrounds/{n}.png","--model","gpt-image/1.5-text-to-image","--ratio","2:3"])
def run(c):
    r=subprocess.run(c,capture_output=True,text=True); return c[3].split('/')[-1], (r.stdout+r.stderr).strip()[-200:]
with cf.ThreadPoolExecutor(6) as ex:
    for n,o in ex.map(run,jobs): print(n,o)
