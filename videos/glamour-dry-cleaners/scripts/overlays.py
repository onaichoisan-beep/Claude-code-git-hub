from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys, os
W=sys.argv[1]; src=sys.argv[2]
im=Image.open(src).convert('RGBA')
# circle: white ring spans x~142..853, y~227..938 in 1038-wide shot
cx,cy,r=497,582,356
box=(cx-r,cy-r,cx+r,cy+r); c=im.crop(box)
S=c.size[0]; m=Image.new('L',(S*4,S*4),0); ImageDraw.Draw(m).ellipse((6,6,S*4-6,S*4-6),fill=255); m=m.resize((S,S),Image.LANCZOS)
c.putalpha(m)
c.save(f'{W}/ov/logo_full.png')
lg=c.resize((210,210),Image.LANCZOS)
# soft shadow
sh=Image.new('RGBA',(250,250),(0,0,0,0)); a=Image.new('L',(250,250),0); ImageDraw.Draw(a).ellipse((22,26,232,236),fill=120); a=a.filter(ImageFilter.GaussianBlur(8))
sh.putalpha(a); sh.alpha_composite(lg,(20,20)); sh.save(f'{W}/ov/logo_corner.png')
B='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'; SB='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
BLUE=(29,98,152,255); YEL=(255,204,41,255)
def card(lines, name, w=940):
    fonts=[ImageFont.truetype(f,s) for f,s,_ in lines]
    hs=[f.getbbox(t)[3]-f.getbbox(t)[1] for f,(_,_,t) in zip(fonts,lines)]
    H=sum(hs)+28*(len(lines)-1)+80
    img=Image.new('RGBA',(w,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    d.rounded_rectangle((0,0,w-1,H-1),36,fill=(15,45,80,225),outline=(255,255,255,235),width=5)
    y=40
    for f,(fp,s,t),h,col in zip(fonts,lines,hs,[l for l in [None]*len(lines)]):
        pass
    y=40
    for i,(f,(fp,s,t)) in enumerate(zip(fonts,lines)):
        bb=f.getbbox(t); tw=bb[2]-bb[0]
        d.text(((w-tw)/2-bb[0],y-bb[1]),t,font=f,fill=YEL if i==0 else (255,255,255,255))
        y+=hs[i]+28
    img.save(f'{W}/ov/{name}.png')
card([(B,58,'VISIT US'),(SB,46,'Near Prem Talkies, Beside Petrol Pump'),(SB,46,'56 Shaheed Road, Gaya')],'address')
card([(B,58,'CALL TODAY'),(B,104,'915 588 4401')],'phone')
card([(B,70,'GLAMOUR DRY CLEANERS'),(SB,52,'Unrivalled in Cleanliness!')],'tagline',w=1000)
