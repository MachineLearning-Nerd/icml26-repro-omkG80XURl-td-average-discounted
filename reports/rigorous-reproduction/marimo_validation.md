# Marimo validation

The tutorial notebook was validated in the repository’s single `.venv` using
uv-managed optional presentation tooling:

```text
uv pip install --python .venv/bin/python marimo==0.14.17
uv pip install --python .venv/bin/python --upgrade marimo
.venv/bin/marimo check --fix notebooks/td_rate_reproduction.py
.venv/bin/marimo check --strict notebooks/td_rate_reproduction.py
```

The first pin installed successfully but did not yet provide the requested
`check` subcommand. The upgrade resolved Marimo 0.23.14, and the strict check
completed with return code 0 and no diagnostics after formatting.

Complete resolved presentation environment:

```text
anyio==4.14.2
click==8.4.2
docutils==0.23
h11==0.16.0
idna==3.18
itsdangerous==2.2.0
jedi==0.19.2
loro==1.13.2
marimo==0.23.14
markdown==3.10.2
msgspec==0.21.1
narwhals==2.24.0
numpy==2.2.6
packaging==26.2
parso==0.8.7
psutil==7.2.2
pygments==2.20.0
pymdown-extensions==10.21.3
python-multipart==0.0.32
pyyaml==6.0.3
pyzmq==27.1.0
starlette==1.3.1
tomlkit==0.15.1
typing-extensions==4.16.0
uvicorn==0.51.0
websockets==16.1.1
```

These extras are not in `pyproject.toml` or `uv.lock`, are not imported by the
formal verifier, and are absent from the clean-clone experiment environment.
