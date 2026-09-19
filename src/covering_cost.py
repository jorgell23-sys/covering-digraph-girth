"""The two lower bounds on a covering prime power. Pure Python, no dependencies.

Versions 1 to 3 of this repository stated the cutoff lemma (*) for the three
functions sigma, sigma* and phi*, and said it held *because those three have a
closed form on prime powers from which q^e >= a_f(P) can be read off*. That
made the machinery look like a property of those three functions.

It is not, and the reason is one line: **on a prime power m = q^e, the q and
the e are determined by m**, so f restricted to the prime powers is a function
of a single argument. Two lower bounds follow, both valid for every
multiplicative f:

    a_f(P) = min { m a prime power : f(m) >= P }                (by SIZE)
    A_f(P) = min { m a prime power, base != P : P divides f(m) } (EXACT)

The first needs no hypothesis at all -- no growth condition, no monotonicity,
no closed form. If P divides f(m) and f(m) >= 1, then f(m) >= P, so m is in the
set and is at least its minimum. It is non-decreasing in P, which is what the
bisection in the cutoff needs. The three closed forms -- ceil(P/2), P-1, P+1 --
are the special case where that minimum has a formula, and the generic minimum
is at least as good as all three, because it also demands that m be a prime
power: for sigma and P = 11 the formula gives 6 and the generic minimum gives 8.

The second keeps the divisibility instead of throwing it away, so it is
strictly stronger. It has no formula; it is **sieved**. Walk the prime powers
m <= M in increasing order, factor f(m), and let every prime P that appears keep
the first m that produced it, which by the ordering is the least. Primes that
never appear have A_f(P) > M, and M + 1 is then a valid bound for them -- in
practice that is the one that excludes the most.

For sigma, over the 1229 primes below 10^4 and sieving prime powers to 10^5,
the ratio A_f(P) / a_f(P) has median 10.5 and mean 12.6. The bound that was
being used was ten times slacker than the same data allowed.

THE TRAP, stated here because it costs a false theorem and gives no symptom
-----------------------------------------------------------------------------
`a_f` is non-decreasing and `A_f` is **not**: A_sigma(11) = 43 while
A_sigma(13) = 9. So `A_f` may be used to discard one particular prime, and to
lower the floor of one particular node, but **never to cut short a walk ordered
by P** -- a `break` claims that every later P is out too, and that claim is
false. The monotone cutoff stays with `a_f`. A search that mixes them up
returns a wrong minimum without ever failing.

    python src/covering_cost.py sigma 100000 10000
"""

import random
import sys
from math import gcd as _gcd_lucas, isqrt as _isqrt
from bisect import bisect_left
from os.path import abspath, dirname

sys.path.insert(0, dirname(abspath(__file__)))

from arithmetic import FUNCTIONS, f_of_prime_power  # noqa: E402

__all__ = ["primes_up_to", "prime_powers_up_to", "SizeFloor", "covering_cost",
           "CoveringCost", "factor", "is_prime"]


# Until version 3.3.3 this was "deterministic Miller-Rabin for n < 3.3e24"
# with the twelve bases 2..37. Twelve bases decide primality only below
# psi_12 = 318665857834031151167461, which is composite and passes all twelve;
# 3.3e24 is psi_13 and needs the base 41 as well (Sorenson and Webster, 2015).
# Above psi_13 no set of bases is known to suffice, so the strong Lucas test is
# added: Miller-Rabin to base 2 plus strong Lucas is BPSW, with no known
# counterexample -- which is not a proof, and is said so. No published number
# depended on it: RESULT.md, "What changed in version 3.3.4".
_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)

#: psi_13: the smallest strong pseudoprime to the first thirteen prime bases.
#: Below it, Miller-Rabin with _BASES decides primality without error.
_PROVEN_BELOW = 3317044064679887385961981


