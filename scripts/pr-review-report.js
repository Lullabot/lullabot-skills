#!/usr/bin/env node
// Run only trusted default-branch code. GitHub blobs are inert review data.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { SKIP_DIRS } = require('./validate-skills.js');
const { TEXT_EXTENSIONS } = require('./check-submissions.js');
const { reviewSkill } = require('./review-skill.js');
const { runReview, renderReview, DEFAULT_MODEL, LIMITS } = require('./llm-review.js');

const SOURCE = Object.freeze({ name: 'Skill validation', path: '.github/workflows/skill-validation.yml' });
const MARKER = '<!-- skill-review-comment -->';
const REPORT_LIMITS = Object.freeze({ requests: 128, timeoutMs: 12_000, overallMs: 180_000, responseBytes: 1_500_000, totalResponseBytes: 10_000_000, pages: 3, changes: 300, treeEntries: 10_000, files: 100, snapshotBytes: 1_500_000, commentBytes: 55_000 });
const sha = (value) => typeof value === 'string' && /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(value);
const id = (value) => Number.isSafeInteger(value) && value > 0;
const repoName = (value) => typeof value === 'string' && /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(value);
const validPath = (value) => typeof value === 'string' && value.length > 0 && value.length <= 240 && !/[\\\x00-\x1f\x7f]/.test(value) && !value.startsWith('/') && value.split('/').every((part) => part && part !== '.' && part !== '..');
const publicPath = (value) => validPath(value) && value.includes('/') && !SKIP_DIRS.has(value.split('/')[0]);
function requireCondition(condition, reason) { if (!condition) throw Object.assign(new Error(reason), { reviewSafe: true }); }

/** Bounded REST transport; never follows submitted URLs or prints response bodies. */
function createGitHubAPI(options = {}) {
  const token = options.token || process.env.GITHUB_TOKEN;
  const transport = options.fetch || globalThis.fetch;
  let requests = 0, bytes = 0;
  const deadline = Date.now() + Math.min(options.overallMs ?? REPORT_LIMITS.overallMs, REPORT_LIMITS.overallMs);
  return { async request(method, endpoint, body) {
    requireCondition(token, 'GitHub credential unavailable.');
    requireCondition(endpoint.startsWith('/repos/') && !/[\r\n]/.test(endpoint), 'Invalid API endpoint.');
    requireCondition(++requests <= Math.min(options.maxRequests ?? REPORT_LIMITS.requests, REPORT_LIMITS.requests), 'GitHub request limit reached.');
    const duration = Math.min(options.timeoutMs ?? REPORT_LIMITS.timeoutMs, REPORT_LIMITS.timeoutMs, deadline - Date.now());
    requireCondition(duration > 0, 'GitHub review deadline reached.');
    const controller = new AbortController();
    let timer;
    try {
      const work = async () => {
        const response = await transport(`https://api.github.com${endpoint}`, {
          method, redirect: 'error', signal: controller.signal,
          headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2026-03-10', 'Content-Type': 'application/json' },
          ...(body === undefined ? {} : { body: JSON.stringify(body) }),
        });
        requireCondition(response.ok, `GitHub request unavailable (HTTP ${response.status}).`);
        const max = Math.min(options.maxResponseBytes ?? REPORT_LIMITS.responseBytes, REPORT_LIMITS.responseBytes);
        requireCondition(Number(response.headers.get('content-length') || 0) <= max, 'GitHub response byte size limit reached.');
        const reader = response.body.getReader();
        const chunks = [];
        let size = 0;
        try {
          while (true) {
            const chunk = await reader.read();
            if (chunk.done) break;
            size += chunk.value.byteLength; bytes += chunk.value.byteLength;
            requireCondition(size <= max && bytes <= REPORT_LIMITS.totalResponseBytes, 'GitHub response byte size limit reached.');
            chunks.push(Buffer.from(chunk.value));
          }
        } finally { reader.releaseLock(); }
        try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch { throw new Error('GitHub JSON response invalid.'); }
      };
      const timeout = new Promise((_, reject) => { timer = setTimeout(() => { controller.abort(); reject(new Error('GitHub request timed out.')); }, duration); });
      return await Promise.race([work(), timeout]);
    } finally { clearTimeout(timer); controller.abort(); }
  } };
}
async function list(api, endpoint, field, expected) {
  const values = [];
  for (let page = 1; page <= REPORT_LIMITS.pages; page++) {
    const data = await api.request('GET', `${endpoint}${endpoint.includes('?') ? '&' : '?'}per_page=100&page=${page}`);
    const items = field ? data[field] : data;
    requireCondition(Array.isArray(items) && items.length <= 100, 'GitHub list response invalid.');
    values.push(...items);
    if (items.length < 100 || (expected !== undefined && values.length >= expected)) return values;
  }
  throw new Error('GitHub pagination limit reached; review coverage unavailable.');
}
function associationMatches(association, pr, run, repository) {
  return association?.number === pr.number && association.id === pr.id && association.head?.sha === run.head_sha &&
    association.head?.repo?.id === run.head_repository.id && association.base?.repo?.id === repository.id && association.base?.sha === pr.base.sha;
}
function validatePR(pr, run, repository) {
  requireCondition(id(pr?.number) && id(pr.id) && pr.state === 'open', 'Pull request is unavailable or closed.');
  requireCondition(pr.base?.repo?.id === repository.id && pr.base.repo.full_name === repository.full_name && sha(pr.base.sha), 'Pull request base repository or commit does not match.');
  requireCondition(pr.head?.repo?.id === run.head_repository.id && pr.head.repo.full_name === run.head_repository.full_name && pr.head.sha === run.head_sha && repoName(pr.head.repo.full_name), 'Pull request head repository or commit does not match.');
  requireCondition(repository.private === false && pr.head.repo.private === false, 'Private repository data is ineligible for this public submission review.');
}

