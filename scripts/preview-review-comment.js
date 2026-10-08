#!/usr/bin/env node
// Temporary PR 45 exercise: read-only GitHub access and no model credentials.
// Writes intercepted reporter output to a file; it never posts to GitHub.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { createGitHubAPI, runReport, MARKER } = require('./pr-review-report.js');

async function main() {
  delete process.env.ANTHROPIC_API_KEY;
  const event = JSON.parse(fs.readFileSync(process.env.GITHUB_EVENT_PATH, 'utf8'));
  const repository = process.env.GITHUB_REPOSITORY;
  assert.equal(repository, 'Lullabot/lullabot-skills');
  assert.equal(event.pull_request.number, 45);
  assert.equal(event.pull_request.head.repo.full_name, repository);
  const head = event.pull_request.head.sha;
  let run;
  // Wait for the independent validation workflow at this exact head.
  for (let attempt = 0; attempt < 60; attempt++) {
    const api = createGitHubAPI();
    const data = await api.request('GET', '/repos/' + repository + '/actions/workflows/skill-validation.yml/runs?event=pull_request&head_sha=' + head + '&per_page=30');
    const runs = data.workflow_runs.filter(item => item.head_sha === head).sort((a, b) => b.id - a.id);
    if (runs[0]?.status === 'completed') { run = runs[0]; break; }
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
  assert(run, 'Validation at the preview head did not complete in time.');
  const readOnly = createGitHubAPI();
  let captured;
  const api = { request: async (method, endpoint, body) => {
    if (method === 'GET') return readOnly.request(method, endpoint);
    assert(['POST', 'PATCH'].includes(method));
    assert(endpoint.startsWith('/repos/' + repository + '/issues/'));
    assert(body.body.startsWith(MARKER));
    assert(Buffer.byteLength(body.body) < 55000);
    captured = body.body;
    return { id: 1 };
  } };
  const result = await runReport({
    api, repository, forkApprovalVerified: false,
    event: { action: 'completed', repository: event.repository, workflow_run: run },
  });
  assert(captured, 'Preview failed: ' + JSON.stringify(result));
  assert(['posted', 'updated'].includes(result.status));
  fs.writeFileSync('preview-comment.md', captured);
  console.log('Rendered exact-head reporter output with intercepted writes; model credentials omitted.');
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
