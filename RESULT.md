# Smallest witnesses by girth for rad(n) | f(n)

**Version 2.0 — 2026-09-03**

Every number in this document can be checked by running `python verify.py`,
which takes about two seconds and needs nothing installed.

**What changed in version 2.** Version 1 published a table of smallest witnesses
and said, honestly, what it could not guarantee: *"the answer is only minimal
among the primes examined."* That made every value a conjecture verified as far
as somebody had looked. Version 2 proves a **cutoff lemma** that bounds, in
terms of any witness already known, the largest prime a smaller witness could
possibly use. With that bound the enumeration is finite, the search terminates,
and the values become **proved minima**. Four further values fall out, and an
irregularity in the growth that the earlier terms could not reveal.

---

## 1. The objects

For a positive integer `n` with prime factorization `n = q1^e1 * ... * qk^ek`:

| | |
|---|---|
| `rad(n)` | the **radical**: `q1 * ... * qk`, the largest squarefree divisor |
| `sigma(n)` | the sum of all divisors of `n` |
| `sigma*(n)` | the sum of the **unitary** divisors: `prod (qi^ei + 1)` |
| `phi*(n)` | the unitary analogue of Euler's phi: `prod (qi^ei - 1)` |

For a multiplicative function `f`, write

    S(f) = { n : rad(n) divides f(n) }.

