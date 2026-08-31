# Draft validation for hausa_g2p.py — run before anything depends on it.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hausa_g2p import normalise, g2p, RULES

fails = []

def check(name, got, want):
    ok = got == want
    if not ok:
        fails.append((name, got, want))
    print(f"{'PASS' if ok else 'FAIL'} {name}: {got!r}" + ("" if ok else f"  (want {want!r})"))

# 1. Spec-flagged risk: .lower() must handle non-standard Latin capitals
check("capitals lower", "Ɓ Ɗ Ƙ Ƴ".lower(), "ɓ ɗ ƙ ƴ")
check("uppercase rule hit", g2p("Ƙofa"), "kʼofa")  # f->f per Kano ruling

# 2. Every apostrophe variant normalises and protects glottalised 'y
for a in ["\u2019", "\u02bc", "\u2018", "`", "\u00b4"]:
    check(f"apos U+{ord(a):04X} -> 'y kept", normalise(f"{a}ya{a}yanshi"),
          "\u02bcya\u02bcyanshi")

# 2b. ASCII apostrophe (U+0027) — the eval set's glottal sentences use it
check("ASCII apos glottal", g2p("'Yan"), "ʔjan")
check("ASCII apos 'ya'yan", g2p("'ya'yan itace"), g2p("ƴaƴan itace"))
check("ASCII apos 'ƴ identity", g2p("'ƴa'ƴa"), g2p("ƴaƴa"))

# 2c. Punctuation passes through (prosodic cue)
check("punct passthrough", g2p("Na gani."), "na ɡani.")
check("punct set", normalise("Yaya kake? Ka zo!"), "Yaya kake? Ka zo!")

# 2d. No 'ch' rule in G2P (moved to prep). ch decomposes to c+h = /tʃh/ —
# orthographically honest, but prep MUST normalise legacy ch-orthography and
# handle English 'ch' names before G2P.
ipa, unk = g2p("chikin", return_unknowns=True)
check("ch decomposes (prep's job to fix)", ipa, "tʃhikin")
check("ch not silently dropped", unk, [])

# 3. Typographic apostrophes NOT before y are stripped
check("typographic strip", normalise("don\u2019t \u2018kai\u2019"), "dont kai")
check("quotes strip", normalise("\u201ckai\u201d \u2018nagari\u2019"), "kai nagari")
# 4. The sharpest test: 'y (Nigerian) and ƴ (Niger) must be identical IPA
check("'y vs ƴ identity", g2p("\u02bcya\u02bcya"), g2p("ƴaƴa"))
check("'y vs ƴ identity (2019)", g2p("\u2019ya\u2019ya"), g2p("ƴaƴa"))
print("   pair IPA:", g2p("ƴaƴa"))

# 5. Longest-match tokenisation
check("ƙw before ƙ+w", g2p("ƙwai"), "kʷʼai̯")
check("ƙy before ƙ+y", g2p("ƙyauta"), "cʼau̯ta")
check("sh before s+h", g2p("shinkafa"), "ʃinkafa")  # f->f per Kano ruling
check("ts ejective", g2p("tsuntsu"), "tsʼuntsʼu")
check("kw labialised", g2p("kwalliya"), "kʷallija")
check("gy palatal", g2p("gyara"), "ɟaɾa")  # r->ɾ per Kano ruling
check("ai diphthong", g2p("kai"), "kai̯")
check("au diphthong", g2p("hauka"), "hau̯ka")

# 6. Misc phonology
check("ɗaya", g2p("ɗaya"), "ɗaja")
check("ɓarna", g2p("ɓarna"), "ɓaɾna")  # r->ɾ per Kano ruling
check("c/pace", g2p("pace"), "patʃe")

# 7. Unknowns are logged, never guessed
ipa, unk = g2p("Zambaƙo 21%", return_unknowns=True)
print(f"   unknown logging on mixed input: IPA={ipa!r} unknown={unk}")
check("digit logged", "2" in unk, True)
check("percent logged", "%" in unk, True)

# 8. Invisibles
check("NBSP -> space", normalise("kai\u00a0na"), "kai na")
check("ZWSP removed", normalise("ka\u200bi"), "kai")

print()
print(f"{len(fails)} failures")
sys.exit(1 if fails else 0)
