# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: Hiragana chart, kana quiz, and Kanji translator.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | Basic 46, dakuten, yoon, sokuon, stroke order, audio, printable tables, confusable tables |
| Quiz | https://hiragana-chart.com/quiz | Characters and Words modes, L1–L4, Hiragana and Katakana |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | Draw or type. English, Romaji, or kana to Kanji |

## Navigation

Desktop: Chart ▾, Quiz, Kanji Translator | Pronunciation, Printable table, FAQ.

Chart dropdown: Hiragana 46, Dakuten & Handakuten, Yoon, Katakana, Sokuon & Long Vowels, Stroke order.

## Chart page

The switcher changes the whole table between Hiragana and Katakana.

- Basic 46, dakuten (25 characters, 23 audio files), yoon (36 sounds, 33 audio files).
- Sokuon examples: がっこう, きって, ずっと, やっぱり.
- Printable Hiragana chart and printable Katakana chart.
- Visual confusables table and pronunciation confusables table.
- The detail panel stays fixed at the top while you scroll. Clicking a character updates the panel without jumping the page.
- Audio plays only when you click a character or a sokuon example. The page does not play sound on load.
- Yoon shows the base character and the small kana side by side. Stroke count is the sum.
- If a diagram is missing: Stroke order animation is not available. Audio only.

## Quiz page

- Characters mode: Romaji → kana, or kana → Romaji.
- Words mode: an English word, pick the correct kana. Each word appears once per round. Wrong answers return for review.
- L1 Basic 46. L2 adds dakuten. L3 adds yoon. L4 is the full set.
- Katakana mirrors the levels at `?script=katakana`.
- A correct answer turns the option green and shows Correct, then Next.
- A wrong answer turns the selected option red, the correct option green, and shows Correct: [answer], then Next.

## Kanji Translator page

- Draw tab: write a Kanji in the box. Handwriting recognition looks it up.
- Type tab: type English, Romaji, or kana.
- Results show the Kanji, reading, and English. Exact English matches rank first.
- Dictionary is the JMdict common-word set: 22,645 entries.

## Capitalization

Hiragana, Katakana, Romaji, and Kanji are capitalized in visible text. kana is lowercase except at the start of a sentence.

## Deploy

Static site on Vercel. Domain hiragana-chart.com on Namecheap.

After a content change: commit and push to GitHub, wait for Vercel.
