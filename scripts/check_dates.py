#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
# ABOUTME: Lints the "Contents last updated" freshness stamp on every content page.
# ABOUTME: Runs repo-wide by default, or over the staged diff (--staged, used by the pre-commit hook).

import argparse
import os
import re
import subprocess
import sys
from datetime import date

STAMP_RE = re.compile(
    r'<p class="freshness"[^>]*>\s*Contents last updated\s*'
    r'<time datetime="(\d{4}-\d{2}-\d{2})">\s*(\d{4}-\d{2}-\d{2})\s*</time>\s*</p>'
)
STAMP_LINE_RE = re.compile(r'^[ \t]*<p class="freshness".*?</p>[ \t]*\n?', re.MULTILINE | re.DOTALL)
SKIP_ENV = "SKIP_DATE_CHECK"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def content_pages():
    """Every tracked HTML page that carries a stamp: content pages, not list pages."""
    pages = []
    for path in git("ls-files", "*.html").splitlines():
        name = path.rsplit("/", 1)[-1]
        if name == "index.html" or path.startswith((".llm/", ".claude/", "templates/")):
            continue
        pages.append(path)
    return pages


def blob(rev, path):
    result = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def strip_stamp(text):
    return STAMP_LINE_RE.sub("", text)


def check_structure(path, text, today, errors):
    """Exactly one well-formed stamp whose two dates agree and are not in the future."""
    matches = STAMP_RE.findall(text)
    if not matches:
        if 'class="freshness"' in text:
            errors.append(f"{path}: freshness stamp is present but malformed")
        else:
            errors.append(f"{path}: missing freshness stamp")
        return None
    if len(matches) > 1:
        errors.append(f"{path}: {len(matches)} freshness stamps, expected 1")
        return None
    attr, shown = matches[0]
    if attr != shown:
        errors.append(f"{path}: datetime attribute {attr} does not match visible date {shown}")
        return None
    try:
        stamped = date.fromisoformat(shown)
    except ValueError:
        errors.append(f"{path}: {shown} is not a valid date")
        return None
    if stamped > today:
        errors.append(f"{path}: stamped {shown}, which is in the future")
        return None
    return stamped


def check_all(today):
    errors = []
    pages = content_pages()
    for path in pages:
        with open(path, encoding="utf-8") as handle:
            check_structure(path, handle.read(), today, errors)
    return errors, len(pages)


def staged_pages():
    pages = set(content_pages())
    staged = []
    for line in git("diff", "--cached", "--name-status", "--diff-filter=ACMR").splitlines():
        path = line.split("\t")[-1]
        if path in pages:
            staged.append(path)
    return staged


def check_staged(today):
    errors = []
    pages = staged_pages()
    for path in pages:
        staged = blob(":0", path)
        if staged is None:
            continue
        stamped = check_structure(path, staged, today, errors)
        if stamped is None:
            continue
        head = blob("HEAD", path)
        changed = head is None or strip_stamp(staged) != strip_stamp(head)
        if changed and stamped != today:
            what = "new page" if head is None else "content changed"
            errors.append(
                f"{path}: {what} but stamp still reads {stamped}. "
                f"Bump it to {today}, or use {SKIP_ENV}=1 if the change is cosmetic."
            )
    return errors, len(pages)


def main():
    parser = argparse.ArgumentParser(description="Lint freshness stamps on content pages.")
    parser.add_argument(
        "--staged",
        action="store_true",
        help="only check pages staged for commit, and require a bumped stamp on content changes",
    )
    args = parser.parse_args()
    today = date.today()

    if args.staged and os.environ.get(SKIP_ENV):
        print(f"{SKIP_ENV} set; skipping the freshness check.")
        return 0

    errors, count = check_staged(today) if args.staged else check_all(today)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    scope = "staged content page" if args.staged else "content page"
    print(f"{count} {scope}{'s' if count != 1 else ''} OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
