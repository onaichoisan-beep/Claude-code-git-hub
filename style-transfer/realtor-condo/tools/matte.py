import sys,glob,os,cv2,numpy as np
from rembg import new_session,remove
from PIL import Image
s=new_session('u2net_human_seg')
fs=sorted(glob.glob('aroll/f/a_*.jpg'))[int(sys.argv[1]):int(sys.argv[2])]
for f in fs:
    o='aroll/m/'+os.path.basename(f).replace('.jpg','.png')
    if os.path.exists(o): continue
    im=Image.open(f).resize((540,960))
    m=remove(im,session=s,only_mask=True)
    m.save(o)
