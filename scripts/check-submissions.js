#!/usr/bin/env node
// Blocking checks only establish disclosures and finite portability rules.
// Semantic completeness, safety, and human approval remain review responsibilities.
const fs = require('node:fs');
const path = require('node:path');
const { ROOT, listSkillDirs, splitFrontmatter } = require('./validate-skills.js');

// Preserve line positions while removing fenced examples and HTML comments.
function markdownLines(text) {
  let fence = null;
  return text.replace(/<!--[\s\S]*?-->/g, (comment) => comment.replace(/[^\n]/g, ' ')).split(/\r?\n/).map((line) => {
    if (fence) {
      if (new RegExp(`^ {0,3}${fence.char}{${fence.length},}[ \\t]*$`).test(line)) fence = null;
      return '';
    }
    const opening = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
    if (opening && !(opening[1][0] === '`' && opening[2].includes('`'))) {
      fence = { char: opening[1][0], length: opening[1].length };
      return '';
    }
    return line;
  });
}

function extractSection(body, title) {
  const lines = markdownLines(body);
  let start = -1;
  let end = lines.length;
  for (let index = 0; index < lines.length; index++) {
    const heading = lines[index].match(/^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$/);
    if (!heading) continue;
    if (start < 0 && heading[1].length === 2 && heading[2].trim().toLowerCase() === title.toLowerCase()) start = index;
    else if (start >= 0 && heading[1].length <= 2) { end = index; break; }
  }
  if (start < 0) return null;
  return { line: start + 1, text: lines.slice(start + 1, end).filter((line) => !/^ {0,3}#{1,6}[ \t]/.test(line)).join('\n') };
}

function substantive(text) {
  const content = text.replace(/<[^>]*>/g, '').replace(/^[ \t>*+-]+/gm, '').replace(/[`*_\[\]().:!?-]/g, '');
  return content.split(/\r?\n/).some((line) => /[\p{L}\p{N}]/u.test(line) &&
    !/^(?:todo|tbd|n\/?a|none|placeholder|coming soon|add (?:requirements|safety)(?: here)?)$/i.test(line.trim()));
}

// Only these known runtime dependencies block. Product names and installation
// directories alone are not violations; broader portability needs human review.
const PORTABILITY_RULES = [
  { id: 'claude-skill-dir', pattern: /\$\{?CLAUDE_SKILL_DIR\}?|\bCLAUDE_SKILL_DIR\b/g, message: 'Resolve companion files from the loaded skill location instead of CLAUDE_SKILL_DIR.' },
  { id: 'agent-arguments', pattern: /\$(?:\{ARGUMENTS\b[^}\r\n]*\}|ARGUMENTS\b)/g, message: 'Read supplied arguments from the user request instead of an agent-provided ARGUMENTS variable.' },
  { id: 'claude-install-path', pattern: /\.claude\/skills\/[^\s"'`<>]*\.(?:[cm]?js|ts|py|php|sh|bash)(?=[\s"'`<>),;:]|$)/g, message: 'Use a resolved skill path for companion execution rather than a hardcoded Claude installation path.' },
  { id: 'claude-builtin', pattern: /(?<![\w./-])\/security-review(?![\w-]|\.[\w])/g, message: 'Replace the Claude-only security-review operation with agent-neutral review instructions, or document the exact optional/quoted occurrence.' },
];
const TEXT_EXTENSIONS = new Set(['.md', '.txt', '.yml', '.yaml', '.json', '.js', '.cjs', '.mjs', '.ts', '.py', '.php', '.sh', '.bash', '.html', '.css']);

function listTextFiles(directory, prefix = '') {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory() && !['node_modules', '.git'].includes(entry.name)) files.push(...listTextFiles(path.join(directory, entry.name), relative));
    else if (entry.isFile() && TEXT_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) files.push(relative);
  }
  return files.sort();
}

// An exemption comment describes one exact matched token on the following line.
// HTML comments work in Markdown; # and // comments work in companion sources.
function checkPortability(text, file) {
  const errors = [];
  const lines = text.split(/\r?\n/);
  const exemptions = new Map();
  const annotationLines = new Set();
  for (let index = 0; index < lines.length; index++) {
    if (!lines[index].includes('portability-exemption:')) continue;
    annotationLines.add(index);
    const match = lines[index].match(/^\s*(?:<!--|#|\/\/)\s*portability-exemption:\s*(\{.*\})(?:\s*-->)?\s*$/);
    let exemption;
    try { exemption = match && JSON.parse(match[1]); } catch { /* reported below */ }
    if (!exemption || Object.keys(exemption).sort().join(',') !== 'reason,rule,text' ||
        !PORTABILITY_RULES.some((rule) => rule.id === exemption.rule) ||
        typeof exemption.text !== 'string' || !exemption.text || /[\r\n]/.test(exemption.text) ||
        typeof exemption.reason !== 'string' || !substantive(exemption.reason)) {
      errors.push({ file, line: index + 1, rule: 'portability-exemption', message: 'Exemption must specify a known rule, one exact occurrence as text, and a substantive reason in a comment before that occurrence.' });
      continue;
    }
    exemptions.set(index + 1, { ...exemption, annotationLine: index + 1, used: false });
  }
  for (let index = 0; index < lines.length; index++) {
    if (annotationLines.has(index)) continue;
    for (const rule of PORTABILITY_RULES) {
      const matches = [...lines[index].matchAll(new RegExp(rule.pattern.source, rule.pattern.flags))];
      for (const match of matches) {
        const exemption = exemptions.get(index);
        if (exemption && exemption.rule === rule.id && exemption.text === match[0] &&
            matches.filter((occurrence) => occurrence[0] === exemption.text).length === 1) {
          exemption.used = true;
          continue;
        }
        errors.push({ file, line: index + 1, rule: rule.id, message: rule.message });
      }
    }
  }
  for (const exemption of exemptions.values()) {
    if (!exemption.used) errors.push({ file, line: exemption.annotationLine, rule: 'portability-exemption', message: 'Unused or ambiguous exemption: the exact text must identify one violation on the immediately following line.' });
  }
  return errors;
}

function checkSkill(skillName, root = ROOT) {
  const errors = [];
  const file = `${skillName}/SKILL.md`;
  const absolute = path.join(root, file);
  if (!fs.existsSync(absolute)) return { name: skillName, errors: [{ file, line: 1, rule: 'skill-file', message: 'Missing SKILL.md' }] };
  const { body, bodyLine } = splitFrontmatter(fs.readFileSync(absolute, 'utf8'));
  for (const [title, rule] of [['Requirements', 'requirements-section'], ['Safety and review', 'safety-section']]) {
    const section = extractSection(body, title);
    if (!section || !substantive(section.text)) errors.push({ file, line: section ? bodyLine + section.line - 1 : 1, rule, message: `Add a substantive second-level ${title} section outside code fences; comments and placeholders do not count.` });
  }
  for (const relative of listTextFiles(path.join(root, skillName))) {
    const companion = `${skillName}/${relative}`;
    errors.push(...checkPortability(fs.readFileSync(path.join(root, companion), 'utf8'), companion));
  }
  return { name: skillName, errors };
}

function checkAll(root = ROOT) {
  const skills = listSkillDirs(root);
  return { errors: skills.flatMap((name) => checkSkill(name, root).errors), count: skills.length };
}

module.exports = { PORTABILITY_RULES, TEXT_EXTENSIONS, listTextFiles, markdownLines, extractSection, substantive, checkPortability, checkSkill, checkAll };

if (require.main === module) {
  const { errors, count } = checkAll();
  if (errors.length) {
    for (const error of errors) console.error(`${error.file}:${error.line} [${error.rule}] ${error.message}`);
    process.exitCode = 1;
  } else console.log(`Checked Requirements, Safety and review, and portability for ${count} skill(s).`);
}
