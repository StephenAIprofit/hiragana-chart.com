"""Kana data used by build_site.py.

Each entry: hiragana, katakana, display romaji, URL slug, audio file name.
Slugs are unique: ぢ/づ use di/du so they do not collide with じ/ず.
"""

BASIC = [
    ("あ", "ア", "a"), ("い", "イ", "i"), ("う", "ウ", "u"), ("え", "エ", "e"), ("お", "オ", "o"),
    ("か", "カ", "ka"), ("き", "キ", "ki"), ("く", "ク", "ku"), ("け", "ケ", "ke"), ("こ", "コ", "ko"),
    ("さ", "サ", "sa"), ("し", "シ", "shi"), ("す", "ス", "su"), ("せ", "セ", "se"), ("そ", "ソ", "so"),
    ("た", "タ", "ta"), ("ち", "チ", "chi"), ("つ", "ツ", "tsu"), ("て", "テ", "te"), ("と", "ト", "to"),
    ("な", "ナ", "na"), ("に", "ニ", "ni"), ("ぬ", "ヌ", "nu"), ("ね", "ネ", "ne"), ("の", "ノ", "no"),
    ("は", "ハ", "ha"), ("ひ", "ヒ", "hi"), ("ふ", "フ", "fu"), ("へ", "ヘ", "he"), ("ほ", "ホ", "ho"),
    ("ま", "マ", "ma"), ("み", "ミ", "mi"), ("む", "ム", "mu"), ("め", "メ", "me"), ("も", "モ", "mo"),
    ("や", "ヤ", "ya"), ("ゆ", "ユ", "yu"), ("よ", "ヨ", "yo"),
    ("ら", "ラ", "ra"), ("り", "リ", "ri"), ("る", "ル", "ru"), ("れ", "レ", "re"), ("ろ", "ロ", "ro"),
    ("わ", "ワ", "wa"), ("を", "ヲ", "wo"), ("ん", "ン", "n"),
]

# hiragana, katakana, romaji, slug, base hiragana, mark ("dakuten" | "handakuten")
DAKUTEN = [
    ("が", "ガ", "ga", "ga", "か", "dakuten"), ("ぎ", "ギ", "gi", "gi", "き", "dakuten"),
    ("ぐ", "グ", "gu", "gu", "く", "dakuten"), ("げ", "ゲ", "ge", "ge", "け", "dakuten"),
    ("ご", "ゴ", "go", "go", "こ", "dakuten"),
    ("ざ", "ザ", "za", "za", "さ", "dakuten"), ("じ", "ジ", "ji", "ji", "し", "dakuten"),
    ("ず", "ズ", "zu", "zu", "す", "dakuten"), ("ぜ", "ゼ", "ze", "ze", "せ", "dakuten"),
    ("ぞ", "ゾ", "zo", "zo", "そ", "dakuten"),
    ("だ", "ダ", "da", "da", "た", "dakuten"), ("ぢ", "ヂ", "ji", "di", "ち", "dakuten"),
    ("づ", "ヅ", "zu", "du", "つ", "dakuten"), ("で", "デ", "de", "de", "て", "dakuten"),
    ("ど", "ド", "do", "do", "と", "dakuten"),
    ("ば", "バ", "ba", "ba", "は", "dakuten"), ("び", "ビ", "bi", "bi", "ひ", "dakuten"),
    ("ぶ", "ブ", "bu", "bu", "ふ", "dakuten"), ("べ", "ベ", "be", "be", "へ", "dakuten"),
    ("ぼ", "ボ", "bo", "bo", "ほ", "dakuten"),
    ("ぱ", "パ", "pa", "pa", "は", "handakuten"), ("ぴ", "ピ", "pi", "pi", "ひ", "handakuten"),
    ("ぷ", "プ", "pu", "pu", "ふ", "handakuten"), ("ぺ", "ペ", "pe", "pe", "へ", "handakuten"),
    ("ぽ", "ポ", "po", "po", "ほ", "handakuten"),
]

