"""FORGE_ENV decides where artifacts come from. The local/prod switch."""
import os

ENV = os.environ.get("FORGE_ENV", "local")

ARTIFACT_ROOTS = {
    # local MVP: bind-mounted experiments repo (see docker-compose.yml)
    "local": os.environ.get("FORGE_ARTIFACTS", "/data/projects"),
    # deployed: published artifact store
    "prod":  os.environ.get("FORGE_ARTIFACTS", "/srv/forge/artifacts"),
}

def artifact_root() -> str:
    return ARTIFACT_ROOTS[ENV]
