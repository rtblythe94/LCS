"""LCS Systems 3 and 4: CSV-backed book management and search.
Python 3.13, standard library only. Call these methods from the team's UI.

The service deliberately never creates or overwrites the team CSV on import.
Set `path` to Robert's actual books.csv, and check headers before integration.
"""
from __future__ import annotations

import csv
import os
import tempfile
import shutil
from pathlib import Path


class BookError(ValueError):
    """A user-facing book-data validation or lookup error."""


class BookService:
    # Supported existing CSV headings; capitalization and spaces are ignored.
    ALIASES = {
        "isbn": ("isbn", "bookisbn", "isbn13", "isbn10"),
        "title": ("title", "booktitle", "name"),
        "author": ("author", "authors", "authorname"),
        "status": ("status", "currentstatus", "bookstatus"),
    }
    VALID_STATUSES = {"available", "borrowed", "checked out", "on hold", "unavailable"}

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Book database not found: {self.path}")

    @staticmethod
    def _normalized(value: str) -> str:
        return "".join(ch for ch in value.strip().casefold() if ch.isalnum())

    def prepare_schema(self) -> Path | None:
        """Explicit one-time upgrade of Robert's Title,Author,Genre CSV.

        Adds empty ISBN and Available status columns without inventing identifiers.
        Creates .bak backup. No changes if columns are already present.
        """
        with self.path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            rows = list(reader)
        if not all(k in headers for k in ("Title", "Author", "Genre")):
            raise BookError("Expected Robert's Title, Author, Genre columns.")
        added = [name for name in ("ISBN", "Status") if name not in headers]
        if not added:
            return None
        backup = self.path.with_suffix(self.path.suffix + ".bak")
        if backup.exists():
            raise BookError(f"Backup already exists: {backup}; no changes made.")
        shutil.copy2(self.path, backup)
        for row in rows:
            row.setdefault("ISBN", "")  # unknown ISBN: do not invent it
            row.setdefault("Status", "Available")
        self._write(headers + added, rows)
        return backup

    def _read(self) -> tuple[list[str], list[dict[str, str]], dict[str, str]]:
        with self.path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            if not headers:
                raise BookError("books.csv has no header row.")
            rows = list(reader)
        canonical = {self._normalized(h): h for h in headers}
        mapping = {}
        for field, aliases in self.ALIASES.items():
            mapping[field] = next((canonical[a] for a in aliases if a in canonical), "")
        missing = [f for f in ("title", "author") if not mapping[f]]
        if missing:
            raise BookError("Unrecognized books.csv columns: " + ", ".join(missing) + ". Please map the team's existing headings.")
        if any(None in row for row in rows):
            raise BookError("Malformed CSV: a row has more fields than the header.")
        return headers, rows, mapping

    def _write(self, headers: list[str], rows: list[dict[str, str]]) -> None:
        # Write to a temp file and replace atomically to avoid partial updates.
        fd, temporary = tempfile.mkstemp(prefix=".books_", suffix=".csv", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def search_books(self, field: str, query: str, *, sort_by: str = "title", reverse: bool = False) -> list[dict[str, str]]:
        """Case-insensitive partial matching by isbn, title or author; sorted results."""
        if field not in ("isbn", "title", "author"):
            raise BookError("Search field must be isbn, title or author.")
        if sort_by not in ("isbn", "title", "author", "status"):
            raise BookError("Sort field must be isbn, title, author or status.")
        query = query.strip()
        if not query:
            raise BookError("Enter an ISBN, title, or author to search.")
        _, rows, mapping = self._read()
        if not mapping.get(field):
            raise BookError(f"Cannot search by {field}: please run prepare_schema() to add the ISBN column.")
        if not mapping.get(sort_by):
            raise BookError(f"Cannot sort by {sort_by}: column does not exist.")
        matches = [r for r in rows if query.casefold() in (r.get(mapping[field]) or "").casefold()]
        return sorted(matches, key=lambda r: (r.get(mapping[sort_by]) or "").casefold(), reverse=reverse)

    def add_book(self, book: dict[str, str]) -> dict[str, str]:
        """Add a book with required fields, preserving all existing CSV columns.

        book keys are logical names ('isbn', 'title', 'author', 'status') or
        actual CSV field names. ISBN uniquely identifies records in this starter.
        If one ISBN can have multiple copies, adjust identity to (ISBN, copyNumber).
        """
        headers, rows, mapping = self._read()
        new = {h: "" for h in headers}
        lower_actual = {self._normalized(h): h for h in headers}
        for key, value in book.items():
            actual = mapping.get(key) or lower_actual.get(self._normalized(key))
            if not actual:
                raise BookError(f"Unknown book field: {key}")
            new[actual] = str(value).strip()
        for key in ("isbn", "title", "author"):
            if not mapping.get(key):
                raise BookError("Run prepare_schema() before adding books to include the ISBN column.")
            if not new[mapping[key]]:
                raise BookError(f"{key.upper()} is required.")
        if any((r.get(mapping["isbn"]) or "").strip().casefold() == new[mapping["isbn"]].casefold() for r in rows):
            raise BookError("A book with this ISBN already exists.")
        if mapping["status"]:
            status = new[mapping["status"]] or "Available"
            if status.casefold() not in self.VALID_STATUSES:
                raise BookError("Invalid book status.")
            new[mapping["status"]] = status
        rows.append(new)
        self._write(headers, rows)
        return new

    def update_book_status(self, isbn: str, status: str) -> dict[str, str]:
        headers, rows, mapping = self._read()
        if not mapping["isbn"]:
            raise BookError("Run prepare_schema() before updating book status.")
        if not mapping["status"]:
            raise BookError("Cannot update status: books.csv has no status column.")
        if not isbn.strip():
            raise BookError("ISBN is required.")
        if status.strip().casefold() not in self.VALID_STATUSES:
            raise BookError("Invalid status. Choose Available, Borrowed, Checked Out, On Hold, or Unavailable.")
        matches = [r for r in rows if (r.get(mapping["isbn"]) or "").strip().casefold() == isbn.strip().casefold()]
        if not matches:
            raise BookError("Book not found.")
        if len(matches) > 1:
            raise BookError("Multiple copies share this ISBN; identify the copy before updating.")
        matches[0][mapping["status"]] = status.strip()
        self._write(headers, rows)
        return matches[0]

    def delete_book(self, isbn: str) -> dict[str, str]:
        headers, rows, mapping = self._read()
        if not mapping["isbn"]:
            raise BookError("Run prepare_schema() before deleting books.")
        if not isbn.strip():
            raise BookError("ISBN is required.")
        matches = [r for r in rows if (r.get(mapping["isbn"]) or "").strip().casefold() == isbn.strip().casefold()]
        if not matches:
            raise BookError("Book not found.")
        if len(matches) > 1:
            raise BookError("Multiple copies share this ISBN; identify the copy before deleting.")
        if mapping["status"] and matches[0][mapping["status"]].strip().casefold() in {"borrowed", "checked out", "on hold"}:
            raise BookError("Cannot delete a borrowed or on-hold book.")
        rows.remove(matches[0])
        self._write(headers, rows)
        return matches[0]
