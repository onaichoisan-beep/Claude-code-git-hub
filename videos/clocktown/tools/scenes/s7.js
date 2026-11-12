// "I spotted a huge lever ... back into every house in town."  76.15 - 91.2
const S = B.stage(CV, { bloom: 1.0, threshold: 0.95, exposure: 1.1, vig: 0.45 });
const cam = S.cam;
const inn = S.scene;
const I = B.interior(inn);
const leo = B.cast("leo", { face: "determined" });
inn.add(leo.root);
const wrist = B.wristProp({ sleeve: "#d94c3d" });
wrist.group.scale.setScalar(0.45);
wrist.group.position.set(14, 3.2, 6);
wrist.group.rotation.set(0.08, -0.9, 0.05);
inn.add(wrist.group);
const sparks = B.streams(Array.from({ length: 40 }, (_, i) => {
  const a = (i / 40) * Math.PI * 2;
  const o = [6.8, 16.5, -11.8];
  return { a: o, b: [o[0] + Math.cos(a) * 5, o[1] - 6 + Math.sin(a) * 2, o[2] + 3 + Math.sin(a * 3) * 2], c: [o[0] + Math.cos(a) * 3, o[1] + 2 + Math.sin(a) * 2, o[2] + 2] };
}), 3, "#ffb04a", 0.22);
inn.add(sparks.points);
// exterior for the last shot
const ext = new T.Scene();
B.sky(ext, "#0a0f2e", "#2a3a78", "#3a4a88");
ext.fog = new T.Fog(0x1a2450, 80, 240);
ext.add(new T.HemisphereLight(0x5a6aff, 0x10162a, 0.6));
const moonL = new T.DirectionalLight(0x9fb4ff, 1.2);
moonL.position.set(-30, 50, 25);
ext.add(moonL);
const town = B.town(ext, { night: true });
town.houses.forEach((h) => h.userData.winMat.color.set("#3a4a7a"));
const tops = [0, 27, -72];
const houseCurves = town.houses.map((h) => {
  const p = h.position;
  return { a: tops, b: [p.x, 3.4, p.z], c: [(p.x) * 0.6, 34, (p.z - 72) / 2] };
});
const goldStreams = B.streams(houseCurves, 34, "#ffc23a", 0.7);
ext.add(goldStreams.points);

