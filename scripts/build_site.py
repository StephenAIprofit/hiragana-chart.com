#!/usr/bin/env python3
"""Build the static, crawlable pages of hiragana-chart.com.

Run from the repository root:  python3 scripts/build_site.py

Generates (do not edit these by hand, edit this script instead):
  index.html                     Hiragana chart (static grids and table)
  katakana-chart/index.html      Katakana chart
  katakana-quiz/index.html       Katakana quiz (derived from quiz/index.html)
  hiragana/index.html            Hiragana stroke order index
  hiragana/<slug>/index.html     One page per hiragana (107)
  katakana/index.html            Katakana stroke order index
  katakana/<slug>/index.html     One page per katakana (107)
  sitemap.xml

It also rewrites the shared <nav> block in the hand-written pages
(quiz, kanji-translator, guides, about, privacy) so navigation stays the same
everywhere.
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kana_data import (BASIC, DAKUTEN, YOON, SMALL_K, ROWS, NOTES, H_WORDS,
                       K_WORDS, CONFUSABLE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://hiragana-chart.com"
TODAY = date.today().isoformat()
E = html.escape

HAND_WRITTEN = ["quiz", "kanji-translator", "hiragana-quiz-guide",
                "confusable-kana", "dakuten-yoon-guide", "about", "privacy"]

# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------
ROW_OF = {}
for row, cons, cells in ROWS:
    for col, r in zip("aiueo", cells):
        if r:
            ROW_OF[r] = (row, col, cons)


def build_entries():
    """Return a list of dicts, one per sound, in chart order."""
    out = []
    for h, k, r in BASIC:
        out.append(dict(h=h, k=k, romaji=r, slug=r, audio=r, group="basic",
                        base=None, small=None))
    for h, k, r, slug, base, mark in DAKUTEN:
        out.append(dict(h=h, k=k, romaji=r, slug=slug, audio=r, group=mark,
                        base=base, small=None))
    for h, k, r, slug, base, small in YOON:
        out.append(dict(h=h, k=k, romaji=r, slug=slug, audio=r, group="yoon",
                        base=base, small=small))
    return out


ENTRIES = build_entries()
BY_H = {e["h"]: e for e in ENTRIES}
BY_K = {e["k"]: e for e in ENTRIES}
H2K = {e["h"]: e["k"] for e in ENTRIES}
H2K.update(SMALL_K)

SCRIPTS = {
    "hiragana": dict(name="Hiragana", other="katakana", Other="Katakana",
                     chart="/", quiz="/quiz", words=H_WORDS),
    "katakana": dict(name="Katakana", other="hiragana", Other="Hiragana",
                     chart="/katakana-chart", quiz="/katakana-quiz", words=K_WORDS),
}


def kana(e, script):
    return e["h"] if script == "hiragana" else e["k"]


def to_script(h_char, script):
    return h_char if script == "hiragana" else H2K[h_char]


WORKBOOK_URL = "https://stephenzy2.gumroad.com/l/kanabook"
BOOK_ICON = ('<svg class="book-icon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
             '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5" '
             'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
             '<path d="M8 8h8M8 12h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')


def is_thin(e, script):
    """Pages without an example word are short and mostly template text: keep them out of the index."""
    return SCRIPTS[script]["words"].get(e["slug"]) is None


def char_url(e, script):
    return "/%s/%s" % (script, e["slug"])


# --------------------------------------------------------------------------
# Stroke order SVGs (animCJK, stored in /strokes)
# --------------------------------------------------------------------------
_svg_cache = {}


def strokes_of(ch):
    """Return [(stroke_no, [path d...], start_point or None)] for one character."""
    if ch in _svg_cache:
        return _svg_cache[ch]
    path = os.path.join(ROOT, "strokes", "%d.svg" % ord(ch))
    with open(path, encoding="utf-8") as f:
        text = f.read()
    shapes = {}
    for m in re.finditer(r'<path id="z\d+d(\d+)[a-z]?" d="([^"]+)"', text):
        shapes.setdefault(int(m.group(1)), []).append(m.group(2))
    starts = {}
    for m in re.finditer(r'clip-path="url\(#z\d+c(\d+)[a-z]?\)" d="M\s*(-?\d+)[ ,]+(-?\d+)', text):
        no, x, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if x >= 0 and no not in starts:
            starts[no] = (x, y)
    result = [(no, shapes[no], starts.get(no)) for no in sorted(shapes)]
    _svg_cache[ch] = result
    return result


def stroke_count(e, script):
    chars = [kana(e, script)] if e["group"] != "yoon" else [
        to_script(e["base"], script), to_script(e["small"], script)]
    return sum(len(strokes_of(c)) for c in chars)


def animated_svg(ch, cls="", offset=0.0):
    parts = ['<svg viewBox="0 0 1024 1024"%s aria-hidden="true">' % (' class="%s"' % cls if cls else "")]
    for i, (no, ds, start) in enumerate(strokes_of(ch)):
        delay = "%.1fs" % (offset + i * 0.7)
        for d in ds:
            parts.append('<path class="glyph-stroke" style="animation-delay:%s" d="%s"/>' % (delay, d))
        if start:
            x, y = start
            parts.append('<g class="stroke-badge" style="animation-delay:%s"><circle cx="%d" cy="%d" r="36"/>'
                         '<text x="%d" y="%d" text-anchor="middle">%d</text></g>' % (delay, x, y, x, y + 12, no))
    parts.append("</svg>")
    return "".join(parts)


def step_svgs(ch, label_prefix=""):
    """One small static SVG per stroke: earlier strokes grey, current stroke dark."""
    items = strokes_of(ch)
    out = []
    for i, (no, _, start) in enumerate(items):
        p = ['<figure class="step"><svg viewBox="0 0 1024 1024" role="img" aria-label="%s stroke %d of %d">'
             % (E(label_prefix + ch), no, len(items))]
        for j, (_, ds, _) in enumerate(items[: i + 1]):
            c = "step-now" if j == i else "step-done"
            for d in ds:
                p.append('<path class="%s" d="%s"/>' % (c, d))
        if start:
            x, y = start
            p.append('<circle class="step-dot" cx="%d" cy="%d" r="44"/><text class="step-no" x="%d" y="%d" '
                     'text-anchor="middle">%d</text>' % (x, y, x, y + 15, no))
        p.append("</svg><figcaption>%d</figcaption></figure>" % no)
        out.append("".join(p))
    return "".join(out)


# --------------------------------------------------------------------------
# Shared layout
# --------------------------------------------------------------------------
NAV = """<nav class="nav-links" aria-label="Site">
      <a href="/">Home</a>
      <div class="dropdown">
        <button class="nav-btn" type="button">Chart ▾</button>
        <div class="dropdown-menu">
          <a href="/#chart">Hiragana chart</a>
          <a href="/#dakuten">Dakuten & Handakuten</a>
          <a href="/#yoon">Yoon</a>
          <a href="/katakana-chart">Katakana chart</a>
          <a href="/#special">Sokuon & Long Vowels</a>
          <a href="/hiragana">Hiragana stroke order</a>
          <a href="/katakana">Katakana stroke order</a>
        </div>
      </div>
      <div class="dropdown">
        <button class="nav-btn" type="button">Quiz ▾</button>
        <div class="dropdown-menu">
          <a href="/quiz">Hiragana quiz</a>
          <a href="/katakana-quiz">Katakana quiz</a>
        </div>
      </div>
      <a href="/kanji-translator">Kanji Translator</a>
      <div class="dropdown">
        <button class="nav-btn" type="button">Guides ▾</button>
        <div class="dropdown-menu">
          <a href="/hiragana-quiz-guide">Hiragana Quiz guide</a>
          <a href="/confusable-kana">Confusable kana</a>
          <a href="/dakuten-yoon-guide">Dakuten and Yoon</a>
        </div>
      </div>
    </nav>"""

HEADER = """<header class="wrap nav">
    <a class="brand" href="/"><img class="mark" src="/logo.png" width="36" height="36" alt="Hiragana Chart logo"><span>Hiragana Chart</span></a>
    <button class="hamburger" type="button" aria-label="Menu">☰</button>
    """ + NAV + """
  </header>"""

FOOTER = """<footer>
    <div class="wrap">
      <p class="site-banner"><a href="/kanji-translator">Kanji Translator</a><a href="/quiz">Hiragana Quiz</a><a href="/katakana-quiz">Katakana Quiz</a></p>
      <p><a href="/">Hiragana chart</a> · <a href="/katakana-chart">Katakana chart</a> · <a href="/hiragana">Hiragana stroke order</a> · <a href="/katakana">Katakana stroke order</a></p>
      <p><a href="/hiragana-quiz-guide">Hiragana Quiz guide</a> · <a href="/confusable-kana">Confusable kana</a> · <a href="/dakuten-yoon-guide">Dakuten and Yoon</a></p>
      <p><a href="/about">About</a> · <a href="/privacy">Privacy</a></p>
    </div>
  </footer>"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=IBM+Plex+Sans:wght@400;600&family=Noto+Sans+JP:wght@400;500&family=Noto+Serif+JP:wght@500&display=swap" rel="stylesheet">')


