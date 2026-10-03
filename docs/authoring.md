Read this when: creating a page, turning raw input into a page, or making a substantive edit.

# Authoring

Terms used here (hub, topic page, content page, list page, raw input, freshness stamp) are
defined in `CONTEXT.md`.

## Public by default

The repo and the site are both public. Anything committed can be read on GitHub, even when the
site leaves it out (see `docs/tooling.md` for what is published).

- Never commit a secret, token, password, or resolved credential. When a page shows how to fetch
  a credential, show the command (`$(op read ...)`, `$(aws secretsmanager get-secret-value ...)`),
  never its output. `gitleaks` checks on commit and in CI, but it only knows token patterns.
- No significant personal information about Ted or anyone else: no ID numbers, addresses, phone
  numbers, health or financial details. Ted's name is fine.
- No material from Ted's employer.
- Commit raw input only when it is Ted's own material or already public (docs, release notes,
  experiment output). Transcripts of conversations with other people stay in `.llm/`.

## Organization

- **The hub.** `index.html` at the root is the site's landing page and is served as the Pages
  root. One section per topic: an `h2`, then a grid of cards. Each card has a
  title with a right arrow, a one to three sentence blurb, and the repo-relative path in
  monospace. Add a card whenever a durable page lands.
- **Topic directories.** Put pages in a directory per topic once there are two or more on the
  same subject. Let the directories emerge; do not create empty ones in advance. The topic
  page is the directory's `index.html`, a list page, and the hub card points to it.
- **Dated list pages for things that go stale.** Meeting write-ups, point-in-time status, and
  similar notes go in a directory with its own `index.html` list page, named
  `YYYY-MM-DD-<subject>.html`, newest first. The hub links the list page once, not each entry.
  Its lede can say plainly that these go stale on purpose.
- **Short-lived pages hang off their parent.** A page that only matters for a few weeks (a
  follow-up list, prep for one meeting) is linked from the page it supports, not from the hub.
- **Every page links back up.** The first line of the page header is a link to the parent page,
  and from there to the hub. A sub-page links to its topic page, not straight to the hub.
- **Version what would otherwise be lost.** If the only copy of a source (a transcript, a
  diagram source file) lives in a gitignored directory or in Downloads, copy it into the repo
  beside the page that uses it.
- **Fix canonical docs where they live.** If a fact belongs to a doc in another repo, fix it
  there and link to it. Do not copy it here, where it will drift. Delete duplicated drafts
  rather than leaving two versions.
- **Live or automated content gets its own repo.** Anything regenerated on a schedule
  (a status page, a dashboard) moves out. This repo stays static notes.
- **Other people's documents stay verbatim.** If a page is someone else's work kept for
  reference, list it in CLAUDE.md or the topic's docs as "do not edit". The only permitted
  change is adding the freshness stamp.
- **`.llm/` is scratch.** Gitignored. Working files, cloned repos for reading, drafts, and
  snippets meant for pasting elsewhere go there.

## From raw input to page

The common request looks like: "here's a transcript in Downloads plus screenshots, write it up,
commit, push, and tell me when it's live."

1. Copy the raw input into the repo beside the page it will feed, as `.md` (for example
   `topic/2026-10-03-subject-notes.md`). Keep it unedited. Check it against "Public by default"
   first.
2. Do not trust speaker attribution in transcripts. Room audio is often attributed to whoever
   was sharing the microphone. When a line matters, ask Ted who said it.
3. Write the page for a reader who was not in the conversation. Remove insider asides, inside
   jokes, and details that were resolved in the session but do not matter to a reader. Drop
   counts from headings ("Three risks"); the count is not important.
4. Record disagreements as disagreements, with who holds each position, rather than picking a
   winner. Label a page "investigation, not a plan" when that is what it is.
5. Verify claims against the source (code, docs, an API) before writing them. Mark anything
   unverified with a `verify` pill, and mark illustrative numbers as placeholders.
6. For a substantial page, ask an independent agent with a clean context to check it before
   telling Ted it is done. In practice this caught wrong arithmetic, circular reasoning, and
   dead cross-references left after renumbering.

## Page anatomy

Start every HTML file with two ABOUTME comments right after the doctype. The first says what
the page is; the second says where it came from or how to maintain it.

