/* Shared slide components. Every options object is built fresh per call,
   because pptxgenjs mutates them in place on first use. */
const W = 13.3, H = 7.5, M = 0.62;
const INK = "0E1A22", TEAL = "1A5F59", TEAL2 = "5E9A91", LT = "EDF2F0",
      GREEN = "2F6B45", RED = "9C3A3A", AMBER = "B07A2E", SLATE = "5B6B78",
      WHITE = "FFFFFF";

/** Tinted card with optional heading + body lines. */
function card(slide, o) {
  slide.addShape("roundRect", {
    x: o.x, y: o.y, w: o.w, h: o.h, rectRadius: 0.06,
    fill: { color: o.fill || LT }, line: { color: o.line || "DCE5E2", width: 0.75 },
    objectName: o.name || "card",
  });
}

/** Small numbered/lettered chip — the deck's one repeated motif. */
function chip(slide, x, y, text, color) {
  slide.addShape("roundRect", {
    x, y, w: 0.42, h: 0.42, rectRadius: 0.12,
    fill: { color: color || TEAL }, line: { color: color || TEAL, width: 0 },
  });
  slide.addText(String(text), {
    x, y, w: 0.42, h: 0.42, align: "center", valign: "middle",
    fontSize: 14, bold: true, color: WHITE, margin: 0, isTextBox: true,
  });
}

function label(slide, x, y, w, text, color) {
  slide.addText(String(text).toUpperCase(), {
    x, y, w, h: 0.26, fontSize: 10, bold: true, charSpacing: 1.2,
    color: color || SLATE, margin: 0, isTextBox: true,
  });
}

function body(slide, x, y, w, h, runs, opts) {
  slide.addText(runs, Object.assign({
    x, y, w, h, fontSize: 13.5, color: INK, lineSpacing: 19,
    margin: 0, isTextBox: true, valign: "top",
  }, opts || {}));
}

/** Bulleted list where every item but the last breaks the line. */
function bullets(items, o) {
  return items.map((t, i) => ({
    text: typeof t === "string" ? t : t.text,
    options: Object.assign({ bullet: true, breakLine: i < items.length - 1 },
                           (typeof t === "object" && t.options) || {}, o || {}),
  }));
}

/** Big figure + caption. */
function stat(slide, x, y, w, value, caption, color) {
  slide.addText(String(value), {
    x, y, w, h: 0.72, fontSize: 40, bold: true, color: color || TEAL,
    margin: 0, isTextBox: true, fontFace: "Cambria",
  });
  slide.addText(String(caption), {
    x, y: y + 0.68, w, h: 0.56, fontSize: 11.5, color: SLATE,
    margin: 0, isTextBox: true, lineSpacing: 14,
  });
}

module.exports = { W, H, M, INK, TEAL, TEAL2, LT, GREEN, RED, AMBER, SLATE, WHITE,
                   card, chip, label, body, bullets, stat };
