const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { reviewSkill } = require('../review-skill.js');
function fixture(t, description, body) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-advisory-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'example', 'references'), { recursive: true });
  fs.writeFileSync(path.join(root, 'example', 'SKILL.md'), `---\nname: example\ndescription: ${description}\n---\n` + body);
  fs.writeFileSync(path.join(root, 'example', 'references', 'exists.md'), 'Reference documentation.\n');
  return root;
}

test('XML tags and missing local references remain mechanical advisory findings', (t) => {
  const root = fixture(t, '"Use when <trigger>validating</trigger> skills and metadata."', '[Valid](references/exists.md)\n[Missing](references/missing.md)\n[External](https://example.org/missing.md)\n');
  const result = reviewSkill('example', root);
  assert.ok(result.findings.some((f) => /XML/.test(f.msg)));
  assert.ok(result.findings.some((f) => /references\/missing.md/.test(f.msg)));
  assert.ok(!result.findings.some((f) => /references\/exists.md.*missing|https.*missing/.test(f.msg)));
});

test('invalid scalar types do not crash the advisory reviewer', (t) => {
  const root = fixture(t, '[not, scalar]', '# Example\n');
  assert.doesNotThrow(() => reviewSkill('example', root));
});
