import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import * as validator from 'gltf-validator';

function parseIso8601(value) {
  const trimmed = value.trim();
  const hasOffset = /[+-]\d\d:\d\d$/.test(trimmed);
  const normalized = trimmed.endsWith('Z') || hasOffset ? trimmed : `${trimmed.replace(' ', 'T')}Z`;
  const parsed = new Date(normalized);
  if (Number.isNaN(parsed.getTime())) {
    throw new Error(`Invalid timestamp: ${value}`);
  }
  return parsed.toISOString();
}

async function resolveGeneratedAt(outputPath) {
  if (process.env.BUILD_TIMESTAMP) {
    return parseIso8601(process.env.BUILD_TIMESTAMP);
  }

  if (process.env.SOURCE_DATE_EPOCH) {
    const epoch = Number(process.env.SOURCE_DATE_EPOCH);
    if (!Number.isNaN(epoch)) {
      return new Date(epoch * 1000).toISOString();
    }
  }

  try {
    const previous = JSON.parse(await fs.readFile(outputPath, 'utf8'));
    if (typeof previous.generated_at === 'string') {
      return parseIso8601(previous.generated_at);
    }
  } catch {
    // No existing report. Fall through to a fresh timestamp.
  }

  try {
    const siblingSummaryPath = path.join(path.dirname(outputPath), 'validation_summary.json');
    const previousSummary = JSON.parse(await fs.readFile(siblingSummaryPath, 'utf8'));
    if (typeof previousSummary.generated_at === 'string') {
      return parseIso8601(previousSummary.generated_at);
    }
  } catch {
    // No sibling validation summary. Fall through to a fresh timestamp.
  }

  return new Date().toISOString();
}

async function validateFile(filePath) {
  const bytes = new Uint8Array(await fs.readFile(filePath));
  const report = await validator.validateBytes(bytes, {
    maxIssues: 256,
    externalResourceFunction: async () => null
  });
  return {
    file: filePath,
    numErrors: report.issues.numErrors,
    numWarnings: report.issues.numWarnings,
    numInfos: report.issues.numInfos,
    messages: report.issues.messages
  };
}

async function main() {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) {
    console.error('Usage: node scripts/validate_gltf.mjs <gltf-dir> <output-json>');
    process.exit(2);
  }

  const stat = await fs.stat(inputPath);
  let files = [];
  if (stat.isDirectory()) {
    const entries = await fs.readdir(inputPath);
    files = entries.filter((entry) => entry.endsWith('.glb')).sort().map((entry) => path.join(inputPath, entry));
  } else {
    files = [inputPath];
  }

  const results = [];
  for (const file of files) {
    results.push(await validateFile(file));
  }

  const generatedAt = await resolveGeneratedAt(outputPath);
  const summary = {
    generated_at: generatedAt,
    files_checked: results.length,
    files_with_errors: results.filter((item) => item.numErrors > 0).length,
    files_with_warnings: results.filter((item) => item.numWarnings > 0).length,
    results
  };

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(summary, null, 2));

  if (summary.files_with_errors > 0) {
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
