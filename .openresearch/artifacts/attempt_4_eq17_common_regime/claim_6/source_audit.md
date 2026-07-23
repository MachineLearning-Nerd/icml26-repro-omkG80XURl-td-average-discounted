# Source audit — Claim 6

Source: [https://ar5iv.labs.arxiv.org/html/2605.02103#A2.Thmtheorem3](https://ar5iv.labs.arxiv.org/html/2605.02103#A2.Thmtheorem3)  
Retrieved HTML SHA-256: `2d40f7e54ced7ee48f9b336f2928e081e679293122d09d09e9fe681a6601a9d9`

Exact audited statement: For every admissible chain and full-column-rank feature matrix, eta1 >= eta3/2 under Equations (3), (2), and the half-scaled Dirichlet seminorm in Equation (7).

Qualification controlling this contract: Equation (7) includes a factor 1/2. Omitting it, as the judged toy implementation did, changes eta1 and invalidates an exact audit.
