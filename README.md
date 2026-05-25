# erdosstrausbash
The Erdős–Straus conjecture states that for every integer $n \ge 2$, the fraction $\frac{4}{n}$ can be expressed as a sum of three positive unit fractions.

Mordell showed that the Erdős–Straus conjecture can be reduced to checking only finitely many arithmetic residue classes, with the remaining unresolved cases ultimately falling into perfect-square families:

- $n = k^2$
- $n = (2k)^2$
- $n = (3k)^2$
- $n = (4k)^2$
- $n = (6k)^2$
- $n = (12k)^2$

We try to reproduce Mordell-type reductions by constructing best-fit template families for the remaining cases, aiming to capture all solutions to the Erdős–Straus equation through structured parameterizations.

CURRENT:
For primes $p \equiv 5 \pmod{6}$, a standard reduction gives a direct Egyptian fraction decomposition by taking $a = \frac{p+1}{3}$, $b = p$, and $c = \frac{p(p+1)}{3}$, yielding $\frac{4}{p} = \frac{1}{a} + \frac{1}{b} + \frac{1}{c}$.

REMAINING:
