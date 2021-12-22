from collections import namedtuple
import csv
import os
import subprocess

import arrow
from sqlite_utils import Database
import yaml


def list_hugo_content():
    """Return a listing of hugo content entries"""
    result = subprocess.run(
        ["hugo", "list", "all"], capture_output=True, text=True, check=True
    ).stdout
    return csv.DictReader(result.split("\n"))


DELIMITER = "---\n"


def get_frontmatter(filename):
    """Get dictionary from a file's YAML frontmatter"""
    _, yaml_text, _ = open(filename).read().split(DELIMITER, maxsplit=2)
    return yaml.safe_load(yaml_text)


SiteEntry = namedtuple("SiteEntry", ["entry", "tags", "announcements", "aliases"])


def prepare_entry(entry):
    """Return a SiteEntry with details about a single content entry"""
    path = entry["path"]
    frontmatter = get_frontmatter(path)

    entry["draft"] = True if entry.get("draft") == "true" else False

    # Convert date strings to native datetime objects.
    for f in ("date", "expiryDate", "publishDate"):
        entry[f] = arrow.get(entry[f]).to("utc").datetime

    sections = ("note", "post", "draft")
    section_fragment = path.split(os.sep)[1]
    entry["section"] = section_fragment if section_fragment in sections else None

    # Extract important fields from frontmatter
    simple_fields = ("caption", "category", "description", "series")
    for field in simple_fields:
        entry[field] = frontmatter.get(field)

    tags = [{"entry_path": path, "tag": tag} for tag in frontmatter.get("tags", [])]
    announcements = [
        {"entry_path": path, "service": service, "url": url}
        for service, url in frontmatter.get("announcements", {}).items()
    ]
    aliases = [
        {"entry_path": path, "url": alias} for alias in frontmatter.get("aliases", [])
    ]
    return SiteEntry(entry, tags, announcements, aliases)


DB_NAME = "site.db"


def build_db():
    """Build the database"""
    entries = []
    tags = []
    announcements = []
    aliases = []

    for entry in list_hugo_content():
        site_entry = prepare_entry(entry)
        entries.append(site_entry.entry)
        tags += site_entry.tags
        announcements += site_entry.announcements
        aliases += site_entry.aliases

    site = Database(DB_NAME, recreate=True)
    site["entries"].insert_all(entries, pk="path")
    site["tags"].insert_all(
        tags, pk=("entry_path", "tag"), foreign_keys=[("entry_path", "entries")]
    )
    site["announcements"].insert_all(
        announcements,
        pk=("entry_path", "url"),
        foreign_keys=[("entry_path", "entries")],
    )
    site["aliases"].insert_all(
        aliases, pk="url", foreign_keys=[("entry_path", "entries")]
    )


if __name__ == "__main__":
    build_db()
