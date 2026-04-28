#!/usr/bin/env python3
"""
Combine SEO audit (markdown) and Lighthouse desktop/mobile (JSON) reports
into a single human-readable PDF. Order: SEO audit first, then Desktop
Lighthouse, then Mobile Lighthouse.

Usage:
    python generate_report_pdf.py [options]

Examples:
    # Use defaults (looks for files in script directory)
    python generate_report_pdf.py

    # Specify all input files
    python generate_report_pdf.py --audit report.md --desktop lh-desktop.json --mobile lh-mobile.json

    # Include the Action Plan section (excluded by default)
    python generate_report_pdf.py --include-action-plan
"""
import argparse
import json
import re
import sys
from pathlib import Path

import markdown
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

REPORT_DIR = Path(__file__).resolve().parent

# Default file paths (can be overridden via CLI)
DEFAULT_SEO_AUDIT = REPORT_DIR / "seo-audit-agr-georgia-gov.md"
DEFAULT_LIGHTHOUSE_DESKTOP = REPORT_DIR / "lighthouse-desktop.json"
DEFAULT_LIGHTHOUSE_MOBILE = REPORT_DIR / "lighthouse-mobile.json"
DEFAULT_OUTPUT_PDF = REPORT_DIR / "combined-seo-and-lighthouse-report.pdf"

# Lullabot brand style (from lullabot.com – clean, professional, red accent)
LULLABOT_RED = colors.HexColor("#E31837")
LULLABOT_DARK = colors.HexColor("#1a1a1a")
LULLABOT_GRAY = colors.HexColor("#444444")
LULLABOT_BORDER = colors.HexColor("#dddddd")
LULLABOT_TABLE_HEADER = colors.HexColor("#1a1a1a")
LULLABOT_CODE_BG = colors.HexColor("#f0f0f0")
LULLABOT_CODE_BORDER = colors.HexColor("#cccccc")

KEY_AUDIT_IDS = {
    "first-contentful-paint",
    "largest-contentful-paint",
    "speed-index",
    "total-blocking-time",
    "cumulative-layout-shift",
    "interactive",
    "server-response-time",
    "render-blocking-resources",
    "uses-responsive-images",
    "meta-description",
    "document-title",
    "link-text",
    "crawlable-anchors",
    "html-has-lang",
    "image-alt",
    "viewport",
    "is-on-https",
}


