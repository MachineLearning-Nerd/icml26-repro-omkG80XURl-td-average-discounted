# Claim 1: VERIFIED

Exact moment propagation converges to the deterministic root. A quadratic tilde-O envelope calibrated on eta>=0.20 holds on strictly smaller held-out eta values without refitting, while the eta^-1 negative-control envelope is rejected.

## Contract checks

- [x] `T_exponent_in_minus_one_band`
- [x] `quadratic_upper_envelope_holds_on_smaller_eta_holdout`
- [x] `eta_inverse_one_negative_control_rejected`
- [x] `regression_r_squared_at_least_0_98`
- [x] `largest_budget_mean_within_0_02_of_unique_root`
- [x] `moment_mass_conserved`

Independent checker return code: `0`. The negative-control verifier returned nonzero as required.
