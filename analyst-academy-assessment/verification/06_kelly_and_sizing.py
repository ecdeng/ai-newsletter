import math
print("="*72); print("KELLY FOR ASSETS (fractional loss), not gambles (total loss)"); print("="*72)
print("Gambling form f* = (p*b - q)/b  assumes you lose the ENTIRE stake.")
print("A losing long is -15%, not -100%. Correct asset form:")
print("   f* = (p*a - q*b)/(a*b)    where a = gain fraction, b = loss fraction\n")
def kelly_asset(p,a,b): return (p*a - (1-p)*b)/(a*b)
for p,a,b in [(0.55,0.20,0.15),(0.55,0.30,0.20),(0.60,0.25,0.15),(0.45,0.18,0.09)]:
    f=kelly_asset(p,a,b)
    mu = p*a-(1-p)*b
    var = p*(a-mu)**2+(1-p)*(-b-mu)**2
    print(f"p={p:.2f} win +{a:.0%} lose -{b:.0%}: f* = ({p}*{a} - {1-p:.2f}*{b})/({a}*{b}) = {f:7.4f}  ({f*100:6.1f}% of capital)")
    print(f"    cross-check mu/sigma^2 = {mu:.6f}/{var:.6f} = {mu/var:7.4f}   (approx agrees)")
print("\nThe p=0.55, +20%/-15% case gives 141.7% of capital in ONE NAME.")
print("That absurdity IS the argument for fractional Kelly.\n")

print("="*72); print("GROWTH CURVE: why overbetting is strictly dominated"); print("="*72)
p,a,b = 0.55,0.20,0.15
fstar = kelly_asset(p,a,b)
def g(f): 
    if 1-f*b<=0 or 1+f*a<=0: return float('-inf')
    return p*math.log(1+f*a)+(1-p)*math.log(1-f*b)
gmax=g(fstar)
print(f"f* = {fstar:.4f}, max log-growth per bet = {gmax:.6f}")
for mult,lab in [(0.25,"quarter-Kelly"),(0.5,"half-Kelly"),(1.0,"full Kelly"),(1.5,"1.5x"),(2.0,"2x Kelly")]:
    f=fstar*mult; gg=g(f)
    # vol of log wealth
    m=p*math.log(1+f*a)+(1-p)*math.log(1-f*b)
    v=p*(math.log(1+f*a)-m)**2+(1-p)*(math.log(1-f*b)-m)**2
    print(f"  {lab:14s} f={f:7.4f}  growth={gg:+.6f} ({gg/gmax*100:6.1f}% of max)  log-vol={math.sqrt(v):.4f}")
print("\n=> half-Kelly keeps ~75% of growth at ~50% of the bet size;")
print("   2x Kelly earns ~ZERO growth at double the volatility. Strictly dominated.")

print("\n"+"="*72); print("PRACTICAL SIZING RULE (what pods actually do)"); print("="*72)
for loss_tol,bear in [(0.0050,0.40),(0.0050,0.25),(0.0075,0.30)]:
    size=loss_tol/bear
    print(f"  tolerable NAV loss {loss_tol:.2%} / bear downside {bear:.0%} -> position {size:.4%} of NAV")
    print(f"      check: {size:.4%} x {bear:.0%} = {size*bear:.4%} ✓")
print("\n=> THE BEAR CASE DETERMINES POSITION SIZE. Not the upside, not conviction.")

print("\n"+"="*72); print("THREE-YEAR DOUBLE: precision check"); print("="*72)
print(f"  1.15^3 = {1.15**3:.6f}  (NOT 1.52 -- rounding early causes drift)")
print(f"  2/1.15^3 = {2/1.15**3:.6f}  => +{(2/1.15**3-1)*100:.2f}% multiple expansion")
print(f"  pure-EPS double g = 2^(1/3)-1 = {2**(1/3)-1:.6%}")
print("  With a 2% dividend yield: (1+g)^3 * k = 2/1.02^3 =", round(2/1.02**3,6))
print("  NOTE: buyback accretion is ALREADY inside EPS growth.")
print("        Adding full shareholder yield on top DOUBLE-COUNTS it (~200-300bp/yr).")
print("        Only DIVIDENDS belong in the (1+y)^3 term.")
