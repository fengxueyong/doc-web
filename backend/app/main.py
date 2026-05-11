import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers.api import router as api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def clone_or_update_repo():
    """Clone the GitHub repo with documents on first startup."""
    import git

    docs_dir = Path(settings.DOCS_DIR)
    repo_url = settings.GITHUB_REPO_URL

    if docs_dir.exists():
        logger.info(f"Docs directory already exists at {docs_dir}")
        return

    logger.info(f"Cloning repository {repo_url}...")
    docs_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        repo = git.Repo.clone_from(repo_url, str(docs_dir), depth=1)
        # If docs are in a subdirectory, move them up
        if settings.DOCS_PATH_IN_REPO:
            sub = docs_dir / settings.DOCS_PATH_IN_REPO
            if sub.exists() and sub.is_dir():
                logger.info(f"Documents found in subdirectory: {settings.DOCS_PATH_IN_REPO}")
        logger.info("Repository cloned successfully")
    except Exception as e:
        logger.error(f"Failed to clone repository: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DocWeb backend...")
    try:
        clone_or_update_repo()
    except Exception as e:
        logger.warning(f"Could not clone repo at startup: {e}")
        logger.warning("You can manually place documents in the docs directory")
    yield
    logger.info("Shutting down DocWeb backend...")


app = FastAPI(title="DocWeb", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