def head(title, desc, path, jsonld, og_title=None, og_desc=None, og_alt=None, robots=None):
    url = SITE + path
    blocks = "\n".join('  <script type="application/ld+json">\n%s\n</script>' % json.dumps(j, ensure_ascii=False, indent=1)
                       for j in jsonld)
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#f6f1e7">
  <link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="canonical" href="{url}">{robots}
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{site}/og-image.png">
  {fonts}
  <link rel="stylesheet" href="/nav.css">
  <link rel="stylesheet" href="/styles.css">
{blocks}
</head>""".format(title=E(title), desc=E(desc), url=url, site=SITE, fonts=FONTS,
                  og_title=E(og_title or title), og_desc=E(og_desc or desc),
                  og_alt=E(og_alt or title), blocks=blocks,
                  robots='\n  <meta name="robots" content="%s">' % robots if robots else "")


def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                for i, (n, p) in enumerate(items)]}


def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                           for q, a in qas]}


def faq_html(qas, insert_after=None, insert_html=""):
    out = []
    for q, a in qas:
        attr = ' id="special"' if q == insert_after else ""
        out.append('      <details%s><summary>%s</summary><p>%s</p></details>' % (attr, q, a))
        if q == insert_after:
            out.append(insert_html)
    return "\n".join(out)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------
# Chart pages ( / and /katakana-chart )
# --------------------------------------------------------------------------
def grid_html(entries, script):
    cells = []
    for e in entries:
        attrs = 'data-kana="%s" data-romaji="%s" data-audio="%s" data-href="%s"' % (
            kana(e, script), e["romaji"], e["audio"], char_url(e, script))
        if e["group"] == "yoon":
            attrs += ' data-base="%s" data-small="%s"' % (to_script(e["base"], script), to_script(e["small"], script))
        cells.append('<button class="cell" type="button" %s><span class="kana">%s</span>'
                     '<span class="romaji">%s</span></button>' % (attrs, kana(e, script), e["romaji"]))
    return "\n        ".join(cells)


def table_rows(script):
    rows = []
    for row, _, cells in ROWS:
        tds = []
        for r in cells:
            if not r:
                tds.append("<td></td>")
                continue
            e = next(x for x in ENTRIES if x["group"] == "basic" and x["romaji"] == r)
            tds.append('<td><a href="%s"><b>%s</b><br>%s</a></td>' % (char_url(e, script), kana(e, script), r))
        label = "" if row == "a" else ("n" if row == "n" else row[0])
        rows.append("<tr><th>%s</th>%s</tr>" % (label, "".join(tds)))
    return "\n          ".join(rows)


def stroke_links(script):
    links = []
    for e in ENTRIES:
        if e["group"] != "basic":
            continue
        links.append('<a href="%s"><span class="kana">%s</span><span class="romaji">%s</span></a>' % (
            char_url(e, script), kana(e, script), e["romaji"]))
    return "\n        ".join(links)


H_FAQ = [
    ("How do I read a Hiragana chart?", "Read left to right, top to bottom. Each row shares a consonant: the ka row is ka, ki, ku, ke, ko. Learn by row, not by column. The empty cells in the ya row and wa row are sounds that do not exist in modern Japanese. Try it: pick the a row, click each character, and say it aloud while you look at its stroke order."),
    ("How many characters are there, including Dakuten and Yoon?", "There are 46 basic characters, from あ to ん. Dakuten and Handakuten add 25, for 71 in total. Yoon adds 36, for 107 in total. The obsolete ゐ and ゑ are not included. Dakuten, Handakuten, and Yoon are not a separate alphabet; they are extensions of the same 46 sounds."),
    ("What Romaji does this chart use?", "Hepburn Romaji. し is shi, not si; ち is chi, not ti; つ is tsu, not tu; ふ is fu; を is written wo. This matters for typing: type じ as ji and ぢ as di, even though both sound like ji in modern Japanese. The same applies to ず as zu and づ as du."),
    ("How do I pronounce shi, chi, tsu, fu, and ん?", "し is shi, ち is chi, つ is tsu, like the end of cats, ふ is a soft fu blown between the lips, halfway between h and f. ん is a syllabic n and takes one beat: にほん has three beats, ni-ho-n. Click any character on the chart to hear it, then say it aloud while you write it."),
    ("Why do は, へ, and を sound different in sentences?", "On the chart you see their dictionary readings: ha, he, wo. In sentences they are particles and change sound: は is wa, へ is e, and を is o. Example: は marks the topic, へ marks direction, and を marks the object. Do not relearn the characters; learn the particle use on top of the chart reading."),
    ("What is the difference between Hiragana and Katakana, and when do I use each?", "Hiragana writes native Japanese words and grammar. Katakana writes foreign loanwords, names, and emphasis. The sounds are the same 46 sounds. Example: コーヒー and コンピューター are Katakana because they are loanwords. Open the <a href=\"/katakana-chart\">Katakana chart</a> to see the same table in the other script, then test yourself in the <a href=\"/katakana-quiz\">Katakana quiz</a>."),
    ("What are Dakuten, Handakuten, and Yoon?", "Dakuten adds two dots and voices the sound: か becomes が. Handakuten adds a circle: は becomes ぱ. Yoon is a large kana plus a small ゃ, ゅ, or ょ, and counts as one beat, not two: きゃ is kya, one beat, while きや is ki-ya, two beats. In modern Japanese, ぢゃ, ぢゅ, and ぢょ sound the same as じゃ, じゅ, and じょ, and are rare."),
    ("What are Sokuon and long vowels?", "Sokuon is a small っ or ッ. It has no sound of its own; it doubles the next consonant and takes one beat. In Romaji this shows as a doubled letter: がっこう is gakkou, with kk. For long vowels, Katakana uses ー, as in コーヒー. Hiragana uses おう, おお, or えい, as in おかあさん, とおい, and せんせい. Tap an example to hear the doubled consonant."),
    ("Do I need to learn stroke order, and how do I see it?", "Click any character. The panel shows its numbered strokes in order. For Yoon, it shows the base character first, then the small kana, and the stroke count is the sum. If you only need to read, you can skip stroke order. If you write by hand, correct stroke order keeps characters balanced and readable. Practice by tracing the Printable chart, then writing the same character without looking."),
    ("How long does it take to learn Hiragana, and how should I practice?", "Most learners recognize the basic 46 in one to two weeks at one row a day, then need more weeks to read them quickly. That is a typical range, not a guarantee. Practice in this order: learn one row a day in gojuon order, say each character aloud while you write it, test yourself backwards and shuffled, then take Quiz L1. When L1 is comfortable, move to L2 for Dakuten and Handakuten, then L3 for Yoon."),
]

K_FAQ = [
    ("How do I read a Katakana chart?", "The same way as the Hiragana chart: left to right, top to bottom, one consonant per row. ア イ ウ エ オ is the vowel row, カ キ ク ケ コ is the ka row. Every Katakana has a Hiragana partner with the same sound, so if you know あ you already know how ア sounds."),
    ("When is Katakana used instead of Hiragana?", "Katakana writes loanwords (コーヒー, coffee; テレビ, television), foreign names (ロンドン, London), animal and plant names in science, sound effects, and words written for emphasis, much like italics. Native words and grammar endings are written in Hiragana."),
    ("How many Katakana are there?", "46 basic characters, from ア to ン. Dakuten and Handakuten add 25 (ガ to ポ), for 71. Yoon such as キャ, シュ, and チョ add 36, for 107. Loanwords also use extra combinations such as ファ, ティ, and ウィ to write sounds that Japanese does not have."),
    ("How are long vowels written in Katakana?", "With the long-vowel mark ー, called chouon. It doubles the length of the vowel before it: コーヒー is ko-o-hi-i, four beats. Hiragana does not use ー in normal writing; it adds a vowel instead, as in おかあさん."),
    ("Which Katakana are easiest to confuse?", "シ (shi) and ツ (tsu), and ソ (so) and ン (n). For シ and ン the last stroke rises from the bottom left; for ツ and ソ it falls from the top. ク, ケ, and タ, and コ and ユ, are also easy to mix up. See <a href=\"/confusable-kana\">Confusable kana</a> for side-by-side drills."),
    ("Should I learn Hiragana or Katakana first?", "Learn Hiragana first: it is used in every sentence. Start Katakana once the basic 46 Hiragana are comfortable. Because the sounds are the same, Katakana usually takes about half as long. Then test yourself in the <a href=\"/katakana-quiz\">Katakana quiz</a>."),
]

SOKUON = """      <p class="sokuon-examples">
        <button class="word-btn" type="button" data-audio="gakkou">がっこう</button>
        <button class="word-btn" type="button" data-audio="kitte">きって</button>
        <button class="word-btn" type="button" data-audio="zutto">ずっと</button>
        <button class="word-btn" type="button" data-audio="yappari">やっぱり</button>
      </p>"""


def chart_page(script):
    s = SCRIPTS[script]
    name = s["name"]
    basic = [e for e in ENTRIES if e["group"] == "basic"]
    dak = [e for e in ENTRIES if e["group"] in ("dakuten", "handakuten")]
    yoon = [e for e in ENTRIES if e["group"] == "yoon"]
    if script == "hiragana":
        path = "/"
        title = "Hiragana Chart: 46 Characters plus Dakuten and Yoon"
        desc = "Free hiragana chart: 46 basic characters, plus dakuten and yoon (107 total), with stroke-order diagrams, Hepburn romaji, and Japanese audio pronunciation. No login."
        og_title = "Hiragana Chart: 46 Characters, Stroke Order & Audio"
        og_desc = "46 basic characters, plus dakuten and yoon (107 total), with stroke-order diagrams and Japanese audio pronunciation. Free, no login."
        h1 = "Hiragana Chart: 46 basic, 107 with Dakuten and Yoon"
        dak_note = "Dakuten add two dots (が ざ だ ば). Handakuten add a circle (ぱ ぴ ぷ ぺ ぽ). In modern Japanese, ぢ is read ji and づ is read zu."
        yoon_note = "Yoon is a large kana plus a small ゃ, ゅ, or ょ. The small character is not an independent sound. ぢゃ, ぢゅ, and ぢょ are rare; they use the same sound as じゃ, じゅ, and じょ."
        faq = H_FAQ
        faq_body = faq_html(faq, "What are Sokuon and long vowels?", SOKUON)
        jsonld = [faq_ld(faq),
                  {"@context": "https://schema.org", "@type": "WebSite", "name": "Hiragana Chart",
                   "url": SITE + "/"}]
    else:
        path = "/katakana-chart"
        title = "Katakana Chart: 46 Characters plus Dakuten and Yoon"
        desc = "Free katakana chart: all 46 basic katakana, plus dakuten and yoon (107 total), with stroke order, Hepburn romaji, loanword examples, and audio. Printable. No login."
        og_title = "Katakana Chart: 46 Characters, Stroke Order & Audio"
        og_desc = "All 46 katakana plus dakuten and yoon (107 total), with stroke-order diagrams and Japanese audio. Free, no login."
        h1 = "Katakana Chart: 46 basic, 107 with Dakuten and Yoon"
        dak_note = "Dakuten add two dots (ガ ザ ダ バ). Handakuten add a circle (パ ピ プ ペ ポ). In modern Japanese, ヂ is read ji and ヅ is read zu."
        yoon_note = "Yoon is a large kana plus a small ャ, ュ, or ョ. The small character is not an independent sound. ヂャ, ヂュ, and ヂョ are rare; they use the same sound as ジャ, ジュ, and ジョ."
        faq = K_FAQ
        faq_body = faq_html(faq)
        jsonld = [faq_ld(faq), breadcrumb([("Hiragana Chart", "/"), ("Katakana chart", path)])]

    lede = "Basic 46, plus dakuten and yoon for 107 in total. Click a character to hear it and watch its stroke order. Romaji is Hepburn."
    first = basic[0]
    pressed_h = "true" if script == "hiragana" else "false"
    pressed_k = "false" if script == "hiragana" else "true"
    body = """
