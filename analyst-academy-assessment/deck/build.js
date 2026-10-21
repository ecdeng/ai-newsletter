const pptxgen = require("pptxgenjs");
const { THEME } = require("./theme.js");
const L = require("./lib.js");
const { W, H, M, INK, TEAL, TEAL2, LT, GREEN, RED, AMBER, SLATE, WHITE,
        card, chip, label, body, bullets, stat } = L;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.3 x 7.5 — set BEFORE any slide
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Fundamental Edge — Analyst Academy";
pres.title = "The Historical Case Engine";
pres.subject = "Assessment infrastructure for the Analyst Academy";
const C = pres.SchemeColor;

/* ---------------------------------------------------------------- layouts */
pres.defineSlideMaster({
  title: "TITLE", background: { color: INK },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.5, w: 10.4, h: 1.5,
        fontSize: 40, bold: true, color: WHITE, fontFace: "Cambria", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.05, w: 9.6, h: 1.5,
        fontSize: 15, color: "AEC2BE", margin: 0, lineSpacing: 21 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "SECTION", background: { color: TEAL },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.9, w: 11.0, h: 1.2,
        fontSize: 34, bold: true, color: WHITE, fontFace: "Cambria", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.15, w: 10.0, h: 1.0,
        fontSize: 14.5, color: "CFE2DE", margin: 0, lineSpacing: 20 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENT", background: { color: WHITE },
  slideNumber: { x: 12.5, y: 7.02, w: 0.5, h: 0.3, fontSize: 9, color: "A7B4B1", align: "right" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.44, w: 12.1, h: 0.62,
        fontSize: 27, bold: true, color: INK, fontFace: "Cambria", margin: 0, valign: "middle" }, text: "" } },
    { text: { text: "The Historical Case Engine  ·  INF-1",
      options: { x: M, y: 7.02, w: 6, h: 0.3, fontSize: 9, color: "A7B4B1", margin: 0, isTextBox: true } } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENT_DARK", background: { color: INK },
  slideNumber: { x: 12.5, y: 7.02, w: 0.5, h: 0.3, fontSize: 9, color: "5B6B78", align: "right" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.44, w: 12.1, h: 0.62,
        fontSize: 27, bold: true, color: WHITE, fontFace: "Cambria", margin: 0, valign: "middle" }, text: "" } },
    { text: { text: "The Historical Case Engine  ·  INF-1",
      options: { x: M, y: 7.02, w: 6, h: 0.3, fontSize: 9, color: "5B6B78", margin: 0, isTextBox: true } } },
  ],
});

const S = (master, section) => pres.addSlide({ masterName: master, sectionTitle: section });

/* ============================================================ 1. TITLE */
pres.addSection({ title: "Opening" });
let s = S("TITLE", "Opening");
s.addText("The Historical Case Engine", { placeholder: "title" });
s.addText([
  { text: "How students practise a full investment decision on a real company — ", options: {} },
  { text: "with the clock frozen, and the answer already known", options: { bold: true, color: WHITE } },
], { placeholder: "body" });
s.addText("Assessment infrastructure for the Analyst Academy  ·  INF-1", {
  x: M, y: 5.9, w: 9, h: 0.3, fontSize: 11.5, color: TEAL2, margin: 0, isTextBox: true, charSpacing: 0.8 });
s.addNotes("The engine is the keystone infrastructure in the assessment blueprint. It serves roughly half the exercises. The point-in-time data layer is already built and tested against live SEC data.");

/* ============================================================ 2. PROBLEM */
s = S("CONTENT", "Opening");
s.addText("You cannot grade an analyst on whether the stock went up", { placeholder: "title" });
body(s, M, 1.22, 7.1, 1.5, [
  { text: "Investing is a low-validity domain. ", options: { bold: true } },
  { text: "Deliberate practice needs well-defined tasks, immediate feedback, repetition and error correction — and stock picking natively supplies none of them. Over a 12-week course, a single idea's outcome is almost pure noise.", options: {} },
]);
card(s, { x: 8.1, y: 1.15, w: 4.6, h: 2.05, fill: "F5F8F7" });
stat(s, 8.45, 1.42, 4.0, "15.37 yrs", "to establish skill at 95% confidence, at an information ratio of 0.50 — longer than the program, longer than most analyst tenures", TEAL);

label(s, M, 3.15, 6, "So the engine grades three things instead");
const graded = [
  ["Process fidelity", "Did they do the work in the right order, and did their action follow their own stated plan?"],
  ["Analytical accuracy", "Checkable arithmetic: the bridge, the implied move, the forward bar. Auto-graded against a key."],
  ["Forecast calibration", "Probabilities scored by a proper rule. Because the case is historical, resolution is instant and free."],
];
graded.forEach((g, i) => {
  const x = M + i * 4.07;
  card(s, { x, y: 3.52, w: 3.82, h: 2.0 });
  chip(s, x + 0.26, 3.78, i + 1);
  s.addText(g[0], { x: x + 0.8, y: 3.8, w: 2.8, h: 0.36, fontSize: 15, bold: true, color: INK, margin: 0, isTextBox: true });
  body(s, x + 0.26, 4.32, 3.3, 1.0, g[1], { fontSize: 12, color: "3C4A50", lineSpacing: 16 });
});
s.addText("Outcome is revealed to the student — but it is never the grade.", {
  x: M, y: 5.78, w: 11, h: 0.32, fontSize: 13, italic: true, color: TEAL, margin: 0, isTextBox: true });
s.addNotes("This is the single most important design decision. Everything downstream follows from it.");

/* ============================================================ 3. NOT A SIMULATOR */
s = S("CONTENT", "Opening");
s.addText("Why this is not a market simulator", { placeholder: "title" });
const cmp = [
  ["A trading simulator", RED, [
    "Optimises for execution and live price feedback",
    "Runs on a seconds-to-days clock",
    "Its distinguishing feature — price feedback — is the least valid signal available here",
    "Expensive real-time infrastructure",
    "Rewards the overconfidence the course is trying to train out",
  ]],
  ["A historical case engine", GREEN, [
    "Optimises for thesis formation and position maintenance",
    "Runs on the quarters clock fundamental analysis actually uses",
    "Compresses a three-year holding period into a 40-minute exercise",
    "No real-time infrastructure at all",
    "Ground truth is free: the answer already happened",
  ]],
];
cmp.forEach((col, i) => {
  const x = M + i * 6.2;
  card(s, { x, y: 1.25, w: 5.9, h: 4.45, fill: i ? "EEF4F0" : "FAF2F2", line: i ? "CFE0D6" : "E8D4D4" });
  s.addText(col[0], { x: x + 0.32, y: 1.5, w: 5.2, h: 0.4, fontSize: 17, bold: true, color: col[1], margin: 0, isTextBox: true, fontFace: "Cambria" });
  s.addText(bullets(col[2]), { x: x + 0.32, y: 2.05, w: 5.26, h: 3.4, fontSize: 12.5, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 9, lineSpacing: 16 });
});
s.addText("You would spend the most money to measure the least.", {
  x: M, y: 5.92, w: 11.5, h: 0.4, fontSize: 15, bold: true, italic: true, color: INK, margin: 0, isTextBox: true });
s.addNotes("The verdict is not budgetary. A simulator is a category error for a quarters-clock curriculum.");

