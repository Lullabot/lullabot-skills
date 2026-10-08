"""Exercise cleanup scope using synthetic Drupal storage, never a live site."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / 'scripts/cleanup.php'
STUB = r'''<?php
class DemoEntity {
  public function __construct(public $id, public $name) {}
  public function label() { return $this->name; }
  public function delete() { echo "DELETED:" . $this->id . "\n"; }
}
class DemoStorage {
  public function load($id) { return new DemoEntity($id, $id == 42 ? 'owned demo' : 'different entity'); }
}
class DemoManager {
  public function hasDefinition($type) { return TRUE; }
  public function getStorage($type) { return new DemoStorage(); }
}
class Drupal {
  public static function entityTypeManager() { return new DemoManager(); }
}
require $argv[1];
'''

class CleanupTests(unittest.TestCase):
    def run_cleanup(self, manifest, apply=False):
        with tempfile.TemporaryDirectory() as directory:
            entry = Path(directory, 'stub.php')
            entry.write_text(STUB)
            source = Path(directory, 'manifest.json')
            source.write_text(json.dumps(manifest))
            env = dict(os.environ, SEC_REVIEW_MANIFEST=str(source), SEC_REVIEW_APPLY='1' if apply else '')
            return subprocess.run(['php', str(entry), str(SCRIPT)], env=env, capture_output=True, text=True)
    def test_preview_does_not_delete(self):
        result = self.run_cleanup({'node': [{'id': 42, 'label': 'owned demo'}]})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('DELETED:', result.stdout)
        self.assertFalse(json.loads(result.stdout)['apply'])
    def test_apply_deletes_only_manifest_id(self):
        result = self.run_cleanup({'node': [{'id': 42, 'label': 'owned demo'}]}, True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('DELETED:'), 1)
        self.assertIn('DELETED:42', result.stdout)
    def test_identity_mismatch_prevents_all_deletions(self):
        result = self.run_cleanup({'node': [{'id': 42, 'label': 'owned demo'}, {'id': 43, 'label': 'owned demo'}]}, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('DELETED:', result.stdout)
    def test_protected_user_rejected(self):
        result = self.run_cleanup({'user': [{'id': 1, 'label': 'different entity'}]}, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('DELETED:', result.stdout)

if __name__ == '__main__':
    unittest.main()
