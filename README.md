# hausa-g2p

**Rule-based Hausa Boko → segmental IPA. No ML, no dependencies — a pure Python rule table and a keep-list text normaliser.**

> ## ✅ Reviewed and approved by a Kano native speaker — 31 August 2026
>
> Every rule in the table below was checked against recorded Kano Hausa by a
> native-speaking reviewer, and the six open linguistic questions (f/p pair,
> ts, gy/ky/ƙy, r, glottal identity, residuals) were all closed. This is not
> a weekend script: the review protocol, the questions asked, and the
> sign-off are in [`LINGUIST_REVIEW.md`](LINGUIST_REVIEW.md).

## Scope boundary — read this first

**Output is segmental IPA only.** Hausa Boko orthography marks neither vowel
length nor tone, and both are phonemic. No rule set can recover from
orthography what orthography does not encode. This module deliberately does
not guess: **TTS models learn suprasegmentals from paired audio, exactly as
a literate Hausa speaker infers them from lexical knowledge when reading
aloud.** A pronunciation lexicon marking length/tone is the obvious v2.

## Install & usage

```bash
pip install hausa-g2p   # or: copy hausa_g2p.py into your project
```

```python
from hausa_g2p import g2p, normalise

g2p("Ƙofar ƙauye")             # -> "kʼofaɾ kʼau̯je"
g2p(text, return_unknowns=True)  # -> (ipa, [unmapped chars])
normalise(text)                  # keep-list normaliser (apostrophes, quotes, invisibles)
```

CLI: `python hausa_g2p.py "ƙofar ’yan ƙasa"`

## The rule table

Longest-match-first tokenisation (ƙw/ƙy before ƙ+w, digraphs before singles).

| Class | Mapping |
|---|---|
| Ejectives | `ts → tsʼ`, `ƙ → kʼ`, `ƙw → kʷʼ`, `ƙy → cʼ` |
| Implosives | `ɓ → ɓ`, `ɗ → ɗ` |
| Labialised / palatalised | `kw → kʷ`, `gw → ɡʷ`, `ky → c`, `gy → ɟ`, `fy → fʲ` |
| Plain consonants | `b c→tʃ d f g h j→dʒ k l m n p r→ɾ s sh→ʃ t w y→j z` |
| Glottal | `'y → ʔj`, `ƴ → ʔj` (Niger orthography, same phoneme), bare `' → ʔ` |
| Vowels | `a e i o u`, diphthongs `ai → ai̯`, `au → au̯` |
| Punctuation | `. , ? ! : ;` pass through (prosodic cues for TTS) |

**Normaliser:** five apostrophe variants (U+2019 U+02BC U+2018 `` ` `` ´ **and
ASCII U+0027**) unify to U+02BC; glottalised `'y`/`'ƴ` protected *before*
stripping; typographic quotes stripped; NBSP → space; ZWSP/ZWNJ removed.
Without the ASCII-apostrophe rule, `'Yan` silently becomes /jan/ — a phoneme
destroyed invisibly.

## Approved vs original draft — changelog

| Rule | Draft (from published phonology) | Approved (Kano review) |
|---|---|---|
| `f` | [ɸ] | **[f]** — labiodental, no vowel conditioning |
| `p` | /p/, independent question | **/p/**, closed as a pair with f — Hausa's native inventory lacks /p/, but Kano keeps written p distinct from f |
| `ts` | [tsʼ] *or* [sʼ] | **[tsʼ]** — ejective |
| `gy`/`ky`/`ƙy` | palatal stops *or* palatalised velars | **palatal stops** /ɟ c cʼ/ — single front contact, not ɡ+j |
| `r` | [r] or [ɾ] | **[ɾ]** — single tap everywhere |

Plus one corpus finding fixed during validation: `p` was missing from the
original spec table entirely (loanwords like *pace* silently lost their
onset).

## Known limits

- **No vowel length, no tone** — by design (see scope boundary)
- **`x` in loanwords** (*exam*) is logged as unknown, never guessed
- **Code-switched English is not handled** — `ts` fires inside *WhatsApp*,
  `ch` decomposes to /tʃh/ in *teacher*. English content in the canonical
  WAXAL Hausa TTS corpus is <1% of rows, so this is an inference-time
  problem (word-level language ID routing, or a Hausa-isation lexicon)
  deferred until the product needs it
- **`rr` (lengthened r) is expressive intensification, not lexical** — same
  out-of-scope category as length/tone. Hausa-specific finding; it does
  **not** transfer to Yoruba or Igbo
- **Single `r`** for both rhotics (tap/trill not distinguished in writing)

## The companion keep-list normaliser

`normalise()` is included in the same module and must be used **identically
in training prep, inference and evaluation** — divergence between those
three is the bug you will not find later.

## Examples

[`examples/waxal_prep/`](examples/waxal_prep/) is a **worked example of
applying this G2P to one corpus (WAXAL Hausa TTS)** — it is *not* part of
the G2P contract. It shows the `ch` guard: alias legacy `ch→c` on Hausa
tokens while protecting English proper nouns (*Okocha*, *Chelsea*,
*Tuchel*), which standard Boko has no `ch` for.

## Validation

- `test_hausa_g2p.py` — 35 checks (rule coverage, apostrophe variants,
  glottal identity, punctuation pass-through, unknown logging)
- `test_waxal_prep.py` — 18 checks (alias behaviour, blocklist, exclusion mode)
- 30-sentence evaluation set with recordings: 29/30 fully mapped; the only
  unknown is `x` in code-switched "exam"
- `ipa_dump.txt` — the eval set's approved IPA output, for review against audio

## Contributing

The rule table is data, not code — corrections from native speakers are the
most valuable contributions. Open an issue with the word, the pronunciation
you hear, and (if possible) a recording. Changes to the table require
native-speaker review; that bar is what makes this artifact trustworthy.

## Licence

Apache-2.0. Part of the Turaco project by Spectre Labs.
