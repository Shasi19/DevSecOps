# MLflow experiment example

Run in an isolated virtual environment; this installs packages and writes a local `mlruns/` experiment store.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python train.py
```

For a real environment, pin and lock dependencies, use a governed tracking server/artifact store, restrict credentials, capture source/data lineage, and enforce evaluation/approval before registration or serving. Do not use this example's built-in dataset as a production data pipeline.
