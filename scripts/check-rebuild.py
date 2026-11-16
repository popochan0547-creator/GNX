"""Rebuild reproducibility and protected baseline checks; no network/user saves."""
import pathlib,hashlib,subprocess,json,sys
R=pathlib.Path(__file__).resolve().parents[1]
paths=[R/'index.html',*sorted((R/'assets').glob('*')),*sorted((R/'data').rglob('*')),*sorted((R/'elden').rglob('*.html')),R/'sitemap.xml']
hash=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(R)):hash(p) for p in paths if p.is_file()}
subprocess.run([sys.executable,str(R/'scripts/build-all.py')],check=True,stdout=subprocess.DEVNULL)
after={f:hash(R/f) for f in before}
assert before==after, [f for f in before if before[f]!=after[f]]
print('Rebuild deterministic:',len(before),'source/data/page files byte-identical after full rebuild.')
