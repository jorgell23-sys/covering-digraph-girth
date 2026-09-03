# Prior art: what was searched, where, and when

**Not finding something is not the same as it being new.** This file records
exactly what was searched so that a reader can judge how much the absence is
worth — and repeat it.

Searches performed **2026-09-03**.

---

## 1. The set itself is not new, and is cited

`S(sigma) = { n : rad(n) divides sigma(n) }` are the **prime-abundant numbers**
of Pollack and Pomerance, *Prime-Perfect Numbers*, INTEGERS 12A (2012), Paper
A14. They are catalogued as [A175200](https://oeis.org/A175200), submitted by
Michel Lagneau in 2010.

Nothing in this repository claims that set as its own. What is computed here is
a **graph invariant over that family**.

## 2. OEIS — the sequences

| query | result |
|---|---|
| `6, 234, 137214, 275900625, 180141399900` | **not in OEIS** |
| `6, 6615, 4380453, 540765225, 474549075, 4485174218525` | **not in OEIS** |

OEIS asks that simple transformations be checked too, since a sequence may be
catalogued doubled or shifted. All five variants were searched:

| variant | result |
|---|---|
| as is | not found |
| without the first term | not found |
| each term + 1 | not found |
| each term − 1 | not found |
| each term doubled | not found |

Result: **`NOT UNDER ANY SIMPLE TRANSFORMATION`**.

## 3. OEIS — the individual values

Each new value was searched on its own digits, across all ~380,000 sequences:

| value | entries containing it |
|---|---:|
| `180141399900` | **0** |
| `1120454775` | **0** |
| `4485174218525` | **0** |

## 4. Bibliographic databases

Searched: **zbMATH**, **OpenAlex**, **Crossref**, **arXiv**. All four responded
in every query.

The method requires terms that must appear **together** in a title or abstract;
without that, any query matches something, since the individual words of a
mathematical statement appear everywhere.

| terms required together | result |
|---|---|
| `prime` *(positive control)* | **finds** Pollack & Pomerance, *Prime-Perfect Numbers* (2012) |
| `girth` + `multiplicative` | nothing |
| `cycle` + `divisor` + `smallest` | nothing |
| `radical` + `sigma` | nothing |

**The positive control is the point.** A search that finds nothing is worthless
unless it can be shown to find something when there is something to find. It
does: it retrieves the paper that defines the underlying set.

### A false positive worth recording

An earlier attempt required `girth` + `digraph` together and reported
*APPEARS IN THE LITERATURE*. That was wrong. Those two words appear together in
any digraph paper — colouring, the Caccetta–Häggkvist conjecture, expander
graphs — and in none of them about arithmetic functions.

**Required terms must pin down both halves of the object**, not one. The
corrected queries above each demand an arithmetic term alongside the graph term.

## 5. Analogous sequences that do exist

Sequences of the form "smallest object of girth n" are an established genre:

- [A000066](https://oeis.org/A000066) — smallest number of vertices in a
  trivalent graph of girth n. Ten terms, keywords `nonn,hard,more,nice`,
  submitted by N. J. A. Sloane.
- [A266731](https://oeis.org/A266731) — the same for bi-regular graphs.

They are about **graphs**; this one is about **divisibility**. The shape of the
question is the same.

## 6. What all this is worth

`NOT FOUND IN WHAT WAS SEARCHED` — and that is the strongest statement
available.

It may exist under other words, in a source not searched, or as an exercise in a
book no index covers. In particular, **Step 2 of the proof in
[RESULT.md](RESULT.md) is elementary graph theory** — that a chord in a minimal
cycle would produce a shorter one — and is likely known under another name. What
did not appear is the conjunction: the girth of the covering digraph **of a
multiplicative function**.

Proving that something has never been known is not possible by searching. What
is possible is to say precisely where one looked, and that is what this file
does.

## Reproducing these searches

The OEIS queries can be repeated at [oeis.org](https://oeis.org) by pasting the
terms. The bibliographic queries were made through the public APIs of the four
databases named above.
