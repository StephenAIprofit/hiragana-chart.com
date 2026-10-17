# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: Hiragana chart, Kana quiz, and Kanji translator.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | Basic 46, dakuten, yoon, special Kana, stroke order, audio, printable table |
| Quiz | https://hiragana-chart.com/quiz | L1–L4 difficulty, instant score, combo, wrong-answer review |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | English, Romaji, or Kana to Kanji, with reading and stroke order |

## Navigation

Desktop: Chart ▾, Quiz, Kanji Translator | Pronunciation, Printable table, FAQ.

Chart dropdown: Hiragana 46, Dakuten & Handakuten, Yoon, Katakana, Special Kana, Stroke order guide.

Mobile: hamburger menu with the same items. Chart expands inside the menu.

## Chart page

The switcher changes the whole table between Hiragana and Katakana.

- Basic 46: あ to ん, in gojuon order.
- Dakuten and handakuten: 25 characters (が–ぼ, ぱ–ぽ).
- Yoon: 36 contracted sounds (きゃ–ぴょ).
- Special Kana: sokuon っ/ッ and long vowels.
- Romaji is Hepburn: し shi, ち chi, つ tsu, ふ fu, を wo.
- Click a character to hear it and watch the stroke order.
- Stroke diagrams come from animCJK.
- Deep link: `https://hiragana-chart.com/#shi` opens し. `#katakana` opens the Katakana view.
- Each section ends with a quiz link: `/quiz#basic`, `/quiz#dakuten`, `/quiz#yoon`.

## Quiz page

- L1 Basic 46 (default).
- L2 adds dakuten and handakuten (71).
- L3 adds yoon (107).
- L4 is the full set.
- Katakana mirrors the same levels at `?script=katakana`.
- Hash preselect: `#basic`, `#dakuten`, `#yoon`, `#katakana`.
- Two directions: Romaji → Kana, and Kana → Romaji.
- A correct answer adds a combo. A wrong answer shows the correct character, plays the sound, and stores the item for review.

## Kanji Translator page

- Input English, Romaji, or Kana. The page returns the Kanji, reading, and English meaning.
- Dictionary is the JMdict common-word set: 22,645 entries.
- Result cards are three rows: Kanji (one line, font scales down), reading (one line), meaning (two lines).
- Draw a character in the canvas. Recognition uses HanziLookup. Stroke order uses animCJK.
- Stroke diagrams show numbered strokes, total stroke count, and a Replay button.
- Pure Kana results do not open a stroke stage.

## Capitalization

Hiragana, Katakana, Romaji, and Kanji are capitalized in visible text. URLs, code, and file names stay lowercase. FAQ stays uppercase.

## Audio

Audio files live in `audio/<romaji>.mp3`.

Examples: `audio/a.mp3`, `audio/shi.mp3`, `audio/tsu.mp3`, `audio/fu.mp3`, `audio/wo.mp3`, `audio/n.mp3`.

## Sources

- Stroke diagrams: animCJK, LGPL-3.0. https://github.com/parsimonhi/animCJK
- Dictionary: JMdict by EDRDG, CC BY-SA 4.0. https://www.edrdg.org/jmdict/j_jmdict.html
- Handwriting recognition: HanziLookup. https://github.com/gugray/HanziLookupJS

## Repo layout

```
index.html              chart page
styles.css              chart styles
app.js                  chart switcher and stroke order
nav.css                 shared navigation styles
nav.js                  shared navigation behavior
audio/                  46 mp3 files
strokes/                46 animCJK SVG files
logo.png
quiz/index.html         quiz page
quiz/quiz.css
quiz/quiz.js
kanji-translator/index.html
kanji-translator/translator.css
kanji-translator/translator.js
kanji-translator/dict.json
sitemap.xml
robots.txt
llms.txt
```

## Deploy

The site is a static site on Vercel, with the domain `hiragana-chart.com` on Namecheap.

After a content change:

1. Commit and push to GitHub.
2. Wait for the Vercel deployment.
3. In Google Search Console, resubmit `https://hiragana-chart.com/sitemap.xml` when a new page is added.
