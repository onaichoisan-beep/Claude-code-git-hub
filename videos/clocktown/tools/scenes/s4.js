// "Then I noticed something strange ... nine hundred years."  31.3 - 41.9  (town square, golden hour)
const S = B.stage(CV, { bloom: 0.75, threshold: 1.05, exposure: 1.05 });
const { scene, cam } = S;
B.sky(scene, "#4a6fc9", "#ffb27a", "#ffd2a0");
scene.fog = new T.Fog(0xffc89a, 90, 240);
const L = B.lights(scene, { sun: 3.4, hemi: 1.1, sunColor: 0xffb070, sky: 0xffd9b0, ground: 0x6b5a4a, sunPos: [40, 30, 20], shadowSize: 30 });
const town = B.town(scene, {});
const tw = town.tower;
const leo = B.cast("leo", { face: "worried" });
leo.root.position.set(2, 0, -50);
leo.root.rotation.y = Math.PI;
scene.add(leo.root);
leo.setScreen({ big: "1", sub: "DAY", color: B.RED });
// crowd in the square
const before = ["12 DAYS", "9 DAYS", "20 DAYS", "7 DAYS", "15 DAYS", "10 DAYS", "8 DAYS"];
const after = ["11 DAYS", "8 DAYS", "19 DAYS", "6 DAYS", "14 DAYS", "9 DAYS", "7 DAYS"];
const crowd = before.map((d, i) => {
  const p = i < 3 ? B.kid(i + 2, { face: "smile" }) : B.person({ shirt: ["#3f7fd9", "#c74a8a", "#5bbf8a", "#e9a23b"][i % 4], hair: ["short", "bob", "pony", "bald"][i % 4], hairColor: ["#2b1d14", "#1b1414", "#c4572b", "#888"][i % 4], skin: ["#f4c89f", "#8d5a3b", "#c98d5e", "#eab993"][i % 4], face: "smile" });
  const a = -0.9 + i * 0.3;
  p.root.position.set(Math.sin(a) * 9, 0, -60 + Math.cos(a) * 4 - 2);
  p.root.rotation.y = Math.PI + a * 0.4;
  scene.add(p.root);
  B.addHolo(p, d, "#ff8a4a");
  return p;
});
// mayor on a little stage in front of the tower
const stage = B.box(7, 0.8, 3.4, B.mat("#8a2a3a"), 0, 0.4, -66.3, 0.1);
scene.add(stage);
scene.add(B.box(7.4, 0.2, 3.8, B.mat("#e0b23c", { p: { metalness: 0.7, roughness: 0.3 } }), 0, 0.85, -66.3));
const mayor = B.cast("mayor");
mayor.root.position.set(0, 0.9, -66.2);
scene.add(mayor.root);
const mh = B.addHolo(mayor, "899 YEARS", B.GOLD, 3.8);
const spot = new T.SpotLight(0xffe0a0, 90, 30, 0.35, 0.5, 1.5);
spot.position.set(0, 12, -56);
spot.target.position.set(0, 2, -66);
scene.add(spot, spot.target);
// bell shockwave
const wave = new T.Mesh(new T.TorusGeometry(1, 0.12, 8, 64), new T.MeshBasicMaterial({ color: new T.Color("#ffd27a").multiplyScalar(3), transparent: true, opacity: 0 }));
wave.position.set(0, 25, -72);
scene.add(wave);

