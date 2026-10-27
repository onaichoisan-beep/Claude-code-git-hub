// Render one jsfxr sound (open source sfxr port, Unlicense) to a WAV file, deterministically.
//
//   node sfxr_gen.mjs <jsfxr_dir> <preset | b58 code from sfxr.me> <seed> <out.wav>
//
// Presets: pickupCoin laserShoot explosion powerUp hitHurt jump blipSelect synth tone click random.
// The seed replaces Math.random while the preset rolls its parameters, so the same seed always
// gives the same sound. Called by osfx.sfxr(); jsfxr is installed into videos/_sfx_library/node.
import { writeFileSync } from "fs";
import { pathToFileURL } from "url";
import { join } from "path";

const [dir, what, seedArg, out] = process.argv.slice(2);
const { sfxr } = await import(pathToFileURL(join(dir, "node_modules", "jsfxr", "sfxr.mjs")).href);

let s = (Number(seedArg) || 1) >>> 0;
Math.random = () => {
  s = (s + 0x6d2b79f5) | 0;
  let t = Math.imul(s ^ (s >>> 15), 1 | s);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const presets = ["pickupCoin", "laserShoot", "explosion", "powerUp", "hitHurt", "jump", "blipSelect", "synth", "tone", "click", "random"];
const sound = presets.includes(what) ? sfxr.generate(what) : sfxr.b58decode(what);
sound.sample_rate = 44100;
sound.sample_size = 16;
const wave = sfxr.toWave(sound);
writeFileSync(out, Buffer.from(wave.wav));
