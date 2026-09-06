# Smallest witnesses by girth for rad(n) | f(n)

<!-- hallazgo:que -->
## What was found

Take an integer, and for each prime `q` dividing it draw one arrow `q -> p`
whenever `p` divides `f(q^e)`, with `q^e` the exact power of `q` in it and `f`
the sum of divisors or a relative of it. Keep the integers where **every prime
receives an arrow**. That drawing always contains a directed cycle, and the
length of its shortest one is an invariant of the integer.

This work computes, for four such functions, **the smallest integer whose
shortest cycle has each given length** -- 26 values, every one *proved* to be
the smallest that exists and not merely the smallest anyone looked far enough to
find, twelve of them computed here for the first time. And it gives a **local
operation on that cycle** which decides, from one value alone, whether the next
one will be **smaller** -- twice in this table it is.

<!-- hallazgo:enunciado -->
## The statement

Write `rad(n)` for the product of the distinct primes of `n`, and
`S(f) = { n : rad(n) divides f(n) }`. For `n` in `S(f)` the drawing above is the
**covering digraph**, and its shortest directed cycle has length `g_f(n)`, the
**girth**. Write `m_f(k)` for the smallest `n` in `S(f)` with `g_f(n) = k`.

> **Cutoff lemma.** If `n = m_f(k)` and `P` is its largest prime, then
>
>     n  >=  P * a_f(P) * (product of the k-2 smallest primes)
>
> with `a_f(P)` the least prime power `m` for which `P` can divide `f(m)`. Read
> backwards from any exhibited witness, this **bounds `P`**: the enumeration
> becomes finite and every value below becomes a proved minimum.

