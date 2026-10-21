# Independent verification of arithmetic I intend to use in sample questions.
# Run with: python3 -I verify_math.py
from itertools import product

print("="*70)
print("1. THREE-YEAR DOUBLE: (1+g)^3 * (M_exit/M_entry) = 2")
print("="*70)
print(f"{'EPS CAGR':>9} {'3yr EPS mult':>13} {'req M_exit/M_entry':>19} {'req multiple chg':>17}")
for g in [0.05,0.08,0.10,0.12,0.15,0.18,0.20,0.25,0.26]:
    eps_mult = (1+g)**3
    req = 2/eps_mult
    print(f"{g*100:8.0f}% {eps_mult:13.4f} {req:19.4f} {(req-1)*100:16.1f}%")
print("\nCheck: g=26% -> (1.26)^3 =", round(1.26**3,4), "(doubles on EPS alone at ~26%)")
print("Exact g for pure-EPS double: 2**(1/3)-1 =", round(2**(1/3)-1,6))

print("\n" + "="*70)
print("2. RETURN DECOMPOSITION with cross term")
print("="*70)
# Stock: entry EPS 4.00, P/E 15 -> price 60. Exit EPS 5.80, P/E 17 -> price 98.60
e0,m0,e1,m1 = 4.00,15.0,5.80,17.0
p0,p1 = e0*m0, e1*m1
print(f"P0={p0}  P1={p1}  total return={(p1/p0-1)*100:.2f}%")
ge, gm = e1/e0-1, m1/m0-1
print(f"EPS growth={ge*100:.4f}%  multiple change={gm*100:.4f}%  cross={ge*gm*100:.4f}%")
print(f"sum of three = {(ge+gm+ge*gm)*100:.4f}%  (must equal total)")
assert abs((1+ge)*(1+gm) - p1/p0) < 1e-12
# 3-year CAGR version
print(f"3yr: EPS CAGR={( (e1/e0)**(1/3)-1)*100:.2f}%  multiple CAGR={((m1/m0)**(1/3)-1)*100:.2f}%  total CAGR={((p1/p0)**(1/3)-1)*100:.2f}%")

print("\n" + "="*70)
print("3. JUSTIFIED MULTIPLE: P/E = (1 - g/ROIC)/(r - g)  [value-driver formula]")
print("="*70)
def justified_pe(g, roic, r):
    return (1 - g/roic)/(r - g)
for g,roic,r in [(0.04,0.20,0.09),(0.04,0.10,0.09),(0.06,0.30,0.09),(0.06,0.09,0.09),(0.02,0.15,0.08)]:
    pe = justified_pe(g,roic,r)
    print(f"g={g:.0%} ROIC={roic:.0%} r={r:.0%} -> justified P/E = {pe:7.2f}   payout ratio=(1-g/ROIC)={1-g/roic:.1%}")
print("\nSanity: ROIC == r  => P/E = (1-g/r)/(r-g) = ((r-g)/r)/(r-g) = 1/r")
print("  g=5%, ROIC=9%, r=9% ->", round(justified_pe(0.05,0.09,0.09),4), " vs 1/r =", round(1/0.09,4))
print("  growth is value-neutral when ROIC=r. Confirmed.")
print("\nEV/EBIT version = (1-t)(1 - g/ROIC)/(WACC-g); t=25%, g=4%, ROIC=20%, WACC=9%:")
print("  ", round(0.75*(1-0.04/0.20)/(0.09-0.04),3))

print("\n" + "="*70)
print("4. GORDON-GROWTH P/E = payout/(r-g) consistency check")
print("="*70)
# payout = 1 - reinvestment = 1 - g/ROIC
g,roic,r = 0.04,0.20,0.09
payout = 1-g/roic
print(f"payout={payout:.2f}, P/E=payout/(r-g)={payout/(r-g):.2f} == value-driver {justified_pe(g,roic,r):.2f}")

