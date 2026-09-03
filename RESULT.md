# Smallest witnesses by girth for rad(n) | f(n)

**Version 1.0 — 2026-09-03**

Every number in this document can be checked by running `python verify.py`,
which takes about two seconds and needs nothing installed.

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

## 2. The theorem

> **Theorem.** Let `f` be multiplicative and `k >= 2`. If some `n` in `S(f)` has
> girth `k`, then the smallest such `n` has exactly `k` distinct prime factors,
> and its covering digraph is a pure directed cycle of length `k`.

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

**Verified independently of the proof:** all fourteen published terms satisfy
both conclusions (check 3 of `verify.py`), and among the 353 members of `S(f)`
with girth at least 3 below 2·10^7, not one has a chord in its minimal cycle.

---

## 3. The theorem as an algorithm

The theorem changes how the smallest witness can be found.

Sieving for a witness of girth 6 under `sigma` is hopeless. The counts per girth
below 10^9 are:

| girth | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|
| members of `S(sigma)` | 4138 | 1065 | 122 | **2** |

The counts fall by factors 3.9, then 8.7, then **61** — and the factor keeps
growing. Even assuming it stopped growing, expecting a single witness of girth 6
would need about 30 times more members, and since the count grows like
`x^(1/3)`, that means sieving to roughly `10^13`. With a more realistic factor,
`10^14` to `10^15`.

But if the smallest witness **is** a pure `k`-cycle on `k` primes, one can build
it instead: for each ordered pair `(q, p)` find the least `e` with
`p | f(q^e)` — the cost of that edge — and search for the `k`-cycle of least
product. The bound stops being the size of `n` and becomes how many primes to
examine.

**One caution, learned the hard way.** Building a cycle is not enough: the girth
must be verified afterwards. Choosing the least exponent per edge can create
*extra* edges among the same primes, and those chords shorten the cycle. The
first version of the search proposed `n = 120 = 2^3 * 3 * 5` as the smallest
witness of girth 3 under `sigma`, on the cycle `2 -> 5 -> 3 -> 2`; the true
girth of 120 is 2. Every candidate is now checked with an independent girth
computation.

---

## 4. The terms

| girth | `sigma` | `sigma*` | `phi*` |
|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 |
| 3 | 234 | 6615 | 66825 |
| 4 | 137214 | 4380453 | **1120454775** |
| 5 | 275900625 | 540765225 | — |
| 6 | **180141399900** | 474549075 | — |
| 7 | — | **4485174218525** | — |

The three values in bold were **not reachable by sieving** and were obtained
with the construction. Their factorizations:

    sigma,  girth 6:  180141399900   = 2^2 * 3^4 * 5^2 * 7^2 * 11^4 * 31
                      cycle 2 -> 7 -> 3 -> 11 -> 5 -> 31 -> 2

    phi*,   girth 4:  1120454775     = 3^11 * 5^2 * 11 * 23
                      cycle 3 -> 23 -> 11 -> 5 -> 3

    sigma*, girth 7:  4485174218525  = 5^2 * 7^3 * 11^3 * 13 * 19 * 37 * 43
                      cycle 5 -> 13 -> 7 -> 43 -> 11 -> 37 -> 19 -> 5

The last one is about `4.5 * 10^12`, far beyond any exhaustive search.

---

## 5. Non-monotonicity: an isolated event

The sequence of smallest witnesses is **not** increasing for `sigma*`:

    6,  6615,  4380453,  540765225,  474549075,  4485174218525
                                          ^ the only decrease

The smallest witness of girth 6 is *smaller* than the one of girth 5. The reason
is visible in the factorizations, which share the skeleton
`3^2 * 5^2 * 11 * 13 = 32175`, differing in a single factor:

| | factor | value |
|---|---|---:|
| girth **6** | `7^3 * 43` | **14749** |
| girth **5** | `7^5` | 16807 |

Closing the 5-cycle forces the exponent of 7 up to `7^5`. Extending to a 6-cycle
admits a new prime, 43, and **that allows the exponent to drop to `7^3`**.
Adding a vertex came out cheaper than raising an exponent.

**This is not a property of `sigma*`.** With the new terms:

| f | previous | next | decrease? |
|---|---:|---:|---|
| `sigma` (5 → 6) | 275900625 | 180141399900 | no |
| `sigma*` (5 → 6) | 540765225 | 474549075 | **yes** |
| `sigma*` (6 → 7) | 474549075 | 4485174218525 | no |
| `phi*` (3 → 4) | 66825 | 1120454775 | no |

The decrease happens once, at `sigma*` from 5 to 6, and nowhere else among the
terms known. In `sigma` the sixth vertex costs 31 **and** forces 11 and 3 up to
the fourth power; in `phi*` the fourth pushes 3 to the eleventh. Where there is
no shortcut, the minimum grows.

---

## 6. What this does not claim

- **It does not claim the sequences are infinite.** Whether a witness of every
  girth exists is a separate question, untouched here.
- **It does not claim the terms are minimal beyond the primes examined.** The
  construction is exhaustive only within its prime set. The published values
  were checked at two different bounds (20 primes, up to 71; and 26 primes, up
  to 101) and did not change.
- **It does not claim novelty.** See [PRIOR_ART.md](PRIOR_ART.md): searches of
  OEIS and four bibliographic sources found nothing, with a positive control
  that does find the relevant literature. **Not found is not the same as new**,
  and Step 2 of the proof is elementary graph theory that likely exists under
  another name.
- **It does not claim mathematical interest.** That is for a human reader to
  judge.

---

## 7. Reproducing everything

    python verify.py            # all checks, ~2 seconds, no dependencies
    python verify.py --full     # also re-derives the sieved terms (needs numpy)

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
