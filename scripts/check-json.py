"""Validate all JSON and the canonical collection CSV mapping, without save/network access."""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
def nonfinite(value):raise ValueError('Non-JSON numeric constant: '+value)
files=sorted(R.rglob('*.json'))
for p in files:json.loads(p.read_text(),parse_constant=nonfinite)
db=json.loads((R/'data/collections.json').read_text());rows=list(csv.DictReader((R/'docs/COLLECTION_LEDGER.csv').open(encoding='utf-8-sig')));byid={r['id']:r for r in rows};assert len(byid)==len(rows),'Duplicate CSV IDs'
for i in db['items']:
 r=byid[i['id']];assert r['entryId']==i['entryId'] and r['checkIds'].split(';')==i['checkIds'],i['id']
print(f'JSON parse OK: {len(files)} files; collection CSV mapping OK: {len(db["items"])} units.')
