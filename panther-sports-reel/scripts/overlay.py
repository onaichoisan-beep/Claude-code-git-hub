import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,DUR=1080,1920,30,75.0
F='../fonts/Mukta-ExtraBold.ttf'
CAPS="""0.00|क्या आप जानना
0.80|चाहते हैं कि
1.52|आपके बच्चे के लिए
2.62|सही क्रिकेट एकेडमी
3.90|या सही स्पोर्ट्स
5.18|प्लेटफॉर्म कौन-सा है?
6.54|तो अब आपके लिए
7.80|एक नई और
8.64|विशेष पहल
9.36|लेकर आया है
10.14|पैंथर स्पोर्ट्स
11.32|इंडिया प्राइवेट लिमिटेड
12.76|हम उन सभी
13.50|माता-पिता और
14.28|खिलाड़ियों के लिए
15.06|काउंसलिंग उपलब्ध
15.72|करा रहे हैं
16.94|जो अपने बेटे
17.74|या बेटी के खेल
18.80|के भविष्य को
19.52|बेहतर दिशा
20.22|देना चाहते हैं
21.26|पैंथर स्पोर्ट्स
22.06|इंडिया प्राइवेट
22.74|लिमिटेड के पास
23.76|बिहार के विभिन्न
24.80|क्षेत्रों में
25.44|क्रिकेट एकेडमी,
26.58|स्कूलों और
27.50|अन्य स्पोर्ट्स
28.14|संस्थानों के साथ
29.16|कई सहयोग
30.06|और नेटवर्क
30.70|उपलब्ध हैं
31.54|हमारा उद्देश्य है
32.62|कि हर खिलाड़ी
33.58|और अभिभावक को
34.52|सही जानकारी मिले
35.62|और वे अपने
36.48|क्षेत्र के अनुसार
37.54|बेहतरीन क्रिकेट
38.52|एकेडमी और
39.46|सही स्पोर्ट्स अवसर
40.44|का चयन कर सकें
41.80|अपने बच्चे के लिए
42.84|सही एकेडमी
43.78|और सही ट्रेनिंग
44.76|कैसे चुनें?
45.76|हम सिर्फ
46.28|क्रिकेट एकेडमी की
47.12|जानकारी ही नहीं देते
48.54|बल्कि हेल्थ टिप्स
49.86|योग सेशन
50.80|फिटनेस गाइडेंस
51.74|और शारीरिक
52.66|एवं मानसिक विकास
53.74|से जुड़ी
54.18|महत्वपूर्ण जानकारी
55.40|भी प्रदान करने
56.18|का प्रयास करते हैं
57.56|हमारा कार्यालय
58.50|डाक बंगला चौराहा,
59.90|पटना में
60.36|स्थित है
60.76|अगर आपके पास
62.02|कार्यालय आने का
62.84|समय नहीं है
63.90|तो आप हमारी
64.52|वेबसाइट के माध्यम से
65.70|वीडियो देख सकते हैं
67.02|और हमें मैसेज
67.74|करके भी
68.26|जानकारी प्राप्त
69.08|कर सकते हैं
70.12|आज ही
70.64|पैंथर स्पोर्ट्स
71.58|इंडिया प्राइवेट
72.26|लिमिटेड से जुड़िए!
73.40|आज ही जुड़िए!
75.00|END"""
caps=[(float(a),b) for a,b in (l.split('|') for l in CAPS.strip().splitlines())]
segs=[(caps[i][0],min(caps[i+1][0],caps[i][0]+3.2),caps[i][1]) for i in range(len(caps)-1)]
RED=(226,30,38,255)
def box_text(text,size,fill=RED,txt=(255,255,255,255),padx=34,pady=14,rad=16):
    f=ImageFont.truetype(F,size,layout_engine=ImageFont.Layout.RAQM)
    bb=f.getbbox(text,language='hi'); tw,th=bb[2]-bb[0],bb[3]-bb[1]
    im=Image.new('RGBA',(tw+2*padx+20,th+2*pady+24),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((10,16,10+tw+2*padx,16+th+2*pady),rad,fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(6)); im=Image.alpha_composite(im,sh)
    d=ImageDraw.Draw(im); d.rounded_rectangle((10,10,10+tw+2*padx,10+th+2*pady),rad,fill=fill)
    d.text((10+padx-bb[0],10+pady-bb[1]),text,font=f,fill=txt,language='hi',stroke_width=2,stroke_fill=(120,0,0,255))
    return im
cap_imgs={t:box_text(t,74) for _,_,t in segs}
# logo: white rounded tile like the reference
badge=Image.open('../logo_badge_patna.png'); bw=badge.width
TS=176; tile=Image.new('RGBA',(TS+40,TS+40),(0,0,0,0))
tsh=Image.new('RGBA',tile.size,(0,0,0,0)); ImageDraw.Draw(tsh).rounded_rectangle((20,24,20+TS,24+TS),26,fill=(0,0,0,110)); tile=Image.alpha_composite(tile,tsh.filter(ImageFilter.GaussianBlur(8)))
ImageDraw.Draw(tile).rounded_rectangle((20,20,20+TS,20+TS),26,fill=(255,253,245,255))
b2=badge.resize((int(bw*0.78),int(bw*0.78)),Image.LANCZOS); tile.alpha_composite(b2,((tile.width-b2.width)//2,(tile.height-b2.height)//2+1))
logo=tile; LX,LY=W-logo.width-26,40
# CALL NOW + phone strip like the reference
FL='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
def pill(text,size,fill,txt,outline=None,padx=14,pady=6,rad=10):
    f=ImageFont.truetype(FL,size); bb=f.getbbox(text); tw,th=bb[2]-bb[0],bb[3]-bb[1]
    im=Image.new('RGBA',(tw+2*padx+6,th+2*pady+6),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((3,3,3+tw+2*padx,3+th+2*pady),rad,fill=fill,outline=outline,width=3 if outline else 0)
    d.text((3+padx-bb[0],3+pady-bb[1]),text,font=f,fill=txt); return im
nums=[pill(n,40,(226,30,38,255),(255,255,255,255),outline=(255,255,255,255)) for n in ('9153834432','6201538442','7870650296')]
gap=10; sw=sum(p.width for p in nums)+gap*2
STRIP=Image.new('RGBA',(W,140),(0,0,0,0))
cn=pill('CALL NOW',22,(18,18,18,235),(255,255,255,255),padx=16,pady=6,rad=14)
STRIP.alpha_composite(cn,((W-cn.width)//2,0))
x=(W-sw)//2
for p in nums: STRIP.alpha_composite(p,(x,cn.height+2)); x+=p.width+gap
STRIP_Y=1440-cn.height-2
# brand titles (red box top, white text) like the reference
def title_img(l1,l2):
    a=box_text(l1,80,padx=30,pady=8,rad=10); b=box_text(l2,56,padx=24,pady=6,rad=10)
    im=Image.new('RGBA',(max(a.width,b.width),a.height+b.height-6),(0,0,0,0))
    im.alpha_composite(a,((im.width-a.width)//2,0)); im.alpha_composite(b,((im.width-b.width)//2,a.height-6)); return im
TITLE=title_img('PANTHOR SPORTS','INDIA PVT. LTD.')
titles=[(21.26,23.76,TITLE),(73.18,75.0,TITLE)]
from edl import FLASH
flashes=FLASH
CAP_CY=1560
out=sys.stdout.buffer
base=Image.new('RGBA',(W,H),(0,0,0,0))
cache={}
for n in range(int(DUR*FPS)):
    t=n/FPS
    cur=[s for s in segs if s[0]<=t<s[1]]
    tit=[x for x in titles if x[0]<=t<x[1]]
    fl=[f for f in flashes if 0<=t-f<0.2]
    key=None
    if cur:
        k=int((t-cur[0][0])*FPS); key=('c',cur[0][2],min(k,5))
    tk=None
    if tit:
        k=int((t-tit[0][0])*FPS); tk=min(k,6)
    flv=round(1-(t-fl[0])/0.2,2) if fl else 0
    ck=(key,tk,flv)
    if ck not in cache:
        im=base.copy()
        if tit:
            ti=tit[0][2]; s=[0.6,0.8,0.95,1.06,1.03,1.0,1.0][tk]
            tim=ti.resize((int(ti.width*s),int(ti.height*s)),Image.BICUBIC)
            im.alpha_composite(tim,((W-tim.width)//2-60,250-tim.height//2+30))
        if key:
            ci=cap_imgs[key[1]]; s=[0.7,0.88,1.06,1.03,1.0,1.0][key[2]]
            ci2=ci.resize((int(ci.width*s),int(ci.height*s)),Image.BICUBIC)
            im.alpha_composite(ci2,((W-ci2.width)//2,CAP_CY-ci2.height//2))
        im.alpha_composite(STRIP,(0,STRIP_Y))
        im.alpha_composite(logo,(LX,LY))
        if flv>0:
            fw=Image.new('RGBA',(W,H),(255,255,255,int(200*flv))); im=Image.alpha_composite(fw,im) if False else Image.alpha_composite(im,fw)
            im.alpha_composite(STRIP,(0,STRIP_Y)); im.alpha_composite(logo,(LX,LY))
        if len(cache)>60: cache.clear()
        cache[ck]=im.tobytes()
    out.write(cache[ck])
