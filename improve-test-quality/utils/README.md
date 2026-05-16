# Mutation Testing Analysis Utilities

Helper scripts for analyzing Stryker mutation testing reports.

## analyze-mutations.js

Efficiently extracts and analyzes data from large mutation JSON reports.

### Usage

```bash
node analyze-mutations.js <command> <file> [options]
```

### Commands

#### `summary <file>`
Get overall mutation metrics for a file.

```bash
node analyze-mutations.js summary server/services/googleSheetsApi.js
```

Output:
```json
{
  "total": 162,
  "killed": 48,
  "survived": 20,
  "noCoverage": 88,
  "timeout": 2,
  "score": 29.63
}
```

#### `survived <file>`
List all survived mutants with line numbers.

```bash
node analyze-mutations.js survived server/routes/projects.js
```

Output:
```json
[
  {
    "id": "346",
    "line": 75,
    "column": 10,
    "mutatorName": "EqualityOperator",
    "replacement": "col <= dateRow.length"
  },
  ...
]
```

#### `by-type <file>`
Group survived mutants by mutator type.

```bash
node analyze-mutations.js by-type server/utils/dateUtils.js
```

Output:
```json
{
  "EqualityOperator": [
    { "id": "346", "line": 75, "replacement": "col <= dateRow.length" }
  ],
  "ConditionalExpression": [
    { "id": "352", "line": 78, "replacement": "false" }
  ],
  ...
}
```

#### `by-line <file> <line>`
Get all mutants at a specific line number.

```bash
node analyze-mutations.js by-line server/services/cacheService.js 45
```

Output:
```json
[
  {
    "id": "123",
    "status": "Killed",
    "mutatorName": "ConditionalExpression",
    "replacement": "true",
    "line": 45,
    "column": 10
  }
]
```

#### `high-priority <file>`
Categorize survived mutants by priority (high/medium/low).

```bash
node analyze-mutations.js high-priority server/services/googleSheetsApi.js
```

Output:
```json
{
  "high": [
    {
      "mutatorName": "EqualityOperator",
      "count": 3,
      "mutants": [...]
    }
  ],
  "medium": [...],
  "low": [...]
}
```

### Priority Levels

- **High**: ConditionalExpression, LogicalOperator, EqualityOperator
  - These reveal critical logic flaws

- **Medium**: ArithmeticOperator, ReturnStatement, BlockStatement, MethodExpression, OptionalChaining
  - Calculation and flow control issues

- **Low**: StringLiteral, ObjectLiteral, etc.
  - Often acceptable edge cases

### Environment Variables

- `MUTATION_REPORT`: Custom path to mutation.json (default: `reports/mutation/mutation.json`)

```bash
MUTATION_REPORT=custom/path/report.json node analyze-mutations.js summary myfile.js
```

### Using as a Module

```javascript
import { getSummary, groupByType, loadReport, findFileData } from './analyze-mutations.js';

const report = loadReport('reports/mutation/mutation.json');
const { data } = findFileData(report, 'server/services/myService.js');
const summary = getSummary(data);
const grouped = groupByType(data);
```

## Benefits

- **Fast**: Loads entire report once, filters efficiently
- **Clean output**: JSON format for easy parsing
- **Reusable**: Use standalone or import as module
- **Handles large files**: Processes 640KB+ reports that exceed Read tool limits
- **Flexible matching**: Finds files by partial path match

## Examples in the Wild

Used by the `/improve-test-quality` skill to:
1. Baseline analysis (get current mutation score)
2. Identify survived mutants to target
3. Categorize by priority for systematic improvement
4. Verify improvements after re-running tests