For `f = sigma` this is a known set: the **prime-abundant numbers** of Pollack
and Pomerance [1], catalogued as [A175200](https://oeis.org/A175200).

### The covering digraph

Given `n` in `S(f)`, the **covering digraph** `D_f(n)` has the primes dividing
`n` as vertices, with an edge

    q -> p     whenever   p divides f(q^e),

where `q^e` is the exact power of `q` dividing `n`.

The name comes from the following observation: `n` lies in `S(f)` precisely when
every vertex of `D_f(n)` has at least one incoming edge. Membership in `S(f)` is
a covering condition on this digraph.

The **girth** of `n` is the length of the shortest directed cycle in `D_f(n)`.
Since a member of `S(f)` cannot have an acyclic covering digraph, the girth is
always defined.

### An example to fix ideas

`n = 234 = 2 * 3^2 * 13`, under `f = sigma`:

    sigma(2)   = 3            so   2 -> 3
    sigma(3^2) = 13           so   3 -> 13
    sigma(13)  = 14 = 2 * 7   so   13 -> 2

The digraph is the directed triangle `2 -> 3 -> 13 -> 2`. Its girth is 3, and no
smaller member of `S(sigma)` has girth 3.

---

## 2. Theorem 1 — the shape of a smallest witness

> **Theorem 1.** Let `f` be multiplicative and `k >= 2`. If some `n` in `S(f)`
> has girth `k`, then the smallest such `n` has exactly `k` distinct prime
> factors, and its covering digraph is a pure directed cycle of length `k`.

*Proof.* Let `n` be the smallest member of `S(f)` of girth `k`, and let `C` be a
directed cycle of length `k` in `D_f(n)`.

**Step 1 — no extra vertices.** Let `n'` be the divisor of `n` formed by the
exact prime powers of the primes on `C`. An edge `q -> p` exists when
`p | f(q^e)`, which **does not depend on the other primes of n**: restricting
preserves the exponents, hence every edge of `C` survives in `D_f(n')`. Each
vertex of `C` therefore still has its incoming edge from within `C`, so
`n'` lies in `S(f)`. Its girth is `k`: it contains `C`, and it cannot contain a
shorter cycle, since its edges are a subset of those of `n`. By minimality of
`n`, `n' = n`, and so `omega(n) = k`.

**Step 2 — no chords.** Suppose there were an edge `v_i -> v_j` with
`j != (i+1) mod k`. Following `C` from `v_j` reaches `v_i` in
`d = (i - j) mod k` steps, so that edge closes a directed cycle of length
`1 + d`. Since `d <= k - 1`, this length is at most `k`, with equality only when
`j = (i+1) mod k` — the excluded case. So it would be a cycle strictly shorter
than `k`, contradicting that the girth is `k`.

**Step 3.** With `omega(n) = k`, no chords, and every vertex having at least one
incoming edge because `n` is in `S(f)`, the only edges are those of `C`. The
digraph *is* the cycle. ∎

Step 2 is a fact about digraphs, not about arithmetic, and should be assumed
known. What this work contributes is joining it to Step 1, which uses the
multiplicativity of `f`.

**Verified independently of the proof:** all eighteen published terms satisfy
both conclusions (check 3 of `verify.py`), and among the 353 members of `S(f)`
with girth at least 3 below 2·10^7, not one has a chord in its minimal cycle.

---

## 3. Theorem 2 — the cutoff lemma, and why it is the point

Theorem 1 turns the search into building cycles over small primes. It does not
say **how small**. Without an answer to that, a search can only ever report
"nothing cheaper among the primes I looked at".

> **Theorem 2 (cutoff lemma).** Let `f` be one of `sigma`, `sigma*`, `phi*`, let
> `n` be a smallest witness of girth `k`, and let `P` be the largest prime
> dividing `n`. Then
>
>     n  >=  P * a_f(P) * primorial(k-2)                                  (*)
>
> where `primorial(j)` is the product of the `j` smallest primes and
>
>     a_sigma(P)  = ceil(P/2),    a_sigma*(P) = P - 1,    a_phi*(P) = P + 1.

*Proof.* By Theorem 1, `n` has exactly `k` distinct primes
`q_1, ..., q_k` and `D_f(n)` is the cycle `q_1 -> ... -> q_k -> q_1`. Let
`P = q_j`, let `q_{j-1}` be its predecessor on the cycle and let `q^e` be the
exact power of `q_{j-1}` dividing `n`. That the edge exists means `P | f(q^e)`,
and since `P` is positive, `P <= f(q^e)`. From the closed forms:

| `f` | `f(q^e)` | consequence of `P <= f(q^e)` |
|---|---|---|
| `sigma` | `(q^(e+1)-1)/(q-1) < 2 q^e` | `q^e > P/2`, i.e. `q^e >= ceil(P/2)` |
| `sigma*` | `q^e + 1` | `q^e >= P - 1` |
| `phi*` | `q^e - 1` | `q^e >= P + 1` |

Now `n` is the product of its `k` exact prime powers. Split them into three
groups, disjoint because `k >= 2` forces `P` and its predecessor to be distinct
vertices:

- the power of `P` itself contributes at least `P`;
- the power of `q_{j-1}` contributes at least `a_f(P)`, by the table;
- the remaining `k-2` are powers of primes distinct from each other and from
  those two, so each contributes at least its own prime, and a product of `k-2`
  distinct primes is at least the product of the `k-2` smallest. ∎

**Corollary — the search becomes finite.** If **any** witness `N` of girth `k`
is known, the smallest one is at most `N`, so by (*) its largest prime satisfies

    P  <=  the largest P with  P * a_f(P) * primorial(k-2) < N

which is of order `sqrt(N / primorial(k-2))`. Enumerating cycles over the primes
up to that bound is therefore exhaustive: what comes out is **the** minimum.

The bound is computed by bisection over integers, never by a floating-point
square root: rounding the wrong way would discard exactly the boundary case the
lemma exists to cover.

**Every published term satisfies (\*)**, and its largest prime lies inside the
cutoff derived from it — check 7 of `verify.py`. If that ever failed, every
"proved minimal" here would be worth nothing.

---

## 4. The search, and a correction to version 1

`src/construct.py` fixed, for each edge `q -> p`, the **smallest** exponent `e`
with `p | f(q^e)`; assembled `n`; checked the girth; and if a chord appeared, it
discarded the whole prime cycle.

That can lose witnesses. The edges leaving `q` **depend on the exponent**:
raising `e` changes the entire out-neighbourhood of `q` and can *remove* the
chord the minimal exponent created. A prime cycle discarded with minimal
exponents may be valid with a larger one.

`src/exact.py` searches over `(prime, exponent)` pairs and requires the absence
of chords **while building**. On adding the `m`-th vertex it demands, then and
there:

1. `q_m` divides `f(q_{m-1}^{e_{m-1}})` — the edge exists;
2. `q_m` divides no earlier `f(q_i^{e_i})` — nothing else points at it;
3. `f(q_m^{e_m})` is divisible by no prime already placed — no edge backwards.

Any violation of 2 or 3 would close a directed cycle shorter than `k`.

**The correction changed no value.** All fourteen terms of version 1 were
reproduced digit for digit. So the earlier restriction had lost nothing *in
these cases* — which was not known before, and now is.

**One caution kept from version 1.** Building a cycle is not enough: the girth
must be verified afterwards from the integer. The first version of the search
proposed `n = 120 = 2^3 * 3 * 5` as the smallest witness of girth 3 under
`sigma`, on the cycle `2 -> 5 -> 3 -> 2`; the true girth of 120 is 2. Every
candidate is still checked with an independent girth computation before it is
accepted.

---

## 5. The terms

**All eighteen are proved minimal.** The four in bold had not been computed
before.

| girth | `sigma` | `sigma*` | `phi*` |
|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 |
| 3 | 234 | 6615 | 66825 |
| 4 | 137214 | 4380453 | 1120454775 |
| 5 | 275900625 | 540765225 | **1663175056640625** |
| 6 | 180141399900 | 474549075 | |
| 7 | **7746928876851255** | 4485174218525 | |
| 8 | **31674203849435875** | **2386830845734335** | |

Factorizations and cycles of the four new terms:

    sigma,  girth 7:  7746928876851255   = 3^2 * 5 * 7^4 * 13 * 19 * 37 * 2801^2
                      cycle 3 -> 13 -> 7 -> 2801 -> 37 -> 19 -> 5 -> 3

    sigma,  girth 8:  31674203849435875  = 5^3 * 7^2 * 13^2 * 19 * 31^2 * 61 * 83 * 331
                      cycle 5 -> 13 -> 61 -> 31 -> 331 -> 83 -> 7 -> 19 -> 5

    sigma*, girth 8:  2386830845734335   = 3^3 * 5 * 7^3 * 11^2 * 13^2 * 31^2 * 43 * 61
                      cycle 3 -> 7 -> 43 -> 11 -> 61 -> 31 -> 13 -> 5 -> 3

    phi*,   girth 5:  1663175056640625   = 3^11 * 5^9 * 11 * 19 * 23
                      cycle 3 -> 23 -> 11 -> 5 -> 19 -> 3

**What "proved" cost.** The gap between the two columns below is the whole
result: the search had to rule out every prime in the left column to be able to
say the answer uses the one on the right.

| | every prime examined up to | largest prime in the answer |
|---|---:|---:|
| `sigma`, girth 7 | 2 589 844 | 2801 |
| `sigma`, girth 8 | 1 452 412 | 331 |
| `sigma*`, girth 8 | 281 925 | 61 |
| `phi*`, girth 5 | 7 445 747 | 23 |

The largest run — `sigma`, girth 7 — walked 74.7 million nodes of the search
tree in 341 seconds. Re-proving all eighteen takes about eighteen minutes:
`python verify.py --exact` — 1098 seconds when this was written.

**Which run the claim rests on.** The first exploratory search for `sigma` at
girth 7 was launched with a cutoff computed as a floating-point square root,
which came out as 2 589 817 — **twenty-seven below the exact bound**. It did not
change the answer, but a cutoff that stops short of what the lemma requires
proves nothing, and that is precisely why `prime_cutoff()` bisects over
integers. The minimality claims here rest on the verifier's runs, which
recompute the cutoff by bisection and sweep the full range.

---

## 6. Growth: no law, and the eighth term is what shows it

Version 1 could not address how fast the smallest witness grows. With eight
terms for `sigma` it can be addressed, and the answer is negative:

| `k` | `sigma`: smallest witness | digits | ratio to previous | `ln n / k^2` |
|---:|---:|---:|---:|---:|
| 2 | 6 | 1 | — | 0.448 |
| 3 | 234 | 3 | 39 | 0.606 |
| 4 | 137214 | 6 | 586 | 0.739 |
| 5 | 275900625 | 9 | 2011 | 0.777 |
| 6 | 180141399900 | 12 | 653 | 0.720 |
| 7 | 7746928876851255 | 16 | **43005** | 0.747 |
| 8 | 31674203849435875 | 17 | **4.09** | 0.594 |

Four consecutive terms — `k = 4` to `7` — have `ln n / k^2` between 0.72 and
0.78, which invites reading `n ~ exp(0.75 k^2)`. That reading predicts
`n_8 ~ 2.7 * 10^20`. **The true value is `3.2 * 10^16`, four orders of magnitude
below.**

The factorizations show why. The girth-7 minimum is **forced to use 2801^2** —
with seven primes no cheap cycle closes — and that factor alone costs 7.8
million. The girth-8 minimum closes with primes no larger than 331 and small
exponents: **the eighth vertex is nearly free, and it avoids the expensive
prime.**

> Adding a prime can make the cycle **cheaper**, not dearer.

That is the same mechanism behind the one known decrease in these sequences —
`sigma*` from girth 5 to 6, where admitting the prime 43 let `7^5` drop to `7^3`
— but here it does not invert the sequence; it stalls it. The term still grows,
and grows four thousand times less than the earlier trend demanded.

**So: with eight terms there is no law to state, and what supported the previous
one was the sample.**

---

## 7. Non-monotonicity: still an isolated event

The sequence of smallest witnesses is **not** increasing for `sigma*`:

    6,  6615,  4380453,  540765225,  474549075,  4485174218525,  2386830845734335
                                          ^ the only decrease

The two numbers involved share the skeleton `3^2 * 5^2 * 11 * 13 = 32175`,
differing in a single factor:

| | factor | value |
|---|---|---:|
| girth **6** | `7^3 * 43` | **14749** |
| girth **5** | `7^5` | 16807 |

Closing the 5-cycle forces the exponent of 7 up to `7^5`. Extending to a 6-cycle
admits a new prime, 43, and **that allows the exponent to drop to `7^3`**.

**It is not a property of `sigma*`.** Across the eighteen terms:

| f | previous | next | decrease? |
|---|---:|---:|---|
| `sigma` (5 → 6) | 275900625 | 180141399900 | no |
| `sigma` (6 → 7) | 180141399900 | 7746928876851255 | no |
| `sigma` (7 → 8) | 7746928876851255 | 31674203849435875 | no |
| `sigma*` (5 → 6) | 540765225 | 474549075 | **yes** |
| `sigma*` (6 → 7) | 474549075 | 4485174218525 | no |
| `sigma*` (7 → 8) | 4485174218525 | 2386830845734335 | no |
| `phi*` (3 → 4) | 66825 | 1120454775 | no |
| `phi*` (4 → 5) | 1120454775 | 1663175056640625 | no |

One decrease in eight consecutive pairs. What section 6 adds is that the same
mechanism operates without producing a decrease: at `sigma` from 7 to 8 it
merely flattens the growth.

---

## 8. What this does not claim

- **It does not claim the sequences are infinite.** Whether a witness of every
  girth exists is a separate question, untouched here.
- **It does not claim minimality for girths beyond the table.** The cutoff lemma
  needs a known witness to start from; without one the bound is infinite.
  Finding the *first* witness of a new girth is still a heuristic search, and
  only afterwards does it become a proof.
- **It does not claim the growth has a functional form.** It claims the opposite:
  the form four terms supported breaks at the fifth.
- **It does not explain why the eighth term is cheap.** The mechanism is visible
  in the factorizations, but that describes one case; it does not predict when
  it recurs.
- **It does not claim novelty.** See [PRIOR_ART.md](PRIOR_ART.md): searches of
  OEIS and four bibliographic sources found nothing, with a positive control
  that does find the relevant literature. **Not found is not the same as new**,
  and both Theorem 2 and Step 2 of Theorem 1 are short arguments over elementary
  closed forms, so they may well exist under other words.
- **It does not claim mathematical interest.** That is for a human reader to
  judge.

---

## 9. Reproducing everything

    python verify.py            # all checks, ~2 seconds, no dependencies
    python verify.py --exact    # also re-proves the large terms (~25 minutes)
    python verify.py --full     # also re-derives the sieved terms (needs numpy)

    python src/exact.py sigma 8
    python src/construct.py sigma 6
    python src/sieve.py 1000000000

The sieve counts 5327 members of `S(sigma)` below 10^9, excluding `n = 1`.
Pollack and Pomerance count 5328 prime-abundant numbers below 10^9 including
`n = 1` [1]. **The two agree exactly** — this is the strongest external check in
this work, since it tests the code against a peer-reviewed result computed
independently.

---

## References

[1] P. Pollack and C. Pomerance, *Prime-Perfect Numbers*, INTEGERS: Electronic
Journal of Combinatorial Number Theory **12A** (2012), Paper A14.
[https://doi.org/10.1515/integers-2012-0044](https://doi.org/10.1515/integers-2012-0044)

[2] OEIS Foundation Inc., *The On-Line Encyclopedia of Integer Sequences*,
[A175200](https://oeis.org/A175200): numbers `k` such that `rad(k)` divides
`sigma(k)`.

[3] OEIS Foundation Inc., [A000066](https://oeis.org/A000066): smallest number
of vertices in a trivalent graph of girth `n` — an analogous "smallest object of
given girth" sequence.

---

## Author

**Jorge Ellena Godoy** — author and responsible for the correctness of
everything published here.

## How this was produced

The system design and the direction of this research are the author's. The
mathematical results were produced by an automated system (Claude, Anthropic)
under that direction. All computations were verified by two independent
implementations and cross-checked against [1]. The author is responsible for the
correctness of everything published here.
