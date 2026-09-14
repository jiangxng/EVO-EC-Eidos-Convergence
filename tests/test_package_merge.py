import unittest,tempfile,json
from pathlib import Path
from convergence.package_manager import FunctionPackManager
from convergence.knowledge_merge import merge_exports
ROOT=Path(__file__).resolve().parents[1]
class PackMergeTests(unittest.TestCase):
 def test_function_pack_backup_install(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);m=FunctionPackManager();p=m.backup(ROOT/'enterprise-packs/apm/function-packs/procurement',d/'p.ecpack');self.assertTrue(m.verify(p)['ok']);r=m.install(p,d/'installed');self.assertEqual(r['current'],'0.1.0')
 def test_merge_preserves_scope_and_provenance(self):
  a=json.loads((ROOT/'examples/knowledge/ec-a.json').read_text());b=json.loads((ROOT/'examples/knowledge/ec-b.json').read_text());r=merge_exports(a,b);self.assertEqual(len(r['merged']),4);self.assertTrue(all('mergedProvenance' in x for x in r['merged']));self.assertTrue(any(e['class']=='SCOPE_DIFFERENT' for e in r['audit']['events']))
 def test_conflict_is_not_overwritten(self):
  a={'ecId':'A','records':[{'recordId':'1','subject':'X','predicate':'p','value':1,'scope':'S','validFrom':'T','provenance':{'sourceEc':'A'}}]};b={'ecId':'B','records':[{'recordId':'2','subject':'X','predicate':'p','value':2,'scope':'S','validFrom':'T','provenance':{'sourceEc':'B'}}]};r=merge_exports(a,b);self.assertEqual(len(r['conflicts']),1);self.assertEqual(r['conflicts'][0]['resolution'],'UNRESOLVED')
if __name__=='__main__': unittest.main()