def load_lighthouse_json(path: Path) -> dict:
    """Load Lighthouse JSON, stripping huge base64 data to avoid memory issues."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    raw = re.sub(r'"data": "data:[^"]*"', '"data": ""', raw)
    return json.loads(raw)


def extract_lighthouse_summary(data: dict) -> dict:
    """Extract category scores and key audits for human-readable summary."""
    categories = data.get("categories", {})
    audits = data.get("audits", {})

    category_scores = []
    for cat_id, cat in categories.items():
        if isinstance(cat, dict) and "score" in cat:
            score = cat["score"]
            title = cat.get("title", cat_id)
            if score is not None:
                pct = round(score * 100)
                category_scores.append({"id": cat_id, "title": title, "score": pct})

    key_audits = []
    for audit_id in KEY_AUDIT_IDS:
        a = audits.get(audit_id)
        if not a or not isinstance(a, dict):
            continue
        title = a.get("title", audit_id)
        score = a.get("score")
        display_value = a.get("displayValue", "") or ""
        if score is not None:
            status = "Pass" if score >= 0.9 else ("Fail" if score < 0.5 else "Needs improvement")
        else:
            status = "N/A"
        key_audits.append({
            "title": title,
            "score": score,
            "displayValue": display_value,
            "status": status,
        })

    return {
        "requestedUrl": data.get("requestedUrl", ""),
        "fetchTime": data.get("fetchTime", ""),
        "categoryScores": category_scores,
        "keyAudits": key_audits,
    }


def _strip_backslash_escapes(s: str) -> str:
    r"""Remove markdown backslash escapes (e.g. \< becomes <, \- becomes -).

    Google Docs and some editors export markdown with backslash-escaped
    punctuation like ``\< 2.5s`` which should display as ``< 2.5s``.
    """
    return re.sub(r"\\([\\`*_{}[\]()#+\-.!<>~|])", r"\1", s)


def _unescape_entities(s: str) -> str:
    """Replace HTML entities with actual characters so we don't double-encode.
    PDF should show & " > < not &amp; &quot; &gt; &lt;
    """
    return (
        s.replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&gt;", ">")
        .replace("&lt;", "<")
    )


def escape(s: str) -> str:
    """Escape for ReportLab Paragraph (XML-style)."""
    if not s:
        return ""
    s = _unescape_entities(s)
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# Placeholders to protect ReportLab-supported tags from escaping
_PARAPH_PLACEHOLDERS = [
    ("<b>", "\x01B\x01"),
    ("</b>", "\x01/B\x01"),
    ("<i>", "\x01I\x01"),
    ("</i>", "\x01/I\x01"),
    ("<br/>", "\x01BR\x01"),
    ("<br>", "\x01BR\x01"),
]


def escape_for_paragraph(s: str) -> str:
    """Escape for ReportLab Paragraph but keep <b>, <i>, <br/> so they render as bold/italic/line break.
    Converts <strong> to <b>. Strips <a> tags (keeps inner text). Renders <code>...</code> as monospace.
    Unescapes &amp; &quot; &gt; &lt; first so PDF shows & " > < not the entity text.
    """
    if not s:
        return ""
    s = _unescape_entities(s)

    # Extract <code>...</code> and replace with placeholders; inner content will be escaped once
    code_blocks = []

    def replace_code(match):
        inner = match.group(1)
        inner_escaped = (
            inner.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        idx = len(code_blocks)
        code_blocks.append(inner_escaped)
        return f"\x02CODE_{idx}\x02"

    s = re.sub(r"<code>(.*?)</code>", replace_code, s, flags=re.DOTALL | re.IGNORECASE)

    # Protect check/cross so we can color them after escaping
    s = s.replace("✓", "\x03CHECK\x03").replace("✗", "\x03CROSS\x03")

    s = s.replace("<strong>", "<b>").replace("</strong>", "</b>")
    s = s.replace("<em>", "<i>").replace("</em>", "</i>")
    # Strip <a> tags but keep their inner text (ReportLab Paragraph doesn't support links)
    s = re.sub(r"<a\s[^>]*>(.*?)</a>", r"\1", s, flags=re.DOTALL | re.IGNORECASE)
    for tag, ph in _PARAPH_PLACEHOLDERS:
        s = s.replace(tag, ph)
    s = (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    for tag, ph in _PARAPH_PLACEHOLDERS:
        s = s.replace(ph, tag)

    # Green ✓ and red ✗
    s = s.replace("\x03CHECK\x03", '<font color="green">✓</font>').replace(
        "\x03CROSS\x03", '<font color="red">✗</font>'
    )

    # Restore code blocks as monospace
    for i, block in enumerate(code_blocks):
        s = s.replace(
            f"\x02CODE_{i}\x02",
            f'<font face="Courier" size="8">{block}</font>',
        )
    return s


def md_to_flowables(md_path: Path, styles: dict, skip_action_plan: bool = True) -> list:
    """Convert markdown file to a list of ReportLab flowables.

    Args:
        md_path: Path to the markdown file.
        styles: ReportLab paragraph styles dictionary.
        skip_action_plan: If True, removes the "## Action Plan" section from output.
    """
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Strip markdown backslash escapes (e.g. \< from Google Docs exports)
    text = _strip_backslash_escapes(text)

    # Optionally remove Action Plan section
    if skip_action_plan:
        text = re.sub(
            r"\n## Action Plan\n\n.*?(?=\n\n---\n\n## Monitoring & Measurement)",
            "",
            text,
            flags=re.DOTALL,
        )

    # Use markdown to get HTML, then split into blocks for flowables
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    flowables = []

    # Simple HTML block extraction (split by tags)
    # Handle h1, h2, h3, p, table, pre/code, ol/ul lists
    style_map = {"h1": "Heading1", "h2": "Heading2", "h3": "Heading3", "p": "Normal"}

    # Strip outer div and split by block-level tags
    part = re.sub(r"^<div[^>]*>|</div>\s*$", "", html)
    # Split by opening tags
    blocks = re.split(r"(<h[1-3]>|<p>|<table>|<pre>|<[ou]l>|</table>|</pre>|</[ou]l>)", part, flags=re.I)

    i = 0
    while i < len(blocks):
        block = blocks[i]
        if re.match(r"<h1>", block, re.I):
            i += 1
            if i < len(blocks):
                content = re.sub(r"</h1>.*", "", blocks[i], flags=re.DOTALL | re.I)
                content = re.sub(r"<[^>]+>", "", content).strip()
                if content:
                    flowables.append(Paragraph(escape_for_paragraph(content), styles["Heading1"]))
                    flowables.append(Spacer(1, 0.15 * inch))
            i += 1
            continue
        if re.match(r"<h2>", block, re.I):
            i += 1
            if i < len(blocks):
                content = re.sub(r"</h2>.*", "", blocks[i], flags=re.DOTALL | re.I)
                content = re.sub(r"<[^>]+>", "", content).strip()
                if content:
                    flowables.append(Paragraph(escape_for_paragraph(content), styles["Heading2"]))
                    flowables.append(Spacer(1, 0.12 * inch))
            i += 1
            continue
        if re.match(r"<h3>", block, re.I):
            i += 1
            if i < len(blocks):
                content = re.sub(r"</h3>.*", "", blocks[i], flags=re.DOTALL | re.I)
                content = re.sub(r"<[^>]+>", "", content).strip()
                if content:
                    flowables.append(Paragraph(escape_for_paragraph(content), styles["Heading3"]))
                    flowables.append(Spacer(1, 0.1 * inch))
            i += 1
            continue
        if re.match(r"<p>", block, re.I):
            i += 1
            if i < len(blocks):
                content = re.sub(r"</p>.*", "", blocks[i], flags=re.DOTALL | re.I)
                # Keep <strong>, <em>, <br/> for Paragraph
                content = content.replace("<br />", "<br/>").replace("<br>", "<br/>").strip()
                content = escape_for_paragraph(content)
                # Remove unsupported tags but preserve <b>, <i>, <br/>, <font ...>
                content = re.sub(r"<(?!b>|/b>|i>|/i>|br/>|font[ >]|/font>)[^>]+>", "", content)
                if content:
                    flowables.append(Paragraph(content, styles["Normal"]))
                    flowables.append(Spacer(1, 0.08 * inch))
            i += 1
            continue
        if re.match(r"<table>", block, re.I):
            i += 1
            table_html = []
            while i < len(blocks) and not re.match(r"</table>", blocks[i], re.I):
                table_html.append(blocks[i])
                i += 1
            if i < len(blocks):
                i += 1  # skip </table>
            full_table = "".join(table_html)
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", full_table, re.DOTALL | re.I)
            data = []
            for row_idx, row in enumerate(rows):
                cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.DOTALL | re.I)
                cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
                # Use Paragraph so ✓/✗ get green/red; header row (row 0) gets white text
                if row_idx == 0:
                    cells = [
                        Paragraph(
                            '<font color="white">' + escape_for_paragraph(c[:80]) + "</font>",
                            styles["Normal"],
                        )
                        for c in cells
                    ]
                else:
                    cells = [
                        Paragraph(escape_for_paragraph(c[:80]), styles["Normal"])
                        for c in cells
                    ]
                if cells:
                    data.append(cells)
            if data:
                t = Table(data, repeatRows=1)
                t.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), LULLABOT_TABLE_HEADER),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 9),
                            ("GRID", (0, 0), (-1, -1), 0.5, LULLABOT_BORDER),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ]
                    )
                )
                flowables.append(t)
                flowables.append(Spacer(1, 0.2 * inch))
            continue
        if re.match(r"<[ou]l>", block, re.I):
            is_ordered = block.lower().startswith("<ol")
            i += 1
            list_html = []
            while i < len(blocks) and not re.match(r"</[ou]l>", blocks[i], re.I):
                list_html.append(blocks[i])
                i += 1
            if i < len(blocks):
                i += 1  # skip </ol> or </ul>
            full_list = "".join(list_html)
            items = re.findall(r"<li>(.*?)</li>", full_list, re.DOTALL | re.I)
            for item_idx, item in enumerate(items):
                # Keep inline formatting, strip other tags
                item = item.replace("<br />", "<br/>").replace("<br>", "<br/>").strip()
                item = escape_for_paragraph(item)
                item = re.sub(r"<[^/].*?>", "", item)
                item = re.sub(r"</[^>]+>", "", item)
                if is_ordered:
                    prefix = f"{item_idx + 1}. "
                else:
                    prefix = "\u2022 "  # bullet
                if item:
                    flowables.append(
                        Paragraph(
                            f"{prefix}{item}",
                            styles["ListItem"],
                        )
                    )
            if items:
                flowables.append(Spacer(1, 0.08 * inch))
            continue
        if re.match(r"<pre>", block, re.I):
            i += 1
            if i < len(blocks):
                content = re.sub(r"</pre>.*", "", blocks[i], flags=re.DOTALL | re.I)
                # Strip <code>...</code> wrapper if present (markdown fenced blocks)
                content = re.sub(r"</?code>", "", content, flags=re.I)
                content = re.sub(r"<[^>]+>", "", content).strip()
                code_flowable = make_code_block_flowable(content, styles)
                if code_flowable:
                    flowables.append(code_flowable)
                    flowables.append(Spacer(1, 0.15 * inch))
            i += 1
            continue
        i += 1

    # If we got nothing from HTML parsing, fall back to raw paragraphs by line
    if not flowables:
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("# "):
                flowables.append(Paragraph(escape_for_paragraph(line[2:]), styles["Heading1"]))
            elif line.startswith("## "):
                flowables.append(Paragraph(escape_for_paragraph(line[3:]), styles["Heading2"]))
            elif line.startswith("### "):
                flowables.append(Paragraph(escape_for_paragraph(line[4:]), styles["Heading3"]))
            elif line.startswith("|") and "|" in line[1:]:
                # Table row - collect following table rows and make one table
                rows = [line]
                j = text.split("\n").index(line) + 1
                lines = text.split("\n")
                while j < len(lines) and lines[j].strip().startswith("|"):
                    rows.append(lines[j].strip())
                    j += 1
                if rows and not all(re.match(r"^[\s|\-]+$", r) for r in rows):
                    rows_list = [
                        row for row in rows if not re.match(r"^[\s|\-]+$", row)
                    ]
                    data = []
                    for row_idx, row in enumerate(rows_list):
                        raw_cells = [cell.strip() for cell in row.split("|")[1:-1]]
                        if row_idx == 0:
                            cells = [
                                Paragraph(
                                    '<font color="white">'
                                    + escape_for_paragraph(c)
                                    + "</font>",
                                    styles["Normal"],
                                )
                                for c in raw_cells
                            ]
                        else:
                            cells = [
                                Paragraph(
                                    escape_for_paragraph(c), styles["Normal"]
                                )
                                for c in raw_cells
                            ]
                        data.append(cells)
                    if data:
                        t = Table(data, repeatRows=1)
                        t.setStyle(
                            TableStyle(
                                [
                                    ("BACKGROUND", (0, 0), (-1, 0), LULLABOT_TABLE_HEADER),
                                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                                    ("GRID", (0, 0), (-1, -1), 0.5, LULLABOT_BORDER),
                                ]
                            )
                        )
                        flowables.append(t)
                        flowables.append(Spacer(1, 0.15 * inch))
                continue
            else:
                flowables.append(Paragraph(escape_for_paragraph(line), styles["Normal"]))
            flowables.append(Spacer(1, 0.06 * inch))

    return flowables


# Code blocks use Lullabot palette (see LULLABOT_CODE_* above)
CODE_BLOCK_BG = LULLABOT_CODE_BG
CODE_BLOCK_BORDER = LULLABOT_CODE_BORDER


def make_code_block_flowable(content: str, styles: dict):
    """Build a code block flowable: grey background, subtle border, monospace text that wraps."""
    content = content.strip()[:4000]
    if not content:
        return None
    # Unescape so PDF shows & " < > not &amp; &quot; &gt; &lt;
    content = _unescape_entities(content)
    # Escape for ReportLab Paragraph (XML), then newlines -> <br/> so Paragraph wraps long lines
    content_escaped = (
        content.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    content_with_breaks = content_escaped.replace("\n", "<br/>")
    code_para = Paragraph(
        f'<font face="Courier" size="8">{content_with_breaks}</font>',
        styles["Code"],
    )
    t = Table([[code_para]], colWidths=[None])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BLOCK_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, CODE_BLOCK_BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def build_styles():
    """Build paragraph styles with Lullabot brand (lullabot.com)."""
    styles = getSampleStyleSheet()
    # Lullabot: clean sans, dark text, red accent for headings
    styles["Normal"].fontName = "Helvetica"
    styles["Normal"].fontSize = 10
    styles["Normal"].textColor = LULLABOT_GRAY
    styles["Normal"].spaceBefore = 6
    styles["Normal"].spaceAfter = 6
    styles["Heading1"].fontName = "Helvetica-Bold"
    styles["Heading1"].fontSize = 18
    styles["Heading1"].textColor = LULLABOT_RED
    styles["Heading1"].spaceBefore = 18
    styles["Heading1"].spaceAfter = 12
    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 14
    styles["Heading2"].textColor = LULLABOT_DARK
    styles["Heading2"].spaceBefore = 14
    styles["Heading2"].spaceAfter = 8
    styles["Heading3"].fontName = "Helvetica-Bold"
    styles["Heading3"].fontSize = 12
    styles["Heading3"].textColor = LULLABOT_DARK
    styles["Heading3"].spaceBefore = 10
    styles["Heading3"].spaceAfter = 6
    styles.add(
        ParagraphStyle(
            name="ListItem",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=LULLABOT_GRAY,
            leftIndent=18,
            spaceBefore=2,
            spaceAfter=2,
        )
    )
    try:
        styles["Code"]
    except KeyError:
        styles.add(
            ParagraphStyle(
                name="Code",
                fontName="Courier",
                fontSize=8,
                leading=10,
                leftIndent=0,
                rightIndent=0,
                spaceBefore=6,
                spaceAfter=6,
                textColor=LULLABOT_DARK,
                splitLongWords=1,
                wordWrap="CJK",
            )
        )
    else:
        styles["Code"].textColor = LULLABOT_DARK
    return styles


def lighthouse_summary_to_flowables(summary: dict, title: str, styles: dict) -> list:
    """Turn Lighthouse summary dict into ReportLab flowables."""
    flowables = [
        Paragraph(escape_for_paragraph(title), styles["Heading1"]),
        Spacer(1, 0.2 * inch),
        Paragraph(f'<b>URL:</b> {escape(summary["requestedUrl"])}', styles["Normal"]),
        Paragraph(f'<b>Fetch time:</b> {escape(summary["fetchTime"])}', styles["Normal"]),
        Spacer(1, 0.15 * inch),
        Paragraph("Category scores", styles["Heading2"]),
        Spacer(1, 0.08 * inch),
    ]
    cat_data = [
        [
            Paragraph('<font color="white">Category</font>', styles["Normal"]),
            Paragraph('<font color="white">Score</font>', styles["Normal"]),
        ]
    ]
    for c in summary["categoryScores"]:
        cat_data.append([_unescape_entities(c["title"]), f'{c["score"]}/100'])
    t1 = Table(cat_data, repeatRows=1)
    t1.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LULLABOT_TABLE_HEADER),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, LULLABOT_BORDER),
            ]
        )
    )
    flowables.append(t1)
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(Paragraph("Key metrics & audits", styles["Heading2"]))
    flowables.append(Spacer(1, 0.08 * inch))
    audit_data = [
        [
            Paragraph('<font color="white">Audit</font>', styles["Normal"]),
            Paragraph('<font color="white">Result</font>', styles["Normal"]),
            Paragraph('<font color="white">Value</font>', styles["Normal"]),
        ]
    ]
    for a in summary["keyAudits"]:
        audit_data.append([
            _unescape_entities(a["title"][:60]),
            a["status"],
            _unescape_entities((a["displayValue"] or "-")[:40]),
        ])
    t2 = Table(audit_data, repeatRows=1)
    t2.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LULLABOT_TABLE_HEADER),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, LULLABOT_BORDER),
            ]
        )
    )
    flowables.append(t2)
    return flowables


def make_lullabot_header(styles: dict) -> list:
    """Lullabot brand header for first page (lullabot.com style)."""
    # Red accent line (thin bar)
    line = Table([[" "]], colWidths=[6 * inch], rowHeights=[4])
    line.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LULLABOT_RED)]))
    return [
        Paragraph(
            '<font color="#E31837" size="24" face="Helvetica-Bold">Lullabot</font>',
            styles["Normal"],
        ),
        Spacer(1, 0.08 * inch),
        Paragraph(
            '<font color="#444444" size="10">A Strategy, Design, and Development Agency</font>',
            styles["Normal"],
        ),
        Spacer(1, 0.12 * inch),
        line,
        Spacer(1, 0.25 * inch),
    ]


def parse_args(argv: list = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Combine SEO audit (Markdown) and Lighthouse (JSON) reports into a PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
      Use default file paths in the script directory.

  %(prog)s --audit my-audit.md --desktop desktop.json --mobile mobile.json -o report.pdf
      Specify all input and output files.

  %(prog)s --include-action-plan
      Include the Action Plan section in the PDF output.
""",
    )
    parser.add_argument(
        "--audit", "-a",
        type=Path,
        default=DEFAULT_SEO_AUDIT,
        help=f"Path to SEO audit Markdown file (default: {DEFAULT_SEO_AUDIT.name})",
    )
    parser.add_argument(
        "--desktop", "-d",
        type=Path,
        default=DEFAULT_LIGHTHOUSE_DESKTOP,
        help=f"Path to Lighthouse desktop JSON (default: {DEFAULT_LIGHTHOUSE_DESKTOP.name})",
    )
    parser.add_argument(
        "--mobile", "-m",
        type=Path,
        default=DEFAULT_LIGHTHOUSE_MOBILE,
        help=f"Path to Lighthouse mobile JSON (default: {DEFAULT_LIGHTHOUSE_MOBILE.name})",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_PDF,
        help=f"Output PDF path (default: {DEFAULT_OUTPUT_PDF.name})",
    )
    parser.add_argument(
        "--include-action-plan",
        action="store_true",
        default=False,
        help="Include the Action Plan section in the PDF (excluded by default)",
    )
    return parser.parse_args(argv)


