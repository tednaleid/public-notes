// ABOUTME: Flags SVG text that crosses a box edge or runs past the viewBox, on every SVG in the page.
// ABOUTME: A function for playwright-cli eval; returns "clean" or a list of issues. See docs/diagrams.md.
() => {
  const issues = [];
  document.querySelectorAll("svg").forEach((svg, si) => {
    const vb = svg.viewBox.baseVal;
    const rects = [...svg.querySelectorAll("rect")].map(r => r.getBBox());
    svg.querySelectorAll("text").forEach(t => {
      const b = t.getBBox();
      const label = `svg#${si} "${t.textContent.trim().slice(0, 30)}"`;
      if (vb && (b.x < vb.x || b.x + b.width > vb.x + vb.width)) issues.push(`${label} outside viewBox`);
      rects.forEach(r => {
        const overlaps = b.x < r.x + r.width && b.x + b.width > r.x && b.y < r.y + r.height && b.y + b.height > r.y;
        const inside = b.x >= r.x && b.x + b.width <= r.x + r.width && b.y >= r.y && b.y + b.height <= r.y + r.height;
        if (overlaps && !inside) issues.push(`${label} crosses a box edge`);
      });
    });
  });
  return issues.length ? issues : "clean";
}
