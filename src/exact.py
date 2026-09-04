"""Find the smallest witness of a given girth and *prove* it is the smallest.

The problem with the other method
---------------------------------

`construct.py` builds cycles from a fixed list of small primes and keeps the
cheapest. It says so honestly:

    "The answer is only minimal among the primes examined. A larger prime
     could in principle give a cheaper cycle."

That makes every value a conjecture verified as far as somebody looked. This
module removes the "as far as somebody looked".

The cutoff lemma
----------------

Let ``n`` be a smallest witness of girth ``k`` for ``f``. By the pure-cycle
theorem (see RESULT.md) ``n`` has exactly ``k`` distinct primes and its covering
digraph is the cycle ``q_1 -> q_2 -> ... -> q_k -> q_1``.

Let ``P`` be the largest of those primes and let ``q^e`` be the exact prime
power of its predecessor in the cycle. The edge exists, so ``P`` divides
``f(q^e)``, hence ``P <= f(q^e)``. From the closed forms:

    f = sigma    sigma(q^e) = (q^(e+1)-1)/(q-1) < 2 q^e   =>  q^e >= ceil(P/2)
    f = sigma*   sigma*(q^e) = q^e + 1                    =>  q^e >= P - 1
    f = phi*     phi*(q^e) = q^e - 1                      =>  q^e >= P + 1

Write ``a_f(P)`` for the right-hand column. Now split the product ``n`` into
three disjoint groups -- the power of ``P`` itself, the power of its predecessor,
and the remaining ``k-2`` prime powers, whose bases are distinct primes:

    n  >=  P * a_f(P) * primorial(k-2)                                     (*)

where ``primorial(j)`` is the product of the ``j`` smallest primes.

**What that buys.** If any witness ``N`` of girth ``k`` is known, the smallest
one is at most ``N``, so by (*) its largest prime satisfies

    P  <=  the largest P with  P * a_f(P) * primorial(k-2) < N

which is of the order of ``sqrt(N / primorial(k-2))``. Enumerating cycles over
the primes up to that bound is therefore *exhaustive*: what comes out is the
minimum, not the minimum of a sample.

The bound is computed by bisection over integers, never by a floating-point
square root. Rounding the wrong way would drop exactly the boundary case the
lemma exists to cover.

Exponents are searched too, not only the minimal one
----------------------------------------------------

`construct.py` picks, for each edge ``q -> p``, the *smallest* ``e`` with
``p | f(q^e)``, assembles ``n``, checks the girth, and if a chord appears it
discards the whole prime cycle.

That can lose witnesses. The edges leaving ``q`` depend on the exponent: raising
``e`` changes the entire out-neighbourhood of ``q`` and can *remove* the chord
that the minimal exponent created. Here the search runs over ``(prime,
exponent)`` pairs and requires the absence of chords **while building**:

  1. ``q_m`` divides ``f(q_{m-1}^{e_{m-1}})``          -- the edge exists;
  2. ``q_m`` divides no other ``f(q_i^{e_i})``          -- nothing else points to it;
  3. ``f(q_m^{e_m})`` is divisible by no prime already placed -- no edge backwards.

Any violation of 2 or 3 would close a directed cycle shorter than ``k``.

As it turned out, this did not change any published value: all thirteen were
reproduced digit for digit. That was not known before; now it is.

Usage
-----

    python src/exact.py sigma 6
    python src/exact.py sigma 2 3 4 5 6 7 8
    python src/exact.py "phi*" 5 --bound 1663175056640625
"""

import argparse
import time
import os
import random
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import f_of_prime_power, covering_digraph, girth  # noqa: E402

__all__ = ["exact_smallest", "prime_cutoff", "cycle_floor", "predecessor_floor"]

_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _is_prime(n):
    """Deterministic Miller-Rabin for n < 3.3e24."""
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _pollard(n):
    """A non-trivial factor of composite n."""
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n)
        x = random.randrange(0, n)
        y, d = x, 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = _gcd(abs(x - y), n)
        if d != n:
            return d


