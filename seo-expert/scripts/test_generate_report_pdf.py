#!/usr/bin/env python3
"""Unit tests for generate_report_pdf.py parsing functions."""
import json
import tempfile
from pathlib import Path
import unittest

from generate_report_pdf import (
    _unescape_entities,
    escape,
    escape_for_paragraph,
    extract_lighthouse_summary,
    load_lighthouse_json,
    parse_args,
)


class TestUnescapeEntities(unittest.TestCase):
    """Tests for _unescape_entities function."""

    def test_unescapes_amp(self):
        self.assertEqual(_unescape_entities("foo &amp; bar"), "foo & bar")

    def test_unescapes_quot(self):
        self.assertEqual(_unescape_entities("&quot;hello&quot;"), '"hello"')

    def test_unescapes_gt_lt(self):
        self.assertEqual(_unescape_entities("&lt;tag&gt;"), "<tag>")

    def test_handles_plain_text(self):
        self.assertEqual(_unescape_entities("no entities here"), "no entities here")

    def test_handles_multiple_entities(self):
        self.assertEqual(
            _unescape_entities("&lt;a href=&quot;url&quot;&gt;"),
            '<a href="url">',
        )


class TestEscape(unittest.TestCase):
    """Tests for escape function."""

    def test_escapes_ampersand(self):
        self.assertEqual(escape("foo & bar"), "foo &amp; bar")

    def test_escapes_angle_brackets(self):
        self.assertEqual(escape("<script>"), "&lt;script&gt;")

    def test_handles_empty_string(self):
        self.assertEqual(escape(""), "")

    def test_handles_none(self):
        self.assertEqual(escape(None), "")

    def test_round_trip_entities(self):
        # Input with HTML entities should be unescaped then re-escaped
        self.assertEqual(escape("&amp;"), "&amp;")


class TestEscapeForParagraph(unittest.TestCase):
    """Tests for escape_for_paragraph function."""

    def test_preserves_bold_tags(self):
        result = escape_for_paragraph("<b>bold</b>")
        self.assertIn("<b>", result)
        self.assertIn("</b>", result)

    def test_preserves_italic_tags(self):
        result = escape_for_paragraph("<i>italic</i>")
        self.assertIn("<i>", result)
        self.assertIn("</i>", result)

    def test_converts_strong_to_bold(self):
        result = escape_for_paragraph("<strong>text</strong>")
        self.assertIn("<b>", result)
        self.assertIn("</b>", result)

    def test_converts_em_to_italic(self):
        result = escape_for_paragraph("<em>text</em>")
        self.assertIn("<i>", result)
        self.assertIn("</i>", result)

    def test_colors_checkmark_green(self):
        result = escape_for_paragraph("✓")
        self.assertIn('color="green"', result)

    def test_colors_cross_red(self):
        result = escape_for_paragraph("✗")
        self.assertIn('color="red"', result)

    def test_handles_code_tags(self):
        result = escape_for_paragraph("<code>example</code>")
        self.assertIn("Courier", result)

    def test_handles_empty_string(self):
        self.assertEqual(escape_for_paragraph(""), "")


class TestExtractLighthouseSummary(unittest.TestCase):
    """Tests for extract_lighthouse_summary function."""

    def test_extracts_category_scores(self):
        data = {
            "categories": {
                "performance": {"title": "Performance", "score": 0.85},
                "accessibility": {"title": "Accessibility", "score": 0.92},
            },
            "audits": {},
        }
        summary = extract_lighthouse_summary(data)
        self.assertEqual(len(summary["categoryScores"]), 2)
        scores = {c["id"]: c["score"] for c in summary["categoryScores"]}
        self.assertEqual(scores["performance"], 85)
        self.assertEqual(scores["accessibility"], 92)

    def test_extracts_key_audits(self):
        data = {
            "categories": {},
            "audits": {
                "first-contentful-paint": {
                    "title": "First Contentful Paint",
                    "score": 0.95,
                    "displayValue": "1.2 s",
                },
                "meta-description": {
                    "title": "Meta Description",
                    "score": 1.0,
                    "displayValue": "",
                },
            },
        }
        summary = extract_lighthouse_summary(data)
        self.assertEqual(len(summary["keyAudits"]), 2)

    def test_status_pass_for_high_score(self):
        data = {
            "categories": {},
            "audits": {
                "meta-description": {"title": "Meta", "score": 1.0},
            },
        }
        summary = extract_lighthouse_summary(data)
        self.assertEqual(summary["keyAudits"][0]["status"], "Pass")

    def test_status_fail_for_low_score(self):
        data = {
            "categories": {},
            "audits": {
                "meta-description": {"title": "Meta", "score": 0.3},
            },
        }
        summary = extract_lighthouse_summary(data)
        self.assertEqual(summary["keyAudits"][0]["status"], "Fail")

    def test_status_needs_improvement_for_mid_score(self):
        data = {
            "categories": {},
            "audits": {
                "meta-description": {"title": "Meta", "score": 0.7},
            },
        }
        summary = extract_lighthouse_summary(data)
        self.assertEqual(summary["keyAudits"][0]["status"], "Needs improvement")

    def test_handles_missing_fields(self):
        data = {}
        summary = extract_lighthouse_summary(data)
        self.assertEqual(summary["categoryScores"], [])
        self.assertEqual(summary["keyAudits"], [])
        self.assertEqual(summary["requestedUrl"], "")


class TestLoadLighthouseJson(unittest.TestCase):
    """Tests for load_lighthouse_json function."""

    def test_loads_valid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"requestedUrl": "https://example.com"}, f)
            f.flush()
            result = load_lighthouse_json(Path(f.name))
            self.assertEqual(result["requestedUrl"], "https://example.com")

    def test_strips_base64_data(self):
        # Simulate Lighthouse JSON with embedded base64 screenshot data
        data_with_base64 = '{"audits": {"screenshot": {"data": "data:image/png;base64,iVBOR..."}}}'
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(data_with_base64)
            f.flush()
            result = load_lighthouse_json(Path(f.name))
            # The base64 data should be stripped
            self.assertEqual(result["audits"]["screenshot"]["data"], "")


class TestParseArgs(unittest.TestCase):
    """Tests for argument parsing."""

    def test_defaults(self):
        args = parse_args([])
        self.assertIsNotNone(args.audit)
        self.assertIsNotNone(args.desktop)
        self.assertIsNotNone(args.mobile)
        self.assertIsNotNone(args.output)
        self.assertFalse(args.include_action_plan)

    def test_custom_audit_path(self):
        args = parse_args(["--audit", "/path/to/audit.md"])
        self.assertEqual(args.audit, Path("/path/to/audit.md"))

    def test_short_flags(self):
        args = parse_args(["-a", "a.md", "-d", "d.json", "-m", "m.json", "-o", "out.pdf"])
        self.assertEqual(args.audit, Path("a.md"))
        self.assertEqual(args.desktop, Path("d.json"))
        self.assertEqual(args.mobile, Path("m.json"))
        self.assertEqual(args.output, Path("out.pdf"))

    def test_include_action_plan_flag(self):
        args = parse_args(["--include-action-plan"])
        self.assertTrue(args.include_action_plan)


if __name__ == "__main__":
    unittest.main()
