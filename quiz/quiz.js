const HIRAGANA = [
  ["あ","a"],["い","i"],["う","u"],["え","e"],["お","o"],
  ["か","ka"],["き","ki"],["く","ku"],["け","ke"],["こ","ko"],
  ["さ","sa"],["し","shi"],["す","su"],["せ","se"],["そ","so"],
  ["た","ta"],["ち","chi"],["つ","tsu"],["て","te"],["と","to"],
  ["な","na"],["に","ni"],["ぬ","nu"],["ね","ne"],["の","no"],
  ["は","ha"],["ひ","hi"],["ふ","fu"],["へ","he"],["ほ","ho"],
  ["ま","ma"],["み","mi"],["む","mu"],["め","me"],["も","mo"],
  ["や","ya"],["ゆ","yu"],["よ","yo"],
  ["ら","ra"],["り","ri"],["る","ru"],["れ","re"],["ろ","ro"],
  ["わ","wa"],["を","wo"],["ん","n"]
];
const KATAKANA = [
  ["ア","a"],["イ","i"],["ウ","u"],["エ","e"],["オ","o"],
  ["カ","ka"],["キ","ki"],["ク","ku"],["ケ","ke"],["コ","ko"],
  ["サ","sa"],["シ","shi"],["ス","su"],["セ","se"],["ソ","so"],
  ["タ","ta"],["チ","chi"],["ツ","tsu"],["テ","te"],["ト","to"],
  ["ナ","na"],["ニ","ni"],["ヌ","nu"],["ネ","ne"],["ノ","no"],
  ["ハ","ha"],["ヒ","hi"],["フ","fu"],["ヘ","he"],["ホ","ho"],
  ["マ","ma"],["ミ","mi"],["ム","mu"],["メ","me"],["モ","mo"],
  ["ヤ","ya"],["ユ","yu"],["ヨ","yo"],
  ["ラ","ra"],["リ","ri"],["ル","ru"],["レ","re"],["ロ","ro"],
  ["ワ","wa"],["ヲ","wo"],["ン","n"]
];

const state = {
  script: "hiragana",
  direction: "romaji",
  deck: [],
  index: 0,
  correct: 0,
  combo: 0,
  best: 0,
  answered: 0,
  wrongs: [],
  locked: false,
  review: false
};

