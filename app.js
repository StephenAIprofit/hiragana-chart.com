const BASIC = [
  ["あ","ア","a"],["い","イ","i"],["う","ウ","u"],["え","エ","e"],["お","オ","o"],
  ["か","カ","ka"],["き","キ","ki"],["く","ク","ku"],["け","ケ","ke"],["こ","コ","ko"],
  ["さ","サ","sa"],["し","シ","shi"],["す","ス","su"],["せ","セ","se"],["そ","ソ","so"],
  ["た","タ","ta"],["ち","チ","chi"],["つ","ツ","tsu"],["て","テ","te"],["と","ト","to"],
  ["な","ナ","na"],["に","ニ","ni"],["ぬ","ヌ","nu"],["ね","ネ","ne"],["の","ノ","no"],
  ["は","ハ","ha"],["ひ","ヒ","hi"],["ふ","フ","fu"],["へ","ヘ","he"],["ほ","ホ","ho"],
  ["ま","マ","ma"],["み","ミ","mi"],["む","ム","mu"],["め","メ","me"],["も","モ","mo"],
  ["や","ヤ","ya"],["ゆ","ユ","yu"],["よ","ヨ","yo"],
  ["ら","ラ","ra"],["り","リ","ri"],["る","ル","ru"],["れ","レ","re"],["ろ","ロ","ro"],
  ["わ","ワ","wa"],["を","ヲ","wo"],["ん","ン","n"]
];
const DAKUTEN = [
  ["が","ガ","ga"],["ぎ","ギ","gi"],["ぐ","グ","gu"],["げ","ゲ","ge"],["ご","ゴ","go"],
  ["ざ","ザ","za"],["じ","ジ","ji"],["ず","ズ","zu"],["ぜ","ゼ","ze"],["ぞ","ゾ","zo"],
  ["だ","ダ","da"],["ぢ","ヂ","ji"],["づ","ヅ","zu"],["で","デ","de"],["ど","ド","do"],
  ["ば","バ","ba"],["び","ビ","bi"],["ぶ","ブ","bu"],["べ","ベ","be"],["ぼ","ボ","bo"],
  ["ぱ","パ","pa"],["ぴ","ピ","pi"],["ぷ","プ","pu"],["ぺ","ペ","pe"],["ぽ","ポ","po"]
];
const YOON = [
  ["きゃ","キャ","kya",["き","キ"],["ゃ","ャ"]],["きゅ","キュ","kyu",["き","キ"],["ゅ","ュ"]],["きょ","キョ","kyo",["き","キ"],["ょ","ョ"]],
  ["しゃ","シャ","sha",["し","シ"],["ゃ","ャ"]],["しゅ","シュ","shu",["し","シ"],["ゅ","ュ"]],["しょ","ショ","sho",["し","シ"],["ょ","ョ"]],
  ["ちゃ","チャ","cha",["ち","チ"],["ゃ","ャ"]],["ちゅ","チュ","chu",["ち","チ"],["ゅ","ュ"]],["ちょ","チョ","cho",["ち","チ"],["ょ","ョ"]],
  ["にゃ","ニャ","nya",["に","ニ"],["ゃ","ャ"]],["にゅ","ニュ","nyu",["に","ニ"],["ゅ","ュ"]],["にょ","ニョ","nyo",["に","ニ"],["ょ","ョ"]],
  ["ひゃ","ヒャ","hya",["ひ","ヒ"],["ゃ","ャ"]],["ひゅ","ヒュ","hyu",["ひ","ヒ"],["ゅ","ュ"]],["ひょ","ヒョ","hyo",["ひ","ヒ"],["ょ","ョ"]],
  ["みゃ","ミャ","mya",["み","ミ"],["ゃ","ャ"]],["みゅ","ミュ","myu",["み","ミ"],["ゅ","ュ"]],["みょ","ミョ","myo",["み","ミ"],["ょ","ョ"]],
  ["りゃ","リャ","rya",["り","リ"],["ゃ","ャ"]],["りゅ","リュ","ryu",["り","リ"],["ゅ","ュ"]],["りょ","リョ","ryo",["り","リ"],["ょ","ョ"]],
  ["ぎゃ","ギャ","gya",["ぎ","ギ"],["ゃ","ャ"]],["ぎゅ","ギュ","gyu",["ぎ","ギ"],["ゅ","ュ"]],["ぎょ","ギョ","gyo",["ぎ","ギ"],["ょ","ョ"]],
  ["じゃ","ジャ","ja",["じ","ジ"],["ゃ","ャ"]],["じゅ","ジュ","ju",["じ","ジ"],["ゅ","ュ"]],["じょ","ジョ","jo",["じ","ジ"],["ょ","ョ"]],
  ["ぢゃ","ヂャ","ja",["ぢ","ヂ"],["ゃ","ャ"]],["ぢゅ","ヂュ","ju",["ぢ","ヂ"],["ゅ","ュ"]],["ぢょ","ヂョ","jo",["ぢ","ヂ"],["ょ","ョ"]],
  ["びゃ","ビャ","bya",["び","ビ"],["ゃ","ャ"]],["びゅ","ビュ","byu",["び","ビ"],["ゅ","ュ"]],["びょ","ビョ","byo",["び","ビ"],["ょ","ョ"]],
  ["ぴゃ","ピャ","pya",["ぴ","ピ"],["ゃ","ャ"]],["ぴゅ","ピュ","pyu",["ぴ","ピ"],["ゅ","ュ"]],["ぴょ","ピョ","pyo",["ぴ","ピ"],["ょ","ョ"]]
];
const ROWS = { "": ["a","i","u","e","o"], k: ["ka","ki","ku","ke","ko"], s: ["sa","shi","su","se","so"], t: ["ta","chi","tsu","te","to"], n: ["na","ni","nu","ne","no"], h: ["ha","hi","fu","he","ho"], m: ["ma","mi","mu","me","mo"], y: ["ya","","yu","","yo"], r: ["ra","ri","ru","re","ro"], w: ["wa","","","","wo"], N: ["n","","","",""] };
const state = { script: "hiragana" };
const cache = new Map();
let currentAudio = null;

function stopAudio() {
  if (currentAudio) { try { currentAudio.pause(); } catch (e) {} currentAudio = null; }
  if (window.speechSynthesis) { try { window.speechSynthesis.cancel(); } catch (e) {} }
}
function play(romaji, fallback) {
  stopAudio();
  const audio = new Audio("/audio/" + romaji + ".mp3");
  currentAudio = audio;
  const run = audio.play();
  if (run && run.catch) run.catch(() => speak(fallback || romaji));
  audio.addEventListener("error", () => speak(fallback || romaji), { once: true });
}
function speak(text) {
  if (!window.speechSynthesis) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "ja-JP";
  window.speechSynthesis.speak(u);
}
function strokeNo(id) {
  const m = /d(\d+)/.exec(id || "");
  return m ? Number(m[1]) : 0;
}
function firstPoint(d) {
  const m = /M\s*(-?\d+(?:\.\d+)?)\s*,?\s*(-?\d+(?:\.\d+)?)/.exec(d || "");
  return m ? [Number(m[1]), Number(m[2])] : null;
}
async function loadSvg(kana) {
  const code = kana.codePointAt(0);
  if (cache.has(code)) return cache.get(code);
  const local = "/strokes/" + code + ".svg";
  const remote = "https://raw.githubusercontent.com/parsimonhi/animCJK/master/svgsJaKana/" + code + ".svg";
  let text = "";
  try { const res = await fetch(local); if (res.ok) text = await res.text(); } catch (e) {}
  if (!text) { try { const res = await fetch(remote); if (res.ok) text = await res.text(); } catch (e) {} }
  cache.set(code, text);
  return text;
}
function buildSvg(text) {
  if (!text) return { svg: null, count: 0 };
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 1024 1024");
  const shapes = [...doc.querySelectorAll("path[id]")].filter((p) => strokeNo(p.id));
  const lines = [...doc.querySelectorAll("path[clip-path]")];
  const starts = new Map();
  lines.forEach((p) => {
    const no = strokeNo(p.getAttribute("clip-path"));
    const pt = firstPoint(p.getAttribute("d"));
    if (no && pt && pt[0] >= 0 && !starts.has(no)) starts.set(no, pt);
  });
  const numbers = [...new Set(shapes.map((p) => strokeNo(p.id)))].sort((a, b) => a - b);
  numbers.forEach((no, index) => {
    shapes.filter((p) => strokeNo(p.id) === no).forEach((p) => {
      const d = document.createElementNS("http://www.w3.org/2000/svg", "path");
      d.setAttribute("d", p.getAttribute("d"));
      d.setAttribute("class", "glyph-stroke");
      d.style.animationDelay = (index * 0.7) + "s";
      svg.appendChild(d);
    });
    const pt = starts.get(no);
    if (!pt) return;
    const badge = document.createElementNS("http://www.w3.org/2000/svg", "g");
    badge.setAttribute("class", "stroke-badge");
    badge.style.animationDelay = (index * 0.7) + "s";
    badge.innerHTML = '<circle cx="' + pt[0] + '" cy="' + pt[1] + '" r="36"/><text x="' + pt[0] + '" y="' + (pt[1] + 12) + '" text-anchor="middle">' + no + '</text>';
    svg.appendChild(badge);
  });
  return { svg, count: numbers.length };
}
function scrollDetail() { /* sticky panel, no forced scroll */ }
async function selectOne(kana, romaji) {
  document.getElementById("reading").textContent = romaji;
  const stage = document.getElementById("glyph");
  stage.innerHTML = "";
  const text = await loadSvg(kana);
  const built = buildSvg(text);
  if (built.svg && built.count) {
    stage.appendChild(built.svg);
    document.getElementById("order").textContent = built.count + (built.count === 1 ? " stroke" : " strokes");
  } else {
    stage.textContent = kana;
    document.getElementById("order").textContent = "Stroke order animation is not available. Audio only.";
  }
  play(romaji, kana);
  scrollDetail();
}
async function selectYoon(kana, romaji, base, small) {
  document.getElementById("reading").textContent = romaji;
  const stage = document.getElementById("glyph");
  stage.innerHTML = "";
  const baseText = await loadSvg(base);
  const smallText = await loadSvg(small);
  const a = buildSvg(baseText);
  const b = buildSvg(smallText);
  if (a.svg && b.svg && a.count && b.count) {
    a.svg.classList.add("glyph-base");
    b.svg.classList.add("glyph-small");

    const delay = a.count * 0.7;
    b.svg.querySelectorAll(".glyph-stroke, .stroke-badge").forEach((el) => {
      const current = parseFloat(el.style.animationDelay) || 0;
      el.style.animationDelay = (current + delay) + "s";
    });
    stage.appendChild(a.svg);
    stage.appendChild(b.svg);
    const total = a.count + b.count;
    document.getElementById("order").textContent = total + " strokes";
  } else {
    stage.textContent = kana;
    document.getElementById("order").textContent = "Stroke order animation is not available. Audio only.";
  }
  play(romaji, kana);
  scrollDetail();
}
function renderGrid(id, rows, isYoon) {
  const box = document.getElementById(id);
  box.innerHTML = "";
  rows.forEach((row) => {
    const kana = state.script === "katakana" ? row[1] : row[0];
    const romaji = row[2];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cell";
    btn.innerHTML = '<span class="kana">' + kana + '</span><span class="romaji">' + romaji + '</span>';
    btn.addEventListener("click", () => {
      if (isYoon) {
        const base = state.script === "katakana" ? row[3][1] : row[3][0];
        const small = state.script === "katakana" ? row[4][1] : row[4][0];
        selectYoon(kana, romaji, base, small);
      } else {
        selectOne(kana, romaji);
      }
    });
    box.appendChild(btn);
  });
}
function fillTable(id, useKana) {
  const tbody = document.getElementById(id);
  if (!tbody) return;
  const map = {};
  BASIC.forEach(([h, k, r]) => { map[r] = useKana ? k : h; });
  tbody.innerHTML = "";
  Object.entries(ROWS).forEach(([label, cells]) => {
    const tr = document.createElement("tr");
    tr.innerHTML = "<th>" + label + "</th>" + cells.map((r) => r ? "<td><b>" + (map[r] || "") + "</b><br>" + r + "</td>" : "<td></td>").join("");
    tbody.appendChild(tr);
  });
}
function renderTable() {
  fillTable("table-body", false);
  fillTable("table-body-k", true);
}
function quizHref(hash) {
  return state.script === "katakana" ? "/quiz?script=katakana#" + hash : "/quiz#" + hash;
}
function setScript(name) {
  state.script = name;
  const isK = name === "katakana";
  document.querySelectorAll(".script-btn").forEach((el) => {
    el.setAttribute("aria-pressed", el.dataset.script === name ? "true" : "false");
  });
  document.getElementById("page-title").textContent = isK ? "Katakana Chart" : "Hiragana Chart";
  document.getElementById("page-lede").textContent = isK
    ? "A Katakana chart lists the same 46 characters, dakuten, and yoon. Click a character to hear it and watch its stroke order. Romaji on this page is Hepburn."
    : "A Hiragana chart lists all 46 modern Hiragana characters in gojuon order, from あ to ん. Click a character to hear it and watch its stroke order. Romaji on this page is Hepburn.";
  document.getElementById("dakuten-title").textContent = isK ? "Katakana dakuten and handakuten" : "Hiragana dakuten and handakuten";
  document.getElementById("dakuten-note").textContent = isK
    ? "Dakuten add two dots (ガ ザ ダ バ). Handakuten add a circle (パ ピ プ ペ ポ). In modern Japanese, ヂ is read ji and ヅ is read zu."
    : "Dakuten add two dots (が ざ だ ば). Handakuten add a circle (ぱ ぴ ぷ ぺ ぽ). In modern Japanese, ぢ is read ji and づ is read zu.";
  document.getElementById("yoon-title").textContent = isK ? "Katakana yoon (contracted sounds)" : "Hiragana yoon (contracted sounds)";
  document.getElementById("yoon-note").textContent = isK
    ? "Yoon is a large kana plus a small ャ, ュ, or ョ. The small character is not an independent sound. ヂャ, ヂュ, and ヂョ are rare; they use the same sound as ジャ, ジュ, and ジョ."
    : "Yoon is a large kana plus a small ゃ, ゅ, or ょ. The small character is not an independent sound. ぢゃ, ぢゅ, and ぢょ are rare; they use the same sound as じゃ, じゅ, and じょ.";
  document.querySelectorAll("[data-quiz]").forEach((el) => {
    el.href = quizHref(el.dataset.quiz);
  });
  renderGrid("grid", BASIC, false);
  renderGrid("dakuten-grid", DAKUTEN, false);
  renderGrid("yoon-grid", YOON, true);
  renderTable();
  if (isK) history.replaceState(null, "", "#katakana");
}
document.querySelectorAll(".script-btn").forEach((el) => {
  el.addEventListener("click", () => setScript(el.dataset.script));
});
document.getElementById("play").addEventListener("click", () => {
  const romaji = document.getElementById("reading").textContent;
  if (romaji) play(romaji);
});
document.getElementById("replay-strokes").addEventListener("click", () => {
  const reading = document.getElementById("reading").textContent;
  const cell = [...document.querySelectorAll(".cell")].find((el) => el.querySelector(".romaji").textContent === reading);
  if (cell) cell.click();
});
document.getElementById("print-k") && document.getElementById("print-k").addEventListener("click", () => window.print());
document.querySelectorAll(".word-btn").forEach((el) => {
  el.addEventListener("click", () => play(el.dataset.audio, el.textContent));
});
const hash = (location.hash || "").replace("#", "");
if (hash === "katakana") setScript("katakana");
else setScript("hiragana");
/* no auto-select on load */

let looping = true;
function startLoop() {
  looping = true;
  selectOne("あ", "a").then(() => {
    document.getElementById("reading").textContent = "";
    const replay = () => {
      if (!looping) return;
      const btn = document.getElementById("replay-strokes");
      if (btn) btn.click();
      setTimeout(replay, 2200);
    };
    setTimeout(replay, 2200);
  });
}
document.addEventListener("click", (e) => {
  if (e.target.closest(".cell")) looping = false;
});
startLoop();
