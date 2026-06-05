# `backend/` — Flask app (reads artifacts, never trains)

- `app.py` — app factory `create_app()`.
- `config.py` — reads `FORGE_ENV` (`local` | `prod`) and resolves the artifact root.
- `api/` — endpoints that map 1:1 onto the artifact contract:

| Route | Serves | From |
|-------|--------|------|
| `GET /api/runs` | list of runs across projects | run.json files |
| `GET /api/runs/<id>` | one run's metrics + epochs | run.json |
| `GET /api/compute/<id>` | cost profile + projection | compute.json |
| `GET /api/genealogy/<project>` | dataset provenance | project.yaml + data/manifest.json |
| `GET /api/eda/<project>` | EDA stats + figure URLs | eda_stats.json + figures/ |
| `GET /api/scorecard/<project>` | ours vs paper, per model | run.json final_metrics vs paper_target |

The backend does zero compute. If a route would need torch, it belongs in Tier R.