# hiragana, katakana, romaji, slug, base hiragana, small hiragana
YOON = []
for base, kbase, stem, slugstem in [
    ("き", "キ", "ky", "ky"), ("し", "シ", "sh", "sh"), ("ち", "チ", "ch", "ch"),
    ("に", "ニ", "ny", "ny"), ("ひ", "ヒ", "hy", "hy"), ("み", "ミ", "my", "my"),
    ("り", "リ", "ry", "ry"), ("ぎ", "ギ", "gy", "gy"), ("じ", "ジ", "j", "j"),
    ("ぢ", "ヂ", "j", "dy"), ("び", "ビ", "by", "by"), ("ぴ", "ピ", "py", "py"),
]:
    for small, ksmall, v in [("ゃ", "ャ", "a"), ("ゅ", "ュ", "u"), ("ょ", "ョ", "o")]:
        YOON.append((base + small, kbase + ksmall, stem + v, slugstem + v, base, small))

SMALL_K = {"ゃ": "ャ", "ゅ": "ュ", "ょ": "ョ"}
H2K = {h: k for h, k, _ in BASIC}
H2K.update({d[0]: d[1] for d in DAKUTEN})

ROWS = [
    ("a", "vowel", ["a", "i", "u", "e", "o"]),
    ("ka", "k", ["ka", "ki", "ku", "ke", "ko"]),
    ("sa", "s", ["sa", "shi", "su", "se", "so"]),
    ("ta", "t", ["ta", "chi", "tsu", "te", "to"]),
    ("na", "n", ["na", "ni", "nu", "ne", "no"]),
    ("ha", "h", ["ha", "hi", "fu", "he", "ho"]),
    ("ma", "m", ["ma", "mi", "mu", "me", "mo"]),
    ("ya", "y", ["ya", "", "yu", "", "yo"]),
    ("ra", "r", ["ra", "ri", "ru", "re", "ro"]),
    ("wa", "w", ["wa", "", "", "", "wo"]),
    ("n", "n", ["n", "", "", "", ""]),
]

# Pronunciation notes keyed by slug. Missing slugs get a generated sentence.
NOTES = {
    "a": "A short, open a, like the a in father but clipped. Japanese vowels are pure: no glide at the end.",
    "i": "A short ee, as in see, but clipped. Keep the lips relaxed.",
    "u": "An unrounded u: say oo with relaxed, not pushed-out, lips. After k and s it often goes quiet, as in です (desu, sounds like dess).",
    "e": "Like the e in pet. It never glides into ay.",
    "o": "Like the o in more, short and without a w at the end.",
    "shi": "Hepburn writes shi, not si. The sound is close to English she, said quickly.",
    "chi": "Hepburn writes chi, not ti. Close to the chee in cheese, short.",
    "tsu": "Hepburn writes tsu, not tu. Start with ts, like the end of cats, then a light u.",
    "fu": "Not an English f. Blow air gently between both lips, as if cooling soup. It sits between h and f.",
    "hi": "A breathy h, close to the h in huge.",
    "ha": "Read ha in words, but as the topic particle は it is read wa: わたしは (watashi wa).",
    "he": "Read he in words, but as the direction particle へ it is read e: にほんへ (nihon e).",
    "wo": "Written wo, but read o in modern Japanese. It is almost only used as the object particle: ほんをよむ (hon o yomu).",
    "n": "The only kana that is just a consonant. It takes one full beat: にほん is three beats, ni-ho-n. Before p, b, and m it sounds like m.",
    "ji": "In modern Japanese じ and ぢ sound the same. じ is the normal spelling; ぢ appears mainly in compounds such as はなぢ.",
    "di": "Read ji, the same sound as じ. It appears mainly in compounds where ち becomes voiced, such as はな + ち = はなぢ. When typing, use di.",
    "zu": "In modern Japanese ず and づ sound the same. ず is the normal spelling; づ appears in words like つづく.",
    "du": "Read zu, the same sound as ず. It appears where つ becomes voiced, such as つづく (tsuzuku). When typing, use du.",
    "ra": "Japanese r is a quick tap of the tongue tip behind the teeth, between English r, l, and d.",
    "ri": "Japanese r is a quick tap of the tongue tip behind the teeth, between English r, l, and d.",
    "ru": "Japanese r is a quick tap of the tongue tip behind the teeth, between English r, l, and d.",
    "re": "Japanese r is a quick tap of the tongue tip behind the teeth, between English r, l, and d.",
    "ro": "Japanese r is a quick tap of the tongue tip behind the teeth, between English r, l, and d.",
    "dya": "Read ja, the same as じゃ. This spelling is rare in modern Japanese.",
    "dyu": "Read ju, the same as じゅ. This spelling is rare in modern Japanese.",
    "dyo": "Read jo, the same as じょ. This spelling is rare in modern Japanese.",
}

