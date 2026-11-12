// Character page: audio and stroke animation replay. All content is static.
(function () {
  let currentAudio = null;
  function speak(text) {
    if (!window.speechSynthesis) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "ja-JP";
    window.speechSynthesis.speak(u);
  }
  function play(name, fallback) {
    if (currentAudio) { try { currentAudio.pause(); } catch (e) {} }
    const audio = new Audio("/audio/" + name + ".mp3");
    currentAudio = audio;
    const run = audio.play();
    if (run && run.catch) run.catch(() => speak(fallback));
    audio.addEventListener("error", () => speak(fallback), { once: true });
  }
  const btn = document.getElementById("play");
  if (btn) btn.addEventListener("click", () => play(btn.dataset.audio, btn.dataset.kana));
  const replay = document.getElementById("replay-strokes");
  const stage = document.getElementById("glyph");
  if (replay && stage) replay.addEventListener("click", () => {
    // Re-inserting the SVG markup restarts the CSS animation.
    stage.innerHTML = stage.innerHTML;
  });
})();
