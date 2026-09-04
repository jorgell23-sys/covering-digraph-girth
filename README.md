# Smallest witnesses by girth for rad(n) | f(n)

Nineteen integers, each **proved** to be the smallest of its kind — five of
them never computed before — and the small theorems that make proving it
possible **without knowing any answer in advance**.

**Everything here is verifiable in two seconds:**

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

No dependencies, no setup. It runs 220 checks and prints PASS or FAIL for each.

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

| girth | `sigma` | `sigma*` | `phi*` |
|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 |
| 3 | 234 | 6615 | 66825 |
| 4 | 137214 | 4380453 | 1120454775 |
| 5 | 275900625 | 540765225 | **1663175056640625** |
| 6 | 180141399900 | 474549075 | |
| 7 | **7746928876851255** | 4485174218525 | |
| 8 | **31674203849435875** | **2386830845734335** | |
| 9 | | **9928651387877145** | |

The five in bold had not been computed before, and **all nineteen are proved
minimal**. The last one is the interesting case: no witness of girth 9 was known
for `sigma*`, so version 2 could not have computed it at all. Version 3 removes
the need to know one.

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
`phi*` at girth 6 and found nothing — those are theorems. The constructor
exhibits witnesses at `8.3e24` and `4.2e22` — those are verified, but not
minimal. So both terms are **bracketed**, and closing the bracket would mean
sieving **5.7 billion** and **14 billion** primes respectively. That does not fit
in memory.

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
share a lot* — is **false**: the largest jump of all sixteen consecutive pairs is
one where the previous term divides the next. `verify.py` recomputes that table.

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