function gearAngle(t) {
  const base = (x) => x * 0.6 + Math.max(0, x - 72.9) * 0.9;
  if (t < 82.7) return base(t);
  const v = 1.5, tau = Math.min(1, t - 82.7);
  return base(82.7) + v * (tau - (tau * tau) / 2);
}
let flip = 0, reverse = false, streamAmt = 1;
const shots = B.shots([
  { at: 76.15, f: (lt, k, d, t) => { // "I spotted a huge lever beside the giant clock."
    S.setScene(inn);
    leo.root.position.set(2.5, 0, 5);
    leo.root.rotation.y = Math.PI + 0.55;
    leo.setFace("determined");
    I.knob.material.emissiveIntensity = 1.6 + Math.sin(t * 8) * 1.2;
    B.camMove(cam, [1.0, 4.9, 9.5], [3.4, 4.0, 3.2], [7.5, 2.8, -4], [7.5, 2.8, -4], B.inOut(k), 40);
  } },
  { at: 79.3, f: (lt, k, d, t) => { // "Three seconds."
    const pulse = 1 - B.seg(t, 79.4, 79.8);
    wrist.set({ big: "3", sub: "SECONDS", color: B.RED }, 1.2 + pulse * 2);
    B.camMove(cam, [11.6, 3.5, 8.3], [11.95, 3.4, 8.0], [13.65, 3.2, 6.62], [13.65, 3.2, 6.62], B.inOut(k), 34);
  } },
  { at: 80.45, f: (lt, k, d, t) => { // "I jumped and pulled it with everything I had."
    S.setScene(inn);
    const jump = B.seg(t, 80.55, 81.05);
    const pull = B.inOut(B.seg(t, 81.0, 81.9));
    I.lever.rotation.z = B.lerp(0.6, -0.9, pull);
    const kx = 7.5 - Math.sin(I.lever.rotation.z) * 3.7, ky = 1.4 + Math.cos(I.lever.rotation.z) * 3.7;
    leo.root.position.set(B.lerp(4.8, kx + 0.2, B.smooth(jump)), Math.max(0, Math.sin(Math.min(jump, 1) * Math.PI * 0.75) * 1.6 * (1 - pull) + (ky - 4.0) * pull * (1 - B.seg(t, 81.9, 82.2))), -2.4);
    leo.root.rotation.y = Math.PI * 0.95;
    leo.setFace(t < 81.0 ? "determined" : "scream");
    leo.pose({ armL: 2.9 * B.smooth(B.seg(t, 80.5, 80.8)), armR: 2.9 * B.smooth(B.seg(t, 80.5, 80.8)), lean: -0.1 });
    B.camMove(cam, [9.5, 3.0, 7.0], [8.8, 3.4, 5.5], [6.4, 3.4, -3], [6.4, 3.0, -3], B.inOut(k), 42);
    if (t > 81.75) { const sh = Math.max(0, 1 - (t - 81.75) * 3) * 0.18; cam.position.y += Math.sin(t * 70) * sh; }
  } },
  { at: 82.6, f: (lt, k, d, t) => { // "The gears screeched to a stop."
    S.setScene(inn);
    I.lever.rotation.z = -0.9;
    sparks.mat.opacity = t < 83.8 ? 1 : Math.max(0, 1 - (t - 83.8) * 2);
    sparks.update(t, 1.4, 1);
    const sh = t < 83.7 ? 0.08 : Math.max(0, 0.08 - (t - 83.7) * 0.2);
    B.camMove(cam, [3.5, 13.5, -4], [4.2, 14.2, -5.5], [6.8, 16.5, -12.4], [6.8, 16.3, -12.4], B.inOut(k), 44);
    cam.position.x += Math.sin(t * 80) * sh;
  } },
  { at: 84.35, f: (lt, k, d, t) => { // "Every hourglass flipped upside down."
    S.setScene(inn);
    I.lever.rotation.z = -0.9;
    flip = B.seg(t, 84.9, 86.4);
    reverse = flip > 0.5;
    streamAmt = flip > 0.5 ? B.seg(t, 85.6, 86.6) : 0;
    B.camMove(cam, [0, 7, 21], [0, 9, 17], [0, 9, 0], [0, 10, 0], B.inOut(k), 52);
  } },
  { at: 86.95, f: (lt, k, d, t) => { // "The golden time poured out of the tower, back into every house in town."
    S.setScene(ext);
    const amt = B.seg(t, 87.0, 89.2);
    goldStreams.update(t, 0.45, amt);
    town.houses.forEach((h, i) => {
      const lit = B.smooth(B.seg(t, 88.0 + (i % 7) * 0.22, 88.6 + (i % 7) * 0.22));
      h.userData.winMat.color.set("#3a4a7a").lerp(new T.Color("#ffc23a"), lit).multiplyScalar(1 + lit * 2.5);
    });
    B.camMove(cam, [14, 34, 30], [10, 30, 22], [0, 10, -45], [0, 8, -40], B.inOut(k), 50);
  } },
], 91.2);

function render(t) {
  wrist.group.visible = (t >= 79.3 && t < 80.45);
  flip = 0; reverse = false; streamAmt = 0;
  I.lever.rotation.z = 0.6;
  shots(t);
  I.animate(t, { gearAngle: gearAngle(t), flip: flip > 0 ? flip : undefined, m: t > 82.7 ? 59 : undefined });
  I.streams.update(t, 0.32, t < 82.7 ? 1 : streamAmt, reverse);
  if (t < 82.6) sparks.update(t, 1.4, 0);
  S.render();
}
