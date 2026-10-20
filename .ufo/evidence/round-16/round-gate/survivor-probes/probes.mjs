#!/usr/bin/env node
/* Off-suite probes for kumitate round-gate.mjs predicted-survivor arms.
 * Runs the PRISTINE pinned blob only. Never runs a mutant.
 * Every fixture under /tmp; deterministic git identity/dates.
 */
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync, openSync, closeSync } from 'node:fs';
import { dirname, join } from 'node:path';

const GATE = process.env.GATE ?? '/tmp/tameshi-r16-survivorprep/round-gate.mjs';
const ROOT = process.env.FXROOT ?? '/tmp/tameshi-r16-survivorprep/fx';
const ONLY = process.argv[2] ?? null;

const GIT_ENV = {
  ...process.env,
  GIT_CONFIG_GLOBAL: '/dev/null', GIT_CONFIG_SYSTEM: '/dev/null',
  GIT_AUTHOR_NAME: 't', GIT_AUTHOR_EMAIL: 't@t',
  GIT_COMMITTER_NAME: 't', GIT_COMMITTER_EMAIL: 't@t',
  GIT_AUTHOR_DATE: '2026-01-02T00:00:00+0000', GIT_COMMITTER_DATE: '2026-01-02T00:00:00+0000',
};
const BASE_ENV = { PATH: process.env.PATH, HOME: '/tmp/tameshi-r16-survivorprep/home-default' };

function git(cwd, args) {
  const r = spawnSync('git', ['-C', cwd, ...args], { encoding: 'utf8', env: GIT_ENV, timeout: 30000 });
  if (r.status !== 0) throw new Error(`git ${args.join(' ')} in ${cwd} -> ${r.status}: ${r.stderr}`);
  return String(r.stdout ?? '').trim();
}
function initRepo(dir) { mkdirSync(dir, { recursive: true }); git(dir, ['init', '-q', '-b', 'main']); }
function w(path, text) { mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, text); }
function commitAll(dir, msg) { git(dir, ['add', '-A']); git(dir, ['commit', '-q', '-m', msg]); return git(dir, ['rev-parse', 'HEAD']); }
function fresh(name) { const d = join(ROOT, name); rmSync(d, { recursive: true, force: true }); mkdirSync(d, { recursive: true }); return d; }

function gate(args, env = {}, opts = {}) {
  const t0 = process.hrtime.bigint();
  const r = spawnSync(process.execPath, [GATE, ...args], {
    encoding: 'utf8', timeout: 120000, env: { ...BASE_ENV, ...env },
    stdio: opts.stdoutFd != null ? ['ignore', opts.stdoutFd, 'pipe'] : ['ignore', 'pipe', 'pipe'],
  });
  const outerMs = Number(process.hrtime.bigint() - t0) / 1e6;
  return {
    argv: args, env, status: r.status, signal: r.signal,
    stdout: String(r.stdout ?? ''), stderr: String(r.stderr ?? ''),
    outerMs: Math.round(outerMs * 100) / 100, spawnError: r.error ? String(r.error) : null,
  };
}

const R = (id, arm, note) => ({ id, arm, note, assertions: [], run: null, control: null });
function A(rec, name, ok, expected, got) { rec.assertions.push({ name, ok: Boolean(ok), expected: String(expected), got: String(got) }); }
function line(stdout, n) { return String(stdout ?? '').trim().split('\n')[n] ?? ''; }
function lastLine(stdout) { return String(stdout ?? '').trim().split('\n').filter(Boolean).at(-1) ?? ''; }
function jparse(r) { try { return JSON.parse(r.stdout); } catch { return null; } }

const BIG = (round) => `# round-${round} lane report\n\n## SHONEN\n\n`
  + `- lane checklist: fixture pass\n\n## Findings\n\n`
  + `The round-${round} fixture landed with evidence on disk. `.repeat(30);
const SCORECARD = (round) => `# Scorecard\n\n| round | axis | evidence |\n|---|---|---|\n`
  + `| ${round} | operability | fixture |\n| ${round} | coverage | fixture |\n\n## Planned\n\nround ${round + 1}: the next fixture move.\n`;
const LOG = (round) => `- 2026-01-02 — round ${round} fixture entry (lane kumitate)\n`;

function cleanAudit(name = 'clean') {
  const base = fresh(name);
  const lane = join(base, 'lane'); initRepo(lane);
  w(join(lane, 'SCORECARD.md'), SCORECARD(5));
  w(join(lane, 'LOG.md'), LOG(5));
  commitAll(lane, 'round-5 fixture seed');
  const reports = join(base, 'reports');
  w(join(reports, 'round-5', 'kumitate.md'), BIG(5));
  const main = join(base, 'main'); initRepo(main); w(join(main, 'README.md'), '# main\n'); commitAll(main, 'main seed');
  const origin = join(base, 'origin'); initRepo(origin); w(join(origin, 'origin.txt'), 'origin\n'); commitAll(origin, 'origin seed');
  return { base, lane, reports, main, origin };
}
const AUDIT_ARGS = (f, extra = []) => ['--round', '5', '--repo', f.lane, '--reports-dir', f.reports,
  '--main-repo', f.main, '--origin', f.origin, ...extra];

const probes = [];
function probe(id, arm, note, fn) { probes.push({ id, arm, note, fn }); }

