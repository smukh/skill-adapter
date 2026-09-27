import importlib.util
from pathlib import Path
import unittest
from datetime import datetime, timezone, timedelta
import subprocess
import sys
import json

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/skill-adapter/scripts/model_profile.py'
spec = importlib.util.spec_from_file_location('identity', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class IdentityTests(unittest.TestCase):
    def test_known_and_explicit_alias(self):
        for value in ['gpt-6-astra', 'openai/gpt-6-astra', 'Astra 6']:
            self.assertEqual(m.resolve(value)['profile'], 'gpt-6-astra')
    def test_no_strength_or_prefix_guess(self):
        for value in ['gpt-6-sol', 'claude-opus-4-8', 'proxy/gpt-6-astra', 'gpt-6-astra-future']:
            self.assertEqual(m.resolve(value)['profile'], 'generic')
    def test_other_profiles(self):
        self.assertEqual(m.resolve('anthropic/claude-opus-5-5')['profile'], 'claude-5')
        self.assertEqual(m.resolve('Kimi K3')['profile'], 'kimi-k3')
    def test_ambiguous(self):
        for value in ['Auto', 'GPT-6', 'Claude', 'Kimi', 'Hermes', '']:
            with self.assertRaises(ValueError): m.resolve(value)
    def test_native_payloads(self):
        cases = [('claude-code', {'session_id':'a', 'model':{'id':'gpt-6-astra'}}),
                 ('cursor', {'conversation_id':'a', 'model':'auto', 'model_id':'gpt-6-astra'}),
                 ('kimi', {'session_id':'a', 'data':{'model':'gpt-6-astra'}}),
                 ('hermes', {'session_id':'a', 'model_id':'gpt-6-astra'}),
                 ('codex', {'session_id':'a', 'model_id':'gpt-6-astra'})]
        for host, data in cases:
            self.assertEqual(m.from_payload(host, data, 'a', live=True)['profile'], 'gpt-6-astra')
    def test_other_session_rejected(self):
        with self.assertRaises(ValueError):
            m.from_payload('cursor', {'conversation_id':'old', 'model':'gpt-6-astra'}, 'new', live=True)
    def test_saved_payload_needs_timestamp(self):
        with self.assertRaises(ValueError):
            m.from_payload('codex', {'session_id':'a','model_id':'gpt-6-astra'}, 'a')
    def test_stale_future_naive(self):
        now = datetime.now(timezone.utc)
        for stamp in [(now-timedelta(seconds=61)).isoformat(), (now+timedelta(seconds=20)).isoformat(), '2026-09-27T12:00:00']:
            with self.assertRaises(ValueError):
                m.from_payload('codex', {'session_id':'a', 'model_id':'gpt-6-astra', 'captured_at':stamp}, 'a', now=now)
    def test_fresh(self):
        now = datetime.now(timezone.utc)
        self.assertEqual(m.from_payload('codex', {'session_id':'a', 'model_id':'gpt-6-astra','captured_at':now.isoformat()}, 'a', now=now)['profile'], 'gpt-6-astra')
    def test_missing_native_model(self):
        with self.assertRaises(ValueError):
            m.from_payload('claude-code', {'session_id':'a'}, 'a', live=True)
    def test_cli_explicit_target_ignores_wrong_payload(self):
        result = subprocess.run([sys.executable,str(SCRIPT),'--target','kimi-k3','--payload','nonexistent.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0)
        self.assertEqual(json.loads(result.stdout)['profile'],'kimi-k3')
    def test_cli_unknown_evidence(self):
        result = subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads(result.stdout)['status'],'needs-model-evidence')

if __name__ == '__main__': unittest.main()
