const SVG_BASE = "https://raw.githubusercontent.com/parsimonhi/animCJK/master/svgsJa/";
let dict = [];
let ready = false;

const form = document.getElementById("form");
const input = document.getElementById("q");
const results = document.getElementById("results");
const stage = document.getElementById("stage");
const stageTitle = document.getElementById("stage-title");
const stageMeta = document.getElementById("stage-meta");
const strokeBox = document.getElementById("stroke");

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
  return dict.filter((row) => {
    if (row.kanji.includes(raw.trim())) return true;
    if (row.reading === kana || row.reading.startsWith(kana)) return true;
    if (row.romaji === q || row.romaji.startsWith(q)) return true;
    if (row.en.toLowerCase().includes(q)) return true;
    return false;
  }).slice(0, 20);
}
function renderResults(rows, query) {
  results.innerHTML = "";
  if (!rows.length) {
    if (hasKanji(query)) showStroke(query.trim()[0], query.trim(), "", "");
    results.innerHTML = "<p>Type a common English word, romaji, or kana such as love, ai, or あい.</p>";
    return;
  }
  rows.forEach((row) => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = '<div class="kj">' + row.kanji + '</div><div><b>' + row.reading + '</b> · ' + row.romaji + '<div class="meta">' + row.en + '</div></div>';
    card.addEventListener("click", () => showStroke(row.kanji[0], row.kanji, row.reading + " · " + row.romaji, row.en));
    results.appendChild(card);
  });
  const first = rows[0];
  showStroke(first.kanji[0], first.kanji, first.reading + " · " + first.romaji, first.en);
}
async function showStroke(char, title, meta, meaning) {
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
    strokeBox.innerHTML = text;
  } catch (err) {
    strokeBox.textContent = char;
  }
}
form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!ready) return;
  const query = input.value;
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
