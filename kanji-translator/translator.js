const SVG_BASE = "https://raw.githubusercontent.com/parsimonhi/animCJK/master/svgsJa/";
let dict = [];
let ready = false;
let currentChar = "";

const form = document.getElementById("form");
const input = document.getElementById("q");
const results = document.getElementById("results");
const stage = document.getElementById("stage");
const stageTitle = document.getElementById("stage-title");
const stageMeta = document.getElementById("stage-meta");
const strokeBox = document.getElementById("stroke");
const strokeCount = document.getElementById("stroke-count");

fetch("/kanji-translator/dict.json")
  .then((res) => res.json())
  .then((data) => { dict = data; ready = true; });

function hasKanji(text) {
  return /[\u4e00-\u9fff]/.test(text);
}
function search(raw) {
  const q = raw.trim().toLowerCase();
  if (!q) return [];
  const kana = window.wanakana ? wanakana.toHiragana(q) : q;
  const katakana = window.wanakana ? wanakana.toKatakana(q) : q;
  const rows = dict.filter((row) => {
    if (row.k.includes(raw.trim())) return true;
    if (row.r === kana || row.r.startsWith(kana) || row.r === katakana || row.r.startsWith(katakana)) return true;
    const en = row.e.toLowerCase();
    if (en === q || en.startsWith(q) || en.split(/,\s*/).some((part) => part === q || part.startsWith(q))) return true;
    return false;
  });
  rows.sort((a, b) => {
    const aExact = a.e.toLowerCase().split(/,\s*/).some((part) => part === q);
    const bExact = b.e.toLowerCase().split(/,\s*/).some((part) => part === q);
    if (aExact !== bExact) return aExact ? -1 : 1;
    return a.k.length - b.k.length;
  });
  return rows.slice(0, 20);
}
function clearStage() {
  stage.hidden = true;
  stageTitle.textContent = "";
  stageMeta.textContent = "";
  strokeBox.innerHTML = "";
  strokeCount.textContent = "";
  currentChar = "";
}
function renderResults(rows, query) {
  clearStage();
  results.innerHTML = "";
  if (!rows.length) {
    results.innerHTML = '<p class="empty">No results for "' + query.replace(/"/g, "") + '".</p>';
    return;
  }
  rows.forEach((row) => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = '<div class="kj">' + row.k + '</div><div class="reading">' + row.r + '</div><div class="meta">' + row.e + '</div>';
    /* result cards do not open a stroke panel */
    results.appendChild(card);
  });
  /* no stroke panel on search results */
}
function strokeNo(id) {
  const match = /d(\d+)/.exec(id || "");
  return match ? Number(match[1]) : 0;
}
function firstPoint(d) {
  const match = /M\s*(-?\d+(?:\.\d+)?)\s*,?\s*(-?\d+(?:\.\d+)?)/.exec(d || "");
  if (!match) return null;
  return [Number(match[1]), Number(match[2])];
}
async function showStroke(char, title, meta, meaning) {
  currentChar = char;
  stage.hidden = false;
  stageTitle.textContent = title;
  stageMeta.textContent = [meta, meaning].filter(Boolean).join(" — ");
  strokeBox.innerHTML = "";
  const code = char.codePointAt(0);
  try {
    const text = await fetch(SVG_BASE + code + ".svg").then((res) => {
      if (!res.ok) throw new Error(String(res.status));
      return res.text();
    });
    drawStrokeSvg(text, char);
  } catch (err) {
    strokeBox.textContent = char;
    strokeCount.textContent = "";
  }
}
function drawStrokeSvg(text, char) {
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 1024 1024");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", char + " stroke order");
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
  strokeCount.textContent = numbers.length + (numbers.length === 1 ? " stroke" : " strokes");
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
    badge.innerHTML = '<circle cx="' + point[0] + '" cy="' + point[1] + '" r="36"/><text x="' + point[0] + '" y="' + (point[1] + 12) + '" text-anchor="middle">' + no + '</text>';
    svg.appendChild(badge);
  });
  strokeBox.innerHTML = "";
  strokeBox.appendChild(svg);
}
document.getElementById("replay").addEventListener("click", () => {
  if (currentChar) showStroke(currentChar, stageTitle.textContent, stageMeta.textContent.split(" — ")[0] || "", stageMeta.textContent.split(" — ")[1] || "");
});
form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!ready) return;
  const query = input.value.trim();
  renderResults(search(query), query);
});

const canvas = document.getElementById("pad");
const ctx = canvas.getContext("2d");
const strokes = [];
let current = null;
function point(event) {
  const rect = canvas.getBoundingClientRect();
  const src = event.touches ? event.touches[0] : event;
  return [
    ((src.clientX - rect.left) / rect.width) * canvas.width,
    ((src.clientY - rect.top) / rect.height) * canvas.height
  ];
}
function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineWidth = 6;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.strokeStyle = "#1c1915";
  strokes.concat(current ? [current] : []).forEach((stroke) => {
    if (!stroke.length) return;
    ctx.beginPath();
    ctx.moveTo(stroke[0][0], stroke[0][1]);
    stroke.slice(1).forEach((pt) => ctx.lineTo(pt[0], pt[1]));
    ctx.stroke();
  });
}
function start(event) {
  event.preventDefault();
  current = [point(event)];
  redraw();
}
function move(event) {
  if (!current) return;
  event.preventDefault();
  current.push(point(event));
  redraw();
}
function end() {
  if (current && current.length) strokes.push(current);
  current = null;
  redraw();
}
canvas.addEventListener("pointerdown", start);
canvas.addEventListener("pointermove", move);
canvas.addEventListener("pointerup", end);
canvas.addEventListener("pointerleave", end);
document.getElementById("undo").addEventListener("click", () => { strokes.pop(); redraw(); });
document.getElementById("clear").addEventListener("click", () => { strokes.length = 0; redraw(); document.getElementById("matches").innerHTML = ""; });

let lookupReady = false;
if (window.HanziLookup) {
  HanziLookup.init("mmah", "https://cdn.jsdelivr.net/gh/gugray/HanziLookupJS@master/dist/mmah.json", (ok) => { lookupReady = ok; });
}
document.getElementById("recognize").addEventListener("click", () => {
  const box = document.getElementById("matches");
  if (!lookupReady || !strokes.length) {
    box.textContent = "Draw a character, then recognize.";
    return;
  }
  const analyzed = new HanziLookup.AnalyzedCharacter(strokes);
  const matcher = new HanziLookup.Matcher("mmah");
  matcher.match(analyzed, 8, (matches) => {
    box.innerHTML = "";
    matches.forEach((item) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = item.character;
      btn.addEventListener("click", () => {
        input.value = item.character;
        const found = search(item.character);
        renderResults(found, item.character);
        if (!found.length) showStroke(item.character, item.character, "", "");
      });
      box.appendChild(btn);
    });
  });
});
