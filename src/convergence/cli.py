from __future__ import annotations
import argparse, json, platform, sys
from pathlib import Path
from . import __version__
from .scenario import run_apm
from .package_manager import FunctionPackManager
from .knowledge_merge import merge_exports
from .util import load_json,dump_json
from .evo_adapter import LiveEvoAdapter
from .eidos_adapter import verify_with_real_eidos_repo

ROOT=Path(__file__).resolve().parents[2]

def emit(v): print(json.dumps(v,ensure_ascii=False,indent=2))
def main(argv=None):
    p=argparse.ArgumentParser(prog='convergence');sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('doctor');sub.add_parser('e2e');sub.add_parser('validate-contracts')
    lp=sub.add_parser('live-check');lp.add_argument('--evo');lp.add_argument('--eidos-repo')
    fp=sub.add_parser('function-pack-smoke')
    km=sub.add_parser('knowledge-merge-smoke')
    a=p.parse_args(argv)
    if a.cmd=='doctor':
        import ec
        emit({'convergenceVersion':__version__,'python':platform.python_version(),'platform':platform.platform(),'ecImport':'ok','ecModule':str(Path(ec.__file__).resolve()),'status':'ok'})
    elif a.cmd=='validate-contracts':
        expected={'evo-intelligence-feed-v0.1.schema.json','ec-command-proposal-v0.1.schema.json','ec-experience-proposal-v0.1.schema.json','eidos-action-request-v0.1.schema.json','evo-outcome-v0.1.schema.json','enterprise-function-pack-v0.1.schema.json','knowledge-merge-v0.1.schema.json'}
        found={x.name for x in (ROOT/'contracts').glob('*.schema.json')};emit({'ok':expected<=found,'expected':sorted(expected),'found':sorted(found)})
        if not expected<=found: raise SystemExit(2)
    elif a.cmd=='e2e': emit(run_apm(ROOT,ROOT/'runtime-output/apm'))
    elif a.cmd=='live-check':
        r={'convergenceVersion':__version__}
        if a.evo: r['evo']=LiveEvoAdapter(a.evo).check()
        xp=ROOT/'runtime-output/apm/03-ec-experience-proposal.json'
        if a.eidos_repo:
            if not xp.exists(): run_apm(ROOT,ROOT/'runtime-output/apm')
            r['eidos']=verify_with_real_eidos_repo(str(xp),a.eidos_repo)
        emit(r)
    elif a.cmd=='function-pack-smoke':
        m=FunctionPackManager();out=ROOT/'runtime-output/packs/apm-procurement-v0.1.0.ecpack';m.backup(ROOT/'enterprise-packs/apm/function-packs/procurement',out);v=m.verify(out);ins=m.install(out,ROOT/'runtime-output/installed-packs');emit({'backup':str(out),'verify':v,'install':ins,'status':'PASS' if v['ok'] else 'FAIL'})
    elif a.cmd=='knowledge-merge-smoke':
        r=merge_exports(load_json(ROOT/'examples/knowledge/ec-a.json'),load_json(ROOT/'examples/knowledge/ec-b.json'));out=dump_json(ROOT/'runtime-output/knowledge-merge.json',r);emit({'output':str(out),'mergedCount':len(r['merged']),'conflictCount':len(r['conflicts']),'auditEvents':len(r['audit']['events']),'status':'PASS'})
