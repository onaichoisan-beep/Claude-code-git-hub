"""Cue plans for the 10 clips (times are seconds in each tightened clip). Writes plans/clipNN.json."""
import json, os

L, R = 380, 1540          # icon columns left / right of the head
TOP, LOW = 400, 700        # icon rows

P = {
 "06": dict(keys={"80000": "money", "mbbs": "red", "too.": "red"}, fix={"80000": "₹80,000", "7k": "₹7K", "8k": "₹8K"}, cues=[
    dict(type="bh", t=0.85, d=1.55, text="80,000", style="money", matte="a"),
    dict(type="pop", t=2.2, d=1.4, x=L, y=TOP, icon="steth", label="1ST YEAR MBBS", tile="red"),
    dict(type="glitch", t=3.5),
    dict(type="broll", t=3.55, d=2.1, img="assets/stock/rupees.jpg", big="₹7K–8K", bigStyle="money", small="every month", nocaps=True),
    dict(type="flash", t=5.62),
  ], zoom=[[0, 1.0], [2.2, 1.16], [5.65, 1.0], [5.75, 1.3, "ease"]]),

 "07": dict(keys={"rishish": "red", "student": "red"}, cues=[
    dict(type="l3", t=0.6, d=1.7, name="Rishish", role="1st year MBBS · medico"),
    dict(type="broll", t=2.3, d=1.25, img="assets/stock/steth.jpg", small="still a first-year medico", nocaps=True),
    dict(type="note", t=3.75, d=1.6, x=1180, y=230, text="results pending…", arrow="left"),
    dict(type="bh", t=5.75, d=1.5, text="FOR YOU", style="chrome", matte="a"),
    dict(type="pop", t=7.75, d=1.5, x=R, y=TOP, icon="rupee", label="EARN AS A STUDENT", tile="red"),
  ]),

 "08": dict(keys={"ajeeb": "red", "4": "red", "trusted.": "money", "easy.": "money"}, cues=[
    dict(type="pop", t=2.55, d=1.5, x=L, y=TOP, icon="home", label="GHAR SE"),
    dict(type="pop", t=2.9, d=1.15, x=R, y=TOP, icon="rupee", label="PAISE"),
    dict(type="note", t=6.85, d=1.2, x=1200, y=250, text="thoda ajeeb…", arrow="left"),
    dict(type="bh", t=9.4, d=2.2, text="4 EASY WAYS", style="red", matte="a"),
    dict(type="pop", t=13.7, d=1.6, x=L, y=TOP, icon="check", label="TRUSTED", tile="red"),
    dict(type="pop", t=14.5, d=0.95, x=R, y=TOP, icon="zap", label="EASY"),
  ]),

 "09": dict(keys={"doomscrolling": "red", "money.": "money"}, cues=[
    dict(type="phone", t=1.9, d=1.45, minutes=462),
    dict(type="bh", t=3.45, d=1.75, text="7+ HOURS", style="white", matte="a"),
    dict(type="broll", t=5.25, d=2.3, img="assets/stock/phone.jpg", big="= MONEY", bigStyle="money", size=260),
  ]),

 "10": dict(keys={"experiences": "red", "skills.": "red"}, cues=[
    dict(type="glitch", t=4.35),
    dict(type="broll", t=5.5, d=1.9, big="7+ HRS", small="of doomscrolling", nocaps=True),
    dict(type="pop", t=8.0, d=1.4, x=L, y=TOP, icon="laptop", label="LEARN"),
    dict(type="pop", t=9.2, d=1.6, x=R, y=TOP, icon="brain", label="SKILLS", tile="red"),
    dict(type="pop", t=11.7, d=1.25, x=L, y=TOP, icon="trending", label="GET BETTER"),
    dict(type="pop", t=13.55, d=0.75, x=R, y=TOP, icon="rupee", label="CHARGE MORE"),
    dict(type="bh", t=15.55, d=0.95, text="MORE SKILL", style="white", matte="a"),
    dict(type="bh", t=16.5, d=0.95, text="MORE MONEY", style="money", matte="b"),
    dict(type="bh", t=17.45, d=0.85, text="BETTER SKILL", style="chrome", matte="c"),
  ]),

 "01": dict(keys={"60k": "money", "faceless": "red", "telegram,": "red"}, cues=[
    dict(type="chapter", t=0.0, d=2.0, num="01", title="UGC Content Creation", sub="User-generated content for brands"),
    dict(type="table", t=2.0, d=1.75, active=1),
    dict(type="bh", t=3.8, d=1.6, text="₹60K+", style="money", matte="a"),
    dict(type="proof", t=5.5, d=2.0, img="assets/proof/payment-7000.jpg", caption="UGC payout", stamp="PAID"),
    dict(type="pop", t=7.6, d=1.6, x=R, y=TOP, icon="eyeoff", label="FACELESS", tile="red"),
    dict(type="glitch", t=9.3),
    dict(type="broll", t=9.35, d=3.5, img="assets/stock/unboxing.jpg", big="UGC", small="content you make for brands"),
    dict(type="pop", t=15.95, d=3.4, x=L, y=TOP, icon="cpu", label="TECH UGC"),
    dict(type="pop", t=17.25, d=2.1, x=R, y=TOP, icon="tag", label="BRAND UGC"),
    dict(type="pop", t=18.15, d=1.2, x=R, y=LOW, icon="link", label="AFFILIATE UGC"),
    dict(type="pop", t=20.25, d=1.6, x=L, y=TOP, icon="trending", label="PAGE GROWS"),
    dict(type="note", t=22.0, d=1.4, x=1180, y=260, text="charge more ↑", color="money", arrow="left"),
    dict(type="pop", t=25.4, d=4.6, x=R, y=TOP, icon="send", label="JOIN TELEGRAM", tile="red"),
    dict(type="pop", t=31.65, d=1.6, x=L, y=TOP, icon="refresh", label="RESELL"),
    dict(type="pop", t=33.55, d=1.4, x=R, y=TOP, icon="gift", label="OR USE THEM"),
    dict(type="bh", t=38.4, d=1.65, text="EARN MORE", style="money", matte="b"),
  ]),

 "02": dict(keys={"viral": "red", "800": "money", "monetized.": "red"}, fix={"25": "2025", "oswal": "Oswaal"}, cues=[
    dict(type="chapter", t=0.0, d=2.2, num="02", title="Content Creation", sub="Grow a page, land brand deals"),
    dict(type="table", t=2.2, d=1.8, active=2),
    dict(type="note", t=4.1, d=1.5, x=1180, y=250, text="after NEET 2025", arrow="left"),
    dict(type="glitch", t=8.5),
    dict(type="broll", t=8.55, d=2.2, img="assets/stock/creator.jpg", big="1 VIRAL VIDEO", size=230),
    dict(type="bh", t=11.5, d=1.6, text="800 SUBS", style="white", matte="a"),
    dict(type="proof", t=14.6, d=2.9, img="assets/proof/payment-10000.jpg", caption="First paid collab", stamp="PAID"),
    dict(type="note", t=17.55, d=1.3, x=1180, y=250, text="not even monetized!", color="red", arrow="left"),
    dict(type="pop", t=21.9, d=3.0, x=L, y=TOP, logo="assets/proof/neetprep.jpg", label="NEETprep"),
    dict(type="pop", t=22.65, d=2.25, x=R, y=TOP, logo="assets/proof/oswaal.jpg", label="OSWAAL BOOKS"),
    dict(type="note", t=24.4, d=1.5, x=800, y=110, text="they pay well", color="money"),
    dict(type="pop", t=26.3, d=1.6, x=L, y=TOP, icon="gift", label="FREE ACCESS"),
    dict(type="pop", t=29.8, d=1.3, x=R, y=TOP, icon="book", label="FREE BOOKS"),
    dict(type="pop", t=30.8, d=1.4, x=L, y=TOP, icon="heart", label="GIVEAWAY", tile="red"),
  ]),

 "03": dict(keys={"knowledge": "red", "investments.": "red", "money.": "money"}, cues=[
    dict(type="chapter", t=0.0, d=2.0, num="03", title="Online Tutoring", sub="Sell what you already know"),
    dict(type="table", t=2.0, d=1.7, active=3),
    dict(type="pop", t=4.5, d=2.2, x=L, y=TOP, icon="users", label="MY FRIEND · GMC"),
    dict(type="broll", t=6.85, d=2.6, img="assets/stock/teacher.jpg", small="teaching NEET aspirants"),
    dict(type="pop", t=12.4, d=1.0, x=R, y=TOP, icon="rupee", label="PAID", tile="red"),
    dict(type="bh", t=14.15, d=1.6, text="KNOWLEDGE", style="chrome", matte="a"),
    dict(type="broll", t=17.3, d=1.75, big="₹0", bigStyle="money", small="investment needed", nocaps=True),
    dict(type="pop", t=25.6, d=2.0, x=L, y=TOP, icon="school", label="LOCAL COACHING"),
    dict(type="note", t=27.5, d=1.6, x=1180, y=250, text="value your knowledge", arrow="left"),
    dict(type="bh", t=29.75, d=1.45, text="DECENT MONEY", style="money", matte="b"),
  ]),

 "04": dict(keys={"freelancing": "red", "-4k": "money"}, fix={"-4k": "₹3–4K", "3": ""}, cues=[
    dict(type="chapter", t=0.0, d=2.3, num="04", title="Freelancing", sub="Video editing for creators"),
    dict(type="table", t=2.3, d=1.8, active=4),
    dict(type="pop", t=5.1, d=1.7, x=L, y=TOP, icon="scissors", label="EDITOR"),
    dict(type="glitch", t=6.85),
    dict(type="timeline", t=6.9, d=2.4, big="₹3–4K", small="per video"),
    dict(type="pop", t=12.3, d=1.6, x=R, y=TOP, icon="trending", label="PRACTICE"),
    dict(type="bh", t=17.9, d=1.1, text="CHARGE MORE", style="money", matte="a"),
    dict(type="pop", t=21.75, d=1.6, x=L, y=TOP, icon="chat", label="DM CREATORS"),
    dict(type="pop", t=24.0, d=1.35, x=R, y=TOP, icon="play", label="DM YOUTUBERS", tile="red"),
    dict(type="pop", t=25.4, d=1.6, x=L, y=TOP, icon="film", label="SEND SAMPLES"),
    dict(type="bh", t=27.9, d=1.7, text="FREELANCING", style="red", matte="b"),
  ]),

 "05": dict(keys={"education.": "red", "consistent.": "red"}, cues=[
    dict(type="bh", t=0.9, d=1.2, text="NO AGE LIMIT", style="white", matte="a"),
    dict(type="pop", t=5.35, d=1.9, x=R, y=TOP, icon="grad", label="EDUCATION FIRST", tile="red"),
    dict(type="pop", t=8.8, d=2.0, x=L, y=TOP, icon="brain", label="BETTER SKILLS"),
    dict(type="pop", t=11.55, d=1.5, x=L, y=TOP, icon="check", label="STAY TRUE"),
    dict(type="pop", t=13.75, d=0.85, x=R, y=TOP, icon="zap", label="CONSISTENT", tile="red"),
    dict(type="flash", t=14.55),
  ], zoom=[[0, 1.0], [2.0, 1.16], [5.4, 1.0], [7.2, 1.22], [11.4, 1.0], [14.55, 1.12], [14.6, 1.3, "ease"]]),
}

os.makedirs("plans", exist_ok=True)
for n, p in P.items():
    cuts = json.load(open(f"../work/base/clip{n}.cuts.json"))
    p.update(id=f"clip{n}", video=f"assets/video/clip{n}.mp4", words=f"../work/base/clip{n}.words.json",
             duration=cuts["duration"])
    json.dump(p, open(f"plans/clip{n}.json", "w"), indent=1, ensure_ascii=False)
    print("plan", n, len(p["cues"]), "cues")