# Example words: slug -> (word, romaji, English). Hiragana words are native
# words; katakana words are loanwords. None means no common example.
H_WORDS = {
    "a": ("あめ", "ame", "rain"), "i": ("いぬ", "inu", "dog"), "u": ("うみ", "umi", "sea"),
    "e": ("えき", "eki", "station"), "o": ("おちゃ", "ocha", "tea"),
    "ka": ("かさ", "kasa", "umbrella"), "ki": ("きって", "kitte", "stamp"), "ku": ("くるま", "kuruma", "car"),
    "ke": ("けむり", "kemuri", "smoke"), "ko": ("こども", "kodomo", "child"),
    "sa": ("さかな", "sakana", "fish"), "shi": ("しお", "shio", "salt"), "su": ("すし", "sushi", "sushi"),
    "se": ("せんせい", "sensei", "teacher"), "so": ("そら", "sora", "sky"),
    "ta": ("たまご", "tamago", "egg"), "chi": ("ちず", "chizu", "map"), "tsu": ("つき", "tsuki", "moon"),
    "te": ("てがみ", "tegami", "letter"), "to": ("とり", "tori", "bird"),
    "na": ("なつ", "natsu", "summer"), "ni": ("にく", "niku", "meat"), "nu": ("ぬの", "nuno", "cloth"),
    "ne": ("ねこ", "neko", "cat"), "no": ("のり", "nori", "seaweed"),
    "ha": ("はな", "hana", "flower"), "hi": ("ひと", "hito", "person"), "fu": ("ふね", "fune", "boat"),
    "he": ("へや", "heya", "room"), "ho": ("ほし", "hoshi", "star"),
    "ma": ("まど", "mado", "window"), "mi": ("みみ", "mimi", "ear"), "mu": ("むし", "mushi", "insect"),
    "me": ("めがね", "megane", "glasses"), "mo": ("もり", "mori", "forest"),
    "ya": ("やま", "yama", "mountain"), "yu": ("ゆき", "yuki", "snow"), "yo": ("よる", "yoru", "night"),
    "ra": ("らいねん", "rainen", "next year"), "ri": ("りんご", "ringo", "apple"), "ru": ("るす", "rusu", "not at home"),
    "re": ("れきし", "rekishi", "history"), "ro": ("ろうそく", "rousoku", "candle"),
    "wa": ("わたし", "watashi", "I, me"), "wo": ("ほんをよむ", "hon o yomu", "to read a book"),
    "n": ("ほん", "hon", "book"),
    "ga": ("がっこう", "gakkou", "school"), "gi": ("ぎんこう", "ginkou", "bank"), "gu": ("ぐあい", "guai", "condition"),
    "ge": ("げんき", "genki", "healthy, well"), "go": ("ごはん", "gohan", "rice, meal"),
    "za": ("ざっし", "zasshi", "magazine"), "ji": ("じかん", "jikan", "time"), "zu": ("ずっと", "zutto", "all along"),
    "ze": ("ぜんぶ", "zenbu", "all"), "zo": ("ぞう", "zou", "elephant"),
    "da": ("だいがく", "daigaku", "university"), "di": ("はなぢ", "hanaji", "nosebleed"), "du": ("つづく", "tsuzuku", "to continue"),
    "de": ("でんわ", "denwa", "telephone"), "do": ("どこ", "doko", "where"),
    "ba": ("ばんごはん", "bangohan", "dinner"), "bi": ("へび", "hebi", "snake"), "bu": ("ぶた", "buta", "pig"),
    "be": ("べんきょう", "benkyou", "study"), "bo": ("ぼうし", "boushi", "hat"),
    "pa": ("かんぱい", "kanpai", "cheers"), "pi": ("えんぴつ", "enpitsu", "pencil"), "pu": ("てんぷら", "tenpura", "tempura"),
    "pe": ("ぺらぺら", "perapera", "fluent"), "po": ("さんぽ", "sanpo", "a walk"),
    "kya": ("きゃく", "kyaku", "guest"), "kyu": ("きゅうり", "kyuuri", "cucumber"), "kyo": ("きょう", "kyou", "today"),
    "sha": ("しゃしん", "shashin", "photo"), "shu": ("しゅくだい", "shukudai", "homework"), "sho": ("しょくじ", "shokuji", "meal"),
    "cha": ("おちゃ", "ocha", "tea"), "chu": ("ちゅうい", "chuui", "caution"), "cho": ("ちょっと", "chotto", "a little"),
    "nya": ("こんにゃく", "konnyaku", "konjac"), "nyu": ("にゅういん", "nyuuin", "hospital stay"), "nyo": None,
    "hya": ("ひゃく", "hyaku", "hundred"), "hyu": None, "hyo": ("ひょうし", "hyoushi", "book cover"),
    "mya": ("みゃく", "myaku", "pulse"), "myu": None, "myo": ("みょうじ", "myouji", "family name"),
    "rya": ("りゃく", "ryaku", "abbreviation"), "ryu": ("りゅう", "ryuu", "dragon"), "ryo": ("りょこう", "ryokou", "travel"),
    "gya": ("ぎゃく", "gyaku", "reverse"), "gyu": ("ぎゅうにゅう", "gyuunyuu", "milk"), "gyo": ("きんぎょ", "kingyo", "goldfish"),
    "ja": ("じゃま", "jama", "in the way"), "ju": ("じゅぎょう", "jugyou", "class, lesson"), "jo": ("じょうず", "jouzu", "skilful"),
    "dya": None, "dyu": None, "dyo": None,
    "bya": ("さんびゃく", "sanbyaku", "three hundred"), "byu": None, "byo": ("びょういん", "byouin", "hospital"),
    "pya": ("はっぴゃく", "happyaku", "eight hundred"), "pyu": None, "pyo": ("ぴょんぴょん", "pyonpyon", "hopping"),
}