/** Validate fresh API state, not artifact PR numbers or mutable event claims. */
async function resolveContext({ api, event, repository, forkApprovalVerified }) {
  requireCondition(repoName(repository) && event?.action === 'completed' && id(event.workflow_run?.id), 'Invalid workflow_run event.');
  const prefix = `/repos/${repository}`;
  const currentRepo = await api.request('GET', prefix);
  requireCondition(currentRepo.full_name === repository && id(currentRepo.id) && event.repository?.id === currentRepo.id && event.repository.full_name === repository, 'Event repository does not match the trusted repository.');
  const workflow = await api.request('GET', `${prefix}/actions/workflows/${path.basename(SOURCE.path)}`);
  requireCondition(workflow.name === SOURCE.name && workflow.path === SOURCE.path && workflow.state === 'active' && id(workflow.id), 'Canonical validation workflow unavailable.');
  const run = await api.request('GET', `${prefix}/actions/runs/${event.workflow_run.id}`);
  requireCondition(run.id === event.workflow_run.id && id(run.run_attempt) && run.run_attempt === event.workflow_run.run_attempt && run.workflow_id === workflow.id && run.name === SOURCE.name && run.path?.split('@')[0] === SOURCE.path, 'Source workflow identity or attempt does not match.');
  requireCondition(run.event === 'pull_request' && run.status === 'completed' && ['success', 'failure'].includes(run.conclusion), 'Source run was not eligible completed pull request validation.');
  requireCondition(run.repository?.id === currentRepo.id && run.repository.full_name === repository && id(run.head_repository?.id) && repoName(run.head_repository.full_name) && sha(run.head_sha), 'Source run repository or head is invalid.');
  const fork = run.head_repository.id !== currentRepo.id;
  requireCondition(!fork || forkApprovalVerified === true, 'Fork review skipped: administrator approval-policy verification is required.');
  requireCondition(Array.isArray(run.pull_requests), 'Source pull request associations unavailable.');
  let candidate, recovered = false;
  if (run.pull_requests.length) {
    requireCondition(run.pull_requests.length === 1 && id(run.pull_requests[0].number), 'Ambiguous source pull request association.');
    candidate = run.pull_requests[0];
  } else {
    // Real fork workflow_run payloads may have no PR entry. This API is the
    // association authority; caller-supplied artifacts/PR numbers never are.
    const associated = await list(api, `${prefix}/commits/${run.head_sha}/pulls`);
    const matching = associated.filter((pr) => pr.state === 'open' && pr.head?.sha === run.head_sha && pr.head?.repo?.id === run.head_repository.id && pr.base?.repo?.id === currentRepo.id);
    requireCondition(matching.length === 1, 'Exact-head commit-associated pull request unavailable or ambiguous.');
    candidate = matching[0]; recovered = true;
  }
  requireCondition(id(candidate.number) && id(candidate.id), 'Commit-associated pull request identity invalid.');
  const pr = await api.request('GET', `${prefix}/pulls/${candidate.number}`);
  validatePR(pr, run, currentRepo);
  requireCondition(associationMatches(candidate, pr, run, currentRepo), 'Source pull request association or base commit does not match.');
  const context = { prefix, repository: currentRepo, workflow, run, pr, headSha: pr.head.sha, baseSha: pr.base.sha, recovered };
  await assertFresh(api, context);
  return context;
}
async function assertFresh(api, context) {
  const pr = await api.request('GET', `${context.prefix}/pulls/${context.pr.number}`);
  validatePR(pr, context.run, context.repository);
  requireCondition(pr.head.sha === context.headSha && pr.base.sha === context.baseSha, 'Pull request head/base changed; stale report suppressed.');
  const run = await api.request('GET', `${context.prefix}/actions/runs/${context.run.id}`);
  requireCondition(run.id === context.run.id && run.workflow_id === context.workflow.id && run.name === SOURCE.name && run.path?.split('@')[0] === SOURCE.path && run.repository?.id === context.repository.id && run.head_repository?.id === context.pr.head.repo.id && run.head_sha === context.headSha && run.event === 'pull_request' && run.run_attempt === context.run.run_attempt && run.status === 'completed' && ['success', 'failure'].includes(run.conclusion), 'Source run was superseded or is no longer eligible.');
  const latest = await list(api, `${context.prefix}/actions/workflows/${context.workflow.id}/runs?event=pull_request&head_sha=${context.headSha}`, 'workflow_runs');
  const matching = latest.filter((item) => item.workflow_id === context.workflow.id && item.head_sha === context.headSha && item.head_repository?.id === context.pr.head.repo.id).sort((a, b) => b.id - a.id || b.run_attempt - a.run_attempt);
  requireCondition(matching.length && matching[0].id === context.run.id && matching[0].run_attempt === context.run.run_attempt, 'A newer validation run superseded this report.');
}

