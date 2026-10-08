"""Behavior checks for the loopback-only prototype server."""
import importlib.util
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import urlopen

SPEC = importlib.util.spec_from_file_location('dev_server', Path(__file__).parents[1] / 'scripts/dev_server.py')
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)

class PrototypeServerTests(unittest.TestCase):
    def test_loopback_static_and_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'index.html').write_text('<p>Static page</p>')
            with SERVER.create_server(Path(directory), 0) as httpd:
                self.assertEqual(httpd.server_address[0], '127.0.0.1')
                thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                thread.start()
                try:
                    base = f'http://127.0.0.1:{httpd.server_port}'
                    self.assertEqual(urlopen(base + '/').read(), b'<p>Static page</p>')
                    with urlopen(base + '/api/example') as response:
                        self.assertIn('text/html', response.headers['Content-Type'])
                        self.assertEqual(response.read(), b'<div>Response HTML</div>')
                finally:
                    httpd.shutdown()
                    thread.join()
    def test_directory_must_exist(self):
        with self.assertRaises(ValueError):
            SERVER.create_server(Path('/path/that/does/not/exist'), 0)

if __name__ == '__main__':
    unittest.main()
