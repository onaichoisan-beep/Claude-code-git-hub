# "6 years in 15 seconds" - slow build, beat drop at 5.4 s, ~0.4 s montage, slow ending.
DROP = 5.4
END = 16.5
F = 0.4  # montage shot length
montage = [("IMG_0396", 0), ("67168F2A", 2.6), ("IMG_4318", 1.5), ("IMG_1366", 1.0), ("IMG_1480", 2.0),
           ("IMG_9200", 1.0), ("FFC484C5", 0.2), ("IMG_9242", 3.0), ("IMG_0959", 6.0), ("E56BD187", 0.5),
           ("IMG_6393", 2.45), ("IMG_1364", 0.5), ("IMG_9323", 2.6), ("2A473245", 1.0), ("IMG_8307", 15.5),
           ("26EEAFDA", 3.5), ("IMG_1510", 1.0), ("IMG_2134", 0.3), ("IMG_6575", 1.0), ("IMG_6261", 1.0)]
SHOTS = [
    {"t": 0.0, "src": "IMG_6261", "in": 0.2, "text": "they said MBBS is 6 years."},
    {"t": 1.8, "src": "IMG_6262", "in": 0.3, "text": "here's year 1 👇"},
    {"t": 3.6, "src": "IMG_6263", "in": 0.2, "text": "here's year 1 👇"},
]
for k, (src, sin) in enumerate(montage):
    shot = {"t": round(DROP + k * F, 2), "src": src, "in": sin}
    if src == "IMG_9200": shot.update({"transpose": 1, "cx": 0.62})
    if src == "IMG_0396": shot["zoom"] = 0.15
    SHOTS.append(shot)
SHOTS.append({"t": round(DROP + len(montage) * F, 2), "src": "IMG_9328", "in": 1.0, "text": "5 more to go."})
