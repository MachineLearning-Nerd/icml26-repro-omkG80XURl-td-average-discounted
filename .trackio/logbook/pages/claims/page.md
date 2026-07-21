# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ffbed7361dc1", "created_at": "2026-07-21T13:11:45+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Under i.i.d. sampling in the double-chain formulation, the algorithm converges to a unique, sample-independent fixed point of the projected Bellman equation with sample complexity Õ(ε^-1 η^-2) (Theorem 4.1).
2. Under Markovian sampling with constant stepsizes in the double-chain setting, the same Õ(ε^-1 η^-2) sample complexity is preserved (Theorem 4.2).
3. With decaying stepsizes, the method attains convergence guarantees with no explicit dimension-dependent terms (Theorem 4.3).
4. The paper reduces the condition-number dependence of average-reward TD learning from quartic (prior state of the art) to quadratic, matching the scaling known for discounted TD learning (Section 1, Table 1).
5. A single-chain variant of the algorithm is also analyzed but only attains quartic sample complexity Õ(1/η^4 T) due to decorrelation requirements, contrasting with the double-chain method's quadratic rate (Theorem 4.4).
6. The condition number η1, defined via min over unit vectors of ||Φx||²_Dir + (μᵀΦx)², is shown to satisfy η1 >= (1/2)η3 relative to prior condition-number definitions (Equation 3, Lemma B.3).
