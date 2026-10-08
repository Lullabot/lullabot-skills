const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const repository = path.resolve(__dirname, '../..');

test('spelling scope rejects a typo, accepts reviewed terminology, and excludes installed tooling', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-spelling-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  for (const file of ['cspell.json', 'cspell-words.txt']) fs.copyFileSync(path.join(repository, file), path.join(root, file));
  for (const directory of ['example', '.agents/tool', 'node_modules/dependency']) fs.mkdirSync(path.join(root, directory), { recursive: true });
  fs.writeFileSync(path.join(root, 'example/SKILL.md'), 'This is definitley a typo.\n');
  fs.writeFileSync(path.join(root, '.agents/tool/SKILL.md'), 'Tooling missspelling.\n');
  fs.writeFileSync(path.join(root, 'node_modules/dependency/README.md'), 'Dependency missspelling.\n');
  const run = () => spawnSync(process.execPath, [path.join(repository, 'node_modules/cspell/bin.mjs'), '--config', 'cspell.json', '--no-progress'], { cwd: root, encoding: 'utf8' });
  const rejected = run();
  assert.equal(rejected.status, 1, rejected.stdout + rejected.stderr);
  assert.match(rejected.stdout + rejected.stderr, /definitley/);
  assert.doesNotMatch(rejected.stdout + rejected.stderr, /missspelling/);
  fs.writeFileSync(path.join(root, 'example/SKILL.md'), 'DDEV, Cloudflare, CSpell, and Lullabot are reviewed names.\n');
  const accepted = run();
  assert.equal(accepted.status, 0, accepted.stdout + accepted.stderr);
});