K_WORDS = {
    "a": ("アイス", "aisu", "ice cream"), "i": ("インク", "inku", "ink"), "u": ("ウイルス", "uirusu", "virus"),
    "e": ("エアコン", "eakon", "air conditioner"), "o": ("オレンジ", "orenji", "orange"),
    "ka": ("カメラ", "kamera", "camera"), "ki": ("キロ", "kiro", "kilo"), "ku": ("クラス", "kurasu", "class"),
    "ke": ("ケーキ", "keeki", "cake"), "ko": ("コーヒー", "koohii", "coffee"),
    "sa": ("サラダ", "sarada", "salad"), "shi": ("シーツ", "shiitsu", "bed sheet"), "su": ("スープ", "suupu", "soup"),
    "se": ("セーター", "seetaa", "sweater"), "so": ("ソファ", "sofa", "sofa"),
    "ta": ("タクシー", "takushii", "taxi"), "chi": ("チーズ", "chiizu", "cheese"), "tsu": ("ツアー", "tsuaa", "tour"),
    "te": ("テレビ", "terebi", "television"), "to": ("トマト", "tomato", "tomato"),
    "na": ("ナイフ", "naifu", "knife"), "ni": ("テニス", "tenisu", "tennis"), "nu": ("カヌー", "kanuu", "canoe"),
    "ne": ("ネクタイ", "nekutai", "necktie"), "no": ("ノート", "nooto", "notebook"),
    "ha": ("ハンバーガー", "hanbaagaa", "hamburger"), "hi": ("ヒーター", "hiitaa", "heater"), "fu": ("フランス", "furansu", "France"),
    "he": ("ヘリコプター", "herikoputaa", "helicopter"), "ho": ("ホテル", "hoteru", "hotel"),
    "ma": ("マスク", "masuku", "mask"), "mi": ("ミルク", "miruku", "milk"), "mu": ("ゲーム", "geemu", "game"),
    "me": ("メール", "meeru", "email"), "mo": ("メモ", "memo", "memo"),
    "ya": ("タイヤ", "taiya", "tyre"), "yu": ("ユーモア", "yuumoa", "humour"), "yo": ("ヨーグルト", "yooguruto", "yogurt"),
    "ra": ("ラジオ", "rajio", "radio"), "ri": ("リボン", "ribon", "ribbon"), "ru": ("ルール", "ruuru", "rule"),
    "re": ("レモン", "remon", "lemon"), "ro": ("ロボット", "robotto", "robot"),
    "wa": ("ワイン", "wain", "wine"), "wo": None, "n": ("パン", "pan", "bread"),
    "ga": ("ガム", "gamu", "chewing gum"), "gi": ("ギター", "gitaa", "guitar"), "gu": ("グラス", "gurasu", "glass"),
    "ge": ("ゲーム", "geemu", "game"), "go": ("ゴルフ", "gorufu", "golf"),
    "za": ("デザイン", "dezain", "design"), "ji": ("ジーンズ", "jiinzu", "jeans"), "zu": ("チーズ", "chiizu", "cheese"),
    "ze": ("ゼロ", "zero", "zero"), "zo": ("ゾーン", "zoon", "zone"),
    "da": ("ダンス", "dansu", "dance"), "di": None, "du": None,
    "de": ("デパート", "depaato", "department store"), "do": ("ドア", "doa", "door"),
    "ba": ("バス", "basu", "bus"), "bi": ("ビール", "biiru", "beer"), "bu": ("ブーツ", "buutsu", "boots"),
    "be": ("ベッド", "beddo", "bed"), "bo": ("ボール", "booru", "ball"),
    "pa": ("パン", "pan", "bread"), "pi": ("ピアノ", "piano", "piano"), "pu": ("プール", "puuru", "swimming pool"),
    "pe": ("ペン", "pen", "pen"), "po": ("ポスト", "posuto", "postbox"),
    "kya": ("キャンプ", "kyanpu", "camping"), "kyu": ("バーベキュー", "baabekyuu", "barbecue"), "kyo": None,
    "sha": ("シャツ", "shatsu", "shirt"), "shu": ("シューズ", "shuuzu", "shoes"), "sho": ("ショップ", "shoppu", "shop"),
    "cha": ("チャンス", "chansu", "chance"), "chu": ("チューリップ", "chuurippu", "tulip"), "cho": ("チョコレート", "chokoreeto", "chocolate"),
    "nya": None, "nyu": ("ニュース", "nyuusu", "news"), "nyo": None,
    "hya": None, "hyu": ("ヒューズ", "hyuuzu", "fuse"), "hyo": None,
    "mya": ("ミャンマー", "myanmaa", "Myanmar"), "myu": ("ミュージック", "myuujikku", "music"), "myo": None,
    "rya": None, "ryu": ("リュック", "ryukku", "backpack"), "ryo": None,
    "gya": ("ギャラリー", "gyararii", "gallery"), "gyu": None, "gyo": None,
    "ja": ("ジャム", "jamu", "jam"), "ju": ("ジュース", "juusu", "juice"), "jo": ("ジョギング", "jogingu", "jogging"),
    "dya": None, "dyu": None, "dyo": None,
    "bya": None, "byu": ("ビュッフェ", "byuffe", "buffet"), "byo": None,
    "pya": None, "pyu": ("コンピューター", "konpyuutaa", "computer"), "pyo": None,
}

# Look-alike groups, matching /confusable-kana.
CONFUSABLE = [
    ["ね", "れ", "わ"], ["さ", "ち", "き"], ["ぬ", "め"], ["る", "ろ"], ["あ", "お"],
    ["シ", "ツ"], ["ソ", "ン"], ["ク", "ケ", "タ"], ["コ", "ユ"],
]
