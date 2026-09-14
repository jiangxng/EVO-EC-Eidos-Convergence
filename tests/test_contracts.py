import unittest
from pathlib import Path
import json
from convergence.contracts import *
from convergence.scenario import run_apm
ROOT=Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
 def setUp(self): self.summary=run_apm(ROOT,ROOT/'runtime-output/test-apm')
 def load(self,n): return json.loads((ROOT/'runtime-output/test-apm'/n).read_text(encoding='utf-8'))
 def test_feed(self): self.assertTrue(validate_evo_feed(self.load('01-evo-intelligence-feed.json')).ok)
 def test_command(self): self.assertTrue(validate_command_proposal(self.load('02-ec-command-proposal.json')).ok)
 def test_eidos(self): self.assertTrue(validate_eidos_proposal(self.load('03-ec-experience-proposal.json')).ok)
 def test_action(self): self.assertTrue(validate_action_request(self.load('04-eidos-action-request.json')).ok)
 def test_outcome(self): self.assertTrue(validate_outcome(self.load('05-evo-outcome.json')).ok)
 def test_e2e(self):
  self.assertEqual(self.summary['status'],'PASS');self.assertEqual(self.summary['approvedSupplier'],'SUPPLIER-B');self.assertTrue(self.summary['promiseProtected'])
 def test_learning_is_candidate_not_truth(self):
  learned=self.load('06-ec-learning.json');self.assertTrue(learned);self.assertTrue(all(x['status']=='candidate' for x in learned))
 def test_eidos_has_composition_context_shape(self):
  p=self.load('03-ec-experience-proposal.json');self.assertIn('composition',p);self.assertIn('context',p);self.assertNotIn('regions',p)
if __name__=='__main__': unittest.main()
