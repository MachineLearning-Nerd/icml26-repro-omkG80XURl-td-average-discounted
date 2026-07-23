# Claim 2: VERIFIED

A conditional-state moment operator exactly propagates two independent stationary Markov chains. After retaining the theorem's explicit mixing factor, the last-iterate error follows the stated tilde-O(1/T) envelope across all controlled eta values.

## Contract checks

- [x] `mixing_adjusted_T_exponent_in_minus_one_band`
- [x] `all_per_eta_T_exponents_in_band`
- [x] `all_horizons_exceed_mixing_time`
- [x] `all_stepsizes_obey_eta_over_18`
- [x] `moment_mass_conserved_with_matrix_power_roundoff_tolerance`

Independent checker return code: `0`. The negative-control verifier returned nonzero as required.
