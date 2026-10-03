Read this when: touching the justfile, the date lint, the git hook, or the publish workflow, or when Ted asks to be told when something is live.

# Tooling

Use `just` recipes instead of running tools directly; `just` with no arguments lists them. Python
helpers are standalone scripts with a `uv` shebang and inline dependencies.

## The pre-commit hook

`just install-hooks` writes a hook that runs `just pre-commit`: a `gitleaks` scan of the staged
changes, then the staged date check. Run it once per clone. It writes into
`git rev-parse --git-common-dir`, not `.git/hooks`, so every git worktree of the repo shares the
hook. `open` in the justfile is macOS; that is fine for Ted.

## Secret scanning

`gitleaks` matches known token and key formats (cloud provider keys, GitHub tokens, private keys,
and similar) plus high-entropy strings in assignments. It does not know what personal information
looks like, so "Public by default" in `docs/authoring.md` still applies.

- `just check-secrets-staged` scans what is about to be committed (the hook runs this).
- `just check-secrets` scans the whole history (CI runs this).
- For a false positive, add a `gitleaks:allow` comment on that line, or add its fingerprint to a
  `.gitleaksignore` file. Never weaken the check for something that might be real.
- GitHub secret scanning and push protection are also on for the repo, as a second layer.

## scripts/check_dates.py

Two modes:

- **Repo-wide** (`just check-dates`): every tracked `*.html` except `index.html` list pages and
  anything under `.llm/`, `.claude/`, or `templates/` must have exactly one well-formed stamp, the
  attribute and visible dates must match, and the date must not be in the future.
- **Staged** (`just check-dates-staged`, run by the hook): for each staged content page, compare
  the staged blob with `HEAD` with the stamp line masked out of both. If anything else changed,
  or the page is new, the stamp must equal today. `SKIP_DATE_CHECK=1` skips this mode for
  cosmetic commits.

When testing it, make sure the working tree is where you think it is. An earlier round of tests
passed vacuously because they ran against the wrong checkout.

When adding stamps to pages that already exist, backfill each page with the date of its last
substantive commit. Skip commits whose diff to that file is three lines or fewer, so bulk
nav-link commits do not count as content changes.

## Publishing

`.github/workflows/pages.yml` runs on every push to `main`: it scans the full history with
`gitleaks`, runs the repo-wide date lint, runs `just build`, and deploys `_site/` with GitHub's
Pages actions. The hook only exists in clones where someone ran `just install-hooks`, so CI is
the backstop.

`just build` copies only tracked files whose extension is on the publish list (`publish_re` in
the justfile: HTML, CSS, JS, images, `.drawio`), skipping `templates/`, `scripts/`, and `docs/`.
Markdown (raw input, specs, `CLAUDE.md`, `CONTEXT.md`) is never published. The repo is public,
so all of it can still be read on GitHub. Run `just build` locally to see the exact file list.

The site is served at `https://notes.naleid.com`. The custom domain is set in the repo's Pages
settings; with Actions-based deploys a `CNAME` file in the artifact is ignored, and Jekyll never
runs, so no `.nojekyll` file is needed. DNS for `notes.naleid.com` is a CNAME at Hover pointing to
`tednaleid.github.io`.

## "Tell me when it's live"

When Ted asks to know when a pushed change is live:

1. Watch the Pages workflow run until it finishes (with `gh`, for example `gh run watch`).
2. Poll the page URL about every 30 seconds, up to about 20 minutes, sending
   `Cache-Control: no-cache` and adding a cache-busting query string (`?cb=$RANDOM`). Grep the
   response for a string that only exists in the new content. A 200 status alone may be the old
   cached page.
3. When the string appears, tell Ted and run `just web <path>`.

## Pointing Ted at docs

- Give an absolute, clickable path (`/Users/.../notes/topic/page.html`), never a relative one.
- Open it with `just open <path>`, unless it is a doc already opened in this session and you
  are iterating on it.
- After a push, prefer `just web <path>` so the link can be shared.

## Workflow habits

- Commit only when Ted asks. Never use `--no-verify`.
- Commit messages: a topic prefix and a plain summary (`baking: write up the hydration class`).
- After writing a page: run `just check-page <path>`, do the render check in both color schemes
  if it has visuals, run `just check-dates`, and for a substantial page get an independent
  review from an agent with a clean context.
- Keep `CLAUDE.md` short. When a convention needs more than a line, put it in the right
  `docs/` file and leave a one-line pointer.
