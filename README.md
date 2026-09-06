# Smallest witnesses by girth for rad(n) | f(n)

<!-- hallazgo:que -->
## What was found

Take an integer, and for each prime `q` dividing it draw one arrow `q -> p`
whenever `p` divides `f(q^e)`, with `q^e` the exact power of `q` in it and `f`
the sum of divisors or a relative of it. Keep the integers where **every prime
receives an arrow**. That drawing always contains a directed cycle, and the
length of its shortest one is an invariant of the integer.

This work computes, for eleven such functions, **the smallest integer whose
shortest cycle has each given length** -- 52 values, every one *proved* to be
the smallest that exists and not merely the smallest anyone looked far enough to
find, 38 of them computed here for the first time. And it gives a **local
operation on that cycle** which decides, from one value alone, whether the next
one will be **smaller** -- twice in 64 consecutive pairs it is, both times at
the same step, and the operation is shown to be sufficient but **not**
necessary.

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

> **New to this? Start here:** [**Explained from scratch**](https://jorgell23-sys.github.io/covering-digraph-girth/) - the whole
> thing in plain words, with pictures and no background needed
> ([en espanol](https://jorgell23-sys.github.io/covering-digraph-girth/es/)).

---

## What this is about

Take a number, say **234 = 2 × 3² × 13**, and two classical functions: `rad(n)`,
the product of its distinct primes, and `sigma(n)`, the sum of its divisors.

Now draw a graph. The **vertices** are the primes dividing `n`. There is an
**arrow q → p** whenever `p` divides `sigma(q^e)`, with `q^e` the exact power of
`q` in `n`:

```
sigma(2)   = 3            →   2 → 3
sigma(3²)  = 13           →   3 → 13
sigma(13)  = 14 = 2 × 7   →   13 → 2
```

The graph is a triangle: `2 → 3 → 13 → 2`. Its shortest cycle has length 3 —
its **girth** is 3. And 234 is the smallest number of its kind with girth 3.

This repository answers: **what is the smallest number of girth k?**

The set of numbers where every prime is covered this way is not new — for
`sigma` they are the *prime-abundant numbers* of Pollack and Pomerance (2012),
catalogued as [A175200](https://oeis.org/A175200). What is computed here is a
graph invariant over that family.

## The results

| girth | `sigma` | `sigma*` | `phi*` | `sigma**` |
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

The twelve in bold had not been computed before, and **all twenty-six are proved
minimal**. Two of them -- `sigma*` at girth 10 and `sigma**` at girth 7 -- were
computed from an upper bound the surgery below exhibits, which costs about
**4.3x less** than searching with no bound at all (measured both ways). And notice `sigma*` from girth 5 to 6, and `sigma**` from 5 to 6: the
sequence goes **down**. Section *"When the next one is smaller"* is about why,
and about how to know it in advance.

## The difference between "smallest we found" and "smallest"

Version 1 said, honestly, what it could not guarantee:

> *The answer is only minimal among the primes examined. A larger prime could in
> principle give a cheaper cycle.*

So every value was a conjecture verified as far as somebody had looked. Closing
that gap takes one lemma.

Let `n` be a smallest witness of girth `k` and let `P` be its largest prime. Its
predecessor on the cycle contributes a prime power `q^e` with `P | f(q^e)`, so
`P ≤ f(q^e)`, and the closed forms give `q^e ≥ P/2` for `sigma`, `≥ P−1` for
`sigma*`, `≥ P+1` for `phi*`. The remaining `k−2` primes are distinct, so:

```
n  ≥  P · a_f(P) · (product of the k−2 smallest primes)
```

Read backwards, that is a **cutoff**: if any witness `N` is known, the smallest
one is at most `N`, so its largest prime cannot exceed roughly
`sqrt(N / primorial(k−2))`. Enumerating cycles over the primes below that is
exhaustive, and the answer stops depending on how far anybody looked.

For `phi*` with girth 5 the cutoff is **7 445 747**. Every prime below it had to
be ruled out to be able to say the answer's largest prime is **23**.

## Starting without knowing the answer

That cutoff is stated **in terms of a witness already known**, so version 2 could
not touch a girth nobody had exhibited an example of. It said as much, and called
finding a first witness *"still a heuristic search"*.

That was wrong, and version 2 had the material to see it. The search below `N` is
**exhaustive**: it returns not "the best we saw" but "the smallest there is, if
any is below `N`". So all that was missing was a starting `N` that owes nothing
to a known answer. A witness of girth `k` has exactly `k` distinct primes, so its
largest prime is at least `p_k`, and the cutoff bound is increasing in it:

```
n  >=  p_k · a_f(p_k) · (product of the k-2 smallest primes)
```

Start there, double until something appears, and **the first thing that appears
is the minimum** — nothing smaller is below this `N`, and nothing at all was
below the previous ones, which were already swept. Doubling is an old technique;
what makes it a proof here is the exhaustiveness underneath it.

```bash
python src/exact.py "sigma*" 9 --no-seed     # no witness given: it finds it
```

The price of not knowing the answer is a factor of about **4** in nodes visited,
measured on the terms where both methods can run. It is paid once per girth.

## Where it ends, with a number

The next two terms did not finish, and version 3 can say exactly why. The search
swept everything below `1.24e21` for `sigma` at girth 9 and below `1.3e18` for
`phi*` at girth 6 and found nothing — those are theorems. Surgery exhibits
witnesses at `1.23e24` and `4.2e22` — those are verified, but not minimal. So
both terms are **bracketed**, and closing the bracket would mean examining every
prime below **2.2 billion** and **14 billion** respectively. That does not fit in
memory.

The first of those two numbers used to be **5.7 billion**: the girth-9 witness
for `sigma` that version 3.1 exhibited was `8.3e24`, and surgery brings it down
to `1.23e24`, a factor of **6.75**. The wall moved by a factor of 2.6, and it is
still a wall.

Before, the limit was *"a known witness is needed"* — a condition on what other
people have published. Now it is a number of primes: a condition on the machine.

## One more thing worth seeing

Under `phi*`, each minimum **divides** the next:

```
girth 3:  3^5  → 11 → 5^2                 66825
girth 4:  3^11 → 23 → 11 → 5^2            1120454775
girth 5:  3^11 → 23 → 11 → 5^9 → 19       1663175056640625
```

Each cycle is the previous one with **one vertex inserted and one exponent
raised**, which is why the divisibility follows. The exhibited girth-6 witness
continues the chain. **Prediction:** the true girth-6 minimum is also a multiple
of `1663175056640625`. Any smaller witness that is not refutes it.

And the reading that looked obvious — *the jump is small when the two witnesses
share a lot* — is **false**: the largest jump of all twenty-two consecutive pairs is
one where the previous term divides the next. `verify.py` recomputes that table.

## When the next one is smaller

Asking for a longer cycle usually costs more. Twice in the table it costs
**less**. The mechanism is a single local move on the cycle, and it is a theorem.

Take a witness of girth `k` whose digraph is the pure cycle
`q_1 -> ... -> q_k -> q_1`. Pick an edge `q_i -> q_{i+1}`, a prime `p` outside
the cycle and exponents `e'`, `a` such that `p | f(q_i^e')`, `q_{i+1} | f(p^a)`,
and **no chord appears** — no `q_j` other than `p` is hit by `q_i^e'`, no `q_j`
other than `q_{i+1}` is hit by `p^a`, and no other vertex hits `p`. Then

```
n' = n * q_i^(e'-e_i) * p^a
```

is a witness of **girth k+1**, so `m_f(k+1) <= m_f(k) * q_i^(e'-e_i) * p^a`.

The three chord conditions are not bookkeeping. Drop them and the same move on
the girth-5 minimum for `sigma` gives `1103602500`, whose girth is **2**.
`verify.py` pins that number.

**The certificate.** If the new stretch costs less than the exponent it saves —
`q_i^e' * p^a < q_i^e_i` — then `m_f(k+1) < m_f(k)`, **proved without computing
`m_f(k+1)`**. And it is decidable by a small finite search: the inequality forces
`e' < e_i`, so `e'` runs over `1 .. e_i-1`, `p` runs over the prime divisors of
`f(q_i^e')` — which the first condition already names, so the primes are never
enumerated — and `a` over `p^a < q_i^(e_i-e')`.

Over the **22** consecutive pairs in the table the certificate fires **exactly
twice**, which is exactly how often the sequence goes down, and both times it
hands back the next minimum on the nose:

| | `m_f(k)` | cut | insert | ratio | next minimum |
|---|---:|---|---|---:|---:|
| `sigma*`, 5→6 | 540765225 | `7^5 → 7^3` | `43` | `43/49` | 474549075 |
| `sigma**`, 5→6 | 10762773021 | `3^6 → 3^2` | `5^2` | `25/81` | 3321843525 |

```bash
python src/surgery.py "sigma*" 540765225 5
```

**One-directional, and that matters.** Finding no insertion below ratio 1 does
*not* prove the next minimum is bigger — it could come from an unrelated cycle.
That this never happens across the 22 pairs is measured, not proved.

**And the bonus, measured.** Even when the insertion is not cheaper, it still
exhibits a real witness of girth `k+1` — and an exhibited witness is exactly the
`N` the exhaustive search needs, which turns every doubling round into one round.
Both ways, on the two terms new here:

| | seedless | from the surgery bound | saved |
|---|---:|---:|---:|
| `sigma*`, girth 10 | 206680700 nodes, 1125 s, 42 rounds | 48321070 nodes, 252 s | **4.28x** |
| `sigma**`, girth 7 | 4266506 nodes, 23 s, 31 rounds | 930082 nodes, 5 s | **4.59x** |

That is the same factor of about 4 that version 3 measured as the price of not
knowing the answer. **It buys speed, not possibility**: the seedless search gets
there too.

## Splitting it across cores

Starting primes are independent -- each opens a tree that touches no other -- so
the search splits exactly. The only thing lost is shared pruning, and the
minimum cannot change: a process's bound is always at least the true minimum, so
the cutoff never drops anything below it.

    python src/parallel.py sigma 7 7746928876851256 --cores 8 --control

**4.54x** on eight cores there, with **identical** node counts and the same
answer; **4.13x** on `sigma*` girth 10, where the nodes grow 9.3% because the
bound is no longer shared. It does not reach eight -- the work is skewed and
each process sieves once -- and it does **not** move the wall of the previous
section, which is a memory wall that splitting makes worse.

Proof, discussion and limits: **[RESULT.md](RESULT.md)**.

## One thing worth seeing

Between girth 7 and girth 8 under `sigma`, the smallest witness grows by a factor
of only **4.09** — after growing by a factor of **43 005** in the step before.

```
sigma, girth 7:  3² · 5 · 7⁴ · 13 · 19 · 37 · 2801²
sigma, girth 8:  5³ · 7² · 13² · 19 · 31² · 61 · 83 · 331
```

With seven primes, no cheap cycle closes, and the minimum is **forced to use
2801²** — 7.8 million from that factor alone. With eight primes available, the
cycle closes using nothing above 331. **The extra vertex is nearly free, and it
buys its way out of the expensive prime.**

That matters beyond the curiosity: `ln n / k²` sits between 0.72 and 0.78 for
`k = 4, 5, 6, 7`, which invites reading `n ≈ exp(0.75 k²)` and predicts
`n₈ ≈ 7 × 10²⁰`. The true value is `3.2 × 10¹⁶`. **Four terms supported a law
and the fifth broke it.**

## What is in here

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | the full report: five theorems, proofs, tables, limits |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched for prior work, where and when |
| `verify.py` | one command, no dependencies |
| `src/arithmetic.py` | the definitions, in plain Python |
| `src/exact.py` | method 3: proves minimality, using the cutoff lemma |
| `src/construct.py` | method 2: builds witnesses from cycles over small primes |
| `src/sieve.py` | method 1: finds them by exhaustive search (needs numpy) |
| `src/make_terms.py` | regenerates `data/terms.json` by computation |
| `data/terms.json` | the terms with their factorizations, machine-readable |

There is also a Spanish walkthrough: [`README.es.md`](README.es.md).

## How it is checked

The three methods share no logic — the sieve knows nothing about cycles, the
construction never looks at an integer that is not built from one, and the exact
search accepts nothing without recomputing the girth from the integer itself.
They agree on every term more than one of them can reach.

And there is an external check: the sieve counts **5327** members of `S(sigma)`
below 10⁹ excluding `n = 1`. Pollack and Pomerance count **5328** including it.
They match exactly. That tests this code against a peer-reviewed result computed
by people who never saw it.

## What this does not claim

- **Not that it is new.** OEIS and four bibliographic databases were searched
  and returned nothing — with a positive control that does find the relevant
  papers. *Not found is not the same as new.* See [PRIOR_ART.md](PRIOR_ART.md).
- **Not that the sequences are infinite.** Whether a witness of every girth
  exists is untouched here.
- **Not minimality beyond the table.** There is no obstacle of principle left —
  the seedless search removes the need for a starting witness — but each further
  girth costs machine time, and only the girths actually computed are claimed.
- **Not that doubling is the best way to start.** It is the simplest one that
  keeps the proof intact; a best-first search would not repeat work.
- **Not that the growth has a law.** Section 8 of RESULT.md argues the opposite,
  and the new term adds to the case: `sigma*` grows by a factor of only **4.16**
  from girth 8 to girth 9.

## Citing

See [`CITATION.cff`](CITATION.cff). Licence: MIT for the code, CC BY 4.0 for
text and data.

## Author

**Jorge Ellena Godoy** — author and responsible for the correctness of
everything published here.

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by independent implementations and cross-checked
against published work. The author is responsible for the correctness of
everything published here.
