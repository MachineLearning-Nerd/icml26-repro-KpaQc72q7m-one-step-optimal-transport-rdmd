"""Reduced local CPU diagnostic for RDMD's Gaussian-to-8-Gaussian toy (Claim 4).
This is not the paper's trained DMD/RDMD network: it uses a deterministic soft assignment
surrogate to expose the stated fidelity/correspondence tradeoff and segment crossings.
"""
import argparse, csv, json, math, random
from pathlib import Path


def centers():
    return [(4*math.cos(2*math.pi*j/8),4*math.sin(2*math.pi*j/8)) for j in range(8)]
def dist2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def proper_intersect(a,b,c,d):
    # strict crossing; shared endpoints/collinearity are excluded
    return cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0

def run(lam, seed, n):
    rng=random.Random(seed); cs=centers(); xs=[(rng.gauss(0,1),rng.gauss(0,1)) for _ in range(n)]
    ys=[]
    # lambda=0: angular target assignment; lambda>0: correspondence-biased nearest center.
    # This is a fixed, disclosed surrogate rather than neural RDMD optimization.
    for x in xs:
        ang=(math.atan2(x[1],x[0])%(2*math.pi)); angular=int((ang+math.pi/8)/(2*math.pi/8))%8
        nearest=min(range(8),key=lambda j:dist2(x,cs[j]))
        j=nearest if lam>=.2 else angular
        ys.append((cs[j][0]+rng.gauss(0,.35),cs[j][1]+rng.gauss(0,.35)))
    cost=sum(dist2(x,y) for x,y in zip(xs,ys))/n
    # target fidelity: radial mean squared error relative to radius-4 target ring
    fidelity=sum((math.hypot(y[0],y[1])-4)**2 for y in ys)/n
    pairs=0
    for i in range(n):
      for j in range(i): pairs+=proper_intersect(xs[i],ys[i],xs[j],ys[j])
    return xs,ys,{"lambda":lam,"seed":seed,"n":n,"transport_mse":cost,"radial_target_mse":fidelity,"trajectory_intersections":pairs}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='outputs/claim4_rdmd_2d_toy');p.add_argument('--n',type=int,default=160);a=p.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True); rows=[]; raw={}
 for lam in (0.0,.2,1.0):
  for seed in (17,23,31):
   x,y,row=run(lam,seed,a.n);rows.append(row);raw[f'{lam}-{seed}']={"x":x,"y":y}
 with (out/'results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'raw.json').write_text(json.dumps(raw,sort_keys=True))
 summary={"verdict":"toy","scope":"Reduced deterministic assignment surrogate preserving 2-D Gaussian/8-Gaussian, squared transport cost, target-fidelity proxy, and trajectory-intersection metric; not trained RDMD.","source_claim":"Section 5.1", "means":{str(l):{k:sum(r[k] for r in rows if r['lambda']==l)/3 for k in ('transport_mse','radial_target_mse','trajectory_intersections')} for l in (0.0,.2,1.0)},"controls":"lambda=0 unregularized surrogate and lambda=1 high-regularization surrogate"}
 (out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 (out/'config.json').write_text(json.dumps({"n":a.n,"seeds":[17,23,31],"lambdas":[0,.2,1.],"noise_sd":.35},indent=2)+'\n')
if __name__=='__main__': main()
