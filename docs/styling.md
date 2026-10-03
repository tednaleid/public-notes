Read this when: creating a page, adding a visual pattern, or changing how the site looks.

# Styling

## Principles

- **One shared stylesheet**, `assets/site.css`, linked by relative path
  (`<link rel="stylesheet" href="../assets/site.css">`). The earlier repo put a full `<style>`
  block in every page. Pages were self-contained but drifted: content widths ranged from 780 to
  1040px, and one late page lost dark mode entirely. A relative link still opens from disk with
  no build step. Page-specific rules (a one-off SVG class, a custom widget) go in a small
  `<style>` block in that page.
- **New pages start from `templates/page.html`**, never from a blank file and never from memory.
- **Dark by default, light by media query.** Light mode overrides only the surface and text
  colors. Accent colors work in both modes and stay the same.
- **No external fonts.** System font stacks only.
- **Check both color schemes** whenever you add a visual element (see diagrams for the
  render-check routine).

## assets/site.css

The stylesheet holds the color tokens, layout, callouts, tables, hub cards, and the SVG vocabulary
that `docs/diagrams.md` depends on. The values are tested. Re-theme by changing the tokens, not by
adding one-off colors.

## templates/page.html

Copy it to the new page's path, then fill in the ABOUTME lines, title, eyebrow, lede, and stamp.

Adjust the `../` depth to the page's location. The template's placeholder stamp fails the date
lint on purpose, so a page cannot be committed with it unfilled.

## Patterns worth knowing

- Callout variants carry meaning: accent for a general note, purple (`.q`) for an open question,
  red (`.warn`) for a risk, green (`.good`) for something settled.
- `ol.settled` for decisions, each with a `.why` line.
- `.pill.verify` marks a fact that has not been checked yet. Remove it once checked.
- `details`/`summary` for expandable answers so a long page stays skimmable.
- Wide tables go in `.tablewrap` so they scroll horizontally on narrow screens instead of
  breaking the layout.
- No print styles exist. Add them only if Ted starts printing.