<body data-script="{script}">
  {header}
  <main class="wrap">
    <p class="kicker">Free · no login</p>
    <h1 id="page-title">{h1}</h1>
    <p class="lede" id="page-lede">{lede}</p>
    <p class="no-print actions">
      <a class="quiz-cta" href="{quiz}">Take the {name} Quiz</a>
      <a class="quiz-cta ghost" href="{oquiz}">Take the {Other} Quiz</a>
    </p>
    <nav class="script-switch" aria-label="Script">
      <a class="script-btn" href="/" aria-current="{cur_h}" aria-pressed="{pressed_h}">Hiragana</a>
      <a class="script-btn" href="/katakana-chart" aria-current="{cur_k}" aria-pressed="{pressed_k}">Katakana</a>
    </nav>
    <section class="detail" id="chart" aria-live="polite">
      <div id="glyph" class="glyph" aria-label="Stroke order diagram">{glyph}</div>
      <div>
        <p class="romaji" id="reading"></p>
        <p id="order">{count} strokes</p>
        <p class="no-print"><button class="play" id="play" type="button">Play audio</button> <button class="play ghost" id="replay-strokes" type="button">Replay strokes</button></p>
        <p class="no-print"><a id="char-link" href="{first_url}">Open the {first_kana} page: stroke order, words, and tips</a></p>
      </div>
    </section>
    <h2>Basic 46</h2>
    <div class="grid" id="grid">
        {grid}
    </div>
    <p class="no-print"><a class="quiz-cta" href="{quiz}#basic">Quiz this set</a></p>
    <section id="dakuten">
      <h2 id="dakuten-title">{name} dakuten and handakuten</h2>
      <p id="dakuten-note">{dak_note}</p>
      <div class="grid" id="dakuten-grid">
        {dgrid}
      </div>
      <p class="no-print"><a class="quiz-cta" href="{quiz}#dakuten">Quiz this set</a></p>
    </section>
    <section id="yoon">
      <h2 id="yoon-title">{name} yoon (contracted sounds)</h2>
      <p id="yoon-note">{yoon_note}</p>
      <div class="grid" id="yoon-grid">
        {ygrid}
      </div>
      <p class="no-print"><a class="quiz-cta" href="{quiz}#yoon">Quiz this set</a></p>
    </section>
    <section class="section printable" id="table">
      <h2>Printable {name} chart</h2>
      <p class="no-print"><button class="print" id="print" type="button">Print this table</button></p>
      <table>
        <caption>46 {name} characters with Hepburn Romaji</caption>
        <thead><tr><th></th><th>a</th><th>i</th><th>u</th><th>e</th><th>o</th></tr></thead>
        <tbody id="table-body">
          {rows}
        </tbody>
      </table>
    </section>
    <section class="section no-print" id="stroke-order">
      <h2>{name} stroke order</h2>
      <p>Each character has its own page with a numbered stroke-by-stroke diagram, audio, an example word, and the look-alikes to watch for. <a href="/{script}">See all 107 {name} stroke order pages</a>.</p>
      <div class="link-grid">
        {links}
      </div>
    </section>
    <section class="section" id="faq">
      <h2>Common questions</h2>
{faq}
    </section>
  </main>
  {footer}
  <script src="/nav.js"></script>
  <script src="/app.js"></script>
