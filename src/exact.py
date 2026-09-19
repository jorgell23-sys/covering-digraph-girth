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

import re as _re

#: same shape as in arithmetic.py
_NAME = _re.compile(r"(sigma|phi)(\*?)(\d*)")

import argparse
import time
import os
import random
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import (FUNCTIONS, f_of_prime_power, covering_digraph,  # noqa: E402
                        girth)
from covering_cost import (CoveringCost, SizeFloor,  # noqa: E402
                           factor as _factor, is_prime as _is_prime)

__all__ = ["exact_smallest", "prime_cutoff", "cycle_floor", "predecessor_floor",
           "Cutoff", "cutoff_for", "smallest_without_seed"]

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

    Integers only, no floating point: see the module docstring. This is the
    published closed form; `Cutoff` below is the general version.
    """
    if f == "sigma":
        return (P + 1) // 2
    if f == "sigma*":
        return P - 1
    if f == "phi*":
        return P + 1
    if f == "sigma**":
        # sigma**(q^e) <= sigma(q^e) < 2 q^e, exactly as for sigma, because the
        # biunitary divisors of q^e are a subset of its divisors. So the same
        # bound holds, and it is valid without any further hypothesis.
        return (P + 1) // 2
    # The parametric families, added in 3.3.0. With a = q^s,
    #
    #     sigma_s(q^e)  = (q^(s(e+1)) - 1)/(q^s - 1) < 2 q^(se)  =>  a > P/2
    #     sigma*_s(q^e) = q^(se) + 1                             =>  a >= P - 1
    #     phi*_s(q^e)   = q^(se) - 1                             =>  a >= P + 1
    #
    # and q^e is the s-th root of a, rounded up. Integer arithmetic throughout:
    # a float at the boundary could drop a legitimate witness, which is exactly
    # what this lemma exists to prevent.
    m = _NAME.fullmatch(f)
    if m is None:
        raise ValueError("unknown function: %r" % (f,))
    base, star, suffix = m.group(1), bool(m.group(2)), m.group(3)
    if base == "phi" and not star:
        raise ValueError("unknown function: %r" % (f,))
    s = int(suffix) if suffix else 1
    if star:
        target = P - 1 if base == "sigma" else P + 1
    else:
        target = (P + 1) // 2
    return _integer_root_up(target, s)


def _integer_root_up(x, s):
    """The least integer r with r^s >= x. Integers only."""
    if x <= 1:
        return 1
    r = int(round(x ** (1.0 / s)))
    while r ** s < x:
        r += 1
    while r > 1 and (r - 1) ** s >= x:
        r -= 1
    return r


def has_published_floor(f):
    """Whether `predecessor_floor` has a closed form for f (releases 2 and 3.3.0)."""
    try:
        predecessor_floor(3, f)
    except ValueError:
        return False
    return True


class Cutoff:
    """The lower bounds on a covering prime power, in their three modes.

    All three are valid; each dominates the one before it.

    - ``published`` -- the closed forms of `predecessor_floor`: version 2 for
      sigma, sigma* and phi*, and release 3.3.0 for sigma** and the families.
    - ``size`` -- ``a_f(P) = min{ m a prime power : f(m) >= P }``. Valid for
      **every** multiplicative f with no hypothesis whatever, and at least as
      large as the published form, since it also demands that m be a prime
      power.
    - ``exact`` -- ``max(size, A_f(P))`` with ``A_f(P) = min{ m a prime power,
      base != P : P divides f(m) }``, sieved to M and truncated at M + 1.

    **`a` is monotone and `A` is not.** `a` is the one that may cut short a walk
    ordered by P -- the bisection of the cutoff, the `break` over starting
    primes, the universal floor. `A` may only discard one particular prime and
    lower the floor of one particular node. Mixing them up yields a search that
    skips legitimate witnesses and returns a wrong minimum without failing.
    """

    def __init__(self, f, mode="auto", M=0, prime_limit=0, verbose=False):
        self.f = f
        if mode == "auto":
            mode = "published" if has_published_floor(f) else "size"
        if mode == "published" and not has_published_floor(f):
            raise ValueError("no published closed form for %r" % (f,))
        self.mode = mode
        self._size = SizeFloor(f)
        self._exact = None
        self.exact_prime_limit = 0
        if mode == "exact":
            if M <= 0 or prime_limit <= 0:
                raise ValueError("exact mode needs M and prime_limit")
            self._exact = CoveringCost(f, M, prime_limit, verbose=verbose)
            self.exact_prime_limit = prime_limit

    def a(self, P):
        """The MONOTONE bound. The only one that may cut short a walk."""
        if self.mode == "published":
            return predecessor_floor(P, self.f)
        return self._size(P)

    def A(self, P):
        """The best bound for this P. NOT monotone in P."""
        base = self.a(P)
        if self._exact is None:
            return base
        return max(base, self._exact(P))

    def monotone_floor(self, P, k):
        """(*) with the monotone bound: increases with P, so it may cut."""
        return P * self.a(P) * primorial(k - 2)

    def floor(self, P, k):
        """(*) with the best bound. Discards this P; never cuts the walk."""
        return P * self.A(P) * primorial(k - 2)

    def prime_cutoff(self, bound, k):
        lo, hi = 2, 4
        while self.monotone_floor(hi, k) < bound:
            hi *= 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.monotone_floor(mid, k) < bound:
                lo = mid
            else:
                hi = mid - 1
        return lo


def cycle_floor(P, k, f):
    """(*) Lower bound for n, for a k-cycle whose largest prime is P."""
    return Cutoff(f).monotone_floor(P, k)


def prime_cutoff(bound, k, f):
    """The largest P that (*) still allows below `bound`.

    Every prime of a witness of girth k smaller than `bound` is at most this.
    Computed by bisection so the answer is exact.
    """
    return Cutoff(f).prime_cutoff(bound, k)


#: How much deeper than the prime cutoff the covering cost is sieved. The
#: filter ``P * A_f(P) * primorial(k-2) < N`` can only exclude primes above
#: ``N / (primorial * M)``, so with M equal to the cutoff it excludes nobody:
#: the sieve has to go DEEPER than the cutoff to be worth anything.
SIEVE_DEPTH = 20


def cutoff_for(f, k, bound, mode="auto", M=0, verbose=False):
    """The `Cutoff` that goes with a bound N, sieving whatever it takes."""
    if mode != "exact":
        return Cutoff(f, mode=mode)
    base = Cutoff(f, mode="published" if has_published_floor(f) else "size")
    limit = base.prime_cutoff(bound, k)
    return Cutoff(f, mode="exact", M=(M if M > 0 else max(1000, SIEVE_DEPTH * limit)),
                  prime_limit=limit, verbose=verbose)


#: Whether the per-arc cost lemma is applied on top of (*). A switch and not
#: an option, because its only legitimate use is to MEASURE: with False the
#: search must return exactly the same values and visit many more nodes. If it
#: returned different values, one of the two lemmas would be wrong.
PER_ARC_LEMMA = True


class _Search:
    """Enumerate pure k-cycles and keep the one of least product."""

    heartbeat = 0

    def __init__(self, f, k, prime_limit, bound, cutoff=None):
        self.f = f
        self.cutoff = cutoff if cutoff is not None else Cutoff(f)
        self.discarded = 0            # starting primes that A_f ruled out
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
        by_closure = self.cutoff.A(max(used))
        for x in free[:missing - 1]:
            by_closure *= x
        return max(by_primes, by_closure)

    def run(self):
        for i, start in enumerate(self.primes):
            # the `break` goes with the MONOTONE bound: it is the only one
            # that guarantees every later prime is out too.
            if self.cutoff.monotone_floor(start, self.k) >= self.bound:
                break
            # the pointwise discard goes with the best bound, which is not
            # monotone -- hence `continue` and not `break`.
            if self.cutoff.floor(start, self.k) >= self.bound:
                self.discarded += 1
                continue
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
        least = (self.cutoff.A(path[0][0])
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
    # with the MONOTONE bound: the argument is "P >= p_k and the floor grows
    # with P", and A_f does not grow with P, so it is of no use here.
    return Cutoff(f, mode="published" if has_published_floor(f) else "size"
                  ).monotone_floor(p_k, k)


def _search_below(f, k, bound, heartbeat=0, cutoff=None):
    """Exhaustive search for the smallest witness of girth k below `bound`.

    Returns ``(n, factorisation, cycle, prime_limit, nodes)`` or
    ``(None, nodes)`` if there is none. Exhaustive is the operative word: the
    cutoff lemma bounds the largest prime any witness below `bound` could use,
    so "nothing found" means "there is none", not "we did not look far enough".
    """
    cutoff = cutoff if cutoff is not None else Cutoff(f)
    limit = cutoff.prime_cutoff(bound, k)
    search = _Search(f, k, limit, bound, cutoff=cutoff)
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


def smallest_without_seed(f, k, heartbeat=0, trace=None, mode="auto", M=0,
                          cap=0):
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
    cutoff = None
    while True:
        rounds += 1
        if cutoff is None or mode != "exact" or                 cutoff.prime_cutoff(bound, k) > cutoff.exact_prime_limit:
            cutoff = cutoff_for(f, k, bound, mode, M)
        if trace is not None:
            trace(rounds, bound, cutoff.prime_cutoff(bound, k))
        out = _search_below(f, k, bound, heartbeat, cutoff=cutoff)
        nodes += out[-1]
        if out[0] is not None:
            return out[0], out[1], out[2], out[3], nodes, rounds
        if cap and bound >= cap:
            # Not a failure and not an exhausted heuristic: the search WAS
            # exhaustive below `bound`, so what is known is a PROVED LOWER
            # BOUND -- there is no witness of girth k below this number. It is
            # returned as such rather than as a bare None, because a None that
            # can mean either "there is none" or "we did not look far enough"
            # is exactly the datum that is of no use.
            return None, None, None, bound, nodes, rounds
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
    parser.add_argument("function", choices=list(FUNCTIONS))
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
    parser.add_argument("--mode", default="auto",
                        choices=("auto", "published", "size", "exact"),
                        help="which lower bound on the covering prime power to "
                             "use (default: the published closed form where "
                             "there is one, the generic size bound otherwise)")
    parser.add_argument("--sieve", type=int, default=0,
                        help="how far to sieve the covering cost in --mode "
                             "exact (default: 20 times the prime cutoff)")
    parser.add_argument("--cap", type=float, default=0,
                        help="stop doubling at this bound and report the proved "
                             "lower bound instead of running forever")
    parser.add_argument("--measure-cutoff", action="store_true",
                        help="run each girth under all three bounds and compare "
                             "values, cutoffs and search trees")
    args = parser.parse_args(argv)

    if args.measure_cutoff:
        print("%-9s %2s | %-10s %10s %13s %8s | value"
              % ("f", "k", "mode", "cutoff P", "nodes", "sec"))
        for k in args.girths:
            seed = args.bound or KNOWN.get((args.function, k))
            if not seed:
                print("girth %d: not in the control table" % k)
                continue
            for mode in ("published", "size", "exact"):
                if mode == "published" and not has_published_floor(args.function):
                    continue
                cut = cutoff_for(args.function, k, seed + 1, mode, args.sieve)
                started = time.time()
                out = _search_below(args.function, k, seed + 1, cutoff=cut)
                print("%-9s %2d | %-10s %10d %13d %8.2f | %s"
                      % (args.function, k, mode, cut.prime_cutoff(seed + 1, k),
                         out[-1], time.time() - started,
                         "ok" if out[0] == seed else "DISAGREES %d" % out[0]))
        return 0

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
                args.function, k, args.heartbeat, trace, mode=args.mode,
                M=args.sieve, cap=int(args.cap))
            if n is None:
                print("  NO WITNESS below %d -- proved lower bound "
                      "(%d rounds, %d nodes)" % (limit, rounds, nodes))
                continue
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
