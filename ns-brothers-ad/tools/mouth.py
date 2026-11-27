import sys, json, numpy as np, subprocess, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
opt=vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=sys.argv[1]),running_mode=vision.RunningMode.IMAGE,num_faces=3)
lm=vision.FaceLandmarker.create_from_options(opt)
FPS=25; out={}
for f in sys.argv[3:]:
    W,H=1440,1000
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-vf",f"fps={FPS},crop=720:500:0:200,scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3)
    tracks={}  # by face x-center bucket
    for i,img in enumerate(fr):
        r=lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(img)))
        for face in r.face_landmarks:
            p=lambda k:np.array([face[k].x*W,face[k].y*H])
            open_=np.linalg.norm(p(13)-p(14)); h=np.linalg.norm(p(10)-p(152))
            cx=round(p(1)[0]/360)
            tracks.setdefault(cx,{})[i]=open_/h
    name=f.split('/')[-1]; out[name]={}
    for cx,d in tracks.items():
        print(name,"bucket",cx,len(d),"of",len(fr))
        if len(d)<len(fr)*0.25: continue
        arr=np.array([d.get(i,np.nan) for i in range(len(fr))])
        out[name][int(cx*360)]=[None if np.isnan(x) else round(float(x),4) for x in arr]
        v=arr[~np.isnan(arr)]
        s=''.join(' ' if np.isnan(x) else ('#' if x>0.06 else ('+' if x>0.03 else '.')) for x in arr)
        print(name,'x~',cx*180,'n',len(v),'std',round(float(np.std(v)),4))
        for k in range(0,len(s),100): print(f"  {k/FPS:5.1f} {s[k:k+100]}")
json.dump(out,open(sys.argv[2],'w'))
