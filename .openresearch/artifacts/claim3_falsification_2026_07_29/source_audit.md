# Source audit — Claim 3 falsification

Source: https://arxiv.org/html/2605.02103  
Retrieved: 2026-07-29 with an explicit OpenResearch browser User-Agent  
SHA-256: `c6d1ec937365657dfb23856b8b705b1aab889b68c1538f840bc459a7930563d9`

The paper defines dimension independence in Introduction item (3): dependence
on `d` is permitted only through `||theta_0||` or `||theta*||`. Theorem 4.3
assumes Assumption 2.1, Algorithm (15), two Markov chains, normalized
full-column-rank features, `alpha_t=a/(t+c0)^xi`, sufficiently large `c0`, and
`T>=tau_mix`. Appendix Theorem D.1 exposes eta, mixing constants, reward and
parameter norms but no free `d`.
