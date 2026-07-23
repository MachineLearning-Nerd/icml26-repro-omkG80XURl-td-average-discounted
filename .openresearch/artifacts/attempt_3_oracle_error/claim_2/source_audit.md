# Source audit — Claim 2

Source: [https://ar5iv.labs.arxiv.org/html/2605.02103#S4.Thmtheorem2](https://ar5iv.labs.arxiv.org/html/2605.02103#S4.Thmtheorem2)  
Retrieved HTML SHA-256: `2d40f7e54ced7ee48f9b336f2928e081e679293122d09d09e9fe681a6601a9d9`

Exact audited statement: Under Assumption 2.1, two independent stationary Markov chains, the stated constant-step restriction, and T>=tau_mix, the double-chain last iterate has a tilde-O(1/T) bound and tilde-O(epsilon^-1 eta^-2) sample complexity, with the explicit mixing factor retained.

Qualification controlling this contract: The displayed theorem retains tau_mix and starts both chains in stationarity. Varying the transition gap also varies mixing, so the checker keeps the explicit (3*tau_mix+1) factor.
