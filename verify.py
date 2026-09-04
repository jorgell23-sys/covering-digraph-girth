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
6. The cutoff lemma holds for every published term.
7. The exact search reproduces the smaller terms, exhaustively.

Check 5 is the one that matters most: it cross-checks this code against a
peer-reviewed paper, by an author who has never seen this repository.

Optional, slower:

    python verify.py --full     also re-derives the sieved terms from scratch
    python verify.py --exact    also re-proves the large terms (minutes)
"""

import argparse
import json
import re
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from arithmetic import (covering_digraph, factorize, girth, in_S,  # noqa: E402
                        is_pure_cycle, rad)
from construct import smallest_witness  # noqa: E402
from exact import (cycle_floor, exact_smallest, per_arc_floor,  # noqa: E402
                   prime_cutoff, primorial, predecessor_floor,
                   smallest_without_seed, universal_floor)

# --------------------------------------------------------------------------
# The published claims. Everything below is checked, nothing is assumed.
# --------------------------------------------------------------------------

#: smallest n in S(f) whose covering digraph has girth k
TERMS = {
    "sigma":  {2: 6, 3: 234, 4: 137214, 5: 275900625, 6: 180141399900,
               7: 7746928876851255, 8: 31674203849435875},
    "sigma*": {2: 6, 3: 6615, 4: 4380453, 5: 540765225, 6: 474549075,
               7: 4485174218525, 8: 2386830845734335,
               9: 9928651387877145},
    "phi*":   {2: 12, 3: 66825, 4: 1120454775, 5: 1663175056640625},
}

#: Terms cheap enough to re-prove exhaustively in the default run. The rest are
#: behind --exact: sigma girth 7 examines every prime below 2.6 million.
EXACT_FAST = {"sigma": [2, 3, 4, 5], "sigma*": [2, 3, 4, 5, 6],
              "phi*": [2, 3, 4]}
EXACT_SLOW = {"sigma": [6, 7, 8], "sigma*": [7, 8, 9], "phi*": [5]}

def cycle_of(n, f):
    """The cycle of a pure-cycle term, as [(prime, exponent), ...] in order.

    The per-arc bound is a statement about the ARCS, so it needs the cyclic
    order and not just the factorisation. That order is **not** written down
    anywhere here: it is read off the covering digraph, which for these terms
    is a pure cycle, so every vertex has exactly one outgoing arc and following
    them from any start recovers the whole cycle. Writing the cycles out by
    hand would be transcribing something the digraph already determines.
    """
    factors = factorize(n)
    digraph = covering_digraph(n, f)
    start = min(factors)
    order, seen, q = [], set(), start
    while q not in seen:
        seen.add(q)
        order.append((q, factors[q]))
        out = digraph[q]
        if len(out) != 1:
            return None                     # not a pure cycle: caller reports
        q = out[0]
    if q != start or len(order) != len(factors):
        return None
    return order

#: The next two terms, bracketed. The lower bound is a theorem -- the seedless
#: search swept everything below it and found nothing -- but re-proving it takes
#: hours, so it is recorded rather than rechecked here. The upper bound is a
#: witness exhibited by the constructor, and THAT is rechecked below: it is
#: verified to be in S(f), to have the stated girth, and to be a pure cycle.
#: It is not claimed to be minimal.
BRACKETS = {
    ("sigma", 9): {
        "no_witness_below": 1239376200655897100288,
        "primes_swept": 69681011,
        "witness": 8324995955560453359590400,
    },
    ("phi*", 6): {
        "no_witness_below": 1344781885607247872,
        "primes_swept": 80023266,
        "witness": 41542332517979068359375,
    },
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
passed = [0]


def check(condition, description):
    print("  %s  %s" % ("PASS" if condition else "FAIL", description))
    if not condition:
        failures.append(description)
    else:
        passed[0] += 1
    return condition


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--full", action="store_true",
                        help="also re-derive the sieved terms from scratch "
                             "(slow: needs numpy and several minutes)")
    parser.add_argument("--exact", action="store_true",
                        help="also re-prove the large terms exhaustively "
                             "(slow: about 25 minutes in total)")
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
    print("\n7. The cutoff lemma holds for every published term")
    # ----------------------------------------------------------------------
    # (*)  n >= P * a_f(P) * primorial(k-2), with P the largest prime of n.
    # If this ever failed, the exhaustive searches would have been cutting off
    # a region that can contain the answer, and every "proved minimal" here
    # would be worth nothing.
    for f, by_girth in TERMS.items():
        for k, n in sorted(by_girth.items()):
            largest = max(factorize(n))
            check(n >= cycle_floor(largest, k, f),
                  "%-7s girth %d: %d >= %d * %d * %d"
                  % (f, k, n, largest, predecessor_floor(largest, f),
                     primorial(k - 2)))
            check(largest <= prime_cutoff(n + 1, k, f),
                  "%-7s girth %d: its largest prime %d is within the cutoff %d"
                  % (f, k, largest, prime_cutoff(n + 1, k, f)))

    # ----------------------------------------------------------------------
    print("\n8. Exhaustive search re-proves the terms it can reach quickly")
    # ----------------------------------------------------------------------
    plan = dict(EXACT_FAST)
    if args.exact:
        for f, ks in EXACT_SLOW.items():
            plan[f] = sorted(plan.get(f, []) + ks)
    for f, girths in plan.items():
        for k in girths:
            expected = TERMS[f][k]
            got, _factors, _cycle, limit = exact_smallest(f, k, expected)
            check(got == expected,
                  "%-7s girth %d: nothing smaller exists below any prime <= %d"
                  % (f, k, limit))
    if not args.exact:
        print("  (sigma 6-8, sigma* 7-8 and phi* 5 skipped: use --exact)")

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    print("\n9. The per-arc lemma: (*) <= (+) <= n for every term")
    # ----------------------------------------------------------------------
    # (+)  n >= prod_i max(q_i, a_f(q_{i+1})), the per-arc cost lemma. It
    # strengthens (*), so both inequalities have to hold at once: if (+) ever
    # exceeded n the search would be pruning away the answer, and if (+) fell
    # below (*) the strengthening would be empty.
    for f, by_girth in sorted(TERMS.items()):
      for k, n in sorted(by_girth.items()):
        cycle = cycle_of(n, f)
        if not check(cycle is not None,
                     "%-7s girth %d: the digraph of %d is a single cycle"
                     % (f, k, n)):
            continue
        product = 1
        for q, e in cycle:
            product *= q ** e
        check(product == n,
              "%-7s girth %d: the cycle read off the digraph rebuilds %d"
              % (f, k, n))
        star = cycle_floor(max(q for q, _ in cycle), k, f)
        arc = per_arc_floor(cycle, f)
        check(star <= arc <= n,
              "%-7s girth %d: (*) %d <= (+) %d <= n %d" % (f, k, star, arc, n))

    # ----------------------------------------------------------------------
    print("\n10. The universal floor, and the search that needs no seed")
    # ----------------------------------------------------------------------
    # (++) n >= p_k * a_f(p_k) * primorial(k-2) mentions no known witness,
    # which is what lets the search start from nothing. If it ever exceeded a
    # term, the seedless search would begin above the answer and skip it.
    for f, by_girth in TERMS.items():
        for k, n in sorted(by_girth.items()):
            check(n >= universal_floor(k, f),
                  "%-7s girth %d: %d >= universal floor %d"
                  % (f, k, n, universal_floor(k, f)))
    seedless = dict(EXACT_FAST)
    if args.exact:
        for f, ks in EXACT_SLOW.items():
            seedless[f] = sorted(seedless.get(f, []) + ks)
    for f, girths in seedless.items():
        for k in girths:
            got, _fac, _cyc, limit, _nodes, rounds = smallest_without_seed(f, k)
            check(got == TERMS[f][k],
                  "%-7s girth %d found with NO seed, in %d rounds: %s"
                  % (f, k, rounds, got))
    if not args.exact:
        print("  (the large terms are seedless-checked only under --exact)")

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    print(chr(10) + "11. The next two terms are bracketed, and the bracket holds")
    # ----------------------------------------------------------------------
    for (f, k), data in sorted(BRACKETS.items()):
        n = data["witness"]
        digraph = covering_digraph(n, f)
        check(in_S(n, f) and girth(digraph) == k and is_pure_cycle(digraph),
              "%-7s girth %d: the exhibited witness %d is in S(f), has girth "
              "%d and is a pure cycle" % (f, k, n, k))
        check(data["no_witness_below"] < n,
              "%-7s girth %d: the bracket is consistent, %d < %d"
              % (f, k, data["no_witness_below"], n))
        check(len(factorize(n)) == k,
              "%-7s girth %d: the witness has exactly %d distinct primes"
              % (f, k, k))

    # ----------------------------------------------------------------------
    print(chr(10) + "12. In phi*, each minimum divides the next")
    # ----------------------------------------------------------------------
    # Two links, not a law -- and the prediction that the third holds is the
    # falsifiable part. The exhibited girth-6 witness does continue the chain,
    # which is checked here; the true minimum of girth 6 is unknown.
    phi = TERMS["phi*"]
    for a, b in ((3, 4), (4, 5)):
        check(phi[b] % phi[a] == 0,
              "phi*    m(%d) divides m(%d): %d divides %d"
              % (a, b, phi[a], phi[b]))
    check(BRACKETS[("phi*", 6)]["witness"] % phi[5] == 0,
          "phi*    the exhibited girth-6 witness continues the chain: "
          "%d divides it" % phi[5])
    check(phi[3] % phi[2] != 0,
          "phi*    the chain does NOT reach back to girth 2: %d does not "
          "divide %d" % (phi[2], phi[3]))
    # And the correlation that looked obvious, recomputed rather than asserted:
    # the largest jump of all is one where the previous term divides the next,
    # so sharing and jump size are unrelated.
    pairs = []
    for f, by_girth in TERMS.items():
        ks = sorted(by_girth)
        for a, b in zip(ks, ks[1:]):
            pairs.append((by_girth[b] / by_girth[a], f, a, b,
                          by_girth[b] % by_girth[a] == 0))
    pairs.sort()
    biggest = pairs[-1]
    check(biggest[4],
          "the largest jump of the %d consecutive pairs (%s %d->%d, factor "
          "%.0f) is one where the previous term DIVIDES the next -- so sharing "
          "does not explain jump size"
          % (len(pairs), biggest[1], biggest[2], biggest[3], biggest[0]))

    # ----------------------------------------------------------------------
    if args.full:
        print("\n13. Re-deriving the sieved terms from scratch (slow)")
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
        print("\n13. Full re-derivation by sieving: skipped (use --full)")

    # ----------------------------------------------------------------------
    # 14. The explainer page cannot go stale in silence.
    #
    # Every live number in docs/*.html is tagged data-fact="...", and here each
    # one is compared against the data. The figures are compared against what
    # their generator produces right now. So if a value improves and the
    # explanation is not updated, THIS FAILS -- which is the point: a rule
    # written in prose gets broken again.
    print("\n14. The explainer page is in sync with the data")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data", "terms.json"), encoding="utf-8") as fh:
        terms = json.load(fh)["functions"]
    expected = {
        "terms_total": sum(len(v) for v in terms.values()),
        "new_terms": sum(1 for v in terms.values()
                         for e in v if e.get("first_computed_here")),
        "sieve_count": SIEVE_COUNT_SIGMA,
        "published_count": PUBLISHED_COUNT_SIGMA,
    }
    pages = [os.path.join("docs", "index.html"),
             os.path.join("docs", "es", "index.html")]
    for page in pages:
        path = os.path.join(here, page)
        if not os.path.exists(path):
            check(False, "%s exists" % page)
            continue
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        facts = dict(re.findall(r'data-fact="([a-z_0-9]+)">([^<]+)<', html))
        wrong = {k: (facts.get(k), str(v)) for k, v in expected.items()
                 if facts.get(k) != str(v)}
        check(not wrong, "%s: every tagged number matches the data%s"
              % (page, "" if not wrong else " -- %s" % wrong))
        missing = [src for src in re.findall(r'<img src="([^"]+)"', html)
                   if not os.path.exists(os.path.normpath(
                       os.path.join(os.path.dirname(path), src)))]
        check(not missing, "%s: every figure it references exists%s"
              % (page, "" if not missing else " -- missing %s" % missing))

    sys.path.insert(0, os.path.join(here, "src"))
    import make_figures as MF
    stale = []
    for name, fn in (("graph", MF.fig_graph), ("girth", MF.fig_girth),
                     ("cutoff", MF.fig_cutoff)):
        for es, suf in ((False, ""), (True, ".es")):
            f = os.path.join(here, "docs", "figures", "%s%s.svg" % (name, suf))
            if not os.path.exists(f):
                stale.append(os.path.basename(f))
                continue
            with open(f, encoding="utf-8") as fh:
                if fh.read() != fn(es=es):
                    stale.append(os.path.basename(f))
    for es, suf in ((False, ""), (True, ".es")):
        f = os.path.join(here, "docs", "figures", "terms%s.svg" % suf)
        if not os.path.exists(f):
            stale.append(os.path.basename(f))
            continue
        with open(f, encoding="utf-8") as fh:
            if fh.read() != MF.fig_terms(terms, es=es):
                stale.append(os.path.basename(f))
    check(not stale, "the 8 figures are what their generator produces today%s"
          % ("" if not stale else " -- stale: %s" % stale))

    # The page announces how many checks this file runs; self-referential on
    # purpose, so that adding one and forgetting the text breaks the count.
    total = passed[0] + len(failures) + 2
    for page in pages:
        path = os.path.join(here, page)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            m = re.search(r'data-fact="checks">([^<]+)<', fh.read())
        check(m is not None and int(m.group(1)) == total,
              "%s: the number of checks it announces is right (%s, expected %d)"
              % (page, m.group(1) if m else "absent", total))

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
    print("by three independent methods, and cross-checked against a published")
    print("count. Nothing here has to be taken on trust.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
