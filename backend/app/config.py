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

    # Menu configuration (header navigation)
    MENUS: List[Dict[str, str]] = [
        {"label": "后端面试", "key": "backend", "icon": "fa-solid fa-microchip"},
        {"label": "AI面试", "key": "ai-interview", "icon": "fa-solid fa-robot"},
        {"label": "AI编程", "key": "ai-coding", "icon": "fa-solid fa-code"},
        {"label": "推荐阅读", "key": "recommended", "icon": "fa-solid fa-star"},
        {"label": "网站相关", "key": "about", "icon": "fa-solid fa-circle-info"},
    ]

    # Sidebar document categories (keyword matching on filename)
    CATEGORIES: List[Dict] = [
        {
            "name": "后端与架构",
            "icon": "fa-solid fa-layer-group",
            "keywords": [
                "java", "spring", "架构师", "微服务", "python", "go语言",
                "tomcat", "jetty", "socket", "rpc", "数据结构", "算法",
                "jvm", "虚拟机", "付费课", "待解决",
            ]
        },
        {
            "name": "前端",
            "icon": "fa-solid fa-laptop-code",
            "keywords": [
                "前端", "vue", "react", "html", "css", "javascript",
                "node", "npm", "webpack", "vite",
            ]
        },
        {
            "name": "容器与运维",
            "icon": "fa-solid fa-cloud",
            "keywords": [
                "docker", "kubernetes", "k8s", "ubuntu", "linux",
                "鸟哥", "安装", "git", "计算机网络", "云原生", "知识备忘录",
            ]
        },
        {
            "name": "数据库与中间件",
            "icon": "fa-solid fa-database",
            "keywords": [
                "mysql", "kafka", "mongo", "postgre", "sql", "redis",
                "大数据", "大模型", "elasticsearch", "消息队列", "缓存",
            ]
        },
    ]


settings = Settings()
