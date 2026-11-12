// "The next morning ... I was never born in this town."  102.8 - 122.0
const S = B.stage(CV, { bloom: 0.7, threshold: 1.05, exposure: 1.05 });
const { scene, cam } = S;
B.sky(scene, "#5f8fe6", "#ffb48a", "#ffd6b0");
scene.fog = new T.Fog(0xffc8a0, 100, 260);
const L = B.lights(scene, { sun: 3.2, hemi: 1.3, sunColor: 0xffc890, sky: 0xffe2c8, sunPos: [-40, 30, -10] });
B.town(scene, {});
const leo = B.cast("leo", { face: "happy" });
leo.root.position.set(1.0, 0, 6);
leo.root.rotation.y = -0.35;
scene.add(leo.root);
leo.setScreen({ big: "75", sub: "YEARS", color: "#59ff9a" });
const mia = B.cast("mia", { face: "smile" });
mia.root.position.set(-1.0, 0, 6);
mia.root.rotation.y = 0.35;
scene.add(mia.root);
mia.setScreen({ blank: true });
const baker = B.cast("baker", { face: "happy" });
baker.root.position.set(-4.4, 0, -3);
baker.root.rotation.y = 1.1;
const mail = B.cast("mailman", { face: "happy" });
mail.root.position.set(-2.2, 0, -3.2);
mail.root.rotation.y = -1.1;
[baker, mail].forEach((p) => scene.add(p.root));
B.addHolo(baker, "62 YEARS", B.GREEN);
B.addHolo(mail, "58 YEARS", B.GREEN);
const yrs = ["70 YEARS", "68 YEARS", "74 YEARS", "71 YEARS", "69 YEARS", "73 YEARS"];
const kids = yrs.map((d, i) => {
  const p = B.kid(i, { face: "happy" });
  p.root.position.set(-6 + i * 2.4, 0, -14 - (i % 2) * 1.2);
  scene.add(p.root);
  B.addHolo(p, d, B.GREEN);
  return p;
});
const crowd = Array.from({ length: 10 }, (_, i) => {
  const p = B.person({ shirt: ["#3f7fd9", "#c74a8a", "#5bbf8a", "#e9a23b", "#9a7bd1"][i % 5], hair: ["short", "bob", "pony", "bald", "bun"][i % 5], hairColor: ["#2b1d14", "#1b1414", "#c4572b", "#888", "#ddd"][i % 5], skin: ["#f4c89f", "#8d5a3b", "#c98d5e", "#eab993", "#a8724a"][i % 5], face: "happy" });
  p.root.position.set((i % 2 ? 1 : -1) * (2 + (i % 3) * 1.6), 0, -24 - i * 2.6);
  p.root.rotation.y = (i % 2 ? -1 : 1) * 0.8;
  scene.add(p.root);
  B.addHolo(p, (60 + ((i * 7) % 20)) + " YEARS", B.GREEN);
  return p;
});
const wrist = B.wristProp({ sleeve: "#7b5cd6", skin: "#eab993" });
wrist.group.scale.setScalar(0.45);
wrist.group.position.set(-0.4, 3.4, 46);
wrist.group.rotation.set(0.08, 0.3, -0.05);
scene.add(wrist.group);
wrist.set({ blank: true }, 1);
let look = [1.05, 0, [1, 1, 1]];
const shots = B.shots([
  { at: 102.8, f: (lt, k, d, t) => { // "The next morning, the whole town was outside,"
    B.camMove(cam, [10, 15, 16], [7, 12, 10], [0, 2, -20], [0, 2, -22], B.inOut(k), 46);
    B.aimSun(L.sun, 0, 0, -15, [-40, 30, -10]);
  } },
  { at: 105.4, f: (lt, k, d, t) => { // "laughing and comparing clocks."
    baker.pose({ armL: 1.6, armLz: -0.3, jump: Math.abs(Math.sin(t * 8)) * 0.15, pitch: -0.1 });
    mail.pose({ armL: 1.6, armLz: -0.3, jump: Math.abs(Math.sin(t * 8 + 1)) * 0.15, pitch: -0.1 });
    B.camMove(cam, [-3.3, 3.2, 2.2], [-3.3, 3.3, 1.2], [-3.3, 2.8, -3.1], [-3.3, 3.0, -3.1], B.inOut(k), 42);
    B.aimSun(L.sun, -3, 0, -3, [-40, 30, -10]);
  } },
  { at: 107.6, f: (lt, k, d, t) => { // "Everyone had their years back."
    B.camMove(cam, [-7, 3.0, -6], [5, 3.3, -6.5], [-5, 2.8, -14.5], [5, 2.8, -14.5], B.inOut(k), 42);
    B.aimSun(L.sun, 0, 0, -14, [-40, 30, -10]);
  } },
  { at: 109.3, f: (lt, k, d, t) => { // "I thought it was over."
    leo.setFace("happy"); mia.setFace("smile");
    B.camMove(cam, [0, 3.0, 13.5], [0, 2.95, 12.0], [0, 2.6, 6], [0, 2.6, 6], B.inOut(k), 38);
    B.aimSun(L.sun, 0, 0, 6, [-40, 30, -10]);
  } },
  { at: 110.55, f: (lt, k, d, t) => { // "Until I looked at Mia's wrist." - tilt down to her arm
    leo.setFace("neutral");
    leo.pose({ pitch: 0.3, yaw: 0.4 });
    mia.pose({ armL: 0.5 });
    B.camMove(cam, [0.4, 3.2, 10], [0.4, 1.9, 7.9], [-0.4, 2.8, 6], [-0.25, 1.35, 6.3], B.inOut(k), 32);
  } },
  { at: 112.15, f: (lt, k, d, t) => { // "Her clock was blank."
    look = [0.95, 0, [0.92, 0.97, 1.1]];
    B.camMove(cam, [0.6, 4.3, 52.5], [0.2, 3.9, 50.5], [-0.25, 3.4, 46], [-0.25, 3.4, 46], B.inOut(k), 32);
  } },
  { at: 113.95, f: (lt, k, d, t) => { // "No numbers. Nothing."
    look = [0.85, 0, [0.88, 0.95, 1.12]];
    wrist.set({ blank: true }, Math.floor(t * 9) % 5 === 0 ? 1.6 : 1);
    B.camMove(cam, [0.05, 3.75, 49.2], [-0.05, 3.6, 48.5], [-0.25, 3.4, 46], [-0.25, 3.4, 46], B.inOut(k), 30);
  } },
  { at: 115.5, f: (lt, k, d, t) => { // "She just smiled at me and whispered,"
    look = [0.8, 0, [0.85, 0.93, 1.15]];
    mia.root.rotation.y = 0.35;
    mia.setFace("eerie");
    mia.pose({ tilt: 0.12 * B.smooth(B.seg(lt, 0, 1)) });
    B.camMove(cam, [-0.2, 3.1, 10.2], [-0.4, 3.0, 9.4], [-1.0, 2.75, 6], [-1.0, 2.8, 6], B.inOut(k), 34);
  } },
  { at: 117.5, f: (lt, k, d, t) => { // "Leo, I was never born in this town."
    const dark = B.seg(t, 117.5, 120.5);
    const end = B.seg(t, 121.0, 122.0);
    look = [B.lerp(0.8, 0.6, dark) * (1 - end), 0, [0.82, 0.92, 1.18]];
    mia.setFace("eerie");
    mia.pose({ tilt: 0.12 });
    mia.setEyeGlow(B.smooth(B.seg(t, 118.75, 119.6)));
    B.camMove(cam, [-0.4, 2.95, 9.6], [-0.82, 2.88, 8.5], [-1.0, 2.88, 6], [-1.0, 2.88, 6], B.inOut(B.seg(t, 117.5, 121.0)), 34);
  } },
], 122.0);

function render(t) {
  look = [1.05, 0, [1, 1, 1]];
  mia.setEyeGlow(0);
  mia.setFace("smile");
  leo.pose({}); mia.pose({});
  kids.concat(crowd).forEach((p, i) => {
    p.pose({ armL: 2.6, armR: 2.6, armLz: 0.3, armRz: 0.3, jump: Math.abs(Math.sin(t * 6 + i)) * 0.35 });
    p.holo.position.y = 3.6 + Math.sin(t * 2 + i) * 0.06;
  });
  baker.pose({}); mail.pose({});
  wrist.group.visible = t >= 112.15 && t < 115.5;
  shots(t);
  S.setLook(look[0], look[1], look[2]);
  S.render();
}
