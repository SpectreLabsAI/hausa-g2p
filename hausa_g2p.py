"""
hausa_g2p.py — Rule table APPROVED. Kano native-speaker review (Abdool,
31 Aug 2026) closed all six questions. Boko still marks neither vowel
length nor tone; segmental IPA only remains the contract.

Hausa Boko orthography -> segmental IPA.
Boko marks neither vowel length nor tone; both are phonemic. This module
deliberately outputs segmental IPA only — length and tone are learned by the
TTS model from paired audio, never guessed here.

Companion keep-list normaliser resolves the open Day 1 apostrophe item.
This exact library must be used identically in training prep, inference and
evaluation — divergence between the three is the bug you will not find later.

Open Kano decisions (blocking sign-off, not blocking code):
  - f -> [ɸ] or [f]
  - ts -> [tsʼ] or [sʼ]
  - gy/ky -> palatal stops /ɟ c/ or palatalised velars /ɡʲ kʲ/
  - r -> tap or trill for v1

Licence: Apache 2.0 — SpectreLabsAI/hausa-g2p
"""

import re
import unicodedata

# --------------------------------------------------------------------------
# Normaliser (keep-list, not strip-list)
# --------------------------------------------------------------------------

GLOTTAL = "\u02bc"  # canonical glottal modifier-letter apostrophe
# Variants seen in WAXAL audit + ASCII apostrophe (U+0027) — the eval set's
# glottal sentences 005-008 use ASCII apostrophes; without it 'Yan loses its
# glottal and becomes /jan/.
APOS_VARIANTS = "\u2019\u02bc\u2018\u0060\u00b4\u0027"
_PLACEHOLDER = "\uE000"  # private-use sentinel to protect glottalised 'y

# NBSP -> space; ZWSP/ZWNJ/ZWJ removed entirely.
_INVISIBLES = re.compile("[\u200b\u200c\u200d]")

def normalise(text: str) -> str:
    t = unicodedata.normalize("NFC", text)
    t = t.replace("\u00a0", " ")
    t = _INVISIBLES.sub("", t)
    # unify every apostrophe variant to U+02BC before any stripping
    for a in APOS_VARIANTS:
        if a != GLOTTAL:
            t = t.replace(a, GLOTTAL)
    # protect phonemic glottalised 'y: 'y / 'Y (Nigerian Boko), and 'ƴ ('Y,
    # Niger orthography with explicit apostrophe). Must run BEFORE stripping.
    t = re.sub(GLOTTAL + r"(?=[yYƴƳ])", _PLACEHOLDER, t)
    t = t.replace(GLOTTAL, "")           # remaining ones are typographic
    t = t.replace(_PLACEHOLDER, GLOTTAL)
    # typographic double quotes carry no phonemic content in Boko
    t = re.sub(r"[\u201c\u201d\u00ab\u00bb\u201e]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

# --------------------------------------------------------------------------
# Rule table — REQUIRES LINGUIST REVIEW
# --------------------------------------------------------------------------

_RULES_RAW = [
    # 1. labialised/pharyngealised ejective trigraph-equivalents
    ("ƙw", "kʷʼ"), ("ƙy", "cʼ"),
    ("ƙƴ", "ʔj"), (GLOTTAL + "ƴ", "ʔj"),  # Niger orthography with apostrophe
    # 2. digraphs
    ("sh", "ʃ"), ("ts", "tsʼ"), ("kw", "kʷ"), ("ky", "c"),
    # NOTE: no 'ch' rule. 'ch' is not Boko; it decomposes to c+h -> /tʃh/ here.
    # Corpus-specific 'ch' handling (legacy romanisation in some corpora,
    # English proper nouns like Chelsea/Okocha in WAXAL-TTS) belongs in the
    # PREP-stage text normaliser, not in this general-purpose G2P.
    ("gw", "ɡʷ"), ("gy", "ɟ"), ("fy", "fʲ"), (GLOTTAL + "y", "ʔj"),
    ("ai", "ai̯"), ("au", "au̯"),
    # 3. hooked / implosive / ejective singles
    ("ɓ", "ɓ"), ("ɗ", "ɗ"), ("ƙ", "kʼ"), ("ƴ", "ʔj"),
    # 4. plain consonants
    ("b", "b"), ("c", "tʃ"), ("d", "d"), ("f", "f"), ("g", "ɡ"),
    ("h", "h"), ("j", "dʒ"), ("k", "k"), ("l", "l"), ("m", "m"),
    ("n", "n"), ("p", "p"), ("r", "ɾ"), ("s", "s"), ("t", "t"),
    ("w", "w"), ("y", "j"), ("z", "z"),
    (GLOTTAL, "ʔ"),  # glottal stop when not part of 'y
    # 5. vowels
    ("a", "a"), ("e", "e"), ("i", "i"), ("o", "o"), ("u", "u"),
    (" ", " "),
    # punctuation passes through: sentence-final punctuation is a prosodic
    # cue for TTS (v2 §1.3.2b) — never silently dropped
    (".", "."), (",", ","), ("?", "?"), ("!", "!"), (":", ":"), (";", ";"),
]

RULES = sorted(_RULES_RAW, key=lambda r: -len(r[0]))  # longest match first

# --------------------------------------------------------------------------
# G2P
# --------------------------------------------------------------------------

def g2p(text: str, return_unknowns: bool = False):
    t = normalise(text).lower()
    out, unknowns, i = [], [], 0
    while i < len(t):
        for src, dst in RULES:
            if t.startswith(src, i):
                out.append(dst)
                i += len(src)
                break
        else:
            unknowns.append(t[i])  # log unknowns in testing; never guess
            i += 1
    ipa = "".join(out)
    return (ipa, unknowns) if return_unknowns else ipa

# --------------------------------------------------------------------------
# CLI:  python hausa_g2p.py "ƙofar ’yan ƙasa"
# --------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        ipa, unk = g2p(arg, return_unknowns=True)
        print(f"{arg!r} -> /{ipa}/" + (f"  UNKNOWN={unk}" if unk else ""))