/* P1 — FAIL-CLOSED detail tail + stderr diagnostic (§13.5 #1) */
probe('P1', 'FAIL-CLOSED detail tail + stderr diagnostic (:615)', 'suite fcA/jFc read the token only; this pins detail tail and the stderr line', () => {
  const rec = R('P1');
  const f = cleanAudit('p1');
  const absent = join(f.base, 'absent-reports');
  const r = gate(['--round', '5', '--repo', f.lane, '--reports-dir', absent]);
  rec.run = { argv: r.argv, status: r.status, stdout: r.stdout, stderr: r.stderr };
  const wantOut = `ROUND_GATE: FAIL-CLOSED (REPORTS_DIR_MISSING) --reports-dir ${absent} is absent`;
  const wantErr = `round-gate: fail-closed — REPORTS_DIR_MISSING: --reports-dir ${absent} is absent`;
  A(rec, 'exit 2', r.status === 2, 2, r.status);
  A(rec, 'stdout is exactly one FAIL-CLOSED line with full detail tail', r.stdout === `${wantOut}\n`, JSON.stringify(wantOut + '\\n'), JSON.stringify(r.stdout));
  A(rec, 'stderr is exactly the diagnostic line', r.stderr === `${wantErr}\n`, JSON.stringify(wantErr + '\\n'), JSON.stringify(r.stderr));
  const j = gate(['--json', '--round', '5', '--repo', f.lane, '--reports-dir', absent]);
  const body = jparse(j);
  const wantKeys = ['checks', 'citations', 'contract', 'durationMs', 'errors', 'findings', 'lane', 'mode',
    'repo', 'reportsDir', 'round', 'verdict', 'warnings'].sort();
  A(rec, 'fail-closed JSON top-level key set == 13 frozen keys', body && JSON.stringify(Object.keys(body).sort()) === JSON.stringify(wantKeys),
    wantKeys.join(','), body ? Object.keys(body).sort().join(',') : 'unparsable');
  A(rec, 'fail-closed JSON citations block is all-default', body && JSON.stringify(body.citations) === JSON.stringify({ checked: 0, external: [], unresolved: [], notAncestor: [], unverifiable: [], mainProbeable: null, originProbeable: null }),
    'checked=0, all lists [], both probeable null', body && JSON.stringify(body.citations));
  A(rec, '--json fail-closed body: checks=[] and finding detail == text tail',
    body && body.checks.length === 0 && body.findings[0].detail === wantOut.slice(wantOut.indexOf('--reports-dir')),
    'checks=[] detail=' + JSON.stringify(wantOut.slice(wantOut.indexOf('--reports-dir'))),
    body ? `checks=${body.checks.length} detail=${JSON.stringify(body.findings[0].detail)}` : 'unparsable');
  rec.control = { json: { status: j.status, stderr: j.stderr } };
  return rec;
});

/* P2 — ROUND_GATE_SELFTEST counts (§13.5 #2) */
probe('P2', 'selftest summary counts (:1505)', 'hermeticity check pins shape \\d+/\\d+ only; exact counts unread', () => {
  const rec = R('P2');
  const r = gate(['--selftest']);
  const lines = r.stdout.trim().split('\n');
  rec.run = { argv: r.argv, status: r.status, tail: lines.slice(-2) };
  A(rec, 'exit 0', r.status === 0, 0, r.status);
  A(rec, 'exact summary line', lines.at(-2) === 'ROUND_GATE_SELFTEST: 60/60 pass', 'ROUND_GATE_SELFTEST: 60/60 pass', lines.at(-2));
  A(rec, 'VERDICT: PASS last line', lines.at(-1) === 'VERDICT: PASS', 'VERDICT: PASS', lines.at(-1));
  return rec;
});

/* P3 — durationMs value (§13.5 #3) */
probe('P3', 'durationMs value (:671 audit / :613 fail-closed / :569 tracked)', 'suite asserts typeof number only; this pins it to measured wall time', () => {
  const rec = R('P3');
  const f = cleanAudit('p3');
  const r1 = gate(AUDIT_ARGS(f, ['--json']));
  const j1 = jparse(r1);
  rec.run = { argv: r1.argv, status: r1.status, durationMs: j1 && j1.durationMs, outerMs: r1.outerMs, verdict: j1 && j1.verdict, checks: j1 && j1.checks.length };
  A(rec, 'clean audit exit 0', r1.status === 0, 0, r1.status);
  A(rec, 'verdict CLEAN, checks=10', j1 && j1.verdict === 'CLEAN' && j1.checks.length === 10, 'CLEAN/10', j1 ? `${j1.verdict}/${j1.checks.length}` : 'unparsable');
  A(rec, 'durationMs > 0 (a constant-0 mutant dies)', j1 && j1.durationMs > 0, '>0', j1 && j1.durationMs);
  A(rec, 'durationMs <= measured wall time + 5ms (an epoch/absolute mutant dies)', j1 && j1.durationMs <= r1.outerMs + 5, `<= ${r1.outerMs}+5`, j1 && j1.durationMs);
  const r2 = gate(AUDIT_ARGS(f, ['--json']));
  const j2 = jparse(r2);
  rec.control = { secondRun: { durationMs: j2 && j2.durationMs, outerMs: r2.outerMs } };
  A(rec, 'second run also satisfies the bracket', j2 && j2.durationMs > 0 && j2.durationMs <= r2.outerMs + 5,
    `0 < d <= ${r2.outerMs}+5`, j2 && `${j2.durationMs} vs ${r2.outerMs}`);
  return rec;
});

