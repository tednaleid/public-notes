# ABOUTME: Task runner for the notes site: open docs locally or live, lint pages, build the Pages artifact.
# ABOUTME: Run `just install-hooks` once per clone to enforce stamp bumps and secret scanning on commit.

# Base URL of the published Pages site.
pages_url := "https://notes.naleid.com"

# Files that make up the published site. Everything else (markdown, scripts, templates) stays in git only.
publish_re := '(\.(html|css|js|png|jpe?g|gif|webp|svg|drawio)$)'

default:
    @just --list

# Open a local doc in the default browser (defaults to the hub).
open file="index.html":
    open "{{justfile_directory()}}/{{file}}"

# Open a doc on the live Pages site; takes a repo-relative path.
web file="":
    open "{{pages_url}}/{{file}}"

# Serve the repo locally for render checks.
serve port="8731":
    python3 -m http.server {{port}}

# Lint the freshness stamp on every content page.
check-dates:
    ./scripts/check_dates.py

# Staged content changes must bump their stamp to today.
# Set SKIP_DATE_CHECK=1 on the commit when the change is cosmetic.
check-dates-staged:
    ./scripts/check_dates.py --staged

# Check pages for leftover chunk sentinels, em-dashes, and SVGs that do not parse.
check-page +files:
    ./scripts/check_page.py {{files}}

# Flag SVG text that crosses a box edge or runs past the viewBox, using a headless browser.
check-svg file:
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{justfile_directory()}}"
    python3 -m http.server 8732 >/dev/null 2>&1 &
    server=$!
    trap 'playwright-cli close >/dev/null; kill $server' EXIT
    sleep 0.5
    playwright-cli open "http://localhost:8732/{{file}}" >/dev/null
    result="$(playwright-cli --raw eval "$(cat scripts/svg-overlap.js)")"
    echo "$result"
    [ "$result" = '"clean"' ]

# Scan the full git history for secrets.
check-secrets:
    gitleaks git --redact --no-banner

# Scan staged changes for secrets.
check-secrets-staged:
    gitleaks git --staged --redact --no-banner

# What the pre-commit hook runs.
pre-commit: check-secrets-staged check-dates-staged

# Copy the published subset of tracked files into _site/ for the Pages artifact.
build:
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf _site
    mkdir _site
    git ls-files | grep -E '{{publish_re}}' | grep -vE '^(templates|scripts|docs)/' | rsync -a --files-from=- . _site/
    find _site -type f | sort

# One-time per clone: wire secret scanning and the staged date check into the pre-commit hook.
install-hooks:
    #!/usr/bin/env bash
    set -euo pipefail
    hook="$(git rev-parse --git-common-dir)/hooks/pre-commit"
    mkdir -p "$(dirname "$hook")"
    printf '#!/usr/bin/env bash\nexec just --justfile "%s" pre-commit\n' \
        "{{justfile()}}" > "$hook"
    chmod +x "$hook"
    echo "Installed $hook"
