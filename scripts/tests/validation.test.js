const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { validateAll, listSkillDirs, parseFrontmatter } = require('../validate-skills.js');

function fixture(t, { skill = '---\nname: example\ndescription: Use when validating a fixture.\n---\n# Example\n', meta = 'title: Example\ndiscipline: development\ndate: 2026-10-08\n' } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-validation-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'example'));
  fs.writeFileSync(path.join(root, 'example', 'SKILL.md'), skill);
  fs.writeFileSync(path.join(root, 'example', 'meta.yml'), meta);
  return root;
}

test('discovery ignores dependency and tool directories but reports incomplete submissions', (t) => {
  const root = fixture(t);
  for (const name of ['node_modules', '.ai', '.agents', '.claude', '.codex', '.github', 'scripts', 'unfinished']) fs.mkdirSync(path.join(root, name));
  assert.deepEqual(listSkillDirs(root), ['example', 'unfinished']);
  const result = validateAll(root);
  assert.equal(result.count, 2);
  assert.match(result.errors.join('\n'), /unfinished\/.*missing SKILL.md/);
});

test('real YAML rejects malformed syntax and typed placeholders', (t) => {
  for (const meta of [
    'title: [broken\ndiscipline: development\ndate: 2026-10-08\n',
    'title: true\ndiscipline: development\ndate: 2026-10-08\n',
    'title: Example\ndiscipline: [development]\ndate: 2026-10-08\n',
    'title: Example\ndiscipline: development\ndate: 2026-02-30\n',
    'title: Example\ndiscipline: development\ndate: 2026-10-08\ntags: some, tags\n',
    'title: Example\ndiscipline: development\ndate: 2026-10-08\nchangelog: [false]\n',
    'title: Example\ntitle: Duplicate\ndiscipline: development\ndate: 2026-10-08\n',
  ]) {
    assert.ok(validateAll(fixture(t, { meta })).errors.length > 0, meta);
  }
});

test('valid metadata lists and quoted scalar frontmatter pass', (t) => {
  const root = fixture(t, { meta: 'title: "Example: YAML"\ndiscipline: development\ndate: 2026-10-08\ntags: [nodejs, "skill authoring"]\nchangelog:\n  - version: 1.0.0\n    date: 2026-10-08\n    summary: Initial release\n' });
  assert.deepEqual(validateAll(root).errors, []);
});

test('name and description require strings represented on single source lines', (t) => {
  for (const description of ['true', '[use, when]', '>\n  Use when testing.', '|\n  Use when testing.', '"Use when\n  testing."', "'Use when\n  testing.'", 'Use when testing\n  continuation', '"Use when testing.\\nSecond line."', '&text Use when testing.']) {
    const root = fixture(t, { skill: `---\nname: example\ndescription: ${description}\n---\n# Example\n` });
    assert.ok(validateAll(root).errors.some((e) => /description/.test(e)), description);
  }
  const root = fixture(t, { skill: '---\nname: example\ndescription: "Use when testing." # valid comment\n---\n' });
  assert.equal(parseFrontmatter(path.join(root, 'example', 'SKILL.md')).description, 'Use when testing.');
});

test('unsupported YAML tags fail in frontmatter and metadata before site rendering', (t) => {
  for (const field of ['name', 'description']) {
    const skill = `---\nname: ${field === 'name' ? '!unsupported ' : ''}example\ndescription: ${field === 'description' ? '!unsupported ' : ''}Use when validating a fixture.\n---\n# Example\n`;
    assert.match(validateAll(fixture(t, { skill })).errors.join('\n'), /unsupported YAML tag/);
  }
  for (const meta of [
    'title: !unsupported Example\ndiscipline: development\ndate: 2026-10-08\n',
    'title: Example\ndiscipline: development\ndate: 2026-10-08\ntags: [!unsupported testing]\n',
  ]) {
    assert.match(validateAll(fixture(t, { meta })).errors.join('\n'), /unsupported YAML tag/);
  }
  const root = fixture(t, { skill: '---\nname: !!str example\ndescription: !!str Use when validating a fixture.\n---\n# Example\n', meta: 'title: !!str Example\ndiscipline: development\ndate: 2026-10-08\n' });
  assert.deepEqual(validateAll(root).errors, []);
});