/* P4 — JSON citations.mainProbeable / unresolved / notAncestor (§13.5 #4) */
probe('P4', 'JSON citations.mainProbeable/unresolved/notAncestor (:387-389, :411)', 'suite reads checked/external/unverifiable/originProbeable only', () => {
  const rec = R('P4');
  const base = fresh('p4');
  const lane = join(base, 'lane'); initRepo(lane);
  w(join(lane, 'a.txt'), 'a\n'); const shaA = commitAll(lane, 'p4 a');
  w(join(lane, 'b.txt'), 'b\n'); const shaB = commitAll(lane, 'p4 b');
  git(lane, ['reset', '--hard', 'HEAD~1']);
  const bAlive = spawnSync('git', ['-C', lane, 'cat-file', '-e', `${shaB}^{commit}`], { env: GIT_ENV }).status === 0;
  const main = join(base, 'main'); initRepo(main); w(join(main, 'm.txt'), 'm\n'); const shaM = commitAll(main, 'p4 main');
  const origin = join(base, 'origin'); initRepo(origin); w(join(origin, 'o.txt'), 'o\n'); commitAll(origin, 'p4 origin');
  const reports = join(base, 'reports');
  w(join(reports, 'round-5', 'kumitate.md'),
    `# round-5 lane report\n\n## SHONEN\n\n## Findings\n\nCited: \`${shaB}\` \`${shaM}\` \`deadbeef1234\`.\n`);
  const r = gate(['--json', '--round', '5', '--repo', lane, '--reports-dir', reports, '--main-repo', main, '--origin', origin]);
  const j = jparse(r);
  rec.run = { argv: r.argv, status: r.status, citations: j && j.citations };
  const c = j && j.citations;
  A(rec, 'orphaned commit object still exists (fixture precondition)', bAlive, 'cat-file -e succeeds', bAlive);
  A(rec, 'citations.checked=3', c && c.checked === 3, 3, c && c.checked);
  A(rec, 'citations.external == [main-repo commit]', c && JSON.stringify(c.external) === JSON.stringify([shaM]), `["${shaM}"]`, c && JSON.stringify(c.external));
  A(rec, 'citations.unresolved == [deadbeef1234]', c && JSON.stringify(c.unresolved) === JSON.stringify(['deadbeef1234']), '["deadbeef1234"]', c && JSON.stringify(c.unresolved));
  A(rec, 'citations.notAncestor == [orphaned commit]', c && JSON.stringify(c.notAncestor) === JSON.stringify([shaB]), `["${shaB}"]`, c && JSON.stringify(c.notAncestor));
  A(rec, 'citations.unverifiable == []', c && c.unverifiable.length === 0, '[]', c && JSON.stringify(c.unverifiable));
  A(rec, 'citations.mainProbeable === true', c && c.mainProbeable === true, true, c && c.mainProbeable);
  A(rec, 'citations.originProbeable === true', c && c.originProbeable === true, true, c && c.originProbeable);
  const unresolvedItem = j && j.checks.find((x) => x.id === 'COMMIT_CITED_UNRESOLVED');
  const ancItem = j && j.checks.find((x) => x.id === 'COMMIT_CITED_NOT_ANCESTOR');
  A(rec, 'COMMIT_CITED_UNRESOLVED detail', unresolvedItem && unresolvedItem.detail === 'cited=3 unresolved=1 [deadbeef1234]',
    'cited=3 unresolved=1 [deadbeef1234]', unresolvedItem && unresolvedItem.detail);
  A(rec, 'COMMIT_CITED_NOT_ANCESTOR detail', ancItem && ancItem.detail === `cited=3 notAncestor=1 [${shaB}]`,
    `cited=3 notAncestor=1 [${shaB}]`, ancItem && ancItem.detail);
  return rec;
});

/* P1b — FAIL-CLOSED detail tails, remaining tokens */
probe('P1b', 'FAIL-CLOSED tails: NOT_A_GIT_WORKTREE (:645), NO_CLOSED_ROUND (:653), MAIN_REPO_NOT_GIT (:471,:531), NO_FILED_REPORTS (:537)', 'fcB–fcF/rt3/rt5 pin the token; every tail and checks count is unread', () => {
  const rec = R('P1b');
  const base = fresh('p1b');
  const lane = join(base, 'lane'); initRepo(lane); w(join(lane, 'x.txt'), 'x\n'); commitAll(lane, 'seed');
  const plain = join(base, 'plain'); mkdirSync(plain, { recursive: true });
  const emptyReports = join(base, 'empty-reports'); mkdirSync(emptyReports, { recursive: true });
  const mainGit = join(base, 'main-git'); initRepo(mainGit); w(join(mainGit, 'm.txt'), 'm\n'); commitAll(mainGit, 'seed');
  const single = join(base, 'single-reports'); w(join(single, 'round-7', 'kumitate.md'), BIG(7));
  // close fixture for the :471 site
  const closeLane = join(base, 'close-lane'); initRepo(closeLane);
  w(join(closeLane, 'SCORECARD.md'), SCORECARD(5));
  w(join(closeLane, 'LOG.md'), LOG(5));
  commitAll(closeLane, 'round-5 fixture seed');
  const bare = join(base, 'lane-origin.git');
  const b = spawnSync('git', ['init', '--bare', '-q', '-b', 'main', bare], { encoding: 'utf8', env: GIT_ENV });
  if (b.status !== 0) throw new Error(`bare init: ${b.stderr}`);
  git(closeLane, ['remote', 'add', 'origin', bare]);
  git(closeLane, ['push', '--quiet', '-u', 'origin', 'main']);
  const closeReports = join(base, 'close-reports'); w(join(closeReports, 'round-5', 'kumitate.md'), BIG(5));

  const notGit = gate(['--round', '5', '--repo', plain, '--reports-dir', emptyReports]);
  const noRound = gate(['--repo', lane, '--reports-dir', emptyReports]);
  const trackedMain = gate(['--tracked', '--lane', 'kumitate', '--reports-dir', emptyReports, '--main-repo', plain, '--json']);
  const closeMain = gate(['--close', '--json', '--round', '5', '--repo', closeLane, '--reports-dir', closeReports, '--main-repo', plain, '--origin', join(base, 'no-origin')]);
  const noFiled = gate(['--tracked', '--lane', 'kumitate', '--reports-dir', single, '--main-repo', mainGit, '--json']);
  const jt = jparse(trackedMain); const jc = jparse(closeMain); const jf = jparse(noFiled);
  rec.run = {
    notGit: { argv: notGit.argv, status: notGit.status, stdout: notGit.stdout, stderr: notGit.stderr },
    noRound: { argv: noRound.argv, status: noRound.status, stdout: noRound.stdout, stderr: noRound.stderr },
    trackedMain: { argv: trackedMain.argv, status: trackedMain.status, body: jt && { mode: jt.mode, checks: jt.checks.length, detail: jt.findings[0].detail } },
    closeMain: { argv: closeMain.argv, status: closeMain.status, body: jc && { mode: jc.mode, checks: jc.checks.length, detail: jc.findings[0].detail } },
    noFiled: { argv: noFiled.argv, status: noFiled.status, body: jf && { checks: jf.checks.length, detail: jf.findings[0].detail } },
  };
  const wantNotGit = `ROUND_GATE: FAIL-CLOSED (NOT_A_GIT_WORKTREE) --repo ${plain} is not a git work tree`;
  const wantNoRound = `ROUND_GATE: FAIL-CLOSED (NO_CLOSED_ROUND) no round-<N>/kumitate.md under ${emptyReports}`;
  A(rec, 'NOT_A_GIT_WORKTREE exact tail', notGit.status === 2 && notGit.stdout.trim() === wantNotGit, wantNotGit, notGit.stdout.trim());
  A(rec, 'NO_CLOSED_ROUND exact tail', noRound.status === 2 && noRound.stdout.trim() === wantNoRound, wantNoRound, noRound.stdout.trim());
  A(rec, 'tracked MAIN_REPO_NOT_GIT tail, mode=tracked, checks=[]',
    trackedMain.status === 2 && jt && jt.mode === 'tracked' && jt.checks.length === 0 && jt.findings[0].detail === `--main-repo ${plain} is not a git work tree`,
    `tracked/0/--main-repo ${plain} is not a git work tree`, jt && `${jt.mode}/${jt.checks.length}/${jt.findings[0].detail}`);
  A(rec, 'close MAIN_REPO_NOT_GIT tail, checks=12 (12 = 10 audit + TREE_DIRTY + UNPUSHED)',
    closeMain.status === 2 && jc && jc.mode === 'close' && jc.checks.length === 12 && jc.findings[0].detail === `--main-repo ${plain} is not a git work tree`,
    `close/12/--main-repo ${plain} is not a git work tree`, jc && `${jc.mode}/${jc.checks.length}/${jc.findings[0].detail}`);
  A(rec, 'NO_FILED_REPORTS exact tail, checks=[]',
    noFiled.status === 2 && jf && jf.checks.length === 0
      && jf.findings[0].detail === `filed=1 round-<N>/kumitate.md under ${single} (the highest round is excluded as in-flight, so >=2 are needed)`,
    `filed=1 round-<N>/kumitate.md under ${single} (…)`, jf && jf.findings[0].detail);
  A(rec, 'every refusal writes the stderr diagnostic with the same tail',
    [notGit, noRound, trackedMain, closeMain, noFiled].every((r) => /^round-gate: fail-closed — [A-Z_]+: /.test(r.stderr) && r.stderr.trim().endsWith(r.stderr.trim().split(': ').slice(2).join(': '))),
    'one stderr line per refusal', [notGit, noRound, trackedMain, closeMain, noFiled].map((r) => r.stderr.split('\n')[0].slice(0, 60)).join(' | '));
  return rec;
});