</body>
</html>
""".format(script=script, header=HEADER, h1=h1, lede=lede, name=name, Other=s["Other"],
           quiz=s["quiz"], oquiz=SCRIPTS[s["other"]]["quiz"],
           cur_h="page" if script == "hiragana" else "false",
           cur_k="page" if script == "katakana" else "false",
           pressed_h=pressed_h, pressed_k=pressed_k,
           glyph=animated_svg(kana(first, script)), count=stroke_count(first, script),
           first_url=char_url(first, script), first_kana=kana(first, script),
           grid=grid_html(basic, script), dgrid=grid_html(dak, script), ygrid=grid_html(yoon, script),
           dak_note=dak_note, yoon_note=yoon_note, rows=table_rows(script),
           links=stroke_links(script), faq=faq_body, footer=FOOTER)
    page = head(title, desc, path, jsonld, og_title, og_desc,
                "%s Chart: all 46 %s characters with stroke order and audio" % (name, name.lower())) + body
    write("index.html" if script == "hiragana" else "katakana-chart/index.html", page)


# --------------------------------------------------------------------------
# Character pages ( /hiragana/<slug>, /katakana/<slug> )
# --------------------------------------------------------------------------
GROUP_LABEL = {"basic": "Basic 46", "dakuten": "Dakuten", "handakuten": "Handakuten", "yoon": "Yoon"}


def describe(e, script):
    k = kana(e, script)
    r = e["romaji"]
    if e["group"] == "basic":
        row, col, cons = ROW_OF[r]
        if cons == "vowel":
            where = "%s is one of the five vowels, in the first row of the chart." % k
        elif r == "n":
            where = "%s is the last character of the chart and stands on its own row." % k
        else:
            where = "%s sits in the %s row, %s column of the gojuon chart." % (k, row, col)
        return where
    if e["group"] in ("dakuten", "handakuten"):
        base = to_script(e["base"], script)
        mark = "two dots (dakuten)" if e["group"] == "dakuten" else "a small circle (handakuten)"
        return "%s is %s with %s added. The mark changes the sound from %s to %s." % (
            k, base, mark, BY_H[e["base"]]["romaji"], r)
    base, small = to_script(e["base"], script), to_script(e["small"], script)
    return ("%s is a yoon: %s (%s) plus a small %s. The two characters are read together as one beat, %s."
            % (k, base, BY_H[e["base"]]["romaji"], small, r))


K_NOTES = {
    "ha": "Always read ha. The particle reading wa only applies to the hiragana は.",
    "he": "Always read he. The particle reading e only applies to the hiragana へ.",
    "wo": "Read o, and very rare. ヲ appears mostly in old texts and in text written entirely in katakana; normal writing uses the hiragana を.",
    "ji": "ジ is the normal katakana spelling of ji. ヂ sounds the same but is very rare.",
    "di": "Read ji, the same sound as ジ. It is very rare in katakana; loanwords use ジ. When typing, use di.",
    "zu": "ズ is the normal katakana spelling of zu. ヅ sounds the same but is very rare.",
    "du": "Read zu, the same sound as ズ. It is very rare in katakana; loanwords use ズ. When typing, use du.",
    "n": "The only kana that is just a consonant. It takes one full beat: パン is two beats, pa-n. Before p, b, and m it sounds like m.",
    "u": "An unrounded u: say oo with relaxed, not pushed-out, lips. It is often quiet between voiceless consonants, as in スキー (sukii, sounds like skii).",
    "dya": "Read ja, the same as ジャ. This spelling is almost never used.",
    "dyu": "Read ju, the same as ジュ. This spelling is almost never used.",
    "dyo": "Read jo, the same as ジョ. This spelling is almost never used.",
}
LARGE = {"ゃ": ("や", "ya"), "ゅ": ("ゆ", "yu"), "ょ": ("よ", "yo")}


def note(e, script):
    if script == "katakana" and e["slug"] in K_NOTES:
        return K_NOTES[e["slug"]]
    if e["slug"] in NOTES:
        return NOTES[e["slug"]]
    r = e["romaji"]
    if e["group"] == "yoon":
        large, large_r = LARGE[e["small"]]
        base = to_script(e["base"], script)
        return ("Say it as one sound, not %s plus %s. Compare %s (%s, one beat) with %s%s (%s-%s, two beats)."
                % (BY_H[e["base"]]["romaji"], large_r, kana(e, script), r, base, to_script(large, script),
                   BY_H[e["base"]]["romaji"], large_r))
    return ("%s is the %s sound followed by a short, pure %s. Keep the vowel short and do not let it glide."
            % (r, r[:-1], r[-1]))


def related(e):
    """Same-row neighbours (same group) as hiragana entries."""
    if e["group"] == "basic":
        row = ROW_OF[e["romaji"]][0]
        return [x for x in ENTRIES if x["group"] == "basic" and ROW_OF[x["romaji"]][0] == row]
    if e["group"] in ("dakuten", "handakuten"):
        same = [x for x in ENTRIES if x["group"] in ("dakuten", "handakuten") and x["romaji"][0] == e["romaji"][0]
                and x["group"] == e["group"]]
        return same
    return [x for x in ENTRIES if x["group"] == "yoon" and x["base"] == e["base"]]


def confusables(e, script):
    k = kana(e, script)
    for g in CONFUSABLE:
        if k in g:
            return [c for c in g if c != k]
    return []


def char_page(e, script, prev_e, next_e):
    s = SCRIPTS[script]
    name, other = s["name"], s["other"]
    k = kana(e, script)
    ok = kana(e, other)
    r = e["romaji"]
    n = stroke_count(e, script)
    path = char_url(e, script)
    word = s["words"].get(e["slug"])
    group = GROUP_LABEL[e["group"]]

    title = "%s %s (%s): Stroke Order, Audio and Example Words" % (name, k, r)
    desc = "How to write %s %s (%s): %d-stroke order diagram, audio pronunciation" % (name.lower(), k, r, n)
    if word:
        desc += ", the example word %s (%s, %s)" % (word[0], word[1], word[2])
    desc += ", and the %s %s." % (s["Other"].lower(), ok)

    # Stroke diagram
    if e["group"] == "yoon":
        b, sm = to_script(e["base"], script), to_script(e["small"], script)
        glyph = animated_svg(b, "glyph-base") + animated_svg(sm, "glyph-small", len(strokes_of(b)) * 0.7)
        steps = ('<p class="step-label">%s (%d strokes)</p><div class="steps">%s</div>'
                 '<p class="step-label">small %s (%d strokes)</p><div class="steps">%s</div>'
                 % (b, len(strokes_of(b)), step_svgs(b), sm, len(strokes_of(sm)), step_svgs(sm, "small ")))
        write_tip = ("Write %s at full size, then the small %s in the lower right of the same square, at about half "
                     "the size. Total: %d strokes." % (b, sm, n))
    else:
        glyph = animated_svg(k)
        steps = '<div class="steps">%s</div>' % step_svgs(k)
        write_tip = ("%s has %d stroke%s. Write them in the numbered order: generally top to bottom and left to "
                     "right, and finish each stroke before starting the next." % (k, n, "" if n == 1 else "s"))
        if e["group"] in ("dakuten", "handakuten"):
            write_tip += " Write %s first, then add the %s in the top right." % (
                to_script(e["base"], script), "two dots" if e["group"] == "dakuten" else "circle")

    # Facts table
    facts = [("Script", name), ("Romaji (Hepburn)", r), ("Set", group), ("Strokes", str(n))]
    if e["group"] == "basic":
        row, col, cons = ROW_OF[r]
        facts.append(("Chart position", "vowel row" if cons == "vowel" else
                      ("own row (syllabic n)" if r == "n" else "%s row, %s column" % (row, col))))
    else:
        be = BY_H[e["base"]]
        facts.append(("Base kana", '<a href="%s">%s (%s)</a>' % (char_url(be, script), kana(be, script), be["romaji"])))
    facts.append(("%s" % s["Other"], '<a href="%s">%s</a>' % (char_url(e, other), ok)))
    if e["slug"] != r:
        facts.append(("Typed as", e["slug"]))
    facts_html = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (a, b) for a, b in facts)

    word_html = ""
    if word:
        word_html = """
    <section class="section">
      <h2>Example word with {k}</h2>
      <table class="facts"><tbody><tr><th scope="row">{name}</th><td><span class="jp">{w}</span></td></tr><tr><th scope="row">Romaji</th><td>{wr}</td></tr><tr><th scope="row">Meaning</th><td>{wm}</td></tr></tbody></table>
    </section>""".format(k=k, name=name, w=word[0], wr=word[1], wm=E(word[2]))
    elif e["group"] == "yoon" or e["slug"] in ("wo", "di", "du"):
        word_html = """
    <section class="section">
      <h2>Is {k} common?</h2>
      <p>{k} is rare in modern {name}. Learn to recognise it, but spend your practice time on the common sounds first.</p>
    </section>""".format(k=k, name=name)

    conf = confusables(e, script)
    conf_html = ""
    if conf:
        lst = []
        for c in conf:
            ce = BY_H.get(c) or BY_K.get(c)
            lst.append('<a href="%s"><span class="kana">%s</span><span class="romaji">%s</span></a>' % (
                char_url(ce, script), c, ce["romaji"]))
        conf_html = """
    <section class="section">
      <h2>Do not confuse {k} with</h2>
      <div class="link-grid">{lst}</div>
      <p>See <a href="/confusable-kana">Confusable kana</a> for the difference and a drill.</p>
    </section>""".format(k=k, lst="".join(lst))

    rel = related(e)
    rel_html = "".join('<a href="%s"%s><span class="kana">%s</span><span class="romaji">%s</span></a>' % (
        char_url(x, script), ' aria-current="page"' if x is e else "", kana(x, script), x["romaji"]) for x in rel)
    rel_title = {"basic": "Same row", "dakuten": "Same dakuten row", "handakuten": "Handakuten row",
                 "yoon": "Same yoon group"}[e["group"]]

    pager = []
    if prev_e:
        pager.append('<a href="%s">← %s %s</a>' % (char_url(prev_e, script), kana(prev_e, script), prev_e["romaji"]))
    pager.append('<a href="/%s">All %s</a>' % (script, name))
    if next_e:
        pager.append('<a href="%s">%s %s →</a>' % (char_url(next_e, script), kana(next_e, script), next_e["romaji"]))

    jsonld = [breadcrumb([("Hiragana Chart", "/"), ("%s stroke order" % name, "/" + script), ("%s (%s)" % (k, r), path)])]
    chart = s["chart"]
    anchor = {"basic": "#grid", "dakuten": "#dakuten", "handakuten": "#dakuten", "yoon": "#yoon"}[e["group"]]
    quiz_hash = {"basic": "#basic", "dakuten": "#dakuten", "handakuten": "#dakuten", "yoon": "#yoon"}[e["group"]]

    body = """
