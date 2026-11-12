// "My name is Leo ... the clocks are never wrong."  8.93 - 19.2  (Leo's bedroom, morning)
const S = B.stage(CV, { bloom: 0.55, threshold: 1.2, exposure: 1.05 });
const { scene, cam } = S;
scene.background = new T.Color("#a9d1f2");
B.bedroom(scene);
scene.add(new T.HemisphereLight(0xfff4e6, 0x7a5a40, 1.6));
const fill = new T.DirectionalLight(0xffffff, 1.2);
fill.position.set(6, 10, 12);
scene.add(fill);
const leo = B.cast("leo", { face: "smile" });
leo.root.position.set(0, 0, 0.5);
scene.add(leo.root);
leo.setScreen({ big: "1", sub: "DAY LEFT", color: B.RED });
const mom = B.cast("mom", { face: "shock" });
mom.root.position.set(4.6, 0, 3.6);
mom.root.rotation.y = -1.25;
scene.add(mom.root);
const wrist = B.wristProp({ sleeve: "#d94c3d" });
wrist.group.scale.setScalar(0.42);
wrist.group.position.set(-1.5, 3.4, -4.5);
wrist.group.rotation.set(0.1, 0.2, 0.05);
scene.add(wrist.group);

const shots = B.shots([
  { at: 8.93, f: (lt, k, d, t) => { // "My name is Leo" - wave
    leo.setFace("smile");
    leo.pose({ armR: 2.6 + Math.sin(t * 9) * 0.25, armRz: 0.3, tilt: Math.sin(t * 3) * 0.05 });
    B.camMove(cam, [0.4, 3.0, 6.4], [0.3, 2.95, 5.2], [0, 2.6, 0.5], [0, 2.6, 0.5], B.outCubic(k), 38);
  } },
  { at: 10.05, f: (lt, k, d, t) => { // "And this morning" - big stretch in the sunbeam
    leo.setFace("happy");
    const s = B.smooth(B.seg(lt, 0, 0.6));
    leo.pose({ armL: 2.9 * s, armR: 2.9 * s, armLz: 0.3 * s, armRz: 0.3 * s, pitch: -0.15 * s });
    B.camMove(cam, [-5.5, 5.5, 9.5], [-5.0, 5.2, 8.6], [1.0, 2.0, -1.5], [1.0, 2.0, -1.5], B.inOut(k), 44);
  } },
  { at: 10.95, f: (lt, k, d, t) => { // "my clock said one day left"
    const flash = t > 11.6 ? 0.5 + 0.5 * Math.sin((t - 11.6) * 12) : 0;
    wrist.set(t < 11.6 ? { big: "1", sub: "DAY LEFT", color: "#ff8a4a" } : { big: "1", sub: "DAY LEFT", color: B.RED }, 1.4 + flash * 0.8);
    const push = B.inOut(B.seg(lt, 0, d)) * 0.5 + B.outExpo(B.seg(t, 11.62, 12.1)) * 0.5;
    wrist.group.visible = true;
    B.camMove(cam, [-1.0, 3.9, 1.2], [-1.2, 3.6, -1.3], [-1.25, 3.4, -4.5], [-1.25, 3.4, -4.5], push, 34);
  } },
  { at: 12.75, f: (lt, k, d, t) => { // "I'm twelve. I'm not even sick." - shocked
    leo.setFace(t < 13.5 ? "shock" : "worried");
    leo.pose({ armL: 1.2, armLz: -0.2, pitch: t < 13.5 ? 0.25 : 0, yaw: t < 13.5 ? 0 : Math.sin(t * 7) * 0.12 });
    B.camMove(cam, [0.3, 3.1, 5.6], [0.2, 3.0, 4.9], [0, 2.7, 0.5], [0, 2.65, 0.5], B.inOut(k), 34);
    cam.rotateZ(0.04);
  } },
  { at: 14.8, f: (lt, k, d, t) => { // "My mom saw it and started crying" - over Leo's shoulder to mom in the doorway
    leo.setFace("worried");
    leo.root.rotation.y = 0.9;
    leo.pose({ armL: 1.0 });
    mom.setFace(t < 15.95 ? "shock" : "cry");
    mom.pose({ armL: t < 15.95 ? 0.4 : 2.0, armR: t < 15.95 ? 0.4 : 2.0, armLz: -0.3, armRz: -0.3, pitch: t < 15.95 ? 0 : 0.15 });
    B.camMove(cam, [0.6, 3.7, -1.6], [1.0, 3.6, -0.8], [4.6, 2.7, 3.6], [4.6, 2.8, 3.6], B.inOut(k), 38);
  } },
  { at: 16.9, f: (lt, k, d, t) => { // "Leo, the clocks are never wrong."
    mom.setFace("cry");
    mom.pose({ armL: 1.2, armR: 1.2, pitch: 0.1 + Math.sin(t * 8) * 0.03, tilt: Math.sin(t * 2) * 0.05 });
    B.camMove(cam, [0.4, 3.2, 6.8], [0.9, 3.1, 6.0], [4.6, 2.85, 3.6], [4.6, 2.85, 3.6], B.inOut(k), 34);
  } },
], 19.2);

function render(t) {
  leo.root.rotation.y = 0;
  wrist.group.visible = false;
  shots(t);
  S.render();
}
