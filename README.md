# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: hiragana and katakana charts, a stroke order page for every kana, quizzes, a Japanese keyboard, a kanji translator, and learning guides.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Hiragana chart | https://hiragana-chart.com/ | Basic 46, dakuten, yoon, sokuon, stroke order, audio, printable table (generated) |
| Katakana chart | https://hiragana-chart.com/katakana-chart | The same chart in katakana (generated) |
| Yoon chart | https://hiragana-chart.com/yoon-chart | All 36 combinations (きゃ…ぴょ), hiragana and katakana side by side, printable (generated) |
| Stroke order pages | https://hiragana-chart.com/hiragana, /katakana | Index plus one page per character, e.g. /hiragana/ka, /katakana/shi (generated) |
| Hiragana quiz | https://hiragana-chart.com/quiz | Characters and Words modes, L1–L4. "Get the Workbook · $9.90" button links to https://stephenzy2.gumroad.com/l/kanabook |
| Katakana quiz | https://hiragana-chart.com/katakana-quiz | The quiz opened in katakana (generated from quiz/index.html) |
| Japanese keyboard | https://hiragana-chart.com/japanese-keyboard | Romaji to kana as you type, on-screen kana keys, paste-and-convert (generated) |
| Kanji translator | https://hiragana-chart.com/kanji-translator | Draw a kanji, or type English, romaji, or kana, to get kanji, reading, and meaning |
| Hiragana Quiz guide | https://hiragana-chart.com/hiragana-quiz-guide | How the quiz works: levels, modes, wrong-answer review |
| Confusable kana | https://hiragana-chart.com/confusable-kana | Pairs that look alike, plus the two confusable tables |
| Dakuten and Yoon | https://hiragana-chart.com/dakuten-yoon-guide | Rules for dakuten, handakuten, and yoon |
| About | https://hiragana-chart.com/about | Why the site exists, contact form |
| Privacy | https://hiragana-chart.com/privacy | No login, quiz data stays in the browser, ads and cookies (Adsterra, AdSense) |

## Navigation

Desktop: Home | Chart ▾ | Quiz ▾ | Tools ▾ | Guides ▾. On phones the same links sit behind the ☰ menu, which starts closed.

- Chart: Hiragana chart, Dakuten & Handakuten, Yoon chart, Katakana chart, Sokuon & Long Vowels, Hiragana stroke order, Katakana stroke order.
- Quiz: Hiragana quiz, Katakana quiz.
- Tools: Japanese keyboard, Kanji translator.
- Guides: Hiragana Quiz guide, Confusable kana, Dakuten and Yoon.

The nav is defined once in `scripts/build_site.py` (`NAV`) and copied into the hand-written pages on every build.

## Footer

Tool and quiz links; Hiragana chart, Katakana chart, both stroke order indexes, and Yoon chart; the three guides; About and Privacy. No email address in the footer.

## Chart pages (/ and /katakana-chart)

- The Hiragana / Katakana buttons link between the two pages (old `/#katakana` links redirect to `/katakana-chart`).
- All grids and the printable table are static HTML, so search engines can read them without running JavaScript. `app.js` only adds audio, stroke animation, and printing.
- The detail panel is sticky. On load it replays the stroke order of the first character with no sound; clicking a character plays its audio, shows its numbered strokes, and links to its own page.
- "After the chart" section links in the body text to the yoon chart, the quiz, the Japanese keyboard, the kanji translator, and confusable kana.
- Sokuon examples (with audio) are in the FAQ, which opens at `/#special`.

## Character pages (/hiragana/<slug>, /katakana/<slug>)

- 107 hiragana and 107 katakana. Slugs are Hepburn romaji; ぢ, づ, and ぢゃ/ぢゅ/ぢょ use di, du, dya/dyu/dyo so they do not clash with じ and ず.
- Each page: animated and step-by-step numbered stroke diagrams, audio, pronunciation note, example word, look-alikes, same-row links, a "Get the Workbook · $9.90" box, and breadcrumbs.
- Pages with no example word (28 rare kana such as ヂ, ヲ, and some yoon) are `noindex, follow` and left out of the sitemap.
- Example words and pronunciation notes live in `scripts/kana_data.py`.

## Quiz pages

- Script tabs: Hiragana and Katakana, plus the workbook button, which opens in a new tab.
- Characters mode and Words mode. L1–L4; L4 is the same set as L3 (107).
- Wrong answers return in the same session. Nothing is stored on a server.
- `/katakana-quiz` is generated from `quiz/index.html`; `/quiz?script=katakana` redirects there (vercel.json).

## Japanese keyboard

- Romaji becomes kana as you type, with the same rules as a system Japanese keyboard: `nn` → ん, doubled consonant → っ, `-` → ー, `[ ]` → 「」, capitals → katakana.
- Hiragana / Katakana output, Copy, Clear. The text is kept in localStorage only.
- On-screen kana keys with ゛ ゜, small kana, ー, punctuation, space, and backspace.
- Paste-and-convert to hiragana, katakana, or romaji. It cannot convert kana to kanji.
- Logic in `japanese-keyboard/keyboard.js`; the page itself is generated.

## Kanji translator

- Draw or Type. Results show kanji, reading, and English meaning (JMdict-based `dict.json`).
- "How to translate Japanese characters" section under the tool.
- The page is hand-written; only its nav and ad block are rewritten by the build.

## Third-party code

- wanakana 5.3.1 (MIT, `vendor/wanakana.min.js`, license in `vendor/wanakana.LICENSE`): romaji/kana conversion for the keyboard and the kanji translator.
- animCJK stroke data (LGPL, `strokes/`): stroke order diagrams.

## Ads

- Adsterra Native Banner only: one slot per page, labelled "Advertisement", after the main content. About and Privacy have none.
- The slot stays hidden until an ad loads, so visitors never see an empty box.
- Social Bar and Smartlink are switched off; their code is kept as comments.
- All ad code is set in the `ADS` dict in `scripts/build_site.py` and inserted by `apply_ads()` between `<!-- ad:* -->` markers. Set a unit to `None` and rebuild to remove it.
- `ads.txt` holds the Google AdSense publisher line.

## Contact form

The About page form posts to Formspree (form ID mqppqrwq).

## Build (generated pages)

```bash
python3 scripts/build_site.py
```

This generates the hiragana and katakana charts, the yoon chart, the Japanese keyboard page, the katakana quiz, the stroke order indexes and all character pages, and `sitemap.xml`. It also rewrites the nav in the hand-written pages and refreshes the ad blocks on every page.

Do not edit `index.html`, `katakana-chart/`, `yoon-chart/`, `japanese-keyboard/index.html`, `katakana-quiz/`, `hiragana/`, `katakana/`, or `sitemap.xml` by hand: change `scripts/build_site.py` or `scripts/kana_data.py` and rebuild. Edits to `quiz/index.html` flow into `katakana-quiz/` on the next build.

## IndexNow (Bing)

The key file is at the site root (`92df07167f3a1127f9208ef0e9ebefe3.txt`). After a deploy that adds or changes pages:

```bash
python3 scripts/indexnow.py
```

## Deploy

Static site on Vercel. Domain hiragana-chart.com on Namecheap. `vercel.json` sets clean URLs without trailing slashes, the katakana quiz redirect, and long caching for `/audio` and `/strokes`.
