# Hausa G2P — Linguist Review Packet
**For:** Kano Hausa-speaking linguist review · **Sprint:** Turaco Day 3+ · **Status:** ✅ **SIGNED OFF** — Abdool (Kano native speaker), 31 Aug 2026. All six questions closed.

Shukran — this review gates every Hausa TTS model we train. An error here
propagates silently into all of them. The questions are numbered; please
answer each with your ruling and, where asked, an example word.

---

## How to review

1. Listen to the 30 eval recordings (`turaco-hausa-eval`, WAVs 001–030) with
   the IPA output for each sentence (`ipa_dump.txt`) side by side.
2. Answer Q1–Q6 below. Each maps to one line (or pair of lines) in the rule
   table — your ruling is a one-line code change, so be specific.
3. Flag anything else that sounds wrong in the IPA. Silent errors are the danger.

---

## Q1 — `f` and `p` (a PAIR, not two questions)

Hausa's native inventory has no /p/; loans often adapt to /f/ (*fasinja*,
*fensir*). Written `p` may be realised [p] or [ɸ] depending on the word.

- Current draft: `f → ɸ` everywhere; `p → p`.
- **Ruling needed:** Kano realisation of written `f`: [f], [ɸ], or
  [ɸ] before rounded vowels / [f] elsewhere?
- **Ruling needed:** written `p` in loans (*pile*, *Polis*): [p] or [ɸ]?
  (If [ɸ], `p → ɸ` follows automatically from the `f` answer.)

Eval sentences touching this: any word with f (001, 002, 003, 015–017…).

## Q2 — `ts`

- Current draft: `ts → tsʼ` (alveolar ejective affricate).
- **Ruling needed:** [tsʼ] or [sʼ] in Kano?

Eval: *tsawo* (001), *tsakar* (chosen clips), *tsuntsu*.

## Q3 — `gy` / `ky` / `ƙy` (one convention, three letters)

- Current draft: palatal stops — `gy → ɟ`, `ky → c`, `ƙy → cʼ`.
- Alternative: palatalised velars — /ɡʲ/, /kʲ/, /kʲʼ/.
- **Ruling needed:** which convention? (Both describe the same sounds;
  we need ONE, used consistently by the G2P and the espeak-ng port.)

Eval: *ƙyau*-type words; *gyara*-type words.

## Q4 — `r`

Hausa has two rhotics (tap /ɾ/ and trill/retroflex /r/), not distinguished
in writing. Same class of loss as length and tone.

- Current draft: single `r → r`.
- **Ruling needed:** tap or trill for v1? (v2 lexicon may distinguish.)

## Q5 — Glottalised `'y` / `ƴ` (identity check, not a decision)

Sentences 005–008 (`'Yan`, `'Ya'yan`, `'Ƴa'ƴa`, `'Yan kasuwa`) must all show
/ʔj/ where written. Confirm the IPA matches the recordings, especially that
'yan (007: *'Ƴa'ƴa*) sounds identical to ƴan.

## Q6 — Anything else

Any IPA that mispronounces a word you hear on the recordings. Mark the
sentence number, the word, what you hear vs what the IPA would produce.

---

## Sign-off

- [x] Q1 f/p pair ruling: **f → f** (labiodental, no vowel conditioning); **p → p** confirmed distinct from f — the pair is closed
- [x] Q2 ts ruling: **ts → tsʼ** (ejective, as in “tsetse”)
- [x] Q3 gy/ky/ƙy convention: **palatal stops** — gy → ɟ, ky → c, ƙy → cʼ (single front contact, not ɡ+j)
- [x] Q4 r ruling: **r → ɾ** (single tap everywhere). Reviewer note: lengthened rr occurs only as expressive intensification, not lexical contrast — same category as length/tone, out of G2P scope. Hausa-specific finding; does not transfer to Yoruba/Igbo
- [x] Q5 glottal identity confirmed ('y ≡ ƴ ≡ /ʔj/)
- [x] Q6 other corrections: none
- [x] **Overall: APPROVED**

Name: Abdool (Kano native speaker)  Date: 31 Aug 2026
