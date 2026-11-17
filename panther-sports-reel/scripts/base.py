import subprocess
from edl import EDL
FPS=30
paths=[]
for i,(a,b,src,si,m) in enumerate(EDL):
    # frame-accurate durations from cumulative frame counts
    fa=round(a*FPS); fb=round(b*FPS); nf=fb-fa; d=nf/FPS
    path=f"../{'ai' if src[0]=='A' else 'real'}/{src}.mp4"
    grade = ",eq=saturation=1.12:contrast=1.04" if src[0]=='R' else ""
    z=f"1+0.06*t/{d:.3f}"  # slow push-in
    if m=='v':
        vf=(f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"scale=w='trunc(1080*({z})/2)*2':h=-2:eval=frame,crop=1080:1920")
    elif m.startswith('c'):
        fx=float(m[1:])
        vf=(f"fps={FPS},crop=ih*9/16:ih:'max(0,min(iw-ih*9/16,iw*{fx}-ih*9/32))':0,scale=1080:1920,"
            f"scale=w='trunc(1080*({z})/2)*2':h=-2:eval=frame,crop=1080:1920")
    elif m=='s3':
        vf=(f"fps={FPS},scale=1080:640:force_original_aspect_ratio=increase,crop=1080:640,split=3[p1][p2][p3];[p1][p2][p3]vstack=3")
    vf+=grade+",setsar=1,format=yuv420p"
    out=f"shots/{i:02d}.mp4"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(si),'-i',path,'-filter_complex',vf,'-frames:v',str(nf),'-an',
        '-c:v','libx264','-preset','fast','-crf','16','-r',str(FPS),out],check=True)
    paths.append(out)
open('shots.txt','w').write(''.join(f"file '{p}'\n" for p in paths))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','shots.txt','-c','copy','base.mp4'],check=True)
