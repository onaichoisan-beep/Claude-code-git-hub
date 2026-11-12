#!/usr/bin/env bash
# Rebuilds every media asset the composition uses.
# Usage: tools/prep.sh /path/to/client.mp4   (the 1280x720 24p interview file)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=${1:?client video path}
mkdir -p assets/{footage,broll,mixkit,audio/src}

# --- client footage: trimmed dialogue (cuts "I think", "really interesting and sort of", pause before "Chamomile")
ffmpeg -v error -y -i "$SRC" -filter_complex "\
[0:a]atrim=0.38:1.80,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st=1.412:d=0.008[a1];\
[0:a]atrim=3.38:6.95,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st=3.562:d=0.008[a2];\
[0:a]atrim=7.30:20.50,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st=13.192:d=0.008[a3];\
[0:a]atrim=20.95:25.10,asetpts=PTS-STARTPTS,afade=t=in:d=0.008[a4];\
[a1][a2][a3][a4]concat=n=4:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7[out]" -map "[out]" -ar 48000 assets/audio/dialogue.wav

# --- 9:16 crops (405x720 window -> 1080x1920)
cut(){ ffmpeg -v error -y -ss "$2" -to "$3" -i "$SRC" -vf "crop=405:720:$4:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0,fps=30,format=yuv420p" -an -c:v libx264 -crf 16 assets/footage/$1.mp4; }
cut camA1 0.38 1.80 300
cut camA2 3.38 4.88 300
cut camBspk 7.30 9.86 110
cut camBint 9.86 10.58 860
cut camC 14.00 17.10 290
ffmpeg -v error -y -ss 21.01 -to 25.10 -i "$SRC" -vf "crop=600:720:250:0,scale=1080:1296:flags=lanczos,unsharp=5:5:0.6:5:5:0,fps=30,format=yuv420p" -an -c:v libx264 -crf 14 assets/footage/camClist_src.mp4
npx -y hyperframes@0.9.38 remove-background assets/footage/camClist_src.mp4 -o assets/footage/camClist_cutout.webm --quality best
ffmpeg -v error -y -c:v libvpx-vp9 -i assets/footage/camClist_cutout.webm -vf "tpad=stop_mode=clone:stop_duration=0.8" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 24 -auto-alt-ref 0 assets/footage/camClist_cutout_hold.webm

# --- Mixkit B-roll (free Mixkit licence)
for s in various-medications-16448 woman-exploring-an-online-sales-page-on-her-cell-phone-42136 different-medications-5697 \
  lot-of-pills-and-capsules-turning-34235 medications-piled-up-2856 prescription-bottles-and-medication-16420 \
  woman-with-red-led-mask-in-a-spa-52163 couple-opening-a-package-with-an-alarm-clock-42122 parcels-on-a-conveyor-belt-20770 \
  capsules-falling-on-a-table-20509 creating-herbal-tea-22670 lavender-flowers-close-up-1244 lavender-in-the-field-close-up-24990; do
  id=${s##*-}; [ -f assets/mixkit/$s.mp4 ] || curl -sSf -o assets/mixkit/$s.mp4 https://assets.mixkit.co/videos/$id/$id-720.mp4
done
enc="-an -c:v libx264 -crf 18 -pix_fmt yuv420p -r 30"
v(){ ffmpeg -v error -y -ss $3 -t $4 -i assets/mixkit/$2.mp4 -vf "$5" $enc assets/broll/$1.mp4; }
v br1_pills various-medications-16448 8 2.6 "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos"
v br2_hero woman-exploring-an-online-sales-page-on-her-cell-phone-42136 1 4.0 "scale=1080:1920:flags=lanczos"
i=0; for f in different-medications-5697 lot-of-pills-and-capsules-turning-34235 medications-piled-up-2856 prescription-bottles-and-medication-16420 \
  woman-with-red-led-mask-in-a-spa-52163 couple-opening-a-package-with-an-alarm-clock-42122 parcels-on-a-conveyor-belt-20770 skip capsules-falling-on-a-table-20509; do
  [ $f = skip ] || v tile$i $f 1.5 3.6 "crop=ih*9/16:ih,scale=540:960"; i=$((i+1)); done
v br3_tea creating-herbal-tea-22670 2 2.2 "crop=ih*9/16:ih,scale=760:1352:flags=lanczos"
v br3_lav lavender-flowers-close-up-1244 1 2.0 "crop=ih*9/16:ih,scale=760:1352:flags=lanczos"
v plate lavender-in-the-field-close-up-24990 0.5 5.0 "crop=ih*9/16:ih,scale=1080:1920:flags=bicubic,gblur=sigma=22,eq=saturation=0.85:brightness=0.03"

# --- Mixkit music + SFX, then the mix
M=https://assets.mixkit.co/music; X=https://assets.mixkit.co/active_storage/sfx
get(){ [ -f assets/audio/src/$1.mp3 ] || curl -sSf -o assets/audio/src/$1.mp3 "$2"; }
get music_serene $M/443/443.mp3; get pop $X/3005/3005-preview.mp3; get bubble $X/2357/2357-preview.mp3
get woosh $X/1489/1489-preview.mp3; get riser $X/645/645-preview.mp3; get ui $X/2573/2573-preview.mp3
get tick $X/1125/1125-preview.mp3; get swoosh $X/1474/1474-preview.mp3; get waves $X/1185/1185-preview.mp3
get chime $X/1107/1107-preview.mp3; get crystal $X/3108/3108-preview.mp3
python3 -I tools/mix.py