/* ============================================================ 4. CORE IDEA */
s = S("CONTENT_DARK", "Opening");
s.addText("The value is not realism", { placeholder: "title" });
s.addText([
  { text: "It is time compression ", options: { color: TEAL2, bold: true } },
  { text: "plus ", options: { color: "AEC2BE" } },
  { text: "free ground truth.", options: { color: TEAL2, bold: true } },
], { x: M, y: 1.3, w: 11.5, h: 0.55, fontSize: 25, margin: 0, isTextBox: true, fontFace: "Cambria" });
body(s, M, 2.05, 11.6, 0.8,
  "Freeze a date on a real company. Serve only what was knowable then. The student produces a thesis and a position; the clock advances; the market answers. A three-year holding period becomes a 40-minute exercise in which the correct answer already exists and costs nothing to obtain.",
  { color: "C6D4D1", fontSize: 14.5, lineSpacing: 21 });
const boons = [
  ["Identical stimulus", "Every student sees exactly the same pack, so their scores are comparable — the property that makes an OSCE work."],
  ["Reusable answer keys", "One expensive authoring effort is amortised across every cohort, forever."],
  ["Instant resolution", "Calibration questions resolve the moment the clock advances. No waiting a quarter for truth."],
];
boons.forEach((b, i) => {
  const x = M + i * 4.07;
  card(s, { x, y: 3.3, w: 3.82, h: 1.95, fill: "17262E", line: "2A3A42" });
  s.addText(b[0], { x: x + 0.3, y: 3.56, w: 3.3, h: 0.34, fontSize: 14.5, bold: true, color: TEAL2, margin: 0, isTextBox: true });
  body(s, x + 0.3, 3.98, 3.26, 1.1, b[1], { fontSize: 12, color: "AEC2BE", lineSpacing: 16 });
});
s.addText("A fixed library of 20–40 cases is better assessment than a dynamic any-company engine — and costs a fraction of it.", {
  x: M, y: 5.6, w: 11.8, h: 0.5, fontSize: 13.5, italic: true, color: "8FA8A3", margin: 0, isTextBox: true });
s.addNotes("The apparent limitation — a fixed library — is the design virtue.");

