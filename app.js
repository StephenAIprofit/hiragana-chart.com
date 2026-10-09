const cache = new Map();
let currentAudio = null;
let token = 0;

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
  const utter = new SpeechSynthesisUtterance(kana);
  utter.lang = "ja-JP";
  window.speechSynthesis.speak(utter);
}

function playKana(kana, romaji) {
  stopAudio();
  const audio = new Audio("audio/" + romaji + ".mp3");
  currentAudio = audio;
  const played = audio.play();
  if (played && played.catch) played.catch(() => speakFallback(kana));
  audio.addEventListener("error", () => speakFallback(kana), { once: true });
}

function firstPoint(d) {
  const match = /M\s*(-?\d+(?:\.\d+)?)\s*,?\s*(-?\d+(?:\.\d+)?)/.exec(d || "");
  if (!match) return null;
  return [Number(match[1]), Number(match[2])];
}

function strokeNo(id) {
  const match = /d(\d+)/.exec(id || "");
  return match ? Number(match[1]) : 0;
}

async function loadSvg(kana) {
  const code = kana.codePointAt(0);
  if (cache.has(code)) return cache.get(code);
  const text = await fetch("strokes/" + code + ".svg").then((res) => {
    if (!res.ok) throw new Error(String(res.status));
    return res.text();
  });
  cache.set(code, text);
  return text;
}

async function drawStrokes(kana) {
  const stage = document.querySelector("#glyph");
  const mine = ++token;
  stage.innerHTML = "";
  const text = await loadSvg(kana);
  if (mine !== token) return;
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 1024 1024");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", kana + " stroke order");
  const shapes = [...doc.querySelectorAll("path[id]")].filter((path) => strokeNo(path.id));
  const lines = [...doc.querySelectorAll("path[clip-path]")];
  const starts = new Map();
  lines.forEach((path) => {
    const no = strokeNo(path.getAttribute("clip-path"));
    const point = firstPoint(path.getAttribute("d"));
    if (!no || !point || point[0] < 0 || starts.has(no)) return;
    starts.set(no, point);
  });
  const numbers = [...new Set(shapes.map((path) => strokeNo(path.id)))].sort((a, b) => a - b);
  numbers.forEach((no, index) => {
    shapes.filter((path) => strokeNo(path.id) === no).forEach((path) => {
      const drawn = document.createElementNS("http://www.w3.org/2000/svg", "path");
      drawn.setAttribute("d", path.getAttribute("d"));
      drawn.setAttribute("class", "glyph-stroke");
      drawn.style.animationDelay = (index * 0.7) + "s";
      svg.appendChild(drawn);
    });
    const point = starts.get(no);
    if (!point) return;
    const badge = document.createElementNS("http://www.w3.org/2000/svg", "g");
    badge.setAttribute("class", "stroke-badge");
    badge.style.animationDelay = (index * 0.7) + "s";
    badge.innerHTML = `<circle cx="${point[0]}" cy="${point[1]}" r="36"/><text x="${point[0]}" y="${point[1] + 12}" text-anchor="middle">${no}</text>`;
    svg.appendChild(badge);
  });
  stage.appendChild(svg);
}

const reading = document.querySelector("#reading");
const order = document.querySelector("#order");

function select(button, opts) {
  opts = opts || {};
  document.querySelectorAll(".cell").forEach((el) => el.setAttribute("aria-pressed", "false"));
  button.setAttribute("aria-pressed", "true");
  reading.textContent = button.dataset.romaji;
  order.textContent = button.dataset.order;
  drawStrokes(button.dataset.kana);
  if (opts.pushHash !== false) history.replaceState(null, "", "#" + button.dataset.romaji);
  if (opts.play !== false) playKana(button.dataset.kana, button.dataset.romaji);
}

function currentButton() {
  return document.querySelector('.cell[aria-pressed="true"]') || document.querySelector(".cell");
}

document.querySelectorAll(".cell").forEach((button) => {
  button.addEventListener("click", () => select(button));
});
document.querySelector("#play").addEventListener("click", () => {
  const button = currentButton();
  playKana(button.dataset.kana, button.dataset.romaji);
});
document.querySelector("#replay-strokes").addEventListener("click", () => drawStrokes(currentButton().dataset.kana));
document.querySelector("#print").addEventListener("click", () => window.print());

const romaji = (location.hash || "").replace("#", "").trim().toLowerCase();
const initial = romaji && document.querySelector('.cell[data-romaji="' + CSS.escape(romaji) + '"]');
select(initial || document.querySelector(".cell"), { play: false, pushHash: false });
