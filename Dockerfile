# Tier S light image — Flask only, NO torch/librosa. Keep it small.
FROM python:3.12-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen || uv sync
COPY . .
ENV PYTHONPATH=/app FORGE_ENV=local
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