```html
<!DOCTYPE html>
<!-- ABOUTME: Notes on how sourdough hydration changes crumb structure. -->
<!-- ABOUTME: Written from the 2026-10-01 baking class transcript beside this file. -->
```

The header, in order: the backlink, an eyebrow (topic and date, small uppercase accent text),
the `h1`, a one or two sentence lede, and the freshness stamp as the last element.

```html
<header class="hero">
  <div class="hero-inner">
    <p class="back"><a href="../index.html">&larr; Notes index</a></p>
    <p class="eyebrow">Baking &middot; 2026-10-01</p>
    <h1>Hydration and crumb</h1>
    <p class="lede">What changes when dough goes from 65% to 80% water, and what to try next.</p>
    <p class="freshness" style="margin:14px 0 0;font-size:12.5px;opacity:.65">Contents last updated <time datetime="2026-10-03">2026-10-03</time></p>
  </div>
</header>
```

Body sections are numbered (`<h2><span class="num">01</span> Title</h2>`) with an `id` for
anchoring. Long pages get a two-column table of contents box near the top.

## The freshness stamp

- Bump it to today whenever you make a real content change. Leave it alone for typos, nav
  links, and styling.
- Use today's date, not the date of the meeting the page describes. That mistake happened.
- The stamp is inline-styled on purpose so it works even on pages with their own styles, and
  the lint keys on the `<time datetime>` attribute. List pages (`index.html`) are exempt.
- `just check-dates` lints the repo; the pre-commit hook enforces the bump (see tooling). For a
  genuinely cosmetic commit, use `SKIP_DATE_CHECK=1 git commit ...`, never `--no-verify`.

## Writing large pages in chunks

A single tool call that writes a large file can exceed the output limit, and the response is cut
off with "API Error: The response stopped arriving" or similar. Pages over roughly 40 KB are at
risk; finished pages in the earlier repo ran up to 157 KB. Build large pages in chunks:

1. `Write` the head, the header, and the first section or two. End the file
   with a sentinel line: `<!--CHUNK-->`.
2. Each following chunk is an `Edit` that replaces `<!--CHUNK-->` with the next block of content
   followed by a fresh `<!--CHUNK-->`. One or two sections, or one large SVG, per chunk.
3. The last chunk replaces the sentinel with the closing footer and `</body></html>`.
4. Validate the result with `just check-page <path>`.

If a response is cut off mid-write, do not retry the same large write. Check what landed on disk and continue in smaller chunks.

## Bulk edits

When you change many references at once with a pattern, verify with a different check than the
one you used to make the change. In the earlier repo, a substitution skipped matches preceded by
`>`, the verification grep had the same exclusion, and it reported clean while 24 references
were still wrong.

## Pages meant to be pasted elsewhere

- If Ted will copy content from a page into a ticket or another doc, add a copy button that
  generates Markdown from the DOM at click time, so it cannot drift from the page. Resolve
  relative links against the published URL so they still work after pasting.
- Give items stable anchors (`#S1`, `#S2`) that survive renames.
- Runnable code samples: commit the source file beside the page, show it in a `<details>` block
  with a copy button that reads `textContent`, and highlight with highlight.js from a CDN. Pair
  two theme stylesheets with `media="(prefers-color-scheme: dark)"` and `light`. Most readers
  will not have the code locally.

## Images

- Do not redraw raster source material (whiteboard photos, slides) as SVG. Retyping is
  error-prone in ways nobody will notice. Embed the image; spend SVG effort on diagrams the
  source did not have.
- Store large images as WebP.
- When converting transparent PNGs, flatten onto white. Converting straight to RGB composites
  onto black, which makes them unreadable.
- Images too wide for the text column can break out of it:
  `figure.board { width: min(1760px, 94vw); margin-left: calc(50% - min(880px, 47vw)); }` with
  an inner scroller (`overflow: auto; max-height: 78vh; background: #fff`) and an "open full
  size" link.

## Prose style

- No emoji, em-dashes, or hyperbole. Concise and skimmable: short paragraphs, real headings,
  tables where the content is tabular.
- Name things plainly. When a term is ambiguous, pick one name, define it, and use it
  consistently. If a name was chosen deliberately, say so in a callout so it does not get
  "simplified" back later.
- No rhetorical parallelism or "not X, but Y" constructions as labels.
- For pages aimed at a wider audience, Simplified Technical English (ASD-STE100) works well:
  short active sentences, one instruction each, no idioms.