/* ============================================================ 5. THE CLOCK */
s = S("CONTENT", "Opening");
s.addText("How one case runs", { placeholder: "title" });
label(s, M, 1.2, 8, "The clock — the student never sees a step before it unlocks");
const steps = [
  ["T − 5d", "Brief opens", "Student receives the pack: as-filed financials, filings, transcripts, the bar, price."],
  ["T", "Decision", "Thesis, model, price target, scenario probabilities, sizing — and a written pre-commitment."],
  ["T + 1q", "The print", "The real quarter is released. 15-minute first read, then re-set the forward bar."],
  ["T + 60d", "Resolution", "Outcome revealed. Forecasts scored for calibration. Forced post-mortem."],
];
const sw = 2.82, gap = 0.33;
steps.forEach((st, i) => {
  const x = M + i * (sw + gap);
  card(s, { x, y: 1.6, w: sw, h: 2.5 });
  s.addShape("roundRect", { x: x + 0.22, y: 1.82, w: 1.05, h: 0.34, rectRadius: 0.1,
    fill: { color: TEAL }, line: { color: TEAL, width: 0 } });
  s.addText(st[0], { x: x + 0.22, y: 1.82, w: 1.05, h: 0.34, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(st[1], { x: x + 0.22, y: 2.3, w: 2.4, h: 0.32, fontSize: 14.5, bold: true, color: INK, margin: 0, isTextBox: true });
  body(s, x + 0.22, 2.68, 2.4, 1.3, st[2], { fontSize: 11.5, color: "3C4A50", lineSpacing: 15 });
  if (i < 3) s.addShape("rightArrow", { x: x + sw + 0.03, y: 2.72, w: 0.27, h: 0.18,
    fill: { color: "C3D2CE" }, line: { color: "C3D2CE", width: 0 } });
});
card(s, { x: M, y: 4.35, w: 12.06, h: 1.5, fill: "F5F8F7" });
s.addText("Answers lock when a step closes", { x: M + 0.3, y: 4.58, w: 6, h: 0.34, fontSize: 14.5, bold: true, color: TEAL, margin: 0, isTextBox: true });
body(s, M + 0.3, 4.98, 11.4, 0.8,
  "The lock is the instrument, not a convenience. Three exercises are only valid because the earlier submission cannot be revised: the two-phase core-debate drill, the earnings pre-commitment, and the forced re-underwrite that measures thesis creep.",
  { fontSize: 12.5, color: "3C4A50", lineSpacing: 17 });
s.addNotes("Each unlock serves a different module: T is Module 10 and 11, T+1q is Module 13, T+60d is Module 14.");


/* ============================================================ 6. ARCHITECTURE */
s = S("CONTENT", "Opening");
s.addText("Four layers — two of them already built", { placeholder: "title" });
const layers = [
  ["1", "Data", "pit/client.py · pit/comps.py", "As-of filtering, restatement detection, rate limiting, on-disk cache.", "BUILT & TESTED", GREEN],
  ["2", "Authoring", "pit/case.py", "CaseManifest schema, facts_from_sec(), and validate_pit_safety() — the guardrail.", "BUILT & TESTED", GREEN],
  ["3", "Runtime", "clock · submission store", "Step-by-step reveal, append-only submissions, hard locks, student_view().", "SPECIFIED", SLATE],
  ["4", "Grading", "deterministic · INF-2 · INF-6", "Check cells and traps; the model auto-grader; the LLM rubric grader on a golden set.", "SPECIFIED", SLATE],
];
layers.forEach((ly, i) => {
  const y = 1.3 + i * 1.18;
  card(s, { x: M, y, w: 12.06, h: 1.02, fill: i < 2 ? "EEF4F0" : "F7F8F8", line: i < 2 ? "CFE0D6" : "E2E6E5" });
  chip(s, M + 0.26, y + 0.3, ly[0], i < 2 ? TEAL : SLATE);
  s.addText(ly[1], { x: M + 0.86, y: y + 0.18, w: 1.6, h: 0.32, fontSize: 15, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addText(ly[2], { x: M + 0.86, y: y + 0.54, w: 2.6, h: 0.3, fontSize: 10.5, color: SLATE, margin: 0, isTextBox: true, fontFace: "Courier New" });
  body(s, M + 3.7, y + 0.26, 6.3, 0.7, ly[3], { fontSize: 12.5, color: "3C4A50", lineSpacing: 16 });
  s.addShape("roundRect", { x: M + 10.3, y: y + 0.32, w: 1.5, h: 0.34, rectRadius: 0.1,
    fill: { color: ly[5] }, line: { color: ly[5], width: 0 } });
  s.addText(ly[4], { x: M + 10.3, y: y + 0.32, w: 1.5, h: 0.34, align: "center", valign: "middle",
    fontSize: 8.5, bold: true, color: WHITE, margin: 0, isTextBox: true, charSpacing: 0.5 });
});
s.addText("Manifests are JSON in version control, not rows in a database — a case is editorial content with an answer key, and it should be reviewable and diffable.", {
  x: M, y: 6.1, w: 12.06, h: 0.5, fontSize: 12.5, italic: true, color: SLATE, margin: 0, isTextBox: true });
s.addNotes("13 of 13 smoke tests pass against the live SEC API as of 21 Oct 2026.");

/* ============================================================ 7. THE LEAK (chart) */
s = S("CONTENT", "Opening");
s.addText("Why point-in-time discipline is the whole game", { placeholder: "title" });
body(s, M, 1.2, 6.0, 1.5, [
  { text: "Envista Holdings reported FY2019 revenue of $2.7516bn in its 2020 and 2021 10-Ks — then $2.2848bn in its 2022 10-K, after a discontinued-operations reclassification.\n\n", options: {} },
  { text: "An analyst in June 2021 saw $2.75bn. A current database shows $2.28bn.", options: { bold: true } },
]);
card(s, { x: M, y: 2.95, w: 6.0, h: 1.45, fill: "FAF2F2", line: "E8D4D4" });
s.addText("−$467m   ·   −17.0%", { x: M + 0.3, y: 3.15, w: 5.4, h: 0.5, fontSize: 24, bold: true,
  color: RED, margin: 0, isTextBox: true, fontFace: "Cambria" });
body(s, M + 0.3, 3.68, 5.4, 0.6, "A case built from today's data hands the student a revenue base the market never saw — and every growth rate, margin and multiple derived from it is wrong.",
  { fontSize: 11.5, color: "5A3A3A", lineSpacing: 15 });
s.addChart(pres.ChartType.bar, [
  { name: "As filed at the time", labels: ["FY2019", "FY2020"], values: [2.7516, 2.2820] },
  { name: "As the record shows today", labels: ["FY2019", "FY2020"], values: [2.2848, 1.9291] },
], {
  x: 7.0, y: 1.3, w: 5.7, h: 4.3,
  barDir: "col", barGrouping: "clustered", barGapWidthPct: 55,
  chartColors: [TEAL, "C98B8B"],
  showTitle: true, title: "Envista revenue, $bn — same periods, two answers",
  titleFontFace: "+mn-lt", titleFontSize: 12, titleColor: INK,
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10,
  dataLabelFontFace: "+mn-lt", dataLabelColor: INK, dataLabelFormatCode: "0.00",
  catAxisLabelColor: SLATE, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt",
  valAxisLabelColor: SLATE, valAxisLabelFontSize: 10, valAxisLabelFontFace: "+mn-lt",
  valAxisMaxVal: 3.2, valGridLine: { color: "E6EBEA", size: 0.75 },
  catGridLine: { style: "none" },
  showLegend: true, legendPos: "b", legendFontFace: "+mn-lt", legendFontSize: 10.5, legendColor: SLATE,
});
s.addText("Source: SEC XBRL companyconcept API, CIK 1757073, accession numbers 0001628280-20-001914 and 0001628280-22-003981.", {
  x: M, y: 6.25, w: 12.06, h: 0.3, fontSize: 9.5, color: "A7B4B1", margin: 0, isTextBox: true });
s.addNotes("This is a real, verified example pulled live from the SEC API. It is also Case C in this deck.");

/* ============================================================ 8. FOUR LEAKS */
s = S("CONTENT", "Opening");
s.addText("Four ways the future leaks in, and how each is closed", { placeholder: "title" });
const leakRows = [
  ["Restated financials", "Today's database shows restatements; the analyst at T saw as-first-reported numbers.", "Closed, free. The SEC stamps every fact with its filing date, so as_of() filters on it."],
  ["Index survivorship", "Today's constituent list is not the list at T, biasing any comp set built from it.", "Hard-code the comp set in the manifest from a contemporaneous document, never a current index."],
  ["Delisting survivorship", "Cheap price feeds drop dead tickers, so the worst outcomes vanish from the library.", "Use a vendor whose reference data keeps delisted tickers — and deliberately include failures."],
  ["The author's own knowledge", "An author who knows the ending writes exhibits that quietly foreshadow it.", "Process, not code: a second author writes the expert key cold, seeing only T-dated material."],
];
const tbl = [[
  { text: "LEAK", options: { bold: true, color: WHITE, fill: { color: TEAL }, fontSize: 10, margin: 6 } },
  { text: "WHAT GOES WRONG", options: { bold: true, color: WHITE, fill: { color: TEAL }, fontSize: 10, margin: 6 } },
  { text: "HOW IT IS CLOSED", options: { bold: true, color: WHITE, fill: { color: TEAL }, fontSize: 10, margin: 6 } },
]].concat(leakRows.map((r, i) => [
  { text: r[0], options: { bold: true, color: INK, fontSize: 12, margin: 6, fill: { color: i % 2 ? "F7FAF9" : WHITE } } },
  { text: r[1], options: { color: "3C4A50", fontSize: 11.5, margin: 6, fill: { color: i % 2 ? "F7FAF9" : WHITE } } },
  { text: r[2], options: { color: "3C4A50", fontSize: 11.5, margin: 6, fill: { color: i % 2 ? "F7FAF9" : WHITE } } },
]));
s.addTable(tbl, { x: M, y: 1.28, w: 12.06, colW: [2.5, 4.4, 5.16],
  border: { type: "solid", color: "E2E8E6", pt: 0.75 }, valign: "top", autoPage: false });
s.addText("Authoring a case by hand will leak the future, and the leak is silent. That is why it is checked mechanically rather than left to discipline.", {
  x: M, y: 5.95, w: 12.06, h: 0.5, fontSize: 13, italic: true, color: INK, margin: 0, isTextBox: true });
s.addNotes("Leak 4 is the subtle one and the only one code cannot catch.");

/* ============================================================ 9. VALIDATOR */
s = S("CONTENT_DARK", "Opening");
s.addText("The guardrail: validate_pit_safety()", { placeholder: "title" });
body(s, M, 1.22, 11.8, 0.6,
  "Every manifest is checked against the SEC's own filing dates before it can ship. Run it in CI — a leaked case is worse than no case, because it teaches students the information was gettable.",
  { color: "C6D4D1", fontSize: 13.5, lineSpacing: 19 });
card(s, { x: M, y: 2.0, w: 12.06, h: 2.62, fill: "17262E", line: "2A3A42" });
s.addText([
  { text: "MISMATCH", options: { color: "E79C9C", bold: true, breakLine: false } },
  { text: ": Revenues 2019-12-31 manifest says 2,284,800,000 but accn\n0001628280-20-001914 reports 2,751,600,000. This is the signature of a\nvalue copied from a CURRENT database rather than the as-filed document.\n\n", options: { color: "D8E2E0" } },
  { text: "LEAK", options: { color: "E79C9C", bold: true } },
  { text: ": fact GrossProfit 2019-01-01..2019-12-31 was filed 2022-02-24,\nafter the freeze date 2020-06-30.\n\n", options: { color: "D8E2E0" } },
  { text: "DEGENERATE", options: { color: "E7C89C", bold: true } },
  { text: ": calibration question Q9 resolves 2020-01-01, on or before\nthe freeze date — it is already knowable.", options: { color: "D8E2E0" } },
], { x: M + 0.34, y: 2.26, w: 11.4, h: 2.1, fontSize: 11, fontFace: "Courier New", margin: 0, isTextBox: true, lineSpacing: 15 });
const checks = [
  ["No fact filed after T", "Every served value's filing date is on or before the freeze date."],
  ["Every value exists in the record", "Checked against its accession number — this is what catches a pasted current figure."],
  ["No filing dated after T", "The filing list the student browses is itself time-bounded."],
  ["No question resolves before T", "A calibration question answerable from the pack is not a forecast."],
];
checks.forEach((c, i) => {
  const x = M + (i % 2) * 6.05, y = 4.9 + Math.floor(i / 2) * 0.82;
  s.addText("✓", { x, y, w: 0.3, h: 0.3, fontSize: 14, bold: true, color: TEAL2, margin: 0, isTextBox: true });
  s.addText(c[0], { x: x + 0.32, y, w: 5.6, h: 0.28, fontSize: 12.5, bold: true, color: WHITE, margin: 0, isTextBox: true });
  body(s, x + 0.32, y + 0.28, 5.5, 0.4, c[1], { fontSize: 10.5, color: "8FA8A3", lineSpacing: 13 });
});
s.addNotes("All three mechanical leak classes are covered by tests that pass today.");

/* ============================================================ 10. DATA */
s = S("CONTENT", "Opening");
s.addText("Where the data comes from", { placeholder: "title" });
card(s, { x: M, y: 1.25, w: 5.9, h: 2.5, fill: "EEF4F0", line: "CFE0D6" });
s.addText("Free, and verified reachable", { x: M + 0.32, y: 1.5, w: 5.2, h: 0.36, fontSize: 16, bold: true, color: GREEN, margin: 0, isTextBox: true, fontFace: "Cambria" });
s.addText(bullets([
  "SEC XBRL — companyconcept, companyfacts, submissions, frames",
  "Every fact carries its filing date and accession number",
  "Solves the restatement leak outright, at no cost",
  "Transcripts from IR sites for a fixed library",
]), { x: M + 0.32, y: 1.95, w: 5.3, h: 1.7, fontSize: 12, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 7, lineSpacing: 15 });
card(s, { x: 6.78, y: 1.25, w: 5.9, h: 2.5, fill: "FDF8EF", line: "EADCC2" });
s.addText("Costs money", { x: 7.1, y: 1.5, w: 5.2, h: 0.36, fontSize: 16, bold: true, color: AMBER, margin: 0, isTextBox: true, fontFace: "Cambria" });
s.addText(bullets([
  "Prices with delisted tickers — the cheapest real gap",
  "Historical index membership, only for index-flow cases",
  "Historical option chains — or hand-curate one straddle per case",
  "Historical consensus — the one genuine gap",
]), { x: 7.1, y: 1.95, w: 5.3, h: 1.7, fontSize: 12, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 7, lineSpacing: 15 });
card(s, { x: M, y: 3.95, w: 12.06, h: 1.85, fill: "F5F8F7" });
s.addText("The consensus gap, and the recommended workaround", { x: M + 0.32, y: 4.18, w: 8, h: 0.34, fontSize: 15, bold: true, color: TEAL, margin: 0, isTextBox: true });
body(s, M + 0.32, 4.58, 11.4, 1.1, [
  { text: "Start by using management guidance as the bar instead of consensus — ", options: { bold: true } },
  { text: "it is in the 8-K, the release and the transcript, so it is free, point-in-time and unambiguous. For a production library, hand-curate consensus for the fixed cases: 20–40 cases is a few hundred data points, and the figures are quoted verbatim in contemporaneous coverage and in the transcripts themselves. Record the provenance either way — a case whose bar is guidance tests a subtly different skill than one whose bar is consensus.", options: {} },
], { fontSize: 12.5, color: "3C4A50", lineSpacing: 17 });
s.addText("Two gotchas found by building it: the SEC requires an email-style User-Agent (a URL alone returns 403), and data.sec.gov and www.sec.gov have separate reachability — you can end up with every number and no documents.", {
  x: M, y: 6.0, w: 12.06, h: 0.6, fontSize: 11.5, italic: true, color: SLATE, margin: 0, isTextBox: true, lineSpacing: 15 });
s.addNotes("Do not budget from circulating vendor prices — several are no longer published.");

/* ============================================================ 11. DIVIDER */
pres.addSection({ title: "Worked cases" });
s = S("SECTION", "Worked cases");
s.addText("Three cases a student can walk through", { placeholder: "title" });
s.addText("For each: what they are given, what they must produce, how it is graded, and what a good and a bad answer actually look like.", { placeholder: "body" });
const caseList = [
  ["A", "The raise that was smaller than the beat", "Free data"],
  ["B", "Eight years of twelve percent", "Free data"],
  ["C", "The numbers you were never shown", "Already built"],
];
caseList.forEach((c, i) => {
  const x = M + i * 4.07;
  s.addShape("roundRect", { x, y: 5.2, w: 3.82, h: 1.25, rectRadius: 0.06,
    fill: { color: "15544F" }, line: { color: "2E6E68", width: 0.75 } });
  chip(s, x + 0.26, 5.44, c[0], "0F3F3A");
  s.addText(c[1], { x: x + 0.82, y: 5.42, w: 2.85, h: 0.6, fontSize: 13, bold: true, color: WHITE, margin: 0, isTextBox: true, lineSpacing: 16 });
  s.addText(c[2], { x: x + 0.82, y: 6.02, w: 2.85, h: 0.26, fontSize: 10, color: "9FC7C2", margin: 0, isTextBox: true });
});

/* ---------- reusable: resources / task / grading blocks ---------- */
function caseHeader(sl, letter, title, sub) {
  chip(sl, M, 1.2, letter, TEAL);
  sl.addText(title, { x: M + 0.58, y: 1.18, w: 9.4, h: 0.4, fontSize: 17, bold: true,
    color: INK, margin: 0, isTextBox: true, fontFace: "Cambria" });
  if (sub) sl.addText(sub, { x: M + 0.58, y: 1.56, w: 11.4, h: 0.3, fontSize: 11.5, color: SLATE, margin: 0, isTextBox: true });
}

/* ============================================================ 12. CASE A — pack */
s = S("CONTENT", "Worked cases");
s.addText("Case A — what the student is given", { placeholder: "title" });
caseHeader(s, "A", "The raise that was smaller than the beat", "Serves Modules 13, 06 and 10  ·  freeze date T = the morning of the Q2 print");
label(s, M, 2.05, 6, "Reference pack served at T");
const packA = [
  ["Segment financials", "Eight quarters, as-filed — every figure carries its filing date and accession number"],
  ["Filings", "Every 10-K, 10-Q and 8-K filed on or before T, and nothing after it"],
  ["Transcripts", "The last two earnings calls, including the Q&A"],
  ["The bar", "Management's FY guidance as given at Q1, plus hand-curated consensus revenue and EPS"],
  ["Market data", "Price, forward multiple vs. its own history, and one ATM straddle price"],
];
packA.forEach((p, i) => {
  const y = 2.4 + i * 0.63;
  card(s, { x: M, y, w: 6.0, h: 0.55, fill: i % 2 ? "F7FAF9" : WHITE, line: "E2E8E6" });
  s.addText(p[0], { x: M + 0.2, y: y + 0.05, w: 1.95, h: 0.45, fontSize: 11.5, bold: true, color: TEAL, margin: 0, isTextBox: true, valign: "middle" });
  s.addText(p[1], { x: M + 2.2, y: y + 0.05, w: 3.65, h: 0.45, fontSize: 10.5, color: "3C4A50", margin: 0, isTextBox: true, valign: "middle", lineSpacing: 13 });
});
label(s, 6.9, 2.05, 6, "What they must produce — five timed deliverables");
const delA = [
  ["T − 2", "Preview memo, 90 min", "The bar, our number, positioning, risk/reward — and a written pre-commitment of what we do in each outcome"],
  ["T", "First read, 15 min", "Five fixed stages, starting with the guidance paragraph"],
  ["T + 90min", "Updated model", "Re-set the forward bar, the multiple and the gap"],
  ["next open", "Action + sizing", "Buy, hold, trim or exit, with the size"],
  ["T + 60d", "Post-mortem", "Scored against their own pre-commitment"],
];
delA.forEach((d, i) => {
  const y = 2.4 + i * 0.63;
  card(s, { x: 6.9, y, w: 5.78, h: 0.55, fill: i % 2 ? "F7FAF9" : WHITE, line: "E2E8E6" });
  s.addText(d[0], { x: 7.05, y: y + 0.05, w: 0.95, h: 0.45, fontSize: 9.5, bold: true, color: WHITE, margin: 0,
    isTextBox: true, valign: "middle", align: "center", fill: { color: SLATE } });
  s.addText(d[1], { x: 8.08, y: y + 0.04, w: 1.75, h: 0.47, fontSize: 10.5, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle", lineSpacing: 12 });
  s.addText(d[2], { x: 9.9, y: y + 0.04, w: 2.7, h: 0.47, fontSize: 9.5, color: "3C4A50", margin: 0, isTextBox: true, valign: "middle", lineSpacing: 11.5 });
});
s.addText("Total student time ≈ 4 hours across the sequence. Fourteen traps are planted in the pack; each is scored independently, so catching three of four earns three-quarters of the marks.", {
  x: M, y: 5.78, w: 12.06, h: 0.5, fontSize: 12, italic: true, color: SLATE, margin: 0, isTextBox: true, lineSpacing: 16 });
s.addNotes("The pre-commitment table at T-2 is what makes the later action gradable.");

/* ============================================================ 13. CASE A — the arithmetic */
s = S("CONTENT", "Worked cases");
s.addText("Case A — the arithmetic hiding inside a guidance raise", { placeholder: "title" });
body(s, M, 1.2, 12.06, 0.4, [
  { text: "The print: ", options: { bold: true } },
  { text: "Q2 revenue beats by $30m. FY guidance is raised by $20m. Management's call language is confident. Every headline reads “beat and raise.”", options: {} },
]);
const bridge = [
  ["$30m", "Q2 revenue beat", SLATE],
  ["$20m", "FY guidance raise", SLATE],
  ["−$10m", "implied 2H revenue", RED],
];
bridge.forEach((b, i) => {
  const x = M + i * 3.0;
  card(s, { x, y: 1.85, w: 2.72, h: 1.12, fill: i === 2 ? "FAF2F2" : "F5F8F7", line: i === 2 ? "E8D4D4" : "DCE5E2" });
  s.addText(b[0], { x: x + 0.2, y: 1.98, w: 2.3, h: 0.5, fontSize: 24, bold: true, color: b[2], margin: 0, isTextBox: true, fontFace: "Cambria" });
  s.addText(b[1], { x: x + 0.2, y: 2.5, w: 2.3, h: 0.3, fontSize: 10.5, color: SLATE, margin: 0, isTextBox: true });
  if (i < 2) s.addText(i === 0 ? "−" : "=", { x: x + 2.74, y: 2.2, w: 0.26, h: 0.4, fontSize: 18, bold: true,
    color: SLATE, align: "center", margin: 0, isTextBox: true });
});
card(s, { x: 9.68, y: 1.85, w: 3.0, h: 1.12, fill: TEAL, line: TEAL });
s.addText("14.17 pts", { x: 9.88, y: 1.98, w: 2.6, h: 0.5, fontSize: 24, bold: true, color: WHITE, margin: 0, isTextBox: true, fontFace: "Cambria" });
s.addText("of deceleration, inside a raise", { x: 9.88, y: 2.5, w: 2.6, h: 0.3, fontSize: 10.5, color: "BFD9D5", margin: 0, isTextBox: true });

label(s, M, 3.15, 6, "The chain, step by step");
const chain = [
  "Implied 2H revenue falls from $2,030m to $2,020m — the raise is $10m smaller than the beat",
  "1H growth was +12.71%; implied 2H growth is −1.46%",
  "That gap decomposes: 2.70 pts is a harder comp, 11.47 pts is a genuine implied slowdown  (2.70 + 11.47 = 14.17 ✓)",
  "Implied Q4 is −2.86% y/y, while FY+1 consensus requires +6.16%",
];
s.addText(bullets(chain), { x: M, y: 3.5, w: 7.5, h: 1.9, fontSize: 12.5, color: INK, margin: 0, isTextBox: true, paraSpaceAfter: 9, lineSpacing: 17 });
card(s, { x: 8.4, y: 3.42, w: 4.28, h: 2.0, fill: "FDF8EF", line: "EADCC2" });
s.addText("The kill shot", { x: 8.68, y: 3.62, w: 3.8, h: 0.3, fontSize: 13, bold: true, color: AMBER, margin: 0, isTextBox: true });
body(s, 8.68, 3.96, 3.75, 1.3, "A 9-point reacceleration that nobody has underwritten — derived from arithmetic alone, with no view of the business required.",
  { fontSize: 12, color: "6B5424", lineSpacing: 16 });
s.addText("This is the whole case: the headline says beat-and-raise, and the arithmetic says the second half just got worse.", {
  x: M, y: 5.68, w: 12.06, h: 0.4, fontSize: 13.5, bold: true, italic: true, color: INK, margin: 0, isTextBox: true });
s.addNotes("Every figure here is independently verified; the decomposition sums exactly.");

/* ============================================================ 14. CASE A — grading */
s = S("CONTENT", "Worked cases");
s.addText("Case A — how the response is graded", { placeholder: "title" });
const gradeCols = [
  ["Deterministic", "55 pts", TEAL, [
    "Model update checked against the golden model by check cells",
    "Perturbation test: change an input, confirm outputs move correctly",
    "The bridge, implied 2H, both 2-year stack conventions, the exit rate",
    "Fourteen planted traps, each scored independently",
  ]],
  ["Rubric-graded", "45 pts", TEAL2, [
    "Preview-memo quality against anchored 0–5 scales",
    "First-read discipline — did they read guidance first?",
    "Pre-commitment consistency: did the action match the plan, and if not, is the deviation justified by new information rather than by the price?",
    "Post-mortem honesty",
  ]],
  ["Not graded", "0 pts", RED, [
    "Whether the stock went up",
    "Whether the trade made money",
    "The outcome is revealed and used only to score the calibration of stated probabilities",
  ]],
];
gradeCols.forEach((g, i) => {
  const x = M + i * 4.07;
  card(s, { x, y: 1.25, w: 3.82, h: 3.75, fill: i === 2 ? "FAF2F2" : "F5F8F7", line: i === 2 ? "E8D4D4" : "DCE5E2" });
  s.addText(g[0], { x: x + 0.28, y: 1.5, w: 2.5, h: 0.34, fontSize: 15, bold: true, color: g[2], margin: 0, isTextBox: true, fontFace: "Cambria" });
  s.addText(g[1], { x: x + 2.6, y: 1.5, w: 1.0, h: 0.34, fontSize: 14, bold: true, color: g[2], margin: 0, isTextBox: true, align: "right" });
  s.addText(bullets(g[3]), { x: x + 0.28, y: 1.98, w: 3.3, h: 2.85, fontSize: 11, color: "3C4A50", margin: 0, isTextBox: true, paraSpaceAfter: 8, lineSpacing: 14 });
});
card(s, { x: M, y: 5.2, w: 12.06, h: 1.05, fill: "EEF4F0", line: "CFE0D6" });
s.addText("The single highest-value dimension", { x: M + 0.3, y: 5.36, w: 5, h: 0.3, fontSize: 13, bold: true, color: GREEN, margin: 0, isTextBox: true });
body(s, M + 0.3, 5.68, 11.4, 0.5, "Pre-commitment consistency is the closest thing in the program to a direct measurement of thesis-creep resistance — and it is only possible because the T−2 submission was locked before the print was released.",
  { fontSize: 12, color: "2C4A38", lineSpacing: 16 });
s.addNotes("Deterministic marks are computed before any LLM sees the submission. Numbers never go to an LLM when a deterministic check exists.");

/* ============================================================ 15. CASE A — good vs bad */
s = S("CONTENT", "Worked cases");
s.addText("Case A — what a good and a bad answer look like", { placeholder: "title" });
function respond(sl, x, kind, color, fill, line, quote, points) {
  card(sl, { x, y: 1.25, w: 5.9, h: 4.6, fill, line });
  sl.addShape("roundRect", { x: x + 0.3, y: 1.5, w: 2.0, h: 0.36, rectRadius: 0.1, fill: { color }, line: { color, width: 0 } });
  sl.addText(kind, { x: x + 0.3, y: 1.5, w: 2.0, h: 0.36, align: "center", valign: "middle",
    fontSize: 10.5, bold: true, color: WHITE, margin: 0, isTextBox: true, charSpacing: 0.6 });
  // valign top on both, or a shorter quote centres in its box and the two
  // columns stop lining up — visible immediately when the deck is read side by side
  sl.addText(quote, { x: x + 0.3, y: 2.0, w: 5.3, h: 1.5, fontSize: 12, italic: true, color: INK,
    margin: 0, isTextBox: true, lineSpacing: 16, valign: "top" });
  sl.addText(bullets(points), { x: x + 0.3, y: 3.62, w: 5.3, h: 2.05, fontSize: 11.5, color: "3C4A50",
    margin: 0, isTextBox: true, paraSpaceAfter: 8, lineSpacing: 15, valign: "top" });
}
respond(s, M, "STRONG RESPONSE", GREEN, "EEF4F0", "CFE0D6",
  "“They beat by $30m and raised by $20m, so implied 2H revenue is $10m lower than it was this morning. 1H ran +12.71%; the back half is now implied at −1.46%. About 2.7 points of that is the comp; the rest is real. Q4 is implied at −2.86% against an FY+1 consensus needing +6.16%. I pre-committed to trimming on a guide that implied 2H deceleration. Trimming a third, keeping the rest into the analyst day.”",
  [
    "Did the subtraction nobody does — raise versus beat",
    "Separated the comp effect from the genuine slowdown",
    "Carried it forward to next year's consensus, where the real risk sits",
    "Acted on the pre-commitment rather than on the price",
  ]);
respond(s, 6.78, "WEAK RESPONSE", RED, "FAF2F2", "E8D4D4",
  "“Solid beat-and-raise quarter. Revenue ahead by $30m, management raised the full-year outlook and sounded confident on the call about demand into next year. Street numbers should move up. The thesis is intact and the setup into the analyst day looks good — staying long, no change to sizing.”",
  [
    "Read the headline and the tone, not the arithmetic",
    "Never compared the size of the raise to the size of the beat",
    "“Street numbers should move up” is exactly backwards — the implied 2H just fell",
    "No reference to the pre-commitment, so the action is unanchored",
  ]);
s.addText("Both students saw the same pack. The difference is one subtraction.", {
  x: M, y: 6.02, w: 12.06, h: 0.4, fontSize: 14, bold: true, italic: true, color: INK, margin: 0, isTextBox: true, align: "center" });
s.addNotes("The weak answer is not lazy — it is fluent and confident, which is what makes it a useful contrast.");

/* ============================================================ 16. CASE B */
s = S("CONTENT", "Worked cases");
s.addText("Case B — the task, the pack, and the frontier", { placeholder: "title" });
caseHeader(s, "B", "Eight years of twelve percent", "Serves Modules 10, 11 and 04  ·  T is an ordinary day with no catalyst pending — deliberately");
label(s, M, 2.0, 6, "Two-phase, with a lock between them");
card(s, { x: M, y: 2.32, w: 6.0, h: 1.32, fill: "F5F8F7" });
s.addText("Phase 1 · 20 min", { x: M + 0.26, y: 2.48, w: 2.2, h: 0.28, fontSize: 11.5, bold: true, color: TEAL, margin: 0, isTextBox: true });
body(s, M + 0.26, 2.78, 5.5, 0.8, "Given only the business description and historical financials, state the core debate and the three key drivers. Submit — it locks.",
  { fontSize: 11.5, color: "3C4A50", lineSpacing: 15 });
card(s, { x: M, y: 3.78, w: 6.0, h: 1.52, fill: "EEF4F0", line: "CFE0D6" });
s.addText("Phase 2 · 40 min", { x: M + 0.26, y: 3.94, w: 2.2, h: 0.28, fontSize: 11.5, bold: true, color: GREEN, margin: 0, isTextBox: true });
body(s, M + 0.26, 4.24, 5.5, 1.0, "Now receive consensus, the multiple versus its own history, positioning, and a reverse-DCF template. Re-write the core debate — then explain in 200 words what changed and why.",
  { fontSize: 11.5, color: "2C4A38", lineSpacing: 15 });
label(s, 6.9, 2.0, 6, "The frontier the student must build  ·  EV $25.0bn on $10.0bn sales, WACC 8%");
const frontier = [["Sales CAGR", "Operating margin", "Investment rate"],
  ["9.935%", "15.0%", "30%"], ["4.0%", "20.37%", "30%"], ["14.59%", "12.0%", "30%"], ["10.89%", "15.0%", "45%"]];
const ftbl = [frontier[0].map(h => ({ text: h, options: { bold: true, color: WHITE, fill: { color: TEAL }, fontSize: 10, margin: 5, align: "center" } }))]
  .concat(frontier.slice(1).map((r, i) => r.map(cv => ({
    text: cv, options: { color: i === 0 ? TEAL : INK, bold: i === 0, fontSize: 12, margin: 5, align: "center",
      fill: { color: i === 0 ? "EEF4F0" : (i % 2 ? "F7FAF9" : WHITE) } } }))));
s.addTable(ftbl, { x: 6.9, y: 2.32, w: 5.78, colW: [1.93, 1.93, 1.92],
  border: { type: "solid", color: "E2E8E6", pt: 0.75 }, valign: "middle", autoPage: false });
body(s, 6.9, 4.28, 5.78, 1.1, [
  { text: "Every row prices the same stock. ", options: { bold: true } },
  { text: "The output is not one implied growth rate — it is the set of driver combinations the price can tolerate, and the analyst's job is to say which one is plausible. Steady-state value is $14.812bn, so 59% of the price is the business as it stands and 41% is future value creation.", options: {} },
], { fontSize: 11.5, color: "3C4A50", lineSpacing: 15 });
s.addText("Companion solve: at EV $22.0bn the market-implied competitive advantage period is 12.96 years — which turns a 2.2x EV/invested-capital multiple into a falsifiable claim about the industry.", {
  x: M, y: 5.55, w: 12.06, h: 0.5, fontSize: 12, italic: true, color: SLATE, margin: 0, isTextBox: true, lineSpacing: 16 });
s.addNotes("The scored quantity is the delta between the two phases, which makes the case robust to a student who already knows the company.");

/* ============================================================ 17. CASE B — good vs bad */
s = S("CONTENT", "Worked cases");
s.addText("Case B — the two answers, and what separates them", { placeholder: "title" });
respond(s, M, "STRONG RESPONSE", GREEN, "EEF4F0", "CFE0D6",
  "“In Phase 1 I asked whether they can sustain double-digit growth. That was the wrong question. The price implies roughly 10% sales growth for eight years at today's margin — more than consensus publishes, which fades to 8%. So the debate is not the growth rate, it is the duration: the market is paying for a 13-year advantage period. I would short the duration, not the number. What would change my mind is evidence the reinvestment runway extends past the current category.”",
  [
    "Treated the reverse DCF as a frontier, not a point estimate",
    "Named which driver is actually contested — duration, not growth",
    "Used implied CAP as a competitive claim that can be checked against history",
    "Honest about the Phase 1 answer being wrong, rather than retrofitting it",
  ]);
respond(s, 6.78, "WEAK RESPONSE", RED, "FAF2F2", "E8D4D4",
  "“The reverse DCF implies about 9.9% sales growth. Consensus has revenue growing 6%. Since the implied number is higher than consensus, the stock is pricing in more than analysts expect, so it is overvalued. My core debate is unchanged from Phase 1: can they sustain double-digit growth? I think the Phase 1 read still holds.”",
  [
    "Collapsed the frontier to a single number and stopped there",
    "Never varied margin or the investment rate, so never saw the trade-off",
    "“Implied > consensus, therefore overvalued” ignores that the market and the Street are different bars",
    "Retrofitted Phase 1 as correct — the specific failure the lock exists to detect",
  ]);
card(s, { x: M, y: 6.0, w: 12.06, h: 0.72, fill: "F5F8F7" });
body(s, M + 0.3, 6.14, 11.5, 0.5, [
  { text: "The grader sees both submissions. ", options: { bold: true } },
  { text: "It is explicitly instructed to detect retrofitting — the student who says “I was already right” when the record shows otherwise loses the intellectual-honesty marks, which are worth more than the arithmetic.", options: {} },
], { fontSize: 12, color: "3C4A50", lineSpacing: 16 });
s.addNotes("Both students computed 9.935% correctly. Arithmetic was never the discriminator here.");

/* ============================================================ 18. CASE C */
s = S("CONTENT", "Worked cases");
s.addText("Case C — when the data itself is the lesson", { placeholder: "title" });
caseHeader(s, "C", "The numbers you were never shown", "Serves Modules 07, 06 and 08  ·  Envista Holdings, CIK 1757073 — already present in the tested data");
label(s, M, 2.0, 6, "Half 1 — T = 30 June 2021");
card(s, { x: M, y: 2.3, w: 6.0, h: 1.55, fill: "F5F8F7" });
body(s, M + 0.26, 2.48, 5.5, 1.25, [
  { text: "The student receives Envista's as-filed financials and is asked for the three-year revenue trajectory, the growth algorithm, and a view.\n\n", options: {} },
  { text: "The record at T shows FY2017 $2.8109bn, FY2018 $2.8445bn, FY2019 $2.7516bn", options: { bold: true } },
  { text: " — a business flat to declining around $2.8bn.", options: {} },
], { fontSize: 11.5, color: "3C4A50", lineSpacing: 15 });
label(s, 6.9, 2.0, 6, "Half 2 — the same periods, today's record");
card(s, { x: 6.9, y: 2.3, w: 5.78, h: 1.55, fill: "FAF2F2", line: "E8D4D4" });
body(s, 7.16, 2.48, 5.3, 1.25, [
  { text: "They are then shown the current figures: ", options: {} },
  { text: "FY2019 $2.2848bn, FY2020 $1.9291bn", options: { bold: true } },
  { text: " — 17.0% and 15.5% lower than what an analyst saw at the time, after a discontinued-operations reclassification the filings describe.", options: {} },
], { fontSize: 11.5, color: "5A3A3A", lineSpacing: 15 });
label(s, M, 4.0, 8, "The task, and how it is graded");
const cTasks = [
  ["Identify", "What happened, from the filings — not from a guess", "Auto"],
  ["Recompute", "Every growth rate and margin on the restated basis", "Auto, tolerance 1e-3"],
  ["Decide", "Which basis a comp sheet should use, and what that does to a multiple built on the other", "Rubric"],
  ["Generalise", "200 words on what this implies for any screen, backtest or comp sheet built from a current database", "Rubric"],
];
cTasks.forEach((t, i) => {
  const y = 4.32 + i * 0.52;
  card(s, { x: M, y, w: 12.06, h: 0.44, fill: i % 2 ? "F7FAF9" : WHITE, line: "E2E8E6" });
  s.addText(t[0], { x: M + 0.2, y: y + 0.02, w: 1.3, h: 0.4, fontSize: 11.5, bold: true, color: TEAL, margin: 0, isTextBox: true, valign: "middle" });
  s.addText(t[1], { x: M + 1.55, y: y + 0.02, w: 8.4, h: 0.4, fontSize: 11, color: "3C4A50", margin: 0, isTextBox: true, valign: "middle" });
  s.addText(t[2], { x: M + 10.1, y: y + 0.02, w: 1.8, h: 0.4, fontSize: 9.5, color: SLATE, margin: 0, isTextBox: true, valign: "middle", align: "right" });
});
s.addText("Full credit requires the student to state that both figures are correct answers to different questions — and to say which question a comp sheet is asking.", {
  x: M, y: 6.48, w: 12.06, h: 0.4, fontSize: 12.5, bold: true, italic: true, color: INK, margin: 0, isTextBox: true });
s.addNotes("This is the only case where the point-in-time leak is the teaching content rather than something to prevent.");

/* ============================================================ 19. CASE C — good vs bad */
s = S("CONTENT", "Worked cases");
s.addText("Case C — the answers, and why this case exists", { placeholder: "title" });
respond(s, M, "STRONG RESPONSE", GREEN, "EEF4F0", "CFE0D6",
  "“Both numbers are right. The 2020 10-K reported $2.7516bn for FY2019 on the basis then in force; the 2022 10-K restated it to $2.2848bn after moving a business to discontinued operations. Neither is an error. For a comp sheet I would use the restated basis, because the question a comp sheet asks is ‘what do I own going forward’ — but I would footnote it, because any multiple quoted from a contemporaneous note is on the old basis and the two are not comparable.”",
  [
    "Read the filings rather than assuming a data error",
    "Named the question each basis answers, instead of picking a winner",
    "Spotted the real hazard: a multiple from a 2021 note and a 2022 revenue figure do not belong in the same row",
    "Generalised correctly to screens and backtests",
  ]);
respond(s, 6.78, "WEAK RESPONSE", RED, "FAF2F2", "E8D4D4",
  "“There is a data error in the pack — the FY2019 revenue figure is wrong. The correct number is $2.2848bn, which is what the current filings and every data provider show. Using the right number, revenue declined from $2.84bn in 2018 to $2.28bn in 2019, a 19.6% drop, so this is a structurally shrinking business and the growth algorithm is negative.”",
  [
    "Treated the as-filed figure as a mistake rather than as history",
    "Computed a 19.6% decline that no market participant ever saw",
    "Built an entire thesis on a comparison between two different definitions of the company",
    "Deferred to “what every data provider shows” — the exact instinct this case exists to break",
  ]);
card(s, { x: M, y: 6.0, w: 12.06, h: 0.72, fill: "EEF4F0", line: "CFE0D6" });
body(s, M + 0.3, 6.14, 11.5, 0.5, [
  { text: "The weak answer is what a careful, diligent student produces by default. ", options: { bold: true } },
  { text: "It is confident, internally consistent and completely wrong — which is why this case inoculates against the most common error in quantitative equity work using a real company and real numbers rather than a parable.", options: {} },
], { fontSize: 12, color: "2C4A38", lineSpacing: 16 });
s.addNotes("This case also teaches students to distrust their own data, which no other case does.");

/* ============================================================ 20. WHAT IT REFUSES */
s = S("CONTENT_DARK", "Worked cases");
s.addText("What the engine deliberately refuses to do", { placeholder: "title" });
const refusals = [
  ["Grade the P&L", "The engine knows what happened, so the temptation is structural. Make it a code-level constraint: the grader interface should not expose the realised return to anything except the calibration scorer."],
  ["Run in real time", "No live market data, no order execution, no market-impact modelling. None of it measures what this curriculum teaches."],
  ["Rank students on returns", "A leaderboard rewards precisely the overconfidence the program should be training out."],
  ["Send numbers to an LLM", "Where a deterministic check exists, it runs first. The LLM grades reasoning only, and always with the worked key in context."],
];
refusals.forEach((r, i) => {
  const x = M + (i % 2) * 6.2, y = 1.35 + Math.floor(i / 2) * 2.35;
  card(s, { x, y, w: 5.9, h: 2.05, fill: "17262E", line: "2A3A42" });
  s.addText("✕", { x: x + 0.3, y: y + 0.24, w: 0.35, h: 0.35, fontSize: 15, bold: true, color: "C98B8B", margin: 0, isTextBox: true });
  s.addText(r[0], { x: x + 0.7, y: y + 0.24, w: 4.9, h: 0.34, fontSize: 15, bold: true, color: WHITE, margin: 0, isTextBox: true, fontFace: "Cambria" });
  body(s, x + 0.3, y + 0.72, 5.3, 1.2, r[1], { fontSize: 11.5, color: "AEC2BE", lineSpacing: 16 });
});
s.addText("Each of these is cheap to add and would quietly invalidate the measurement.", {
  x: M, y: 6.1, w: 12.06, h: 0.4, fontSize: 13, italic: true, color: TEAL2, margin: 0, isTextBox: true });
s.addNotes("Refusing the leaderboard is the one stakeholders push back on most.");

/* ============================================================ 21. BUILD PLAN */
pres.addSection({ title: "Next steps" });
s = S("CONTENT", "Next steps");
s.addText("What it takes to build", { placeholder: "title" });
const phases = [
  ["MVP", "4–6 weeks", "one engineer + one analyst author", [
    "The pit/ layer — done and tested",
    "8–12 cases as JSON manifests plus a document bundle",
    "Clock as a manual instructor action",
    "Deterministic grading of numbers and calibration",
    "Append-only submission store with hard locks",
  ], TEAL],
  ["v1", "+8–10 weeks", "adds the runtime", [
    "Web runtime with timers, staged release and locking",
    "INF-2 integration for workbook grading",
    "INF-6 anchor set and LLM rubric grading",
    "20–25 cases",
    "Validator running in CI",
  ], TEAL2],
  ["v2", "later", "scale and analytics", [
    "30–40 cases across the situation taxonomy",
    "Cohort analytics: which traps are systematically missed",
    "Per-case difficulty calibration",
    "Dependency-graph comparison in the model grader",
  ], SLATE],
];
phases.forEach((p, i) => {
  const x = M + i * 4.07;
  card(s, { x, y: 1.25, w: 3.82, h: 3.95 });
  s.addShape("roundRect", { x: x + 0.28, y: 1.5, w: 0.95, h: 0.34, rectRadius: 0.1, fill: { color: p[4] }, line: { color: p[4], width: 0 } });
  s.addText(p[0], { x: x + 0.28, y: 1.5, w: 0.95, h: 0.34, align: "center", valign: "middle", fontSize: 11, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(p[1], { x: x + 1.35, y: 1.5, w: 2.2, h: 0.34, fontSize: 13, bold: true, color: INK, margin: 0, isTextBox: true, valign: "middle" });
  s.addText(p[2], { x: x + 0.28, y: 1.9, w: 3.3, h: 0.28, fontSize: 10, color: SLATE, margin: 0, isTextBox: true, italic: true });
  s.addText(bullets(p[3]), { x: x + 0.28, y: 2.28, w: 3.3, h: 2.75, fontSize: 11, color: "3C4A50", margin: 0, isTextBox: true, paraSpaceAfter: 8, lineSpacing: 14.5 });
});
card(s, { x: M, y: 5.42, w: 12.06, h: 1.05, fill: "FDF8EF", line: "EADCC2" });
s.addText("Three questions to settle before anyone writes code", { x: M + 0.3, y: 5.58, w: 7, h: 0.3, fontSize: 13, bold: true, color: AMBER, margin: 0, isTextBox: true });
s.addText([
  { text: "1.  Can your build environment reach www.sec.gov/Archives, not just data.sec.gov?   ", options: {} },
  { text: "2.  Guidance or consensus as the default bar?   ", options: {} },
  { text: "3.  Who writes the cold expert keys?", options: {} },
], { x: M + 0.3, y: 5.92, w: 11.5, h: 0.45, fontSize: 11.5, color: "6B5424", margin: 0, isTextBox: true, lineSpacing: 15 });
s.addNotes("Question 1 decides whether the filing-reading exercises make the MVP. Question 3 is the one that cannot be automated and determines whether cases are gradable at all.");

/* ---------------------------------------------------------------- write */
(async () => {
  await pres.writeFile({ fileName: "historical-case-engine.pptx" });
  const { applyTheme } = require("/root/.claude/skills/synced/1cc75cfe-ccf6-4e4b-a430-bfe682f107bb_83f7b310-b0e4-4e5f-9f5a-aa12933542b8/pptx/scripts/apply_theme.js");
  await applyTheme("historical-case-engine.pptx", THEME);
  console.log("wrote historical-case-engine.pptx");
})();
