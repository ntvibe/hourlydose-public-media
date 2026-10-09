from PIL import Image,ImageDraw,ImageFilter
import math,random,pathlib
from generate import W,H,background
p=pathlib.Path(__file__).resolve().parent
img=background('math');a=Image.new('RGBA',(W,H));d=ImageDraw.Draw(a,'RGBA')
# Original abstract mathematical manuscript/certificate fragments, not depictions of a verified theorem.
for i in range(9):
 x=150+(i%3)*135+(i//3%2)*19;y=175+(i//3)*126
 w=110;h=100
 col=(63,213,240) if i%3 else (250,180,97)
 quad=[(x-52,y-45),(x+43,y-61),(x+60,y+40),(x-34,y+55)]
 d.polygon(quad,fill=(*col,21),outline=(*col,109))
 for j in range(4):
  bx=x-26+j*3
  d.line((bx,y-17+j*14,x+35,y-20+j*14),fill=(*col,57+j*23),width=2)
 d.ellipse((x-6,y-3,x+5,y+8),fill=(*col,170))
 for j in range(3):
  px=75+(i%3)*135+j*55
  d.line((x,y,px,620),fill=(*col,18),width=1)
blur=a.filter(ImageFilter.GaussianBlur(17));img=Image.alpha_composite(img,blur);img=Image.alpha_composite(img,a)
g=ImageDraw.Draw(img,'RGBA')
for i in range(15):
 t=i*.39;cx=W*.53+110*math.cos(t);cy=H*.4+85*math.sin(t)
 g.ellipse((cx-2,cy-2,cx+2,cy+2),fill=(253,241,213,180))
for j in range(200):g.line((0,H-200+j,W,H-200+j),fill=(3,9,17,int(j*.94)),width=1)
out=p/'math-scene-04-20261009.jpg';img.convert('RGB').resize((1080,1350),Image.Resampling.LANCZOS).save(out,quality=93,optimize=True)
print(out, out.stat().st_size)