/* P4b — citations.mainProbeable=false branch */
probe('P4b', 'JSON citations.mainProbeable false branch (:375-389)', 'a mutant pinning mainProbeable true is invisible to P4 (which asserts true)', () => {
  const rec = R('P4b');
  const base = fresh('p4b');
  const lane = join(base, 'lane'); initRepo(lane); w(join(lane, 'a.txt'), 'a\n'); commitAll(lane, 'seed');
  const plainMain = join(base, 'plain-main'); mkdirSync(plainMain, { recursive: true });
  const origin = join(base, 'origin'); initRepo(origin); w(join(origin, 'o.txt'), 'o\n'); commitAll(origin, 'seed');
  const reports = join(base, 'reports');
  w(join(reports, 'round-5', 'kumitate.md'), '# round-5 lane report\n\n## SHONEN\n\n## Findings\n\nCite `deadbeef1234`.\n');
  const r = gate(['--json', '--round', '5', '--repo', lane, '--reports-dir', reports, '--main-repo', plainMain, '--origin', origin]);
  const j = jparse(r); const c = j && j.citations;
  rec.run = { argv: r.argv, status: r.status, citations: c };
  A(rec, 'mainProbeable === false', c && c.mainProbeable === false, false, c && c.mainProbeable);
  A(rec, 'originProbeable === true', c && c.originProbeable === true, true, c && c.originProbeable);
  A(rec, 'unverifiable == [deadbeef1234] (main not probeable)', c && JSON.stringify(c.unverifiable) === JSON.stringify(['deadbeef1234']), '["deadbeef1234"]', c && JSON.stringify(c.unverifiable));
  A(rec, 'unresolved == []', c && c.unresolved.length === 0, '[]', c && JSON.stringify(c.unresolved));
  return rec;
});

