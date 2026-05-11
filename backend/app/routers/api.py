import os
import re
import mimetypes
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


def build_tree(dir_path: Path, rel_path: str = "") -> list:
    """Build a document tree structure from the file system."""
    items = []
    try:
        entries = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return items

    for entry in entries:
        # Skip hidden files/dirs and asset directories
        if entry.name.startswith("."):
            continue
        if entry.name.endswith(".assets") and entry.is_dir():
            continue

        item = {"name": entry.name}
        if entry.is_dir():
            children = build_tree(entry, f"{rel_path}/{entry.name}" if rel_path else entry.name)
            if children:
                item["type"] = "directory"
                item["path"] = f"{rel_path}/{entry.name}" if rel_path else entry.name
                item["children"] = children
                items.append(item)
        elif entry.suffix.lower() == ".md":
            item["type"] = "file"
            # Store path without extension for cleaner URLs
            stem = str(entry.relative_to(dir_path.parent))[:-3]
            item["path"] = stem.replace("\\", "/")
            items.append(item)

    return items


def flatten_tree_for_search(items: list, base_path: str = "") -> list:
    """Flatten the tree into a list of searchable items."""
    results = []
    for item in items:
        if item["type"] == "file":
            results.append({
                "name": item["name"].replace(".md", ""),
                "path": item["path"],
            })
        elif item["type"] == "directory" and "children" in item:
            results.extend(flatten_tree_for_search(item["children"]))
    return results


@router.get("/tree")
def get_tree():
    """Get the full document tree structure."""
    docs_dir = Path(settings.DOCS_DIR)
    if not docs_dir.exists():
        return {"tree": [], "message": "Documents directory not found"}
    tree = build_tree(docs_dir)
    return {"tree": tree}


@router.get("/search")
def search_docs(q: str = ""):
    """Search documents by name."""
    docs_dir = Path(settings.DOCS_DIR)
    if not docs_dir.exists():
        return {"results": []}
    tree = build_tree(docs_dir)
    flat = flatten_tree_for_search(tree)
    if q:
        q_lower = q.lower()
        flat = [item for item in flat if q_lower in item["name"].lower()]
    return {"results": flat}


def resolve_asset_path(doc_path: Path, img_src: str) -> Path | None:
    """Resolve image paths relative to the document location.
    Supports Typora .assets/ convention.
    """
    doc_dir = doc_path.parent
    doc_stem = doc_path.stem

    # 1. Try direct relative path from doc directory
    candidate = (doc_dir / img_src).resolve()
    if candidate.exists():
        return candidate

    # 2. Try Typora-style: doc.assets/image.png
    assets_dir = doc_dir / f"{doc_stem}.assets"
    candidate = (assets_dir / img_src).resolve()
    if candidate.exists():
        return candidate

    # 3. Try assets as sibling of doc directory (from any parent reference)
    # e.g. img src="../other.assets/img.png"
    candidate = (doc_dir / img_src).resolve()
    if candidate.exists():
        return candidate

    return None


def process_markdown_images(content: str, doc_path: Path, docs_base: Path) -> str:
    """Replace relative markdown image paths with API asset endpoints."""

    def replace_img(match):
        alt = match.group(1)
        src = match.group(2)

        # Skip absolute URLs and data URIs
        if src.startswith(("http://", "https://", "data:", "ftp://")):
            return match.group(0)

        resolved = resolve_asset_path(doc_path, src)
        if resolved and resolved.exists():
            try:
                rel = resolved.relative_to(docs_base)
                api_path = str(rel).replace("\\", "/")
                return f"![{alt}](/api/assets/{api_path})"
            except ValueError:
                pass

        # Keep original if not found
        return match.group(0)

    # Match standard markdown images: ![alt](src)
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, content)
    return content


def process_html_images(content: str, doc_path: Path, docs_base: Path) -> str:
    """Replace relative paths in <img> tags with API asset endpoints."""

    def replace_img_tag(match):
        attrs = match.group(1)
        def replace_src(m):
            src = m.group(1)
            if src.startswith(("http://", "https://", "data:", "ftp://")):
                return m.group(0)
            resolved = resolve_asset_path(doc_path, src)
            if resolved and resolved.exists():
                try:
                    rel = resolved.relative_to(docs_base)
                    api_path = str(rel).replace("\\", "/")
                    return f'src="/api/assets/{api_path}"'
                except ValueError:
                    pass
            return m.group(0)
        attrs = re.sub(r'src\s*=\s*"([^"]+)"', replace_src, attrs)
        return f"<img {attrs}>"

    content = re.sub(r'<img\s+([^>]+)>', replace_img_tag, content)
    return content


@router.get("/content")
def get_content(path: str):
    """Get markdown content for a document path.
    The path should be relative to the docs directory, without .md extension.
    """
    docs_base = Path(settings.DOCS_DIR).resolve()
    md_path = (docs_base / path).with_suffix(".md")

    if not md_path.exists() or not md_path.is_file():
        md_path = docs_base / path
        if not md_path.exists() or not md_path.is_file():
            raise HTTPException(status_code=404, detail="Document not found")

    try:
        md_path = md_path.resolve()
        content = md_path.read_text(encoding="utf-8")
        content = process_markdown_images(content, md_path, docs_base)
        content = process_html_images(content, md_path, docs_base)

        rel_path = str(md_path.relative_to(docs_base)).replace("\\", "/")
        return {"content": content, "path": rel_path}
    except Exception as e:
        logger.error(f"Error reading document {path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assets/{path:path}")
def serve_asset(path: str):
    """Serve static asset files (images, etc.)."""
    docs_base = Path(settings.DOCS_DIR).resolve()
    asset_path = (docs_base / path).resolve()

    # Security: ensure the path is within the docs directory
    try:
        asset_path.relative_to(docs_base)
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    if not asset_path.exists() or not asset_path.is_file():
        raise HTTPException(status_code=404, detail="Asset not found")

    mime_type, _ = mimetypes.guess_type(str(asset_path))
    return FileResponse(asset_path, media_type=mime_type or "application/octet-stream")


@router.get("/menus")
def get_menus():
    """Get menu configuration."""
    return {"menus": settings.MENUS}