/** Read only immutable tree/blob data at the verified head commit. */
async function collectSnapshot(api, context) {
  const changes = await list(api, `${context.prefix}/pulls/${context.pr.number}/files`, undefined, context.pr.changed_files);
  requireCondition(Number.isSafeInteger(context.pr.changed_files) && changes.length === context.pr.changed_files && changes.length <= REPORT_LIMITS.changes, 'Changed file coverage exceeded the snapshot limit.');
  const statuses = { added: 'added', modified: 'modified', removed: 'deleted', renamed: 'renamed', copied: 'added', changed: 'modified' };
  const snapshot = { baseSha: context.baseSha, headSha: context.headSha, changes: changes.map((item) => {
    requireCondition(validPath(item.filename) && statuses[item.status] && (item.status !== 'renamed' || validPath(item.previous_filename)), 'Changed file metadata invalid.');
    return { path: item.filename, status: statuses[item.status], ...(item.status === 'renamed' ? { previousPath: item.previous_filename } : {}) };
  }), files: [], omissions: [] };
  const source = `/repos/${context.pr.head.repo.full_name}`;
  const commit = await api.request('GET', `${source}/git/commits/${context.headSha}`);
  requireCondition(commit.sha === context.headSha && sha(commit.tree?.sha), 'Exact head commit tree unavailable.');
  const tree = await api.request('GET', `${source}/git/trees/${commit.tree.sha}?recursive=1`);
  requireCondition(tree.sha === commit.tree.sha && tree.truncated === false && Array.isArray(tree.tree) && tree.tree.length <= REPORT_LIMITS.treeEntries, 'Head tree coverage unavailable or truncated.');
  const changed = new Set(snapshot.changes.filter((item) => publicPath(item.path)).map((item) => item.path.split('/')[0]));
  const definitions = tree.tree.filter((item) => publicPath(item.path) && item.path.split('/').length === 2 && item.path.endsWith('/SKILL.md'));
  const companions = tree.tree.filter((item) => publicPath(item.path) && changed.has(item.path.split('/')[0]) && !definitions.includes(item) && item.type !== 'tree');
  const wanted = [...definitions.sort((a, b) => Number(changed.has(b.path.split('/')[0])) - Number(changed.has(a.path.split('/')[0])) || a.path.localeCompare(b.path)), ...companions.sort((a, b) => a.path.localeCompare(b.path))];
  for (const item of wanted) {
    const omit = (reason) => snapshot.omissions.push({ path: item.path, reason });
    if (item.type !== 'blob' || !['100644', '100755'].includes(item.mode)) { omit('Symlink or unsupported object omitted; never followed or executed.'); continue; }
    if (!TEXT_EXTENSIONS.has(path.extname(item.path).toLowerCase())) { omit('Binary or unsupported companion omitted.'); continue; }
    if (!sha(item.sha) || !Number.isSafeInteger(item.size) || item.size > LIMITS.fileBytes) { omit('File exceeds full-body size limit or blob metadata unavailable.'); continue; }
    if (snapshot.files.length >= REPORT_LIMITS.files || Buffer.byteLength(JSON.stringify(snapshot)) + item.size > REPORT_LIMITS.snapshotBytes) { omit('Snapshot file/context limit reached; full body omitted.'); continue; }
    const blob = await api.request('GET', `${source}/git/blobs/${item.sha}`);
    requireCondition(blob.sha === item.sha && blob.encoding === 'base64' && typeof blob.content === 'string', 'Blob response identity invalid.');
    const buffer = Buffer.from(blob.content.replace(/\s/g, ''), 'base64');
    requireCondition(buffer.length === item.size && buffer.length <= LIMITS.fileBytes, 'Blob size does not match its tree entry.');
    const text = buffer.toString('utf8');
    if (buffer.includes(0) || !Buffer.from(text).equals(buffer)) { omit('Companion is not valid UTF-8 text; body omitted.'); continue; }
    snapshot.files.push({ path: item.path, text });
  }
  requireCondition(Buffer.byteLength(JSON.stringify(snapshot)) <= REPORT_LIMITS.snapshotBytes, 'Snapshot context limit exceeded.');
  await assertFresh(api, context);
  return snapshot;
}
function display(value) {
  return String(value).replace(/https?:\/\/\S+/gi, '[link omitted]').replace(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi, '[email omitted]').replace(/\b(?:sk-|gh[opsu]_|github_pat_)[A-Za-z0-9_-]{12,}\b/g, '[credential omitted]').replace(/\b(?:password|secret|token|api[_ -]?key)\s*[:=]\s*[^\s,;]+/gi, '[private value omitted]').replace(/@/g, '[at]').replace(/[\r\n]+/g, ' ').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\\`*_{}\[\]()#!|]/g, '\\$&');
}
function mechanicalReview(snapshot) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-review-data-'));
  try {
    for (const file of snapshot.files) {
      requireCondition(validPath(file.path), 'Invalid mechanical snapshot path.');
      const target = path.join(root, file.path);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, file.text);
    }
    const changed = [...new Set(snapshot.changes.filter((item) => publicPath(item.path)).map((item) => item.path.split('/')[0]))].sort();
    const lines = ['### Mechanical authoring review — advisory', '', 'Trusted deterministic authoring checks on supplied data; these do not replace blocking CI or human review.'];
    if (!changed.length) lines.push('', 'No public skill changes to assess.');
    for (const name of changed) {
      if (!snapshot.files.some((file) => file.path === `${name}/SKILL.md`)) { lines.push('', `- ${display(name)}: definition unavailable or deleted; no mechanical clean result is claimed.`); continue; }
      const result = reviewSkill(name, root);
      if (!result.findings.length) lines.push('', `- ${display(name)}: no mechanical authoring findings in supplied files.`);
      else for (const finding of result.findings.slice(0, 30)) lines.push('', `- ${display(name)} · ${display(finding.severity)}: ${display(finding.msg)}`);
    }
    if (snapshot.omissions.length) lines.push('', `Mechanical coverage is incomplete: ${snapshot.omissions.length} supplied-data omissions. Missing-reference checks can reflect omitted companions.`);
    return lines.join('\n');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
function renderCombined(context, mechanical, report) {
  const metadata = { headSha: context.headSha, baseSha: context.baseSha, runId: context.run.id, runAttempt: context.run.run_attempt };
  let modelSection;
  try { modelSection = renderReview(report); }
  catch { modelSection = renderReview(unavailableReport(context, report?.model, 'Advisory model rendering unavailable; no completed model review is claimed.')); }
  const body = [MARKER, `<!-- skill-review-meta: ${JSON.stringify(metadata)} -->`, '## Automated skill review (advisory)', '',
    `Reviewed head: \`${context.headSha}\`. Base: \`${context.baseSha}\`. Validation run: ${context.run.id}, attempt ${context.run.run_attempt}, conclusion ${context.run.conclusion}.`,
    context.recovered ? 'Source PR association recovered from the exact-head commit-associated PR API; base captured from the current PR and rechecked before publishing.' : 'Source PR association and base/head commits verified against the canonical workflow run and current PR.',
    'This comment is automated feedback for the submitter. Findings, omissions, and service failures never change blocking checks; human self-review and qualified approval remain required.', '', mechanical, '', modelSection].join('\n');
  requireCondition(Buffer.byteLength(body) <= REPORT_LIMITS.commentBytes, 'Advisory comment size limit exceeded; no truncated clean review published.');
  return body;
}
function unavailableReport(context, model, reason) {
  return { status: 'failed', headSha: context.headSha, baseSha: context.baseSha, model: model || DEFAULT_MODEL, requests: 0, findings: [], coverage: {}, reason };
}
function botOwns(comment) { return comment.user?.type === 'Bot' && comment.user.login === 'github-actions[bot]' && typeof comment.body === 'string' && comment.body.startsWith(MARKER); }
async function publish(api, context, body) {
  await assertFresh(api, context);
  const comments = await list(api, `${context.prefix}/issues/${context.pr.number}/comments`);
  const existing = comments.filter(botOwns).sort((a, b) => b.id - a.id)[0];
  if (existing) {
    const match = existing.body.match(/<!-- skill-review-meta: (.+?) -->/);
    if (match) {
      const metadata = JSON.parse(match[1]);
      requireCondition(!(metadata.headSha === context.headSha && (metadata.runId > context.run.id || metadata.runId === context.run.id && metadata.runAttempt > context.run.run_attempt)), 'A newer sticky report already owns this commit.');
    }
    requireCondition(id(existing.id), 'Sticky comment identity invalid.');
  }
  // The workflow serializes every reporter in the repository. This final live
  // check prevents queued old reports from overwriting current results; GitHub
  // does not offer an atomic PR-head-and-comment conditional write.
  await assertFresh(api, context);
  if (existing) { await api.request('PATCH', `${context.prefix}/issues/comments/${existing.id}`, { body }); return 'updated'; }
  await api.request('POST', `${context.prefix}/issues/${context.pr.number}/comments`, { body });
  return 'posted';
}