print("\n" + "="*70)
print("5. IMPLIED MOVE FROM ATM STRADDLE")
print("="*70)
S, call, put = 82.50, 3.40, 3.10
straddle = call+put
print(f"Stock ${S}, ATM call ${call}, ATM put ${put}, straddle ${straddle:.2f}")
print(f"Implied move = straddle/S = {straddle/S*100:.2f}%")
print(f"Breakevens: ${S+straddle:.2f} up / ${S-straddle:.2f} down")
# the 0.8 adjustment convention sometimes used for expected absolute move
print(f"Expected |move| using 0.8*straddle/S convention = {0.8*straddle/S*100:.2f}%")

print("\n" + "="*70)
print("6. TWO-YEAR STACK conventions")
print("="*70)
g1,g2 = 0.22, -0.04   # yr1 +22%, yr2 -4%
print(f"y/y growth: year1={g1:.0%}, year2={g2:.0%}")
print(f"Additive 2yr stack      = {(g1+g2)*100:.1f}%")
print(f"Geometric 2yr stack     = {((1+g1)*(1+g2)-1)*100:.2f}%  (cumulative vs 2 yrs ago)")
print(f"2yr CAGR                = {(((1+g1)*(1+g2))**0.5-1)*100:.2f}%")

print("\n" + "="*70)
print("7. INCREMENTAL MARGIN")
print("="*70)
r0,e0_,r1,e1_ = 1000.0, 150.0, 1120.0, 198.0
print(f"Rev {r0}->{r1} (+{(r1/r0-1)*100:.1f}%), EBIT {e0_}->{e1_}")
print(f"Incremental margin = dEBIT/dRev = {(e1_-e0_)}/{(r1-r0)} = {(e1_-e0_)/(r1-r0)*100:.1f}%")
print(f"EBIT margin {e0_/r0*100:.1f}% -> {e1_/r1*100:.1f}%  (+{(e1_/r1-e0_/r0)*10000:.0f}bps)")

print("\n" + "="*70)
print("8. SHORT P&L WITH BORROW + DIVIDEND")
print("="*70)
P0,P1,sh = 50.0, 42.0, 10000
gross = (P0-P1)*sh
notional = P0*sh
days=180; borrow_bps=350; div_ps=0.30; n_div=2
borrow_cost = notional*(borrow_bps/10000)*(days/360)
div_cost = div_ps*n_div*sh
print(f"Short {sh} @ ${P0} -> cover @ ${P1}: gross P&L ${gross:,.0f} ({(P0-P1)/P0*100:.1f}% of notional)")
print(f"Borrow {borrow_bps}bps on ${notional:,.0f} for {days}d (360 basis) = ${borrow_cost:,.0f}")
print(f"Dividends owed: {n_div} x ${div_ps} x {sh} = ${div_cost:,.0f}")
net = gross-borrow_cost-div_cost
print(f"Net P&L = ${net:,.0f}  = {net/notional*100:.2f}% of initial notional")
print(f"Carry drag = {(borrow_cost+div_cost)/notional*100:.2f}%")

print("\n" + "="*70)
print("9. SHORT ASYMMETRY / POSITION GROWTH")
print("="*70)
print("Short $1m notional in a 20-stock-equivalent sleeve; stock +50%:")
print(f"  loss = $500,000; position notional now ${1e6*1.5:,.0f} -> exposure grew 50% while equity fell")
print("Short that goes to zero: +100% max gain. Short that triples: -200%.")
for mv in [0.5,1.0,2.0]:
    print(f"  stock +{mv*100:.0f}% -> P&L {-mv*100:.0f}% of original notional; to hold constant notional you must cover {mv/(1+mv)*100:.1f}% of shares")

