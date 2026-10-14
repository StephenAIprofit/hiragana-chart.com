# Hiragana Chart

Live site: https://hiragana-chart.com/

A static site for the 46 modern hiragana characters, plus a kana quiz.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | Gojuon table, stroke order, native audio, printable table |
| Quiz | https://hiragana-chart.com/quiz | 46-character quiz, instant score, combo, wrong-answer review |

## Chart page

- 46 characters, あ to ん, in gojuon order.
- Romaji is Hepburn: し shi, ち chi, つ tsu, ふ fu, を wo.
- Click a character to hear the reading and watch the stroke order.
- Stroke diagrams come from animCJK `svgsJaKana`. Each file is `strokes/<unicode>.svg`, for example `strokes/12354.svg` for あ.
- Deep link: `https://hiragana-chart.com/#shi` opens し.
- Printable table is on the same page.

## Quiz page

- Default set is the 46 hiragana characters. The Katakana tab uses the matching 46 katakana.
- Two directions: romaji to kana, and kana to romaji.
- A correct answer adds a combo. A wrong answer shows the correct character, plays the sound, and stores the item for review.
- Hiragana wrong answers link to the chart stroke order, for example `/#ka`.
- Score, combo, and review run in the browser.

## Audio

Audio files live in `audio/<romaji>.mp3`.

Examples: `audio/a.mp3`, `audio/shi.mp3`, `audio/tsu.mp3`, `audio/fu.mp3`, `audio/wo.mp3`, `audio/n.mp3`.

The chart and the quiz both use these files.

## Repo layout

```
index.html          chart page
styles.css          chart styles
app.js              chart audio and stroke order
audio/              46 mp3 files
strokes/            46 animCJK SVG files
logo.png            header mark
favicon-48.png
favicon-192.png
apple-touch-icon.png
og-image.png
quiz/index.html     quiz page
quiz/quiz.css
quiz/quiz.js
sitemap.xml
robots.txt
llms.txt
```

Quiz assets use absolute paths: `/quiz/quiz.css` and `/quiz/quiz.js`.

## Deploy

The site is a static site on Vercel, with the domain `hiragana-chart.com` on Namecheap.

After a content change:

1. Commit and push to GitHub.
2. Wait for the Vercel deployment.
3. In Google Search Console, resubmit `https://hiragana-chart.com/sitemap.xml` when a new page is added.

## Attribution

Stroke diagrams: animCJK `svgsJaKana`.