/** Mocks inject only transports, not submitted programs. Every failure is advisory. */
async function runReport(options) {
  try {
    const context = await resolveContext(options);
    let snapshot, mechanical, report;
    try {
      snapshot = await collectSnapshot(options.api, context);
      mechanical = mechanicalReview(snapshot);
    } catch {
      mechanical = '### Mechanical authoring review — advisory\n\nUnavailable: bounded immutable snapshot collection or review failed. No clean mechanical result is claimed.';
      report = unavailableReport(context, options.reviewOptions?.model, 'Snapshot or mechanical review unavailable; no completed model review is claimed.');
    }
    if (!report) {
      try { report = await (options.review || runReview)(snapshot, options.reviewOptions || {}); }
      catch { report = unavailableReport(context, options.reviewOptions?.model, 'Advisory model service unavailable; no completed model review is claimed.'); }
    }
    const body = renderCombined(context, mechanical, report);
    return { status: await publish(options.api, context, body), headSha: context.headSha, baseSha: context.baseSha };
  } catch (error) {
    // Reasons are our fixed validation messages; never provider response data.
    return { status: 'skipped', reason: error.reviewSafe ? display(error.message).slice(0, 500) : 'Advisory provenance, network, or reporting unavailable; no completed review is claimed.' };
  }
}
async function main() {
  requireCondition(process.env.GITHUB_EVENT_NAME === 'workflow_run', 'Reporter requires a trusted workflow_run context.');
  requireCondition(fs.statSync(process.env.GITHUB_EVENT_PATH).size <= REPORT_LIMITS.responseBytes, 'Workflow event size limit exceeded.');
  const event = JSON.parse(fs.readFileSync(process.env.GITHUB_EVENT_PATH, 'utf8'));
  const result = await runReport({ event, repository: process.env.GITHUB_REPOSITORY, api: createGitHubAPI(), forkApprovalVerified: process.env.SKILL_REVIEW_FORK_APPROVAL_VERIFIED === 'true' });
  console.log(`Advisory reporter: ${result.status}${result.reason ? ` — ${result.reason}` : ''}`);
}
module.exports = { runReport, resolveContext, collectSnapshot, renderCombined, createGitHubAPI, MARKER, SOURCE, REPORT_LIMITS };
if (require.main === module) main().catch(() => { console.log('Advisory reporter unavailable; no completed review is claimed.'); });
