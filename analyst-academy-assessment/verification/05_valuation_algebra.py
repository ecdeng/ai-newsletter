print("="*72); print("CORRECTED VALUE-DRIVER FAMILY"); print("="*72)
def pe_equity(g,roe,re): return (1-g/roe)/(re-g)      # justified FORWARD P/E
def ev_nopat(g,roic,wacc): return (1-g/roic)/(wacc-g)
def ev_ebit(g,roic,wacc,t): return (1-t)*(1-g/roic)/(wacc-g)
def ev_ic(g,roic,wacc): return (roic-g)/(wacc-g)

print("\n1) Justified forward P/E = (1 - g/ROE)/(re - g)   [EQUITY: ROE with COST OF EQUITY]")
for g,roe,re in [(0.04,0.16,0.09),(0.05,0.20,0.09),(0.03,0.12,0.085)]:
    print(f"   g={g:.0%} ROE={roe:.0%} re={re:.0%} -> {pe_equity(g,roe,re):6.2f}x  (payout {1-g/roe:.1%})")

print("\n2) EV/NOPAT = (1 - g/ROIC)/(WACC - g)   [ENTERPRISE: ROIC with WACC]")
print("   g=4% ROIC=16% WACC=9% ->", round(ev_nopat(0.04,0.16,0.09),4),"x")
print("   EV/EBIT at t=25%      ->", round(ev_ebit(0.04,0.16,0.09,0.25),4),"x  (= 0.75 x 15.00)")

print("\n3) EV/IC = (ROIC - g)/(WACC - g)  -- falls out of EV = NOPAT(1-g/ROIC)/(WACC-g), NOPAT=ROIC*IC")
for g in [0.0,0.02,0.04,0.06,0.08]:
    print(f"   ROIC=WACC=9%, g={g:.0%} -> EV/IC = {ev_ic(g,0.09,0.09):.6f}   EV/NOPAT = {ev_nopat(g,0.09,0.09):.4f}x (=1/WACC={1/0.09:.4f})")
print("   => COROLLARY VERIFIED: ROIC=WACC gives EV/IC=1.0 for EVERY g. Growth is value-neutral.")
print("   ROIC=16%, WACC=9%, g=4% -> EV/IC =", round(ev_ic(0.04,0.16,0.09),4))

print("\n4) THE GRID: EV/NOPAT, WACC=9%")
print("        g=0%    g=2%    g=4%    g=6%")
for roic in [0.06,0.09,0.16,0.25]:
    row=f"ROIC {roic:>4.0%} "
    for g in [0.0,0.02,0.04,0.06]:
        row += f"{ev_nopat(g,roic,0.09):7.2f} " if g<roic else f"{'0.00':>7} "
    print("   "+row)
print("   ROIC=WACC row is FLAT at 1/WACC = 11.11x  <- the 'commodity multiple'")
print("   At ROIC=6% (<WACC) growth DESTROYS multiple: 11.11 -> 9.52 -> 6.67")

print("\n5) VALUE OF GROWTH closed form: GV = NOPAT*g*(ROIC-WACC)/[ROIC*WACC*(WACC-g)]")
def gv(nopat,g,roic,wacc): return nopat*g*(roic-wacc)/(roic*wacc*(wacc-g))
for g,roic in [(0.04,0.16),(0.04,0.06),(0.04,0.09),(0.0,0.16)]:
    direct = (ev_nopat(g,roic,0.09)-1/0.09)*180 if g<roic else float('nan')
    print(f"   NOPAT=180 g={g:.0%} ROIC={roic:>4.0%}: GV={gv(180,g,roic,0.09):+9.2f}  cross-check={direct:+9.2f}")
print("   => sign(GV) = sign(ROIC - WACC). Verified.")

print("\n"+"="*72); print("6) LEVERAGE AND P/E -- the mis-keyed exam item"); print("="*72)
EV,EBIT,t = 1000.0, 75.0, 0.25
unlev_eq_yield = EBIT*(1-t)/EV
print(f"EV {EV}, EBIT {EBIT}, t {t:.0%}; unlevered equity earnings yield = EBIT(1-t)/EV = {unlev_eq_yield:.4%}")
print(f"Break-even pre-tax cost of debt = {unlev_eq_yield/(1-t):.4%}  (after-tax {unlev_eq_yield:.4%})")
for rd in [0.06,0.075,0.10]:
    print(f"\n  cost of debt {rd:.1%}:")
    for D in [0.0,300.0,600.0]:
        NI=(EBIT-rd*D)*(1-t); E=EV-D
        print(f"    D={D:6.0f}  equity={E:6.0f}  NI={NI:7.3f}  P/E={E/NI:8.3f}x")
print("\n  => Cheap debt (6% < 7.5% BE) LOWERS P/E; expensive debt (10%) RAISES it;")
print("     at the break-even 7.5% P/E is invariant to leverage.")
print("     An item keyed 'leverage raises P/E' as a general rule is MIS-KEYED.")
