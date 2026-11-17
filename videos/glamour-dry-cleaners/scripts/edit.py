import subprocess, sys, os
W=sys.argv[1]; os.makedirs(f'{W}/seg',exist_ok=True)
REAL=f'{W}/real/real.mp4'; PHOTO=f'{W}/real/drive_img.png'
def ai(n): return f'{W}/ai/ai{n:02d}.mp4'
# (out_start, out_end, kind, src, src_in, src_out)   kind: R=real video, A=ai, P=photo
E=[
(0.00,2.00,'R',REAL,0.0,2.0),          # storefront (first frame)
(2.00,3.40,'A',ai(1),2.3,3.7),          # shaadi ke mehenge kapde
(3.40,4.30,'A',ai(2),0.0,0.9),          # designer lehenge
(4.30,5.90,'A',ai(4),0.0,1.6),          # banarasi
(5.90,7.15,'R',REAL,12.55,13.78),       # heavy lehenga
(7.15,10.00,'A',ai(2),1.2,4.03),        # chinta / naazuk kapde
(10.00,11.30,'R',REAL,1.6,2.9),         # walk into shop - samadhan
(11.30,13.00,'R',REAL,2.97,4.45),       # GR logo wall
(13.00,14.40,'R',REAL,4.48,5.38),       # Glamour sign
(14.40,15.95,'A',ai(6),0.05,1.6),       # shaadi
(15.95,17.00,'A',ai(6),1.8,2.85),       # reception
(17.00,17.70,'A',ai(6),3.3,4.0),        # sagai
(17.70,19.10,'A',ai(6),4.6,6.0),        # party
(19.10,20.60,'R',REAL,8.2,9.55),        # khaas mauke ke kapde
(20.60,22.20,'R',REAL,18.0,19.6),
(22.20,24.20,'A',ai(5),4.0,6.0),        # dry cleaning suvidha
(24.20,26.00,'R',REAL,13.85,15.65),     # banarasi saree (real)
(26.00,27.00,'A',ai(4),1.6,2.6),        # designer lehenga
(27.00,28.20,'R',REAL,20.55,21.75),     # kamaan lehenga
(28.20,29.00,'A',ai(4),5.0,5.8),        # heavy suit
(29.00,29.90,'A',ai(3),0.2,1.1),        # sherwani
(29.90,30.55,'R',REAL,11.4,12.05),      # coat-pant
(30.55,31.30,'A',ai(3),2.8,3.55),       # party wear
(31.30,33.20,'R',REAL,15.95,17.85),     # pasandida kapde
(33.20,34.50,'R',REAL,34.05,35.33),
(34.50,36.00,'A',ai(3),4.5,6.0),        # bharosa - Glamour
(36.00,38.95,'A',ai(12),1.1,4.03),      # ab baat sardiyon ki
(38.95,39.70,'R',REAL,50.05,50.8),      # kambal (packed)
(39.70,40.40,'A',ai(11),0.75,1.45),     # rajai
(40.40,41.00,'A',ai(11),0.0,0.6),       # sweater/woollen
(41.00,42.40,'R',REAL,40.7,42.1),       # jacket / blazer
(42.40,43.90,'R',REAL,37.55,39.0),      # sabhi oonee kapde
(43.90,45.30,'A',ai(9),0.0,1.4),
(45.30,46.80,'R',REAL,5.4,6.9),         # sampark - owner at counter
(46.80,49.30,'R',REAL,42.9,45.4),       # chhote ho ya bade
(49.30,51.80,'A',ai(10),0.5,3.0),       # rozmarra / khaas mauka
(51.80,54.40,'A',ai(9),1.4,4.0),        # sahi dekhbhaal
(54.40,58.60,'A',ai(8),0.0,4.03),       # alag-alag jagah - sab ek jagah
(58.60,60.40,'R',REAL,31.05,32.85),     # steam machine
(60.40,62.80,'A',ai(7),3.6,6.0),        # bharosemand naam
(62.80,64.40,'R',REAL,28.5,29.8),       # Glamour storefront
(64.40,66.60,'R',REAL,25.25,27.15),      # address street
(66.60,67.60,'R',REAL,27.2,28.0),
(67.60,68.60,'R',REAL,24.1,25.1),       # GAYA
(68.60,77.00,'P',PHOTO,0,0),            # call + end card
]
FPS=30
real_t=sum(b-a for a,b,k,*_ in E if k in 'RP'); ai_t=sum(b-a for a,b,k,*_ in E if k=='A')
print(f'real {real_t:.1f}s  ai {ai_t:.1f}s  ({100*real_t/(real_t+ai_t):.0f}% real)')
lst=[]
for i,(a,b,k,src,si,so) in enumerate(E):
    d=b-a; out=f'{W}/seg/{i:02d}.mp4'; lst.append(out)
    if os.path.exists(out): continue  # delete seg/ after changing the EDL
    nf=round(b*FPS)-round(a*FPS)
    if k=='P':
        vf=(f"scale=2160:-1,zoompan=z='1+0.10*on/{nf}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={nf}:s=1080x1920:fps={FPS},"
            "eq=saturation=1.08,format=yuv420p")
        cmd=['ffmpeg','-v','error','-y','-loop','1','-i',src,'-vf',vf,'-frames:v',str(nf)]
    else:
        sp=(so-si)/d
        if k=='R':
            base="crop=720:1030:0:0,scale=-2:1920:flags=lanczos,crop=1080:1920,eq=contrast=1.04:saturation=1.10"
        else:
            base="scale=1080:1920:flags=lanczos"
        vf=f"trim={si}:{so},setpts=(PTS-STARTPTS)/{sp:.5f},fps={FPS},{base},setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=30"
        cmd=['ffmpeg','-v','error','-y','-i',src,'-vf',vf,'-frames:v',str(nf)]
    cmd+=['-an','-c:v','libx264','-preset','medium','-crf','16','-r',str(FPS),out]
    subprocess.run(cmd,check=True)
