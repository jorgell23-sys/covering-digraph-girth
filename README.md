# Smallest witnesses by girth for `rad(n) | f(n)`

<!-- hallazgo:que -->
## What was found

For a multiplicative function `f` and an integer `n`, draw an arc `q -> p`
between primes dividing `n` whenever `p | f(q^e)`, with `q^e` the exact power of
`q` in `n`. Restrict to those `n` in which every prime receives an arc; such an
`n` always contains a directed cycle, and the length of the shortest one is an
invariant of `n`.

This repository computes **the least `n` whose shortest cycle has length `k`**,
for eleven functions and `k = 2, ..., 10`: **52 values, each proved minimal**, 38
of them computed here for the first time. It also proves a local operation on the
cycle that yields an upper bound for the next value, and a **certificate**
derived from it deciding `m_f(k+1) < m_f(k)` without computing `m_f(k+1)`. The
certificate is proved **sufficient and not necessary**.

<!-- hallazgo:enunciado -->
## Definitions and statements

Let `f` be multiplicative and **local**, meaning that `q` never divides
`f(q^e)`. Write `rad(n)` for the product of the distinct primes of `n` and

    S(f) = { n >= 1 : rad(n) divides f(n) }.

For `n = prod q_j^{e_j}` in `S(f)`, the **covering digraph** `D_f(n)` has the
primes of `n` as vertices and an arc `q_i -> q_j` (`i != j`) whenever
`q_j | f(q_i^{e_i})`. Membership in `S(f)` is equivalent to every vertex having
an incoming arc, so `D_f(n)` always contains a directed cycle. Its **girth**
`g_f(n)` is the length of the shortest one, and

    m_f(k) = min { n in S(f) : g_f(n) = k }.

The eleven functions are `sigma`, `sigma*` (unitary), `phi*` (unitary totient),
`sigma**` (biunitary), and the parametric families

    sigma_s(q^e)  = (q^{s(e+1)} - 1)/(q^s - 1),    sigma*_s(q^e) = q^{se} + 1,
    phi*_s(q^e)   = q^{se} - 1,                    for s = 3, 4, 5, 6.

> **Theorem 1 (shape of a minimum).** `m_f(k)` has exactly `k` distinct primes,
> and `D_f(m_f(k))` is a pure `k`-cycle.

> **Theorem 2 (cutoff lemma).** Let `n` be a witness of girth `k` and `P` its
> largest prime, and let `a_f(P)` be the least prime power `m` with `P | f(m)`.
> Then
>
>     n  >=  P * a_f(P) * primorial(k-2).
>
> Consequently, once any witness `N` of girth `k` is exhibited, the largest prime
> of `m_f(k)` is bounded by the largest `P` for which the inequality still admits
> `n < N`. Enumeration below that bound is exhaustive, so a search that finds
> nothing proves that nothing exists.

