# `frontend/`

Decision pending: keep the dynamic frontend here, or fold it into the
`documentation` repo's existing static site and have it probe the Flask API.

Recommended: reuse the documentation site's shell (TRON aesthetic already built),
add an `apiBase` config. If the backend answers `/api/health`, light up interactive
panels (live runs, compute projections, later posterior exploration). If not, fall
back to the committed static JSON. One frontend, two data sources.
