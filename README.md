# INFO_698_software — Tier S (full-stack application)

> **Bible for the application tier.** One backend, one frontend, two run modes.
> This repo never trains anything — it *reads* the artifacts emitted by
> `INFO_698_experiments` and serves them.

## The key idea: the MVP is not a third codebase

There is **one** full-stack app. The "local MVP" and the "deployed app" are the **same
code in two modes**, switched by an environment variable:

| Mode | `FORGE_ENV` | Reads artifacts from | Features |
|------|-------------|----------------------|----------|
| **MVP / local** | `local` | `../INFO_698_experiments/projects/*/runs` (bind mount) | reduced set lit up |
| **deployed** | `prod` | the published artifact store | everything on |

Write the backend once; the env decides where artifacts come from. That collapse is
why this tier doesn't need a separate "MVP" project.

## Layout
```
INFO_698_software/
├── README.md              ← you are here
├── pyproject.toml         # LIGHT deps — Flask, gunicorn, pandas. NO torch.
├── Dockerfile             # light image (see §Docker)
├── docker-compose.yml     # wires backend to experiments' artifacts for local MVP
├── .devcontainer/
│   └── devcontainer.json
├── backend/               → backend/README.md
│   ├── app.py             # Flask app factory
│   ├── config.py          # FORGE_ENV local|prod -> artifact source
│   └── api/               # /runs, /genealogy, /eda, /scorecard, /compute
├── frontend/              → frontend/README.md  (or lives in the documentation repo)
└── site_export/           → site_export/README.md (curated JSON for static publish)
```

## Docker — the LIGHT image (and why it's separate from R)

This repo deliberately does **not** share the experiments image. It never imports
torch or librosa, so its image stays small (Flask + pandas). Mixing them would triple
the serving image for no reason.

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen || uv sync
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
```

### Local MVP via compose (the artifact contract made physical)
`docker-compose.yml` bind-mounts the experiments artifacts read-only and sets
`FORGE_ENV=local`:

```bash
docker compose up        # backend on :5000, reading ../INFO_698_experiments runs
```

So R emits `run.json`/`compute.json` → the bind mount exposes them → the backend
serves them → the frontend renders them. Same path the deployed app uses, minus the
mount.

### VS Code workflow
Same as R: **Dev Containers: Reopen in Container** → light image builds → `uv sync` →
interpreter selected. No GPU, no audio libs needed here.

## Relationship to the documentation repo
The documentation repo (GitHub Pages) serves **committed static JSON** from its own
`site_export/`. `export_site.py` (run from this repo or R) copies curated artifacts
there for the always-on, no-server public view. The Flask backend is the *dynamic*
counterpart — live dashboards now, posterior exploration for the Bayesian layer later.
Frontend probes a configurable API base: backend reachable → interactive panels;
unreachable → static fallback. (Mirrors the HELIX pattern.)
