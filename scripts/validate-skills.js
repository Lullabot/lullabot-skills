#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');
const YAML = require('yaml');

const ROOT = path.resolve(__dirname, '..');
// Keep discovery shared by structural, submission, and advisory checks.
const SKIP_DIRS = new Set(['.git', '.github', '.agents', '.ai', '.claude', '.codex', 'scripts', 'node_modules']);
const VALID_DISCIPLINES = new Set([
  'development', 'content-strategy', 'design', 'project-management',
  'quality-assurance', 'sales-marketing',
]);

function readFile(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function splitFrontmatter(raw) {
  const match = raw.match(/^---[ \t]*\r?\n([\s\S]*?)^---[ \t]*(?:\r?\n|$)/m);
  if (!match || match.index !== 0) return { yaml: null, body: raw, bodyLine: 1 };
  return { yaml: match[1], body: raw.slice(match[0].length), bodyLine: match[0].split('\n').length };
}

function parseYamlDocument(raw, filePath) {
  const doc = YAML.parseDocument(raw, { uniqueKeys: true, keepSourceTokens: true });
  if (doc.errors.length) throw new Error(`${filePath}: invalid YAML: ${doc.errors[0].message}`);
  // The public site's js-yaml loader rejects unknown tags; yaml reports them as warnings.
  if (doc.warnings.some((warning) => warning.code === 'TAG_RESOLVE_FAILED')) throw new Error(`${filePath}: unsupported YAML tag`);
  if (!YAML.isMap(doc.contents)) throw new Error(`${filePath}: metadata must be a YAML mapping`);
  return doc;
}

// Retain the export name used by the advisory checker; parsing is now real YAML.
function parseSimpleYaml(raw, filePath = 'metadata') {
  return parseYamlDocument(raw, filePath).toJS({ maxAliasCount: 50 });
}

function parseFrontmatter(filePath) {
  const { yaml } = splitFrontmatter(readFile(filePath));
  if (yaml === null) throw new Error(`${filePath}: must start with closed YAML frontmatter`);
  const doc = parseYamlDocument(yaml, filePath);
  const data = doc.toJS({ maxAliasCount: 50 });
  for (const field of ['name', 'description']) {
    const pair = doc.contents.items.find((item) => item.key.value === field);
    const value = pair?.value;
    const source = pair && value?.range ? yaml.slice(pair.key.range[0], value.range[1]) : '';
    if (!YAML.isScalar(value) || typeof data[field] !== 'string' || !data[field].trim() ||
        /[\r\n]/.test(data[field]) || /[\r\n]/.test(source) || value.anchor ||
        value.type === 'BLOCK_FOLDED' || value.type === 'BLOCK_LITERAL' ||
        !new RegExp(`^${field}:[ \\t]+\\S`).test(source)) {
      throw new Error(`${filePath}: ${field} must be a nonempty string scalar on one source line`);
    }
  }
  return data;
}

function listSkillDirs(root = ROOT) {
  return fs.readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !SKIP_DIRS.has(entry.name))
    .map((entry) => entry.name).sort();
}

function nonemptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function validDate(value) {
  return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) &&
    !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value;
}

function validateMetadata(meta, file, errors) {
  if (!nonemptyString(meta.title)) errors.push(`${file}: title must be a nonempty string`);
  if (!validDate(meta.date)) errors.push(`${file}: date must be a valid YYYY-MM-DD string`);
  if (!VALID_DISCIPLINES.has(meta.discipline)) errors.push(`${file}: discipline must be one allowed scalar (${[...VALID_DISCIPLINES].join(', ')})`);
  if ('tags' in meta && (!Array.isArray(meta.tags) || !meta.tags.every(nonemptyString))) errors.push(`${file}: tags must be a list of nonempty strings`);
  if ('version' in meta && !nonemptyString(meta.version)) errors.push(`${file}: version must be a nonempty string`);
  if ('lastUpdated' in meta && !validDate(meta.lastUpdated)) errors.push(`${file}: lastUpdated must be a valid YYYY-MM-DD string`);
  if ('changelog' in meta && (!Array.isArray(meta.changelog) || !meta.changelog.every((entry) =>
    entry && typeof entry === 'object' && !Array.isArray(entry) && nonemptyString(entry.version) && validDate(entry.date) && nonemptyString(entry.summary)))) {
    errors.push(`${file}: changelog must be a list of entries with string version, valid date, and nonempty summary`);
  }
}

function validateAll(root = ROOT) {
  const errors = [];
  const skillDirs = listSkillDirs(root);
  for (const skillName of skillDirs) {
    const skillFile = path.join(root, skillName, 'SKILL.md');
    const metaFile = path.join(root, skillName, 'meta.yml');
    for (const file of [skillFile, metaFile]) {
      if (!fs.existsSync(file)) errors.push(`${path.relative(root, file)} is missing ${path.basename(file)}`);
    }
    if (fs.existsSync(skillFile)) {
      try {
        const frontmatter = parseFrontmatter(skillFile);
        if (frontmatter.name !== skillName) errors.push(`${skillName}/SKILL.md: name "${frontmatter.name}" must match directory name "${skillName}"`);
      } catch (error) {
        errors.push(error.message.replaceAll(root + path.sep, ''));
      }
    }
    if (fs.existsSync(metaFile)) {
      try {
        validateMetadata(parseSimpleYaml(readFile(metaFile), `${skillName}/meta.yml`), `${skillName}/meta.yml`, errors);
      } catch (error) {
        errors.push(error.message);
      }
    }
  }
  return { errors, count: skillDirs.length };
}

module.exports = { ROOT, SKIP_DIRS, VALID_DISCIPLINES, readFile, splitFrontmatter, parseFrontmatter, parseSimpleYaml, listSkillDirs, validateAll };

if (require.main === module) {
  const { errors, count } = validateAll();
  if (errors.length) {
    console.error('Skill validation failed:');
    for (const error of errors) console.error(`- ${error}`);
    process.exitCode = 1;
  } else {
    console.log(`Validated ${count} skill(s).`);
  }
}
