// Word cues from assets/audio/transcript.json (whisper writes English words, so match on those).
module.exports = (cue) => {
  const C = {
    yr: cue('2013'), down: cue('down'), syndrome: cue('syndrome'),
    doY: cue('two'), out1: cue('out', 10), teen: cue('three', 10.5), out2: cue('out', 14), mono: cue('mono'), out3: cue('out', 20),
    sahi: cue('correct'), trisomy: cue('trisomy'), forty: cue('47', 26), reason: cue('reason', 28), alag: cue('not', 31),
    ab: cue('now', 33), kary: cue('cryotype'), comment: cue('comment'), follow: cue('follow'),
  };
  C.opts = +(C.down + 0.25).toFixed(2);
  return C;
};