def _jacobi(a, n):
    """The Jacobi symbol (a/n), for odd n > 0."""
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def _half(x, n):
    """x / 2 modulo odd n."""
    if x % 2:
        x += n
    return (x // 2) % n


def _strong_lucas(n):
    """Strong Lucas probable-prime test, Selfridge's parameters (method A).

    n must be odd, greater than 2, and free of the small prime factors.
    """
    r = _isqrt(n)
    if r * r == n:
        return False                      # no D with (D/n) = -1 exists
    d = 5
    while True:
        j = _jacobi(d, n)
        if j == -1:
            break
        if j == 0 and _gcd_lucas(abs(d), n) not in (1, n):
            return False
        d = -d - 2 if d > 0 else -d + 2
    p, q = 1, (1 - d) // 4
    k, s = n + 1, 0
    while k % 2 == 0:
        k //= 2
        s += 1
    u, v, qk = 1, p % n, q % n           # U_1, V_1, Q^1
    for bit in bin(k)[3:]:
        u, v, qk = u * v % n, (v * v - 2 * qk) % n, qk * qk % n
        if bit == "1":
            u, v = _half(p * u + v, n), _half(d * u + p * v, n)
            qk = qk * q % n
    if u == 0 or v == 0:
        return True
    for _ in range(s - 1):
        v = (v * v - 2 * qk) % n
        qk = qk * qk % n
        if v == 0:
            return True
    return False


def is_prime(n):
    """Proven below psi_13; BPSW, with no known counterexample, above."""
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
    if n < _PROVEN_BELOW:
        return True
    return _strong_lucas(n)


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


def factor(n):
    """Full factorisation. Trial division by small primes, then Pollard rho.

    ``arithmetic.factorize`` is plain trial division, which is the right choice
    there -- it is the code a reader checks by eye. Here the numbers factored
    are ``f(q^e)`` for large ``q``, which reach 10^13 and beyond, so rho is
    needed. The two agree; ``verify.py`` checks that they do.

    It lives in this module and not in the search because factoring ``f`` is
    what this module is for; the search imports it from here.
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
        if is_prime(m):
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
            sieve[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    return [i for i in range(2, n + 1) if sieve[i]]


def prime_powers_up_to(limit):
    """``(m, q, e)`` with ``m = q^e <= limit``, sorted by m increasing."""
    out = []
    for q in primes_up_to(limit):
        e, power = 1, q
        while power <= limit:
            out.append((power, q, e))
            e += 1
            power *= q
    out.sort()
    return out


class SizeFloor:
    """``a_f(P) = min{ m a prime power : f(m) >= P }``, cached.

    The running maximum of f over the prime powers generated so far is
    non-decreasing by construction, and the first index at which it reaches P
    is exactly the first index at which f reaches P. So the lookup is a binary
    search and not a scan. That is not an optional optimisation: with a linear
    scan, sigma girth 7 took 280 seconds against 23 for the closed form **while
    visiting fewer nodes**, which would have made a cheaper bound look dearer.
    """

    def __init__(self, f, search_limit=2 ** 62):
        self.f = f
        self.limit = search_limit
        self._powers = []
        self._running_max = []
        self._upto = 1

    def _extend(self, target):
        while not self._running_max or self._running_max[-1] < target:
            nxt = max(4, self._upto * 2)
            if nxt > self.limit:
                raise RuntimeError(
                    "value %d is not reached by any prime power <= %d"
                    % (target, self.limit))
            running = self._running_max[-1] if self._running_max else 0
            for (m, q, e) in prime_powers_up_to(nxt):
                if m <= self._upto:
                    continue
                v = f_of_prime_power(q, e, self.f)
                if v > running:
                    running = v
                self._powers.append(m)
                self._running_max.append(running)
            self._upto = nxt

    def __call__(self, P):
        if not self._running_max or self._running_max[-1] < P:
            self._extend(P)
        return self._powers[bisect_left(self._running_max, P)]


#: Above this the value sieve is not built and each value is factored alone.
#: The number is a memory budget, not a mathematical one: an int32 array of
#: this length is about 480 MB.
SIEVE_VALUE_LIMIT = 120_000_000


def _smallest_prime_factor(n):
    """Least prime factor of every integer up to n. numpy if present, else not."""
    try:
        import numpy as np
    except ImportError:
        spf = list(range(n + 1))
        i = 2
        while i * i <= n:
            if spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1
        return spf
    dtype = np.int32 if n < 2 ** 31 - 1 else np.int64
    spf = np.arange(n + 1, dtype=dtype)
    i = 2
    while i * i <= n:
        if spf[i] == i:
            block = spf[i * i::i]
            own = np.arange(i * i, n + 1, i)
            spf[i * i::i] = np.where(block == own, i, block)
        i += 1
    return spf


def _factor_with(spf, v):
    out = set()
    x = int(v)
    while x > 1:
        p = int(spf[x])
        out.add(p)
        while x % p == 0:
            x //= p
    return out


def covering_cost(f, M, prime_limit, verbose=False):
    """``{P: A_f(P)}`` for every prime P <= prime_limit covered below M.

    A prime absent from the result has ``A_f(P) > M``.
    """
    powers = prime_powers_up_to(M)
    if not powers:
        return {}
    biggest = max(f_of_prime_power(q, e, f) for _m, q, e in powers)
    # A least-prime-factor sieve over the VALUES is much the fastest way in,
    # but its size is the largest value and not M: for sigma2 with M = 2*10^5
    # the values reach 4*10^10 and the array would be 298 GiB. Above the
    # threshold each value is factored on its own instead. Getting this wrong
    # is not a slow run, it is a MemoryError.
    by_sieve = biggest <= SIEVE_VALUE_LIMIT
    spf = _smallest_prime_factor(int(biggest) + 1) if by_sieve else None
    cost = {}
    for (m, q, e) in powers:                     # already sorted by m
        v = f_of_prime_power(q, e, f)
        if v < 2:
            continue
        primes = _factor_with(spf, v) if by_sieve else set(factor(v))
        for P in primes:
            if P != q and P <= prime_limit and P not in cost:
                cost[P] = m                      # first is least: sorted order
    if verbose:
        print("  covering cost: prime powers <= %d -> %d of %d primes covered"
              % (M, len(cost), len(primes_up_to(prime_limit))))
    return cost


class CoveringCost:
    """``A_f`` truncated at M: the exact value, or M+1 when none was found.

    **Only for P <= prime_limit.** The sieve discards larger primes while
    factoring, so for those, absence from the table says nothing: it is not
    "has no cheap cover", it is "was not looked at". Returning M+1 there would
    exclude legitimate primes, which is precisely how a minimum gets lost with
    nothing failing. Outside the range this returns 1, which carries no
    information and excludes nobody.
    """

    def __init__(self, f, M, prime_limit, verbose=False):
        self.M = M
        self.prime_limit = prime_limit
        self.table = covering_cost(f, M, prime_limit, verbose=verbose)

    def __call__(self, P):
        if P > self.prime_limit:
            return 1
        return self.table.get(P, self.M + 1)


def _main(argv):
    name = argv[0] if argv else "sigma"
    M = int(argv[1]) if len(argv) > 1 else 100000
    limit = int(argv[2]) if len(argv) > 2 else 10000
    if name not in FUNCTIONS:
        print("unknown function %r; known: %s" % (name, ", ".join(FUNCTIONS)))
        return 2
    a = SizeFloor(name)
    A = CoveringCost(name, M, limit, verbose=True)
    ps = primes_up_to(limit)
    ratios = sorted(A(P) / a(P) for P in ps)
    n = len(ratios)
    print("f = %s   M = %d   primes <= %d: %d" % (name, M, limit, n))
    print("  A_f/a_f  median=%.2f  mean=%.2f  min=%.2f  max=%.1f"
          % (ratios[n // 2], sum(ratios) / n, ratios[0], ratios[-1]))
    print("  samples (P, a_f, A_f):", [(P, a(P), A(P)) for P in ps[:10]])
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
