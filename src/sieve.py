"""Find the witnesses by exhaustive sieving. The slow, independent method.

This is the first of the two methods, and the one that needs no theory: it walks
every integer in a range, keeps those with rad(n) dividing f(n), computes the
girth of each, and records the smallest witness of each girth.

It is here for two reasons:

1. **It cross-checks the construction.** The two methods share no logic. The
   sieve knows nothing about cycles; the construction never looks at an integer
   that is not built from a cycle. When they agree on a term, that agreement is
   evidence.
2. **It measures how rare the high-girth witnesses are**, which is what shows
   that sieving cannot reach them. Up to 10^9 under sigma the counts per girth
   are 4138, 1065, 122, 2 -- falling by factors 3.9, then 8.7, then 61. The
   factor keeps growing, so a witness of girth 6 would need a range of roughly
   10^13. That is why the construction exists.

Requires numpy, which is the only dependency in this repository and is needed
only here. `verify.py` runs without it.

Usage:

    python src/sieve.py 1000000000
"""

import sys
import time

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import FUNCTIONS, covering_digraph, girth


def _primes_up_to(limit):
    """Sieve of Eratosthenes, as a numpy array."""
    flags = np.ones(limit + 1, dtype=bool)
    flags[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = False
    return np.nonzero(flags)[0]


def _segment(low, high, primes):
    """rad, sigma, sigma*, phi* and sigma** for every integer in [low, high).

    One pass per prime, writing into arrays. `remainder` tracks what is left of
    each integer after dividing out the primes found; whatever survives above 1
    is a prime factor with exponent 1.

    ``sigma**`` needs the exponent's parity, which the array of exact powers
    carries implicitly: ``q^e`` is a perfect square exactly when ``e`` is even,
    and then the divisor to subtract is its square root. The root is taken in
    integers and corrected, never trusted from floating point.
    """
    length = high - low
    radical = np.ones(length, dtype=np.int64)
    sig = np.ones(length, dtype=np.int64)
    usig = np.ones(length, dtype=np.int64)
    uphi = np.ones(length, dtype=np.int64)
    bsig = np.ones(length, dtype=np.int64)
    remainder = np.arange(low, high, dtype=np.int64)

    for p in primes.tolist():
        if p * p > high:
            break
        start = (-low) % p
        if start >= length:
            continue
        # exact_power[i] = p^(v_p(n)) for the i-th multiple of p in the segment,
        # built by overwriting with increasing powers; the last one written wins.
        exact_power = np.full((length - start + p - 1) // p, p, dtype=np.int64)
        index = np.arange(start, length, p)
        q = p * p
        while q <= high:
            j = (-low) % q
            if j < length:
                exact_power[(j - start) // p::q // p] = q
            q *= p
        radical[index] *= p
        usig[index] *= exact_power + 1
        uphi[index] *= exact_power - 1
        sigma_pp = (exact_power * p - 1) // (p - 1)
        sig[index] *= sigma_pp
        root = np.sqrt(exact_power.astype(np.float64)).astype(np.int64)
        root = np.where(root * root > exact_power, root - 1, root)
        root = np.where((root + 1) * (root + 1) <= exact_power, root + 1, root)
        square = root * root == exact_power
        bsig[index] *= np.where(square, sigma_pp - root, sigma_pp)
        remainder[index] //= exact_power

    left = remainder > 1
    tail = remainder[left]
    radical[left] *= tail
    usig[left] *= tail + 1
    uphi[left] *= tail - 1
    sig[left] *= tail + 1
    bsig[left] *= tail + 1          # exponent 1 is odd: sigma** = sigma = q+1
    return {"rad": radical, "sigma": sig, "sigma*": usig, "phi*": uphi,
            "sigma**": bsig, "low": low}


def members(segment, f):
    """The integers of the segment with rad(n) dividing f(n)."""
    mask = (segment[f] % segment["rad"]) == 0
    return (np.nonzero(mask)[0] + segment["low"]).tolist()


def sieve_terms(limit, step=5_000_000, verbose=False):
    """Smallest witness of each girth, for each function, below `limit`.

    Returns {function: {girth: smallest n}}.
    """
    if np is None:
        raise ImportError("numpy is required for sieving; verify.py runs without it")

    smallest = {f: {} for f in FUNCTIONS}
    counts = {f: {} for f in FUNCTIONS}
    primes = _primes_up_to(int(limit ** 0.5) + 1)
    started = time.time()

    low = 2
    while low < limit:
        high = min(low + step, limit)
        segment = _segment(low, high, primes)
        for f in FUNCTIONS:
            for n in members(segment, f):
                if n < 2:
                    continue
                k = girth(covering_digraph(int(n), f))
                if k is None:
                    # Impossible for a member of S(f): the code would be wrong.
                    raise AssertionError(
                        "acyclic covering digraph for %d in S(%s)" % (n, f))
                counts[f][k] = counts[f].get(k, 0) + 1
                if k not in smallest[f] or n < smallest[f][k]:
                    smallest[f][k] = int(n)
        if verbose:
            print("  ...up to %d (%.0fs)" % (high, time.time() - started),
                  flush=True)
        low = high

    if verbose:
        print()
        for f in FUNCTIONS:
            total = sum(counts[f].values())
            print("%s: %d members below %d" % (f, total, limit))
            for k in sorted(smallest[f]):
                print("    girth %d: smallest %d  (%d members)"
                      % (k, smallest[f][k], counts[f][k]))
    return smallest


def main(argv=None):
    limit = int(argv[0]) if argv else 10 ** 9
    sieve_terms(limit, verbose=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
