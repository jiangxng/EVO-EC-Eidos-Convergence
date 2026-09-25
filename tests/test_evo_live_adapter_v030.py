import unittest

from convergence.evo_live_adapter import LiveEvoAdapter


class LiveEvoAdapterTests(unittest.TestCase):
    def test_real_vertical_slice_transport_boundaries(self):
        calls = []
        def transport(method, path, body):
            calls.append((method, path, body))
            if path.endswith('/observation'):
                return {'contractVersion':'1.0.0','observationId':'obs-1','enterpriseId':'APM'}
            if path.endswith('/admit'):
                return {'admitted': True, 'executionStatus':'NOT_EXECUTED', 'authorization':'EVO_REEVALUATES_AT_EXECUTION'}
            return {'command': {'businessDataId':'bd-1'}, 'outcome': {'status':'EXECUTED'}, 'observation': {'observationId':'obs-2'}}

        evo = LiveEvoAdapter(transport=transport)
        self.assertEqual(evo.observation()['enterpriseId'], 'APM')
        admitted = evo.admit_command_proposal({'proposalId':'p1'})
        self.assertEqual(admitted['executionStatus'], 'NOT_EXECUTED')
        result = evo.execute_action({'actionRequestId':'a1'})
        self.assertEqual(result['outcome']['status'], 'EXECUTED')
        self.assertEqual([x[1] for x in calls], [
            '/api/v1/apm/observation',
            '/api/v1/apm/command-proposals/admit',
            '/api/v1/apm/actions/execute'
        ])

    def test_fail_closed_if_admission_executes(self):
        evo = LiveEvoAdapter(transport=lambda *_: {'executionStatus':'EXECUTED'})
        with self.assertRaises(RuntimeError):
            evo.admit_command_proposal({'proposalId':'p1'})


if __name__ == '__main__':
    unittest.main()