> **Theorem 3 (surgery).** Let `n` be a witness of girth `k` whose digraph is the
> pure cycle `q_1 -> ... -> q_k -> q_1`, let `p` be a prime outside it, and let
> `e', a >= 1` satisfy, for some index `i`:
>
> 1. `p | f(q_i^{e'})`;
> 2. `q_{i+1} | f(p^a)`;
> 3. `q_j` does not divide `f(q_i^{e'})` for every `j != i`;
> 4. `q_j` does not divide `f(p^a)` for every `j != i+1`;
> 5. `p` does not divide `f(q_j^{e_j})` for every `j != i`.
>
> Then `n' = n * q_i^{e'-e_i} * p^a` is a witness of girth `k+1`, whence
>
>     m_f(k+1)  <=  m_f(k) * q_i^{e'-e_i} * p^a.
>
> **Corollary (certificate).** If moreover `q_i^{e'} * p^a < q_i^{e_i}`, then
> `m_f(k+1) < m_f(k)`. Deciding this is a finite search that never enumerates
> primes: the inequality forces `e' < e_i`, so `e'` ranges over `1..e_i-1`, `p`
> over the prime divisors of `f(q_i^{e'})`, and `a` over `p^a < q_i^{e_i-e'}`.

> **Theorem 4 (the certificate is not necessary).** For every `k >= 2` and every
> `C > 0` there exists a multiplicative, local `f` with `m_f(k+1) < m_f(k)/C`,
> with `m_f(k)` squarefree — so that no certificate can fire — and with the
> cycles of `m_f(k)` and `m_f(k+1)` **disjoint**.

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

Let `n = 234 = 2 * 3^2 * 13` and `f = sigma`:

    sigma(2)   = 3            ->   2 -> 3
    sigma(3^2) = 13           ->   3 -> 13
    sigma(13)  = 14 = 2 * 7   ->   13 -> 2

Every prime receives an arc, so `234` lies in `S(sigma)`, and the arcs form the
triangle `2 -> 3 -> 13 -> 2`: girth 3. Theorem 2 applied with the witness
`N = 234` bounds the largest prime of any smaller witness by 13; enumerating
those cases leaves nothing. Hence `m_sigma(3) = 234` is a minimum, not a record.

For the certificate take `f = sigma*`, where `sigma*(q^e) = q^e + 1`, and

    m_{sigma*}(5) = 540765225 = 3^2 * 5^2 * 7^5 * 11 * 13.

Cut `7^5` down to `7^3` and insert the prime `43`. Conditions 1–5 hold, and
`7^3 * 43 < 7^5` because `43 < 49`. Therefore `m_{sigma*}(6) < m_{sigma*}(5)`,
known before computing it. The witness the construction returns,
`474549075 = 3^2 * 5^2 * 7^3 * 11 * 13 * 43`, turns out to be `m_{sigma*}(6)`.

<!-- hallazgo:prueba -->
## Why the statements hold

**Theorem 2** is two lower bounds on the same product. The predecessor of `P` on
the cycle contributes a prime power `q^e` with `P | f(q^e)`, so `q^e >= a_f(P)`
by the definition of `a_f`; the remaining `k-2` primes are pairwise distinct and
distinct from `P` and `q`, so their product is at least the primorial. The bound
is evaluated in integer arithmetic throughout: a floating-point value at the
boundary could discard a legitimate witness.

**Theorem 3** is a count of arcs. In `n'` the vertices `q_j` with `j != i` keep
their exponents, so they still point only to `q_{j+1}`, and condition 5 says they
do not point to `p`; `q_i` points to `p` by condition 1 and to no `q_j` by
condition 3; `p` points to `q_{i+1}` by condition 2, to no other `q_j` by
condition 4, and not to itself by locality. The digraph is therefore exactly the
`(k+1)`-cycle. Conditions 3–5 are not bookkeeping: dropping them, the same move
applied to `m_sigma(5)` yields `1103602500`, whose girth is **2**.

**Theorem 4** is a construction. Let `p_1 < ... < p_{k+1}` be the `k+1` least
primes and let `P_1 < ... < P_k` be any `k` primes distinct from them. Set
`f(p_i^e) = p_{i+1}` and `f(P_j^e) = P_{j+1}` cyclically, and `f(q^e) = 1`
otherwise. This is multiplicative by construction and local, and its arc set is
exactly two disjoint cycles, of lengths `k+1` and `k`. A witness of girth `k`
must therefore contain every `P_j`, giving `m_f(k) = P_1...P_k`, while
`m_f(k+1) = p_1...p_{k+1}`; choosing the `P_j` large makes the ratio unbounded.

<!-- hallazgo:comprobar -->
## Verification

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

413 checks, no dependencies, `PASS` or `FAIL` on each, exit code 1 if any fails.
They re-derive every published value from the definitions, re-prove the reachable
ones exhaustively, build the `f` of Theorem 4 and locate its minima by brute
force, and cross-check the count of `S(sigma)` below `10^9` against Pollack and
Pomerance (2012).

<!-- hallazgo:nodice -->
## What is not claimed

The underlying set is **not new**: for `sigma` these are the prime-abundant
numbers of Pollack and Pomerance, catalogued as
[A175200](https://oeis.org/A175200). What is computed here is a graph invariant
over that family. Minimality is claimed only for the girths listed; empty cells
are unknown, not zero. Whether a witness of every girth exists is untouched. The
certificate is one-directional, and Theorem 4 shows it cannot be turned into a
characterisation for general `f`.

---

> New to this? [**Explained from scratch**](https://jorgell23-sys.github.io/covering-digraph-girth/),
> with pictures and no background assumed
> ([español](https://jorgell23-sys.github.io/covering-digraph-girth/es/)).

---

## The terms

Values in **bold** were computed in this work; every entry is proved minimal.

| `k` | `sigma` | `sigma*` | `phi*` | `sigma**` |
|---:|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 | **6** |
| 3 | 234 | 6615 | 66825 | **15925** |
| 4 | 137214 | 4380453 | 1120454775 | **2321865** |
| 5 | 275900625 | 540765225 | **1663175056640625** | **10762773021** |
| 6 | 180141399900 | 474549075 | | **3321843525** |
| 7 | **7746928876851255** | 4485174218525 | | **345358414826425** |
| 8 | **31674203849435875** | **2386830845734335** | | |
| 9 | | **9928651387877145** | | |
| 10 | | **10858178043907173985005** | | |

| `k` | `sigma*_3` | `sigma*_5` | `sigma*_6` |
|---:|---:|---:|---:|
| 2 | **6** | **6** | **10** |
| 3 | **2565** | **2013** | **207553** |
| 4 | **9933** | **32175** | **237133** |
| 5 | **2175327** | **3910725** | |
| 6 | **1278999267** | | |

| `k` | `phi*_3` | `phi*_4` | `phi*_5` | `phi*_6` |
|---:|---:|---:|---:|---:|
| 2 | **12** | **6** | **12** | **6** |
| 3 | **16891** | **207553** | **27951** | **17501** |
| 4 | **26217125** | **16099333** | **161994931** | **4176227** |
| 5 | **76670443861** | **2534414641** | | |

`data/terms.json` carries each value with its factorisation, its cycle and the
prime bound up to which the enumeration ran. It is regenerated by computation,
not transcribed.

## Descents

`m_f(k+1) < m_f(k)` occurs **twice** among the 64 consecutive pairs with both
minima known, both times at the step `5 -> 6`:

| f | step | `m_f(k)` | `m_f(k+1)` | ratio |
|---|---|---:|---:|---:|
| `sigma**` | 5 -> 6 | 10762773021 | 3321843525 | **0.309** |
| `sigma*` | 5 -> 6 | 540765225 | 474549075 | **0.878** |

The median of the 64 ratios is **587**, so the two descents are isolated rather
than the tail of a distribution reaching down to 1. The smallest ratio that is
not a descent is `sigma*_6` from girth 3 to 4, at 1.143, and it lies outside the
`5 -> 6` step.

The certificate of Theorem 3 fires on exactly those two pairs and returns the
next minimum exactly. Comparing factorisations across the 49 pairs on which the
surgery can be tested, it is exact precisely when `m_f(k+1)` is obtained from
`m_f(k)` by adding one prime and changing one exponent — 49 agreements out of 49.
Since `m_f(k+1)` always has exactly one prime more than `m_f(k)` by Theorem 1,
inserting two vertices cannot produce the next minimum.

Conditions 3–5 have to hold against every vertex of the cycle, which suggests
they become harder to satisfy as `k` grows. Measured over 6661 candidate
insertions satisfying conditions 1 and 2, the survival rate drops once — from
7.59 % at girth at most 3 to 1.72 % at girth 4 or more, `chi^2 = 138.5` on one
degree of freedom — and is then **constant**: the homogeneity `chi^2` is 10.2 on
six degrees of freedom. What runs out as `k` grows is not admissibility but cheap
admissibility.

## Limits, with numbers

Two terms are bracketed rather than determined:

| | proved to exceed | witness exhibited at | primes needed to close it |
|---|---:|---:|---:|
| `m_sigma(9)` | `1.24e21` | `1.23e24` | `2.20e9` |
| `m_phi*(6)` | `1.3e18` | `4.15e22` | `1.4e10` |

Both bounds are theorems: the lower one because the search beneath it was
exhaustive, the upper one because the witness is exhibited and verified. Closing
either requires enumerating the stated number of primes, which does not fit in
memory here. Several further terms are out of reach by cost rather than by
principle: `sigma*_6` at girth 5 and `phi*_5` at girth 5 are estimated at 184 and
18 days respectively on six cores, and `sigma*_4` at girth 4 would require
`1.5e12` primes.

## Methods, and how they are cross-checked

Three implementations share no logic. A sieve finds witnesses by exhaustive
search over integers and knows nothing about cycles; a constructor builds them
from cycles over small primes and never inspects an integer not built from one;
the exact search proves minimality via Theorem 2 and accepts nothing without
recomputing the girth from the integer itself. They agree on every term that more
than one of them can reach.

There is also an external check. The sieve counts **5327** members of `S(sigma)`
below `10^9` excluding `n = 1`; Pollack and Pomerance count **5328** including
it. The agreement tests this code against a peer-reviewed result obtained
independently.

Prior-art searches — OEIS and six bibliographic databases, each accompanied by a
positive control that does return the relevant literature — are recorded with
their dates and query terms in [`PRIOR_ART.md`](PRIOR_ART.md). *Not found is not
the same as new.*

## Contents

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | full report: statements, proofs, tables, limits |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched for prior work, where and when |
| `verify.py` | every check, one command, no dependencies |
| `src/arithmetic.py` | the definitions, in plain Python |
| `src/exact.py` | proves minimality using the cutoff lemma |
| `src/construct.py` | builds witnesses from cycles over small primes |
| `src/sieve.py` | exhaustive search over integers (requires numpy) |
| `src/surgery.py` | Theorem 3 and its certificate |
| `src/parallel.py` | the same exact search, split across cores |
| `src/make_terms.py` | regenerates `data/terms.json` by computation |

A Spanish version of this page: [`README.es.md`](README.es.md).

## Citing

See [`CITATION.cff`](CITATION.cff). Licence: MIT for the code, CC BY 4.0 for text
and data.

## Author

**Jorge Ellena Godoy**.

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by independent implementations and cross-checked
against published work. The author is responsible for the correctness of
everything published here.