/* P5 — text finding details (§13.5 #5) */
probe('P5a', 'REPORT_MISSING detail path (:343)', 'r3 reads the kind list only; the path is unread', () => {
  const rec = R('P5a');
  const f = cleanAudit('p5a');
  const reports = join(f.base, 'empty-reports'); mkdirSync(reports, { recursive: true });
  const r = gate(['--round', '5', '--repo', f.lane, '--reports-dir', reports]);
  const wantPath = join(reports, 'round-5', 'kumitate.md');
  const want = `ROUND_GATE  error  REPORT_MISSING  ${wantPath}`;
  rec.run = { argv: r.argv, status: r.status, stdout: r.stdout };
  A(rec, 'exit 1', r.status === 1, 1, r.status);
  A(rec, 'exact REPORT_MISSING detail line', r.stdout.split('\n')[0] === want, JSON.stringify(want), JSON.stringify(r.stdout.split('\n')[0]));
  A(rec, 'verdict checks=5 (report branch contributes 1)', lastLine(r.stdout) === 'ROUND_GATE: DRIFT (round=5 lane=kumitate checks=5 errors=1 warnings=0)',
    'checks=5 errors=1 warnings=0', lastLine(r.stdout));
  return rec;
});
probe('P5b', 'r7 mismatch message + r10/r15 detail paths (:350, :402, :429)', 'exact details of REPORT_ROUND_MISMATCH, SCORECARD_ROW_MISSING, SCORECARD_PLAN_MISSING, LOG_ENTRY_MISSING', () => {
  const rec = R('P5b');
  const base = fresh('p5b');
  const lane = join(base, 'lane'); initRepo(lane);
  w(join(lane, 'SCORECARD.md'), '# Scorecard\n\n| round | axis |\n|---|---|\n| 1 | coverage |\n');
  w(join(lane, 'LOG.md'), '- 2026-01-02 — round 4 fixture entry\n');
  commitAll(lane, 'seed p5b');
  const reports = join(base, 'reports');
  const reportPath = join(reports, 'round-5', 'kumitate.md');
  w(reportPath, '# lane report\n\n## SHONEN\n\n## Findings\n\n' + 'Only round-6 is mentioned here. '.repeat(60));
  const r = gate(['--round', '5', '--repo', lane, '--reports-dir', reports]);
  rec.run = { argv: r.argv, status: r.status, stdout: r.stdout };
  const lines = r.stdout.split('\n');
  const wantMismatch = `ROUND_GATE  error  REPORT_ROUND_MISMATCH  neither "round-5" nor "round <5>" in ${reportPath}`;
  const wantRow = `ROUND_GATE  error  SCORECARD_ROW_MISSING  no table row starting "| 5 |" in ${join(lane, 'SCORECARD.md')}`;
  const wantPlan = `ROUND_GATE  warning  SCORECARD_PLAN_MISSING  no ## Planned section in ${join(lane, 'SCORECARD.md')}`;
  const wantLog = `ROUND_GATE  error  LOG_ENTRY_MISSING  no "- YYYY-MM-DD — round 5" line in ${join(lane, 'LOG.md')}`;
  A(rec, 'exit 1', r.status === 1, 1, r.status);
  A(rec, 'exact REPORT_ROUND_MISMATCH detail', lines.includes(wantMismatch), JSON.stringify(wantMismatch), JSON.stringify(lines.find((l) => l.includes('REPORT_ROUND_MISMATCH'))));
  A(rec, 'exact SCORECARD_ROW_MISSING detail', lines.includes(wantRow), JSON.stringify(wantRow), JSON.stringify(lines.find((l) => l.includes('SCORECARD_ROW_MISSING'))));
  A(rec, 'exact SCORECARD_PLAN_MISSING detail', lines.includes(wantPlan), JSON.stringify(wantPlan), JSON.stringify(lines.find((l) => l.includes('SCORECARD_PLAN_MISSING'))));
  A(rec, 'exact LOG_ENTRY_MISSING detail', lines.includes(wantLog), JSON.stringify(wantLog), JSON.stringify(lines.find((l) => l.includes('LOG_ENTRY_MISSING'))));
  const commitLine = lines.find((l) => l.includes('COMMIT_MISSING')) ?? '';
  A(rec, 'COMMIT_MISSING detail', /^ROUND_GATE {2}error {2}COMMIT_MISSING {2}no message matching \\bround\[- \]5\\b in \d+ messages of /.test(commitLine),
    'no message matching \\bround[- ]5\\b in <n> messages of <repo>', JSON.stringify(commitLine));
  return rec;
});

/* P6 — tracked-mode REPORTS_DIR_MISSING site (:527) */
probe('P6', 'tracked REPORTS_DIR_MISSING (:527)', 'fcA/jFc exercise the main site only; site swap is invisible', () => {
  const rec = R('P6');
  const base = fresh('p6');
  const main = join(base, 'main'); initRepo(main); w(join(main, 'README.md'), '# main\n'); commitAll(main, 'seed');
  const absent = join(base, 'absent-reports');
  const r = gate(['--tracked', '--lane', 'kumitate', '--reports-dir', absent, '--main-repo', main, '--json']);
  const j = jparse(r);
  rec.run = { argv: r.argv, status: r.status, body: j ? { mode: j.mode, round: j.round, verdict: j.verdict, kind: j.findings[0] && j.findings[0].kind, detail: j.findings[0] && j.findings[0].detail, checks: j.checks.length } : null, stderr: r.stderr };
  const wantDetail = `--reports-dir ${absent} is absent`;
  A(rec, 'exit 2', r.status === 2, 2, r.status);
  A(rec, 'JSON mode=tracked (site discriminator vs main site)', j && j.mode === 'tracked', 'tracked', j && j.mode);
  A(rec, 'round=null', j && j.round === null, null, j && j.round);
  A(rec, 'verdict FAIL-CLOSED', j && j.verdict === 'FAIL-CLOSED', 'FAIL-CLOSED', j && j.verdict);
  A(rec, 'finding kind REPORTS_DIR_MISSING', j && j.findings.length === 1 && j.findings[0].kind === 'REPORTS_DIR_MISSING', 'REPORTS_DIR_MISSING', j && j.findings[0] && j.findings[0].kind);
  A(rec, 'exact detail', j && j.findings[0].detail === wantDetail, wantDetail, j && j.findings[0] && j.findings[0].detail);
  A(rec, 'checks=[] (fails before any tracked enumeration)', j && j.checks.length === 0, 0, j && j.checks.length);
  A(rec, 'stderr diagnostic', r.stderr === `round-gate: fail-closed — REPORTS_DIR_MISSING: ${wantDetail}\n`, JSON.stringify(`round-gate: fail-closed — REPORTS_DIR_MISSING: ${wantDetail}\\n`), JSON.stringify(r.stderr));
  const audit = gate(['--round', '5', '--repo', main, '--reports-dir', absent]);
  rec.control = { mainSite: { status: audit.status, mode: 'audit (text)' } };
  A(rec, 'main site control: same token/detail, mode=audit', audit.status === 2 && audit.stdout.trim() === `ROUND_GATE: FAIL-CLOSED (REPORTS_DIR_MISSING) ${wantDetail}`,
    'exit 2 + same tail', `${audit.status} ${JSON.stringify(audit.stdout)}`);
  return rec;
});

