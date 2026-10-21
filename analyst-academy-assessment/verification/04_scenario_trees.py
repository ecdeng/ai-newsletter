print("SCENARIO TREE v2 (non-degenerate)")
px=100.0; bull,base_,bear=150.0,100.0,70.0
for pbe in [0.20,0.25,0.30]:
    # p*bull + (1-p-pbe)*base + pbe*bear = px
    p=(px - pbe*bear - (1-pbe)*base_)/(bull-base_)
    chk=p*bull+(1-p-pbe)*base_+pbe*bear
    print(f"  bear prob {pbe:.0%} -> market-implied bull prob {p*100:5.2f}%  (EV check ${chk:.4f}, base prob {(1-p-pbe)*100:.1f}%)")
print()
# our underwritten view
for pb,pba,pbe in [(0.35,0.45,0.20),(0.30,0.45,0.25)]:
    ev=pb*bull+pba*base_+pbe*bear
    assert abs(pb+pba+pbe-1)<1e-12
    print(f"  our probs {pb:.0%}/{pba:.0%}/{pbe:.0%}: EV ${ev:.2f} = {(ev/px-1)*100:+.1f}% expected return")
print(f"\n  asymmetry (upside to bull)/(downside to bear) = {(bull-px)/(px-bear):.2f}x")
print(f"  upside {bull/px-1:+.0%}, downside {bear/px-1:+.0%}")
