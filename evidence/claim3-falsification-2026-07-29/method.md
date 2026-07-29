# Method

Three materially different routes were used. Route 1 transcribed the main and
appendix formulas and applied the paper's own definition. Route 2 derived and
checked the normalization-implied trace bound `eta1 <= 3/d`, then evaluated
the peer's reported endpoint. Route 3 independently implemented Algorithm
(15) on an irreducible, aperiodic uniform-chain family with `Phi=I`, 64 fixed
seeds, exact `eta1=1/d`, `a=1/eta1`, `xi=1`, and two independent chains.

The falsification verifier exits nonzero unless it finds either a forbidden
free `d` or an assumption-valid, fully instantiated bound violation. An
injected-`d` control must make the same detector exit zero.
