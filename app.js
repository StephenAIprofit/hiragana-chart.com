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
  ["きゃ","キャ","kya"],["きゅ","キュ","kyu"],["きょ","キョ","kyo"],
  ["しゃ","シャ","sha"],["しゅ","シュ","shu"],["しょ","ショ","sho"],
  ["ちゃ","チャ","cha"],["ちゅ","チュ","chu"],["ちょ","チョ","cho"],
  ["にゃ","ニャ","nya"],["にゅ","ニュ","nyu"],["にょ","ニョ","nyo"],
  ["ひゃ","ヒャ","hya"],["ひゅ","ヒュ","hyu"],["ひょ","ヒョ","hyo"],
  ["みゃ","ミャ","mya"],["みゅ","ミュ","myu"],["みょ","ミョ","myo"],
  ["りゃ","リャ","rya"],["りゅ","リュ","ryu"],["りょ","リョ","ryo"],
  ["ぎゃ","ギャ","gya"],["ぎゅ","ギュ","gyu"],["ぎょ","ギョ","gyo"],
  ["じゃ","ジャ","ja"],["じゅ","ジュ","ju"],["じょ","ジョ","jo"],
  ["ぢゃ","ヂャ","ja"],["ぢゅ","ヂュ","ju"],["ぢょ","ヂョ","jo"],
  ["びゃ","ビャ","bya"],["びゅ","ビュ","byu"],["びょ","ビョ","byo"],
  ["ぴゃ","ピャ","pya"],["ぴゅ","ピュ","pyu"],["ぴょ","ピョ","pyo"]
];

const state = { script: "hiragana" };
const cache = new Map();
let currentAudio = null;

function stopAudio() {
  if (currentAudio) { try { currentAudio.pause(); } catch (e) {} currentAudio = null; }
  if (window.speechSynthesis) { try { window.speechSynthesis.cancel(); } catch (e) {} }
}
function play(kana, romaji) {
  stopAudio();
  const audio = new Audio("/audio/" + romaji + ".mp3");
  currentAudio = audio;
  const run = audio.play();
  if (run && run.catch) run.catch(() => speak(kana));
  audio.addEventListener("error", () => speak(kana), { once: true });
}
function speak(kana) {
  if (!window.speechSynthesis) return;
  const u = new SpeechSynthesisUtterance(kana);
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
  try {
    const res = await fetch(local);
    if (res.ok) text = await res.text();
  } catch (e) {}
  if (!text) {
    try {
      const res = await fetch(remote);
      if (res.ok) text = await res.text();
    } catch (e) {}
  }
  cache.set(code, text);
  return text;
}
function drawSvg(text, kana) {
  const stage = document.getElementById("glyph");
  stage.innerHTML = "";
  if (!text) { stage.textContent = kana; return; }
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
  stage.appendChild(svg);
  document.getElementById("order").textContent = numbers.length + (numbers.length === 1 ? " stroke" : " strokes");
}
async function select(kana, romaji) {
  document.getElementById("reading").textContent = romaji;
  const text = await loadSvg(kana);
  drawSvg(text, kana);
  play(kana, romaji);
}
function renderGrid(id, rows) {
  const box = document.getElementById(id);
  box.innerHTML = "";
  rows.forEach(([h, k, r]) => {
    const kana = state.script === "katakana" ? k : h;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cell";
    btn.innerHTML = '<span class="kana">' + kana + '</span><span class="romaji">' + r + '</span>';
    btn.addEventListener("click", () => select(kana, r));
    box.appendChild(btn);
  });
}
function setScript(name) {
  state.script = name;
  document.querySelectorAll(".script-btn").forEach((el) => {
    el.setAttribute("aria-pressed", el.dataset.script === name ? "true" : "false");
  });
  renderGrid("grid", BASIC);
  renderGrid("dakuten-grid", DAKUTEN);
  renderGrid("yoon-grid", YOON);
  if (name === "katakana") history.replaceState(null, "", "#katakana");
}
document.querySelectorAll(".script-btn").forEach((el) => {
  el.addEventListener("click", () => setScript(el.dataset.script));
});
document.getElementById("play").addEventListener("click", () => {
  const kana = document.querySelector(".cell .kana");
  const romaji = document.getElementById("reading").textContent;
  if (romaji) play(romaji === "n" ? "ん" : romaji, romaji);
});
document.getElementById("replay-strokes").addEventListener("click", () => {
  const reading = document.getElementById("reading").textContent;
  const cell = [...document.querySelectorAll(".cell")].find((el) => el.querySelector(".romaji").textContent === reading);
  if (cell) select(cell.querySelector(".kana").textContent, reading);
});

const hash = (location.hash || "").replace("#", "");
if (hash === "katakana") setScript("katakana");
else setScript("hiragana");

const first = document.querySelector("#grid .cell");
if (first) select(first.querySelector(".kana").textContent, first.querySelector(".romaji").textContent);
