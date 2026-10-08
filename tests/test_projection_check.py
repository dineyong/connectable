"""The CI asset check must detect drift and remain read-only."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectionCheckTests(unittest.TestCase):
    def test_real_asset_check_is_read_only(self):
        p = ROOT/'web/site-content-v2.js'
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        r = subprocess.run([sys.executable, str(ROOT/'web/derive-site-content.py'), '--check'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), before)

    def test_stale_asset_is_rejected_without_repair(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for folder in ('data', 'scripts', 'schemas'):
                shutil.copytree(ROOT/folder, root/folder, ignore=shutil.ignore_patterns('__pycache__'))
            (root/'web').mkdir()
            shutil.copy(ROOT/'web/derive-site-content.py', root/'web/derive-site-content.py')
            target = root/'web/site-content-v2.js'
            target.write_text('stale asset\n')
            r = subprocess.run([sys.executable, str(root/'web/derive-site-content.py'), '--check'], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('is stale', r.stderr)
            self.assertEqual(target.read_text(), 'stale asset\n')
