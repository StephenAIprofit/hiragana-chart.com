const STROKES = {
  "あ": ["M18 28 H78", "M32 18 V70 Q32 84 48 84", "M46 40 Q70 36 74 58 Q70 78 48 72 Q40 66 52 52"],
  "い": ["M34 18 Q28 48 36 82", "M62 30 Q56 52 64 74"],
  "う": ["M40 24 H62", "M28 36 Q48 30 70 48 Q74 70 46 78 Q30 74 34 58"],
  "え": ["M24 30 H76", "M34 22 V58 Q34 78 62 78 H78"],
  "お": ["M22 26 H74", "M36 18 V68 Q36 82 50 82", "M50 42 Q74 40 76 60 Q70 78 50 70"],
  "か": ["M24 30 H78", "M36 18 V82", "M42 46 Q68 40 76 62 Q70 80 50 74"],
  "き": ["M28 24 H74", "M28 42 H70", "M40 16 V78", "M34 62 Q34 84 56 84 H76"],
  "く": ["M70 22 Q34 46 70 78"],
  "け": ["M30 16 V82", "M36 34 H74", "M36 54 Q60 50 74 70 Q68 84 48 78"],
  "こ": ["M28 36 H74", "M24 62 H78"],
  "さ": ["M26 28 H76", "M40 18 V58", "M36 58 Q36 82 62 82 H80"],
  "し": ["M62 18 Q40 40 42 62 Q50 84 72 72"],
  "す": ["M30 30 H72 V52", "M34 52 Q34 80 60 80 Q78 80 70 60"],
  "せ": ["M24 30 H78", "M38 18 V70", "M30 58 H62 Q78 58 74 78 H40"],
  "そ": ["M30 24 H70 L40 46 H68 Q74 70 46 78 Q28 74 36 58"],
  "た": ["M24 28 H78", "M40 16 V62 Q40 80 58 80", "M58 46 H74", "M58 60 H76"],
  "ち": ["M36 26 H64", "M30 34 Q55 28 68 50 Q70 76 42 80 Q30 74 40 58"],
  "つ": ["M28 40 Q50 28 72 46 Q68 70 42 68"],
  "て": ["M24 32 H78 V70 Q78 84 52 84"],
  "と": ["M48 22 Q62 28 58 42", "M30 48 H62 V78 H36"],
  "な": ["M26 28 H78", "M40 16 V80", "M46 40 Q70 34 74 54", "M48 58 Q72 62 68 82 Q46 86 44 68"],
  "に": ["M36 20 Q30 48 38 80", "M46 36 H74", "M46 58 H76"],
  "ぬ": ["M34 18 Q28 48 36 82", "M42 36 Q68 30 72 52 Q66 78 44 70 Q40 60 52 54"],
  "ね": ["M34 18 Q28 50 36 82", "M42 34 Q70 28 74 50 Q68 78 46 72 Q40 62 54 56 Q66 62 60 74"],
  "の": ["M58 24 Q30 30 32 54 Q36 80 64 76 Q80 70 70 50 Q62 36 48 42"],
  "は": ["M30 16 V82", "M38 32 H74", "M38 52 Q62 46 74 66 Q68 84 46 76"],
  "ひ": ["M40 22 Q70 28 68 50 Q60 78 36 70 Q28 60 46 52 Q64 46 58 64"],
  "ふ": ["M46 18 H64", "M34 30 H56", "M30 40 Q48 34 62 50", "M40 52 Q36 78 58 78 Q76 76 70 58"],
  "へ": ["M24 46 L50 28 L76 50"],
  "ほ": ["M30 16 V82", "M38 30 H76", "M38 50 H74", "M40 58 Q64 54 74 74 Q66 86 44 78"],
  "ま": ["M24 26 H78", "M40 16 V78", "M46 42 Q72 38 74 58 Q66 80 46 70"],
  "み": ["M36 24 Q50 20 58 34", "M30 40 Q52 36 66 54 Q64 80 38 76 Q30 68 44 60"],
  "む": ["M40 22 Q54 18 60 32", "M28 40 Q50 34 68 52 Q70 80 40 78", "M48 50 L62 66"],
  "め": ["M36 22 Q58 16 64 34", "M30 40 Q52 36 70 56 Q66 84 40 78 Q32 66 50 58 Q64 64 58 76"],
  "も": ["M36 20 Q28 36 40 42", "M30 50 H74", "M28 68 H76"],
  "や": ["M36 22 Q50 16 56 32", "M26 40 Q50 34 68 54 Q70 82 38 78", "M48 52 L64 68"],
  "ゆ": ["M58 18 Q70 36 62 58 Q50 78 34 66", "M30 28 Q24 48 34 58"],
  "よ": ["M28 32 H74", "M42 20 V62 Q42 82 64 80 H78"],
  "ら": ["M42 22 H64", "M30 34 Q54 30 66 50 Q66 78 40 76 Q32 68 44 60"],
  "り": ["M36 20 Q30 48 38 80", "M56 28 Q50 52 60 74"],
  "る": ["M34 22 Q58 16 66 36 Q62 58 44 52 Q36 58 48 70 Q62 80 74 68"],
  "れ": ["M32 16 V82", "M38 36 Q64 30 74 52 Q70 80 46 74"],
  "ろ": ["M40 18 V58 Q40 82 64 80 Q80 76 72 58 Q64 46 50 52"],
  "わ": ["M32 16 V62 Q32 82 50 82", "M40 36 Q66 32 74 54 Q70 78 48 70"],
  "を": ["M24 30 H76", "M40 18 V78", "M46 44 Q70 40 72 60 Q64 80 46 70"],
  "ん": ["M30 36 Q52 24 66 46 Q70 70 46 76 Q34 70 42 58"]
};

