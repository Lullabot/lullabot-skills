#!/usr/bin/env python3
"""Verify missing crawler prerequisites never trigger package installation."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class CrawlPrerequisiteTest(unittest.TestCase):
    def test_missing_environment_stops_without_installing(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "skill"
            scripts = skill / "scripts"
            scripts.mkdir(parents=True)
            script = scripts / "crawl_site.sh"
            # Normalize original CRLF so this checks setup behavior, not shell parsing.
            script.write_text(Path(__file__).with_name("crawl_site.sh").read_text())
            (skill / "tools" / "LibreCrawl").mkdir(parents=True)
            tools = Path(directory) / "bin"
            tools.mkdir()
            marker = Path(directory) / "installer-called"
            # Stub installers so the test can never install dependencies.
            for command in ("python3", "pip"):
                stub = tools / command
                stub.write_text('#!/bin/sh\n: > "$INSTALL_MARKER"\nexit 23\n')
                stub.chmod(0o755)
            env = dict(os.environ, PATH=f"{tools}:{os.environ['PATH']}", INSTALL_MARKER=str(marker))
            result = subprocess.run(
                ["bash", str(script), "https://example.com"],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists(), "Crawler attempted implicit dependency setup")
            self.assertFalse((skill / "tools" / "LibreCrawl" / "venv").exists())


if __name__ == "__main__":
    unittest.main()
