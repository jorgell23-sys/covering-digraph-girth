"""Build the smallest witness of a given girth, without sieving.

Why this works
--------------

The theorem in RESULT.md says: if any n in S(f) has girth k, then the smallest
such n has exactly k distinct prime factors and its covering digraph is a pure
directed cycle of length k.

That turns the search into a different problem. Sieving for a witness of girth 6
under sigma would mean scanning integers up to roughly 10^13 -- the counts per
girth fall by a factor that keeps growing (3.9, then 8.7, then 61), so witnesses
of high girth are astronomically rare. But if the smallest one *is* a pure
k-cycle on k primes, it is enough to build k-cycles out of small primes and keep
the cheapest product. The bound stops being the size of n and becomes how many
primes we look at.

How
---

For each ordered pair of primes (q, p) we find the smallest exponent e with
p dividing f(q^e). That exponent is the cost of the edge q -> p, because it
contributes q^e to the product. Then we search for the k-cycle of least product,
depth first, pruning a branch as soon as its partial product reaches the best
complete cycle found so far.

Two things this code checks, and why
------------------------------------

1. **Building the cycle is not enough: the girth must be verified.** The theorem
   says the minimal witness *is* a pure k-cycle; it does not say that every n
   built on a k-cycle has girth k. Choosing the smallest exponent per edge can
   create *extra* edges among the same primes, and those chords shorten the
   cycle. The first version of this program proposed n = 120 = 2^3 * 3 * 5 as
   the smallest witness of girth 3 under sigma, on the cycle 2 -> 5 -> 3 -> 2 --
   and the true girth of 120 is 2. So each candidate is checked with an
   independent girth computation before being accepted.

2. **The answer is only minimal among the primes examined.** A larger prime
   could in principle give a cheaper cycle. The program reports how far it
   looked, and the published values were confirmed stable at two different
   bounds.

Usage:

    python src/construct.py sigma 6
    python src/construct.py sigma 6 --primes 26
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import FUNCTIONS, covering_digraph, f_of_prime_power, girth

#: How far up we look for the exponent that realizes an edge. The published
#: witnesses use exponents at most 11; we look well past that so the limit is
#: not silently doing the cutting.
MAX_EXPONENT = 24


def first_primes(count):
    """The first `count` primes, by a plain sieve of Eratosthenes."""
    if count < 1:
        return []
    # Upper bound for the n-th prime (n >= 6): n(ln n + ln ln n). Padded.
    import math
    if count < 6:
        limit = 15
    else:
        limit = int(count * (math.log(count) + math.log(math.log(count)))) + 10
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    return primes[:count]


def edge_cost(q, p, f, max_exponent=MAX_EXPONENT):
    """Smallest e >= 1 with p dividing f(q^e), or 0 if there is none in range."""
    for e in range(1, max_exponent + 1):
        if f_of_prime_power(q, e, f) % p == 0:
            return e
    return 0


def smallest_witness(f, k, n_primes=20, max_exponent=MAX_EXPONENT):
    """Smallest n of girth k built from the first `n_primes` primes.

    Returns (n, cycle, largest_prime_examined). n is None if no k-cycle exists
    within that set of primes -- which does not mean none exists at all.
    """
    if k < 2:
        raise ValueError("girth must be at least 2")
    primes = first_primes(n_primes)

    # cost[q][p] = smallest exponent of q realizing the edge q -> p
    cost = {}
    for q in primes:
        cost[q] = {}
        for p in primes:
            if p == q:
                continue
            e = edge_cost(q, p, f, max_exponent)
            if e:
                cost[q][p] = e

    best = [None, None]  # [value, cycle]

    def descend(cycle, partial):
        if len(cycle) == k:
            e = cost[cycle[-1]].get(cycle[0])
            if not e:
                return
            total = partial * cycle[-1] ** e
            if best[0] is not None and total >= best[0]:
                return
            # See the module docstring, point 1: the girth must be verified.
            if girth(covering_digraph(total, f)) == k:
                best[0], best[1] = total, tuple(cycle)
            return
        for p in primes:
            # Start each cycle at its smallest prime, so every cycle is
            # considered once instead of k times.
            if p in cycle or p < cycle[0]:
                continue
            e = cost[cycle[-1]].get(p)
            if not e:
                continue
            # The edge's cost is paid by the vertex it leaves from, so the
            # partial product does not yet include the last prime: its exponent
            # depends on where it will point, which is not known yet.
            step = partial * cycle[-1] ** e
            if best[0] is not None and step >= best[0]:
                continue
            cycle.append(p)
            descend(cycle, step)
            cycle.pop()

    for start in primes:
        descend([start], 1)

    return best[0], best[1], (primes[-1] if primes else 0)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build the smallest witness of a given girth.")
    parser.add_argument("function", choices=list(FUNCTIONS))
    parser.add_argument("girth", type=int)
    parser.add_argument("--primes", type=int, default=20,
                        help="how many small primes to examine (default 20)")
    args = parser.parse_args(argv)

    n, cycle, largest = smallest_witness(args.function, args.girth, args.primes)
    print("f = %s, girth %d, examining the first %d primes (up to %d)"
          % (args.function, args.girth, args.primes, largest))
    if n is None:
        print("  no %d-cycle within those primes." % args.girth)
        print("  This does not decide anything: a larger prime set may contain one.")
        return 0

    parts = []
    for i, q in enumerate(cycle):
        p = cycle[(i + 1) % args.girth]
        e = edge_cost(q, p, args.function)
        parts.append("%d^%d" % (q, e) if e > 1 else str(q))
    print("  smallest n = %d" % n)
    print("             = %s" % " * ".join(parts))
    print("  cycle      = %s -> %d"
          % (" -> ".join(str(x) for x in cycle), cycle[0]))
    print("  girth of n = %d (verified independently)"
          % girth(covering_digraph(n, args.function)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