function pool() {
  return state.script === "katakana" ? KATAKANA : HIRAGANA;
}
function shuffle(list) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function play(romaji, kana) {
  const audio = new Audio("/audio/" + romaji + ".mp3");
  const run = audio.play();
  if (run && run.catch) run.catch(() => speak(kana));
  audio.addEventListener("error", () => speak(kana), { once: true });
}
function speak(kana) {
  if (!window.speechSynthesis) return;
  const utter = new SpeechSynthesisUtterance(kana);
  utter.lang = "ja-JP";
  window.speechSynthesis.speak(utter);
}
function current() {
  return state.deck[state.index];
}
function optionsFor(item) {
  const others = shuffle(pool().filter((row) => row[1] !== item[1])).slice(0, 3);
  return shuffle([item].concat(others));
}
function setText(id, value) {
  document.getElementById(id).textContent = value;
}
function renderStats() {
  const total = state.deck.length || 1;
  const done = Math.min(state.answered, total);
  const accuracy = state.answered ? Math.round((state.correct / state.answered) * 100) : 0;
  setText("score", String(state.correct));
  setText("combo", String(state.combo));
  setText("accuracy", accuracy + "%");
  setText("count", (Math.min(state.index + 1, total)) + " / " + total);
  document.querySelector(".progress i").style.width = Math.round((done / total) * 100) + "%";
}
function start(review) {
  state.review = review;
  state.deck = review ? state.wrongs.slice() : shuffle(pool());
  state.wrongs = review ? [] : [];
  state.index = 0;
  state.correct = review ? state.correct : 0;
  if (!review) {
    state.combo = 0;
    state.answered = 0;
  }
  document.getElementById("result").classList.add("hidden");
  document.getElementById("play").classList.remove("hidden");
  ask();
}
function ask() {
  if (state.index >= state.deck.length) return finish();
  state.locked = false;
  const item = current();
  const choices = optionsFor(item);
  const kanaMode = state.direction === "kana";
  setText("prompt", kanaMode ? item[0] : item[1]);
  document.getElementById("prompt").classList.toggle("kana", kanaMode);
  setText("ask", kanaMode ? "Which romaji matches this character?" : "Which character matches this reading?");
  const box = document.getElementById("options");
  box.innerHTML = "";
  choices.forEach((row) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "opt" + (kanaMode ? "" : " kana");
    btn.textContent = kanaMode ? row[1] : row[0];
    btn.dataset.romaji = row[1];
    btn.addEventListener("click", () => answer(row, btn));
    box.appendChild(btn);
  });
  document.getElementById("feedback").innerHTML = "";
  renderStats();
}
function answer(row, btn) {
  if (state.locked) return;
  state.locked = true;
  state.answered += 1;
  const item = current();
  const ok = row[1] === item[1];
  const buttons = document.querySelectorAll(".opt");
  buttons.forEach((el) => {
    if (el.dataset.romaji === item[1]) el.classList.add("correct");
  });
  if (!ok) btn.classList.add("wrong");
  if (ok) {
    state.correct += 1;
    state.combo += 1;
    state.best = Math.max(state.best, state.combo);
  } else {
    state.combo = 0;
    state.wrongs.push(item);
  }
  play(item[1], item[0]);
  const stroke = state.script === "hiragana"
    ? ' <a href="/#' + item[1] + '">See stroke order</a>'
    : "";
  document.getElementById("feedback").innerHTML =
    "<p>" + (ok ? "Correct." : "Not this one.") + " " + item[0] + " is <b>" + item[1] + "</b>.</p>" +
    '<p><button class="next" id="next" type="button">Next</button>' + stroke + "</p>";
  document.getElementById("next").addEventListener("click", next);
  renderStats();
}
function next() {
  state.index += 1;
  ask();
}
function finish() {
  document.getElementById("play").classList.add("hidden");
  const box = document.getElementById("result");
  box.classList.remove("hidden");
  const total = state.deck.length;
  const wrong = state.wrongs.length;
  const right = total - wrong;
  let html = "<h2>Round done</h2><p>" + right + " correct, " + wrong + " to review. Best combo: " + state.best + ".</p>";
  if (wrong) html += '<p><button class="next" id="review" type="button">Review wrong answers</button></p>';
  html += '<p><button class="ghost" id="again" type="button">Start again</button></p>';
  box.innerHTML = html;
  const review = document.getElementById("review");
  if (review) review.addEventListener("click", () => start(true));
  document.getElementById("again").addEventListener("click", () => start(false));
  renderStats();
}
function setScript(name) {
  state.script = name;
  document.querySelectorAll(".tab").forEach((el) => {
    el.setAttribute("aria-selected", el.dataset.script === name ? "true" : "false");
  });
  const params = new URLSearchParams(location.search);
if (params.get("script") === "katakana") setScript("katakana");
else start(false);
}
function setDirection(name) {
  state.direction = name;
  document.querySelectorAll(".dir").forEach((el) => {
    el.setAttribute("aria-pressed", el.dataset.dir === name ? "true" : "false");
  });
  const params = new URLSearchParams(location.search);
if (params.get("script") === "katakana") setScript("katakana");
else start(false);
}
document.querySelectorAll(".tab").forEach((el) => {
  el.addEventListener("click", () => setScript(el.dataset.script));
});
document.querySelectorAll(".dir").forEach((el) => {
  el.addEventListener("click", () => setDirection(el.dataset.dir));
});
const params = new URLSearchParams(location.search);
if (params.get("script") === "katakana") setScript("katakana");
else start(false);
