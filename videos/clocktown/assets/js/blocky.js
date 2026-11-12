/* Blocky: shared Three.js builders for the clock-town story.
   Toy-world look: rounded box characters with flat 2D face textures, pastel kit-bashed sets,
   soft shadows, bloom on everything that glows. Every scene builds once, then renders a pure
   function of time (no clocks, seeded randomness only). */
(function () {
  const T = THREE;
  const B = (window.Blocky = {});
  T.ColorManagement.legacyMode = false;
  B.W = 720;
  B.H = 1280;
  B.FONT = "Fredoka, 'Arial Rounded MT Bold', sans-serif";

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
  const lerp = (B.lerp = (a, b, k) => a + (b - a) * k);
  B.seg = (t, a, b) => clamp((t - a) / (b - a));
  B.smooth = (k) => k * k * (3 - 2 * k);
  B.inOut = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  B.outCubic = (k) => 1 - Math.pow(1 - k, 3);
  B.inCubic = (k) => k * k * k;
  B.outExpo = (k) => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k));
  B.outBack = (k, s = 1.70158) => 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2);
  B.v3 = (x, y, z) => new T.Vector3(x, y, z);
  B.vl = (a, b, k) => new T.Vector3(lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k));

  // ---------- textures ----------
  B.canvasTex = function (w, h, draw) {
    const c = document.createElement("canvas");
    c.width = w;
    c.height = h;
    const g = c.getContext("2d");
    draw(g, w, h);
    const tex = new T.CanvasTexture(c);
    tex.encoding = T.sRGBEncoding;
    tex.anisotropy = 4;
    tex.userData.canvas = c;
    tex.userData.g = g;
    return tex;
  };
  B.redraw = function (tex, draw) {
    const c = tex.userData.canvas;
    tex.userData.g.clearRect(0, 0, c.width, c.height);
    draw(tex.userData.g, c.width, c.height);
    tex.needsUpdate = true;
  };
  function roundRect(g, x, y, w, h, r) {
    g.beginPath();
    g.moveTo(x + r, y);
    g.arcTo(x + w, y, x + w, y + h, r);
    g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r);
    g.arcTo(x, y, x + w, y, r);
    g.closePath();
  }
  B.roundRect = roundRect;

  // ---------- geometry ----------
  B.rbox = function (w, h, d, r, seg = 3) {
    const g = new T.BoxGeometry(w, h, d, seg * 2, seg * 2, seg * 2);
    const p = g.attributes.position;
    const v = new T.Vector3(), c = new T.Vector3(), n = new T.Vector3();
    const ix = w / 2 - r, iy = h / 2 - r, iz = d / 2 - r;
    for (let i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      c.set(clamp(v.x, -ix, ix), clamp(v.y, -iy, iy), clamp(v.z, -iz, iz));
      n.subVectors(v, c);
      if (n.lengthSq() > 0) n.normalize().multiplyScalar(r);
      p.setXYZ(i, c.x + n.x, c.y + n.y, c.z + n.z);
    }
    g.computeVertexNormals();
    return g;
  };
  const matCache = {};
  B.mat = function (color, o = {}) {
    const key = color + JSON.stringify(o);
    if (!o.unique && matCache[key]) return matCache[key];
    const m = new T.MeshStandardMaterial(Object.assign({ color: new T.Color(color), roughness: 0.82, metalness: 0 }, o.p || {}));
    if (o.emissive) {
      m.emissive = new T.Color(o.emissive);
      m.emissiveIntensity = o.ei ?? 2.5;
    }
    if (!o.unique) matCache[key] = m;
    return m;
  };
  B.glow = (color, intensity = 3) => {
    const m = new T.MeshBasicMaterial({ color: new T.Color(color).multiplyScalar(intensity) });
    return m;
  };
  B.box = function (w, h, d, mat, x = 0, y = 0, z = 0, r = 0) {
    const m = new T.Mesh(r ? B.rbox(w, h, d, r, 2) : new T.BoxGeometry(w, h, d), typeof mat === "string" ? B.mat(mat) : mat);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    return m;
  };

  // ---------- stage: renderer + bloom + tone map ----------
  const FinalShader = {
    uniforms: { tDiffuse: { value: null }, exposure: { value: 1.0 }, vig: { value: 0.35 }, tint: { value: new T.Vector3(1, 1, 1) }, flash: { value: 0 } },
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
    fragmentShader: [
      "uniform sampler2D tDiffuse; uniform float exposure; uniform float vig; uniform vec3 tint; uniform float flash; varying vec2 vUv;",
      "vec3 aces(vec3 x){ const float a=2.51; const float b=0.03; const float c=2.43; const float d=0.59; const float e=0.14; return clamp((x*(a*x+b))/(x*(c*x+d)+e),0.0,1.0); }",
      "vec3 srgb(vec3 c){ return mix(c*12.92, 1.055*pow(c, vec3(1.0/2.4))-0.055, step(vec3(0.0031308), c)); }",
      "void main(){ vec3 c = texture2D(tDiffuse, vUv).rgb * exposure * tint; c = aces(c); c = srgb(c);",
      " float d = distance(vUv*vec2(1.0,1.25), vec2(0.5,0.625)); c *= 1.0 - vig*smoothstep(0.3, 0.85, d);",
      " c = mix(c, vec3(1.0), flash); gl_FragColor = vec4(c, 1.0); }",
    ].join("\n"),
  };
  B.stage = function (canvas, o = {}) {
    const r = new T.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
    r.setPixelRatio(1);
    r.setSize(B.W, B.H, false);
    r.outputEncoding = T.LinearEncoding;
    r.toneMapping = T.NoToneMapping;
    r.physicallyCorrectLights = true;
    r.shadowMap.enabled = o.shadows !== false;
    r.shadowMap.type = T.PCFSoftShadowMap;
    const scene = new T.Scene();
    const cam = new T.PerspectiveCamera(o.fov || 40, B.W / B.H, 0.1, 600);
    const rt = new T.WebGLRenderTarget(B.W, B.H, { type: T.HalfFloatType, samples: 4 });
    const composer = new T.EffectComposer(r, rt);
    composer.addPass(new T.RenderPass(scene, cam));
    const bloom = new T.UnrealBloomPass(new T.Vector2(B.W, B.H), o.bloom ?? 0.8, o.bloomRadius ?? 0.55, o.threshold ?? 1.0);
    composer.addPass(bloom);
    const fin = new T.ShaderPass(FinalShader);
    fin.uniforms.exposure.value = o.exposure ?? 1.0;
    fin.uniforms.vig.value = o.vig ?? 0.35;
    composer.addPass(fin);
    const rp = composer.passes[0];
    const st = { r, scene, cam, composer, bloom, fin };
    st.setScene = (sc) => { rp.scene = sc; st.scene = sc; };
    st.render = () => composer.render();
    st.setLook = (exposure, flash = 0, tint) => {
      fin.uniforms.exposure.value = exposure;
      fin.uniforms.flash.value = flash;
      if (tint) fin.uniforms.tint.value.set(tint[0], tint[1], tint[2]);
    };
    return st;
  };
  B.camAt = function (cam, pos, look, fov) {
    cam.position.set(pos[0], pos[1], pos[2]);
    cam.lookAt(look[0], look[1], look[2]);
    if (fov && cam.fov !== fov) {
      cam.fov = fov;
      cam.updateProjectionMatrix();
    }
  };
  // move camera between two framings with progress k (already eased)
  B.camMove = function (cam, p0, p1, l0, l1, k, fov) {
    const p = B.vl(p0, p1, k), l = B.vl(l0, l1, k);
    B.camAt(cam, [p.x, p.y, p.z], [l.x, l.y, l.z], fov);
  };
  // pick the active shot: shots = [{at, f(lt, k, dur)}], sorted; last one runs to `end`
  B.shots = function (list, end) {
    return function (t) {
      let i = list.length - 1;
      while (i > 0 && t < list[i].at) i--;
      const s = list[i];
      const e = i + 1 < list.length ? list[i + 1].at : end;
      const lt = t - s.at;
      s.f(lt, clamp(lt / (e - s.at)), e - s.at, t);
      return i;
    };
  };

  B.sky = function (scene, top, horizon, bottom) {
    const tex = B.canvasTex(4, 512, (g, w, h) => {
      const gr = g.createLinearGradient(0, 0, 0, h);
      gr.addColorStop(0, top);
      gr.addColorStop(0.5, horizon);
      gr.addColorStop(1, bottom || horizon);
      g.fillStyle = gr;
      g.fillRect(0, 0, w, h);
    });
    const m = new T.Mesh(new T.SphereGeometry(400, 32, 16), new T.MeshBasicMaterial({ map: tex, side: T.BackSide, fog: false }));
    scene.add(m);
    return m;
  };
  B.lights = function (scene, o = {}) {
    const hemi = new T.HemisphereLight(o.sky || 0xdfefff, o.ground || 0x6b7f5a, o.hemi ?? 1.4);
    scene.add(hemi);
    const sun = new T.DirectionalLight(o.sunColor || 0xfff0d8, o.sun ?? 3.0);
    sun.position.set(...(o.sunPos || [-30, 50, 25]));
    sun.castShadow = o.shadows !== false;
    const s = o.shadowSize || 40;
    sun.shadow.camera.left = -s;
    sun.shadow.camera.right = s;
    sun.shadow.camera.top = s;
    sun.shadow.camera.bottom = -s;
    sun.shadow.camera.far = 200;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.bias = -0.0004;
    sun.shadow.normalBias = 0.03;
    sun.shadow.radius = 4;
    scene.add(sun);
    scene.add(sun.target);
    return { hemi, sun };
  };
  // keep the shadow frustum centred on what the camera sees
  B.aimSun = function (sun, x, y, z, off = [-30, 50, 25]) {
    sun.target.position.set(x, y, z);
    sun.position.set(x + off[0], y + off[1], z + off[2]);
  };

  // ---------- faces (the 2D part of the look) ----------
  const faceCache = {};
  function dotEye(g, x, y, rx, ry) {
    g.fillStyle = "#1b1310";
    g.beginPath();
    g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
    g.fill();
    g.fillStyle = "#ffffff";
    g.beginPath();
    g.arc(x + rx * 0.3, y - ry * 0.35, rx * 0.32, 0, Math.PI * 2);
    g.fill();
  }
  function line(g, pts, wdt, col) {
    g.strokeStyle = col || "#1b1310";
    g.lineWidth = wdt;
    g.lineCap = "round";
    g.lineJoin = "round";
    g.beginPath();
    g.moveTo(pts[0], pts[1]);
    for (let i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]);
    g.stroke();
  }
  function arc(g, x, y, r, a0, a1, wdt) {
    g.strokeStyle = "#1b1310";
    g.lineWidth = wdt;
    g.lineCap = "round";
    g.beginPath();
    g.arc(x, y, r, a0, a1);
    g.stroke();
  }
  B.drawFace = function (g, kind, skin, o = {}) {
    g.fillStyle = skin;
    g.fillRect(0, 0, 256, 256);
    const L = 88, R = 168, EY = 118, PI = Math.PI;
    const blush = () => {
      g.fillStyle = "rgba(255,120,130,0.45)";
      g.beginPath(); g.ellipse(62, 160, 20, 11, 0, 0, PI * 2); g.fill();
      g.beginPath(); g.ellipse(194, 160, 20, 11, 0, 0, PI * 2); g.fill();
    };
    if (o.freckles) {
      g.fillStyle = "rgba(150,80,40,0.55)";
      [[66, 150], [78, 158], [60, 162], [190, 150], [178, 158], [196, 162]].forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 3.2, 0, PI * 2); g.fill(); });
    }
    if (o.wrinkles) {
      line(g, [44, 92, 60, 96], 3, "rgba(80,40,20,0.45)");
      line(g, [212, 92, 196, 96], 3, "rgba(80,40,20,0.45)");
      line(g, [100, 70, 156, 70], 3, "rgba(80,40,20,0.35)");
    }
    switch (kind) {
      case "smile":
        dotEye(g, L, EY, 13, 18); dotEye(g, R, EY, 13, 18);
        arc(g, 128, 150, 34, 0.18 * PI, 0.82 * PI, 8);
        break;
      case "happy":
        arc(g, L, EY + 8, 16, 1.1 * PI, 1.9 * PI, 8); arc(g, R, EY + 8, 16, 1.1 * PI, 1.9 * PI, 8);
        g.fillStyle = "#4a1414";
        g.beginPath(); g.moveTo(92, 156); g.quadraticCurveTo(128, 214, 164, 156); g.closePath(); g.fill();
        g.fillStyle = "#e86a6a"; g.beginPath(); g.ellipse(128, 186, 16, 9, 0, 0, PI * 2); g.fill();
        blush();
        break;
      case "neutral":
        dotEye(g, L, EY, 12, 17); dotEye(g, R, EY, 12, 17);
        line(g, [110, 170, 146, 170], 7);
        break;
      case "shock":
        line(g, [66, 76, 80, 70, 104, 72], 7); line(g, [152, 72, 176, 70, 190, 76], 7);
        g.fillStyle = "#fff"; g.beginPath(); g.ellipse(L, EY, 20, 24, 0, 0, PI * 2); g.ellipse(R, EY, 20, 24, 0, 0, PI * 2); g.fill();
        dotEye(g, L, EY, 10, 12); dotEye(g, R, EY, 10, 12);
        g.fillStyle = "#3b1010"; g.beginPath(); g.ellipse(128, 176, 15, 19, 0, 0, PI * 2); g.fill();
        break;
      case "worried":
        line(g, [66, 86, 102, 74], 7); line(g, [154, 74, 190, 86], 7);
        dotEye(g, L, EY, 12, 16); dotEye(g, R, EY, 12, 16);
        line(g, [104, 176, 116, 168, 128, 176, 140, 168, 152, 176], 6);
        g.fillStyle = "#7fd3ff"; g.beginPath(); g.moveTo(214, 70); g.quadraticCurveTo(226, 96, 214, 102); g.quadraticCurveTo(202, 96, 214, 70); g.fill();
        break;
      case "cry":
        line(g, [66, 84, 102, 76], 7); line(g, [154, 76, 190, 84], 7);
        arc(g, L, EY - 4, 15, 0.1 * PI, 0.9 * PI, 7); arc(g, R, EY - 4, 15, 0.1 * PI, 0.9 * PI, 7);
        g.fillStyle = "rgba(110,200,255,0.95)";
        g.fillRect(L - 7, EY + 8, 14, 120); g.fillRect(R - 7, EY + 8, 14, 120);
        arc(g, 128, 196, 26, 1.15 * PI, 1.85 * PI, 7);
        break;
      case "angry":
        line(g, [62, 78, 106, 98], 9); line(g, [150, 98, 194, 78], 9);
        dotEye(g, L, EY + 4, 12, 14); dotEye(g, R, EY + 4, 12, 14);
        arc(g, 128, 196, 28, 1.2 * PI, 1.8 * PI, 8);
        break;
      case "determined":
        line(g, [64, 84, 106, 94], 8); line(g, [150, 94, 192, 84], 8);
        dotEye(g, L, EY + 2, 12, 15); dotEye(g, R, EY + 2, 12, 15);
        line(g, [108, 172, 150, 168], 7);
        break;
      case "sly":
        line(g, [64, 82, 104, 86], 7); line(g, [152, 76, 192, 68], 7);
        dotEye(g, L, EY + 4, 13, 13); dotEye(g, R, EY + 4, 13, 13);
        g.fillStyle = skin; g.fillRect(L - 18, EY - 16, 36, 14); g.fillRect(R - 18, EY - 16, 36, 14);
        line(g, [L - 16, EY - 3, L + 16, EY - 3], 6); line(g, [R - 16, EY - 3, R + 16, EY - 3], 6);
        g.strokeStyle = "#1b1310"; g.lineWidth = 7; g.beginPath(); g.moveTo(104, 168); g.quadraticCurveTo(140, 182, 160, 158); g.stroke();
        break;
      case "grin": {
        line(g, [62, 84, 104, 94], 7); line(g, [152, 94, 194, 84], 7);
        g.fillStyle = "#fff"; g.beginPath(); g.arc(L, EY, 22, 0, PI * 2); g.arc(R, EY, 22, 0, PI * 2); g.fill();
        g.fillStyle = "#1b1310"; g.beginPath(); g.arc(L, EY, 7, 0, PI * 2); g.arc(R, EY, 7, 0, PI * 2); g.fill();
        g.fillStyle = "#2a0808"; g.beginPath(); g.moveTo(54, 150); g.quadraticCurveTo(128, 236, 202, 150); g.quadraticCurveTo(128, 184, 54, 150); g.fill();
        g.fillStyle = "#fff";
        for (let i = 0; i < 9; i++) { const x = 70 + i * 13.5; g.fillRect(x, 156 + Math.abs(i - 4) * -1.5 + 6, 9, 11); }
        break;
      }
      case "scream":
        line(g, [62, 74, 104, 92], 9); line(g, [152, 92, 194, 74], 9);
        g.fillStyle = "#fff"; g.beginPath(); g.arc(L, EY + 2, 17, 0, PI * 2); g.arc(R, EY + 2, 17, 0, PI * 2); g.fill();
        g.fillStyle = "#1b1310"; g.beginPath(); g.arc(L, EY + 2, 5, 0, PI * 2); g.arc(R, EY + 2, 5, 0, PI * 2); g.fill();
        g.fillStyle = "#2a0808"; g.beginPath(); g.ellipse(128, 190, 30, 40, 0, 0, PI * 2); g.fill();
        g.fillStyle = "#c94a4a"; g.beginPath(); g.ellipse(128, 214, 18, 12, 0, 0, PI * 2); g.fill();
        break;
      case "eerie":
        g.fillStyle = "#1b1310"; g.beginPath(); g.ellipse(L, EY, 15, 19, 0, 0, PI * 2); g.ellipse(R, EY, 15, 19, 0, 0, PI * 2); g.fill();
        arc(g, 128, 146, 30, 0.22 * PI, 0.78 * PI, 7);
        break;
      case "sleep":
        line(g, [L - 16, EY + 4, L + 16, EY + 4], 7); line(g, [R - 16, EY + 4, R + 16, EY + 4], 7);
        arc(g, 128, 160, 16, 0.2 * PI, 0.8 * PI, 6);
        break;
    }
    if (o.mustache) {
      g.fillStyle = o.mustache;
      g.beginPath();
      g.moveTo(128, 146);
      g.bezierCurveTo(108, 128, 74, 134, 66, 158);
      g.bezierCurveTo(84, 150, 104, 160, 128, 154);
      g.bezierCurveTo(152, 160, 172, 150, 190, 158);
      g.bezierCurveTo(182, 134, 148, 128, 128, 146);
      g.fill();
    }
  };
  function faceTex(kind, skin, o) {
    const key = kind + skin + JSON.stringify(o || {});
    if (!faceCache[key]) faceCache[key] = B.canvasTex(256, 256, (g) => B.drawFace(g, kind, skin, o || {}));
    return faceCache[key];
  }

  // ---------- characters ----------
  function torsoTex(o) {
    return B.canvasTex(256, 256, (g) => {
      g.fillStyle = o.shirt; g.fillRect(0, 0, 256, 256);
      const st = o.style;
      if (st === "jacket") {
        g.fillStyle = o.shirt2; g.fillRect(96, 0, 64, 256);
        g.fillStyle = "rgba(0,0,0,0.18)"; g.fillRect(90, 0, 6, 256); g.fillRect(160, 0, 6, 256);
        g.fillStyle = "rgba(0,0,0,0.12)"; g.fillRect(28, 150, 46, 30); g.fillRect(182, 150, 46, 30);
      } else if (st === "hoodie") {
        g.fillStyle = "rgba(255,255,255,0.9)"; g.fillRect(100, 0, 6, 90); g.fillRect(150, 0, 6, 90);
        g.fillStyle = "rgba(0,0,0,0.14)"; roundRect(g, 64, 160, 128, 70, 18); g.fill();
      } else if (st === "suit") {
        g.fillStyle = o.shirt2; g.beginPath(); g.moveTo(92, 0); g.lineTo(128, 110); g.lineTo(164, 0); g.fill();
        g.fillStyle = "#8b0f1a"; g.beginPath(); g.moveTo(120, 8); g.lineTo(136, 8); g.lineTo(140, 96); g.lineTo(128, 112); g.lineTo(116, 96); g.fill();
        g.fillStyle = "#ffd257"; [140, 180, 220].forEach((y) => { g.beginPath(); g.arc(108, y, 8, 0, 7); g.arc(148, y, 8, 0, 7); g.fill(); });
        g.strokeStyle = "#ffd257"; g.lineWidth = 6; g.beginPath(); g.moveTo(40, 120); g.quadraticCurveTo(70, 170, 92, 140); g.stroke();
      } else if (st === "apron") {
        g.fillStyle = o.shirt2; roundRect(g, 54, 40, 148, 230, 20); g.fill();
        g.fillStyle = "rgba(0,0,0,0.1)"; roundRect(g, 92, 150, 72, 50, 10); g.fill();
      } else if (st === "postal") {
        g.fillStyle = o.shirt2; g.fillRect(0, 0, 256, 40);
        g.fillStyle = "#ffd257"; g.fillRect(150, 70, 50, 34);
      } else if (st === "cardigan") {
        g.fillStyle = o.shirt2; g.fillRect(100, 0, 56, 256);
        g.fillStyle = "#fff"; [60, 120, 180].forEach((y) => { g.beginPath(); g.arc(94, y, 7, 0, 7); g.fill(); });
      }
    });
  }
  function hair(p, o) {
    const hg = new T.Group();
    const c = o.hairColor || "#6b3f1d";
    const m = B.mat(c, { p: { roughness: 0.7 } });
    const s = o.hair;
    if (s === "spiky") {
      hg.add(B.box(0.9, 0.24, 0.9, m, 0, 0.42, -0.02, 0.08));
      hg.add(B.box(0.9, 0.5, 0.2, m, 0, 0.2, -0.38, 0.06));
      hg.add(B.box(0.2, 0.3, 0.86, m, -0.38, 0.28, -0.02, 0.06));
      hg.add(B.box(0.2, 0.3, 0.86, m, 0.38, 0.28, -0.02, 0.06));
      const r = B.rng(7);
      for (let i = 0; i < 9; i++) {
        const sp = new T.Mesh(new T.ConeGeometry(0.16, 0.36, 4), m);
        sp.castShadow = true;
        const a = (i % 3) - 1, b = Math.floor(i / 3) - 1;
        sp.position.set(a * 0.27, 0.6, b * 0.26 + 0.02);
        sp.rotation.set(b * 0.5 + (r() - 0.5) * 0.3, r() * 1.5, -a * 0.5);
        hg.add(sp);
      }
      hg.add(B.box(0.86, 0.16, 0.14, m, 0, 0.32, 0.4, 0.05)); // fringe
    } else if (s === "bob") {
      hg.add(B.box(0.94, 0.26, 0.94, m, 0, 0.43, 0, 0.1));
      hg.add(B.box(0.2, 0.86, 0.94, m, -0.46, 0.06, -0.02, 0.08));
      hg.add(B.box(0.2, 0.86, 0.94, m, 0.46, 0.06, -0.02, 0.08));
      hg.add(B.box(0.94, 0.86, 0.2, m, 0, 0.06, -0.44, 0.08));
      hg.add(B.box(0.9, 0.2, 0.14, m, 0, 0.3, 0.42, 0.06));
    } else if (s === "bun") {
      hg.add(B.box(0.9, 0.24, 0.9, m, 0, 0.42, -0.02, 0.1));
      hg.add(B.box(0.9, 0.5, 0.18, m, 0, 0.2, -0.4, 0.06));
      hg.add(B.box(0.16, 0.36, 0.8, m, -0.42, 0.26, -0.04, 0.06));
      hg.add(B.box(0.16, 0.36, 0.8, m, 0.42, 0.26, -0.04, 0.06));
      const bun = new T.Mesh(new T.SphereGeometry(0.24, 16, 12), m);
      bun.position.set(0, 0.64, -0.26);
      hg.add(bun);
    } else if (s === "short") {
      hg.add(B.box(0.88, 0.2, 0.88, m, 0, 0.42, -0.02, 0.08));
      hg.add(B.box(0.88, 0.42, 0.16, m, 0, 0.22, -0.4, 0.06));
      hg.add(B.box(0.84, 0.12, 0.12, m, 0, 0.36, 0.41, 0.05));
    } else if (s === "tophat") {
      const hm = B.mat("#16131c", { p: { roughness: 0.4 } });
      const brim = new T.Mesh(new T.CylinderGeometry(0.66, 0.66, 0.06, 32), hm);
      brim.position.y = 0.42;
      const crown = new T.Mesh(new T.CylinderGeometry(0.42, 0.44, 0.78, 32), hm);
      crown.position.y = 0.82;
      const band = new T.Mesh(new T.CylinderGeometry(0.445, 0.445, 0.14, 32), B.mat("#e0b23c", { p: { roughness: 0.3, metalness: 0.7 } }));
      band.position.y = 0.52;
      [brim, crown, band].forEach((x) => { x.castShadow = true; hg.add(x); });
      hg.add(B.box(0.84, 0.2, 0.12, B.mat("#cfcfd4"), 0, 0.12, -0.42, 0.05));
    } else if (s === "chef") {
      const wm = B.mat("#fbfbf7");
      const band = new T.Mesh(new T.CylinderGeometry(0.47, 0.47, 0.22, 24), wm);
      band.position.y = 0.48;
      const puff = new T.Mesh(new T.SphereGeometry(0.56, 20, 14), wm);
      puff.scale.set(1, 0.72, 1);
      puff.position.y = 0.86;
      [band, puff].forEach((x) => { x.castShadow = true; hg.add(x); });
    } else if (s === "cap") {
      const cm = B.mat(o.capColor || "#2e4f9e");
      hg.add(B.box(0.9, 0.28, 0.9, cm, 0, 0.44, 0, 0.12));
      hg.add(B.box(0.8, 0.06, 0.4, cm, 0, 0.32, 0.56, 0.02));
      hg.add(B.box(0.9, 0.3, 0.16, m, 0, 0.18, -0.4, 0.05));
    } else if (s === "bald") {
      hg.add(B.box(0.14, 0.3, 0.6, m, -0.44, 0.1, -0.1, 0.05));
      hg.add(B.box(0.14, 0.3, 0.6, m, 0.44, 0.1, -0.1, 0.05));
      hg.add(B.box(0.84, 0.3, 0.14, m, 0, 0.1, -0.42, 0.05));
    } else if (s === "pony") {
      hg.add(B.box(0.92, 0.24, 0.92, m, 0, 0.43, -0.02, 0.1));
      hg.add(B.box(0.92, 0.52, 0.18, m, 0, 0.2, -0.42, 0.06));
      hg.add(B.box(0.84, 0.14, 0.12, m, 0, 0.34, 0.42, 0.05));
      hg.add(B.box(0.26, 0.6, 0.26, m, 0, 0.12, -0.6, 0.1));
    }
    return hg;
  }
  B.screenTex = function () {
    return B.canvasTex(256, 160, (g) => { g.fillStyle = "#000"; g.fillRect(0, 0, 256, 160); });
  };
  // draw a wrist-clock screen: big number + small unit, colour coded
  B.drawScreen = function (g, w, h, s) {
    g.fillStyle = s.bg || "#05060a";
    g.fillRect(0, 0, w, h);
    if (s.blank) {
      g.fillStyle = "#121821";
      g.fillRect(0, 0, w, h);
      g.fillStyle = "rgba(150,175,200,0.18)";
      for (let y = 0; y < h; y += 8) g.fillRect(0, y, w, 3);
      g.strokeStyle = "rgba(160,200,230,0.35)";
      g.lineWidth = w * 0.012;
      g.strokeRect(w * 0.06, h * 0.08, w * 0.88, h * 0.84);
      return;
    }
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillStyle = s.color || "#ff3b3b";
    g.shadowColor = s.color || "#ff3b3b";
    g.shadowBlur = w * 0.04;
    const big = s.big || "";
    let fs = h * (s.sub ? 0.56 : 0.7);
    g.font = `700 ${fs}px ${B.FONT}`;
    while (g.measureText(big).width > w * 0.9 && fs > 10) { fs *= 0.92; g.font = `700 ${fs}px ${B.FONT}`; }
    g.fillText(big, w / 2, s.sub ? h * 0.4 : h * 0.52);
    if (s.sub) {
      g.font = `600 ${h * 0.22}px ${B.FONT}`;
      g.fillText(s.sub, w / 2, h * 0.8);
    }
    g.shadowBlur = 0;
  };
  B.setScreen = function (tex, s) {
    const key = JSON.stringify(s);
    if (tex.userData.key === key) return;
    tex.userData.key = key;
    B.redraw(tex, (g, w, h) => B.drawScreen(g, w, h, s));
  };

  B.person = function (o = {}) {
    o = Object.assign({ skin: "#f4c89f", shirt: "#d94c3d", shirt2: "#f4f1ea", pants: "#33406e", shoes: "#2a2a30", hair: "short", style: "plain", face: "smile" }, o);
    const root = new T.Group();
    const body = new T.Group();
    root.add(body);
    const skinM = B.mat(o.skin);
    const shirtM = B.mat(o.shirt);
    const pantsM = B.mat(o.pants);
    const shoeM = B.mat(o.shoes);
    // legs
    const mkLeg = (x) => {
      const piv = new T.Group();
      piv.position.set(x, 1.0, 0);
      piv.add(B.box(0.46, 0.86, 0.5, pantsM, 0, -0.43, 0, 0.06));
      piv.add(B.box(0.48, 0.16, 0.56, shoeM, 0, -0.92, 0.02, 0.05));
      body.add(piv);
      return piv;
    };
    const legL = mkLeg(0.25), legR = mkLeg(-0.25);
    // torso
    const tt = torsoTex(o);
    const tm = new T.MeshStandardMaterial({ map: tt, roughness: 0.85 });
    const torso = new T.Mesh(B.rbox(1.0, 1.0, 0.52, 0.08, 2), [shirtM, shirtM, shirtM, shirtM, tm, shirtM]);
    torso.position.y = 1.5;
    torso.castShadow = torso.receiveShadow = true;
    body.add(torso);
    // arms
    const mkArm = (x) => {
      const piv = new T.Group();
      piv.position.set(x, 1.96, 0);
      piv.add(B.box(0.42, 0.72, 0.46, shirtM, 0, -0.36, 0, 0.06));
      piv.add(B.box(0.38, 0.3, 0.42, skinM, 0, -0.86, 0, 0.08));
      body.add(piv);
      return piv;
    };
    const armL = mkArm(0.72), armR = mkArm(-0.72);
    // wrist clock on the left arm
    const band = B.box(0.44, 0.12, 0.48, B.mat("#222228", { p: { roughness: 0.4 } }), 0, -0.76, 0);
    armL.add(band);
    const scrTex = B.screenTex();
    const scr = new T.Mesh(new T.PlaneGeometry(0.34, 0.2), new T.MeshBasicMaterial({ map: scrTex, toneMapped: false }));
    scr.position.set(0, -0.76, 0.247);
    armL.add(scr);
    B.setScreen(scrTex, { big: "70", sub: "YEARS", color: "#59ff9a" });
    // head
    const neck = new T.Group();
    neck.position.y = 2.0;
    body.add(neck);
    const faceM = new T.MeshStandardMaterial({ map: faceTex(o.face, o.skin, o.faceOpts), roughness: 0.8 });
    const head = new T.Mesh(B.rbox(0.82, 0.82, 0.82, 0.12, 3), [skinM, skinM, skinM, skinM, faceM, skinM]);
    head.position.y = 0.42;
    head.castShadow = true;
    neck.add(head);
    const hr = hair(head, o);
    head.add(hr);
    if (o.monocle) {
      const mono = new T.Mesh(new T.TorusGeometry(0.11, 0.018, 8, 24), B.mat("#e0b23c", { p: { metalness: 0.8, roughness: 0.3 } }));
      mono.position.set(-0.155, 0.04, 0.42);
      head.add(mono);
    }
    if (o.glasses) {
      const gm = B.mat("#1b1b20");
      const l = new T.Mesh(new T.TorusGeometry(0.1, 0.018, 8, 20), gm), rr = l.clone();
      l.position.set(-0.155, 0.04, 0.42); rr.position.set(0.155, 0.04, 0.42);
      head.add(l, rr, B.box(0.1, 0.02, 0.02, gm, 0, 0.06, 0.42));
    }
    // glowing eye pads, used for the final eerie shot
    const eyeGlowM = new T.MeshBasicMaterial({ color: new T.Color("#9ff6ff"), transparent: true, opacity: 0, toneMapped: false });
    const eyeGlow = new T.Group();
    [-0.157, 0.157].forEach((x) => {
      const e = new T.Mesh(new T.CircleGeometry(0.055, 20), eyeGlowM);
      e.scale.y = 1.25;
      e.position.set(x, 0.045, 0.413);
      eyeGlow.add(e);
    });
    head.add(eyeGlow);

    const P = {
      root, body, legL, legR, armL, armR, neck, head, torso, screen: scrTex, scr, opts: o,
      setFace(kind, fo) { faceM.map = faceTex(kind, o.skin, Object.assign({}, o.faceOpts, fo)); },
      setScreen(s) { B.setScreen(scrTex, s); },
      setEyeGlow(k) { eyeGlowM.opacity = k; eyeGlowM.color.set("#9ff6ff").multiplyScalar(1 + k * 3); },
      // pose: walk phase/amount, arm raises (radians, + = forward/up), head yaw/pitch, jump height
      pose(p = {}) {
        const w = p.walk || 0, a = p.walkAmt ?? (p.walk !== undefined ? 1 : 0);
        const sw = Math.sin(w) * 0.7 * a;
        legL.rotation.x = sw; legR.rotation.x = -sw;
        armL.rotation.x = -sw * 0.8 - (p.armL || 0);
        armR.rotation.x = sw * 0.8 - (p.armR || 0);
        armL.rotation.z = p.armLz || 0; armR.rotation.z = -(p.armRz || 0);
        body.position.y = Math.abs(Math.cos(w)) * 0.08 * a + (p.jump || 0);
        neck.rotation.y = p.yaw || 0;
        neck.rotation.x = p.pitch || 0;
        neck.rotation.z = p.tilt || 0;
        body.rotation.x = p.lean || 0;
      },
    };
    P.pose({});
    root.userData.person = P;
    return P;
  };

  // floating hologram number above someone's head
  B.holo = function () {
    const tex = B.canvasTex(512, 200, () => {});
    const sp = new T.Sprite(new T.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, toneMapped: false }));
    sp.scale.set(1.9, 0.74, 1);
    sp.userData.tex = tex;
    sp.userData.set = (text, color, crack) => {
      const key = text + color + (crack || "");
      if (tex.userData.key === key) return;
      tex.userData.key = key;
      B.redraw(tex, (g, w, h) => {
        g.fillStyle = "rgba(8,10,20,0.62)";
        roundRect(g, 10, 30, w - 20, h - 60, 50);
        g.fill();
        g.strokeStyle = color;
        g.lineWidth = 7;
        roundRect(g, 10, 30, w - 20, h - 60, 50);
        g.stroke();
        g.fillStyle = color;
        g.shadowColor = color;
        g.shadowBlur = 18;
        g.textAlign = "center";
        g.textBaseline = "middle";
        let fs = 86;
        g.font = `700 ${fs}px ${B.FONT}`;
        while (g.measureText(text).width > w - 70) { fs -= 4; g.font = `700 ${fs}px ${B.FONT}`; }
        g.fillText(text, w / 2, h / 2 + 4);
        if (crack) {
          g.shadowBlur = 0;
          g.strokeStyle = "#ffffff";
          g.lineWidth = 5;
          g.beginPath();
          g.moveTo(w * 0.46, 30); g.lineTo(w * 0.52, 80); g.lineTo(w * 0.44, 110); g.lineTo(w * 0.55, h - 30);
          g.moveTo(w * 0.52, 80); g.lineTo(w * 0.7, 70); g.lineTo(w * 0.8, 120);
          g.moveTo(w * 0.44, 110); g.lineTo(w * 0.25, 140);
          g.stroke();
        }
      });
    };
    return sp;
  };

  // ---------- town set ----------
  B.tree = function (x, z, s = 1, seed = 1) {
    const g = new T.Group();
    const r = B.rng(seed);
    const trunk = new T.Mesh(new T.CylinderGeometry(0.22 * s, 0.3 * s, 2.2 * s, 8), B.mat("#7a5232"));
    trunk.position.y = 1.1 * s;
    trunk.castShadow = true;
    g.add(trunk);
    const greens = ["#4fae4a", "#5cbf52", "#469d44"];
    for (let i = 0; i < 3; i++) {
      const b = new T.Mesh(new T.IcosahedronGeometry((1.05 + r() * 0.3) * s, 1), B.mat(greens[i], { p: { flatShading: true } }));
      b.position.set((r() - 0.5) * 0.9 * s, (2.6 + r() * 0.7) * s, (r() - 0.5) * 0.9 * s);
      b.castShadow = true;
      g.add(b);
    }
    g.position.set(x, 0, z);
    return g;
  };
  B.house = function (o) {
    const g = new T.Group();
    const w = o.w || 6, h = o.h || 4.4, d = o.d || 6;
    const walls = B.box(w, h, d, o.color || "#e8b4a0", 0, h / 2, 0, 0.08);
    g.add(walls);
    const roof = new T.Mesh(new T.ConeGeometry(Math.max(w, d) * 0.78, 2.6, 4), B.mat(o.roof || "#7e4a46", { p: { flatShading: true } }));
    roof.rotation.y = Math.PI / 4;
    roof.position.y = h + 1.3;
    roof.scale.set(1, 1, d / w);
    roof.castShadow = true;
    g.add(roof);
    const winM = o.night ? B.glow(o.window || "#ffcf7a", 2.2) : B.mat("#8fc8ef", { p: { roughness: 0.15, metalness: 0.2 } });
    const frameM = B.mat("#fbf6ee");
    const wins = [];
    [[-w * 0.27, h * 0.68], [w * 0.27, h * 0.68], [-w * 0.27, h * 0.3]].forEach(([x, y]) => {
      g.add(B.box(1.25, 1.25, 0.12, frameM, x, y, d / 2 + 0.02));
      const wi = new T.Mesh(new T.PlaneGeometry(1.0, 1.0), winM);
      wi.position.set(x, y, d / 2 + 0.09);
      g.add(wi);
      wins.push(wi);
    });
    g.add(B.box(1.1, 2.0, 0.14, B.mat(o.door || "#6b3b2e"), w * 0.27, 1.0, d / 2 + 0.03));
    g.add(B.box(1.6, 0.18, 1.2, "#d8d2c8", w * 0.27, 0.09, d / 2 + 0.6));
    g.userData.windows = wins;
    g.userData.winMat = winM;
    g.position.set(o.x || 0, 0, o.z || 0);
    g.rotation.y = o.ry || 0;
    return g;
  };
  B.fence = function (x0, x1, z, rot = 0) {
    const g = new T.Group();
    const m = B.mat("#fbfaf6");
    const n = Math.round(Math.abs(x1 - x0) / 0.5);
    for (let i = 0; i <= n; i++) g.add(B.box(0.18, 0.9, 0.08, m, x0 + ((x1 - x0) * i) / n, 0.45, 0));
    g.add(B.box(Math.abs(x1 - x0), 0.1, 0.06, m, (x0 + x1) / 2, 0.62, -0.05));
    g.position.z = z;
    g.rotation.y = rot;
    return g;
  };
  B.lamp = function (x, z, night) {
    const g = new T.Group();
    const pm = B.mat("#3b3f4a", { p: { roughness: 0.5 } });
    const pole = new T.Mesh(new T.CylinderGeometry(0.08, 0.1, 4.2, 8), pm);
    pole.position.y = 2.1;
    pole.castShadow = true;
    g.add(pole);
    g.add(B.box(0.9, 0.08, 0.08, pm, x > 0 ? -0.4 : 0.4, 4.15, 0));
    const bulb = new T.Mesh(new T.SphereGeometry(0.2, 12, 8), night ? B.glow("#ffd890", 4) : B.mat("#fff6e0"));
    bulb.position.set(x > 0 ? -0.8 : 0.8, 4.0, 0);
    g.add(bulb);
    if (night) {
      const pl = new T.PointLight(0xffc878, 18, 9, 2);
      pl.position.copy(bulb.position);
      pl.position.y -= 0.3;
      g.add(pl);
    }
    g.position.set(x, 0, z);
    return g;
  };
  B.clockFaceTex = function (o = {}) {
    return B.canvasTex(512, 512, (g, w) => {
      const c = w / 2;
      g.fillStyle = o.rim || "#3a2a1c";
      g.beginPath(); g.arc(c, c, c, 0, 7); g.fill();
      g.fillStyle = o.face || "#f6ecd2";
      g.beginPath(); g.arc(c, c, c * 0.88, 0, 7); g.fill();
      g.fillStyle = o.ink || "#2b1d14";
      for (let i = 0; i < 60; i++) {
        const a = (i / 60) * Math.PI * 2, big = i % 5 === 0;
        const r0 = c * (big ? 0.7 : 0.78), r1 = c * 0.84;
        g.lineWidth = big ? 10 : 4;
        g.strokeStyle = o.ink || "#2b1d14";
        g.beginPath();
        g.moveTo(c + Math.sin(a) * r0, c - Math.cos(a) * r0);
        g.lineTo(c + Math.sin(a) * r1, c - Math.cos(a) * r1);
        g.stroke();
      }
      g.font = `700 ${c * 0.24}px ${B.FONT}`;
      g.textAlign = "center"; g.textBaseline = "middle";
      ["XII", "III", "VI", "IX"].forEach((s, i) => {
        const a = (i / 4) * Math.PI * 2;
        g.fillText(s, c + Math.sin(a) * c * 0.52, c - Math.cos(a) * c * 0.52);
      });
    });
  };
  // a clock (face + two hands) facing +z; returns {group, set(hours, minutes)}
  B.clock = function (radius, o = {}) {
    const g = new T.Group();
    const faceMat = o.glow
      ? new T.MeshBasicMaterial({ map: B.clockFaceTex(o), color: new T.Color(1, 1, 1).multiplyScalar(o.glow) })
      : new T.MeshStandardMaterial({ map: B.clockFaceTex(o), roughness: 0.6 });
    const face = new T.Mesh(new T.CircleGeometry(radius, 48), faceMat);
    g.add(face);
    const hm = B.mat(o.hand || "#20160f", { p: { roughness: 0.4, metalness: 0.3 } });
    const mk = (len, wdt) => {
      const piv = new T.Group();
      const m = new T.Mesh(new T.BoxGeometry(wdt, len, 0.04 * radius), hm);
      m.position.y = len * 0.4;
      piv.add(m);
      piv.position.z = 0.03 * radius;
      g.add(piv);
      return piv;
    };
    const hh = mk(radius * 0.5, radius * 0.07), mh = mk(radius * 0.78, radius * 0.045);
    const cap = new T.Mesh(new T.CylinderGeometry(radius * 0.07, radius * 0.07, radius * 0.05, 16), hm);
    cap.rotation.x = Math.PI / 2;
    cap.position.z = 0.06 * radius;
    g.add(cap);
    return {
      group: g, face,
      set(h, m) {
        hh.rotation.z = -((h % 12) / 12) * Math.PI * 2 - (m / 60 / 12) * Math.PI * 2;
        mh.rotation.z = -(m / 60) * Math.PI * 2;
      },
    };
  };
  B.tower = function (o = {}) {
    const g = new T.Group();
    const brick = B.mat(o.brick || "#b7745a");
    const trim = B.mat("#e9dcc4");
    g.add(B.box(8, 4, 8, trim, 0, 2, 0, 0.1));
    g.add(B.box(6.4, 20, 6.4, brick, 0, 12, 0, 0.1));
    g.add(B.box(7.2, 0.6, 7.2, trim, 0, 18.4, 0, 0.1));
    g.add(B.box(7.2, 0.6, 7.2, trim, 0, 22.2, 0, 0.1));
    // belfry: four corner posts, bell inside
    [[-2.8, -2.8], [2.8, -2.8], [-2.8, 2.8], [2.8, 2.8]].forEach(([x, z]) => g.add(B.box(0.9, 3.6, 0.9, brick, x, 24.3, z)));
    g.add(B.box(7.2, 0.6, 7.2, trim, 0, 26.4, 0, 0.1));
    const bellPiv = new T.Group();
    bellPiv.position.set(0, 25.9, 0);
    const pts = [];
    for (let i = 0; i <= 12; i++) { const k = i / 12; pts.push(new T.Vector2(0.4 + Math.pow(k, 2.2) * 1.2, -k * 2.0)); }
    const bell = new T.Mesh(new T.LatheGeometry(pts, 24), B.mat("#d9a23a", { p: { metalness: 0.8, roughness: 0.3 } }));
    bell.castShadow = true;
    bellPiv.add(bell);
    g.add(bellPiv);
    const roof = new T.Mesh(new T.ConeGeometry(5.6, 7, 4), B.mat(o.roof || "#3d4b7a", { p: { flatShading: true } }));
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 30.2;
    roof.castShadow = true;
    g.add(roof);
    const tip = new T.Mesh(new T.ConeGeometry(0.25, 2.2, 8), B.mat("#e0b23c", { p: { metalness: 0.8, roughness: 0.3 } }));
    tip.position.y = 34.6;
    g.add(tip);
    const clocks = [];
    for (let i = 0; i < 4; i++) {
      const c = B.clock(2.5, { glow: o.night ? 1.6 : 0 });
      const holder = new T.Group();
      holder.rotation.y = (i * Math.PI) / 2;
      c.group.position.set(0, 15, 3.24);
      holder.add(c.group);
      g.add(holder);
      clocks.push(c);
    }
    g.add(B.box(2.4, 3.6, 0.3, B.mat("#5a3424"), 0, 1.8, 4.02));
    g.position.set(o.x || 0, 0, o.z || 0);
    return { group: g, bell: bellPiv, clocks, setTime(h, m) { clocks.forEach((c) => c.set(h, m)); } };
  };
  // the street: road along z, houses both sides, trees, lamps, fences, tower at the far end
  B.town = function (scene, o = {}) {
    const night = !!o.night;
    const ground = new T.Mesh(new T.PlaneGeometry(400, 400), B.mat(night ? "#2f6a3a" : "#68c25a"));
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);
    const road = new T.Mesh(new T.PlaneGeometry(7, 200), B.mat(night ? "#3a3d48" : "#5a5e6a"));
    road.rotation.x = -Math.PI / 2;
    road.position.set(0, 0.02, -60);
    road.receiveShadow = true;
    scene.add(road);
    const dashM = B.mat("#f2c84b");
    for (let z = 30; z > -150; z -= 4) {
      const d = new T.Mesh(new T.PlaneGeometry(0.22, 1.8), dashM);
      d.rotation.x = -Math.PI / 2;
      d.position.set(0, 0.03, z);
      scene.add(d);
    }
    [-4.6, 4.6].forEach((x) => scene.add(B.box(2.2, 0.2, 200, night ? "#8c8f99" : "#cfd2d8", x, 0.1, -60)));
    const houses = [];
    const cols = ["#f2b8a2", "#a9d3f2", "#f6e1a0", "#c7e7b8", "#e7c3ea", "#f7c9a4", "#b8d8d0", "#f0a8a8"];
    const roofs = ["#7e4a46", "#465a8a", "#8a5a3a", "#5a7a4a", "#6a4a7a"];
    let k = 0;
    for (let z = 22; z > -48; z -= 10) {
      [-1, 1].forEach((sd) => {
        const h = B.house({ x: sd * 11.5, z, ry: sd > 0 ? -Math.PI / 2 : Math.PI / 2, color: cols[k % cols.length], roof: roofs[k % roofs.length], night, window: k % 3 === 0 ? "#9fd2ff" : "#ffcf7a", h: 4.2 + (k % 3) * 0.5 });
        scene.add(h);
        houses.push(h);
        const f = B.fence(-3.6, 3.6, 0);
        f.position.set(sd * 7.2, 0, z);
        f.rotation.y = Math.PI / 2;
        scene.add(f);
        scene.add(B.tree(sd * 7.8, z - 5, 0.9, k * 3 + 1));
        k++;
      });
    }
    for (let z = 18; z > -48; z -= 13) [-1, 1].forEach((sd) => scene.add(B.lamp(sd * 5.4, z + sd * 3, night)));
    // town square + tower
    const square = new T.Mesh(new T.CircleGeometry(16, 40), B.mat(night ? "#7c7469" : "#d9cfbf"));
    square.rotation.x = -Math.PI / 2;
    square.position.set(0, 0.04, -66);
    square.receiveShadow = true;
    scene.add(square);
    const tower = B.tower({ z: -72, night });
    scene.add(tower.group);
    // far background trees
    const r = B.rng(99);
    for (let i = 0; i < 40; i++) scene.add(B.tree((r() - 0.5) * 140, -90 - r() * 60, 1.2 + r(), 200 + i));
    for (let i = 0; i < 20; i++) { const sd = r() < 0.5 ? -1 : 1; scene.add(B.tree(sd * (24 + r() * 30), 30 - r() * 110, 1 + r() * 0.6, 300 + i)); }
    return { houses, tower, ground };
  };

  // ---------- tower interior props ----------
  B.hourglass = function (o = {}) {
    const g = new T.Group();
    const frame = B.mat(o.frame || "#7a4f2c", { p: { roughness: 0.6 } });
    const gold = B.mat("#e0b23c", { p: { metalness: 0.7, roughness: 0.35 } });
    const capT = new T.Mesh(new T.CylinderGeometry(0.62, 0.62, 0.14, 20), frame);
    capT.position.y = 1.1;
    const capB = capT.clone();
    capB.position.y = -1.1;
    g.add(capT, capB);
    [0, 2.09, 4.19].forEach((a) => {
      const post = new T.Mesh(new T.CylinderGeometry(0.04, 0.04, 2.2, 6), gold);
      post.position.set(Math.cos(a) * 0.52, 0, Math.sin(a) * 0.52);
      g.add(post);
    });
    const glass = new T.MeshStandardMaterial({ color: 0xcfe9ff, transparent: true, opacity: 0.22, roughness: 0.05, metalness: 0.1, depthWrite: false });
    const top = new T.Mesh(new T.ConeGeometry(0.46, 1.0, 20, 1, true), glass);
    top.rotation.x = Math.PI;
    top.position.y = 0.52;
    const bot = new T.Mesh(new T.ConeGeometry(0.46, 1.0, 20, 1, true), glass);
    bot.position.y = -0.52;
    g.add(top, bot);
    const sandM = new T.MeshBasicMaterial({ color: new T.Color(o.sand || "#ffc23a").multiplyScalar(o.sandGlow ?? 2.4) });
    // upper sand: inverted cone that shrinks as time drains; lower sand: pile that grows
    const upPiv = new T.Group();
    upPiv.position.y = 0.04;
    const up = new T.Mesh(new T.ConeGeometry(0.4, 0.88, 20), sandM);
    up.rotation.x = Math.PI;
    up.position.y = 0.44;
    upPiv.add(up);
    const lowPiv = new T.Group();
    lowPiv.position.y = -1.0;
    const low = new T.Mesh(new T.ConeGeometry(0.4, 0.6, 20), sandM);
    low.position.y = 0.3;
    lowPiv.add(low);
    g.add(upPiv, lowPiv);
    let tag = null;
    if (o.name) {
      tag = new T.Mesh(new T.PlaneGeometry(1.1, 0.34), new T.MeshBasicMaterial({
        map: B.canvasTex(256, 80, (cg, w, h) => {
          cg.fillStyle = "#f3e6c4"; roundRect(cg, 2, 2, w - 4, h - 4, 14); cg.fill();
          cg.strokeStyle = "#8a5a2a"; cg.lineWidth = 5; roundRect(cg, 4, 4, w - 8, h - 8, 12); cg.stroke();
          cg.fillStyle = "#3a2210"; cg.textAlign = "center"; cg.textBaseline = "middle";
          cg.font = `700 46px ${B.FONT}`; cg.fillText(o.name, w / 2, h / 2 + 2);
        }),
        transparent: true,
      }));
      tag.position.set(0, -1.42, 0.3);
      g.add(tag);
    }
    const H = {
      group: g, tag, sandM,
      setFill(f) {
        f = clamp(f, 0.001, 1);
        up.scale.set(Math.sqrt(f), f, Math.sqrt(f));
        up.position.y = 0.44 * f + 0.0;
        const lf = 1 - f;
        low.scale.set(0.3 + 0.7 * Math.sqrt(lf), Math.max(0.02, lf), 0.3 + 0.7 * Math.sqrt(lf));
        low.position.y = 0.3 * Math.max(0.02, lf);
      },
    };
    H.setFill(o.fill ?? 0.7);
    return H;
  };
  B.gear = function (radius, teeth, thick, mat) {
    const s = new T.Shape();
    const inner = radius * 0.86, outer = radius;
    const n = teeth * 4;
    for (let i = 0; i <= n; i++) {
      const a = (i / n) * Math.PI * 2;
      const r = i % 4 < 2 ? outer : inner;
      const x = Math.cos(a) * r, y = Math.sin(a) * r;
      if (i === 0) s.moveTo(x, y); else s.lineTo(x, y);
    }
    const hole = new T.Path();
    hole.absarc(0, 0, radius * 0.2, 0, Math.PI * 2, true);
    s.holes.push(hole);
    for (let k = 0; k < 4; k++) {
      const a = (k / 4) * Math.PI * 2 + Math.PI / 4;
      const h = new T.Path();
      h.absarc(Math.cos(a) * radius * 0.52, Math.sin(a) * radius * 0.52, radius * 0.18, 0, Math.PI * 2, true);
      s.holes.push(h);
    }
    const geo = new T.ExtrudeGeometry(s, { depth: thick, bevelEnabled: true, bevelSize: thick * 0.15, bevelThickness: thick * 0.15, bevelSegments: 1, curveSegments: 6 });
    geo.translate(0, 0, -thick / 2);
    const m = new T.Mesh(geo, mat || B.mat("#c9973a", { p: { metalness: 0.75, roughness: 0.35 } }));
    m.castShadow = true;
    return m;
  };
  // glowing particle streams along quadratic curves: list of {a:[x,y,z], b:[x,y,z], c:[x,y,z]}
  B.streams = function (curves, perCurve, color, size) {
    const n = curves.length * perCurve;
    const pos = new Float32Array(n * 3);
    const geo = new T.BufferGeometry();
    geo.setAttribute("position", new T.BufferAttribute(pos, 3));
    const tex = B.canvasTex(64, 64, (g) => {
      const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
      gr.addColorStop(0, "rgba(255,255,255,1)");
      gr.addColorStop(0.4, "rgba(255,255,255,0.6)");
      gr.addColorStop(1, "rgba(255,255,255,0)");
      g.fillStyle = gr;
      g.fillRect(0, 0, 64, 64);
    });
    const mat = new T.PointsMaterial({ size: size || 0.25, map: tex, transparent: true, depthWrite: false, blending: T.AdditiveBlending, color: new T.Color(color).multiplyScalar(3) });
    const pts = new T.Points(geo, mat);
    pts.frustumCulled = false;
    const rr = B.rng(5);
    const offs = Array.from({ length: n }, () => rr());
    return {
      points: pts, mat,
      // t = time, speed = curve lengths per second, amount = 0..1 visible fraction (fills from start), reverse
      update(t, speed = 0.35, amount = 1, reverse = false) {
        for (let ci = 0; ci < curves.length; ci++) {
          const C = curves[ci];
          for (let j = 0; j < perCurve; j++) {
            const idx = ci * perCurve + j;
            let u = (offs[idx] + t * speed) % 1;
            if (reverse) u = 1 - u;
            const vis = reverse ? 1 - u <= amount : u <= amount;
            const a = C.a, b = C.b, c = C.c, iu = 1 - u;
            const x = iu * iu * a[0] + 2 * iu * u * c[0] + u * u * b[0];
            const y = iu * iu * a[1] + 2 * iu * u * c[1] + u * u * b[1];
            const z = iu * iu * a[2] + 2 * iu * u * c[2] + u * u * b[2];
            pos[idx * 3] = x;
            pos[idx * 3 + 1] = vis ? y : -999;
            pos[idx * 3 + 2] = z;
          }
        }
        geo.attributes.position.needsUpdate = true;
      },
    };
  };
  // a close-up forearm with the wrist clock, filling the frame; screen faces +z
  B.wristProp = function (o = {}) {
    const g = new T.Group();
    const skin = B.mat(o.skin || "#f4c89f");
    const sleeve = B.mat(o.sleeve || "#d94c3d");
    g.add(B.box(6, 2.2, 2.4, skin, 0, 0, 0, 0.35));
    g.add(B.box(3.2, 2.6, 2.8, sleeve, -4.4, 0, 0, 0.35));
    g.add(B.box(2.2, 2.0, 2.3, skin, 3.9, -0.1, 0.05, 0.5));
    const band = B.box(2.1, 2.5, 2.7, B.mat("#24242c", { p: { roughness: 0.35, metalness: 0.3 } }), 0.6, 0, 0, 0.3);
    g.add(band);
    const bezel = B.box(2.6, 2.0, 0.3, B.mat("#1a1a20", { p: { roughness: 0.25, metalness: 0.5 } }), 0.6, 0, 1.3, 0.22);
    g.add(bezel);
    const tex = B.canvasTex(512, 384, (cg) => { cg.fillStyle = "#000"; cg.fillRect(0, 0, 512, 384); });
    const scr = new T.Mesh(new T.PlaneGeometry(2.24, 1.66), new T.MeshBasicMaterial({ map: tex, toneMapped: false }));
    scr.position.set(0.6, 0, 1.47);
    g.add(scr);
    let gain = 1;
    return {
      group: g, screen: scr,
      set(s, glow = 1.6) {
        B.setScreen(tex, s);
        if (glow !== gain) { gain = glow; scr.material.color.setScalar(glow); }
      },
    };
  };

  // ---------- the cast ----------
  const CAST = {
    leo: { shirt: "#d94c3d", shirt2: "#f4f1ea", style: "jacket", pants: "#33406e", hair: "spiky", hairColor: "#7a4a22", faceOpts: { freckles: true } },
    mia: { shirt: "#7b5cd6", style: "hoodie", pants: "#2c2c3a", hair: "bob", hairColor: "#1b1414", skin: "#eab993" },
    mom: { shirt: "#2fa39a", shirt2: "#e9f7f2", style: "cardigan", pants: "#3a3a4a", hair: "bun", hairColor: "#6b3f1d" },
    mayor: { shirt: "#2a2340", shirt2: "#f4f1ea", style: "suit", pants: "#1d1a2c", hair: "tophat", skin: "#f0c49a", monocle: true, faceOpts: { mustache: "#d8d8de", wrinkles: true }, face: "sly" },
    baker: { shirt: "#e3a35a", shirt2: "#fbfbf7", style: "apron", pants: "#4a3a2a", hair: "chef", skin: "#e2a77a", faceOpts: { mustache: "#5a3a1a" } },
    mailman: { shirt: "#4a78c9", shirt2: "#2e4f9e", style: "postal", pants: "#2e3b5c", hair: "cap", hairColor: "#2b1d14", skin: "#a8724a" },
  };
  B.cast = (name, extra) => B.person(Object.assign({}, CAST[name], extra || {}));
  B.kid = (i, extra) => {
    const shirts = ["#f2a93b", "#4fb3d9", "#e05a8a", "#6cc46a", "#9a7bd1", "#f06a4a"];
    const hairs = ["short", "pony", "spiky", "bob", "short", "pony"];
    const hc = ["#2b1d14", "#c4572b", "#e3c35a", "#1b1414", "#6b3f1d", "#2b1d14"];
    const sk = ["#f4c89f", "#c98d5e", "#8d5a3b", "#eab993", "#f4c89f", "#a8724a"];
    return B.person(Object.assign({ shirt: shirts[i % 6], hair: hairs[i % 6], hairColor: hc[i % 6], skin: sk[i % 6], pants: i % 2 ? "#2c2c3a" : "#33406e", style: i % 3 === 0 ? "hoodie" : "plain" }, extra || {}));
  };
  B.addHolo = (p, text, color, y = 3.55) => {
    const h = B.holo();
    h.position.set(0, y, 0);
    h.userData.set(text, color);
    p.root.add(h);
    p.holo = h;
    return h;
  };
  B.RED = "#ff4a4a";
  B.GREEN = "#7dffb0";
  B.GOLD = "#ffd257";

  // ---------- Leo's bedroom (morning) ----------
  B.bedroom = function (scene) {
    const g = new T.Group();
    const floor = B.box(16, 0.4, 16, B.mat("#c79a6b"), 0, -0.2, 0);
    g.add(floor);
    const wallM = B.mat("#a9d1f2");
    g.add(B.box(16, 9, 0.4, wallM, 0, 4.5, -8));
    g.add(B.box(0.4, 9, 16, wallM, -8, 4.5, 0));
    g.add(B.box(0.4, 9, 16, wallM, 8, 4.5, 0));
    g.add(B.box(16, 0.4, 16, B.mat("#eef4fa"), 0, 9, 0));
    // window with morning light
    g.add(B.box(4.6, 3.6, 0.3, B.mat("#ffffff"), -2.5, 5, -7.8));
    const sky = new T.Mesh(new T.PlaneGeometry(4.0, 3.0), B.glow("#ffe7b0", 2.6));
    sky.position.set(-2.5, 5, -7.6);
    g.add(sky);
    g.add(B.box(0.2, 3.0, 0.1, B.mat("#ffffff"), -2.5, 5, -7.55));
    g.add(B.box(4.0, 0.2, 0.1, B.mat("#ffffff"), -2.5, 5, -7.55));
    // bed
    g.add(B.box(3.6, 1.0, 6.2, B.mat("#8a5a3a"), 4.8, 0.5, -3.8, 0.1));
    g.add(B.box(3.4, 0.5, 5.4, B.mat("#3f6fc9"), 4.8, 1.15, -3.3, 0.15));
    g.add(B.box(2.6, 0.5, 1.2, B.mat("#f7f4ee"), 4.8, 1.4, -6.2, 0.2));
    g.add(B.box(3.8, 2.6, 0.4, B.mat("#8a5a3a"), 4.8, 1.3, -7.0, 0.1));
    // desk + poster + rug
    g.add(B.box(3.4, 0.2, 1.8, B.mat("#d8b48a"), -5.8, 2.2, -6.6));
    g.add(B.box(0.2, 2.2, 1.6, B.mat("#d8b48a"), -7.3, 1.1, -6.6));
    g.add(B.box(0.2, 2.2, 1.6, B.mat("#d8b48a"), -4.3, 1.1, -6.6));
    const poster = new T.Mesh(new T.PlaneGeometry(2.2, 3.0), new T.MeshStandardMaterial({
      map: B.canvasTex(220, 300, (cg, w, h) => {
        cg.fillStyle = "#1e2a5a"; cg.fillRect(0, 0, w, h);
        cg.fillStyle = "#ffd257"; for (let i = 0; i < 30; i++) { cg.fillRect((i * 53) % w, (i * 97) % h, 4, 4); }
        cg.fillStyle = "#e05a3a"; cg.beginPath(); cg.moveTo(110, 60); cg.lineTo(150, 220); cg.lineTo(70, 220); cg.fill();
        cg.fillStyle = "#fff"; cg.font = `700 34px ${B.FONT}`; cg.textAlign = "center"; cg.fillText("SPACE!", 110, 270);
      }), roughness: 0.8,
    }));
    poster.position.set(-7.75, 5.2, -2);
    poster.rotation.y = Math.PI / 2;
    g.add(poster);
    const rug = new T.Mesh(new T.CircleGeometry(3, 32), B.mat("#e5c25a"));
    rug.rotation.x = -Math.PI / 2;
    rug.position.set(0, 0.02, 0);
    g.add(rug);
    // door (where mom stands)
    g.add(B.box(2.4, 4.6, 0.2, B.mat("#f2efe9"), 7.85, 2.3, 3.5));
    scene.add(g);
    const sunbeam = new T.SpotLight(0xffe2b0, 900, 40, 0.5, 0.6, 1.5);
    sunbeam.position.set(-2.5, 8, -14);
    sunbeam.target.position.set(1, 0, 2);
    sunbeam.castShadow = true;
    scene.add(sunbeam, sunbeam.target);
    return g;
  };

  // ---------- inside the clock tower ----------
  B.interior = function (scene, o = {}) {
    scene.background = new T.Color("#0c0816");
    scene.fog = new T.Fog(0x120a22, 18, 60);
    const g = new T.Group();
    scene.add(g);
    const floor = new T.Mesh(new T.CylinderGeometry(26, 26, 0.6, 48), B.mat("#2a2238"));
    floor.position.y = -0.3;
    floor.receiveShadow = true;
    g.add(floor);
    const ring = new T.Mesh(new T.RingGeometry(9, 9.4, 64), B.glow("#ffb340", 1.4));
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.02;
    g.add(ring);
    const wall = new T.Mesh(new T.CylinderGeometry(26, 26, 44, 48, 1, true), B.mat("#34274a", { p: { side: T.BackSide } }));
    wall.position.y = 21;
    g.add(wall);
    // tall moonlit windows
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2 + 0.3;
      const w = new T.Mesh(new T.PlaneGeometry(2.4, 9), B.glow("#5a7dff", 1.2));
      w.position.set(Math.sin(a) * 25.7, 14, Math.cos(a) * 25.7);
      w.lookAt(0, 14, 0);
      g.add(w);
    }
    // pillars
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2;
      const pl = new T.Mesh(new T.CylinderGeometry(0.9, 1.1, 40, 12), B.mat("#4a3a5e"));
      pl.position.set(Math.sin(a) * 22, 20, Math.cos(a) * 22);
      pl.castShadow = true;
      g.add(pl);
    }
    scene.add(new T.HemisphereLight(0x8a7aff, 0x1a1020, 1.1));
    const key = new T.PointLight(0xffb84a, 900, 60, 2);
    key.position.set(0, 10, -2);
    key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024);
    scene.add(key);
    const moon = new T.DirectionalLight(0x8fa8ff, 1.2);
    moon.position.set(-20, 30, 30);
    scene.add(moon);
    // giant clock, gears behind it
    const CL = [0, 10, -10];
    const clock = B.clock(6.5, { glow: 0.62, face: "#ffe9b8", rim: "#7a4a18", ink: "#5a2e08", hand: "#3a1e08" });
    clock.group.position.set(...CL);
    g.add(clock.group);
    const rim = new T.Mesh(new T.TorusGeometry(6.6, 0.45, 12, 64), B.mat("#e0b23c", { p: { metalness: 0.8, roughness: 0.3 } }));
    rim.position.set(...CL);
    g.add(rim);
    const gearM = B.mat("#b8862e", { p: { metalness: 0.8, roughness: 0.35 } });
    const gears = [
      [9.5, 4.6, 14, [-6.5, 15.5, -12.5]], [-1, 3.4, 11, [6.8, 16.5, -12.4]], [1, 5.2, 16, [7.5, 5.0, -12.2]],
      [-1, 3.0, 10, [-7.5, 4.5, -12.2]], [1, 2.2, 8, [-3, 18.5, -11.6]], [-1, 2.6, 9, [3.5, 1.8, -11.2]],
    ].map(([dir, r, n, pos]) => {
      const gm = B.gear(r, n, 0.6, gearM);
      gm.position.set(...pos);
      g.add(gm);
      return { m: gm, dir: Math.sign(dir) * (6 / r) };
    });
    // lever beside the clock
    const lever = new T.Group();
    lever.position.set(7.5, 0, -4);
    g.add(lever);
    lever.add(B.box(2.6, 1.4, 2.0, B.mat("#3b3346", { p: { metalness: 0.6, roughness: 0.4 } }), 0, 0.7, 0, 0.12));
    const lpiv = new T.Group();
    lpiv.position.set(0, 1.4, 0);
    lever.add(lpiv);
    const stick = new T.Mesh(new T.CylinderGeometry(0.16, 0.16, 3.6, 12), B.mat("#c9cbd4", { p: { metalness: 0.8, roughness: 0.25 } }));
    stick.position.y = 1.8;
    lpiv.add(stick);
    const knob = new T.Mesh(new T.SphereGeometry(0.45, 20, 14), B.mat("#e22d2d", { emissive: "#ff2020", ei: 1.6 }));
    knob.position.y = 3.7;
    lpiv.add(knob);
    lpiv.rotation.z = 0.6;
    // hourglasses floating in rings
    const r = B.rng(31);
    const glasses = [];
    for (let i = 0; i < 64; i++) {
      const a = r() * Math.PI * 2;
      const rad = 10 + r() * 11;
      const x = Math.sin(a) * rad, z = Math.cos(a) * rad;
      if (z < -6 && Math.abs(x) < 9) continue;
      const hg = B.hourglass({ fill: 0.15 + r() * 0.6 });
      hg.group.position.set(x, 3 + r() * 16, z);
      hg.group.rotation.y = r() * 6;
      const s = 0.8 + r() * 0.5;
      hg.group.scale.setScalar(s);
      g.add(hg.group);
      glasses.push(Object.assign(hg, { base: hg.group.position.clone(), ph: r() * 6 }));
    }
    // named hourglasses in a row near the entrance path
    const named = {};
    [["BOB", -3.6, 4.2, 9.0, 0.08], ["ROSA", -1.2, 4.8, 8.4, 0.12], ["MAX", 1.2, 4.3, 8.8, 0.1], ["LEO", 3.6, 4.9, 8.4, 0.035], ["MAYOR", -8, 11, -2, 1.0]].forEach(([n, x, y, z, f]) => {
      const hg = B.hourglass({ name: n, fill: f });
      hg.group.position.set(x, y, z);
      g.add(hg.group);
      named[n] = Object.assign(hg, { base: hg.group.position.clone(), ph: x });
      glasses.push(named[n]);
    });
    // streams: every hourglass -> centre of the giant clock
    const target = [CL[0], CL[1], CL[2] + 0.5];
    const curves = glasses.map((h) => {
      const p = h.base;
      return { a: [p.x, p.y - 1.1, p.z], b: target, c: [(p.x + target[0]) / 2, Math.max(p.y, target[1]) + 4, (p.z + target[2]) / 2] };
    });
    const streams = B.streams(curves, 30, "#ffc23a", 0.5);
    g.add(streams.points);
    // entrance doors
    const doors = [-1, 1].map((sd) => {
      const piv = new T.Group();
      piv.position.set(sd * 3.2, 0, 22);
      piv.add(B.box(3.2, 8, 0.5, B.mat("#5a3424"), -sd * 1.6, 4, 0, 0.08));
      piv.add(B.box(0.3, 0.3, 0.3, B.mat("#e0b23c"), -sd * 2.8, 4, -0.35));
      g.add(piv);
      return piv;
    });
    g.add(B.box(8, 1.2, 1.2, B.mat("#4a3a5e"), 0, 8.6, 22));
    return {
      group: g, clock, gears, lever: lpiv, knob, glasses, named, streams, doors, key, clockPos: CL,
      // float / tick everything; gearSpeed scales the rotation (0 = stopped); spin accumulates externally
      animate(t, o2 = {}) {
        const gs = o2.gearAngle ?? t * 0.6;
        gears.forEach((gm) => (gm.m.rotation.z = gs * gm.dir));
        glasses.forEach((h) => {
          h.group.position.y = h.base.y + Math.sin(t * 0.9 + h.ph) * 0.18;
          h.group.rotation.x = o2.flip !== undefined ? Math.PI * B.outBack(clamp(o2.flip * 1.4 - (h.ph % 1) * 0.4)) : 0;
        });
        clock.set(o2.h ?? 11, o2.m ?? 59 + Math.sin(t * 6) * 0.2);
      },
    };
  };
  B.sandBurst = function (count, seed) {
    const geo = new T.BoxGeometry(0.16, 0.16, 0.16);
    const m = new T.InstancedMesh(geo, B.mat("#e2c27a"), count);
    m.castShadow = true;
    const r = B.rng(seed || 3);
    const data = Array.from({ length: count }, () => ({
      p: [(r() - 0.5) * 1.1, 0.1 + r() * 2.9, (r() - 0.5) * 0.6],
      v: [(r() - 0.5) * 2.5, r() * 1.5, (r() - 0.5) * 2.5],
      d: r() * 0.5,
      s: 0.6 + r() * 0.9,
    }));
    const M = new T.Matrix4(), q = new T.Quaternion(), e = new T.Euler(), sc = new T.Vector3(), pos = new T.Vector3();
    return {
      mesh: m,
      set(k) { // 0 = body shape, 1 = settled pile on the floor
        data.forEach((d, i) => {
          const u = clamp((k - d.d) / (1 - d.d) * 1.2);
          const fall = u * u;
          const pileY = 0.08 + Math.max(0, (0.6 - Math.hypot(d.p[0], d.p[2])) * 0.6) * (d.p[1] / 3);
          pos.set(d.p[0] + d.v[0] * u * 0.6, lerp(d.p[1], pileY, fall) + d.v[1] * Math.sin(u * Math.PI) * 0.3, d.p[2] + d.v[2] * u * 0.6);
          e.set(u * d.v[0] * 3, u * 2, u * d.v[2] * 3);
          q.setFromEuler(e);
          sc.setScalar(d.s);
          M.compose(pos, q, sc);
          m.setMatrixAt(i, M);
        });
        m.instanceMatrix.needsUpdate = true;
      },
    };
  };
})();