/* P7 — main-repo UPSTREAM_MISSING site (:488) */
probe('P7', 'main-repo UPSTREAM_MISSING (:488)', 'fcE exercises the lane `--repo` site only; detail prefix and checks count are the discriminators', () => {
  const rec = R('P7');
  const base = fresh('p7');
  const lane = join(base, 'lane'); initRepo(lane);
  w(join(lane, 'SCORECARD.md'), SCORECARD(5));
  w(join(lane, 'LOG.md'), LOG(5));
  commitAll(lane, 'round-5 fixture seed');
  const bare = join(base, 'lane-origin.git');
  const b = spawnSync('git', ['init', '--bare', '-q', '-b', 'main', bare], { encoding: 'utf8', env: GIT_ENV });
  if (b.status !== 0) throw new Error(`bare init: ${b.stderr}`);
  git(lane, ['remote', 'add', 'origin', bare]);
  git(lane, ['push', '--quiet', '-u', 'origin', 'main']);
  const main = join(base, 'main'); initRepo(main);
  w(join(main, 'README.md'), '# main\n');
  w(join(main, '.ufo', 'reports', 'round-5', 'kumitate.md'), BIG(5));
  commitAll(main, 'round-5 fixture report');
  const origin = join(base, 'no-origin');
  const r = gate(['--close', '--json', '--round', '5', '--repo', lane,
    '--reports-dir', join(main, '.ufo', 'reports'), '--main-repo', main, '--origin', origin]);
  const j = jparse(r);
  rec.run = { argv: r.argv, status: r.status, body: j ? { mode: j.mode, verdict: j.verdict, checks: j.checks.length, kind: j.findings[0] && j.findings[0].kind, detail: j.findings[0] && j.findings[0].detail } : null, stderr: r.stderr };
  A(rec, 'exit 2', r.status === 2, 2, r.status);
  A(rec, 'mode=close', j && j.mode === 'close', 'close', j && j.mode);
  A(rec, 'verdict FAIL-CLOSED', j && j.verdict === 'FAIL-CLOSED', 'FAIL-CLOSED', j && j.verdict);
  A(rec, 'kind UPSTREAM_MISSING', j && j.findings.length === 1 && j.findings[0].kind === 'UPSTREAM_MISSING', 'UPSTREAM_MISSING', j && j.findings[0] && j.findings[0].kind);
  A(rec, 'detail names --main-repo (not the lane --repo site)', j && j.findings[0].detail.startsWith(`--main-repo ${main}: exit 128`), `--main-repo ${main}: exit 128 …`, j && j.findings[0] && j.findings[0].detail);
  A(rec, 'checks=12 (10 audit + TREE_DIRTY + UNPUSHED survive into the refusal)', j && j.checks.length === 12, 12, j && j.checks.length);
  A(rec, 'stderr diagnostic carries the same tail', r.stderr.startsWith('round-gate: fail-closed — UPSTREAM_MISSING: --main-repo '), 'round-gate: fail-closed — UPSTREAM_MISSING: --main-repo …', JSON.stringify(r.stderr));
  A(rec, 'fail-closed durationMs bracket (0 < d <= wall+5)', j && j.durationMs > 0 && j.durationMs <= r.outerMs + 5,
    `0 < d <= ${r.outerMs}+5`, j && `${j.durationMs} vs ${r.outerMs}`);
  return rec;
});

/* P8 — usage/validation siblings (§13.6 #4) */
probe('P8', 'usage siblings: --round non-safe (:256), dirValue flag-like (:246), env lane (:278)', 'u1-u5 pin other spellings only', () => {
  const rec = R('P8');
  const a = gate(['--round', '9007199254740992']);
  const b = gate(['--repo', '--json']);
  const c = gate([], { KUMITATE_LANE: '1bad' });
  rec.run = { a: { argv: a.argv, status: a.status, first: a.stderr.split('\n')[0] }, b: { argv: b.argv, status: b.status, first: b.stderr.split('\n')[0] }, c: { argv: c.argv, env: c.env, status: c.status, first: c.stderr.split('\n')[0] } };
  A(rec, '--round 2^53 → exit 64', a.status === 64, 64, a.status);
  A(rec, '--round out-of-range message', a.stderr.split('\n')[0] === 'round-gate: --round out of range (got "9007199254740992")', 'round-gate: --round out of range (got "9007199254740992")', a.stderr.split('\n')[0]);
  A(rec, '--repo --json → exit 64', b.status === 64, 64, b.status);
  A(rec, 'dirValue flag-like message', b.stderr.split('\n')[0] === 'round-gate: --repo requires a directory (got "--json")', 'round-gate: --repo requires a directory (got "--json")', b.stderr.split('\n')[0]);
  A(rec, 'KUMITATE_LANE=1bad → exit 64', c.status === 64, 64, c.status);
  A(rec, 'env-lane message', c.stderr.split('\n')[0] === 'round-gate: KUMITATE_LANE must match ^[A-Za-z][A-Za-z0-9-]*$ (got "1bad")', 'round-gate: KUMITATE_LANE must match ^[A-Za-z][A-Za-z0-9-]*$ (got "1bad")', c.stderr.split('\n')[0]);
  A(rec, 'usage block printed after the message (3 lines then usage)', /round-gate: [^\n]+\n\nusage: node scripts\/round-gate\.mjs/u.test(a.stderr), '…\\n\\nusage: node scripts/round-gate.mjs …', JSON.stringify(a.stderr.slice(0, 120)));
  return rec;
});

