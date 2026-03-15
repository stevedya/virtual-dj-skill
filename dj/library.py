from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_DATABASE_XML = os.getenv(
    "VIRTUALDJ_DATABASE_XML",
    str(Path.home() / "Documents" / "VirtualDJ" / "database.xml"),
)


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _track_blob(path: str, artist: str, title: str, remix: str) -> str:
    return " ".join([path, artist, title, remix]).lower()


def list_library_results(
    query: str,
    limit: int = 10,
    database_xml: str | None = None,
) -> list[dict[str, str]]:
    """
    Search VirtualDJ database.xml and return matching tracks.

    This is an offline index lookup and may not exactly match in-app ranking.
    """
    safe_query = (query or "").strip().lower()
    if not safe_query:
        raise ValueError("Query cannot be empty.")

    db_path = Path(database_xml or DEFAULT_DATABASE_XML).expanduser()
    if not db_path.exists():
        raise FileNotFoundError(
            f"VirtualDJ database not found at '{db_path}'. "
            "Set VIRTUALDJ_DATABASE_XML to the correct path."
        )

    tree = ET.parse(db_path)
    root = tree.getroot()
    matches: list[dict[str, str]] = []

    for song in root.findall(".//Song"):
        path = _normalize_text(song.get("FilePath"))
        tags = song.find("Tags")
        artist = _normalize_text(tags.get("Author") if tags is not None else "")
        title = _normalize_text(tags.get("Title") if tags is not None else "")
        remix = _normalize_text(tags.get("Remix") if tags is not None else "")

        if safe_query not in _track_blob(path, artist, title, remix):
            continue

        matches.append(
            {
                "artist": artist,
                "title": title,
                "remix": remix,
                "path": path,
            }
        )
        if len(matches) >= max(1, int(limit)):
            break

    return matches