> **Surgery.** Let `n` be a witness of girth `k` whose digraph is the pure cycle
> `q_1 -> ... -> q_k -> q_1`, let `p` be a prime outside it, and let `e', a >= 1`
> satisfy `p | f(q_i^e')` and `q_{i+1} | f(p^a)` with no chord created. Then
> `n' = n * q_i^(e'-e_i) * p^a` is a witness of girth `k+1`, so
>
>     m_f(k+1)  <=  m_f(k) * q_i^(e'-e_i) * p^a
>
> **Certificate.** If that factor is less than 1, then `m_f(k+1) < m_f(k)` --
> proved *without computing* `m_f(k+1)`, by a finite search that never
> enumerates primes.

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

Take `n = 234 = 2 * 3^2 * 13` and `f = sigma`:

    sigma(2)   = 3             ->  arrow  2  -> 3
    sigma(3^2) = 13            ->  arrow  3  -> 13
    sigma(13)  = 14 = 2 * 7    ->  arrow  13 -> 2

Every prime receives an arrow, so `234` is in `S(sigma)`, and the arrows form
the triangle `2 -> 3 -> 13 -> 2`: girth 3. **No smaller integer has one** --
that is the entry `m_sigma(3) = 234` in the table, and the cutoff lemma is what
turns "none found" into "none exists".

Now the certificate, on `f = sigma*` where `sigma*(q^e) = q^e + 1`:

    m(5) = 540765225 = 3^2 * 5^2 * 7^5 * 11 * 13

Cut `7^5` down to `7^3` and insert the prime `43`. The new stretch costs `43`
and the exponent it releases was worth `7^2 = 49`, so the ratio is `43/49 < 1`.
Therefore `m(6) < m(5)`, and the integer the operation hands back,

    474549075 = 3^2 * 5^2 * 7^3 * 11 * 13 * 43

is `m(6)` **exactly**. The sequence goes down at `k = 5`, and that was known
before computing `m(6)` at all.

<!-- hallazgo:prueba -->
## Why it is proved

The cutoff lemma is two inequalities on the same factor: the predecessor of `P`
on the cycle contributes a prime power `q^e` with `P | f(q^e)`, hence
`q^e >= a_f(P)`; the remaining `k-2` primes are distinct, hence at least the
primorial. With `P` bounded, enumerating cycles over the primes below the bound
is enumerating **all** of them, so a search that finds nothing has proved there
is nothing.

The surgery is a count of arrows. In `n'` the vertices `q_j` with `j != i` kept
their exponents, so they still point only to `q_{j+1}`; `q_i` points to `p` and,
by the no-chord conditions, nowhere else; and `p` points to `q_{i+1}` and
nowhere else. The digraph is exactly the `(k+1)`-cycle. Those conditions are not
bookkeeping: drop them and the same move on `m_sigma(5)` yields `1103602500`,
whose girth is **2**.

<!-- hallazgo:comprobar -->
## Check it yourself, in five seconds

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

396 checks, no dependencies, `PASS` or `FAIL` on each and exit code 1 if any
fails. They re-derive every published value from the definitions, re-prove the
reachable ones exhaustively, and cross-check the count of `S(sigma)` below `10^9`
against Pollack and Pomerance (2012), who never saw this repository.

<!-- hallazgo:nodice -->
## What it does not say

The family of integers is **not new**: for `sigma` these are the *prime-abundant
numbers* of Pollack and Pomerance, catalogued as
[A175200](https://oeis.org/A175200). What is computed here is a graph invariant
over that family. The certificate works in **one direction only**: finding no
insertion below ratio 1 does not prove the next minimum is larger. And the table
stops where the computation stopped -- empty cells are empty, not zero.

---

---

---

**Version 3.2 — 2026-09-04.** Every number in this document is checked by
`python verify.py`, in about five seconds and with nothing installed. The
change log is at the end.

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

**Verified independently of the proof:** all nineteen published terms satisfy
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

## 4. Theorem 3 — the per-arc cost lemma

Theorem 2 keeps two factors of the witness and bounds the rest by a primorial.
Every arc of the cycle carries the same kind of information, and using all of
them gives a bound that is stronger by orders of magnitude.

> **Theorem 3.** Let `f` be one of `sigma`, `sigma*`, `phi*`, let `n` be the
> smallest element of `S(f)` of girth `k`, and let
> `q_1 -> q_2 -> ... -> q_k -> q_1` be its covering digraph, which by Theorem 1
> is a directed cycle on exactly `k` primes. Writing `n = prod q_i^{e_i}`, for
> every `i` (indices mod `k`)
>
>     q_i^{e_i}  >=  max( q_i , a_f(q_{i+1}) )
>
> and therefore
>
>     n  >=  prod_{i=1..k} max( q_i , a_f(q_{i+1}) )                        (+)

*Proof.* Two bounds on the same factor. The first is `e_i >= 1`, so
`q_i^{e_i} >= q_i`. The second is the arc: `q_i -> q_{i+1}` means
`q_{i+1} | f(q_i^{e_i})`, and since `q_{i+1}` is positive,
`q_{i+1} <= f(q_i^{e_i})`; the closed forms then give `q_i^{e_i} >= a_f(q_{i+1})`
exactly as in Theorem 2. A factor satisfying both satisfies their maximum, and
the product of the `k` factors is `n`. QED

**Theorem 2 is what is left after keeping two factors.** With `P = max q_i` and
`q_{j-1}` its predecessor, factor `j` contributes at least `P`, factor `j-1` at
least `a_f(P)`, and the remaining `k-2` at least their own primes, which are
`k-2` distinct primes different from those two, hence at least the primorial of
the `k-2` smallest. That is `n >= P * a_f(P) * primorial(k-2)`.

**How much stronger, on the published terms:**

| | `n` | (*) | (+) | ratio |
|---|---:|---:|---:|---:|
| `sigma`, 7 | 7746928876851255 | 9064904310 | 1255214552865 | 138x |
| `sigma`, 8 | 31674203849435875 | 1650028380 | 11469839585540 | **6951x** |
| `sigma*`, 8 | 2386830845734335 | 109909800 | 79914416400 | 727x |
| `sigma*`, 9 | 9928651387877145 | 1868466600 | 5018546030400 | 2686x |
| `phi*`, 5 | 1663175056640625 | 16560 | 2307360 | 139x |

`verify.py` checks `(*) <= (+) <= n` for **every** term, not only these: if (+)
ever exceeded `n` the search would be pruning away the answer.

**Where it enters the search.** (+) names the whole cycle, which a depth-first
search does not know until the end. What it does know from the first step is
**who will have to close**: the enumeration always starts at the largest prime
`q_1`, so the last vertex is its predecessor and its prime power satisfies
`q^e >= a_f(q_1)`. While at least one vertex is unplaced, the floor for the
remaining stretch is

    max( product of the smallest free primes ,  a_f(q_1) * product of one fewer )

and the second dominates almost always: with `q_1 ~ 10^6` under `sigma`,
`a_f(q_1) ~ 5 * 10^5` against a five-digit primorial. Measured with the same
code, with the lemma switched on and off (`python src/exact.py <f> <k>
--measure-lemma`):

| `f` | `k` | nodes with (*) only | nodes with (+) | saved |
|---|---:|---:|---:|---:|
| `sigma` | 5 | 46691 | 11751 | 4.0x |
| `sigma` | 6 | 638918 | 100043 | 6.4x |
| `sigma*` | 6 | 12940 | 4397 | 2.9x |
| `sigma*` | 7 | 643175 | 97608 | 6.6x |
| `phi*` | 4 | 136898 | 23430 | 5.8x |
| `sigma` | 7 | **74731325** | **4658867** | **16.0x** |

The last row is the one that says most, for two reasons. It is the large case —
287 seconds against 23 — and **the 74731325 nodes with the lemma switched off
reproduce, to the digit, the "74.7 million" that version 2 published** for that
same run. So the switch turns off exactly what is new here and nothing else: the
16x is not shared with any other change.

In all six rows the value found is **identical**, which is what has to happen
if both lemmas are correct: (+) does not change the answer, it changes the cost
of reaching it.

---

## 5. Theorem 4 — the universal floor, and a search that needs no seed

Theorem 2 bounds the primes **in terms of a witness already known**. Version 2
therefore could not touch a girth for which no witness had ever been exhibited,
and said so. The following removes the need.

> **Theorem 4 (universal floor).** Every smallest witness of girth `k` satisfies
>
>     n  >=  p_k * a_f(p_k) * primorial(k-2)                               (++)
>
> where `p_k` is the `k`-th prime.

*Proof.* By Theorem 1 the witness has exactly `k` distinct primes, so its
largest prime `P` satisfies `P >= p_k`. The map
`P -> P * a_f(P) * primorial(k-2)` is increasing, and Theorem 2 places `n` above
its value at `P`. QED

What (++) has and (*) has not is that **it mentions no witness**. With it the
search can start from nothing:

    N <- (++) + 1
    while the exhaustive search below N returns nothing:
        N <- 2N
    return what it returned

> **Theorem 5 (seedless search).** The first value that procedure returns is the
> smallest element of `S(f)` of girth `k`, with proof.

*Proof.* The search with bound `N` is **exhaustive below `N`** -- that is
exactly what Theorem 2 bought: it returns not "the best we saw" but "the
smallest there is, if any is below `N`". Let `v` be the first value returned, on
a round with bound `N`. Then `v < N`, and by exhaustiveness there is no element
of girth `k` smaller than `v` and below `N`; since anything smaller than `v` is
also below `N`, there is none at all. QED

**What is new here and what is not.** Doubling a bound until the answer falls
inside is an old and standard technique (*exponential search*, *galloping
search*); nothing is claimed about it. What was needed was the other half: that
the search below `N` be **exhaustive rather than heuristic**, and a lower bound
(++) that does not depend on knowing the answer. With those two, doubling stops
being a way to start and becomes part of the proof. Without them it proves
nothing.

**What it costs.** Starting without knowing the answer costs a factor of about
four, measured on the terms where both methods can run:

| `f` | `k` | nodes with a seed | nodes with none | overhead |
|---|---:|---:|---:|---:|
| `sigma` | 7 | 4658867 | 20109417 | 4.32x |
| `sigma` | 8 | 2901464 | 12475319 | 4.30x |
| `sigma*` | 8 | 547002 | 2134982 | 3.90x |
| `phi*` | 5 | 7442712 | 30032423 | 4.04x |

The final round runs with a bound of up to twice the answer, and the work is
not linear in the bound: doubling `N` multiplies the prime cutoff by `sqrt(2)`
and the tree by more. With work proportional to `N^a` the total overhead is
`2^a / (1 - 2^-a)`, which is 4.00 at `a = 1` and 4.38 at `a = 1.5`; the four
measurements say `a` is about 1.45. **A factor of four is the whole price of not
knowing the answer**, paid once per girth.

All eighteen terms of version 2 were recomputed this way, with none of them
entering as data, and all eighteen came out to the digit. `verify.py` repeats
that check.

---

## 6. The search, and a correction to version 1

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

## 7. The terms

**All twenty-six are proved minimal.** The twelve in bold had not been computed
before; the one marked with a dagger is the first that **had no seed at all**,
so it could not have been computed by the method of version 2; the two marked
with a double dagger are the ones that version 3 could not reach in practice and
that the surgery of section 9 unlocked.

| girth | `sigma` | `sigma*` | `phi*` | `sigma**` |
|---:|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 | **6** |
| 3 | 234 | 6615 | 66825 | **15925** |
| 4 | 137214 | 4380453 | 1120454775 | **2321865** |
| 5 | 275900625 | 540765225 | **1663175056640625** | **10762773021** |
| 6 | 180141399900 | 474549075 | | **3321843525** |
| 7 | **7746928876851255** | 4485174218525 | | **345358414826425** (dd) |
| 8 | **31674203849435875** | **2386830845734335** | | |
| 9 | | **9928651387877145** (dagger) | | |
| 10 | | **10858178043907173985005** (dd) | | |

The fourth function is `sigma**`, the sum of the **biunitary** divisors: a
divisor `d` of `n` is biunitary when the greatest common unitary divisor of `d`
and `n/d` is 1, which on a prime power leaves every `q^i` except the middle one
when `e` is even, so `sigma**(q^e) = sigma(q^e) - q^(e/2)` for `e` even and
`sigma(q^e)` for `e` odd. `verify.py` compares that closed form against the
definition rather than assuming it.

The two terms marked with a double dagger:

    sigma*,  girth 10:  10858178043907173985005
                        = 3^8 * 5 * 7^3 * 11^2 * 13^2 * 31^2 * 43 * 61 * 97 * 193
                        cycle 193 -> 97 -> 7 -> 43 -> 11 -> 61 -> 31 -> 13 -> 5 -> 3 -> 193
                        every prime up to 36871065 examined; the lemma required
                        33457967. 48321070 nodes, 252 seconds.

    sigma**, girth 7:   345358414826425 = 5^2 * 7^4 * 11^4 * 13 * 19 * 37 * 43
                        cycle 43 -> 11 -> 37 -> 19 -> 5 -> 13 -> 7 -> 43
                        every prime up to 1048575 examined; the lemma required
                        523775. 930082 nodes, 5 seconds.

**What surgery bought here is a measured factor, not a possibility.** The
seedless search reaches both on its own -- it had simply been stopped at round 40
on `sigma*` girth 10, and gets there on round **42**: two short -- and running it
to the end gives the comparison:

| | seedless, from the universal floor | from the surgery bound | saved |
|---|---:|---:|---:|
| `sigma*`, girth 10 | 206680700 nodes, 1125 s, 42 rounds | 48321070 nodes, 252 s | **4.28x** |
| `sigma**`, girth 7 | 4266506 nodes, 23 s, 31 rounds | 930082 nodes, 5 s | **4.59x** |

That factor is exactly the price of not knowing the answer that section 5
measured at about 4, now confirmed on two cases where the two methods can be run
side by side. An exhibited upper bound replaces every doubling round with one.

    python src/exact.py "sigma*" 10 --no-seed     # the 1125 s run
    python src/exact.py "sigma*" 10               # the 252 s one

    sigma*, girth 9:  9928651387877145   = 3^3 * 5 * 7^3 * 11^2 * 19 * 31^2 * 37 * 43 * 61
                      cycle 61 -> 31 -> 37 -> 19 -> 5 -> 3 -> 7 -> 43 -> 11 -> 61

Found with no witness of girth 9 known, on round 27 of the doubling, in 1366619
nodes and about six seconds. The run examined every prime up to 184274 -- the
lemma required only 139458, the difference being that the last round carries a
bound of up to twice the answer -- and the largest prime of the answer is **61**.

Factorizations and cycles of the four terms new in version 2:

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
| `sigma*`, girth 9 | 184 274 | 61 |
| `phi*`, girth 5 | 7 445 747 | 23 |

The largest run — `sigma`, girth 7 — walked 74.7 million nodes of the search
tree in 341 seconds under version 2. **Under version 3 the same run visits
4 658 867 nodes**, sixteen times fewer, because of the per-arc lemma of section
4. Re-proving all nineteen, seeded *and* seedless, now takes
`python verify.py --exact` — **571 seconds** and 223 checks when this was
written, against 1098 seconds and fewer checks in version 2, and with two other
searches competing for the machine at the time.

**Which run the claim rests on.** The first exploratory search for `sigma` at
girth 7 was launched with a cutoff computed as a floating-point square root,
which came out as 2 589 817 — **twenty-seven below the exact bound**. It did not
change the answer, but a cutoff that stops short of what the lemma requires
proves nothing, and that is precisely why `prime_cutoff()` bisects over
integers. The minimality claims here rest on the verifier's runs, which
recompute the cutoff by bisection and sweep the full range.

---

## 8. Growth: no law, and the eighth term is what shows it

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
`n_8 ~ 7 * 10^20`. **The true value is `3.2 * 10^16`, more than four orders of magnitude
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

## 9. Non-monotonicity, and how the extra vertex is paid for

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

**It is not a property of `sigma*`.** `sigma**` does it too, at the same step,
and there the whole difference is one factor: `3^6` against `3^2 * 5^2`, a ratio
of `25/81`. Across the consecutive pairs of the first three functions:

| f | previous | next | decrease? |
|---|---:|---:|---|
| `sigma` (5 → 6) | 275900625 | 180141399900 | no |
| `sigma` (6 → 7) | 180141399900 | 7746928876851255 | no |
| `sigma` (7 → 8) | 7746928876851255 | 31674203849435875 | no |
| `sigma*` (5 → 6) | 540765225 | 474549075 | **yes** |
| `sigma*` (6 → 7) | 474549075 | 4485174218525 | no |
| `sigma*` (7 → 8) | 4485174218525 | 2386830845734335 | no |
| `sigma*` (8 → 9) | 2386830845734335 | 9928651387877145 | no |
| `phi*` (3 → 4) | 66825 | 1120454775 | no |
| `phi*` (4 → 5) | 1120454775 | 1663175056640625 | no |

One decrease in nine consecutive pairs there, two in the twenty-two of the full
table. What section 8 adds is that the same mechanism operates without producing
a decrease: at `sigma` from 7 to 8 it merely flattens the growth.

**The new pair shows the mechanism exactly**, because unlike `sigma` 7 → 8 the
two witnesses share almost everything:

    girth 8 = 3^3 * 5 * 7^3 * 11^2 * 13^2 * 31^2 * 43 * 61
    girth 9 = 3^3 * 5 * 7^3 * 11^2 * 19   * 31^2 * 37 * 43 * 61

Their greatest common divisor is `14123259442215`, and the whole difference is
one stretch of the cycle:

| | stretch | costs |
|---|---|---:|
| girth 8 | `31^2 -> 13^2 -> 5` | `13^2 = 169` |
| girth 9 | `31^2 -> 37 -> 19 -> 5` | `37 * 19 = 703` |

**The extra vertex is bought by splitting one expensive step of exponent 2 into
two cheap steps of exponent 1.** The detour exists because `31^2 + 1 = 2 * 13 *
37` offers both exits, and because `37 + 1 = 2 * 19` and `19 + 1 = 2^2 * 5`
complete it. The ratio of the two terms is exactly `703/169 = 4.1598...`, exact
as a fraction: `m(9) * 169 = m(8) * 703`.

### Theorem 6 — surgery on the cycle

The description above is of one case. Here is the theorem it is a case of.

> **Theorem 6.** Let `f` be multiplicative and **local** -- `q` never divides
> `f(q^e)` -- and let `n = prod q_j^e_j` be a witness of girth `k` whose covering
> digraph is the pure cycle `q_1 -> ... -> q_k -> q_1`. Let `p` be a prime
> outside the cycle and `e', a >= 1` be such that, for some index `i`:
>
> 1. `p | f(q_i^e')`;
> 2. `q_{i+1} | f(p^a)`;
> 3. no `q_j` with `j != i` divides `f(q_i^e')`;
> 4. no `q_j` with `j != i+1` divides `f(p^a)`;
> 5. `p` divides no `f(q_j^e_j)` with `j != i`.
>
> Then `n' = n * q_i^(e'-e_i) * p^a` has as its covering digraph the pure cycle
> of length `k+1` obtained by inserting `p` between `q_i` and `q_{i+1}`. Hence
>
>     m_f(k+1)  <=  m_f(k) * q_i^(e'-e_i) * p^a                          (C)

*Proof.* The vertices of `D_f(n')` are the `k+1` primes. The edges out of `q_j`
with `j != i` did not change, because that exponent did not change: in `n` they
went only to `q_{j+1}`, and (5) says they do not go to `p` either. The edges out
of `q_i` go to `p` by (1) and to no `q_j` by (3) -- and not to `q_i`, by
locality. The edges out of `p` go to `q_{i+1}` by (2), to no other `q_j` by (4),
and not to `p` by locality. So the digraph is exactly the `(k+1)`-cycle: every
vertex has an incoming edge, hence `n'` is in `S(f)`, and its only cycle has
length `k+1`. The arithmetic of (C) is that `n'` replaces `q_i^e_i` by `q_i^e'`
and multiplies by `p^a`. QED

**Conditions 3, 4 and 5 are not bookkeeping.** On the girth-5 minimum for
`sigma`, `275900625`, the pair `13 -> 2^2 -> 7` satisfies (1) and (2) -- `2`
divides `sigma(13)` and `7` divides `sigma(2^2)` -- and yields `1103602500`,
whose girth is **2**, not 6. `verify.py` pins that number, and also checks that
the enumerator does not propose it.

**One implementation note, because it is what makes the enumeration terminate.**
The condition `p | f(q_i^e')` names the primes, so they are read off a
factorisation rather than enumerated -- but factoring `f(q_i^e')` *whole* is
almost always wasted work. A prime is usable only if `q_i^e' p^a` fits the
budget, so `p < budget / q_i^e'`, and every factor above that bound will never
be used. On `sigma_5` with the witness 234 the value `sigma_5(13^7)` has 39
digits and Pollard rho takes 15 seconds to split it, while the bound for that
case is **2**: a 39-digit number factored to find out whether 2 divides it.
Asking only for the prime divisors below the bound takes 0.07 seconds and
returns the same four insertions. `verify.py` checks the two answers against
each other on several hundred cases rather than assuming they agree.

### Corollary — a certificate that the next minimum is smaller

> **Corollary.** If in addition `q_i^e' * p^a < q_i^e_i`, then
> `m_f(k+1) < m_f(k)`.

And this is **decidable by a small finite search**, which is what makes it
useful. With `p^a >= 2` the inequality forces `e' < e_i`, so:

- `e'` runs over `1 .. e_i - 1`;
- `p` runs over the **prime divisors of `f(q_i^e')`**, which condition (1)
  already names -- the primes are never enumerated, they are read off a
  factorisation;
- `a` runs over the exponents with `p^a < q_i^(e_i-e')`.

Nothing in that mentions girth `k+1` or any witness of girth `k+1`. An immediate
consequence: **if every exponent of `m_f(k)` is 1, no certificate can exist**. A
squarefree minimum cannot certify that the next one drops.

**Measured over all 22 consecutive pairs of the table, the certificate fires
exactly twice -- exactly where the sequence goes down -- and both times it
returns the next minimum itself:**

| | `m_f(k)` | cut | insert | ratio | certificate gives | true `m_f(k+1)` |
|---|---:|---|---|---:|---:|---:|
| `sigma*`, 5→6 | 540765225 | `7^5 -> 7^3` | `43` | `43/49` | 474549075 | 474549075 |
| `sigma**`, 5→6 | 10762773021 | `3^6 -> 3^2` | `5^2` | `25/81` | 3321843525 | 3321843525 |

**It is one-directional.** Finding no insertion of ratio below 1 does **not**
prove `m_f(k+1) >= m_f(k)`: the next minimum could come from a cycle unrelated to
this one. That this never happens across the 22 pairs is measured, not proved.

**And surgery gives the next minimum exactly in 12 of the 22 pairs, so it is not
a law either.** In the other 10 the next minimum changes more than one vertex.
That is precisely why (C) is useful as a **bound** and not as a prediction.

### What the bound unlocks

An upper bound that is *exhibited* is what the exhaustive search of section 5
needs to start, and it replaces every doubling round with one. That is how the
two terms marked with a double dagger in section 7 were computed. It also
improves the girth-9 bound for `sigma` -- see section 10 -- and produces bounds
where there were none:

| | upper bound from surgery | ratio |
|---|---:|---:|
| `m_sigma**(8)` | 247135929796462577545675 | 715592611 |

**And it has a limit, which is visible.** From `sigma*` at girth 10 there is **no
admissible insertion at all** with ratio below `10^9`: as `k` grows, conditions
3, 4 and 5 -- which must hold against *every* vertex of the cycle -- get harder
to satisfy. For `phi*` at girth 6 there is exactly **one** admissible insertion
below ratio `10^8`, and it is the bound version 3 already had, so surgery cannot
improve that one.

---

## 10. Bounds on the next two terms, and where the wall is

With the seed gone, the obvious next targets are `sigma` at girth 9 and `phi*`
at girth 6. Neither finished, and the reason is worth stating precisely, because
it is no longer a limitation of the method.

**From below, proved.** The seedless search sweeps exhaustively below each bound
before doubling, so every failed round is a theorem:

| | no witness exists below | primes sieved to say so |
|---|---:|---:|
| `sigma`, girth 9 | **1239376200655897100288** (1.24e21) | 69681011 |
| `phi*`, girth 6 | **1344781885607247872** (1.3e18) | 80023266 |

**That lower bound already says something about the growth.** The eighth term of
`sigma` grew by only 4.09 over the seventh; the ninth is provably more than
**39000 times** the eighth (`1.24e21 / 3.17e16`). So the flattening at the eighth
term **does not continue**: the sequence jumps again. That is a new piece of
evidence against there being a law, and it does not depend on what the ninth term
turns out to be.

**From above, exhibited.** The constructor of version 1 — which builds cycles
over the first few primes and proves no minimality — produces two witnesses, both
verified with the independent code (in `S(f)`, correct girth, pure cycle):

    sigma, girth 9 <= 8324995955560453359590400
                    = 2^10 * 3^4 * 5^2 * 7^6 * 11^4 * 13^2 * 23^2 * 29^2 * 31
                    cycle 2^10 -> 23^2 -> 7^6 -> 29^2 -> 13^2 -> 3^4 -> 11^4 -> 5^2 -> 31

    phi*, girth 6  <= 41542332517979068359375
                    = 3^23 * 5^9 * 11 * 19 * 23 * 47
                    cycle 3^23 -> 47 -> 23 -> 11 -> 5^9 -> 19

Both upper bounds are **stable**: they do not drop when the constructor is given
more primes -- `phi*` girth 6 gives the same value with primes up to 101, 173 and
281; `sigma` girth 9, with primes up to 101 and 131. That does not make them
minima -- the constructor proves no minimality, and stability is not a proof --
but it is the same check section 6 already applies to the published terms.

**And stability is not the same as being the best available.** Surgery on the
girth-8 minimum for `sigma` gives a strictly better witness:

    sigma, girth 9 <= 1232737113370661112862375
                    = 5^3 * 7^2 * 13^2 * 19^2 * 31^2 * 61 * 83 * 127^3 * 331
                    cut 19^1 -> 19^2, insert 127^3, ratio 38919277

That is **6.75 times smaller** than the constructor's, and the reason the
constructor could not find it is not the range of primes -- it uses 127, and the
constructor was given primes up to 131. It is that the constructor fixes, for
each edge, the **least** exponent that realises it, and this witness needs `127^3`
and `19^2`. The same limit is visible on a term that *is* known: for `sigma**` at
girth 4 the constructor returns 49160475 where the true minimum is 2321865,
because the minimum needs `3^6`. `verify.py` checks both facts.

For `phi*` at girth 6, surgery reproduces the constructor's bound exactly -- it
is `m_phi*(5) * 3^12 * 47` -- and proves something the constructor could not: it
is the **only** admissible insertion with ratio below `10^8`. Improving that one
means leaving the mechanism.

So both terms are **bracketed between two verified bounds**:

    1.24e21 <  m_sigma(9)  <=  1.233e24
    1.3e18  <  m_phi*(6)   <=  4.2e22

**And here is the wall, with its number.** To make the enumeration a proof one
has to examine every prime up to the cutoff the upper bound imposes:

| | cutoff the upper bound demands |
|---|---:|
| `sigma`, girth 9, with the bound of version 3.1 | 5710904352 |
| `sigma`, girth 9, with the bound above | **2197597268** |
| `phi*`, girth 6 | 14064872236 |

Two point two and fourteen billion. That does not fit in the machine this was run
on, and not for lack of patience: the sieve alone exceeds memory. The wall is not
in the method any more — the method needs nothing it does not have — but in the
size of the terms, and it moves only two ways: by lowering the upper bound (a
smaller witness narrows the cutoff by a square root) or by sieving in blocks
instead of all at once. Surgery moved it the first way, by a factor of 2.6, and
it is still a wall.

**This is the first time this work can say where it ends.** Before, the limit was
"a known witness is needed", which is a condition on what other people have
published. Now it is a number of primes, which is a condition on the machine.

---

## 11. In `phi*`, each minimum divides the next

Laid out with their cycles, the `phi*` terms show something the factorizations
alone do not:

    phi*, girth 3:  3^5  -> 11 -> 5^2
    phi*, girth 4:  3^11 -> 23 -> 11 -> 5^2
    phi*, girth 5:  3^11 -> 23 -> 11 -> 5^9 -> 19

Each comes from the previous by **inserting one vertex and raising one
exponent**, and nothing else:

- from 3 to 4, `23` enters behind `3` and the exponent of `3` rises from 5 to 11,
  because `3^11 - 1 = 2 * 23 * 3851` creates the arc `3^11 -> 23`; and
  `23 - 1 = 2 * 11` closes onto the `11` that was already there;
- from 4 to 5, `19` enters behind `5` and the exponent of `5` rises from 2 to 9,
  because `19 | 5^9 - 1`; and `19 - 1 = 2 * 3^2` closes onto the `3`.

As a consequence rather than a coincidence:

    m(3) | m(4) | m(5)     (66825 | 1120454775 | 1663175056640625)

**A falsifiable prediction.** The girth-6 witness exhibited in section 10
continues the chain: `3^23 * 5^9 * 11 * 19 * 23 * 47` equals `m(5) * 3^12 * 47`,
and its cycle is the girth-5 cycle with `47` inserted behind `3`. The prediction
is that the **true** minimum of girth 6 is also a multiple of `m(5)`. Any witness
of girth 6 below `4.2e22` that is not a multiple of `1663175056640625` refutes it.

**What does not hold, and it looked obvious.** The first reading of the mechanism
was that the jump is small when the two witnesses share a lot. That is false.
Over the consecutive pairs available, comparing the fraction of bits that
survive from one term to the next against the ratio between them:

| pair | ratio | fraction shared |
|---|---:|---:|
| `phi*` 4->5 | **1484375** | **1.000** |
| `sigma` 6->7 | 43005 | 0.297 |
| `sigma` 7->8 | **4.09** | 0.301 |
| `sigma*` 8->9 | **4.16** | 0.855 |
| `sigma*` 5->6 | **0.88** | 0.806 |

The largest jump of them all -- `phi*` from 4 to 5, a factor of a million and a
half -- is one of those that shares *everything*: the previous term divides the
next. And the two smallest jumps have opposite sharing, 0.30 and 0.86. Sharing
and jump size are **unrelated**. `verify.py` recomputes the whole table.

What does survive is section 9: when the jump is small, the ratio is explained
**to the digit** by one stretch of the cycle changing. Whether it is small or
large is decided by which exponent has to rise for the detour to exist, not by
how much is kept.

---

## 12. What this does not claim

- **It does not claim the sequences are infinite.** Whether a witness of every
  girth exists is a separate question, untouched here.
- **It does not claim minimality for girths beyond the table.** There is no
  longer any obstacle of principle -- Theorem 5 removes the need for a seed --
  but section 10 gives the number of primes that would have to be sieved for the
  next two terms, and it is in the billions.
  **The upper bounds in section 10 are not minima**: they come from the
  constructor or from surgery, neither of which proves minimality. What is proved
  there is that a witness of that size exists, and that is verified.
- **The inversion certificate of section 9 is one-directional.** Finding no
  insertion of ratio below 1 does not prove that the next minimum is larger; the
  next minimum could come from a cycle unrelated to this one. That this never
  happens over the 22 consecutive pairs of the table is a measurement, not a
  proof.
- **The enumeration of insertions is complete within a ratio and an exponent
  bound**, not absolutely. The runs behind this document use ratio below `10^9`
  and exponent at most 64, and both numbers are printed by the tool.
- **The divisibility chain in `phi*` is two links, not a law.** Three terms give
  two pairs, and the third link is predicted, not verified.
- **It does not claim the doubling search is the best way to start.** It is the
  simplest one that keeps the proof intact. A best-first search over partial
  cycles, ordered by the partial product times the floor of what remains, would
  find the minimum without repeating work, and the measured factor of four is
  exactly what such a version would save.
- **It does not claim the growth has a functional form.** It claims the opposite:
  the form four terms supported breaks at the fifth.
- **It does not explain why the eighth term is cheap.** The mechanism is visible
  in the factorizations, but that describes one case; it does not predict when
  it recurs.
- **It does not claim novelty.** See [PRIOR_ART.md](PRIOR_ART.md): searches of
  OEIS and four bibliographic sources found nothing, with a positive control
  that does find the relevant literature. **Not found is not the same as new**,
  and Theorems 2, 3, 4 and 6 and Step 2 of Theorem 1 are short arguments over
  elementary closed forms, so they may well exist under other words. Theorem 5
  in particular combines a standard technique (doubling) with Theorem 2; only
  the combination is claimed, not the technique. Theorem 6 is three lines once
  the right quantity is looked at, and the same caution applies to it.
- **It does not claim mathematical interest.** That is for a human reader to
  judge.

---

## 12b. Splitting the search across cores

The enumeration walks **starting primes** -- the largest prime of the cycle --
and each opens a tree that touches no other, because the walk always begins at
the largest prime and no candidate appears under two starts. Splitting them is
exact, not approximate. The one thing lost is shared pruning: the whole search
lowers its bound on every improvement and that prunes the remaining starts,
while separate processes each carry their own.

**The minimum cannot change.** A process's bound is always at least the true
minimum `m`: it starts at `N > m` and only drops to values of witnesses that
exist, which are `>= m`. The cutoff drops a start `P` only when every witness
beginning at `P` measures at least `cycle_floor(P) >= bound >= m`. Nothing below
`m` is ever dropped.

| `sigma*`, girth 10, same bound | nodes | time |
|---|---:|---:|
| whole, one core | 48321070 | 287.7 s |
| split, twelve cores | 52828732 (+9.3%) | **69.7 s** |

**4.13x**, and the minimum is identical digit for digit. On `sigma` at girth 7
the speedup is 4.54x on eight cores and the node counts are **identical** --
with a tight bound there was nothing left to share.

It does not reach twelve for two measured reasons: the work is skewed, so the
busiest process sets the time; and each process sieves its primes once, which
does not parallelise. **And it does not move the wall of section 10.** That wall
is 2197597268 primes, and splitting makes it worse, because each process would
sieve its own table. A factor of four does not turn an infeasible search into a
feasible one.

    python src/parallel.py sigma 7 7746928876851256 --cores 8 --control

The `--control` flag runs both and compares. This is deliberately not part of
`verify.py`: that file's promise is to run in seconds with nothing installed,
and starting a process pool is a dependency on the machine rather than on a
package. A parallel search that returns a different number is not an
optimisation but a bug, and "it is faster" means nothing without that comparison
beside it.

---

## 12c. Release 3.3.0 — the families, and where the descents are not

Everything above uses four functions with no parameter. Nothing in the cutoff
lemma or in the pure-cycle theorem mentions **which** `f` is used, so the same
machinery applies to the three classical families

    sigma_s(q^e)  = (q^{s(e+1)} - 1)/(q^s - 1)      sigma*_s(q^e) = q^{se} + 1
    phi*_s(q^e)   = q^{se} - 1                       with s = 1..6

What was missing was not mathematics: `arithmetic.py` and `exact.py` each kept
their own hand-written list of four names. Release 3.3.0 replaces both by the
closed forms above, and `verify.py` checks that the two implementations agree on
all 19 functions.

### 26 terms in seven functions, 22 of them computed here

| f | k=2 | k=3 | k=4 | k=5 | k=6 |
|---|---:|---:|---:|---:|---:|
| `sigma*_3` | 6 | 2,565 | 9,933 | 2,175,327 | **1,278,999,267** |
| `sigma*_5` | 6 | 2,013 | 32,175 | 3,910,725 | |
| `sigma*_6` | 10 | 207,553 | 237,133 | | |
| `phi*_3` | 12 | 16,891 | 26,217,125 | 76,670,443,861 | |
| `phi*_4` | 6 | 207,553 | 16,099,333 | 2,534,414,641 | |
| `phi*_5` | 12 | 27,951 | 161,994,931 | | |
| `phi*_6` | 6 | 17,501 | 4,176,227 | | |

Every one is proved minimal the same way as the rest: exhaustive enumeration
below an exhibited upper bound, with the cutoff lemma bounding the largest prime
a smaller witness could use. Twenty-two of the twenty-six were computed for this
release; the four `sigma*_3` terms at girth 2 to 5 were computed earlier in the
same project and are published here for the first time.

**What is out of reach, with the number.** `sigma*_6` at girth 5 would need an
estimated 184 days of six cores, `phi*_5` at girth 5 about 18 days, and
`sigma*_4` at girth 4 is a hard wall: the cutoff lemma demands 1.5 * 10^12
primes. Those are not gaps in the method, they are its cost, and the cost is
now estimated before a search is launched rather than discovered by running it.

### The descents are still only two, and both at 5 -> 6

Section 9 exhibited two functions where `m_f(k+1) < m_f(k)`, and both descents
happen at the same step. With the families the table goes from 48 consecutive
pairs to **64**, and the count does not move:

| f | step | ratio `m_f(k+1)/m_f(k)` |
|---|---|---:|
| `sigma**` | 5 -> 6 | **0.309** |
| `sigma*` | 5 -> 6 | **0.878** |
| `sigma*_6` | 3 -> 4 | 1.143 |
| `sigma_3` | 3 -> 4 | 2.538 |
| `sigma*_3` | 3 -> 4 | 3.873 |

The median of the 64 ratios is **587**, so the two descents are not the tail of
a distribution that grazes 1: they are isolated. The closest miss, `sigma*_6`
from girth 3 to 4, **is** outside the 5 -> 6 step, and is the only non-descent
below 1.2 — which is where to look next.

### The surgery certificate is sufficient and NOT necessary

Section 9 gives a certificate that proves `m_f(k+1) < m_f(k)` without computing
`m_f(k+1)`, and it agreed with the data in 48 out of 48 pairs. It is **not** a
characterisation.

> **Theorem.** For every `k >= 2` and every `C > 0` there is a multiplicative
> and local `f` with `m_f(k+1) < m_f(k)/C`, with `m_f(k)` squarefree — so no
> certificate can fire — and with the cycles of the two minima **disjoint**.

*Proof.* Let `p_1 < ... < p_{k+1}` be the `k+1` smallest primes and let
`P_1 < ... < P_k` be any `k` primes distinct from them. Put
`f(p_i^e) = p_{i+1}` and `f(P_j^e) = P_{j+1}` cyclically, and `f(q^e) = 1` for
every other prime. This is multiplicative by construction and local, because no
prime is its own image, and the digraph of possible arcs is exactly the union of
two disjoint cycles, one of length `k+1` and one of length `k`. So a witness of
girth `k` must contain the `P_j` cycle and `m_f(k) = P_1...P_k`, while
`m_f(k+1) = p_1...p_{k+1}`. Taking the `P_j` large makes the ratio unbounded. []

Checked by brute force in three cases, the minimum found matching the predicted
one digit for digit: `(77, 30)`, `(10403, 30)` and `(1113121, 210)`.

This also settles the other half of the question: a descent does **not** force
the two cycles to share all but one arc. Here they share nothing.

### The surgery is exact exactly when the distance is 2

Measured over the 49 pairs with both minima known, comparing the factorisations
of `m_f(k)` and `m_f(k+1)`:

| primes removed | exponents changed | pairs | of those, surgery exact |
|---:|---:|---:|---:|
| 0 | 1 | **13** | **13** |
| 0 | 3 | 1 | 0 |
| 1 | 0 | 5 | 0 |
| 1 | 1 | 10 | 0 |
| 1 | 2-4 | 4 | 0 |
| 2 | 0-3 | 14 | 0 |
| 3 | 3 | 2 | 0 |

The 13 pairs at distance 2 are exactly the 13 the surgery gets right: 49 out of
49. And since `m_f(k+1)` always has exactly one prime more than `m_f(k)` — a
consequence of Theorem 1 — inserting **two** vertices cannot give the next
minimum. What would help is removing one prime while adding two, which would
take the coverage from 13 to 28 of 49.

### The conditions do not become impossible as k grows

Section 9 suspected that conditions 3, 4 and 5 of the surgery — which must hold
against **every** vertex — become impossible as `k` grows. Measured over 6,661
candidate insertions that satisfy conditions 1 and 2:

| k | candidates | surviving | rate |
|---:|---:|---:|---:|
| 2 | 1,465 | 124 | 8.46 % |
| 3 | 1,369 | 91 | 6.65 % |
| 4 | 1,214 | 29 | 2.39 % |
| 5 | 1,341 | 24 | 1.79 % |
| 6 | 565 | 6 | 1.06 % |
| 7 | 274 | 5 | 1.82 % |
| 8 | 193 | 0 | 0.00 % |
| 9 | 116 | 2 | 1.72 % |
| 10 | 124 | 0 | 0.00 % |

There is one drop and only one: from 7.59 % at girth `<= 3` to 1.72 % at
`>= 4`, with `chi^2 = 138.5` on 1 degree of freedom. **Within `k >= 4` there is
no trend**: the homogeneity `chi^2` is 10.2 on 6 degrees of freedom, so the
seven values are consistent with a **constant** rate, and the two zeros are what
that rate predicts on samples of 193 and 124. What runs out as `k` grows is not
admissibility but *cheap* admissibility.

### Three functions with the same minimum, and why

`sigma*_2`, `phi*_4` and `sigma*_6` all have `m(3) = 207,553 = 17 * 29 * 421`.
With `a = q^s`, `a + 1` divides both `a^2 - 1` and `a^3 + 1`, so

    sigma*_s(q) | phi*_{2s}(q)       and       sigma*_s(q) | sigma*_{3s}(q)

every arc of `sigma*_s` between distinct primes is an arc of the other two, and
a squarefree witness of `sigma*_s` is a witness of both — unless the extra arcs
open a chord. The algebra is elementary; what is not obvious is that the
*minimal* witness survives the change of family, and it does at girth 3 for all
three, and does not at girth 4.

## 13. Reproducing everything

    python verify.py            # all checks, ~2 seconds, no dependencies
    python verify.py --exact    # also re-proves the large terms (~25 minutes)
    python verify.py --full     # also re-derives the sieved terms (needs numpy)

    python src/exact.py "sigma*" 9 --no-seed     # no witness given: it finds it
    python src/exact.py sigma 5 6 --measure-lemma
    python src/exact.py sigma 8
    python src/construct.py sigma 6
    python src/sieve.py 1000000000
    python src/make_terms.py                     # regenerates data/terms.json

    python src/parallel.py sigma 7 7746928876851256 --cores 8 --control

    python src/surgery.py "sigma*" 540765225 5   # the certificate, and it fires
    python src/surgery.py "sigma**" 10762773021 5
    python src/surgery.py sigma 31674203849435875 8 1000000000
    python src/surgery.py "phi*" 1663175056640625 5 100000000

The sieve counts 5327 members of `S(sigma)` below 10^9, excluding `n = 1`.
Pollack and Pomerance count 5328 prime-abundant numbers below 10^9 including
`n = 1` [1]. **The two agree exactly** — this is the strongest external check in
this work, since it tests the code against a peer-reviewed result computed
independently.

---

## Version history

**What changed in version 3.2.** Version 3 could prove a term minimal and could
start with no seed, but it could not say **in advance** whether the next term
would be larger or smaller, and twice in the table it is smaller. Version 3.2
adds a **surgery theorem**: inserting one vertex into the cycle of a witness of
girth `k` yields a witness of girth `k+1`, under three chord conditions that a
negative control shows are indispensable. Two things follow. A **certificate**:
if the inserted stretch costs less than the exponent it saves, then
`m_f(k+1) < m_f(k)`, proved without computing `m_f(k+1)`, by a finite search that
never enumerates primes. And an **exhibited upper bound**, which is exactly what
the exhaustive search needs to start: with it, two terms that could not be
reached before were computed -- `sigma*` at girth 10 and `sigma**` at girth 7 --
the girth-9 bound for `sigma` improved by a factor of 6.75, and a fourth
function, `sigma**`, entered the tables.

**What changed in version 3.** Version 2 could only reach a girth for which
somebody had already exhibited *some* witness, because the cutoff lemma needs a
known `N` to bound anything; it said so itself, and called finding a first
witness *"still a heuristic search"*. That was wrong, and the material to see it
was already in version 2: the search below `N` was **exhaustive**, not
heuristic. Version 3 adds a lower bound that mentions no witness at all, starts
there and doubles, and so **needs no seed**; adds a per-arc strengthening of the
cutoff lemma that makes the search three to seven times cheaper; and computes
the first term that had no seed available — `sigma*` at girth 9.

**What changed in version 2.** Version 1 published a table of smallest witnesses
and said, honestly, what it could not guarantee: *"the answer is only minimal
among the primes examined."* That made every value a conjecture verified as far
as somebody had looked. Version 2 proves a **cutoff lemma** that bounds, in
terms of any witness already known, the largest prime a smaller witness could
possibly use. With that bound the enumeration is finite, the search terminates,
and the values become **proved minima**. Four further values fall out, and an
irregularity in the growth that the earlier terms could not reveal.

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

[4] J. L. Bentley and A. C.-C. Yao, *An almost optimal algorithm for unbounded
searching*, Information Processing Letters **5** (1976), no. 3, 82–87. The
doubling search of Theorem 5 is this technique; it is standard and nothing about
it is claimed here.

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
