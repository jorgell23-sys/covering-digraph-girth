# Prior art: what was searched, where, and when

**Not finding something is not the same as it being new.** This file records
exactly what was searched so that a reader can judge how much the absence is
worth — and repeat it.

Searches performed **2026-09-03** (versions 1 and 2), and repeated and extended
**2026-09-04** for **version 3** and again for **version 3.2**.

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
| `sigma*`: 6, 6615, 4380453, 540765225, 474549075, 4485174218525, 2386830845734335, 9928651387877145 | **not in OEIS** |
| `phi*`: 12, 66825, 1120454775, 1663175056640625 | **not in OEIS** |
| `sigma*` with the version-3.2 term appended, up to 10858178043907173985005 | **not in OEIS** |
| `sigma**`: 6, 15925, 2321865, 10762773021, 3321843525, 345358414826425 | **not in OEIS** |

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
| `9928651387877145` *(v3)* | **0** |
| `10858178043907173985005` *(v3.2)* | **0** |
| `345358414826425` *(v3.2)* | **0** |
| `10762773021` *(v3.2)* | **0** |
| `3321843525` *(v3.2)* | **0** |

**Two positive controls, run with the same code on the same day.** For the
sequences: the perfect numbers `6, 28, 496, 8128, 33550336` return `ALREADY
CATALOGUED` ([A000396](https://oeis.org/A000396)), and the abundant numbers
`12, 18, 20, 24, 30, 36, 40, 42, 48, 54` return
[A005101](https://oeis.org/A005101). For the **single values** -- which are a
different query and so need their own control -- searching `33550336` on its own
digits returns **10 entries**, A000396 among them. The zeros in the table above
are therefore the instrument saying nothing, not the instrument being broken.

**And the first attempt at this control failed, which is why it is here.** The
single-value queries were first run through the same helper used for sequences,
which refuses anything shorter than a few terms: it returned "too short" for the
new values *and for the perfect number*, so it could not tell an absence from a
refusal. The numbers above come from the query that does answer, checked against
the control first.

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
| `covering digraph` + `girth` *(v3)* | zbMATH, OpenAlex, Crossref, arXiv | nothing |
| `rad(n)` + `sigma(n)` *(v3)* | zbMATH, OpenAlex, Crossref, arXiv | nothing |
| `unitary sigma` + `girth` *(v3)* | zbMATH, OpenAlex, Crossref, arXiv | nothing |
| `sigma(n)` + `radical` *(v3, positive control)* | zbMATH, OpenAlex, Crossref, arXiv | **finds** work on the sum-of-divisors function |

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

## 6. The seedless search specifically (version 3)

Theorem 5 of [RESULT.md](RESULT.md) says that doubling a bound over an
exhaustive search finds the minimum with no seed. **The doubling itself is
standard** and is not claimed: it is *exponential search* / *galloping search*,
textbook material since Bentley and Yao (1976), *An almost optimal algorithm for
unbounded searching*, Information Processing Letters 5(3).

What is claimed is only the combination with Theorem 2 — that the search below a
bound is exhaustive rather than heuristic, which is what turns the doubling into
a proof — and the universal floor (Theorem 4) that gives it somewhere to start.
Both are two-line arguments over the same closed forms as Theorem 2, and the
same caveat applies: arguments of this shape live inside papers without reaching
their titles or abstracts.

**Version 2 got this wrong in the other direction**, and it is recorded here for
the same reason the two false positives above are. It wrote that finding a first
witness was *"still a heuristic search"* — a claim about what its own method
could not do, made without checking, and false. The exhaustiveness that refutes
it was proved in that same document. A limit stated about one's own work is a
claim like any other and needs the same checking.

## 6b. The surgery theorem specifically (version 3.2)

Theorem 6 of [RESULT.md](RESULT.md) inserts one vertex into the cycle and gives
a bound on the next minimum, with a certificate for when the next minimum is
smaller.

Two searches, with the terms required to appear together:

| query | terms required together | result |
|---|---|---|
| covering digraph girth multiplicative function radical divides | girth, digraph, divisor | **not found in what was searched** (arXiv did not answer) |
| smallest integer whose covering digraph has girth k unitary sigma | girth, unitary | **not found in what was searched** (arXiv did not answer) |

**The positive control for the same run**: `unitary perfect numbers sum of
unitary divisors`, terms `unitary` and `perfect` required together, returns
Subbarao and Warren, *Unitary perfect numbers*, Canad. Math. Bull. 9 (1966);
Wall, *The fifth unitary perfect number* (1975); and Wall, *Bi-unitary perfect
numbers*, Proc. AMS (1972). The sources answer and do find the relevant
literature when there is some.

**What is and is not claimed.** Inserting a vertex into a cycle is an elementary
move, and the proof of Theorem 6 is a paragraph of bookkeeping once the right
five conditions are written down. What did not appear anywhere searched is the
conjunction: this move on the **covering digraph of a multiplicative function**,
and the use of the cost inequality as a **certificate of non-monotonicity** for
the sequence of smallest witnesses. As with Theorems 2, 3 and 4, an argument of
this shape can live inside a paper without reaching its title or abstract.

**A note on sigma\*\***. The biunitary divisor function is not new -- Wall
studied bi-unitary perfect numbers in 1972 -- and nothing about the function
itself is claimed here. What is computed is the same graph invariant over it.

## 7. Analogous sequences that do exist

Sequences of the form "smallest object of girth n" are an established genre:

- [A000066](https://oeis.org/A000066) — smallest number of vertices in a
  trivalent graph of girth n. Ten terms, keywords `nonn,hard,more,nice`,
  submitted by N. J. A. Sloane.
- [A266731](https://oeis.org/A266731) — the same for bi-regular graphs.

They are about **graphs**; this one is about **divisibility**. The shape of the
question is the same.

## 8. What all this is worth

`NOT FOUND IN WHAT WAS SEARCHED` — and that is the strongest statement
available.

It may exist under other words, in a source not searched, or as an exercise in a
book no index covers. In particular, **Step 2 of Theorem 1 in
[RESULT.md](RESULT.md) is elementary graph theory** — that a chord in a minimal
cycle would produce a shorter one — and is likely known under another name. What
did not appear is the conjunction: the girth of the covering digraph **of a
multiplicative function**, a cutoff that turns its computation into a proof, and
a floor that lets that computation start from nothing.

Proving that something has never been known is not possible by searching. What
is possible is to say precisely where one looked, to say when the looking was
wrong, and to correct it. That is what this file does.

## Reproducing these searches

The OEIS queries can be repeated at [oeis.org](https://oeis.org) by pasting the
terms. The bibliographic queries were made through the public APIs of the four
databases named above.