const shots = B.shots([
  { at: 31.3, f: (lt, k, d, t) => { // "Then I noticed something strange."
    leo.setFace(t < 32.1 ? "worried" : "determined");
    leo.pose({ tilt: t < 32.1 ? 0 : 0.12, yaw: Math.sin(t * 1.4) * 0.1 });
    B.camMove(cam, [2.6, 3.0, -54.6], [2.4, 2.95, -53.8], [2.0, 2.8, -50], [2.0, 2.8, -50], B.inOut(k), 36);
    B.aimSun(L.sun, 2, 0, -50, [40, 30, 20]);
  } },
  { at: 33.1, f: (lt, k, d, t) => { // "Every time the old clock tower rang," - low angle, bell swings
    B.camMove(cam, [7, 1.6, -44], [5.5, 2.2, -48], [0, 21, -72], [0, 23, -72], B.inOut(k), 44);
    B.aimSun(L.sun, 0, 0, -66, [40, 30, 20]);
  } },
  { at: 35.4, f: (lt, k, d, t) => { // "everyone's clock jumped down."
    const hit = t >= 36.14;
    crowd.forEach((p, i) => {
      p.holo.userData.set(hit ? after[i] : before[i], hit ? B.RED : "#ff8a4a");
      p.holo.scale.setScalar(1 + (hit ? 0.35 * (1 - B.outCubic(B.seg(t, 36.14, 36.5))) : 0));
      p.setFace(hit ? "shock" : "smile");
      p.pose({ armL: hit ? 1.2 : 0, pitch: hit ? 0.3 : 0 });
    });
    const shake = hit ? Math.max(0, 1 - (t - 36.14) * 3) * 0.12 : 0;
    B.camMove(cam, [0, 4.6, -47.5], [0, 4.3, -49], [0, 3.0, -59], [0, 3.0, -59], B.inOut(k), 44);
    cam.position.x += Math.sin(t * 60) * shake;
    cam.position.y += Math.cos(t * 53) * shake;
    B.aimSun(L.sun, 0, 0, -58, [40, 30, 20]);
  } },
  { at: 37.2, f: (lt, k, d, t) => { // "Everyone except one man." - push between the crowd to the stage
    crowd.forEach((p, i) => { p.holo.userData.set(after[i], B.RED); p.holo.scale.setScalar(1); p.setFace("worried"); p.pose({}); });
    mayor.setFace("sly");
    mayor.pose({});
    B.camMove(cam, [4.2, 3.8, -48], [2.4, 3.6, -59.5], [0, 3.2, -66], [0, 3.6, -66], B.inOut(k), 38);
    B.aimSun(L.sun, 0, 0, -62, [40, 30, 20]);
  } },
  { at: 39.1, f: (lt, k, d, t) => { // "The mayor," - adjusts monocle
    mayor.setFace("sly");
    mayor.pose({ armR: 2.4 * B.smooth(B.seg(lt, 0, 0.4)), armRz: -0.5, yaw: 0.1 });
    mh.userData.set("899 YEARS", B.GOLD);
    B.camMove(cam, [-1.4, 3.4, -61.2], [-1.0, 3.5, -62.0], [0, 3.7, -66], [0, 3.8, -66], B.outCubic(k), 36);
  } },
  { at: 39.9, f: (lt, k, d, t) => { // "his clock said nine hundred years." - low angle, number pops
    const hit = t >= 40.64;
    mh.userData.set(hit ? "900 YEARS" : "899 YEARS", B.GOLD);
    mh.scale.set(1.9, 0.74, 1).multiplyScalar(1 + (hit ? 0.45 * (1 - B.outBack(B.seg(t, 40.64, 41.0))) + 0.25 : 0));
    mayor.setFace(hit ? "grin" : "sly");
    mayor.pose({ armL: 0.3, armR: 0.3, pitch: -0.12 });
    B.camMove(cam, [0.8, 1.6, -60.8], [0.6, 1.8, -62.0], [0, 4.2, -66], [0, 4.4, -66], B.inOut(k), 40);
  } },
], 41.9);

function render(t) {
  tw.setTime(5, 2 + t * 0.5);
  const bk = Math.max(0, t - 34.3);
  tw.bell.rotation.z = t > 34.3 ? Math.sin(bk * 7) * 0.5 * Math.exp(-bk * 0.6) : 0;
  const wk = B.seg(t, 34.76, 36.3);
  wave.scale.setScalar(1 + wk * 60);
  wave.material.opacity = t > 34.76 ? (1 - wk) * 0.9 : 0;
  wave.rotation.x = Math.PI / 2;
  if (t >= 36.14) { const w2 = B.seg(t, 36.0, 37.2); wave.position.y = 25 - w2 * 23; }
  mh.position.y = 3.8 + Math.sin(t * 2) * 0.05;
  shots(t);
  S.render();
}
