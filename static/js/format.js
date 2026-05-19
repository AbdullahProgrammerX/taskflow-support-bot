/** Lightweight markdown subset for assistant messages (no external deps). */
export function formatMarkdown(text) {
  if (!text) return "";

  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return escaped
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p>")
    .concat("</p>")
    .replace(/<p><\/p>/g, "");
}

/** Deduplicate sources by file, keep first excerpt per file. */
export function dedupeSources(sources) {
  const seen = new Map();
  for (const src of sources || []) {
    if (!seen.has(src.file)) seen.set(src.file, src);
  }
  return [...seen.values()];
}
