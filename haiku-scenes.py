"""Six original media panels for the Claude Haiku 5.5 editorial brief. No third-party art."""
import math, random, pathlib
from PIL import Image, ImageDraw, ImageFilter
from generate import W,H,background,draw_frame
BASE=pathlib.Path(__file__).resolve().parent
P=[(70,212,253),(146,72,252),(247,101,205)]
def render(k):
    if k==0:
        s=random.Random(42).random()
        stars=[(random.Random(i).randrange(W),random.Random(i+56).randrange(H),random.Random(i+98).random()*2) for i in range(110)]
        return draw_frame('haiku',1.4,background('haiku'),stars)
    img=background('haiku'); layers=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(layers,'RGBA')
    cx,cy=W*.51,H*.39
    # The six panels are authored visual metaphors, not measurements or product screenshots.
    if k==1: # row of repeatable low-cost workers
        for row in range(8,-1,-1):
            z=(row+2)/11;py=160+row*45
            for col in range(-4,5):
                px=cx+col*(38+z*26)
                s=13+z*14
                op=int(58+160*z)
                d.polygon([(px,py-s),(px+s,py),(px,py+s),(px-s,py)],fill=(36,33,106,op),outline=(*P[(row+col)%3],op))
                if (row+col)%4==0:d.ellipse((px-3,py-3,px+3,py+3),fill=(255,249,252,170))
    elif k==2: # symbolic price reduction, two size-different energy pillars
        for x,r,h,co in [(W*.32,59,290,(240,157,87)),(W*.68,32,135,(67,225,255))]:
            y=580
            for j in range(10):
                fy=y-j*h/10
                w=r*(1-.35*j/10)
                d.line((x-w,fy,x+w,fy),fill=(*co,14+j*14),width=3)
            d.polygon([(x-r,y),(x-r*.62,y-h),(x+r*.62,y-h),(x+r,y)],fill=(*co,39),outline=(*co,230))
            d.ellipse((x-r*.65,y-h-12,x+r*.65,y-h+11),fill=(*co,86))
        for i in range(11):
            y=150+i*25;d.line((W*.48,y,W*.58,y-10),fill=(163,113,255,35+i*9),width=2)
    elif k==3: # detailed photonic wafer wiring
        d.polygon([(cx,205),(cx+160,350),(cx,510),(cx-160,350)],fill=(15,32,87,200),outline=(76,233,255,210))
        for i in range(-7,8):
            ox=cx+i*19
            d.line((ox,245,ox+68,351,ox,464),fill=(*P[abs(i)%3],72),width=2)
            x=cx+185+16*abs(i);y=350+14*i
            d.line((cx+70,y,x,y,x+36,y+8),fill=(*P[abs(i)%3],134),width=2)
            d.ellipse((x+31,y+5,x+39,y+13),fill=(223,242,255,169))
        d.polygon([(cx,289),(cx+55,349),(cx,409),(cx-55,349)],fill=(23,22,111,255),outline=(195,101,255,255))
    elif k==4: # glowing memory crystal stacks
        for i in range(5):
            x=125+i*105;y=305+(i%2)*28;w=78
            for layer in range(4):
                ly=y+layer*46
                col=P[(i+layer)%3]
                points=[(x,ly-34),(x+w*.85,ly-22),(x+w,ly+16),(x+w*.2,ly+8)]
                d.polygon(points,fill=(*col,30+layer*7),outline=(*col,85+layer*19))
                d.line((x+w*.2,ly+8,x+w*.2,ly+35),fill=(*col,145),width=2)
        for i in range(7):
            y=520+i*15
            d.arc((100,y-90,610,y+90),190+20*i,300+10*i,fill=(*P[i%3],74),width=3)
    elif k==5: # leader model and worker swarm
        x=W*.42;y=350
        poly=[(x-90,y+150),(x-67,y-175),(x+50,y-201),(x+94,y+125)]
        d.polygon(poly,fill=(32,33,106,158),outline=(98,232,255,226))
        for i in range(8):d.line((x-70+i*17,y-131,x-72+i*18,y+97),fill=(135,157,247,40+i*10),width=2)
        for i in range(16):
            theta=i*2.399+1;x2=W*.7+100*math.cos(theta);y2=350+170*math.sin(theta)
            size=6+(i%4)*4;co=P[i%3]
            d.line((x+66,y+20,x2,y2),fill=(*co,76),width=2)
            d.polygon([(x2,y2-size),(x2+size,y2),(x2,y2+size),(x2-size,y2)],fill=(*co,140),outline=(*co,220))
    img=Image.alpha_composite(img,layers.filter(ImageFilter.GaussianBlur(19)))
    img=Image.alpha_composite(img,layers)
    # bottom editorial copy-safe fade
    gd=ImageDraw.Draw(img,'RGBA')
    for q in range(190):
        yy0=H-190+q
        gd.line((0,yy0,W,yy0),fill=(2,4,12,int(183*q/190)),width=1)
    return img.convert('RGB')
for index in range(6):
    im=render(index).resize((1080,1350),Image.Resampling.LANCZOS)
    outfile=BASE/f'haiku-scene-{index+1:02d}-20261009.jpg'
    im.save(outfile,quality=91,optimize=True)
    print(outfile.name,outfile.stat().st_size,flush=True)