def main(argv: list = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Validate input files exist
    for path, desc in [
        (args.audit, "SEO audit"),
        (args.desktop, "Lighthouse desktop"),
        (args.mobile, "Lighthouse mobile"),
    ]:
        if not path.exists():
            print(f"Error: {desc} file not found: {path}", file=sys.stderr)
            return 1

    styles = build_styles()
    story = []

    # Lullabot brand header
    story.extend(make_lullabot_header(styles))

    print(f"Loading SEO audit: {args.audit}")
    try:
        skip_action_plan = not args.include_action_plan
        seo_flowables = md_to_flowables(args.audit, styles, skip_action_plan=skip_action_plan)
        story.extend(seo_flowables)
    except Exception as e:
        # Fallback: add raw text
        with open(args.audit, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    story.append(Paragraph(escape_for_paragraph(line), styles["Normal"]))
                    story.append(Spacer(1, 0.04 * inch))
        print(f"Markdown parsing warning: {e}")

    story.append(PageBreak())

    print(f"Loading Lighthouse Desktop: {args.desktop}")
    lh_desktop = load_lighthouse_json(args.desktop)
    desktop_summary = extract_lighthouse_summary(lh_desktop)
    story.extend(lighthouse_summary_to_flowables(desktop_summary, "Lighthouse Report – Desktop", styles))

    story.append(PageBreak())

    print(f"Loading Lighthouse Mobile: {args.mobile}")
    lh_mobile = load_lighthouse_json(args.mobile)
    mobile_summary = extract_lighthouse_summary(lh_mobile)
    story.extend(lighthouse_summary_to_flowables(mobile_summary, "Lighthouse Report – Mobile", styles))

    def add_footer(canvas, doc):
        """Lullabot brand footer on each page."""
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(LULLABOT_GRAY)
        canvas.drawString(inch, 0.5 * inch, "Lullabot — A Strategy, Design, and Development Agency")
        canvas.setStrokeColor(LULLABOT_RED)
        canvas.setLineWidth(1)
        canvas.line(inch, 0.4 * inch, 7.5 * inch, 0.4 * inch)
        canvas.restoreState()

    print(f"Writing PDF to {args.output}...")
    doc = SimpleDocTemplate(
        str(args.output),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=0.75 * inch,
    )
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Done. PDF saved: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
