"""
waxal_prep.py — training-prep text normaliser for WAXAL Hausa.

Scope ruling (31 Aug): corpus-specific handling lives HERE, not in
hausa_g2p.py, which stays a general-purpose, corpus-free utility.

Covers the 'ch' question verified against canonical google/WaxalNLP
data/TTS/hau (1,572 train rows):
  - 96/1,971 rows contain 'ch', and they are ENGLISH proper nouns and loans
    (Okocha, Chelsea, Thomas Tuchel, Clive Myrie, blue) — standard Boko has
    no 'ch'; 'c' alone is /tʃ/.
  - A blanket alias ch->c would corrupt those names ('Okoca' is wrong).
  - Rule: alias ch->c ONLY on tokens judged Hausa; blocklisted English
    tokens pass through untouched. Callers who prefer zero risk can use
    row-exclusion mode instead and let G2P decompose ch to /tʃh/ on the
    excluded rows — or drop those rows (4.9% of the corpus).

If legacy ch-orthography corpora are ever mixed in (the mislabeled
suleiman2003 mirror, 33.7% ch = chi/cikin/che), the same alias applies:
there ch->c is always correct because such text has no English names.

NOTE: this module does NOT handle vowel length, tone, or the broader
legacy-orthography conversions (sey->sai, jaiki->aiki) — those are a
separate prep workstream pending the linguist sign-off.
"""

import re

# Tokens where 'ch' is English /tʃ/ or part of a name — never aliased.
# Seed list from the verified canonical TTS 'ch' rows; extend as the full
# 333-clip segmentation run surfaces more.
ENGLISH_CH = frozenset({
    "okocha", "chelsea", "tuchel", "myrie", "clive",
    # common English loans that may appear with 'ch'
    "chairman", "change", "check", "chief", "child", "china", "chip",
    "chocolate", "choose", "church",
})

_TOKEN_RE = re.compile(r"[A-Za-z\u0181\u0198\u018A\u01B3\u0253\u0199"
                       r"\u0257\u01B4']+")

def _tokens(text):
    return _TOKEN_RE.findall(text)

def alias_legacy_ch(text: str, blocklist=ENGLISH_CH):
    """Alias ch->c on Hausa tokens, leave blocklisted English tokens alone.

    Case-preserving. Returns (new_text, n_aliased, n_protected).
    """
    out, n_alias, n_prot = [], 0, 0
    last = 0
    for m in _TOKEN_RE.finditer(text):
        tok = m.group(0)
        low = tok.lower()
        if "ch" not in low:
            continue
        if low in blocklist:
            n_prot += 1
            continue
        # ch -> c (ONE char), mirroring the case of the matched pair
        def _alias(mm):
            src = mm.group(0)
            return src[0] if src[0].isupper() else "c"
        repl = re.sub("ch", _alias, tok, flags=re.IGNORECASE)
        out.append(text[last:m.start()])
        out.append(repl)
        last = m.end()
        n_alias += 1
    out.append(text[last:])
    return "".join(out), n_alias, n_prot

def row_has_english_ch(text: str, blocklist=ENGLISH_CH) -> bool:
    """Row-exclusion mode: True if this row must NOT be aliased."""
    return any(t.lower() in blocklist for t in _tokens(text))

def prep_text(text: str, mode: str = "token", blocklist=ENGLISH_CH):
    """Main entry. mode='token' (alias around English names, default) or
    mode='exclude' (return None for rows containing English ch-names)."""
    if mode == "exclude":
        if row_has_english_ch(text, blocklist):
            return None
        aliased, _, _ = alias_legacy_ch(text, blocklist=frozenset())
        return aliased
    aliased, _, _ = alias_legacy_ch(text, blocklist)
    return aliased

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(prep_text(arg))
