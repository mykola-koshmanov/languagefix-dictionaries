# LanguageFix word lists

Files: `pl cs sk hu ro lt lv et nb sl hr sq mk sr` (`<code>.txt`, UTF-8, one lower-case word per line).

**Source:** FrequencyWords by Hermit Dave — https://github.com/hermitdave/FrequencyWords
(commit `525f9b560de45753a5ea01069454e72e9aa541c6`, lists `content/2018/<lang>/<lang>_50k.txt`),
built from the OpenSubtitles 2018 corpus (http://opus.nlpl.eu/OpenSubtitles2018.php).

**License:** the original lists are licensed under Creative Commons Attribution-ShareAlike 4.0
(https://creativecommons.org/licenses/by-sa/4.0/). These files are adapted works and are
distributed under the same license, CC BY-SA 4.0.

**Changes made** (by `scripts/dictionaries/build.py`): frequency counts removed; words lower-cased and
NFC-normalised; only words of two or more letters in the script of the macOS keyboard layout kept;
Romanian ş/ţ replaced with ș/ț; Serbian Latin converted to Cyrillic with the standard letter mapping
(words with q, w, x, y dropped); for Norwegian the `no` list is used as `nb`.

The LanguageFix application code is a separate work and is not covered by this license.
