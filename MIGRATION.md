Migration plan: layered refactor

1. Tag current `main` as `v0_legacy_snapshot`.
2. Create branch `refactor-layered-architecture` (done).
3. Move core runtime into `/core` and expose stable APIs under `/core/api`.
4. Create `/modules` for governance/predictive/operational (scaffolded).
5. Move apps (APIs/frontends) to `/apps/*` (FastAPI scaffold added at `apps/api/main.py`).
6. Add infra manifests to `/infrastructure` and CI workflows.

Testing:
- Run `pytest -q` after each move; keep tests green.

Notes:
- LongTermGraphManager now contains `semantic_search` with a simple in-memory cache to assist profiling and early integration tests.
