import csv,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_toy_tradeoff_and_artifacts():
 with tempfile.TemporaryDirectory() as d:
  subprocess.run(['python3','src/claim4_rdmd_2d_toy.py','--out',d,'--n','80'],cwd=ROOT,check=True)
  rows=list(csv.DictReader(open(Path(d)/'results.csv')))
  assert len(rows)==9
  assert all(float(r['trajectory_intersections'])>=0 for r in rows)
  s=json.load(open(Path(d)/'summary.json')); assert s['verdict']=='toy'
