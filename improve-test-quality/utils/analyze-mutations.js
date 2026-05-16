#!/usr/bin/env node

/**
 * Mutation Testing Analysis Helper
 *
 * Analyzes Stryker mutation testing JSON reports efficiently.
 *
 * Usage:
 *   node analyze-mutations.js summary <file>
 *   node analyze-mutations.js survived <file>
 *   node analyze-mutations.js by-type <file>
 *   node analyze-mutations.js by-line <file> <line>
 *   node analyze-mutations.js high-priority <file>
 *
 * Examples:
 *   node analyze-mutations.js summary server/services/googleSheetsApi.js
 *   node analyze-mutations.js survived server/routes/projects.js
 *   node analyze-mutations.js by-type server/utils/dateUtils.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Default report path (relative to project root)
const DEFAULT_REPORT_PATH = 'reports/mutation/mutation.json';

/**
 * Load mutation report from JSON file
 */
function loadReport(reportPath) {
  try {
    const fullPath = path.resolve(process.cwd(), reportPath);
    const content = fs.readFileSync(fullPath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error loading report: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Find file data in report (handles path variations)
 */
function findFileData(report, targetFile) {
  const files = report.files;

  // Try exact match first
  if (files[targetFile]) {
    return { path: targetFile, data: files[targetFile] };
  }

  // Try finding by filename
  const matches = Object.keys(files).filter(f => f.includes(targetFile));

  if (matches.length === 0) {
    console.error(`File not found in report: ${targetFile}`);
    console.error(`Available files:`);
    Object.keys(files).forEach(f => console.error(`  - ${f}`));
    process.exit(1);
  }

  if (matches.length > 1) {
    console.error(`Multiple matches found for: ${targetFile}`);
    matches.forEach(m => console.error(`  - ${m}`));
    process.exit(1);
  }

  return { path: matches[0], data: files[matches[0]] };
}

/**
 * Get summary metrics for a file
 */
function getSummary(fileData) {
  const mutants = fileData.mutants;
  const killed = mutants.filter(m => m.status === 'Killed').length;
  const survived = mutants.filter(m => m.status === 'Survived').length;
  const noCoverage = mutants.filter(m => m.status === 'NoCoverage').length;
  const timeout = mutants.filter(m => m.status === 'Timeout').length;
  const total = mutants.length;
  const score = total > 0 ? ((killed / total) * 100).toFixed(2) : '0.00';

  return {
    total,
    killed,
    survived,
    noCoverage,
    timeout,
    score: parseFloat(score)
  };
}

/**
 * Get survived mutants with details
 */
function getSurvivedMutants(fileData) {
  return fileData.mutants
    .filter(m => m.status === 'Survived')
    .map(m => ({
      id: m.id,
      line: m.location.start.line,
      column: m.location.start.column,
      mutatorName: m.mutatorName,
      replacement: m.replacement,
      original: m.mutatorName
    }))
    .sort((a, b) => a.line - b.line);
}

/**
 * Group survived mutants by type
 */
function groupByType(fileData) {
  const survived = fileData.mutants.filter(m => m.status === 'Survived');
  const groups = {};

  survived.forEach(m => {
    if (!groups[m.mutatorName]) {
      groups[m.mutatorName] = [];
    }
    groups[m.mutatorName].push({
      id: m.id,
      line: m.location.start.line,
      replacement: m.replacement
    });
  });

  // Sort lines within each group
  Object.keys(groups).forEach(key => {
    groups[key].sort((a, b) => a.line - b.line);
  });

  return groups;
}

/**
 * Get mutants at a specific line
 */
function getMutantsAtLine(fileData, lineNumber) {
  return fileData.mutants
    .filter(m => m.location.start.line === parseInt(lineNumber))
    .map(m => ({
      id: m.id,
      status: m.status,
      mutatorName: m.mutatorName,
      replacement: m.replacement,
      line: m.location.start.line,
      column: m.location.start.column
    }));
}

/**
 * Categorize mutants by priority
 */
function categorizeBypriority(fileData) {
  const survived = fileData.mutants.filter(m => m.status === 'Survived');
  const groups = groupByType(fileData);

  const highPriority = ['ConditionalExpression', 'LogicalOperator', 'EqualityOperator'];
  const mediumPriority = ['ArithmeticOperator', 'ReturnStatement', 'BlockStatement', 'MethodExpression', 'OptionalChaining'];

  const categorized = {
    high: [],
    medium: [],
    low: []
  };

  Object.keys(groups).forEach(mutatorName => {
    const mutants = groups[mutatorName];
    if (highPriority.includes(mutatorName)) {
      categorized.high.push({ mutatorName, count: mutants.length, mutants });
    } else if (mediumPriority.includes(mutatorName)) {
      categorized.medium.push({ mutatorName, count: mutants.length, mutants });
    } else {
      categorized.low.push({ mutatorName, count: mutants.length, mutants });
    }
  });

  return categorized;
}

/**
 * Format output for display
 */
function formatOutput(data, format = 'json') {
  if (format === 'json') {
    return JSON.stringify(data, null, 2);
  }
  // Could add other formats (table, markdown, etc.) in the future
  return data;
}

// Main CLI handler
function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: analyze-mutations.js <command> <file> [options]');
    console.error('Commands: summary, survived, by-type, by-line, high-priority');
    process.exit(1);
  }

  const command = args[0];
  const targetFile = args[1];
  const reportPath = process.env.MUTATION_REPORT || DEFAULT_REPORT_PATH;

  // Load report and find file
  const report = loadReport(reportPath);
  const { path: filePath, data: fileData } = findFileData(report, targetFile);

  let output;

  switch (command) {
    case 'summary':
      output = getSummary(fileData);
      break;

    case 'survived':
      output = getSurvivedMutants(fileData);
      break;

    case 'by-type':
      output = groupByType(fileData);
      break;

    case 'by-line':
      if (args.length < 3) {
        console.error('Usage: analyze-mutations.js by-line <file> <line>');
        process.exit(1);
      }
      output = getMutantsAtLine(fileData, args[2]);
      break;

    case 'high-priority':
      output = categorizeBypriority(fileData);
      break;

    default:
      console.error(`Unknown command: ${command}`);
      console.error('Available commands: summary, survived, by-type, by-line, high-priority');
      process.exit(1);
  }

  console.log(formatOutput(output));
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export functions for use as a module
export {
  loadReport,
  findFileData,
  getSummary,
  getSurvivedMutants,
  groupByType,
  getMutantsAtLine,
  categorizeBypriority
};
