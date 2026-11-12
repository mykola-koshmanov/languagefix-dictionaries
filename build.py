#!/usr/bin/env python3
"""Builds LanguageFix word lists from FrequencyWords (OpenSubtitles 2018).

Source: https://github.com/hermitdave/FrequencyWords (code MIT, word lists CC BY-SA 4.0),
pinned to one commit so the output is reproducible. The output lists are derived works and are
distributed under CC BY-SA 4.0 (see dictionaries/NOTICE.md).

usage: python3 -I build.py <download dir> <output dir>
Prints the Swift manifest entries (sha256, size, word count) for DictionaryCatalog.swift.
"""
import hashlib, os, sys, unicodedata, urllib.request

COMMIT = "525f9b560de45753a5ea01069454e72e9aa541c6"
URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/" + COMMIT + "/content/2018/{src}/{src}_50k.txt"

# app language -> (FrequencyWords folder, script of the macOS layout)
LANGS = {
    "pl": ("pl", "LATIN"), "cs": ("cs", "LATIN"), "sk": ("sk", "LATIN"), "hu": ("hu", "LATIN"),
    "ro": ("ro", "LATIN"), "lt": ("lt", "LATIN"), "lv": ("lv", "LATIN"), "et": ("et", "LATIN"),
    "nb": ("no", "LATIN"), "sl": ("sl", "LATIN"), "hr": ("hr", "LATIN"), "sq": ("sq", "LATIN"),
    "mk": ("mk", "CYRILLIC"), "sr": ("sr", "CYRILLIC"),
}

# Serbian subtitles are mostly in Latin script; the Serbian layout is Cyrillic. Standard 1:1 mapping.
SR_DIGRAPHS = [("dž", "џ"), ("lj", "љ"), ("nj", "њ")]
SR_LETTERS = dict(zip("abcčćdđefghijklmnoprsštuvzž", "абцчћдђефгхијклмнопрсштувзж"))


def to_serbian_cyrillic(w):
    if any(c in w for c in "qwxy"):
        return None  # foreign word
    for a, b in SR_DIGRAPHS:
        w = w.replace(a, b)
    return "".join(SR_LETTERS.get(c, c) for c in w)


def script_ok(word, script):
    return all(c.isalpha() and unicodedata.name(c, "").startswith(script) for c in word)


def build(lang, src, script, raw):
    words = set()
    for line in raw.splitlines():
        w = unicodedata.normalize("NFC", line.split(" ")[0].strip().lower())
        if lang == "ro":  # subtitles often use cedilla letters; the Romanian layout types comma-below
            w = w.replace("ş", "ș").replace("ţ", "ț")
        if lang == "sr" and w and script_ok(w, "LATIN"):
            w = to_serbian_cyrillic(w) or ""
        if len(w) >= 2 and script_ok(w, script):
            words.add(w)
    return sorted(words)


def main(dl, out):
    os.makedirs(dl, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    for lang, (src, script) in LANGS.items():
        path = os.path.join(dl, src + "_50k.txt")
        if not os.path.exists(path):
            urllib.request.urlretrieve(URL.format(src=src), path)
        raw = open(path, encoding="utf-8", errors="strict").read()
        words = build(lang, src, script, raw)
        data = ("\n".join(words) + "\n").encode("utf-8")
        with open(os.path.join(out, lang + ".txt"), "wb") as f:
            f.write(data)
        print('        "%s": .init(sha256: "%s", size: %d, words: %d),'
              % (lang, hashlib.sha256(data).hexdigest(), len(data), len(words)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
