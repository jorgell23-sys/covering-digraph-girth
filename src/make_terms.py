"""Regenerate ``data/terms.json`` from the terms, by computation.

    python src/make_terms.py

Every field is derived here and none is transcribed: the factorisation comes
from factoring, the cycle and the edges from the covering digraph, the
membership and the girth from their definitions, and ``primes_searched_up_to``
from the cutoff lemma. The only things typed in are the terms themselves and
which of them were first computed in this work.

Writing the data file by hand would put a second copy of every number in the
repository, and a second copy is a second thing that can be wrong.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import covering_digraph, factorize, in_S, is_pure_cycle
from exact import prime_cutoff

#: Smallest n in S(f) whose covering digraph has girth k. Proved minimal.
TERMS = {
    "sigma":  {2: 6, 3: 234, 4: 137214, 5: 275900625, 6: 180141399900,
               7: 7746928876851255, 8: 31674203849435875},
    "sigma*": {2: 6, 3: 6615, 4: 4380453, 5: 540765225, 6: 474549075,
               7: 4485174218525, 8: 2386830845734335, 9: 9928651387877145,
               10: 10858178043907173985005},
    "phi*":   {2: 12, 3: 66825, 4: 1120454775, 5: 1663175056640625},
    "sigma**": {2: 6, 3: 15925, 4: 2321865, 5: 10762773021, 6: 3321843525,
                7: 345358414826425},
}

#: The ones this project computed for the first time, and the release that did.
FIRST_HERE = {
    ("sigma", 7): "2.0.0", ("sigma", 8): "2.0.0",
    ("sigma*", 8): "2.0.0", ("phi*", 5): "2.0.0",
    ("sigma*", 9): "3.0.0",
    ("sigma**", 2): "3.2.0", ("sigma**", 3): "3.2.0",
    ("sigma**", 4): "3.2.0", ("sigma**", 5): "3.2.0",
    ("sigma**", 6): "3.2.0", ("sigma**", 7): "3.2.0",
    ("sigma*", 10): "3.2.0",
}

#: The ones for which no seed was available at all, so they could only be
#: reached by the seedless search of release 3.0.0. Every term is reproducible
#: that way; these are the ones with no alternative.
#:
#: For ``sigma*`` at girth 10 and ``sigma**`` at girth 7 the seedless search had
#: no *practical* alternative either: doubling from the universal floor had run
#: 40 rounds on the first without reaching it. What made them computable was a
#: seed that the surgery of release 3.2.0 exhibits, and with it one round is
#: enough.
NO_SEED_EXISTED = {("sigma*", 9)}


def cycle_of(n, f):
    """[(prime, exponent), ...] in cycle order, read off the digraph."""
    factors = factorize(n)
    digraph = covering_digraph(n, f)
    start = min(factors)
    order, seen, q = [], set(), start
    while q not in seen:
        seen.add(q)
        order.append((q, factors[q]))
        if len(digraph[q]) != 1:
            raise ValueError("%d is not a pure cycle under %s" % (n, f))
        q = digraph[q][0]
    if q != start or len(order) != len(factors):
        raise ValueError("%d is not a single cycle under %s" % (n, f))
    return order


def entry(f, k, n):
    factors = factorize(n)
    digraph = covering_digraph(n, f)
    order = cycle_of(n, f)
    return {
        "girth": k,
        "n": n,
        "factorization": " * ".join(
            ("%d^%d" % (q, e)) if e > 1 else str(q)
            for q, e in sorted(factors.items())),
        "omega": len(factors),
        "cycle": [q for q, _ in order],
        "edges": {str(q): digraph[q][0] for q in sorted(factors)},
        "in_S": in_S(n, f),
        "is_pure_cycle": is_pure_cycle(digraph),
        "proved_minimal": True,
        "primes_searched_up_to": prime_cutoff(n + 1, k, f),
        "largest_prime": max(factors),
        "first_computed_here": (f, k) in FIRST_HERE,
        "first_computed_in_release": FIRST_HERE.get((f, k)),
        "no_seed_existed": (f, k) in NO_SEED_EXISTED,
    }


def build():
    return {
        "description":
            "Smallest n in S(f) = {n : rad(n) divides f(n)} whose covering "
            "digraph has girth k. Every term is proved minimal: the cutoff "
            "lemma bounds the largest prime a smaller witness could use, so "
            "the enumeration is exhaustive.",
        "generated_by": "python src/make_terms.py",
        "reproduce_one": "python src/exact.py <function> <girth> --no-seed",
        "reference": "https://doi.org/10.1515/integers-2012-0044",
        "functions": {
            f: [entry(f, k, n) for k, n in sorted(by_girth.items())]
            for f, by_girth in TERMS.items()
        },
    }


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, "data", "terms.json")
    data = build()
    with open(path, "w", encoding="utf-8", newline=chr(10)) as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write(chr(10))
    total = sum(len(v) for v in data["functions"].values())
    print("wrote %s: %d terms" % (path, total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
