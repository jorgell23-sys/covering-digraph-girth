"""The same exhaustive search, split across cores.

    python src/parallel.py <function> <girth> <bound> [--cores 8] [--control]

Why this can be split, and why the answer does not change
---------------------------------------------------------

The enumeration walks **starting primes** -- the largest prime of the cycle --
and each one opens a tree that touches no other: no candidate appears under two
starts, because the walk always begins at the largest prime. Splitting those
starts across processes is exact, not approximate.

The one thing lost is **shared pruning**. The whole search lowers its bound
every time it finds something better, and that bound prunes the remaining
starts; with ``W`` processes each carries its own. The minimum does not change,
and here is why: a process's bound is always at least the true minimum ``m`` --
it starts at ``N > m`` and only drops to values of witnesses that exist, which
are ``>= m``. The cutoff ``cycle_floor(P) >= bound`` drops the start ``P`` only
when every witness beginning at ``P`` measures at least
``cycle_floor(P) >= bound >= m``. So nothing below ``m`` is ever dropped, the
process owning the minimum's start finds it, and the global answer is the
smallest of what the processes return.

What it costs, measured
-----------------------

On ``sigma*`` at girth 10, same bound, same machine:

    whole, one core        48321070 nodes   287.7 s
    split, twelve cores    52828732 nodes    69.7 s     4.13x

The nodes grow 9.3% -- that is the lost pruning -- and the minimum is identical
digit for digit. On ``sigma`` at girth 7 the speedup is 4.6x and the node counts
are **identical**, because with a tight bound there was nothing left to share.

It does not reach twelve, for two measured reasons. The work is skewed: small
starts have a large budget and open huge trees, large ones are pruned at once,
so the busiest process sets the time. And each process sieves its primes once,
which does not parallelise.

**And it does not move the wall.** The girth-9 cutoff for ``sigma`` is
2197597268 primes, and splitting makes that *worse*: each process would sieve
its own table. A factor of four does not turn an infeasible search into a
feasible one.

This is deliberately **not** part of ``verify.py``. That file's promise is to
run in seconds with nothing installed, and starting a process pool is a
dependency on the machine rather than on a package. The equality control lives
here instead, behind ``--control``: it runs both and compares. A parallel search
that returns a different number is not an optimisation, it is a bug, and "it is
faster" means nothing without that comparison beside it.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exact import _Search, _search_below, prime_cutoff, primes_up_to

__all__ = ["smallest_below_parallel"]

#: Sieve and prime table, cached **per process**. Without it every task sieves
#: again, and with several tasks per core that costs more than the balancing
#: gains: measured, six tasks per core took 6.8 s against 5.9 s with one.
_CACHE = {}

#: Tasks per process. With one each the work is unbalanced and the busiest sets
#: the time; with several smaller ones the pool hands out the next as each frees
#: up. Not worth raising without limit -- see _CACHE.
TASKS_PER_CORE = 6


def _slice(task):
    """One task: the same search, over its share of the starting primes."""
    f, k, bound, which, howmany = task
    key = (f, k, bound)
    if key not in _CACHE:
        limit = prime_cutoff(bound, k, f)
        _CACHE[key] = (limit, primes_up_to(limit))
    limit, primes = _CACHE[key]
    search = _Search(f, k, 2, bound)          # no sieving: set by hand below
    search.primes = primes[which::howmany]
    search.prime_limit = limit
    search._small = primes[: k + 2]
    found = search.run()
    if found is None:
        return None, search.nodes
    product, path = found
    return (product, [(q, e) for q, e, _ in path]), search.nodes


def smallest_below_parallel(f, k, bound, cores=8,
                            tasks_per_core=TASKS_PER_CORE):
    """The smallest witness of girth k below `bound`, split across processes.

    Returns ``((n, [(prime, exponent), ...]), nodes, seconds)`` or
    ``(None, nodes, seconds)``.
    """
    from multiprocessing import Pool
    chunks = max(1, cores * tasks_per_core)
    tasks = [(f, k, bound, i, chunks) for i in range(chunks)]
    started = time.time()
    nodes = 0
    found = []
    with Pool(processes=cores) as pool:
        for best, n in pool.imap_unordered(_slice, tasks):
            nodes += n
            if best is not None:
                found.append(best)
    best = min(found, key=lambda x: x[0]) if found else None
    return best, nodes, time.time() - started


def _main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    f, k, bound = argv[0], int(argv[1]), int(argv[2])
    cores = int(argv[argv.index("--cores") + 1]) if "--cores" in argv else 8
    control = "--control" in argv

    best, nodes, seconds = smallest_below_parallel(f, k, bound, cores)
    if best is None:
        print("no witness below %d (%d cores, %d nodes, %.1fs)"
              % (bound, cores, nodes, seconds))
        return 1
    product, path = best
    shown = " * ".join(("%d^%d" % (q, e)) if e > 1 else str(q) for q, e in path)
    print("SMALLEST n = %d" % product)
    print("  factorisation  %s" % shown)
    print("  %d cores: %d nodes, %.1fs" % (cores, nodes, seconds))

    if control:
        started = time.time()
        out = _search_below(f, k, bound)
        one = out[0]
        elapsed = time.time() - started
        print("  CONTROL, whole search: n = %s (%d nodes, %.1fs)"
              % (one, out[-1], elapsed))
        if one != product:
            print("  !! THE TWO DISAGREE: the parallel search is WRONG")
            return 1
        print("  == they agree. Speedup %.2fx in time, %.2fx in nodes"
              % (elapsed / seconds if seconds else 0,
                 out[-1] / nodes if nodes else 0))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
