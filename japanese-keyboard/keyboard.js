// Japanese keyboard: romaji -> kana as you type (wanakana IME mode),
// an on-screen kana keyboard, and a paste-and-convert box.
// Everything runs in the browser; the text is only kept in localStorage.
(function () {
  var MAP = { "[": "「", "]": "」" };
  var STORE = "hc-keyboard-text";
  var input = document.getElementById("kb-input");
  var count = document.getElementById("kb-count");
  var script = "hiragana";

  function save() {
    count.textContent = Array.from(input.value).length + " characters";
    try { localStorage.setItem(STORE, input.value); } catch (e) {}
  }
  function bind() {
    try { wanakana.unbind(input); } catch (e) {}
    wanakana.bind(input, {
      IMEMode: script === "katakana" ? "toKatakana" : "toHiragana",
      customKanaMapping: MAP
    });
  }
  function copy(text, button) {
    function done() {
      var label = button.textContent;
      button.textContent = "Copied";
      setTimeout(function () { button.textContent = label; }, 1200);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
    function fallback() {
      var t = document.createElement("textarea");
      t.value = text;
      document.body.appendChild(t);
      t.select();
      try { document.execCommand("copy"); done(); } catch (e) {}
      document.body.removeChild(t);
    }
  }

  // Restore the last text, then start converting.
  try { input.value = localStorage.getItem(STORE) || ""; } catch (e) {}
  bind();
  save();
  input.addEventListener("input", save);

  // Hiragana / Katakana output
  document.querySelectorAll("[data-kb-script]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      script = btn.dataset.kbScript;
      document.querySelectorAll("[data-kb-script]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      document.querySelectorAll(".kb-key[data-h]").forEach(function (key) {
        key.textContent = script === "katakana" ? key.dataset.k : key.dataset.h;
      });
      bind();
      input.focus();
    });
  });

  document.getElementById("kb-copy").addEventListener("click", function () {
    copy(input.value, this);
  });
  document.getElementById("kb-clear").addEventListener("click", function () {
    input.value = "";
    save();
    input.focus();
  });

  // On-screen keys
  var DAKU_FROM = "かきくけこさしすせそたちつてとはひふへほうカキクケコサシスセソタチツテトハヒフヘホウ";
  var DAKU_TO = "がぎぐげござじずぜぞだぢづでどばびぶべぼゔガギグゲゴザジズゼゾダヂヅデドバビブベボヴ";
  var HANDAKU_FROM = "はひふへほハヒフヘホばびぶべぼバビブベボ";
  var HANDAKU_TO = "ぱぴぷぺぽパピプペポぱぴぷぺぽパピプペポ";
  var SMALL_FROM = "あいうえおつやゆよわアイウエオツヤユヨワ";
  var SMALL_TO = "ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ";

  function insert(text) {
    var s = input.selectionStart, e = input.selectionEnd;
    input.setRangeText(text, s, e, "end");
    save();
  }
  function swapBefore(from, to, back) {
    var pos = input.selectionStart;
    if (pos < 1 || input.selectionEnd !== pos) return;
    var ch = input.value.charAt(pos - 1);
    var i = from.indexOf(ch), out = null;
    if (i !== -1) out = to.charAt(i);
    else if (back && to.indexOf(ch) !== -1) out = back.charAt(to.indexOf(ch));
    if (!out) return;
    input.setRangeText(out, pos - 1, pos, "end");
    save();
  }
  document.querySelectorAll(".kb-key").forEach(function (key) {
    key.addEventListener("click", function () {
      var act = key.dataset.act;
      if (act === "daku") swapBefore(DAKU_FROM, DAKU_TO, DAKU_FROM);
      else if (act === "handaku") swapBefore(HANDAKU_FROM, HANDAKU_TO, "はひふへほハヒフヘホはひふへほハヒフヘホ");
      else if (act === "small") swapBefore(SMALL_FROM, SMALL_TO, SMALL_FROM);
      else if (act === "back") {
        var s = input.selectionStart, e = input.selectionEnd;
        if (s === e && s > 0) input.setRangeText("", s - 1, s, "end");
        else input.setRangeText("", s, e, "end");
        save();
      } else insert(key.textContent === "Space" ? "　" : key.textContent);
    });
  });

  // Paste and convert
  var convIn = document.getElementById("conv-in");
  var convOut = document.getElementById("conv-out");
  document.querySelectorAll("[data-conv]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var t = convIn.value;
      var kind = btn.dataset.conv;
      if (kind === "hiragana") convOut.value = wanakana.toHiragana(t, { customKanaMapping: MAP });
      else if (kind === "katakana") convOut.value = wanakana.toKatakana(t, { customKanaMapping: MAP });
      else convOut.value = wanakana.toRomaji(t);
    });
  });
  document.getElementById("conv-copy").addEventListener("click", function () {
    copy(convOut.value, this);
  });
})();
