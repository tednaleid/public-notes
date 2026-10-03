# public-notes

Ted's research notes: self-contained static HTML pages published to https://notes.naleid.com.
This repo is notes, not software. Deliverables are documents. If a topic could lead to building
something, write up the reasoning as a doc and let Ted decide separately.

- The repo and site are public. Never commit a secret, token, resolved credential, significant
  personal information, or employer material (`docs/authoring.md`, "Public by default").
- Ted reads HTML, not markdown. Keep raw input beside the page; markdown is never published.
- No emoji, em-dashes, or hyperbole. Concise and skimmable.
- Every content page has a freshness stamp; bump it on real content changes (`just check-dates`).
- When pointing Ted at a doc, give an absolute path and open it with `just open <path>`.
  After pushing, use `just web <path>` for the shareable URL.
- `.llm/` is gitignored scratch space. Vocabulary lives in `CONTEXT.md`.

Read before acting:
- Writing or editing a page: docs/authoring.md
- Styling, layout, or a new CSS pattern: docs/styling.md
- Drawing a diagram: docs/diagrams.md
- Justfile, date lint, secret scanning, hooks, publishing: docs/tooling.md
- Where things live: index.html (the hub; add a card when a page lands)
