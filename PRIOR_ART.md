# Prior art: what was searched, where, and when

**Not finding something is not the same as it being new.** This file records
exactly what was searched so that a reader can judge how much the absence is
worth — and repeat it.

Searches performed **2026-09-03** (version 1), repeated and extended the same
day for **version 2**.

---

## 1. The set itself is not new, and is cited

`S(sigma) = { n : rad(n) divides sigma(n) }` are the **prime-abundant numbers**
of Pollack and Pomerance, *Prime-Perfect Numbers*, INTEGERS 12A (2012), Paper
A14. They are catalogued as [A175200](https://oeis.org/A175200), submitted by
Michel Lagneau in 2010.

Nothing in this repository claims that set as its own. What is computed here is
a **graph invariant over that family**, and — new in version 2 — a bound that
makes computing it a proof rather than a search.

## 2. OEIS — the sequences

All three complete sequences, with the version-2 terms included:

| sequence | result |
|---|---|
| `sigma`: 6, 234, 137214, 275900625, 180141399900, 7746928876851255, 31674203849435875 | **not in OEIS** |
| `sigma*`: 6, 6615, 4380453, 540765225, 474549075, 4485174218525, 2386830845734335 | **not in OEIS** |
| `phi*`: 12, 66825, 1120454775, 1663175056640625 | **not in OEIS** |

OEIS asks that simple transformations be checked too, since a sequence may be
catalogued doubled or shifted. All five variants were searched for each — as is,
without the first term, each term ± 1, each term doubled.

Result for all three: **`NOT UNDER ANY SIMPLE TRANSFORMATION`**.

## 3. OEIS — the individual values

Each new value was searched on its own digits, across all ~380,000 sequences:

| value | entries containing it |
|---|---:|
| `180141399900` *(v1)* | **0** |
| `1120454775` *(v1)* | **0** |
| `4485174218525` *(v1)* | **0** |
| `7746928876851255` *(v2)* | **0** |
| `31674203849435875` *(v2)* | **0** |
| `2386830845734335` *(v2)* | **0** |
| `1663175056640625` *(v2)* | **0** |

## 4. Bibliographic databases

Searched: **zbMATH**, **OpenAlex**, **Crossref**, **arXiv**. Which of the four
answered varies between queries and is recorded below; a source that did not
answer contributes nothing either way.

The method requires terms that must appear **together** in a title or abstract;
without that, any query matches something, since the individual words of a
mathematical statement appear everywhere.

| terms required together | sources that answered | result |
|---|---|---|
| `prime` *(positive control)* | zbMATH, OpenAlex, Crossref | **finds** Pollack & Pomerance, *Prime-Perfect Numbers* (2012) |
| `multiplicative function` + `girth` | zbMATH, Crossref, arXiv | nothing |
| `prime divisor` + `girth` | zbMATH, Crossref | nothing |
| `largest prime` + `radical` | zbMATH, OpenAlex, Crossref | nothing |
| `cycle` + `divisor` + `smallest` | zbMATH, Crossref, arXiv | nothing |
| `arithmetic function` + `minimal` | zbMATH, Crossref | nothing |

**The positive control is the point.** A search that finds nothing is worthless
unless it can be shown to find something when there is something to find. It
does: it retrieves the paper that defines the underlying set.

### Two false positives, and the rule they produced

**Version 1** required `girth` + `digraph` together and reported *APPEARS IN THE
LITERATURE*. That was wrong. Those two words appear together in any digraph
paper — colouring, the Caccetta–Häggkvist conjecture, expander graphs — and in
none of them about arithmetic functions. The rule written down at the time was:
*required terms must pin down both halves of the object, not one.*

**Version 2 broke the same rule again**, which is why it is now recorded here
rather than only in prose. Requiring `girth` + `multiplicative` returned
*Diameter and girth of the multiplicative zero-divisor graph of multiplicative
lattices* (2016), [doi:10.1142/s1793557116500716](https://doi.org/10.1142/s1793557116500716).
That paper has nothing to do with this one: "multiplicative" there qualifies a
**lattice**, not an arithmetic function.

Version 1's table listed `girth` + `multiplicative` as returning nothing. **That
entry was wrong and is corrected here.** With the object named as a phrase —
`multiplicative function` — the query returns nothing, which is the row in the
table above.

The lesson, now enforced rather than written down: **a one-word required term
matches that word in any field's sense**, so a verdict resting on one arrives
with the caveat attached. The positive control above is deliberately one word
and is deliberately loose; that is what a control is for. Note that it also
retrieves a paper on the NLRP3 inflammasome, which is exactly the failure mode
in miniature.

## 5. The cutoff lemma specifically

The lemma of version 2 — bounding the largest prime of a minimal witness by
`sqrt(N / primorial(k-2))`, so that the enumeration is finite — is a three-step
argument over the closed forms of `sigma`, `sigma*` and `phi*` on prime powers.
Nothing of that shape appeared in the searches above.

That is a weak statement and is meant to be. Arguments of this kind are the sort
of thing that exists in a paper's Lemma 2.1 without appearing in its title or
abstract, which is all these databases index.

## 6. Analogous sequences that do exist

Sequences of the form "smallest object of girth n" are an established genre:

- [A000066](https://oeis.org/A000066) — smallest number of vertices in a
  trivalent graph of girth n. Ten terms, keywords `nonn,hard,more,nice`,
  submitted by N. J. A. Sloane.
- [A266731](https://oeis.org/A266731) — the same for bi-regular graphs.

They are about **graphs**; this one is about **divisibility**. The shape of the
question is the same.

## 7. What all this is worth

`NOT FOUND IN WHAT WAS SEARCHED` — and that is the strongest statement
available.

It may exist under other words, in a source not searched, or as an exercise in a
book no index covers. In particular, **Step 2 of Theorem 1 in
[RESULT.md](RESULT.md) is elementary graph theory** — that a chord in a minimal
cycle would produce a shorter one — and is likely known under another name. What
did not appear is the conjunction: the girth of the covering digraph **of a
multiplicative function**, and a cutoff that turns its computation into a proof.

Proving that something has never been known is not possible by searching. What
is possible is to say precisely where one looked, to say when the looking was
wrong, and to correct it. That is what this file does.

## Reproducing these searches

The OEIS queries can be repeated at [oeis.org](https://oeis.org) by pasting the
terms. The bibliographic queries were made through the public APIs of the four
databases named above.
