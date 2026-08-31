# Tests for waxal_prep.py — the ch-guard ruling.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from waxal_prep import prep_text, alias_legacy_ch, row_has_english_ch

fails = []
def check(name, got, want):
    ok = got == want
    if not ok:
        fails.append(name)
    print(f"{'PASS' if ok else 'FAIL'} {name}: {got!r}" + ("" if ok else f"  (want {want!r})"))

# Hausa legacy-orthography tokens alias
check("chi -> ci", prep_text("chi"), "ci")
check("chikin -> cikin", prep_text("chikin"), "cikin")
check("che -> ce", prep_text("che"), "ce")
check("tachi -> taci", prep_text("tachi"), "taci")
check("sentence alias", prep_text("na chita hutu a chikin gida"),
      "na cita hutu a cikin gida")

# English names untouched
check("Okocha protected", prep_text("Okocha"), "Okocha")
check("Chelsea protected", prep_text("Chelsea"), "Chelsea")
check("Tuchel protected", prep_text("Tuchel"), "Tuchel")
check("mixed sentence", prep_text("Chelsea ta doke Okocha a Garba"),
      "Chelsea ta doke Okocha a Garba")
check("mixed with alias", prep_text("Chelsea da chikin garin London"),
      "Chelsea da cikin garin London")

# case preservation on alias
check("case preserved", prep_text("Chikin"), "Cikin")

# standard Boko 'c' never touched
check("c untouched", prep_text("cikin ce ci"), "cikin ce ci")

# row-exclusion mode
check("exclude flags English row", prep_text("Kungiyar Chelsea", mode="exclude"), None)
check("exclude passes clean row", prep_text("chikin gida", mode="exclude"), "cikin gida")
check("row_has_english_ch", row_has_english_ch("Tuchel ya kebe"), True)
check("row_has_english_ch false", row_has_english_ch("chikin gida"), False)

# canonical verified examples behave
check("Okocha row", prep_text("Okocha, Kanu, Ahmad musa,"), "Okocha, Kanu, Ahmad musa,")
check("Tuchel row aliases nothing else", prep_text("Thomas Tuchel ya nada"),
      "Thomas Tuchel ya nada")

print()
print(f"{len(fails)} failures: {fails}" if fails else "all checks passed")
sys.exit(1 if fails else 0)