print("\n" + "="*70)
print("10. BENEISH M-SCORE (8-variable) - coefficient check")
print("="*70)
# M = -4.84 + 0.920*DSRI + 0.528*GMI + 0.404*AQI + 0.892*SGI + 0.115*DEPI
#     - 0.172*SGAI + 4.679*TATA - 0.327*LVGI    (threshold -1.78)
co = dict(DSRI=0.920,GMI=0.528,AQI=0.404,SGI=0.892,DEPI=0.115,SGAI=-0.172,TATA=4.679,LVGI=-0.327)
vals = dict(DSRI=1.31,GMI=1.08,AQI=1.05,SGI=1.42,DEPI=1.12,SGAI=0.95,TATA=0.065,LVGI=1.02)
M = -4.84 + sum(co[k]*vals[k] for k in co)
print("inputs:", vals)
for k in co: print(f"  {k}: {co[k]:+.3f} x {vals[k]} = {co[k]*vals[k]:+.4f}")
print(f"M-score = -4.84 + {sum(co[k]*vals[k] for k in co):.4f} = {M:.4f}")
print(f"Threshold -1.78 -> {'FLAGGED (potential manipulator)' if M > -1.78 else 'not flagged'}")

print("\n" + "="*70)
print("11. IR = IC * sqrt(breadth); PARAMETRIC VaR; BRIER")
print("="*70)
import math
ic, breadth = 0.05, 200
print(f"IC={ic}, breadth={breadth} -> IR = {ic*math.sqrt(breadth):.3f}")
print(f"IC=0.03, breadth=100 -> IR = {0.03*math.sqrt(100):.3f}")
# parametric VaR
nav, vol_ann, z = 100e6, 0.18, 1.645
var_1d = nav*vol_ann/math.sqrt(252)*z
print(f"1-day 95% parametric VaR on ${nav/1e6:.0f}m at {vol_ann:.0%} ann vol: daily vol={vol_ann/math.sqrt(252)*100:.3f}%, VaR=${var_1d/1e6:.3f}m ({var_1d/nav*100:.3f}%)")
z99=2.326
print(f"  at 99% (z=2.326): ${nav*vol_ann/math.sqrt(252)*z99/1e6:.3f}m")
# Brier
fc = [(0.7,1),(0.3,0),(0.6,0),(0.9,1),(0.4,1)]
bs = sum((p-o)**2 for p,o in fc)/len(fc)
print(f"Brier score for {fc} = {bs:.4f}  (0=perfect, 0.25=always 50%, 1=max wrong)")
print(f"  always-50% baseline = {sum((0.5-o)**2 for _,o in fc)/len(fc):.4f}")

print("\n" + "="*70)
print("12. BATTING AVERAGE / SLUGGING RATIO EV")
print("="*70)
ba, avg_win, avg_loss = 0.45, 0.18, 0.09
ev = ba*avg_win - (1-ba)*avg_loss
print(f"Batting avg {ba:.0%}, avg winner +{avg_win:.0%}, avg loser -{avg_loss:.0%}")
print(f"Slugging ratio = {avg_win/avg_loss:.2f}x")
print(f"EV per idea = {ba}*{avg_win} - {1-ba:.2f}*{avg_loss} = {ev*100:.2f}%")
print(f"Break-even batting avg at this slugging ratio = {avg_loss/(avg_win+avg_loss)*100:.1f}%")

print("\n" + "="*70)
print("13. FACTOR RISK DECOMPOSITION")
print("="*70)
tot_vol=0.14; fac_vol=0.11
print(f"Total vol {tot_vol:.0%}; factor vol {fac_vol:.0%}")
spec_var = tot_vol**2 - fac_vol**2
print(f"Total var={tot_vol**2:.6f}, factor var={fac_vol**2:.6f}, specific var={spec_var:.6f}, specific vol={math.sqrt(spec_var)*100:.2f}%")
print(f"% of variance from factors = {fac_vol**2/tot_vol**2*100:.1f}%  (idiosyncratic {spec_var/tot_vol**2*100:.1f}%)")

print("\n" + "="*70)
print("14. EPS SURPRISE BRIDGE (must sum)")
print("="*70)
# consensus: rev 1000, GM 40%, opex 250, tax 21%, shares 100 -> EPS
def eps(rev,gm,opex,tax,sh):
    ebit = rev*gm - opex
    return ebit*(1-tax)/sh, ebit