<body data-script="{script}">
  {header}
  <main class="wrap char-page">
    <p class="crumb"><a href="/">Hiragana chart</a> / <a href="/{script}">{name} stroke order</a> / {k}</p>
    <p class="kicker">{name} · {group}</p>
    <h1>{name} {k} ({r})</h1>
    <p class="lede">{describe} Click play to hear it, and watch the numbered strokes below.</p>
    <section class="detail" aria-live="polite">
      <div id="glyph" class="glyph" aria-label="Stroke order animation for {k}">{glyph}</div>
      <div>
        <p class="romaji big-kana"><span class="jp">{k}</span> {r}</p>
        <p>{n} stroke{plural}</p>
        <p class="no-print"><button class="play" id="play" type="button" data-audio="{audio}" data-kana="{k}">Play audio</button> <button class="play ghost" id="replay-strokes" type="button">Replay strokes</button></p>
      </div>
    </section>
    <section class="section">
      <h2>How to write {k}: stroke order</h2>
      {steps}
      <p>{write_tip}</p>
      <aside class="workbook-cta no-print">
        <p>Practise writing {k} by hand, then keep going with the rest of the kana in the workbook.</p>
        <a class="workbook-btn" href="{wb}" target="_blank" rel="noopener">{icon}Get the Workbook · $9.90</a>
      </aside>
    </section>
    <section class="section">
      <h2>How to pronounce {k}</h2>
      <p>{note}</p>
    </section>{word}
    <section class="section">
      <h2>{k} at a glance</h2>
      <table class="facts"><tbody>{facts}</tbody></table>
    </section>{conf}
    <section class="section">
      <h2>{rel_title}</h2>
      <div class="link-grid">{rel}</div>
      <p class="no-print actions"><a class="quiz-cta" href="{quiz}{quiz_hash}">Quiz this set</a> <a href="{chart}{anchor}">See {k} on the full {name} chart</a></p>
    </section>
    <nav class="pager" aria-label="Previous and next">{pager}</nav>
  </main>
  {footer}
  <script src="/nav.js"></script>
  <script src="/char.js"></script>
