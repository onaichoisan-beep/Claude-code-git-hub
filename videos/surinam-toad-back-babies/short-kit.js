// short-kit.js — shared helpers for the text-only engagement shorts (STYLE_GUIDE.md section 6).
// Load after pixel-engine.js and captions.js. Gives: pop, sky, uiText, uiCentre, bubble, beatsT, tapeT and
// KIT.start(C, T, cfg) which wires PX.setup + the GSAP proxy + the loop (tape-stop -> rewind glitch onto frame 1).
//   T needs: BREAK, HIT (the big moment: 0.25 s dark break before it, a flash on it), STOP, REWIND.
//   cfg: { scenes, sceneAt, cuts, ui, hitCol, post(t, img) }
function pop(t, t0) { var p = clamp01((t - t0) / 0.22); return p <= 0 ? 0 : 0.6 + 0.4 * easeOut(p) + 0.2 * Math.sin(p * Math.PI); }
function sky(stops) { screen(); g.fillStyle = vgrad(0, H, stops); g.fillRect(0, 0, W, H); }
function uiText(str, x, y, S, col) {
  u.fillStyle = col;
  for (var i = 0; i < str.length; i++) { var gl = FONT[str[i]] || FONT[" "]; for (var p = 0; p < 35; p++) if (gl[p] === "1") u.fillRect(x + i * 6 * S + (p % 5) * S, y + Math.floor(p / 5) * S, S, S); }
}
function uiCentre(str, y, S, col) { var w = str.length * 6 * S - S; uiText(str, Math.round(180 - w / 2) + 1, y + 1, S, "#0a0614"); uiText(str, Math.round(180 - w / 2), y, S, col); }
function bubble(x, y, str, col) { var w = str.length * 6 + 5; rrect(x - w / 2, y - 6, w, 11, 2, "#ffffff"); poly([[x - 3, y + 5], [x + 2, y + 5], [x - 5, y + 10]], "#ffffff"); worldText(str, x, y - 3.5, 1, col || "#0a0614"); }
function counterLines(l1, c1, S1, l2, c2) { uiCentre(l1, 18, S1, c1); if (l2) uiCentre(l2, 18 + 7 * S1 + 8, 2, c2 || "#ffffff"); }
// time as seen through the tape-stop (slows to a halt between STOP and REWIND)
function tapeT(t, T) { if (t <= T.STOP) return t; var tau = Math.min(t, T.REWIND) - T.STOP, TT = T.REWIND - T.STOP; return T.STOP + tau - tau * tau / (2 * TT); }
// an accelerating schedule of event times (shared with the audio): rate r0 -> r1 per second between t0 and t1
function schedule(t0, t1, r0, r1, pw) { var a = [], t = t0; while (t < t1) { a.push(t); var u0 = (t - t0) / (t1 - t0); t += 1 / (r0 + (r1 - r0) * Math.pow(u0, pw || 2)); } return a; }
function lastOf(list, t) { var l = -9; for (var i = 0; i < list.length; i++) if (list[i] <= t) l = list[i]; return l; }
function countOf(list, t) { var n = 0; for (var i = 0; i < list.length; i++) if (list[i] <= t) n++; return n; }

var KIT = {
  start: function (C, T, cfg) {
    PX.setup(C, {
      scenes: cfg.scenes, sceneAt: cfg.sceneAt, cuts: cfg.cuts || [], ui: cfg.ui,
      post: function (t, img) {
        if (cfg.post) cfg.post(t, img);
        if (t > T.BREAK && t < T.HIT) tintImg(img, "#0a0614", 0.5);
        if (t >= T.HIT && t < T.HIT + 0.2) tintImg(img, cfg.hitCol || "#ffffff", 1 - (t - T.HIT) / 0.2);
        if (t > T.STOP && t < T.REWIND) tintImg(img, "#0a0614", 0.7 * (t - T.STOP) / (T.REWIND - T.STOP));
      },
      captions: (window.CAPS || []).map(function (c) {
        return { a: c.a, b: c.b, lines: c.segs.map(function (ln) { return ln.map(function (s) { return [s[0], s[1] === "g" ? (C.gold || "#ffc83a") : (C.paper || "#f1eef4")]; }); }) };
      }),
    });
    var DUR = window.DUR;
    function renderLoop(t) {
      if (t < T.REWIND) { PX.render(t); return; }
      PX.render(0);                                   // the loop lands exactly on frame 1 (no cold-open hook)
      var k = 1 - clamp01((t - T.REWIND) / 0.35);
      if (k > 0) { var img = wctx.getImageData(0, 0, PW, PH); glitchRows(img, 12 * k, Math.floor(t * 30)); wctx.putImageData(img, 0, 0); }
    }
    var proxy = { t: 0 };
    var tl = gsap.timeline({ paused: true });
    tl.to(proxy, { t: DUR, duration: DUR, ease: "none", onUpdate: function () { renderLoop(proxy.t); } }, 0);
    PX.render(0);
    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
  },
};
