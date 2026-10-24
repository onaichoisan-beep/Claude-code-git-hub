/* Bio3D: shared Three.js builders for the malaria film. Everything is a pure function of
   scene time: scenes call build once, then pose(t) from their paused GSAP timeline. */
(function () {
  const T = THREE;
  const B = (window.Bio3D = {});
  T.ColorManagement.legacyMode = false; // hex colours are sRGB, converted to linear
  B.W = 1080;
  B.H = 1920;

  // ---------- math ----------
  B.rng = function (seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  const clamp = (B.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)));
  B.lerp = (a, b, k) => a + (b - a) * k;
  B.seg = (t, a, b) => clamp((t - a) / (b - a));
  B.smooth = (k) => k * k * (3 - 2 * k);
  B.outExpo = (k) => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k));
  B.outCubic = (k) => 1 - Math.pow(1 - k, 3);
  B.inCubic = (k) => k * k * k;
  B.inOut = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  B.outBack = (k, s = 1.6) => 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2);

  // ---------- renderer / stage ----------
  B.renderer = function (canvas) {
    const r = new T.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
    r.setPixelRatio(1);
    r.setSize(B.W, B.H, false);
    r.outputEncoding = T.sRGBEncoding;
    r.toneMapping = T.ACESFilmicToneMapping;
    r.toneMappingExposure = 0.95;
    r.physicallyCorrectLights = true;
    r.localClippingEnabled = true;
    return r;
  };

  // studio environment: dark-grey room with three soft light strips, for glossy reflections
  B.env = function (renderer) {
    const s = new T.Scene();
    const room = new T.Mesh(new T.BoxGeometry(20, 20, 20), new T.MeshBasicMaterial({ color: 0x5a6670, side: T.BackSide }));
    s.add(room);
    const strip = (w, h, x, y, z, ry, c) => {
      const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: new T.Color(c).multiplyScalar(2.2), side: T.DoubleSide }));
      m.position.set(x, y, z);
      m.lookAt(0, 0, 0);
      s.add(m);
    };
    strip(10, 2.2, -6, 7, 4, 0, 0xfff1e0);
    strip(2, 10, 8, 2, -3, 0, 0xc8f2ff);
    strip(8, 1.4, 0, -2, 9, 0, 0xffffff);
    const pm = new T.PMREMGenerator(renderer);
    const tex = pm.fromScene(s, 0.04).texture;
    pm.dispose();
    return tex;
  };

  B.lights = function (scene, o = {}) {
    scene.add(new T.HemisphereLight(o.sky || 0xe9f6ff, o.ground || 0x8a5a48, o.hemi ?? 0.6));
    const key = new T.DirectionalLight(0xfff1e0, o.key ?? 2.4);
    key.position.set(-5, 8, 6);
    scene.add(key);
    const rim = new T.DirectionalLight(0x9fe6ff, o.rim ?? 1.6);
    rim.position.set(4, 3, -7);
    scene.add(rim);
    return { key, rim };
  };

  B.canvasTex = function (w, h, draw, srgb = true) {
    const c = document.createElement("canvas");
    c.width = w;
    c.height = h;
    draw(c.getContext("2d"), w, h);
    const t = new T.CanvasTexture(c);
    if (srgb) t.encoding = T.sRGBEncoding;
    t.anisotropy = 8;
    return t;
  };

  // flat cyan cutaway ground from the reference films
  B.cyanBackground = function (scene) {
    scene.background = B.canvasTex(540, 960, (g, w, h) => {
      const gr = g.createRadialGradient(w * 0.5, h * 0.42, 40, w * 0.5, h * 0.5, h * 0.75);
      gr.addColorStop(0, "#4fd3ea");
      gr.addColorStop(0.55, "#2cbbd9");
      gr.addColorStop(1, "#1592b8");
      g.fillStyle = gr;
      g.fillRect(0, 0, w, h);
    });
  };

  B.camera = function (fov = 35) {
    return new T.PerspectiveCamera(fov, B.W / B.H, 0.02, 400);
  };

  // ---------- skin ----------
  B.skinTextures = function (seed = 7) {
    const rnd = B.rng(seed);
    const pores = [];
    for (let i = 0; i < 2600; i++) pores.push([rnd(), rnd(), 0.6 + rnd() * 1.8, rnd()]);
    const lines = [];
    for (let i = 0; i < 260; i++) lines.push([rnd(), rnd(), rnd() * Math.PI, 10 + rnd() * 34]);
    const blot = [];
    for (let i = 0; i < 40; i++) blot.push([rnd(), rnd(), 30 + rnd() * 110, rnd()]);
    const paint = (g, w, h, gray) => {
      g.fillStyle = gray ? "#808080" : "#d9a184";
      g.fillRect(0, 0, w, h);
      for (const [x, y, r, a] of blot) {
        const gr = g.createRadialGradient(x * w, y * h, 0, x * w, y * h, r);
        gr.addColorStop(0, gray ? "rgba(140,140,140,0.25)" : `rgba(${200 + a * 30},${110 + a * 20},${100},0.22)`);
        gr.addColorStop(1, "rgba(0,0,0,0)");
        g.fillStyle = gr;
        g.fillRect(0, 0, w, h);
      }
      g.lineCap = "round";
      for (const [x, y, ang, len] of lines) {
        g.strokeStyle = gray ? "rgba(40,40,40,0.3)" : "rgba(150,90,70,0.14)";
        g.lineWidth = 1.1;
        g.beginPath();
        g.moveTo(x * w, y * h);
        g.lineTo(x * w + Math.cos(ang) * len, y * h + Math.sin(ang) * len);
        g.stroke();
      }
      for (const [x, y, r, a] of pores) {
        g.fillStyle = gray ? `rgba(20,20,20,${0.5 + a * 0.4})` : `rgba(120,70,55,${0.25 + a * 0.3})`;
        g.beginPath();
        g.arc(x * w, y * h, r, 0, Math.PI * 2);
        g.fill();
      }
    };
    const map = B.canvasTex(1024, 1024, (g, w, h) => paint(g, w, h, false));
    const bump = B.canvasTex(1024, 1024, (g, w, h) => paint(g, w, h, true), false);
    for (const t of [map, bump]) {
      t.wrapS = t.wrapT = T.RepeatWrapping;
      t.repeat.set(5, 5);
    }
    return { map, bump };
  };

  B.skinMaterial = function () {
    const { map, bump } = B.skinTextures();
    return new T.MeshPhysicalMaterial({
      map,
      bumpMap: bump,
      bumpScale: 0.035,
      roughness: 0.52,
      sheen: 0.6,
      sheenColor: new T.Color(0xffd2c0),
      sheenRoughness: 0.5,
      clearcoat: 0.12,
      clearcoatRoughness: 0.45,
      envMapIntensity: 0.6,
    });
  };

  // ---------- mosquito (Anopheles: tilted head-down, spotted wings, long palps) ----------
  B.mosquito = function () {
    const root = new T.Group();
    const body = new T.Group();
    root.add(body);
    const brown = new T.MeshPhysicalMaterial({ color: 0x4a382c, roughness: 0.55, clearcoat: 0.3, clearcoatRoughness: 0.5, sheen: 0.8, sheenColor: new T.Color(0xc8a888) });
    const dark = new T.MeshPhysicalMaterial({ color: 0x2a1e18, roughness: 0.5, clearcoat: 0.4 });
    const eyeM = new T.MeshPhysicalMaterial({ color: 0x1c0d0a, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.1 });
    const bands = B.canvasTex(64, 512, (g, w, h) => {
      for (let i = 0; i < 16; i++) {
        g.fillStyle = i % 2 ? "#7c6450" : "#3a2b22";
        g.fillRect(0, (i * h) / 16, w, h / 16 + 1);
      }
    });
    const abdM = new T.MeshPhysicalMaterial({ map: bands, color: 0xffffff, roughness: 0.5, clearcoat: 0.5, clearcoatRoughness: 0.3, sheen: 0.6, sheenColor: new T.Color(0xd8b8a0) });

    // thorax at body origin, long axis +Z (head forward)
    const thorax = new T.Mesh(new T.SphereGeometry(1, 40, 28), brown);
    thorax.scale.set(0.36, 0.38, 0.5);
    body.add(thorax);
    const head = new T.Mesh(new T.SphereGeometry(0.21, 32, 24), dark);
    head.position.set(0, -0.08, 0.58);
    body.add(head);
    for (const s of [-1, 1]) {
      const eye = new T.Mesh(new T.SphereGeometry(0.12, 32, 24), eyeM);
      eye.position.set(0.11 * s, -0.04, 0.63);
      body.add(eye);
    }
    // proboscis + palps hang from a pivot at the head so they can swing down to bite
    const mouth = new T.Group();
    mouth.position.set(0, -0.16, 0.72);
    body.add(mouth);
    const prob = new T.Mesh(new T.CylinderGeometry(0.016, 0.028, 1.35, 10), dark);
    prob.geometry.translate(0, -0.675, 0);
    mouth.add(prob);
    // palps stay at rest while the proboscis bends down to bite
    const palps = new T.Group();
    palps.position.copy(mouth.position);
    palps.rotation.x = -1.42;
    body.add(palps);
    for (const s of [-1, 1]) {
      const palp = new T.Mesh(new T.CylinderGeometry(0.015, 0.022, 1.25, 8), brown);
      palp.geometry.translate(0, -0.62, 0);
      palp.position.x = 0.045 * s;
      palp.rotation.z = 0.06 * s;
      palps.add(palp);
      const ant = new T.Mesh(new T.CylinderGeometry(0.008, 0.016, 0.75, 6), brown);
      ant.geometry.translate(0, 0.37, 0);
      ant.position.set(0.07 * s, 0.02, 0.72);
      ant.rotation.set(0.9, 0, -0.35 * s);
      body.add(ant);
    }
    // abdomen behind the thorax
    const abdGeo = new T.SphereGeometry(1, 40, 32);
    abdGeo.rotateX(Math.PI / 2);
    const abdomen = new T.Mesh(abdGeo, abdM);
    abdomen.position.set(0, 0.04, -1.2);
    abdomen.scale.set(0.24, 0.22, 0.95);
    body.add(abdomen);
    // wings folded over the abdomen, dark spots along the front edge
    const wingTex = B.canvasTex(128, 512, (g, w, h) => {
      g.clearRect(0, 0, w, h);
      g.fillStyle = "rgba(225,235,240,0.32)";
      g.beginPath();
      g.ellipse(w / 2, h / 2, w / 2 - 2, h / 2 - 2, 0, 0, Math.PI * 2);
      g.fill();
      g.strokeStyle = "rgba(70,55,45,0.45)";
      g.lineWidth = 1.5;
      for (let i = 0; i < 6; i++) {
        g.beginPath();
        g.moveTo(w / 2, 8);
        g.quadraticCurveTo(w * (0.15 + i * 0.14), h * 0.5, w * (0.2 + i * 0.12), h - 10);
        g.stroke();
      }
      g.fillStyle = "rgba(40,28,22,0.8)";
      for (const y of [0.22, 0.4, 0.56, 0.72, 0.86]) g.fillRect(w * 0.1, h * y, w * 0.18, h * 0.06);
    });
    const wingM = new T.MeshPhysicalMaterial({ map: wingTex, transparent: true, side: T.DoubleSide, roughness: 0.15, clearcoat: 1, depthWrite: false, iridescence: 0.6, iridescenceIOR: 1.3 });
    for (const s of [-1, 1]) {
      const wg = new T.PlaneGeometry(0.5, 2.1);
      wg.rotateX(-Math.PI / 2);
      wg.translate(0, 0, -1.05);
      if (s < 0) wg.scale(-1, 1, 1);
      const wing = new T.Mesh(wg, wingM);
      wing.position.set(0.1 * s, 0.3, 0.05);
      wing.rotation.set(-0.08, 0.2 * s, -0.12 * s);
      body.add(wing);
    }
    body.rotation.x = 0.7; // ~40° head-down rest pose
    body.position.y = 1.35;
    // six jointed legs, feet on y = 0
    const legM = brown;
    const feet = [
      [0.55, 1.75], [1.85, 0.35], [1.25, -1.9],
    ];
    const legs = [];
    for (const s of [-1, 1]) {
      feet.forEach(([fx, fz], i) => {
        const hipZ = 0.12 - i * 0.12;
        const hip = new T.Vector3(0.12 * s, 1.2, hipZ + 0.1);
        const foot = new T.Vector3(fx * s, 0.0, fz);
        const knee = new T.Vector3(hip.x * 0.4 + foot.x * 0.6, 1.95 + i * 0.1, hip.z * 0.4 + foot.z * 0.6);
        const curve = new T.CatmullRomCurve3([hip, knee, new T.Vector3(foot.x * 0.95, 0.45, foot.z * 0.95), foot]);
        const leg = new T.Mesh(new T.TubeGeometry(curve, 48, 0.027, 8), legM);
        root.add(leg);
        legs.push(leg);
      });
    }
    root.userData = { body, mouth, abdomen, abdM, legs };
    return root;
  };

  // pose: bite 0..1 swings proboscis down into the skin; fill 0..1 swells abdomen red
  B.poseMosquito = function (m, bite, fill) {
    const u = m.userData;
    u.mouth.rotation.x = B.lerp(-1.42, -0.86, bite);
    const f = B.smooth(clamp(fill));
    u.abdomen.scale.set(0.24 + 0.2 * f, 0.22 + 0.24 * f, 0.95 + 0.12 * f);
    u.abdM.color.setRGB(1, 1 - 0.75 * f, 1 - 0.78 * f);
    u.abdM.sheen = 0.6 - 0.4 * f;
  };

  // ---------- cells and parasites ----------
  // Evans-Fung biconcave disc, radius 1
  B.rbcGeometry = function (seg = 64) {
    const pts = [];
    const N = 40;
    const h = (r) => Math.sqrt(Math.max(0, 1 - r * r)) * (0.207 + 2.003 * r * r - 1.123 * r * r * r * r) * 0.5;
    for (let i = 0; i <= N; i++) {
      const r = Math.sin((i / N) * Math.PI * 0.5);
      pts.push(new T.Vector2(r, h(r) + 0.004));
    }
    for (let i = N; i >= 0; i--) {
      const r = Math.sin((i / N) * Math.PI * 0.5);
      pts.push(new T.Vector2(r, -h(r) - 0.004));
    }
    const g = new T.LatheGeometry(pts.map((p) => new T.Vector2(Math.max(0.0001, p.x), p.y)), seg);
    g.computeVertexNormals();
    return g;
  };
  B.rbcMaterial = function (o = {}) {
    return new T.MeshPhysicalMaterial({
      color: o.color ?? 0xb3121f,
      roughness: 0.32,
      clearcoat: 0.6,
      clearcoatRoughness: 0.25,
      sheen: 0.7,
      sheenColor: new T.Color(0xff8a7a),
      transparent: !!o.opacity,
      opacity: o.opacity ?? 1,
      depthWrite: !o.opacity,
      side: o.opacity ? T.DoubleSide : T.FrontSide,
      envMapIntensity: 0.8,
    });
  };
  B.parasiteMaterial = function () {
    return new T.MeshPhysicalMaterial({ color: 0x6fd36a, roughness: 0.3, clearcoat: 0.8, clearcoatRoughness: 0.2, sheen: 0.5, sheenColor: new T.Color(0xe6ffb0) });
  };
  // sporozoite: slender crescent worm
  B.sporozoiteGeometry = function () {
    const pts = [];
    for (let i = 0; i <= 12; i++) {
      const a = -0.7 + (1.4 * i) / 12;
      pts.push(new T.Vector3(Math.sin(a) * 0.6, Math.cos(a) * 0.6 - 0.6, 0));
    }
    const g = new T.TubeGeometry(new T.CatmullRomCurve3(pts), 40, 0.045, 10);
    // taper both ends
    const p = g.attributes.position;
    const n = 11;
    for (let i = 0; i < p.count; i++) {
      const ring = Math.floor(i / n) / 40;
      const k = Math.sin(ring * Math.PI) ** 0.6;
      const c = new T.Vector3();
      const tpt = new T.CatmullRomCurve3(pts).getPoint(ring);
      c.set(p.getX(i), p.getY(i), p.getZ(i)).sub(tpt).multiplyScalar(k).add(tpt);
      p.setXYZ(i, c.x, c.y, c.z);
    }
    g.computeVertexNormals();
    return g;
  };
  // merozoite: small teardrop
  B.merozoiteGeometry = function () {
    const pts = [];
    for (let i = 0; i <= 24; i++) {
      const a = (i / 24) * Math.PI;
      const r = Math.sin(a) * (0.5 + 0.5 * Math.cos(a * 0.5)) * 0.5;
      pts.push(new T.Vector2(Math.max(0.0001, r), Math.cos(a) * 0.6));
    }
    const g = new T.LatheGeometry(pts, 20);
    g.computeVertexNormals();
    return g;
  };

  // ---------- shatter: split a mesh into flying shards ----------
  B.shatter = function (geometry, material, groups, seed) {
    const g = geometry.index ? geometry.toNonIndexed() : geometry.clone();
    const pos = g.attributes.position;
    const nor = g.attributes.normal;
    const tris = pos.count / 3;
    const rnd = B.rng(seed);
    const bins = [];
    for (let i = 0; i < groups; i++) bins.push([]);
    // bin triangles by direction from centre so shards are contiguous patches
    const seeds = [];
    for (let i = 0; i < groups; i++) {
      const v = new T.Vector3(rnd() * 2 - 1, rnd() * 2 - 1, rnd() * 2 - 1).normalize();
      seeds.push(v);
    }
    const c = new T.Vector3();
    for (let t = 0; t < tris; t++) {
      c.set(0, 0, 0);
      for (let k = 0; k < 3; k++) c.add(new T.Vector3().fromBufferAttribute(pos, t * 3 + k));
      c.divideScalar(3).normalize();
      let best = 0, bd = -2;
      seeds.forEach((s, i) => { const d = s.dot(c); if (d > bd) { bd = d; best = i; } });
      bins[best].push(t);
    }
    const grp = new T.Group();
    bins.forEach((list, i) => {
      if (!list.length) return;
      const p = new Float32Array(list.length * 9);
      const n = new Float32Array(list.length * 9);
      const cen = new T.Vector3();
      list.forEach((t, j) => {
        for (let k = 0; k < 3; k++) {
          for (let a = 0; a < 3; a++) {
            p[j * 9 + k * 3 + a] = pos.array[(t * 3 + k) * 3 + a];
            n[j * 9 + k * 3 + a] = nor.array[(t * 3 + k) * 3 + a];
          }
          cen.add(new T.Vector3(p[j * 9 + k * 3], p[j * 9 + k * 3 + 1], p[j * 9 + k * 3 + 2]));
        }
      });
      cen.divideScalar(list.length * 3);
      for (let j = 0; j < list.length * 3; j++) {
        p[j * 3] -= cen.x; p[j * 3 + 1] -= cen.y; p[j * 3 + 2] -= cen.z;
      }
      const sg = new T.BufferGeometry();
      sg.setAttribute("position", new T.BufferAttribute(p, 3));
      sg.setAttribute("normal", new T.BufferAttribute(n, 3));
      const m = new T.Mesh(sg, material);
      m.userData = { home: cen.clone(), dir: cen.clone().normalize(), spin: new T.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).multiplyScalar(6), speed: 0.7 + rnd() * 0.8 };
      m.position.copy(cen);
      grp.add(m);
    });
    // k: 0 intact .. 1 fully blown apart; dist in units
    grp.userData.pose = function (k, dist) {
      const e = B.outCubic(clamp(k));
      grp.children.forEach((m) => {
        const u = m.userData;
        m.position.copy(u.home).addScaledVector(u.dir, e * dist * u.speed);
        m.rotation.set(u.spin.x * e, u.spin.y * e, u.spin.z * e);
        m.scale.setScalar(1 - 0.6 * clamp((k - 0.4) / 0.6));
      });
    };
    return grp;
  };

  // ---------- organs ----------
  B.liver = function () {
    const g = new T.SphereGeometry(1, 160, 120);
    const p = g.attributes.position;
    const v = new T.Vector3();
    for (let i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      // wedge: big right lobe, thin left lobe, flat underside
      const lobe = 1 + 0.55 * Math.max(0, v.x);
      let y = v.y * (0.55 + 0.25 * (1 - (v.x + 1) / 2));
      if (y < -0.1) y = -0.1 + (y + 0.1) * 0.35;
      const bump = 1 + 0.025 * Math.sin(v.x * 9 + v.z * 7) * Math.cos(v.y * 8);
      p.setXYZ(i, v.x * 1.6 * bump, y * lobe * bump, v.z * (0.75 + 0.2 * v.x) * bump);
    }
    g.computeVertexNormals();
    const m = new T.MeshPhysicalMaterial({ color: 0x7c2125, roughness: 0.3, clearcoat: 0.7, clearcoatRoughness: 0.2, sheen: 0.5, sheenColor: new T.Color(0xd06060) });
    return new T.Mesh(g, m);
  };

  B.labelPos = function (obj3d, camera, out) {
    const v = new T.Vector3();
    obj3d.getWorldPosition(v);
    v.project(camera);
    out.x = (v.x * 0.5 + 0.5) * B.W;
    out.y = (-v.y * 0.5 + 0.5) * B.H;
    return out;
  };
})();
