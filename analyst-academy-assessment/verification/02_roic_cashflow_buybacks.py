import math
print("="*70); print("A. ROIC DECOMPOSITION (NOPAT margin x invested-capital turns)"); print("="*70)
rev, ebit, tax = 4200.0, 630.0, 0.23
nopat = ebit*(1-tax)
# invested capital: working capital + net PP&E + intangibles(ex goodwill optional)
ar,inv,ap,ppe,intang = 520.0, 410.0, 380.0, 1150.0, 340.0
ic = (ar+inv-ap)+ppe+intang
print(f"Revenue {rev}, EBIT {ebit} (margin {ebit/rev:.2%}), tax {tax:.0%} -> NOPAT {nopat:.1f}")
print(f"Invested capital = (AR {ar} + Inv {inv} - AP {ap}) + PPE {ppe} + Intangibles {intang} = {ic:.1f}")
print(f"ROIC = NOPAT/IC = {nopat:.1f}/{ic:.1f} = {nopat/ic:.2%}")
print(f"Decomp: NOPAT margin {nopat/rev:.2%} x IC turns {rev/ic:.3f}x = {nopat/rev*rev/ic:.2%}  [ties]")
assert abs(nopat/rev*(rev/ic) - nopat/ic) < 1e-12
wacc=0.085
print(f"ROIC - WACC spread = {nopat/ic:.2%} - {wacc:.1%} = {(nopat/ic-wacc)*10000:.0f}bps")
print(f"Economic profit = (ROIC-WACC) x IC = {(nopat/ic-wacc)*ic:.1f}")

print("\n"+"="*70); print("B. CASH CONVERSION CYCLE"); print("="*70)
cogs=2520.0
dso, dio, dpo = ar/rev*365, inv/cogs*365, ap/cogs*365
print(f"DSO = AR/Rev*365 = {ar}/{rev}*365 = {dso:.1f}d")
print(f"DIO = Inv/COGS*365 = {inv}/{cogs}*365 = {dio:.1f}d")
print(f"DPO = AP/COGS*365 = {ap}/{cogs}*365 = {dpo:.1f}d")
print(f"CCC = DSO + DIO - DPO = {dso:.1f} + {dio:.1f} - {dpo:.1f} = {dso+dio-dpo:.1f} days")

print("\n"+"="*70); print("C. TREASURY STOCK METHOD -> diluted shares"); print("="*70)
basic=100.0e6; opts=4.0e6; strike=28.0; px=70.0; rsu=1.5e6
proceeds=opts*strike; repurch=proceeds/px; net_opt=opts-repurch
dil=basic+net_opt+rsu
print(f"Basic {basic/1e6:.1f}m; options {opts/1e6:.1f}m @ ${strike} strike; price ${px}; RSUs {rsu/1e6:.1f}m")
print(f"Proceeds = {opts/1e6:.1f}m x ${strike} = ${proceeds/1e6:.1f}m -> repurchases {repurch/1e6:.4f}m shares at ${px}")
print(f"Net new from options = {opts/1e6:.1f} - {repurch/1e6:.4f} = {net_opt/1e6:.4f}m")
print(f"Diluted shares = {basic/1e6:.1f} + {net_opt/1e6:.4f} + {rsu/1e6:.1f} = {dil/1e6:.4f}m")
print(f"Dilution vs basic = {(dil/basic-1)*100:.2f}%")

print("\n"+"="*70); print("D. ORGANIC GROWTH BRIDGE (reported -> organic)"); print("="*70)
r0,r1 = 3000.0, 3384.0
m_contrib, fx_contrib = 150.0, -66.0   # acquisitions added 150; FX cost 66
print(f"Reported: {r0} -> {r1} = {(r1/r0-1)*100:+.2f}%")
print(f"  M&A contribution +{m_contrib} = {m_contrib/r0*100:+.2f}pp")
print(f"  FX {fx_contrib} = {fx_contrib/r0*100:+.2f}pp")
org = r1 - m_contrib - fx_contrib
print(f"Organic constant-currency revenue = {r1} - {m_contrib} - ({fx_contrib}) = {org}")
print(f"Organic growth = {org}/{r0} - 1 = {(org/r0-1)*100:+.2f}%")
print(f"Bridge check: {(r1/r0-1)*100:.2f}% = organic {(org/r0-1)*100:.2f}% + M&A {m_contrib/r0*100:.2f}% + FX {fx_contrib/r0*100:.2f}% = {((org/r0-1)+m_contrib/r0+fx_contrib/r0)*100:.2f}%")