const SVG_NS = "http://www.w3.org/2000/svg";
const STROKE_MS = 620;   // time to draw one stroke
const STROKE_GAP = 180;  // pause between strokes

function drawStrokes(kana) {
  const board = document.querySelector("#strokes");
  const paths = STROKES[kana] || [];
  board.innerHTML = "";
  paths.forEach((d, i) => {
    const svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("viewBox", "0 0 100 100");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", kana + " stroke " + (i + 1) + " of " + paths.length);
    const guide = document.createElementNS(SVG_NS, "path");
    guide.setAttribute("d", d);
    guide.setAttribute("class", "guide");
    const drawn = document.createElementNS(SVG_NS, "path");
    drawn.setAttribute("d", d);
    drawn.setAttribute("class", "drawn");
    svg.append(guide, drawn);
    board.appendChild(svg);
    // Measure after insertion, then animate the stroke drawing itself.
    let len = 0;
    try { len = drawn.getTotalLength(); } catch (e) { len = 0; }
    if (len > 0) {
      drawn.style.strokeDasharray = String(len);
      drawn.style.strokeDashoffset = String(len);
    }
    // Stroke number sits at the stroke's starting point.
    try {
      const p0 = drawn.getPointAtLength(0);
      const n = document.createElementNS(SVG_NS, "text");
      n.setAttribute("x", String(Math.max(4, Math.min(88, p0.x - 5))));
      n.setAttribute("y", String(Math.max(14, Math.min(96, p0.y - 5))));
      n.setAttribute("class", "stroke-num");
      n.textContent = String(i + 1);
      svg.appendChild(n);
    } catch (e) { /* keep diagram without number */ }
    if (len > 0) {
      // Force layout so the transition starts from the hidden state.
      void drawn.getBoundingClientRect();
      window.setTimeout(() => { drawn.style.strokeDashoffset = "0"; }, 150 + i * (STROKE_MS + STROKE_GAP));
    }
  });
}

// --- Audio: pre-recorded MP3 per kana (consistent on every device),
// with speechSynthesis as a last-resort fallback.
let currentAudio = null;

function stopAudio() {
  if (currentAudio) {
    try { currentAudio.pause(); } catch (e) {}
    currentAudio = null;
  }
  if (window.speechSynthesis) {
    try { window.speechSynthesis.cancel(); } catch (e) {}
  }
}

function speakFallback(kana) {
  if (!window.speechSynthesis) return;
  try {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(kana);
    utter.lang = "ja-JP";
    window.speechSynthesis.speak(utter);
  } catch (e) {}
}

function playKana(kana, romaji) {
  stopAudio();
  try {
    const a = new Audio("audio/" + romaji + ".mp3");
    currentAudio = a;
    const p = a.play();
    if (p && typeof p.catch === "function") {
      p.catch(() => speakFallback(kana));
    }
    a.addEventListener("error", () => speakFallback(kana), { once: true });
  } catch (e) {
    speakFallback(kana);
  }
}

const big = document.querySelector("#big");
const reading = document.querySelector("#reading");
const order = document.querySelector("#order");

function select(button, opts) {
  opts = opts || {};
  const play = opts.play !== false;
  const pushHash = opts.pushHash !== false;
  document.querySelectorAll(".cell").forEach((el) => el.setAttribute("aria-pressed", "false"));
  button.setAttribute("aria-pressed", "true");
  big.textContent = button.dataset.kana;
  reading.textContent = button.dataset.romaji;
  order.textContent = button.dataset.order;
  drawStrokes(button.dataset.kana);
  if (pushHash) {
    try { history.replaceState(null, "", "#" + button.dataset.romaji); } catch (e) {}
  }
  if (play) playKana(button.dataset.kana, button.dataset.romaji);
}

function currentButton() {
  const pressed = document.querySelector('.cell[aria-pressed="true"]');
  return pressed || document.querySelector(".cell");
}

document.querySelectorAll(".cell").forEach((button) => {
  button.addEventListener("click", () => select(button));
});
document.querySelector("#play").addEventListener("click", () => {
  const b = currentButton();
  playKana(b.dataset.kana, b.dataset.romaji);
});
document.querySelector("#replay-strokes").addEventListener("click", () => {
  const b = currentButton();
  drawStrokes(b.dataset.kana);
});
document.querySelector("#print").addEventListener("click", () => window.print());

// Deep link: hiragana-chart.com/#shi selects し on load.
(function init() {
  const romaji = (location.hash || "").replace("#", "").trim().toLowerCase();
  let initial = null;
  if (romaji) {
    initial = document.querySelector('.cell[data-romaji="' + CSS.escape(romaji) + '"]');
  }
  select(initial || document.querySelector(".cell"), { play: false, pushHash: false });
})();