with open(f'{W}/seg/list.txt','w') as f: f.writelines(f"file '{p}'\n" for p in lst)
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/seg/list.txt','-c','copy',f'{W}/body.mp4'],check=True)
# final: logo corner always, address 64.4-68.6, phone 68.9-73.4, tagline + big logo 73.4-end
fc=("[0:v]format=gbrp[base];[8:v]scale=1080:1920:flags=bicubic,gblur=sigma=6,format=gbrp[fx];[base][fx]blend=all_mode=screen,format=yuv420p[vb];"
    "[vb][2:v]overlay=W-w-14:14[v1];"
    "[3:v]fade=in:st=64.5:d=0.3:alpha=1,fade=out:st=68.3:d=0.25:alpha=1[ad];[v1][ad]overlay=(W-w)/2:1180:enable='between(t,64.4,68.6)'[v2];"
    "[4:v]fade=in:st=68.8:d=0.3:alpha=1,fade=out:st=73.2:d=0.2:alpha=1[ph];[v2][ph]overlay=(W-w)/2:1200:enable='between(t,68.7,73.45)'[v3];"
    "[5:v]scale=520:520,fade=in:st=73.4:d=0.4:alpha=1[bl];[v3][bl]overlay=(W-w)/2:560:enable='gte(t,73.4)'[v4];"
    "[6:v]fade=in:st=73.7:d=0.4:alpha=1[tg];[v4][tg]overlay=(W-w)/2:1180:enable='gte(t,73.6)'[vout];"
    "[1:a]aresample=48000,volume=1.0,asplit=2[vo][key];"
    "[7:a]aresample=48000,volume=0.62[bg];[bg][key]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=350[bgd];"
    "[vo][bgd]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:77,apad=whole_dur=77[aout]")
cmd=['ffmpeg','-v','error','-y','-i',f'{W}/body.mp4','-i',f'{W}/vo.mp3',
     '-loop','1','-i',f'{W}/ov/logo_corner.png','-loop','1','-i',f'{W}/ov/address.png','-loop','1','-i',f'{W}/ov/phone.png',
     '-loop','1','-i',f'{W}/ov/logo_full.png','-loop','1','-i',f'{W}/ov/tagline.png','-i',f'{W}/bgm.wav','-i',f'{W}/fx.mp4',
     '-filter_complex',fc,'-map','[vout]','-map','[aout]','-t','77','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p',
     '-c:a','aac','-b:a','192k','-movflags','+faststart',f'{W}/glamour_final.mp4']
subprocess.run(cmd,check=True)