</body>
</html>
""".format(script=script, header=HEADER, name=name, k=k, r=r, group=group, describe=E(describe(e, script)),
           glyph=glyph, n=n, plural="" if n == 1 else "s", audio=e["audio"], steps=steps, write_tip=write_tip,
           note=note(e, script), word=word_html, facts=facts_html, conf=conf_html, rel_title=rel_title,
           rel=rel_html, chart=chart, anchor=anchor, quiz=s["quiz"], quiz_hash=quiz_hash,
           pager=" ".join(pager), footer=FOOTER, wb=WORKBOOK_URL, icon=BOOK_ICON)
    robots = "noindex, follow" if is_thin(e, script) else None
    write(path.lstrip("/") + "/index.html", head(title, desc, path, jsonld, robots=robots) + body)


def index_page(script):
    s = SCRIPTS[script]
    name = s["name"]
    path = "/" + script
    title = "%s Stroke Order: All 107 Characters with Diagrams" % name
    desc = ("Stroke order diagrams for every %s character: the basic 46, dakuten, handakuten, and yoon. "
            "Numbered strokes, audio, and example words for each." % name.lower())
    sections = []
    for label, groups in [("Basic 46", ("basic",)), ("Dakuten and handakuten", ("dakuten", "handakuten")),
                          ("Yoon", ("yoon",))]:
        links = "".join('<a href="%s"><span class="kana">%s</span><span class="romaji">%s · %d</span></a>' % (
            char_url(e, script), kana(e, script), e["romaji"], stroke_count(e, script))
            for e in ENTRIES if e["group"] in groups)
        sections.append('<section class="section"><h2>%s</h2><div class="link-grid">%s</div></section>' % (label, links))
    jsonld = [breadcrumb([("Hiragana Chart", "/"), ("%s stroke order" % name, path)])]
    body = """