/* P9 — UFO_SRC set-value branch (:162-163) */
probe('P9', 'UFO_SRC set-value branch (:162-163)', 'derived-origin fixtures force UFO_SRC:"" and never give a set origin; this pins env-wins and whitespace fallback', () => {
  const rec = R('P9');
  const base = fresh('p9');
  const home = join(base, 'home');
  const cand = join(home, 'Projects', 'ufo-fsd-alpha'); initRepo(cand); w(join(cand, 'c.txt'), 'c\n'); const shaCand = commitAll(cand, 'candidate');
  const alt = join(base, 'alt-origin'); initRepo(alt); w(join(alt, 'a.txt'), 'a\n'); const shaAlt = commitAll(alt, 'alt');
  const lane = join(base, 'lane'); initRepo(lane); w(join(lane, 's.txt'), 's\n'); commitAll(lane, 'seed');
  const main = join(base, 'main'); initRepo(main); w(join(main, 'm.txt'), 'm\n'); commitAll(main, 'seed');
  const reportsAlt = join(base, 'reports-alt');
  w(join(reportsAlt, 'round-5', 'kumitate.md'), `# round-5 lane report\n\n## SHONEN\n\n## Findings\n\nOrigin \`${shaAlt}\`.\n`);
  const reportsCand = join(base, 'reports-cand');
  w(join(reportsCand, 'round-5', 'kumitate.md'), `# round-5 lane report\n\n## SHONEN\n\n## Findings\n\nOrigin \`${shaCand}\`.\n`);
  const rA = gate(['--json', '--round', '5', '--repo', lane, '--reports-dir', reportsAlt, '--main-repo', main], { HOME: home, UFO_SRC: alt });
  const jA = jparse(rA);
  const rB = gate(['--json', '--round', '5', '--repo', lane, '--reports-dir', reportsCand, '--main-repo', main], { HOME: home, UFO_SRC: '   ' });
  const jB = jparse(rB);
  rec.run = { A: { env: { HOME: home, UFO_SRC: alt }, citations: jA && jA.citations }, B: { env: { HOME: home, UFO_SRC: '   ' }, citations: jB && jB.citations } };
  A(rec, 'set UFO_SRC wins over an existing candidate: external=[alt commit]', jA && JSON.stringify(jA.citations.external) === JSON.stringify([shaAlt]), `["${shaAlt}"]`, jA && JSON.stringify(jA.citations.external));
  A(rec, 'set UFO_SRC: originProbeable=true', jA && jA.citations.originProbeable === true, true, jA && jA.citations.originProbeable);
  A(rec, 'set UFO_SRC: no unresolved token', jA && jA.citations.unresolved.length === 0, '[]', jA && JSON.stringify(jA.citations.unresolved));
  A(rec, 'whitespace-only UFO_SRC falls back to ~/Projects/ufo-fsd-alpha: external=[candidate commit]', jB && JSON.stringify(jB.citations.external) === JSON.stringify([shaCand]), `["${shaCand}"]`, jB && JSON.stringify(jB.citations.external));
  A(rec, 'whitespace-only: originProbeable=true', jB && jB.citations.originProbeable === true, true, jB && jB.citations.originProbeable);
  return rec;
});

/* P10 — documented readings with no pin (§13.6 #6) */
probe('P10', '--help/-h unknown (:125-126), --selftest wins over --json (:48), main-repo flag>env (:273)', 'u1 pins --bogus only; no combined selftest+json fixture; r45 does not discriminate main-repo precedence', () => {
  const rec = R('P10');
  const h = gate(['--help']);
  const hh = gate(['-h']);
  const sj = gate(['--selftest', '--json']);
  const sjLines = sj.stdout.trim().split('\n');
  const base = fresh('p10');
  const main = join(base, 'main'); initRepo(main); w(join(main, 'README.md'), '# main\n'); commitAll(main, 'seed');
  for (const round of [3, 4, 5]) w(join(main, '.ufo', 'reports', `round-${round}`, 'kumitate.md'), BIG(round));
  git(main, ['add', '-A']); git(main, ['commit', '-q', '-m', 'filed reports']);
  const reports = join(main, '.ufo', 'reports');
  const p = gate(['--tracked', '--lane', 'kumitate', '--reports-dir', reports, '--main-repo', main, '--json'], { KUMITATE_MAIN_REPO: join(base, 'env-main-should-lose') });
  const pj = jparse(p);
  rec.run = {
    help: { argv: h.argv, status: h.status, first: h.stderr.split('\n')[0] },
    h: { argv: hh.argv, status: hh.status, first: hh.stderr.split('\n')[0] },
    selftestJson: { argv: sj.argv, status: sj.status, first: sjLines[0], last: sjLines.at(-1) },
    precedence: { argv: p.argv, env: p.env, status: p.status, mainRepo: pj && pj.mainRepo, checked: pj && pj.checked, excludedRound: pj && pj.excludedRound, durationMs: pj && pj.durationMs, outerMs: p.outerMs },
  };
  A(rec, '--help → exit 64', h.status === 64, 64, h.status);
  A(rec, '--help unknown-argument message', h.stderr.split('\n')[0] === 'round-gate: unknown argument: --help', 'round-gate: unknown argument: --help', h.stderr.split('\n')[0]);
  A(rec, '-h → exit 64 and unknown-argument message', hh.status === 64 && hh.stderr.split('\n')[0] === 'round-gate: unknown argument: -h', '64 / unknown argument: -h', `${hh.status} ${hh.stderr.split('\n')[0]}`);
  A(rec, '--selftest --json runs the TEXT suite (selftest wins)', sj.status === 0 && sjLines[0].startsWith('kumitate round-gate --selftest (hermetic, node ') && sjLines.at(-1) === 'VERDICT: PASS' && !sj.stdout.trimStart().startsWith('{'),
    'text suite, VERDICT: PASS', `${sj.status} ${JSON.stringify(sjLines[0])} … ${JSON.stringify(sjLines.at(-1))}`);
  A(rec, 'tracked --main-repo flag beats KUMITATE_MAIN_REPO env', p.status === 0 && pj && pj.mainRepo === main && pj.checked === 2 && pj.excludedRound === 5,
    `exit 0 mainRepo=${main} checked=2 excludedRound=5`, `${p.status} ${pj && JSON.stringify({ mainRepo: pj.mainRepo, checked: pj.checked, excludedRound: pj.excludedRound })}`);
  A(rec, 'tracked durationMs bracket (0 < d <= wall+5)', pj && pj.durationMs > 0 && pj.durationMs <= p.outerMs + 5,
    `0 < d <= ${p.outerMs}+5`, pj && `${pj.durationMs} vs ${p.outerMs}`);
  return rec;
});

