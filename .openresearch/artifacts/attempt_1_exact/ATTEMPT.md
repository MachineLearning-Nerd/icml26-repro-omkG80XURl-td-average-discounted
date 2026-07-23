# Attempt 1 — exact moments and proof-step audit

- Experiment: `Exact moment contracts on controlled chain family`
- Run: `59aeff21-1b2e-481e-ac04-184cb3ff423d`
- Git SHA: `31adeb90942b7bf7ef467cf0040e80ee3ed9ae43`
- Backend: local CPU
- Fixed command: `uv run --frozen python repro/src/verify_td.py`
- Run status: done

These files are copied byte-for-byte from the completed run directory, then
namespaced so later cumulative runs cannot overwrite them. Claim 1 was BLOCKED;
Claims 4 and 5 were deliberately BLOCKED. Claim 6's primary checks passed, but
its independent checker crashed while parsing the text-valued `family` column;
therefore the generated Claim 6 `VERIFIED` label is not accepted at campaign
level. The child experiment repairs and reruns that independent path.
