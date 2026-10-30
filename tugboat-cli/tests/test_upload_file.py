"""Check upload payload roundtrips without calling a remote service."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('upload_file', Path(__file__).parents[1] / 'scripts/upload_file.py')
UPLOAD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPLOAD)

class UploadTests(unittest.TestCase):
    def test_roundtrip_quoted_destination_and_no_clobber(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory, "report'; touch INJECTED; '.html")
            data = b'\x00binary\xff\ncontents'
            payload = UPLOAD.build_command(data, str(destination))
            subprocess.run(payload, check=True, capture_output=True)
            self.assertEqual(destination.read_bytes(), data)
            failed = subprocess.run(UPLOAD.build_command(b'replacement', str(destination)), capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(destination.read_bytes(), data)
            self.assertFalse(Path('INJECTED').exists())
    def test_relative_destination_rejected(self):
        with self.assertRaises(ValueError):
            UPLOAD.build_command(b'data', '../../report.html')
    def test_default_is_preview_without_remote_call(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, 'report.html')
            source.write_text('<p>public fixture</p>')
            with patch.object(UPLOAD.subprocess, 'run') as remote:
                self.assertEqual(UPLOAD.main([str(source), '--service', 'service123', '--destination', '/tmp/report.html']), 0)
                remote.assert_not_called()

if __name__ == '__main__':
    unittest.main()
