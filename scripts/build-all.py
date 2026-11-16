"""Rebuild data/pages from the preserved V20 baseline; never touches user saves."""
import pathlib,runpy
R=pathlib.Path(__file__).resolve().parents[1]
runpy.run_path(str(R/'scripts/extend21.py'))
p=R/'assets/elden.js';body=p.read_text();marker='/* GNX 14.0 ELDEN RING DB.';assert marker in body
p.write_text((R/'assets/npc-core.js').read_text()+'\n'+(R/'assets/collection-core.js').read_text()+'\n'+(R/'assets/collection-loader.js').read_text()+'\n'+body[body.index(marker):])
for f in ['build-npc.py','build-story.py','build-collections.py','build-ledger.py']:runpy.run_path(str(R/'scripts'/f))

runpy.run_path(str(R/"scripts/release21.py"))
