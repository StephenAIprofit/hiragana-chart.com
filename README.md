# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: Hiragana and Katakana chart, kana quiz, Kanji translator, and learning guides.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | Basic 46, dakuten, yoon, sokuon, stroke order, audio, printable tables |
| Katakana chart | https://hiragana-chart.com/katakana-chart | Same chart in Katakana (generated) |
| Stroke order pages | https://hiragana-chart.com/hiragana, /katakana | Index plus one page per character, e.g. /hiragana/ka, /katakana/shi (generated) |
| Katakana Quiz | https://hiragana-chart.com/katakana-quiz | Quiz opened in Katakana (generated from quiz/index.html) |
| Quiz | https://hiragana-chart.com/quiz | Characters and Words modes, L1–L4, Hiragana and Katakana. Get the Workbook · $9.90 button links to https://stephenzy2.gumroad.com/l/kanabook |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | Draw or type. English, Romaji, or kana to Kanji |
| Hiragana Quiz guide | https://hiragana-chart.com/hiragana-quiz-guide | How the quiz works: levels, modes, wrong-answer review |
| Confusable kana | https://hiragana-chart.com/confusable-kana | Pairs that look alike, plus the two confusable tables |
| Dakuten and Yoon | https://hiragana-chart.com/dakuten-yoon-guide | Rules for dakuten, handakuten, and yoon |
| About | https://hiragana-chart.com/about | Why the site exists, contact form |
| Privacy | https://hiragana-chart.com/privacy | No login, quiz data in session, cookies and ads |

## Navigation

Desktop: Home | Chart ▾ | Quiz | Kanji Translator | Guides ▾.

Chart dropdown: Hiragana 46, Dakuten & Handakuten, Yoon, Katakana, Sokuon & Long Vowels, Stroke order.

Guides dropdown: Hiragana Quiz guide, Confusable kana, Dakuten and Yoon.

## Chart page

The switcher changes the whole table between Hiragana and Katakana.

- Detail panel is sticky. On load it loops the stroke order of あ with no sound. Clicking a character loads that character.
- Basic 46, dakuten, yoon. Sokuon examples are in the FAQ.
- Printable tables. The two confusable tables moved to /confusable-kana.
- Audio plays only when a character or sokuon example is clicked.
- H1: Hiragana Chart: 46 basic, 107 with Dakuten and Yoon.

## Quiz page

- Script tabs: Hiragana, Katakana, and a Get the Workbook · $9.90 button (book icon) (https://stephenzy2.gumroad.com/l/kanabook) that opens in a new tab.
- Characters mode and Words mode.
- L1–L4. L4 is the same set as L3 (107). Katakana at `/katakana-quiz` (old `/quiz?script=katakana` links redirect there).
- Wrong answers return in the same session. Nothing is stored on a server.

## Kanji Translator page

- Draw or Type.
- Results show Kanji, reading, and English.
- Page width matches the other pages (1080px).

## Footer

About and Privacy links, plus the three guides. No email address in the footer.

## Contact form

The About page form posts to Formspree (form ID mqppqrwq).

## Build (generated pages)

The chart pages, character pages, Katakana quiz, sitemap, and the shared nav are generated:

```bash
python3 scripts/build_site.py
```

Do not edit `index.html`, `katakana-chart/`, `katakana-quiz/`, `hiragana/`, `katakana/`, or `sitemap.xml` by hand: change `scripts/build_site.py` or `scripts/kana_data.py` and rebuild. Edits to `quiz/index.html` flow into `katakana-quiz/` on the next build.

## IndexNow (Bing)

The key file is at the site root (`92df07167f3a1127f9208ef0e9ebefe3.txt`). After each deploy:

```bash
python3 scripts/indexnow.py
```

## Deploy

Static site on Vercel. Domain hiragana-chart.com on Namecheap.
