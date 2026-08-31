# waxal_prep — worked example: applying hausa-g2p to one corpus

**This is an example, not part of the G2P contract.** It shows how to use
[`hausa_g2p`](../../README.md) with a specific corpus (WAXAL Hausa TTS,
`google/WaxalNLP data/TTS/hau`) and the corpus-specific cleanup that entails.

## What it does

Standard Boko has no `ch` — bare `c` is /tʃ/. But WAXAL's Hausa transcripts
contain `ch` in two flavours:

1. **English proper nouns and loans** — *Okocha, Chelsea, Thomas Tuchel,
   Clive Myrie* (4.9% of rows). Aliasing these to `c` produces *Okoca* — wrong.
2. **Legacy romanisation** (in third-party WAXAL-derived corpora, up to a
   third of rows) — *chi*=ci "eat", *chikin*=cikin, *che*=ce. Here `ch→c`
   is always correct.

The guard: **alias `ch→c` only on Hausa tokens** (blocklist for English
names), with a row-exclusion mode if you prefer zero risk. Everything else
is the G2P's job, not this module's.

## Usage

```python
from waxal_prep import prep_text

prep_text("chikin gida")                    # -> "cikin gida"
prep_text("Okocha ya ziyarci Chelsea")      # -> unchanged (names protected)
prep_text(text, mode="exclude")             # -> None if row has English ch-names
```

## Lesson this example encodes

**Verify the corpus before citing statistics about it.** A third-party
mirror named `waxalnlp-hau-tts-final` turned out to be 31,925 rows of
legacy-orthography text that is *not* WAXAL's Hausa TTS split (1,572 rows,
canonical `google/WaxalNLP`). The 33.7% "legacy ch" figure came from that
mirror; the real training data needed the guard for a completely different
reason — English names. Same class of error as reading a README instead of
a LICENSE: check the source repo, not the convenient name.

## Tests

`test_waxal_prep.py` — 18 checks. Run: `python test_waxal_prep.py`
