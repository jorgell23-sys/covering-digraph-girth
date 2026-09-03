"""Arithmetic functions and covering digraphs. Pure Python, no dependencies.

This module is deliberately self-contained: it imports nothing outside the
standard library, so that anyone can clone the repository and run it.

The objects
-----------

For a positive integer n with prime factorization n = q1^e1 * ... * qk^ek:

    rad(n)      = q1 * ... * qk            the radical (largest squarefree divisor)
    sigma(n)    = sum of all divisors of n
    sigma*(n)   = sum of the unitary divisors of n  = prod (qi^ei + 1)
    phi*(n)     = unitary analogue of Euler's phi   = prod (qi^ei - 1)

Given a multiplicative function f and an integer n, the **covering digraph**
D_f(n) has the primes dividing n as vertices, with an edge q -> p whenever
p divides f(q^e), where q^e is the exact power of q dividing n.

n belongs to S(f) = {n : rad(n) divides f(n)} exactly when every vertex of
D_f(n) has at least one incoming edge -- hence the name "covering".

The **girth** of n is the length of the shortest directed cycle in D_f(n).
For n in S(f) the digraph cannot be acyclic, so the girth always exists; if
this code ever returns None for a member of S(f), the code is wrong.
"""

from collections import deque

__all__ = [
    "factorize", "rad", "sigma", "unitary_sigma", "unitary_phi",
    "f_of_prime_power", "in_S", "covering_digraph", "girth", "is_pure_cycle",
    "FUNCTIONS",
]

#: The three multiplicative functions studied here, by name.
FUNCTIONS = ("sigma", "sigma*", "phi*")


def factorize(n):
    """Return the prime factorization of n as a dict {prime: exponent}.

    Trial division. For the integers in this work (up to about 4.5e12, all with
    small prime factors) this takes well under a second; there is no need for
    anything cleverer, and simple code is easier to check.
    """
    if n < 1:
        raise ValueError("factorize expects a positive integer")
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def rad(n):
    """The radical of n: the product of its distinct prime factors."""
    result = 1
    for p in factorize(n):
        result *= p
    return result


def f_of_prime_power(q, e, f):
    """Evaluate f at the prime power q^e, for the three functions studied.

    These are the standard closed forms:

        sigma(q^e)  = (q^(e+1) - 1) / (q - 1) = 1 + q + ... + q^e
        sigma*(q^e) = q^e + 1        (the unitary divisors of q^e are 1 and q^e)
        phi*(q^e)   = q^e - 1
    """
    if f == "sigma":
        return (q ** (e + 1) - 1) // (q - 1)
    if f == "sigma*":
        return q ** e + 1
    if f == "phi*":
        return q ** e - 1
    raise ValueError("unknown function: %r (expected one of %r)" % (f, FUNCTIONS))


def _evaluate(n, f):
    """Evaluate the multiplicative function f at n."""
    result = 1
    for q, e in factorize(n).items():
        result *= f_of_prime_power(q, e, f)
    return result


def sigma(n):
    """Sum of the divisors of n."""
    return _evaluate(n, "sigma")


def unitary_sigma(n):
    """Sum of the unitary divisors of n: prod (q^e + 1)."""
    return _evaluate(n, "sigma*")


def unitary_phi(n):
    """The unitary analogue of Euler's phi: prod (q^e - 1)."""
    return _evaluate(n, "phi*")


def in_S(n, f):
    """Does n belong to S(f) = {n : rad(n) divides f(n)}?"""
    return _evaluate(n, f) % rad(n) == 0


def covering_digraph(n, f):
    """The covering digraph of n, as {vertex: [vertices it points to]}.

    An edge q -> p means that p divides f(q^e), where q^e is the exact power of
    q dividing n. Only primes dividing n are vertices; edges to primes outside
    n are ignored, since those primes are not part of the digraph.
    """
    factors = factorize(n)
    primes = sorted(factors)
    out = {p: [] for p in primes}
    for q in primes:
        value = f_of_prime_power(q, factors[q], f)
        for p in primes:
            if value % p == 0:
                out[q].append(p)
    return out


def girth(out_edges):
    """Length of the shortest directed cycle, or None if the digraph is acyclic.

    Breadth-first search from every vertex, stopping as soon as we return to the
    starting vertex. With at most a dozen vertices this is instant, so the code
    stays plain on purpose.

    A self-loop q -> q counts as a cycle of length 1.
    """
    best = None
    for origin in out_edges:
        distance = {origin: 0}
        queue = deque([origin])
        while queue:
            u = queue.popleft()
            if best is not None and distance[u] + 1 >= best:
                continue
            for w in out_edges[u]:
                if w == origin:
                    length = distance[u] + 1
                    if best is None or length < best:
                        best = length
                elif w not in distance:
                    distance[w] = distance[u] + 1
                    queue.append(w)
    return best


def is_pure_cycle(out_edges):
    """Is this digraph a single directed cycle through all of its vertices?

    That means: every vertex has exactly one outgoing edge and exactly one
    incoming edge, and following the edges visits every vertex before returning
    to the start. This is the shape the main theorem predicts for every minimal
    witness.
    """
    vertices = list(out_edges)
    if not vertices:
        return False
    if any(len(targets) != 1 for targets in out_edges.values()):
        return False
    incoming = {v: 0 for v in vertices}
    for targets in out_edges.values():
        for w in targets:
            incoming[w] += 1
    if any(count != 1 for count in incoming.values()):
        return False
    # Walk the cycle: it must visit every vertex exactly once.
    start = vertices[0]
    seen, current = set(), start
    for _ in vertices:
        if current in seen:
            return False
        seen.add(current)
        current = out_edges[current][0]
    return current == start and len(seen) == len(vertices)
