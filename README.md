# Smallest witnesses by girth for rad(n) | f(n)

Three integers that had not been computed before, and a small theorem that makes
computing them possible.

**Everything here is verifiable in two seconds:**

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

No dependencies, no setup. It prints PASS or FAIL for each of 56 checks.

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
| 4 | 137214 | 4380453 | **1120454775** |
| 5 | 275900625 | 540765225 | — |
| 6 | **180141399900** | 474549075 | — |
| 7 | — | **4485174218525** | — |

The three in bold were out of reach of any search by enumeration. The last is
about 4.5 × 10¹².

## Why they were out of reach, and how they were found

Witnesses of high girth are vanishingly rare. Below 10⁹ under `sigma` there are
4138 of girth 2, 1065 of girth 3, 122 of girth 4 — and **2** of girth 5. The
counts fall by a factor that keeps growing. Finding one of girth 6 by scanning
integers would require going to roughly **10¹³**.

The way out is a small theorem:

> If any `n` has girth `k`, the **smallest** such `n` has exactly `k` distinct
> prime factors, and its graph is a pure directed cycle of length `k`.

So instead of scanning integers, one builds cycles out of small primes and keeps
the cheapest. The problem stops being about the size of `n` and becomes about
how many primes to consider.

Proof, discussion and limits: **[RESULT.md](RESULT.md)**.

## One thing worth seeing

Under `sigma*` the sequence of minima **goes down** once:

```
6,  6615,  4380453,  540765225,  474549075,  4485174218525
                          ↑ smaller than the previous one
```

The two numbers involved share the skeleton `3² × 5² × 11 × 13`, and differ in a
single factor:

| | factor | value |
|---|---|---:|
| girth 6 | `7³ × 43` | **14749** |
| girth 5 | `7⁵` | 16807 |

Closing the 5-cycle forces `7⁵`. Extending to a 6-cycle lets a new prime (43) in,
**and that allows the exponent to drop to `7³`**. Adding a vertex came out
cheaper than raising an exponent.

It happens exactly once among all known terms — it is an accident of that
particular prime, not a property of the function.

## What is in here

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | the full report: theorem, proof, tables, limits |
| [`PRIOR_ART.md`](PRIOR_ART.md) | what was searched for prior work, where and when |
| `verify.py` | one command, 56 checks, no dependencies |
| `src/arithmetic.py` | the definitions, in plain Python |
| `src/construct.py` | method 2: builds the witnesses from cycles |
| `src/sieve.py` | method 1: finds them by exhaustive search (needs numpy) |
| `data/terms.json` | the terms with their factorizations, machine-readable |

There is also a Spanish walkthrough: [`README.es.md`](README.es.md).

## How it is checked

The two methods share no logic — the sieve knows nothing about cycles, the
construction never looks at an integer that is not built from one — and they
agree on every term both can reach.

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
- **Not that it is interesting.** That is for a reader to judge.

## Citing

See [`CITATION.cff`](CITATION.cff), or use the "Cite this repository" button.

## Author

**Jorge Ellena Godoy**, who is responsible for the correctness of everything
here.

## How this was produced

The system design and research direction are the author's. The mathematical
results were produced by an automated system (Claude, Anthropic) under that
direction. All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything here.

## License

Code under [MIT](LICENSE); text and data under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
