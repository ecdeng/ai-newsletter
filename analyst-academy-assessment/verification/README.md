# Arithmetic verification

Every quantitative worked example in `BLUEPRINT.md` was computed and checked
with these scripts. They double as the answer keys.

Run any of them with:

    python3 -I <script>.py

(`-I` is used because these read nothing and import nothing outside the
standard library; it keeps the run isolated.)

| Script | Covers |
|---|---|
| `01_core_identities.py` | Three-year double table; return decomposition with cross term; justified-multiple family; straddle-implied move; 2-year stack (all three conventions); incremental margin; short P&L with borrow and dividend; short asymmetry; Beneish M-score; IR = IC·√BR; parametric VaR; Brier; batting/slugging; factor risk decomposition; EPS surprise bridge; reverse-DCF implied-growth solve |
| `02_roic_cashflow_buybacks.py` | ROIC decomposition; cash conversion cycle; treasury-stock method; organic growth bridge; Piotroski F-score; Altman Z; SBC net dilution |
| `03_maintcapex_buyback_value.py` | Maintenance capex (corrected after the first version returned a negative figure); buyback EPS accretion vs. value creation, including the E/P-vs-cost-of-equity fallacy |
| `04_scenario_trees.py` | Scenario trees and market-implied bull probability (rebuilt after the first version was degenerate at 0%) |
| `05_valuation_algebra.py` | The corrected value-driver family (P/E with ROE and cost of equity; EV/NOPAT and EV/IC with ROIC and WACC); the ROIC=WACC ⇒ EV/IC=1 corollary; the ROIC × growth multiple grid; the value-of-growth closed form; the leverage-and-P/E break-even that shows "leverage raises P/E" is mis-keyed |
| `06_kelly_and_sizing.py` | Kelly for fractional-loss assets vs. the gambling form; the growth curve showing 2x Kelly is strictly dominated; the practical bear-case sizing rule; three-year-double precision |
| `07_incremental_margin.py` | The three incremental-margin identities (margin forecast, expansion condition, DOL = i/m₀); the decremental round trip; the day-count decomposition |

Two examples were **rejected and rebuilt** when verification showed they were
unusable: a scenario tree whose numbers implied a 0% probability of the bull
case, and a maintenance-capex calculation that returned a negative number.
Both corrected versions are what appear in the blueprint.
