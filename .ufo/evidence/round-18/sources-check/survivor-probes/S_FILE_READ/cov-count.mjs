// cov-count.mjs — sum V8 block-coverage execution counts (NODE_V8_COVERAGE output)
// at chosen source points of one script, across every recorded process.
// Usage: node cov-count.mjs COVDIR SCRIPT LINE:NEEDLE...
// A point is the first occurrence of NEEDLE on 1-based LINE; its count in one
// process is the count of the innermost reported range containing it.
import { readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [covDir, script, ...points] = process.argv.slice(2);
if (!covDir || !script || points.length === 0) {
  process.stderr.write('usage: node cov-count.mjs COVDIR SCRIPT LINE:NEEDLE...\n');
  process.exit(64);
}
const url = pathToFileURL(resolve(script)).href;
const src = readFileSync(script, 'utf8');
const starts = [0];
for (let i = 0; i < src.length; i += 1) if (src[i] === '\n') starts.push(i + 1);
const targets = points.map((point) => {
  const sep = point.indexOf(':');
  const line = Number(point.slice(0, sep));
  const needle = point.slice(sep + 1);
  const text = src.slice(starts[line - 1], (starts[line] ?? src.length + 1) - 1);
  const col = text.indexOf(needle);
  if (!Number.isInteger(line) || col < 0) throw new Error(`needle not found on line ${line}: ${needle}`);
  return { line, needle, offset: starts[line - 1] + col, count: 0, executing: 0 };
});
const files = readdirSync(covDir).filter((name) => name.endsWith('.json')).sort();
let withScript = 0;
for (const name of files) {
  const entry = JSON.parse(readFileSync(join(covDir, name), 'utf8')).result.find((r) => r.url === url);
  if (!entry) continue;
  withScript += 1;
  const ranges = entry.functions.flatMap((fn) => fn.ranges);
  for (const t of targets) {
    let best = null;
    for (const r of ranges) {
      if (r.startOffset <= t.offset && t.offset < r.endOffset
        && (best === null || r.endOffset - r.startOffset < best.endOffset - best.startOffset)) best = r;
    }
    if (best === null) throw new Error(`${name}: no range covers line ${t.line}`);
    t.count += best.count;
    if (best.count > 0) t.executing += 1;
  }
}
process.stdout.write(`COVERAGE script=${url} coverage-files=${files.length} processes-with-script=${withScript}\n`);
for (const t of targets) {
  process.stdout.write(`COVERAGE line=${t.line} offset=${t.offset} count=${t.count} processes-executing=${t.executing} needle=${t.needle}\n`);
}