print("\n"+"="*70); print("E. PIOTROSKI F-SCORE (9 binary signals)"); print("="*70)
sig = {
 "1. ROA > 0":1, "2. CFO > 0":1, "3. ROA improved y/y":0, "4. CFO > ROA (accruals ok)":1,
 "5. Leverage (LTD/assets) decreased":1, "6. Current ratio improved":0,
 "7. No new equity issued":1, "8. Gross margin improved":0, "9. Asset turnover improved":1}
for k,v in sig.items(): print(f"   {k:42s} {v}")
print(f"F-Score = {sum(sig.values())}/9  -> {'strong' if sum(sig.values())>=8 else 'middling' if sum(sig.values())>=4 else 'weak'}")

print("\n"+"="*70); print("F. ALTMAN Z-SCORE (public manufacturer)"); print("="*70)
# Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
X1,X2,X3,X4,X5 = 0.14, 0.22, 0.09, 1.10, 0.95
co=[("X1 WC/TA",1.2,X1),("X2 RE/TA",1.4,X2),("X3 EBIT/TA",3.3,X3),("X4 MVE/TL",0.6,X4),("X5 Sales/TA",1.0,X5)]
Z=sum(c*v for _,c,v in co)
for n,c,v in co: print(f"   {n:14s} {c} x {v} = {c*v:.4f}")
print(f"Z = {Z:.4f}  -> zones: >2.99 safe, 1.81-2.99 grey, <1.81 distress => {'SAFE' if Z>2.99 else 'GREY' if Z>=1.81 else 'DISTRESS'}")

print("\n"+"="*70); print("G. MAINTENANCE CAPEX ESTIMATE (Greenwald method)"); print("="*70)
ppe_gross_prior, sales_prior, sales_now, capex, dep = 2800.0, 3000.0, 3384.0, 300.0, 210.0
ppe_per_sales = ppe_gross_prior/sales_prior
growth_capex = (sales_now-sales_prior)*ppe_per_sales
print(f"Gross PP&E/Sales (prior) = {ppe_gross_prior}/{sales_prior} = {ppe_per_sales:.4f}")
print(f"Sales growth in $ = {sales_now-sales_prior}; growth capex = {sales_now-sales_prior} x {ppe_per_sales:.4f} = {growth_capex:.1f}")
print(f"Maintenance capex = total capex {capex} - growth {growth_capex:.1f} = {capex-growth_capex:.1f}")
print(f"(cross-check vs D&A {dep}: {'consistent' if abs(capex-growth_capex-dep)/dep<0.35 else 'divergent - investigate'})")

print("\n"+"="*70); print("H. NET DILUTION FROM SBC"); print("="*70)
so_begin=250.0e6; issued=6.2e6; buyback_sh=4.0e6
print(f"Shares begin {so_begin/1e6:.1f}m; issued for SBC {issued/1e6:.1f}m ({issued/so_begin*100:.2f}% gross dilution)")
print(f"Buyback retired {buyback_sh/1e6:.1f}m ({buyback_sh/so_begin*100:.2f}%)")
net=(issued-buyback_sh)/so_begin
print(f"Net dilution = ({issued/1e6:.1f} - {buyback_sh/1e6:.1f})/{so_begin/1e6:.1f} = {net*100:+.2f}%  => buyback did NOT cover dilution")
sbc=420e6; mcap=250e6*70
print(f"SBC ${sbc/1e6:.0f}m on mcap ${mcap/1e9:.2f}bn = {sbc/mcap*100:.2f}% of mcap/yr")
fcf_rep=1800e6
print(f"Reported FCF ${fcf_rep/1e6:.0f}m; FCF after charging SBC = ${(fcf_rep-sbc)/1e6:.0f}m ({(fcf_rep-sbc)/fcf_rep-1:+.1%} vs reported)")

print("\n"+"="*70); print("I. BUYBACK VALUE TEST + EPS ACCRETION"); print("="*70)
ni=900.0; sh=300.0; px=45.0; spend=600.0
eps0=ni/sh; sh_ret=spend/px; sh1=sh-sh_ret; eps1=ni/sh1
print(f"NI ${ni}m, shares {sh}m, EPS ${eps0:.3f}; price ${px}, P/E {px/eps0:.2f}x; spend ${spend}m")
print(f"Shares retired = {spend}/{px} = {sh_ret:.3f}m -> shares {sh1:.3f}m, EPS ${eps1:.4f} (+{(eps1/eps0-1)*100:.2f}%)")
print(f"Earnings yield bought = 1/(P/E) = {eps0/px*100:.2f}%  vs cost of equity 9.0% -> {'VALUE-ACCRETIVE' if eps0/px>0.09 else 'DILUTIVE to value (buying below own cost of capital)'}")
print("NOTE: EPS accretion is guaranteed whenever E/P > after-tax cost of cash; it is NOT a value test.")
