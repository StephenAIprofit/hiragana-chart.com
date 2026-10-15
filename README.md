# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: hiragana chart, kana quiz, and kanji translator.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | 46 hiragana in gojuon order, stroke order, audio, printable table |
| Quiz | https://hiragana-chart.com/quiz | 46-character quiz, instant score, combo, wrong-answer review |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | English, romaji, or kana to kanji, with reading and stroke order |

## Chart page

- 46 characters, あ to ん, in gojuon order.
- Romaji is Hepburn: し shi, ち chi, つ tsu, ふ fu, を wo.
- Click a character to hear the reading and watch the stroke order.
- Stroke diagrams come from animCJK `svgsJaKana`. Each file is `strokes/<unicode>.svg`.
- Deep link: `https://hiragana-chart.com/#shi` opens し.
- Printable table is on the same page.
- Buttons link to the hiragana quiz and the katakana quiz.

## Quiz page

- Default set is the 46 hiragana characters.
- Katakana opens at `https://hiragana-chart.com/quiz?script=katakana`.
- Two directions: Romaji → Kana, and Kana → Romaji.
- A correct answer adds a combo. A wrong answer shows the correct character, plays the sound, and stores the item for review.
- Hiragana wrong answers link to the chart stroke order, for example `/#ka`.

## Kanji Translator page

- Input English, romaji, or kana. The page returns the kanji, reading, and English meaning.
- Dictionary is the JMdict common-word set: 22,645 entries.
- Draw a character in the canvas. Recognition uses HanziLookup. Stroke order uses animCJK `svgsJa`.
- Stroke diagrams show numbered strokes, total stroke count, and a Replay button.

## Audio

Audio files live in `audio/<romaji>.mp3`.

Examples: `audio/a.mp3`, `audio/shi.mp3`, `audio/tsu.mp3`, `audio/fu.mp3`, `audio/wo.mp3`, `audio/n.mp3`.

The chart and the quiz both use these files.

## Sources

- Stroke diagrams: animCJK, LGPL-3.0. https://github.com/parsimonhi/animCJK
- Dictionary: JMdict by EDRDG, CC BY-SA 4.0. https://www.edrdg.org/jmdict/j_jmdict.html
- Handwriting recognition: HanziLookup. https://github.com/gugray/HanziLookupJS

## Repo layout

```
index.html              chart page
styles.css              chart styles
app.js                  chart audio and stroke order
audio/                  46 mp3 files
strokes/                46 animCJK SVG files
logo.png
favicon-48.png
favicon-192.png
apple-touch-icon.png
og-image.png
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

Quiz and translator assets use absolute paths: `/quiz/quiz.css`, `/kanji-translator/translator.js`.

## Deploy

The site is a static site on Vercel, with the domain `hiragana-chart.com` on Namecheap.

After a content change:

1. Commit and push to GitHub.
2. Wait for the Vercel deployment.
3. In Google Search Console, resubmit `https://hiragana-chart.com/sitemap.xml` when a new page is added.

## Attribution

Stroke diagrams: animCJK.
Dictionary: JMdict, EDRDG.
Handwriting: HanziLookup.
