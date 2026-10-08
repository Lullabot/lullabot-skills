const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { checkAll, checkSkill, checkPortability } = require('../check-submissions.js');

const sections = '## Requirements\nNo external tools are required.\n\n## Safety and review\nA human reviews the generated text before sharing. Public input stays in the chosen tool.\n';
function fixture(t, body = sections) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-submission-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'example'));
  fs.writeFileSync(path.join(root, 'example', 'SKILL.md'), '---\nname: example\ndescription: Use when testing a fixture.\n---\n' + body);
  return root;
}

test('disclosures require actual substantive second-level sections outside code fences', (t) => {
  for (const body of [
    '```md\n' + sections + '```\n',
    '~~~~md\n' + sections + '~~~~\n',
    '## Requirements\n<!-- No tools needed. -->\n## Safety and review\nTODO\n',
    '## Requirements\n### Details\n## Safety and review\n<!-- comment -->\n',
    '    ## Requirements\n    fake code heading\n    ## Safety and review\n    fake code heading\n',
    '## Requirements\nTBD\n## Another section\nUseful words here.\n## Safety and review\nPlaceholder.\n',
  ]) {
    const result = checkSkill('example', fixture(t, body));
    assert.ok(result.errors.some((e) => e.rule === 'requirements-section'), body);
    assert.ok(result.errors.some((e) => e.rule === 'safety-section'), body);
  }
  assert.deepEqual(checkAll(fixture(t)).errors, []);
});

test('known runtime dependencies fail with rule and exact file location, including companions', (t) => {
  const root = fixture(t, sections + '\npython ${CLAUDE_SKILL_DIR}/scripts/tool.py\nRead $ARGUMENTS.\nnode .claude/skills/example/tool.js\nUse the built-in /security-review.\n');
  fs.mkdirSync(path.join(root, 'example', 'scripts'));
  fs.writeFileSync(path.join(root, 'example', 'scripts', 'helper.py'), 'location = "${CLAUDE_SKILL_DIR}/scripts/tool.py"\n');
  const errors = checkAll(root).errors;
  assert.equal(errors.filter((e) => e.rule === 'claude-skill-dir').length, 2);
  assert.ok(errors.some((e) => e.rule === 'agent-arguments'));
  assert.ok(errors.some((e) => e.rule === 'claude-install-path'));
  assert.ok(errors.some((e) => e.rule === 'claude-builtin'));
  assert.ok(errors.every((e) => e.line > 0 && e.file.startsWith('example/')));
});

test('installation and vendor discussion do not constrain execution', (t) => {
  const root = fixture(t, sections + '\nInstall for Claude Code:\n```sh\ngit clone https://example.org/skills.git .claude/skills\n```\nAgents can read references/security-review.md. Use /custom-command with your declared CLI.\n');
  assert.deepEqual(checkAll(root).errors, []);
});

test('quoted references need a rationale exemption scoped to one exact occurrence', () => {
  const exemption = '<!-- portability-exemption: {"rule":"claude-skill-dir","text":"$CLAUDE_SKILL_DIR","reason":"Quoted upstream syntax for comparison; instructions use a resolved skill path."} -->';
  assert.deepEqual(checkPortability(exemption + '\n> Upstream calls it `$CLAUDE_SKILL_DIR`.\n', 'example/reference.md'), []);
  const errors = checkPortability(exemption + '\n> Upstream calls it `$CLAUDE_SKILL_DIR`.\npython $CLAUDE_SKILL_DIR/helper.py\n', 'example/reference.md');
  assert.equal(errors.length, 1);
  assert.equal(errors[0].line, 3);
  assert.equal(errors[0].rule, 'claude-skill-dir');
  assert.ok(checkPortability(exemption + '\n> $CLAUDE_SKILL_DIR and $CLAUDE_SKILL_DIR\n', 'example/reference.md').some((e) => e.rule === 'portability-exemption'));
  assert.ok(checkPortability(exemption.replace('Quoted upstream syntax for comparison; instructions use a resolved skill path.', '') + '\n$CLAUDE_SKILL_DIR\n', 'example/reference.md').some((e) => e.rule === 'portability-exemption'));
  assert.ok(checkPortability(exemption + '\nNo occurrence here.\n$CLAUDE_SKILL_DIR\n', 'example/reference.md').some((e) => e.rule === 'portability-exemption'));
});

test('required disclosures do not turn semantic safety guesses into blocking errors', (t) => {
  const root = fixture(t, sections + '\nHuman-approved deletion is limited to the sandbox fixture. Tool eligibility needs human review.\n');
  assert.deepEqual(checkAll(root).errors, []);
});

test('multiple placeholder lines and HTML formatting alone do not become substantive disclosures', (t) => {
  const result = checkAll(fixture(t, '## Requirements\n- TODO\n- TBD\n\n## Safety and review\n<br>\n[Placeholder]\n'));
  assert.equal(result.errors.filter((error) => error.rule.endsWith('-section')).length, 2);
});

test('braced ARGUMENTS defaults and array access remain known runtime coupling', () => {
  const errors = checkPortability('input="${ARGUMENTS:-default}"\nfirst="${ARGUMENTS[0]}"\n', 'example/helper.sh');
  assert.equal(errors.length, 2);
  assert.ok(errors.every((error) => error.rule === 'agent-arguments'));
  const exemption = '# portability-exemption: {"rule":"agent-arguments","text":"${ARGUMENTS:-default}","reason":"A quoted upstream example, not the active command."}';
  assert.deepEqual(checkPortability(exemption + '\nexample="${ARGUMENTS:-default}"\n', 'example/helper.sh'), []);
});
