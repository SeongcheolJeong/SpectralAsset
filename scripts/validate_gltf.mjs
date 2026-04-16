import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import * as validator from 'gltf-validator';

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

  const summary = {
    generated_at: new Date().toISOString(),
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

