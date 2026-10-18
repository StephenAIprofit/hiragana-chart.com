# Hiragana Chart

Live site: https://hiragana-chart.com/

A static Japanese learning site: Hiragana chart, kana quiz, and Kanji translator.

## Pages

| Page | URL | What it does |
| --- | --- | --- |
| Chart | https://hiragana-chart.com/ | Basic 46, dakuten, yoon, sokuon, stroke order, audio, printable table |
| Quiz | https://hiragana-chart.com/quiz | L1–L4 difficulty, Hiragana and Katakana, instant score, combo, review |
| Kanji Translator | https://hiragana-chart.com/kanji-translator | English, Romaji, or kana to Kanji. Handwriting lookup stays on the page |

## Navigation

Desktop: Chart ▾, Quiz, Kanji Translator | Pronunciation, Printable table, FAQ.

Chart dropdown: Hiragana 46, Dakuten & Handakuten, Yoon, Katakana, Sokuon & Long Vowels, Stroke order.

Mobile: hamburger menu with the same items.

## Chart page

The switcher changes the whole table between Hiragana and Katakana. Titles, examples, the printable table, and the quiz links follow the switcher.

- Basic 46: あ to ん, in gojuon order.
- Dakuten and handakuten: 25 characters. ぢ and じ share ji.mp3. づ and ず share zu.mp3. 23 audio files cover 25 characters.
- Yoon: 36 contracted sounds. ぢゃ, ぢゅ, and ぢょ share ja.mp3, ju.mp3, and jo.mp3 with じゃ, じゅ, and じょ. 33 audio files cover 36 sounds. ぢゃ, ぢゅ, and ぢょ are rare and use the same sound as じゃ, じゅ, and じょ.
- Sokuon: っ / ッ. Four examples with audio: がっこう, きって, ずっと, やっぱり.
- Long vowels: Katakana uses ー. Hiragana uses おう, おお, or えい.
- Romaji is Hepburn: し shi, ち chi, つ tsu, ふ fu, を wo.
- Click a character to hear it, see the stroke order, and scroll to the detail panel.
- Basic 46 and dakuten show one diagram. Yoon shows the base character and the small kana side by side, and the stroke count is the sum.
- If a diagram is missing, the panel shows: Stroke order animation is not available. Audio only.
- Quiz links: `/quiz#basic`, `/quiz#dakuten`, `/quiz#yoon`. In Katakana mode they add `?script=katakana`.

## Quiz page

- L1 Basic 46 (default).
- L2 adds dakuten and handakuten (71).
- L3 adds yoon (107).
- L4 is the full set.
- Katakana mirrors the same levels at `?script=katakana`.
- Hash preselect: `#basic`, `#dakuten`, `#yoon`, `#katakana`.
- The FAQ switches between Hiragana and Katakana.
- Two directions: Romaji → kana, and kana → Romaji.

## Kanji Translator page

- Input English, Romaji, or kana. The page returns the Kanji, reading, and English meaning.
- Dictionary is the JMdict common-word set: 22,645 entries.
- Exact English matches rank first. Searching water puts 水 first.
- Result cards do not open a stroke panel. The handwriting panel stays for lookup by drawing.
- Result cards are three rows: Kanji, reading, meaning.

## Capitalization

Hiragana, Katakana, Romaji, and Kanji are capitalized in visible text. kana is lowercase except at the start of a sentence. URLs, code, and file names stay lowercase. FAQ stays uppercase.

## Audio

Audio files live in `audio/<romaji>.mp3`.

Basic 46, dakuten (23 files for 25 characters), yoon (33 files for 36 sounds), and four sokuon examples: gakkou, kitte, zutto, yappari.

## Sources

- Dictionary: JMdict by EDRDG, CC BY-SA 4.0.
- Handwriting recognition: HanziLookup.

## Repo layout

```
index.html
styles.css
app.js
nav.css
nav.js
audio/                  mp3 files
strokes/                basic animCJK SVG files
quiz/index.html
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

The site is a static site on Vercel, with the domain hiragana-chart.com on Namecheap.

After a content change:

1. Commit and push to GitHub.
2. Wait for the Vercel deployment.
3. In Google Search Console, request indexing for the homepage if you want a faster recrawl.
