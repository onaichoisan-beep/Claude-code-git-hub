// "That night ... a giant clock in the middle of the room."  41.9 - 60.6
const S = B.stage(CV, { bloom: 0.95, threshold: 0.95, exposure: 1.1, vig: 0.45 });
const cam = S.cam;
// --- exterior at night ---
const ext = S.scene;
B.sky(ext, "#0a0f2e", "#2a3a78", "#3a4a88");
ext.fog = new T.Fog(0x1a2450, 70, 220);
const L = B.lights(ext, { sun: 1.4, hemi: 0.55, sunColor: 0x9fb4ff, sky: 0x5a6aff, ground: 0x10162a, sunPos: [-30, 50, 25] });
const town = B.town(ext, { night: true });
const moon = new T.Mesh(new T.SphereGeometry(6, 32, 16), new T.MeshBasicMaterial({ color: new T.Color("#fff6dc").multiplyScalar(2.4), fog: false }));
moon.position.set(-40, 70, -180);
ext.add(moon);
const leoX = B.cast("leo"), miaX = B.cast("mia");
[leoX, miaX].forEach((p) => { p.root.rotation.y = Math.PI; ext.add(p.root); });
leoX.setScreen({ big: "1", sub: "DAY", color: B.RED });
// --- interior ---
const inn = new T.Scene();
const I = B.interior(inn);
const leo = B.cast("leo", { face: "shock" }), mia = B.cast("mia", { face: "shock" });
leo.root.position.set(1.0, 0, 15);
mia.root.position.set(-1.0, 0, 15.5);
[leo, mia].forEach((p) => { p.root.rotation.y = Math.PI; inn.add(p.root); });
leo.setScreen({ big: "1", sub: "DAY", color: B.RED });
I.named.LEO.sandM.color.set("#ff6a3a").multiplyScalar(2.6);

let streamAmt = 0;
const shots = B.shots([
  { at: 41.9, f: (lt, k, d, t) => { // "That night, Mia and I snuck into the clock tower."
    S.setScene(ext);
    const z = -50 - lt * 2.2;
    leoX.root.position.set(0.9, 0, z);
    miaX.root.position.set(-0.9, 0, z - 0.4);
    leoX.pose({ walk: t * 7, walkAmt: 0.7, lean: 0.25, pitch: -0.2 });
    miaX.pose({ walk: t * 7 + 1.5, walkAmt: 0.7, lean: 0.25, pitch: -0.2 });
    B.camMove(cam, [3.2, 2.6, -40], [2.4, 2.8, -44], [0, 7, -72], [0, 9, -72], B.inOut(k), 48);
    B.aimSun(L.sun, 0, 0, -60);
  } },
  { at: 44.85, f: (lt, k, d, t) => { // "Inside, thousands of glowing hourglasses floated in the air." - crane up
    S.setScene(inn);
    streamAmt = 0;
    leo.setFace("shock"); mia.setFace("shock");
    leo.pose({ pitch: -0.35 }); mia.pose({ pitch: -0.35, armL: 0.6 });
    B.camMove(cam, [0, 2.4, 21], [0, 9.5, 23], [0, 4, 8], [0, 10, 0], B.inOut(k), 50);
  } },
  { at: 48.95, f: (lt, k, d, t) => { // "One for every person in town." - glide through the hourglasses
    S.setScene(inn);
    const a = 0.3 + k * 0.9;
    B.camAt(cam, [Math.sin(a) * 15, 9 + k * 2, Math.cos(a) * 15], [0, 9, 0], 48);
  } },
  { at: 51.1, f: (lt, k, d, t) => { // "Each one had a name on it." - tags BOB / ROSA / MAX
    S.setScene(inn);
    B.camMove(cam, [-3.6, 3.4, 14.4], [0.6, 3.3, 14.0], [-3.6, 3.3, 8.6], [0.6, 3.2, 8.6], B.inOut(k), 38);
  } },
  { at: 52.55, f: (lt, k, d, t) => { // "Mine was almost empty." - LEO's glass, push in
    S.setScene(inn);
    I.named.LEO.setFill(0.035 + Math.sin(t * 8) * 0.004);
    B.camMove(cam, [4.4, 4.2, 15.2], [3.9, 4.3, 13.0], [3.6, 4.0, 8.4], [3.6, 4.1, 8.4], B.outCubic(k), 34);
  } },
  { at: 53.85, f: (lt, k, d, t) => { // "A thin golden stream was pouring out of every hourglass"
    S.setScene(inn);
    streamAmt = B.smooth(B.seg(t, 54.0, 56.5));
    B.camMove(cam, [-6, 5, 16], [-3, 7, 10], [0, 7, 0], [0, 9, -6], B.inOut(k), 46);
  } },
  { at: 57.45, f: (lt, k, d, t) => { // "straight into a giant clock in the middle of the room."
    S.setScene(inn);
    streamAmt = 1;
    const reveal = B.inOut(k);
    B.camMove(cam, [1.5, 2.0, 8], [0.5, 3.0, 4.5], [0, 8, -10], [0, 10, -10], reveal, 52);
  } },
], 60.6);

function render(t) {
  town.tower.setTime(11, 50);
  I.animate(t);
  I.streams.update(t, 0.32, streamAmt);
  shots(t);
  S.render();
}
