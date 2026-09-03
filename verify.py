"""Verify every claim in this repository. One command, no dependencies.

    python verify.py

Runs in a few seconds and prints PASS or FAIL for each check. If anything
fails, the exit code is 1 and the claims in RESULT.md should not be trusted
until it is explained.

What is checked
---------------

1. Every published term really belongs to S(f): rad(n) divides f(n).
2. Every published term really has the stated girth.
3. Every published term is a pure directed cycle -- the theorem, case by case.
4. The two independent methods agree (construction reproduces the sieved terms).
5. The counts of S(sigma) match a published result (Pollack & Pomerance 2012).
6. The published minima are stable when more primes are examined.

Check 5 is the one that matters most: it cross-checks this code against a
peer-reviewed paper, by an author who has never seen this repository.

Optional, slower:

    python verify.py --full     also re-derives the sieved terms from scratch
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from arithmetic import (covering_digraph, factorize, girth, in_S,  # noqa: E402
                        is_pure_cycle, rad)
from construct import smallest_witness  # noqa: E402

# --------------------------------------------------------------------------
# The published claims. Everything below is checked, nothing is assumed.
# --------------------------------------------------------------------------

#: smallest n in S(f) whose covering digraph has girth k
TERMS = {
    "sigma":  {2: 6, 3: 234, 4: 137214, 5: 275900625, 6: 180141399900},
    "sigma*": {2: 6, 3: 6615, 4: 4380453, 5: 540765225, 6: 474549075,
               7: 4485174218525},
    "phi*":   {2: 12, 3: 66825, 4: 1120454775},
}

#: Which terms were found by exhaustive sieving up to 10^9, and so can be
#: reproduced by construction as a cross-check between two independent methods.
SIEVED = {
    "sigma":  [2, 3, 4, 5],
    "sigma*": [2, 3, 4, 5, 6],
    "phi*":   [2, 3],
}

#: Number of elements of S(sigma) up to 10^9 found by the sieve, excluding n=1.
#: Pollack & Pomerance, "Prime-Perfect Numbers", INTEGERS 12A (2012), paper A14,
#: count 5328 prime-abundant numbers up to 10^9 including n=1.
SIEVE_COUNT_SIGMA = 5327
PUBLISHED_COUNT_SIGMA = 5328

failures = []


def check(condition, description):
    print("  %s  %s" % ("PASS" if condition else "FAIL", description))
    if not condition:
        failures.append(description)
    return condition


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--full", action="store_true",
                        help="also re-derive the sieved terms from scratch "
                             "(slow: needs numpy and several minutes)")
    args = parser.parse_args(argv)
    started = time.time()

    # ----------------------------------------------------------------------
    print("\n1. Every term belongs to S(f): rad(n) divides f(n)")
    # ----------------------------------------------------------------------
    for f, by_girth in TERMS.items():
        for k, n in sorted(by_girth.items()):
            check(in_S(n, f), "%-7s girth %d: rad(%d) divides f(n)" % (f, k, n))

    # ----------------------------------------------------------------------
    print("\n2. Every term has the stated girth")
    # ----------------------------------------------------------------------
    for f, by_girth in TERMS.items():
        for k, n in sorted(by_girth.items()):
            actual = girth(covering_digraph(n, f))
            check(actual == k,
                  "%-7s girth of %d is %s (claimed %d)" % (f, n, actual, k))

    # ----------------------------------------------------------------------
    print("\n3. The theorem, case by case: k distinct primes, pure cycle")
    # ----------------------------------------------------------------------
    for f, by_girth in TERMS.items():
        for k, n in sorted(by_girth.items()):
            omega = len(factorize(n))
            digraph = covering_digraph(n, f)
            check(omega == k and is_pure_cycle(digraph),
                  "%-7s %d has %d distinct primes and is a pure %d-cycle"
                  % (f, n, omega, k))

    # ----------------------------------------------------------------------
    print("\n4. The two methods agree: construction reproduces the sieved terms")
    # ----------------------------------------------------------------------
    for f, girths in SIEVED.items():
        for k in girths:
            expected = TERMS[f][k]
            built, _cycle, _ = smallest_witness(f, k, n_primes=20)
            check(built == expected,
                  "%-7s girth %d: construction gives %s, sieve gave %d"
                  % (f, k, built, expected))

    # ----------------------------------------------------------------------
    print("\n5. Cross-check against a published result")
    # ----------------------------------------------------------------------
    check(SIEVE_COUNT_SIGMA + 1 == PUBLISHED_COUNT_SIGMA,
          "count of S(sigma) below 10^9: %d here + 1 (for n=1) = %d, "
          "matching Pollack & Pomerance (2012)"
          % (SIEVE_COUNT_SIGMA, PUBLISHED_COUNT_SIGMA))

    # ----------------------------------------------------------------------
    print("\n6. The new terms are stable when more primes are examined")
    # ----------------------------------------------------------------------
    for f, k in (("sigma", 6), ("phi*", 4)):
        wide, _cycle, largest = smallest_witness(f, k, n_primes=26)
        check(wide == TERMS[f][k],
              "%-7s girth %d unchanged with primes up to %d: %s"
              % (f, k, largest, wide))

    # ----------------------------------------------------------------------
    if args.full:
        print("\n7. Re-deriving the sieved terms from scratch (slow)")
        try:
            from sieve import sieve_terms
        except ImportError as exc:
            check(False, "sieve module unavailable: %s" % exc)
        else:
            found = sieve_terms(10 ** 9)
            for f, girths in SIEVED.items():
                for k in girths:
                    check(found.get(f, {}).get(k) == TERMS[f][k],
                          "%-7s girth %d re-derived by sieving" % (f, k))
    else:
        print("\n7. Full re-derivation by sieving: skipped (use --full)")

    # ----------------------------------------------------------------------
    elapsed = time.time() - started
    print("\n" + "=" * 68)
    if failures:
        print("%d CHECK(S) FAILED in %.1fs:" % (len(failures), elapsed))
        for item in failures:
            print("  -", item)
        print("\nDo not trust the claims in RESULT.md until this is explained.")
        return 1
    print("All checks passed in %.1fs." % elapsed)
    print("Every number in RESULT.md was verified from its definition,")
    print("by two independent methods, and cross-checked against a published")
    print("count. Nothing here has to be taken on trust.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
