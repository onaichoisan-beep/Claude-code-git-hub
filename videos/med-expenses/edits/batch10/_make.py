# Generates 10 NEET-aspirant specs (shared style: centred plain text, dissolves, watermark, 2 soft SFX).
HEAD = '''DROP = None
END = {end}
FADE_OUT = 0.5
MID_CAPTIONS = True
CAPTION_BOX = False
XFADE = "dissolve"
XFADE_DUR = 0.3
WATERMARK = ("@hey.rishish", 0.79)
SHOTS = {shots}
SFX = [("Lit_heartbeat1", 0.8, -13), ("Quick_whoosh", {turn}, -13)]
'''
V = {
 "01_one_year_from_now": [
   ("IMG_8965", 3.9, 2.2, "NEET aspirant, one year from now…", {"vzoom": 1.22, "cy": 1.0}),
   ("IMG_9242", 1.83, 2.0, "you could be walking here", {}),
   ("IMG_0752", 1.4, 2.0, "sitting in medical conferences", {"fit": True}),
   ("MeinLAB", 9.0, 2.0, "wearing the coat you dreamed of", {}),
   ("IMG_8307", 14.43, 2.2, "it's closer than you think 🤍", {"smooth": True})],
 "02_what_rank_unlocks": [
   ("IMG_6262", 0.0, 2.0, "NEET aspirant, this is what your rank unlocks", {"smooth": True}),
   ("E56BD187", 0.75, 1.15, "a campus you'll call home", {"denoise": True}),
   ("IMG_4318", 1.5, 1.8, "friends for the next 6 years", {}),
   ("IMG_9858", 9.1, 1.8, "a stage to share what you learn", {"fit": True}),
   ("bc1a3ac4", 20.33, 2.2, "so give it everything 🔥", {"smooth": True})],
 "03_call_home": [
   ("F1D19DE4", 4.5, 2.2, "NEET aspirant, think about the call home", {"smooth": True}),
   ("IMG_8965", 8.7, 1.8, "the day you say \"mumma, ho gaya\"", {}),
   ("IMG_6261", 0.0, 1.0, "the day this college becomes yours", {"smooth": True}),
   ("IMG_8785", 1.33, 2.0, "the day they see you in the coat", {"transpose": 1, "fit": True, "smooth": True}),
   ("IMG_9323", 0.55, 2.2, "study for that day 🤍", {"smooth": True})],
 "04_low_mock_score": [
   ("IMG_0959", 5.3, 2.2, "NEET aspirant, low mock score today?", {}),
   ("IMG_1479", 4.9, 1.8, "it's a test, not your result", {}),
   ("IMG_0752", 11.0, 1.8, "your final score decides this seat", {"fit": True}),
   ("MeinLAB", 3.5, 1.8, "not today's number", {}),
   ("IMG_2515", 0.3, 2.2, "fix the mistakes. move on. keep going 🤍", {"fit": True, "smooth": True})],
 "05_months_decide": [
   ("IMG_1510", 2.2, 2.2, "NEET 2027 aspirant, these months decide your next 6 years", {}),
   ("IMG_1480", 4.77, 1.8, "every chapter you finish now", {}),
   ("IMG_1364", 2.27, 1.6, "every question you solve tonight", {}),
   ("bc1a3ac4", 16.83, 1.8, "is a step closer to this", {"smooth": True}),
   ("MeinLAB", 16.6, 2.2, "make them count 🔥", {})],
 "06_every_doctor_started": [
   ("studyclip", 0.5, 2.2, "NEET aspirant, every doctor started at a desk like this", {}),
   ("IMG_0959", 8.7, 1.8, "same doubts. same late nights.", {}),
   ("IMG_9858", 2.2, 1.8, "now they teach their batch", {"fit": True}),
   ("IMG_0752", 8.0, 1.8, "and sit in conferences", {"fit": True}),
   ("MeinLAB", 12.3, 2.2, "your desk is your starting line 🤍", {})],
 "07_quiet_grind": [
   ("IMG_0959", 10.9, 2.2, "NEET aspirant, nobody sees the quiet grind", {}),
   ("IMG_1480", 5.7, 1.8, "the notes. the revisions. the doubts.", {}),
   ("bc1a3ac4", 12.8, 1.8, "but one day everyone sees this", {"smooth": True}),
   ("IMG_9858", 5.0, 1.8, "your name on the slide", {"fit": True}),
   ("IMG_9323", 1.38, 2.2, "trust the process 🤍", {"smooth": True})],
 "08_imagine_first_day": [
   ("IMG_6262", 0.3, 2.2, "NEET aspirant, imagine your first day", {"smooth": True}),
   ("IMG_6273", 0.0, 1.1, "practical rooms with your name on the list", {}),
   ("IMG_9839", 1.6, 1.8, "tests you only read about", {}),
   ("IMG_4318", 10.0, 1.8, "a lab partner by your side", {}),
   ("IMG_8307", 15.4, 1.8, "walking in like you belong there", {"smooth": True}),
   ("IMG_9247", 5.0, 1.8, "it's waiting for you 🤍", {"transpose": 2, "fit": True, "smooth": True})],
 "09_remember_why": [
   ("IMG_8965", 0.4, 2.2, "NEET aspirant, remember why you started", {"smooth": True}),
   ("2A473245", 4.4, 1.8, "for the version of you that made it", {"smooth": True}),
   ("IMG_9200", 4.8, 1.8, "riding to medical college every morning", {"transpose": 1, "fit": True, "smooth": True}),
   ("IMG_6261", 0.0, 1.0, "this name on your ID card", {"smooth": True}),
   ("IMG_8785", 2.2, 2.2, "that's why 🤍", {"transpose": 1, "fit": True, "smooth": True})],
 "10_your_sign": [
   ("F1D19DE4", 0.0, 2.2, "NEET aspirant, this is your sign to open the book again", {"smooth": True}),
   ("studyclip", 4.6, 1.8, "one chapter today", {}),
   ("IMG_1366", 1.03, 1.6, "one concept clear", {}),
   ("MeinLAB", 14.0, 1.8, "one step closer to the coat", {}),
   ("IMG_0773", 3.85, 1.9, "go study. you've got this 🤍", {"smooth": True})],
}
import glob, subprocess
A = "/tmp/claude-0/-home-user-Claude-code-git-hub/63355ac8-e737-5185-a230-1c95badec4de/scratchpad/assets/money spent"
def clip_len(stem):
    p = glob.glob(f"{A}/**/{stem}*", recursive=True)[0]
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
STRETCH = 1.3
for name, shots in V.items():
    t = 0.0; out = []
    for i, (src, sin, d, txt, ex) in enumerate(shots):
        last = i == len(shots) - 1
        room = clip_len(src) - sin - (0.05 if last else 0.35)      # never run past the clip (no frozen frames)
        d = round(min(d * STRETCH, room), 2)
        sh = {"t": round(t, 2), "src": src, "in": sin, "text": txt}; sh.update(ex); out.append(sh); t += d
    turn = round(out[2]["t"], 2)
    open(f"{name}.py", "w").write(f"# NEET-aspirant batch video {name}\n" + HEAD.format(end=round(t, 2), shots=repr(out).replace("}, {", "},\n    {"), turn=turn))
    print(name, "END", round(t, 2))
