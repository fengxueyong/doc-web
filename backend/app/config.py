import os
from typing import List, Dict


class Settings:
    # GitHub repo URL for docs
    GITHUB_REPO_URL: str = os.getenv(
        "GITHUB_REPO_URL",
        "https://github.com/fengxueyong/study-diary.git"
    )
    # Path inside the repo where docs are stored
    DOCS_PATH_IN_REPO: str = os.getenv("DOCS_PATH_IN_REPO", "typora-notes")
    # Where to store docs locally
    DOCS_DIR: str = os.getenv("DOCS_DIR", "/data/docs")
    # Server config
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Menu configuration
    MENUS: List[Dict[str, str]] = [
        {"label": "后端面试", "key": "backend"},
        {"label": "AI面试", "key": "ai-interview"},
        {"label": "AI编程", "key": "ai-coding"},
        {"label": "推荐阅读", "key": "recommended"},
        {"label": "网站相关", "key": "about"},
    ]


settings = Settings()
