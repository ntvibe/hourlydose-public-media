#!/usr/bin/env python3
"""Original editorial motion studies; no borrowed footage or model demonstrations."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, math, random, subprocess, pathlib, sys

W,H=720,900
FPS=20
DURATION=7
OUT=pathlib.Path(__file__).resolve().parent
noise=np.random.default_rng(20261009)
xx,yy=np.meshgrid(np.arange(W),np.arange(H))
def background(kind):
    c=(28,13,55) if kind=='haiku' else (9,26,42)
    vignette=np.maximum(0,1-((xx-W*.53)**2/(W*.7)**2+(yy-H*.37)**2/(H*.8)**2)*.75)
    glow=np.exp(-((xx-W*.54)**2/(W*.5)**2+(yy-H*.38)**2/(H*.52)**2)*3)
    ar=np.zeros((H,W,3),dtype=np.uint8)
    colors=([6,6,18],c) if kind=='haiku' else ([4,10,18],c)
    n=noise.normal(0,2.0,(H,W))
    for i in range(3):
        ar[:,:,i]=np.clip(colors[0][i]+glow*colors[1][i]+vignette*4+n,0,255)
    return Image.fromarray(ar,'RGB').convert('RGBA')
def draw_frame(kind,t,base,stars):
    frame=base.copy()
    # Motion-layer bloom and refracted backlight
    halo=Image.new('RGBA',(W,H)); hd=ImageDraw.Draw(halo,'RGBA')
    for j in range(7):
        x=int(W*(.51+.07*math.sin(t*.6+j))); y=int(H*(.40+.03*math.cos(t*.7+j)))
        width=int(195+j*30)
        if kind=='haiku': color=(116,54,255,max(0,12-j))
        else: color=(26,205,245,max(0,13-j))
        hd.ellipse((x-width,y-width*.83,x+width,y+width*.83),fill=color)
    frame=Image.alpha_composite(frame,halo.filter(ImageFilter.GaussianBlur(43)))
    d=ImageDraw.Draw(frame,'RGBA')
    # Perspective floor and the orbiting technical grid
    for i in range(12):
        y=H*.22+i**1.55*13
        alpha=int(23*(1-i/15))
        d.line((0,y,W,y+4), fill=(85,128,202,alpha),width=1)
    for i in range(-8,9):
        x=W*.5+i*80
        d.line((W*.50,H*.30,x,H*.85),fill=(80,134,202,27),width=1)
    for x,y,z in stars:
        dy=(y+t*11*(.2+z))%H
        col=(130,150,255,40+int(z*100)) if kind=='haiku' else (90,218,240,30+int(z*110))
        d.ellipse((x,dy,x+1+z,dy+1+z),fill=col)
    cx,cy=W*.53,H*.40
    # Geometric light trails under the data structure.
    glow_layer=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow_layer,'RGBA')
    palette=[(60,223,255),(138,76,248),(255,93,190)] if kind=='haiku' else [(19,238,247),(91,150,255),(242,173,89)]
    for i in range(12):
        p=i*math.pi/6+t*.29
        r=145+38*math.sin(i*4+t*.6)
        px=cx+r*math.cos(p);py=cy+.57*r*math.sin(p)
        co=palette[i%3]
        g.line((cx,cy,px,py),fill=(*co,38),width=5)
        g.ellipse((px-6,py-6,px+6,py+6),fill=(*co,160))
    frame=Image.alpha_composite(frame,glow_layer.filter(ImageFilter.GaussianBlur(16)))
    d=ImageDraw.Draw(frame,'RGBA')
    # Main central original scene changes per topic.
    if kind=='haiku':
        # Supervisor diamond shape, connected to small task shards.
        for i in range(10):
            rot=t*.24+i*math.tau/10
            rad=175+22*math.sin(t*.5+i)
            px=cx+rad*math.cos(rot);py=cy+rad*.56*math.sin(rot)
            co=palette[i%3]
            d.line((cx,cy,px,py),fill=(*co,52),width=2)
            rr=11+2*math.sin(t*2+i)
            shape=[(px,py-rr),(px+rr*.78,py),(px,py+rr),(px-rr*.78,py)]
            d.polygon(shape,fill=(*co,96),outline=(*co,190))
            d.ellipse((px-3,py-3,px+3,py+3),fill=(239,249,255,210))
        for layer in range(5,0,-1):
            r=24+layer*18
            diamond=[(cx,cy-r*1.5),(cx+r*1.15,cy),(cx,cy+r*1.5),(cx-r*1.15,cy)]
            d.line(diamond+[diamond[0]],fill=(86,210,255,38+layer*20),width=2)
        d.polygon([(cx,cy-51),(cx+38,cy),(cx,cy+51),(cx-38,cy)],fill=(36,27,103,230),outline=(123,243,255,255))
        d.line((cx,cy-33,cx+25,cy), fill=(225,234,255,220),width=2)
        d.line((cx+25,cy,cx,cy+33),fill=(200,106,255,200),width=2)
    else:
        # Archival manuscript sheets, orbiting a proof network.
        for i in range(7):
            p=t*.2+i*math.tau/7; x=cx+178*math.cos(p); y=cy+95*math.sin(p)
            rr=16+5*(.5+.5*math.sin(t+i))
            quad=[(x-rr*.7,y-rr),(x+rr*.6,y-rr*.65),(x+rr,y+rr),(x-rr*.6,y+rr*.6)]
            d.polygon(quad,fill=(15,42,66,140),outline=(71,204,237,130))
            for k in range(3):d.line((x-rr*.4,y-rr*.4+k*rr*.34,x+rr*.6,y-rr*.2+k*rr*.34),fill=(123,232,236,95),width=1)
            d.line((cx,cy,x,y),fill=(103,200,238,46),width=2)
        for i in range(13):
            p=t*.15+i*math.tau/13
            x=cx+106*math.cos(p);y=cy+74*math.sin(p)
            d.ellipse((x-2,y-2,x+2,y+2),fill=(209,231,255,180))
        for rad in (52,69,86):
            d.ellipse((cx-rad,cy-rad*.67,cx+rad,cy+rad*.67),outline=(44,193,253,110),width=2)
        d.polygon([(cx,cy-32),(cx+47,cy),(cx,cy+32),(cx-47,cy)],fill=(5,51,68,210),outline=(250,203,124,220))
    # Fine motion rings and luminous small tracer particles
    for i in range(3):
        angle=t*.5+i*2.09
        px=cx+225*math.cos(angle);py=cy+110*math.sin(angle)
        d.arc((cx-220,cy-105,cx+220,cy+105),int(math.degrees(angle)),int(math.degrees(angle))+63,fill=(*palette[i],120),width=2)
        d.ellipse((px-4,py-4,px+4,py+4),fill=(232,249,255,220))
    # Dark text safe-region + accent separators for HourlyDose native overlays.
    safe=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(safe,'RGBA')
    for j in range(200):
        y=H-200+j
        gd.line((0,y,W,y),fill=(4,7,21,int(j/200*223)),width=1)
    frame=Image.alpha_composite(frame,safe)
    return frame.convert('RGB')

def render(kind):
    out=str(OUT/(kind+'-original-20261009.mp4'))
    cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-vf','scale=1080:1350:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','18','-movflags','+faststart','-an',out]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    base=background(kind);rnd=random.Random(3604)
    stars=[(rnd.randrange(W),rnd.randrange(H),rnd.random()*2) for _ in range(180)]
    try:
        for frame in range(FPS*DURATION):
            img=draw_frame(kind,frame/FPS,base,stars)
            if frame==int(FPS*DURATION*.28):img.save(str(OUT/(kind+'-preview-20261009.jpg')),quality=94)
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
        code=proc.wait()
        if code:raise RuntimeError('ffmpeg failed: '+str(code))
    finally:
        if proc.poll() is None:proc.kill()
    print(kind, 'ORIGINAL_VIDEO_READY',out,flush=True)

if __name__=='__main__':
    for k in ('math','haiku'):render(k)
