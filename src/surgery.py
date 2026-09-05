"""Surgery on the cycle: insert one vertex and decide whether the next
smallest witness is smaller.

    python src/surgery.py <function> <n> <girth> [max_ratio]

The theorem
-----------

Let ``f`` be multiplicative and *local* -- meaning ``q`` never divides
``f(q^e)`` -- and let ``n = prod q_j^e_j`` be a witness of girth ``k`` whose
covering digraph is the pure cycle ``q_1 -> ... -> q_k -> q_1``.  Let ``p`` be a
prime outside the cycle and ``e', a >= 1`` such that, for some index ``i``:

1. ``p`` divides ``f(q_i^e')``                  -- the edge ``q_i -> p`` exists
2. ``q_{i+1}`` divides ``f(p^a)``               -- the edge ``p -> q_{i+1}``
3. no ``q_j`` with ``j != i`` divides ``f(q_i^e')``
4. no ``q_j`` with ``j != i+1`` divides ``f(p^a)``
5. ``p`` divides no ``f(q_j^e_j)`` with ``j != i``

Then ``n' = n * q_i^(e'-e_i) * p^a`` has as its covering digraph the pure cycle
of length ``k+1`` obtained by inserting ``p`` between ``q_i`` and ``q_{i+1}``,
so it is a witness of girth ``k+1``, and

    m_f(k+1)  <=  m_f(k) * q_i^(e'-e_i) * p^a                            (C)

*Proof.*  The vertices of the digraph of ``n'`` are the ``k+1`` primes.  Edges
out of ``q_j`` with ``j != i`` did not change, because that exponent did not
change: in ``n`` they went only to ``q_{j+1}``, and (5) says they do not go to
``p`` either.  Edges out of ``q_i`` go to ``p`` by (1) and to no ``q_j`` by (3)
-- and not to ``q_i``, by locality.  Edges out of ``p`` go to ``q_{i+1}`` by
(2), to no other ``q_j`` by (4), and not to ``p`` by locality.  So the digraph
is exactly the ``(k+1)``-cycle: every vertex has an incoming edge, hence ``n'``
lies in ``S(f)``, and its only cycle has length ``k+1``.  QED

Conditions 3, 4 and 5 are not decoration.  On the smallest witness of girth 5
for ``sigma`` the pair ``13 -> 2^2 -> 7`` satisfies (1) and (2) and produces
``1103602500``, whose girth is **2**, not 6.  ``verify.py`` pins that number.

The certificate
---------------

If in addition ``q_i^e' * p^a < q_i^e_i`` then ``m_f(k+1) < m_f(k)``: the
sequence goes *down* at ``k``, proved without computing ``m_f(k+1)``.

And it is decidable by a small finite search.  With ``p^a >= 2`` the inequality
forces ``e' < e_i``, so ``e'`` runs over ``1 .. e_i - 1``; ``p`` runs over the
prime divisors of ``f(q_i^e')``, which condition (1) already names, so the
primes need not be enumerated; and ``a`` runs over the exponents with
``p^a < q_i^(e_i-e')``.  Nothing there mentions girth ``k+1``.

An immediate consequence: if every exponent of ``m_f(k)`` is 1, no certificate
can exist.  A squarefree minimum cannot certify that the next one drops.

What the certificate does not do
--------------------------------

It is **one-directional**.  The absence of an insertion of ratio below 1 does
not prove ``m_f(k+1) >= m_f(k)``: the next minimum could come from a cycle with
no relation to this one.  That this does not happen is measured over every
consecutive pair known, not proved.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetic import covering_digraph, f_of_prime_power, factorize  # noqa: E402
from exact import _factor as factor_large  # noqa: E402

__all__ = ["pure_cycle", "admissible", "insertions", "inversion_certificate"]


def pure_cycle(n, f):
    """[(prime, exponent), ...] in cycle order, or None if not a pure cycle."""
    factors = factorize(n)
    out = covering_digraph(n, f)
    if any(len(v) != 1 for v in out.values()):
        return None
    start = min(factors)
    order, seen, q = [], set(), start
    while q not in seen:
        seen.add(q)
        order.append((q, factors[q]))
        q = out[q][0]
    if q != start or len(order) != len(factors):
        return None
    return order


def admissible(cycle, f, i, new_exp, p, a):
    """The five conditions of the theorem, plus locality, checked."""
    k = len(cycle)
    q = cycle[i][0]
    r = cycle[(i + 1) % k][0]
    vq = f_of_prime_power(q, new_exp, f)
    if vq % p:                                              # (1)
        return False
    vp = f_of_prime_power(p, a, f)
    if vp % r:                                              # (2)
        return False
    for j, (x, ex) in enumerate(cycle):
        if j != i and vq % x == 0:                          # (3)
            return False
        if x != r and vp % x == 0:                          # (4)
            return False
        if j != i and f_of_prime_power(x, ex, f) % p == 0:   # (5)
            return False
    return vq % q != 0 and vp % p != 0                      # locality


def insertions(n, f, max_ratio, max_exponent=64):
    """Every admissible insertion of ratio strictly below ``max_ratio``.

    Complete within that bound: ``p`` can only be a prime divisor of
    ``f(q^e')``, a finite set obtained by factoring.  Returns dicts sorted by
    the resulting integer.
    """
    cycle = pure_cycle(n, f)
    if cycle is None:
        raise ValueError("the digraph of %d under %s is not a pure cycle"
                         % (n, f))
    max_ratio = Fraction(max_ratio)
    inside = {q for q, _ in cycle}
    found = []
    for i, (q, e_i) in enumerate(cycle):
        budget = Fraction(q ** e_i) * max_ratio     # q^e' * p^a < budget
        new_exp = 1
        while new_exp <= max_exponent and q ** new_exp * 2 < budget:
            value = f_of_prime_power(q, new_exp, f)
            for p in sorted(factor_large(value)):
                if p in inside:
                    continue
                a, power = 1, p
                while q ** new_exp * power < budget:
                    if admissible(cycle, f, i, new_exp, p, a):
                        found.append({
                            "index": i, "q": q, "old_exponent": e_i,
                            "new_exponent": new_exp, "p": p, "a": a,
                            "ratio": Fraction(q ** new_exp * power, q ** e_i),
                            "n": n // q ** e_i * q ** new_exp * power,
                        })
                    a += 1
                    power *= p
            new_exp += 1
    found.sort(key=lambda d: d["n"])
    return found


def inversion_certificate(n, f):
    """The best insertion of ratio below 1, or None.

    If it returns something and ``n`` is ``m_f(k)``, then ``m_f(k+1) < m_f(k)``
    is proved.
    """
    found = insertions(n, f, 1)
    return found[0] if found else None


def _main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    f, n, k = argv[0], int(argv[1]), int(argv[2])
    ratio = Fraction(argv[3]) if len(argv) > 3 else Fraction(10 ** 7)
    cycle = pure_cycle(n, f)
    print("%s, girth %d, n = %d" % (f, k, n))
    print("  cycle  " + " -> ".join(
        "%d^%d" % (q, e) if e > 1 else str(q) for q, e in cycle)
        + " -> %d" % cycle[0][0])
    found = insertions(n, f, ratio)
    print("  admissible insertions with ratio < %s: %d" % (ratio, len(found)))
    for d in found[:10]:
        print("    n' = %d   ratio %s   %d^%d -> %d^%d, insert %d^%d"
              % (d["n"], d["ratio"], d["q"], d["old_exponent"],
                 d["q"], d["new_exponent"], d["p"], d["a"]))
    cert = inversion_certificate(n, f)
    print("  inversion certificate: %s"
          % ("ratio %s, so m_%s(%d) < m_%s(%d), and the witness is %d"
             % (cert["ratio"], f, k + 1, f, k, cert["n"]) if cert else "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
