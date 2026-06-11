#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SKIP_DIRS = new Set(['.git', '.github', 'scripts']);
const VALID_DISCIPLINES = new Set([
  'development',
  'content-strategy',
  'design',
  'project-management',
  'quality-assurance',
  'sales-marketing',
]);

function readFile(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function parseFrontmatter(filePath) {
  const raw = readFile(filePath);
  if (!raw.startsWith('---\n')) {
    throw new Error(`${path.relative(ROOT, filePath)} must start with YAML frontmatter`);
  }

  const end = raw.indexOf('\n---', 4);
  if (end === -1) {
    throw new Error(`${path.relative(ROOT, filePath)} has no closing frontmatter delimiter`);
  }

  return parseSimpleYaml(raw.slice(4, end), filePath);
}

function parseSimpleYaml(raw, filePath) {
  const data = {};
  for (const line of raw.split('\n')) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    if (/^\s/.test(line)) continue;

    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;

    let value = match[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    data[match[1]] = value;
  }

  if (Object.keys(data).length === 0) {
    throw new Error(`${path.relative(ROOT, filePath)} has no parseable top-level metadata`);
  }

  return data;
}

function fail(errors) {
  console.error('Skill validation failed:');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

function listSkillDirs() {
  return fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !SKIP_DIRS.has(entry.name))
    .map((entry) => entry.name)
    .sort();
}

function validateAll() {
  const errors = [];
  const skillDirs = listSkillDirs();

  for (const skillName of skillDirs) {
    const skillDir = path.join(ROOT, skillName);
    const skillMdPath = path.join(skillDir, 'SKILL.md');
    const metaPath = path.join(skillDir, 'meta.yml');

    if (!fs.existsSync(skillMdPath)) {
      errors.push(`${skillName}/ is missing SKILL.md`);
      continue;
    }
    if (!fs.existsSync(metaPath)) {
      errors.push(`${skillName}/ is missing meta.yml`);
      continue;
    }

    try {
      const frontmatter = parseFrontmatter(skillMdPath);
      if (!frontmatter.name) {
        errors.push(`${skillName}/SKILL.md is missing frontmatter name`);
      } else if (frontmatter.name !== skillName) {
        errors.push(`${skillName}/SKILL.md name "${frontmatter.name}" must match directory name "${skillName}"`);
      }
      if (!frontmatter.description) {
        errors.push(`${skillName}/SKILL.md is missing frontmatter description`);
      }
    } catch (error) {
      errors.push(error.message);
    }

    try {
      const meta = parseSimpleYaml(readFile(metaPath), metaPath);
      if (!meta.title) errors.push(`${skillName}/meta.yml is missing title`);
      if (!meta.date) errors.push(`${skillName}/meta.yml is missing date`);
      if (!meta.discipline) {
        errors.push(`${skillName}/meta.yml is missing discipline`);
      } else if (!VALID_DISCIPLINES.has(meta.discipline)) {
        errors.push(`${skillName}/meta.yml discipline "${meta.discipline}" is invalid`);
      }
    } catch (error) {
      errors.push(error.message);
    }
  }

  return { errors, count: skillDirs.length };
}

module.exports = {
  ROOT,
  SKIP_DIRS,
  VALID_DISCIPLINES,
  readFile,
  parseFrontmatter,
  parseSimpleYaml,
  listSkillDirs,
  validateAll,
};

if (require.main === module) {
  const { errors, count } = validateAll();
  if (errors.length > 0) fail(errors);
  console.log(`Validated ${count} skill(s).`);
}