<body data-script="{script}">
  {header}
  <main class="wrap">
    <p class="crumb"><a href="/">Hiragana chart</a> / {name} stroke order</p>
    <p class="kicker">Free · no login</p>
    <h1>{name} stroke order</h1>
    <p class="lede">Pick a character to see its numbered strokes one by one, hear it, and learn an example word. The number after each reading is the stroke count.</p>
    <p class="no-print actions"><a class="quiz-cta" href="{chart}">Open the {name} chart</a> <a class="quiz-cta ghost" href="{quiz}">Take the {name} Quiz</a></p>
    {sections}
    <section class="section">
      <h2>General stroke order rules</h2>
      <p>Kana follow the same basic rules as kanji: write top to bottom, then left to right, and finish horizontal strokes before the vertical strokes that cross them. For dakuten, write the base character first and add the two dots last. For yoon, write the full-size character first and then the small {small} in the lower right.</p>
    </section>
  </main>
  {footer}
  <script src="/nav.js"></script>
</body>
</html>
""".format(script=script, header=HEADER, name=name, chart=s["chart"], quiz=s["quiz"],
           sections="\n    ".join(sections), small="ゃ, ゅ, or ょ" if script == "hiragana" else "ャ, ュ, or ョ",
           footer=FOOTER)
    write(script + "/index.html", head(title, desc, path, jsonld) + body)


# --------------------------------------------------------------------------
# Katakana quiz (derived from quiz/index.html)
# --------------------------------------------------------------------------
K_QUIZ_FAQ = [
    ("How does the Katakana quiz work?", "Each question shows a reading or a katakana and asks you to pick the match. Choose Romaji → Kana to practise recognition from sound, or Kana → Romaji to practise reading. Every answer plays the audio."),
    ("What do L1, L2, L3, and L4 mean in Katakana?", "L1 is the basic 46 katakana, ア to ン. L2 adds dakuten and handakuten (ガ to ポ) for 71. L3 adds yoon such as キャ and ショ for 107. L4 is the same set as L3."),
    ("Which katakana do learners miss most?", "シ and ツ, ソ and ン, and the group ク, ケ, タ. If the quiz keeps catching you on these, compare them on the <a href=\"/confusable-kana\">Confusable kana</a> page, then retest."),
    ("Can I practise Katakana words?", "Words mode uses Hiragana spellings, so stay in Characters mode for Katakana. To see Katakana in real words, open any character on the <a href=\"/katakana-chart\">Katakana chart</a>: each page shows a loanword example."),
    ("Do I need an account?", "No. Wrong answers return later in the same session, and nothing is saved to a server."),
]


def katakana_quiz():
    with open(os.path.join(ROOT, "quiz", "index.html"), encoding="utf-8") as f:
        src = f.read()

    def sub(pattern, repl, text, flags=0):
        new, count = re.subn(pattern, repl, text, count=1, flags=flags)
        if count != 1:
            raise SystemExit("katakana-quiz: pattern not found: %s" % pattern)
        return new

    t = src
    t = sub(r"<title>.*?</title>", "<title>Katakana Quiz: 46 to 107 Characters | Hiragana Chart</title>", t)
    kdesc = "Free katakana quiz: test all 46 katakana, then dakuten and yoon (107), with instant score, audio, and wrong-answer review. No login."
    t = sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % kdesc, t)
    t = sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s/katakana-quiz">' % SITE, t)
    t = sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Katakana Quiz: Test All 46 Characters | Hiragana Chart">', t)
    t = sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % kdesc, t)
    t = sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s/katakana-quiz">' % SITE, t)
    t = sub(r'<script type="application/ld\+json">.*?</script>',
            '<script type="application/ld+json">\n%s\n</script>' % json.dumps(faq_ld(K_QUIZ_FAQ), ensure_ascii=False), t, re.S)
    t = sub(r"<body>", '<body data-script="katakana">', t)
    t = sub(r'<p class="crumb">.*?</p>', '<p class="crumb"><a href="/katakana-chart">Katakana chart</a> / Katakana quiz</p>', t)
    t = sub(r'<h1 id="quiz-title">.*?</h1>', '<h1 id="quiz-title">Katakana Quiz</h1>', t)
    t = sub(r'<p class="lede" id="quiz-lede">.*?</p>', '<p class="lede" id="quiz-lede">Test the basic 46 katakana, or add dakuten and yoon for 107. Instant score, audio on every answer, and wrong answers return in the same session.</p>', t)
    t = sub(r'data-script="hiragana" aria-selected="true"', 'data-script="hiragana" aria-selected="false"', t)
    t = sub(r'data-script="katakana" aria-selected="false"', 'data-script="katakana" aria-selected="true"', t)
    faq = "\n".join('      <details><summary>%s</summary><p>%s</p></details>' % qa for qa in K_QUIZ_FAQ)
    t = sub(r'<section class="section" id="quiz-faq">.*?</section>',
            '<section class="section" id="quiz-faq">\n      <h2>Katakana quiz questions</h2>\n%s\n    </section>' % faq, t, re.S)
    write("katakana-quiz/index.html", t)


# --------------------------------------------------------------------------
# Shared nav in hand-written pages, sitemap
# --------------------------------------------------------------------------
def update_hand_written():
    for d in HAND_WRITTEN:
        p = os.path.join(ROOT, d, "index.html")
        with open(p, encoding="utf-8") as f:
            t = f.read()
        t, n = re.subn(r'<nav class="nav-links" aria-label="Site">.*?</nav>', NAV, t, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("nav block not found in %s" % p)
        t = t.replace("/quiz?script=katakana", "/katakana-quiz")
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)


def sitemap():
    urls = [("/", "weekly", "1.0"), ("/katakana-chart", "weekly", "0.9"), ("/quiz", "weekly", "0.9"),
            ("/katakana-quiz", "weekly", "0.9"), ("/kanji-translator", "weekly", "0.9"),
            ("/hiragana", "monthly", "0.8"), ("/katakana", "monthly", "0.8"),
            ("/hiragana-quiz-guide", "monthly", "0.8"), ("/confusable-kana", "monthly", "0.8"),
            ("/dakuten-yoon-guide", "monthly", "0.8"), ("/about", "monthly", "0.5"),
            ("/privacy", "yearly", "0.3")]
    for script in ("hiragana", "katakana"):
        for e in ENTRIES:
            if is_thin(e, script):
                continue  # noindex pages stay out of the sitemap
            urls.append((char_url(e, script), "monthly", "0.6" if e["group"] == "basic" else "0.5"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, freq, pr in urls:
        lines.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n"
                     "    <priority>%s</priority>\n  </url>" % (SITE, u, TODAY, freq, pr))
    lines.append("</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return [SITE + u for u, _, _ in urls]


def main():
    for script in ("hiragana", "katakana"):
        chart_page(script)
        index_page(script)
        for i, e in enumerate(ENTRIES):
            char_page(e, script, ENTRIES[i - 1] if i else None, ENTRIES[i + 1] if i + 1 < len(ENTRIES) else None)
    katakana_quiz()
    update_hand_written()
    urls = sitemap()
    print("Built %d URLs in sitemap.xml" % len(urls))


if __name__ == "__main__":
    main()