base = dict(rev=1000.0,gm=0.400,opex=250.0,tax=0.21,sh=100.0)
act  = dict(rev=1030.0,gm=0.392,opex=256.0,tax=0.19,sh=98.5)
e_b,_ = eps(**base); e_a,_ = eps(**act)
print(f"Consensus EPS = {e_b:.4f}; Actual EPS = {e_a:.4f}; surprise = {e_a-e_b:+.4f} ({(e_a/e_b-1)*100:+.2f}%)")
# sequential attribution
steps=[]; cur=dict(base)
for k in ['rev','gm','opex','tax','sh']:
    prev,_ = eps(**cur); cur[k]=act[k]; new,_ = eps(**cur)
    steps.append((k,new-prev))
print("Sequential bridge:")
for k,v in steps: print(f"  {k:5s}: {v:+.4f}")
print(f"  sum = {sum(v for _,v in steps):+.4f}  (equals total surprise {e_a-e_b:+.4f})")
assert abs(sum(v for _,v in steps)-(e_a-e_b))<1e-9

print("\n" + "="*70)
print("15. REVERSE DCF: solve implied growth")
print("="*70)
# Price 100, FCF0 = 4.00, WACC 8%, 10yr explicit then terminal g 2.5%. Solve g_explicit.
def pv(g, fcf0=4.0, wacc=0.08, n=10, gt=0.025):
    tot=0.0; f=fcf0
    for t in range(1,n+1):
        f = f*(1+g); tot += f/(1+wacc)**t
    tv = f*(1+gt)/(wacc-gt)
    return tot + tv/(1+wacc)**n
lo,hi=-0.2,0.6
for _ in range(200):
    mid=(lo+hi)/2
    if pv(mid)<100.0: lo=mid
    else: hi=mid
print(f"Price $100, FCF0 $4.00, WACC 8%, 10yr explicit, terminal g 2.5%")
print(f"-> implied explicit-period FCF CAGR = {(lo+hi)/2*100:.3f}%  (PV check = ${pv((lo+hi)/2):.4f})")
print(f"Terminal value share of PV = {(pv((lo+hi)/2)-sum((4.0*(1+(lo+hi)/2)**t)/(1.08**t) for t in range(1,11)))/pv((lo+hi)/2)*100:.1f}%")

print("\n" + "="*70)
print("16. SCENARIO TREE + IMPLIED PROBABILITY OF BULL")
print("    NOTE: these inputs turned out DEGENERATE (implied bull prob = 0%).")
print("    Superseded by 04_scenario_trees.py, which is what the blueprint uses.")
print("="*70)
px=100.0; bull,base_,bear = 160.0,110.0,70.0
pb,pba,pbe = 0.25,0.50,0.25
ev_px = pb*bull+pba*base_+pbe*bear
print(f"Price ${px}; bull ${bull} base ${base_} bear ${bear}; probs {pb}/{pba}/{pbe}")
print(f"EV price = ${ev_px:.2f} -> expected return {(ev_px/px-1)*100:+.1f}%")
print(f"Upside to bull {bull/px-1:+.0%}, downside to bear {bear/px-1:+.0%}, asymmetry {(bull-px)/(px-bear):.2f}x")
# implied prob of bull holding bear prob fixed such that EV = current price
# p*bull + (1-p-pbe)*base + pbe*bear = px  -> solve p
p = (px - pbe*bear - (1-pbe)*base_)/(bull-base_)
print(f"Prob of bull that makes EV = current price (bear prob fixed {pbe}): {p*100:.2f}%")
chk = p*bull+(1-p-pbe)*base_+pbe*bear
print(f"  check EV = ${chk:.4f}")
print(f"Market is implying <= {p*100:.1f}% bull odds; we underwrite {pb*100:.0f}% -> that gap IS the thesis")
