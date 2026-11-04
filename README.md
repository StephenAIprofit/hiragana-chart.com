# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: Hiragana and Katakana chart, kana quiz, and Kanji translator.

## Pages

```
| Page             | URL                                         | What it does                                                           |
| ---------------- | ------------------------------------------- | ---------------------------------------------------------------------- |
| Chart            | https://hiragana-chart.com/                 | Basic 46, dakuten, yoon, sokuon, stroke order, audio, printable tables |
| Quiz             | https://hiragana-chart.com/quiz             | Characters and Words modes, L1–L4, Hiragana and Katakana. Kana Book button links to https://stephenzy2.gumroad.com/l/kanabook |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | Draw or type. English, Romaji, or kana to Kanji                        |
| About            | https://hiragana-chart.com/about            | Why the site exists, contact form                                      |
| Privacy          | https://hiragana-chart.com/privacy          | No login, quiz data in session, cookies and ads                        |
```

## Navigation

Desktop: Home | Chart ▾ | Quiz | Kanji Translator.

Chart dropdown: Hiragana 46, Dakuten & Handakuten, Yoon, Katakana, Sokuon & Long Vowels, Stroke order.

## Chart page

The switcher changes the whole table between Hiragana and Katakana.

- Detail panel is sticky. On load it loops the stroke order of あ with no sound. Clicking a character loads that character.
- Basic 46, dakuten, yoon. Sokuon examples are in the FAQ.
- Printable tables and confusable tables. Printable table switches with the script.
- Audio plays only when a character or sokuon example is clicked.
- H1: Hiragana Chart: 46 basic, 107 with Dakuten and Yoon.

## Quiz page

- Script tabs: Hiragana, Katakana, and a Kana Book link (https://stephenzy2.gumroad.com/l/kanabook).
- Characters mode and Words mode.
- L1–L4. L4 is the same set as L3 (107). Katakana at `?script=katakana`.
- Wrong answers return in the same session. Nothing is stored on a server.

## Kanji Translator page

- Draw or Type.
- Results show Kanji, reading, and English.
- Page width matches the other pages (1080px).

## Footer

About and Privacy links. No email address in the footer.

## Contact form

The About page form posts to Formspree (form ID mqppqrwq).

## Deploy

Static site on Vercel. Domain hiragana-chart.com on Namecheap.
