print("="*72); print("INCREMENTAL MARGIN IDENTITIES"); print("="*72)
print("Claim 1: m1 = (m0 + i*g)/(1+g)   where m=EBIT margin, i=incremental margin, g=rev growth")
print("Claim 2: margin expands iff i > m0")
print("Claim 3: DOL = i/m0\n")
def check(r0,m0,g,i):
    r1=r0*(1+g); e0=r0*m0; e1=e0+i*(r1-r0); m1=e1/r1
    pred=(m0+i*g)/(1+g)
    dol_emp=((e1/e0)-1)/g
    print(f"  r0={r0}, m0={m0:.1%}, g={g:.1%}, i={i:.1%}")
    print(f"    direct m1 = {m1:.6f}   formula (m0+i*g)/(1+g) = {pred:.6f}   match={abs(m1-pred)<1e-12}")
    print(f"    margin {'EXPANDS' if m1>m0 else 'CONTRACTS'}; i>m0 is {i>m0} -> claim 2 holds: {(m1>m0)==(i>m0)}")
    print(f"    empirical DOL = %dEBIT/%dRev = {dol_emp:.6f};  i/m0 = {i/m0:.6f}  match={abs(dol_emp-i/m0)<1e-12}")
for args in [(1000,0.15,0.12,0.30),(1000,0.15,0.12,0.10),(4000,0.15,0.125,0.30),(1000,0.20,0.05,0.20)]:
    check(*args); print()
print("All three identities verified algebraically and numerically.\n")

print("="*72); print("DECREMENTAL MARGIN ROUND TRIP (permanent destruction)"); print("="*72)
r=[4000,4500,4000]; e=[600,750,None]
i_up=(e[1]-e[0])/(r[1]-r[0])
print(f"Up-leg: rev {r[0]}->{r[1]}, EBIT {e[0]}->{e[1]}, incremental margin = {i_up:.1%}")
for dec in [0.30,0.34,0.38]:
    e2=e[1]-dec*(r[1]-r[2])
    print(f"  down-leg decremental {dec:.0%}: EBIT falls to {e2:.1f} vs original {e[0]} -> permanent loss {e[0]-e2:+.1f}")
print("  => if decremental > incremental, a full revenue round trip LOSES profit permanently.")
print("     That asymmetry is the short signal.")

print("\n"+"="*72); print("DAY-COUNT HACK"); print("="*72)
per_day, days = 1.05238, 0.96923
print(f"  reported growth = per-selling-day {per_day-1:+.3%} x day-count {days-1:+.3%}")
print(f"  = {per_day*days:.5f} -> {(per_day*days-1):+.3%} reported")
print("  A +2.0% reported quarter is actually +5.2% per selling day with a 3.1% day-count headwind.")
