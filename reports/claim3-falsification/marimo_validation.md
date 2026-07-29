# Marimo validation

Notebook: `notebooks/claim3_falsification.py`  
Validator: marimo 0.23.14  
Command: `.venv/bin/marimo check --strict notebooks/claim3_falsification.py`  
Result: exit code 0, no findings.

Marimo was installed with `uv pip` into the single repository `.venv` only for
presentation validation. It is not a formal experiment dependency and was not
added to `pyproject.toml` or `uv.lock`.
