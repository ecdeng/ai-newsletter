print("="*70); print("G-fixed. MAINTENANCE CAPEX (Greenwald)"); print("="*70)
ppe_g, s0, s1, capex, da = 1500.0, 3000.0, 3384.0, 450.0, 210.0
ratio = ppe_g/s0
growth_capex = (s1-s0)*ratio
maint = capex - growth_capex
print(f"Gross PP&E/Sales (prior yr) = {ppe_g}/{s0} = {ratio:.4f}")
print(f"$ sales growth = {s1-s0}; growth capex = {s1-s0} x {ratio:.4f} = ${growth_capex:.1f}m")
print(f"Maintenance capex = total capex ${capex} - growth ${growth_capex:.1f} = ${maint:.1f}m")
print(f"Sanity vs D&A ${da}: maint/D&A = {maint/da:.2f}x -> plausible (maint capex usually >= D&A under inflation)")
print(f"Owner earnings proxy: EBIT(1-t) - maint capex, t=23%, EBIT 630 -> {630*0.77 - maint:.1f}")

print("\n"+"="*70); print("I-fixed. BUYBACK: EPS ACCRETION vs VALUE CREATION"); print("="*70)
ni, sh, px, spend = 900.0, 300.0, 45.0, 600.0
eps0 = ni/sh; retired = spend/px; sh1 = sh-retired; eps1 = ni/sh1
print(f"EPS {eps0:.3f} -> {eps1:.4f} (+{(eps1/eps0-1)*100:.2f}%). Shares {sh} -> {sh1:.3f}m")
print("EPS accretion test: buying back always lifts EPS when E/P exceeds the after-tax")
print(f"  return forgone on the cash. E/P = {eps0/px*100:.2f}%; cash yield say 4.0% pre-tax /")
print(f"  {4.0*0.77:.2f}% after tax -> accretive to EPS. This is ARITHMETIC, not value creation.")
print()
print("VALUE test: a buyback creates value only if price < intrinsic value per share.")
for iv in [40.0, 45.0, 56.0]:
    gain_ps = (iv-px)*retired/sh1    # value transferred to remaining holders
    print(f"  If intrinsic value = ${iv:.2f}: {'value CREATED' if iv>px else 'value DESTROYED' if iv<px else 'value NEUTRAL'}; "
          f"transfer to stayers ~= (${iv:.2f}-${px:.2f}) x {retired:.3f}m / {sh1:.3f}m = ${gain_ps:+.3f}/sh")
print()
print("Common wrong answer: 'E/P 6.67% < cost of equity 9%, so the buyback destroys value.'")
print("  That comparison is only a valid value test for a NO-GROWTH perpetuity, where")
print("  intrinsic P/E = 1/r = 11.1x. For a growing firm E/P below r is normal and says nothing.")
nogrowth_pe = 1/0.09
print(f"  No-growth justified P/E = 1/0.09 = {nogrowth_pe:.2f}x vs actual {px/eps0:.2f}x")
print(f"  -> at zero growth the stock would be CHEAP (15.0x < {nogrowth_pe:.1f}x is false; 15 > 11.1 so expensive)")
print(f"  Correct reading: 15.0x > {nogrowth_pe:.1f}x means the market prices in growth; whether the")
print("  buyback creates value depends on your own IV estimate, not on E/P vs r.")
