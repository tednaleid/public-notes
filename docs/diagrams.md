Read this when: adding or fixing a diagram, chart, or image on a page.

# Diagrams

## Which tool

1. **Hand-written inline SVG** is the default. It is version-controlled text, it follows light
   and dark mode through the CSS classes, the text stays selectable, and it needs no library.
2. **draw.io** when someone will want to edit the diagram later in a visual editor, or for a
   large poster. Commit the `.drawio` source and give the export its own page.
3. **Mermaid: no.** It was used early and replaced. The output looked generic, the layout was
   hard to control, and it needed a CDN script plus theme switching. Mermaid source is still a
   fine way to sketch a structure before drawing it properly.
4. **Excalidraw** was tried and reverted the same day. If it comes back, the `.excalidraw.svg`
   format (renders inline and stays editable) is the variant to use.

## Inline SVG rules

- Always set a `viewBox` and no fixed width; the CSS makes it `width: 100%; height: auto`.
- `role="img"` and an `aria-label` that is a full sentence describing what the diagram shows.
  The label also makes figures easy to target in render checks.
- Style through the shared classes (`.box`, `.abox`, `.title`, `.desc`, `.edge`, `.elbl`, ...),
  never with hard-coded colors. That is what makes diagrams work in both color schemes.
- Place every `<text>` with explicit `x`/`y`. Use `text-anchor="middle"` for centered labels.
- Group regions with comments (`<!-- row 1: inputs -->`).
- One arrowhead marker per SVG, with a **unique id per SVG on the page** (`ah1`, `ah2`, ...).
  Duplicate ids across SVGs on one page make arrowheads silently use the wrong definition.
- Wrap each SVG in `<figure>` with a `<figcaption>` that says what to notice.

```html
<figure>
<svg viewBox="0 0 760 170" role="img" aria-label="Raw input flows into an HTML page, which is published to the Pages site.">
  <defs>
    <marker id="ah1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" class="head"/>
    </marker>
  </defs>
  <!-- three columns: 220px boxes, 50px gutters, 20px margin -->
  <rect class="box"  x="20"  y="50" width="220" height="70" rx="10"/>
  <text class="title" x="130" y="80"  text-anchor="middle">Raw input</text>
  <text class="desc"  x="130" y="100" text-anchor="middle">transcript, screenshots</text>

  <rect class="abox" x="270" y="50" width="220" height="70" rx="10"/>
  <text class="title" x="380" y="80"  text-anchor="middle">HTML page</text>
  <text class="desc"  x="380" y="100" text-anchor="middle">stamped, linked from hub</text>

  <rect class="box"  x="520" y="50" width="220" height="70" rx="10"/>
  <text class="title" x="630" y="80"  text-anchor="middle">Pages site</text>
  <text class="desc"  x="630" y="100" text-anchor="middle">published on push</text>

  <!-- edges run gutter to gutter; labels sit above, centered on the gutter -->
  <path class="edge" d="M240 85 H268" marker-end="url(#ah1)"/>
  <path class="edge" d="M490 85 H518" marker-end="url(#ah1)"/>
  <text class="elbl" x="255" y="40" text-anchor="middle">write</text>
  <text class="elbl" x="505" y="40" text-anchor="middle">push</text>
</svg>
<figcaption>The usual path from a meeting to a published page.</figcaption>
</figure>
```

## Layout: use a grid

The fix that worked every time a diagram looked wrong was to rebuild it on an even grid. One
rebuild used three columns of 220px boxes with 90px gutters, so every arrow is a straight
horizontal or right-angle run and its label sits in the gutter directly above it. Before
drawing, write the grid down as a comment (column x positions, row y positions) and place
everything on it.

Failures this prevents, all seen in practice:

- A label drifted 100px away from the arrow it describes.
- An arrow starting inside its source box instead of at the edge.
- An elbow routed through a block of text for no reason.
- Numbered circles sitting on top of arrowheads (widening the gap from 32px to 68px fixed it).
- Text running past the box it belongs in, or past the right edge of the `viewBox`.

Rules of thumb: allow about 7px per character at 13px, 6px at 11.5px, and size boxes from the
longest line. Leave at least 20px inside each box edge. Labels go in gutters, never on lines.

## Render check: look at it in both modes

Never call a diagram done without seeing it. With `playwright-cli` (or any headless browser):

1. Serve the repo: `just serve` (port 8731).
2. Open the page and screenshot each figure, targeting it by its label:
   `screenshot "figure:has(svg[aria-label^='Raw input'])" --hires`.
3. Switch to dark (`emulateMedia({ colorScheme: 'dark' })`) and screenshot again. Then light.
   Both, every time.
4. Run the overlap check and a horizontal-overflow check
   (`document.documentElement.scrollWidth > document.documentElement.clientWidth`), and confirm
   every TOC `href="#id"` has a matching element.

`just check-svg <path>` runs the overlap check (`scripts/svg-overlap.js`) in a headless browser and
fails if any SVG text crosses a box edge or runs past the `viewBox`. In an open `playwright-cli`
session, `playwright-cli eval "$(cat scripts/svg-overlap.js)"` does the same.

## draw.io exports

- Commit the `.drawio` source beside the exported page. Pages serves it too, so anyone can open
  it in draw.io. The export page's second ABOUTME line and a visible note say "edit the .drawio
  beside this file and re-export; do not hand-edit the SVG."
- **Strip the PNG fallbacks.** The SVG export writes a raster `<switch>` fallback beside each
  `<foreignObject>` label. Removing them took one poster from 5.4 MB to 82 KB, and the text
  stayed live and selectable.
- **Lock the color scheme.** draw.io text uses `light-dark()` colors over hard-coded fills, so
  in OS dark mode the text turns near-black on dark panels. Wrap the export in an element with
  `color-scheme: only light;` and a comment saying why.
- **Posters get their own page.** A 3000px-wide poster scaled into a 980px column renders 13px
  text at about 3.5px. Give it a full-width page with "Fit to width" and "Actual size" toggle
  buttons (`aria-pressed`), and put a smaller hand-drawn SVG summary on the page that links to it.

## Charts

For charts with real data (bars, lines, distributions), use the `dataviz` skill if it is
available. Draw axes with `.axis`, bars with the translucent `.fill-*` classes, and label values
directly rather than relying on a legend.