_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def _factor(n):
    """Full factorisation. Trial division by small primes, then Pollard rho.

    ``arithmetic.factorize`` is plain trial division, which is the right choice
    there -- it is the code a reader checks by eye. Here the numbers factored
    are ``f(q^e)`` for large ``q``, which reach 10^13 and beyond, so rho is
    needed. The two agree; ``verify.py`` checks that they do.
    """
    out = {}
    for p in _SMALL:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    if n == 1:
        return out
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if _is_prime(m):
            out[m] = out.get(m, 0) + 1
            continue
        d = _pollard(m)
        stack.append(d)
        stack.append(m // d)
    return out


def primes_up_to(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= n:
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
        i += 1
    return [i for i in range(2, n + 1) if sieve[i]]


_PRIMORIAL = None


def primorial(j):
    """Product of the j smallest primes. primorial(0) = 1."""
    global _PRIMORIAL
    if _PRIMORIAL is None:
        _PRIMORIAL = [1]
        acc = 1
        for p in primes_up_to(1000):
            acc *= p
            _PRIMORIAL.append(acc)
    return _PRIMORIAL[j]


def predecessor_floor(P, f):
    """Exact lower bound for q^e when the prime P divides f(q^e).

    Integers only, no floating point: see the module docstring.
    """
    if f == "sigma":
        return (P + 1) // 2
    if f == "sigma*":
        return P - 1
    if f == "phi*":
        return P + 1
    raise ValueError("unknown function: %r" % (f,))


def cycle_floor(P, k, f):
    """(*) Lower bound for n, for a k-cycle whose largest prime is P."""
    return P * predecessor_floor(P, f) * primorial(k - 2)


def prime_cutoff(bound, k, f):
    """The largest P that (*) still allows below `bound`.

    Every prime of a witness of girth k smaller than `bound` is at most this.
    Computed by bisection so the answer is exact.
    """
    lo, hi = 2, 4
    while cycle_floor(hi, k, f) < bound:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cycle_floor(mid, k, f) < bound:
            lo = mid
        else:
            hi = mid - 1
    return lo


#: Whether the per-arc cost lemma is applied on top of (*). A switch and not
#: an option, because its only legitimate use is to MEASURE: with False the
#: search must return exactly the same values and visit many more nodes. If it
#: returned different values, one of the two lemmas would be wrong.
PER_ARC_LEMMA = True


class _Search:
    """Enumerate pure k-cycles and keep the one of least product."""

    heartbeat = 0

    def __init__(self, f, k, prime_limit, bound):
        self.f = f
        self.k = k
        self.bound = bound              # best product known (exclusive)
        self.best = None
        self.primes = primes_up_to(prime_limit)
        self.prime_limit = prime_limit
        self._value = {}
        self._succ = {}
        self.nodes = 0
        self._small = self.primes[: k + 2]

    def value(self, q, e):
        v = self._value.get((q, e))
        if v is None:
            v = f_of_prime_power(q, e, self.f)
            self._value[(q, e)] = v
        return v

    def successors(self, q, budget):
        """(p, e, q^e) with q^e <= budget, p prime dividing f(q^e), p != q.

        Every exponent, not just the smallest per p. Computed on demand: for a
        large q, factoring f(q^e) for exponents the budget forbids is most of
        the work and buys nothing.
        """
        state = self._succ.get(q)
        if state is None:
            state = self._succ[q] = [[], 1, q]      # list, next e, next power
        items, e, power = state
        while power <= budget:
            for p in _factor(self.value(q, e)):
                if p != q and p <= self.prime_limit:
                    items.append((p, e, power))
            e += 1
            power *= q
            state[1], state[2] = e, power
        return [t for t in items if t[2] <= budget]

    def _floor(self, used, missing):
        """Lower bound on what the `missing` unplaced vertices contribute.

        Two bounds, the larger wins (per-arc cost lemma):

        1. **By the primes.** The missing vertices carry distinct primes, none
           of them used, so together they contribute at least the product of
           the `missing` smallest free primes.

        2. **By the closure.** While at least one vertex is unplaced, the one
           that CLOSES the cycle -- the predecessor of ``q_1`` -- is among
           them, and its prime power satisfies ``q^e >= a_f(q_1)`` because
           ``q_1 | f(q^e)``. The search always starts at the LARGEST prime, so
           ``q_1 = max(used)`` and that ``a_f`` is the largest available. The
           other ``missing - 1`` contribute at least the product of the
           ``missing - 1`` smallest free primes.

        The second dominates almost always: with ``q_1 ~ 1e6`` under sigma,
        ``a_f(q_1) ~ 5e5`` against a five-digit primorial.
        """
        free = []
        for x in self._small:
            if len(free) == missing:
                break
            if x not in used:
                free.append(x)
        by_primes = 1
        for x in free:
            by_primes *= x
        if missing < 1 or not PER_ARC_LEMMA:
            return by_primes
        by_closure = predecessor_floor(max(used), self.f)
        for x in free[:missing - 1]:
            by_closure *= x
        return max(by_primes, by_closure)

    def run(self):
        for i, start in enumerate(self.primes):
            if cycle_floor(start, self.k, self.f) >= self.bound:
                break
            self._from(start)
            if self.heartbeat and i % self.heartbeat == 0:
                print("    ... start %d of %d, best=%s, nodes=%d"
                      % (start, self.primes[-1],
                         self.best[0] if self.best else 0, self.nodes))
        return self.best

    def _from(self, start):
        # the k-1 remaining vertices contribute at least _floor()
        margin = max(1, self.bound // self._floor({start}, self.k - 1))
        for p, e, power in self.successors(start, margin):
            if p >= start:
                continue
            self._step([(start, e, power)], p, power, {start})

    def _step(self, path, nxt, product, used):
        self.nodes += 1
        m = len(path)
        if nxt in used or nxt >= path[0][0]:
            return
        for i in range(m - 1):                      # nothing else points to nxt
            if self.value(path[i][0], path[i][1]) % nxt == 0:
                return
        missing = self.k - m - 1
        floor = self._floor(used | {nxt}, missing)
        budget = self.bound // (product * floor)
        if budget <= 1:
            return
        closing = (m + 1 == self.k)
        # the closing vertex has to pay a_f(q_1): its prime power is what makes
        # q_1 | f(q^e). Same per-arc lemma, applied to the last vertex.
        least = (predecessor_floor(path[0][0], self.f)
                 if (closing and PER_ARC_LEMMA) else 1)
        for p, e, power in self.successors(nxt, budget):
            total = product * power
            if total >= self.bound:
                break
            if power < least:
                continue
            value = self.value(nxt, e)
            back = [x[0] for x in path if value % x[0] == 0]
            if closing:
                if p != path[0][0] or back != [path[0][0]]:
                    continue
                self._accept(path + [(nxt, e, power)], total)
                continue
            if back:                                # any edge backwards shortens
                continue
            self._step(path + [(nxt, e, power)], p, total, used | {nxt})

    def _accept(self, path, product):
        factors = {q: e for q, e, _ in path}
        if len(factors) != self.k:
            return
        # Independent girth computation, from the integer, before accepting.
        n = 1
        for q, e in factors.items():
            n *= q ** e
        if girth(covering_digraph(n, self.f)) != self.k:
            return
        if self.best is None or product < self.best[0]:
            self.best = (product, path)
            self.bound = product


def per_arc_floor(cycle, f):
    """(+) The per-arc lower bound for a pure cycle given as [(q, e), ...].

    ``n >= prod_i max(q_i, a_f(q_{i+1}))``, indices mod k. Strictly stronger
    than (*), which is what is left of it after keeping only the two factors
    that involve the largest prime.
    """
    k = len(cycle)
    out = 1
    for i, (q, _e) in enumerate(cycle):
        nxt = cycle[(i + 1) % k][0]
        out *= max(q, predecessor_floor(nxt, f))
    return out


def universal_floor(k, f):
    """(++) Lower bound for EVERY witness of girth k, knowing none of them.

    A witness of girth k has exactly k distinct primes (pure-cycle theorem),
    so its largest prime P satisfies ``P >= p_k``, the k-th prime; and
    ``cycle_floor`` is increasing in P. Hence

        n >= p_k * a_f(p_k) * primorial(k - 2)

    This is what lets the search start with **no seed at all**: it gives an N
    below which nothing exists.
    """
    p_k = primes_up_to(100 * (k + 3))[k - 1]
    return cycle_floor(p_k, k, f)


def _search_below(f, k, bound, heartbeat=0):
    """Exhaustive search for the smallest witness of girth k below `bound`.

    Returns ``(n, factorisation, cycle, prime_limit, nodes)`` or
    ``(None, nodes)`` if there is none. Exhaustive is the operative word: the
    cutoff lemma bounds the largest prime any witness below `bound` could use,
    so "nothing found" means "there is none", not "we did not look far enough".
    """
    limit = prime_cutoff(bound, k, f)
    search = _Search(f, k, limit, bound)
    search.heartbeat = heartbeat
    found = search.run()
    if found is None:
        return None, search.nodes
    product, path = found
    return (product, {q: e for q, e, _ in path},
            [q for q, _, _ in path], limit, search.nodes)


def exact_smallest(f, k, known_witness, heartbeat=0):
    """The smallest witness of girth k, proved.

    `known_witness` is any n in S(f) of girth k; it seeds the cutoff. Returns
    ``(n, factorisation, cycle, prime_limit_searched)``.

    If the search finds nothing below `known_witness`, then `known_witness`
    itself is the minimum -- it is attained, and nothing smaller exists.
    """
    out = _search_below(f, k, known_witness + 1, heartbeat)
    if out[0] is None:                               # cannot happen: the seed
        raise AssertionError("the seeding witness was not reachable")
    return out[:4]


def smallest_without_seed(f, k, heartbeat=0, trace=None):
    """The smallest witness of girth k, **with no known witness to start from**.

    The search of `exact_smallest` needs a witness N so that the cutoff lemma
    can bound the largest prime; without one the bound is infinite and the
    enumeration does not terminate. That kept the table pinned to the girths
    for which some element had already been exhibited.

    Doubling removes the need, and the proof was already in hand:

    - ``_search_below(f, k, N)`` is **exhaustive below N**. That is what the
      cutoff lemma bought: not "the best we saw" but "the smallest there is,
      if any is below N".
    - ``universal_floor(k, f)`` gives an N with nothing below it.
    - Run at that N; if nothing appears, double N. Since each round is
      exhaustive below its own bound, **the first value that appears is the
      minimum**: nothing smaller exists below this N, and nothing at all
      existed below the previous ones, which were already swept.

    No step is heuristic. The only difference from `exact_smallest` is where N
    comes from, and N does not enter the proof: it enters the running time.

    Returns ``(n, factorisation, cycle, prime_limit, nodes, rounds)``.
    """
    bound = universal_floor(k, f) + 1
    rounds, nodes = 0, 0
    while True:
        rounds += 1
        if trace is not None:
            trace(rounds, bound, prime_cutoff(bound, k, f))
        out = _search_below(f, k, bound, heartbeat)
        nodes += out[-1]
        if out[0] is not None:
            return out[0], out[1], out[2], out[3], nodes, rounds
        bound *= 2


KNOWN = {
    ("sigma", 2): 6, ("sigma", 3): 234, ("sigma", 4): 137214,
    ("sigma", 5): 275900625, ("sigma", 6): 180141399900,
    ("sigma", 7): 7746928876851255, ("sigma", 8): 31674203849435875,
    ("sigma*", 2): 6, ("sigma*", 3): 6615, ("sigma*", 4): 4380453,
    ("sigma*", 5): 540765225, ("sigma*", 6): 474549075,
    ("sigma*", 7): 4485174218525, ("sigma*", 8): 2386830845734335,
    ("sigma*", 9): 9928651387877145,
    ("phi*", 2): 12, ("phi*", 3): 66825, ("phi*", 4): 1120454775,
    ("phi*", 5): 1663175056640625,
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("function", choices=("sigma", "sigma*", "phi*"))
    parser.add_argument("girths", nargs="+", type=int)
    parser.add_argument("--bound", type=int, default=0,
                        help="a known witness of that girth, to seed the "
                             "cutoff (default: the published one)")
    parser.add_argument("--heartbeat", type=int, default=0,
                        help="print progress every N starting primes")
    parser.add_argument("--no-seed", action="store_true",
                        help="start from the universal floor and double, "
                             "using no known witness at all")
    parser.add_argument("--measure-lemma", action="store_true",
                        help="run each girth twice, with and without the "
                             "per-arc lemma, and compare the search trees")
    args = parser.parse_args(argv)

    if args.measure_lemma:
        global PER_ARC_LEMMA
        print("%-8s %2s | %14s %7s | %14s %7s | %6s | same"
              % ("f", "k", "nodes with (*)", "sec", "nodes with (+)", "sec",
                 "saved"))
        for k in args.girths:
            seed = args.bound or KNOWN.get((args.function, k))
            if not seed:
                print("girth %d: not in the control table" % k)
                continue
            row = []
            for flag in (False, True):
                PER_ARC_LEMMA = flag
                started = time.time()
                out = _search_below(args.function, k, seed + 1)
                row.append((out[0], out[-1], time.time() - started))
            PER_ARC_LEMMA = True
            print("%-8s %2d | %14d %7.2f | %14d %7.2f | %5.1fx | %s"
                  % (args.function, k, row[0][1], row[0][2],
                     row[1][1], row[1][2], row[0][1] / max(1, row[1][1]),
                     "yes" if row[0][0] == row[1][0] == seed else "NO"))
        return 0

    if args.no_seed:
        for k in args.girths:
            print(chr(10) + "=== %s, girth %d (no seed) ===" % (args.function, k))

            def trace(rounds, bound, cutoff, k=k):
                print("  round %d: N = %d (primes <= %d)"
                      % (rounds, bound, cutoff), flush=True)

            started = time.time()
            n, factors, cycle, limit, nodes, rounds = smallest_without_seed(
                args.function, k, args.heartbeat, trace)
            shown = " * ".join("%d^%d" % (q, e) if e > 1 else str(q)
                               for q, e in sorted(factors.items()))
            print("  MINIMUM n = %d   (%d rounds, %d nodes, %.0fs)"
                  % (n, rounds, nodes, time.time() - started))
            print("  factorisation  %s" % shown)
            print("  cycle          %s"
                  % " -> ".join(str(q) for q in cycle + [cycle[0]]))
            print("  searched every prime up to %d" % limit)
            published = KNOWN.get((args.function, k))
            if published is None:
                print("  *** NEW: no witness of this girth was published ***")
            elif published == n:
                print("  == equals the published value, found without using it")
            else:
                print("  != DISAGREES with the published %d" % published)
        return 0

    for k in args.girths:
        seed = args.bound or KNOWN.get((args.function, k))
        if not seed:
            print("girth %d: no known witness to seed the cutoff" % k)
            continue
        print("\n=== %s, girth %d ===" % (args.function, k))
        print("  seed witness N = %d" % seed)
        print("  cutoff lemma: every prime of the cycle is <= %d"
              % prime_cutoff(seed + 1, k, args.function))
        n, factors, cycle, limit = exact_smallest(args.function, k, seed,
                                                  args.heartbeat)
        shown = " * ".join("%d^%d" % (q, e) if e > 1 else str(q)
                           for q, e in sorted(factors.items()))
        print("  MINIMUM n = %d" % n)
        print("  factorisation  %s" % shown)
        print("  cycle          %s"
              % " -> ".join(str(q) for q in cycle + [cycle[0]]))
        print("  searched every prime up to %d" % limit)
        if n == seed:
            print("  == equals the published value, now proved minimal")
        else:
            print("  != the published value was %d" % seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