/* P11 — citationTokens range form (:315-324) */
probe('P11', 'citationTokens range form (:315-324)', 'all fixture citations are single tokens; the documented `a..b` split is unpinned', () => {
  const rec = R('P11');
  const base = fresh('p11');
  const lane = join(base, 'lane'); initRepo(lane);
  w(join(lane, 'a.txt'), 'a\n'); const shaA = commitAll(lane, 'p11 a');
  w(join(lane, 'b.txt'), 'b\n'); const shaB = commitAll(lane, 'p11 b');
  const a7 = shaA.slice(0, 7); const b7 = shaB.slice(0, 7);
  const reports = join(base, 'reports');
  w(join(reports, 'round-5', 'kumitate.md'), `# round-5 lane report\n\n## SHONEN\n\n## Findings\n\nRange \`${a7}..${b7}\`.\n`);
  const r = gate(['--json', '--round', '5', '--repo', lane, '--reports-dir', reports]);
  const j = jparse(r);
  const unresolved = j && j.checks.find((x) => x.id === 'COMMIT_CITED_UNRESOLVED');
  const anc = j && j.checks.find((x) => x.id === 'COMMIT_CITED_NOT_ANCESTOR');
  rec.run = { argv: r.argv, status: r.status, checked: j && j.citations.checked, unresolvedDetail: unresolved && unresolved.detail, notAncestorDetail: anc && anc.detail };
  A(rec, '7-hex parts are distinct (fixture precondition)', a7 !== b7, 'distinct prefixes', `${a7}/${b7}`);
  A(rec, 'range splits into 2 tokens: citations.checked=2', j && j.citations.checked === 2, 2, j && j.citations.checked);
  A(rec, 'COMMIT_CITED_UNRESOLVED detail reads cited=2', unresolved && unresolved.detail === 'cited=2 unresolved=0', 'cited=2 unresolved=0', unresolved && unresolved.detail);
  A(rec, 'COMMIT_CITED_NOT_ANCESTOR detail reads cited=2', anc && anc.detail === 'cited=2 notAncestor=0', 'cited=2 notAncestor=0', anc && anc.detail);
  return rec;
});

/* P12 — INTERNAL_ERROR reachability attempt (:683) */
probe('P12', 'INTERNAL_ERROR catch-all (:683)', 'no fixture reaches it; this attempts the only constructor-visible routes and records whether the token can fire', () => {
  const rec = R('P12');
  const badTmp = gate(['--selftest'], { TMPDIR: '/nonexistent/t' });
  const base = fresh('p12');
  const f = cleanAudit('p12');
  const fullFd = openSync('/dev/full', 'w');
  let full;
  try {
    full = gate(AUDIT_ARGS(f, ['--json']), {}, { stdoutFd: fullFd });
  } finally { closeSync(fullFd); }
  const file = join(base, 'not-a-repo.txt'); w(file, 'x\n');
  const notGit = gate(['--round', '5', '--repo', file, '--reports-dir', f.reports]);
  rec.run = {
    badTmp: { argv: badTmp.argv, env: badTmp.env, status: badTmp.status, stderrFirst: badTmp.stderr.split('\n')[0] },
    devFull: { argv: full.argv, status: full.status, stderr: full.stderr.split('\n').slice(0, 4) },
    notGit: { argv: notGit.argv, status: notGit.status, stdoutFirst: notGit.stdout.split('\n')[0] },
  };
  A(rec, 'broken TMPDIR --selftest escapes the catch-all (exit 1, raw stack, no token)',
    badTmp.status === 1 && /binding\.mkdtemp|mkdtemp/u.test(badTmp.stderr) && !badTmp.stderr.includes('INTERNAL_ERROR'),
    'exit 1 + mkdtemp stack, no INTERNAL_ERROR', `${badTmp.status} ${JSON.stringify(badTmp.stderr.split('\n')[0])}`);
  A(rec, '--repo a regular file → NOT_A_GIT_WORKTREE, not INTERNAL_ERROR', notGit.status === 2 && notGit.stdout.includes('NOT_A_GIT_WORKTREE'), '2 NOT_A_GIT_WORKTREE', `${notGit.status} ${JSON.stringify(notGit.stdout.split('\n')[0])}`);
  const tokenFired = full.stderr.includes('INTERNAL_ERROR');
  A(rec, 'stdout write failure (/dev/full) does NOT reach the token', tokenFired === false,
    'no INTERNAL_ERROR on stderr', JSON.stringify(full.stderr.split('\n').slice(0, 4)));
  A(rec, 'write failure surfaces as an async unhandled error event after main returned, exit 1',
    full.status === 1 && /Unhandled 'error' event/u.test(full.stderr), "exit 1 + Unhandled 'error' event", `${full.status} ${JSON.stringify(full.stderr.split('\n').slice(0, 4))}`);
  return rec;
});

const selected = ONLY ? probes.filter((p) => p.id === ONLY) : probes;
const out = [];
for (const p of selected) {
  let rec;
  try { rec = p.fn(); } catch (e) { rec = R(p.id); rec.error = String(e && e.stack ? e.stack : e); }
  rec.id = p.id; rec.arm = p.arm; rec.note = p.note;
  rec.ok = rec.assertions.every((a) => a.ok) && !rec.error;
  out.push(rec);
  const failed = rec.assertions.filter((a) => !a.ok);
  console.log(`\n## ${rec.id} — ${rec.arm} :: ${rec.ok ? 'ALL ASSERTIONS PASS' : `FAIL (${failed.length})`}`);
  for (const a of rec.assertions) console.log(`  ${a.ok ? 'PASS' : 'FAIL'}  ${a.name}\n        expected: ${a.expected}\n        got     : ${a.got}`);
  if (rec.error) console.log(`  ERROR ${rec.error}`);
}
console.log('\n' + JSON.stringify(out, null, 2));
process.exitCode = out.every((r) => r.ok) ? 0 : 1;
