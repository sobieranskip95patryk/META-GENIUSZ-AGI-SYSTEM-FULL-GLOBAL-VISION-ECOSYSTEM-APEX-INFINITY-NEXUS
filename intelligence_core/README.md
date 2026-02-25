# intelligence_core — META-GENIUSZ Unified Intelligence Core (starter)

Starter scaffold for the Unified Intelligence Engine (UIE v1).

Quickstart
-----------

Install deps:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run API:

```bash
uvicorn intelligence_core.apps.api.main:app --reload --port 8000
```
