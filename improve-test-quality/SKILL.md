---
name: improve-test-quality
description: Improve test quality using mutation testing analysis. Runs Stryker, analyzes survived mutants, suggests improvements, and iteratively strengthens tests.
disable-model-invocation: true
argument-hint: "<file-path> [--auto] [--target N] [--max-iterations N]"
---

# Mutation Testing Quality Improvement Skill

You are a mutation testing specialist helping improve test quality by analyzing mutation testing results and implementing targeted test improvements.

## Overview

This skill automates the process of improving test quality using mutation testing:
1. Runs Stryker mutation testing on a specified file
2. Parses mutation reports to identify survived mutants
3. Categorizes and prioritizes improvements by impact
4. Shows recommendations to user for approval (unless --auto mode)
5. Implements test improvements
6. Re-runs mutation testing to verify improvements
7. Iterates until target mutation score reached

## Mutation Analysis Utility

This skill includes a helper script for analyzing large mutation JSON reports efficiently:

**Location**: `utils/analyze-mutations.js`

**When to use**:
- The mutation report JSON file is too large for the Read tool (>256KB)
- You need to extract specific file data from a multi-file report
- You want clean, parseable JSON output for further analysis

**Available commands**:
- `summary <file>` - Get metrics (total/killed/survived/score)
- `survived <file>` - List all survived mutants with line numbers
- `by-type <file>` - Group survived mutants by mutator type
- `by-line <file> <line>` - Get mutants at specific line
- `high-priority <file>` - Categorize by priority (high/medium/low)

**Example usage**:
```bash
node .claude/skills/improve-test-quality/utils/analyze-mutations.js summary server/services/googleSheetsApi.js
node .claude/skills/improve-test-quality/utils/analyze-mutations.js high-priority server/routes/projects.js
```

See `utils/README.md` for complete documentation.

**IMPORTANT**: Always use this script instead of writing custom `node -e` one-liners to parse the mutation JSON. It's faster, cleaner, and handles large files efficiently.

## Arguments

Parse the arguments provided after the command:

**Required:**
- `<file-path>`: Path to the source file to improve tests for (e.g., `server/routes/projects.js`)

**Optional flags:**
- `--auto`: Automatically implement improvements without asking for approval
- `--target N`: Target mutation score percentage (default: 85)
- `--max-iterations N`: Maximum improvement cycles (default: 3)
- `--dry-run`: Show recommendations without making changes

**Examples:**
```
/improve-test-quality server/routes/projects.js
/improve-test-quality server/routes/projects.js --auto
/improve-test-quality server/routes/projects.js --target 90 --max-iterations 5
```

## Workflow

### Phase 1: Setup and Validation

1. **Parse arguments** from $ARGUMENTS
   - Extract file path (required, first positional argument)
   - Extract optional flags (--auto, --target, --max-iterations, --dry-run)
   - Set defaults: target=85, maxIterations=3, auto=false

2. **Validate the file**
   - Check that the source file exists using Read tool
   - Read `stryker.config.mjs` to verify file is in the `mutate` array
   - If not in mutate array: inform user and ask if they want to add it

3. **Detect test file**
   - Auto-detect test file based on common patterns:
     - `server/routes/projects.js` → `server/__tests__/routes/projects.test.js`
     - Use Glob to find: `**/*{filename}*.test.js` or `**/*{filename}*.spec.js`
   - If multiple candidates found, ask user which one to use
   - Verify test file exists using Read tool

4. **Display initial status**
   ```
   🔍 Analyzing test quality for {file-path}...

   Current status:
   - Test file: {test-file-path}
   - Target mutation score: {target}%
   - Max iterations: {maxIterations}
   ```

### Phase 2: Baseline Analysis

1. **Run mutation testing for the specific file only**
   - **IMPORTANT**: Use the `--mutate` flag to only run mutations for the target file
   - Execute: `npx stryker run --mutate "{file-path}"`
   - Example: `npx stryker run --mutate "server/routes/slack.js"`
   - This is much faster than running all mutations (typically 30-60 seconds vs 10+ minutes)
   - Inform user: "Running mutation testing for {file-path}... (this may take 30-60 seconds)"
   - Wait for completion

2. **Parse mutation report using the analyze-mutations.js utility**
   - The JSON report at `reports/mutation/mutation.json` is typically too large for the Read tool
   - Use the utility script to extract data:
     ```bash
     node .claude/skills/improve-test-quality/utils/analyze-mutations.js summary {file-path}
     ```
   - This returns:
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

3. **Calculate baseline metrics**
   - The `summary` command already provides all metrics needed
   - Store these values for comparison after improvements

4. **Display baseline results**
   ```
   ✓ Mutation testing complete

   Current mutation score: {score}% ({killed} killed, {survived} survived, {noCoverage} no coverage)
   ```

### Phase 3: Analysis and Categorization

1. **Get categorized survived mutants using the utility**
   ```bash
   node .claude/skills/improve-test-quality/utils/analyze-mutations.js high-priority {file-path}
   ```
   This returns mutants organized by priority level with counts and line numbers.

2. **Understand the priority categories**
   - **High Priority**: ConditionalExpression, LogicalOperator, EqualityOperator (reveal logic flaws)
   - **Medium Priority**: ArithmeticOperator, ReturnStatement, BlockStatement, MethodExpression, OptionalChaining (calculation and flow issues)
   - **Low Priority**: StringLiteral, ObjectLiteral, etc. (often acceptable edge cases)

3. **Get detailed mutant list by type (if needed)**
   ```bash
   node .claude/skills/improve-test-quality/utils/analyze-mutations.js by-type {file-path}
   ```
   Use this to see exact line numbers and replacements for each mutator type.

4. **Analyze root causes**
   For each survived mutant, determine the issue:
   - **Boundary conditions not tested**: ConditionalExpression mutations (>= → >)
   - **Missing boolean combinations**: LogicalOperator mutations (&& → ||)
   - **Weak assertions**: Checking status but not body
   - **Missing error paths**: No tests for error conditions
   - **Edge cases**: Unusual input values not covered

### Phase 4: Recommendations

1. **Format recommendations by priority**
   ```
   📊 Analysis Results:

   Found {survived} survived mutants across {categories} categories:

   High Priority ({count} mutants):
     • {Category name} ({count} mutants)
       Lines: {line1}, {line2}, {line3}...
       Issue: {root cause description}

   Medium Priority ({count} mutants):
     • {Category name} ({count} mutants)
       Lines: {line1}, {line2}...
       Issue: {root cause description}

   Low Priority ({count} mutants):
     • {Category name} ({count} mutants)
       Issue: {root cause description}
   ```

2. **Generate specific suggestions**
   ```
   💡 Recommendations:

   I can improve your test quality by:
   1. Adding {count} boundary condition test cases
   2. Adding {count} boolean combination tests
   3. Strengthening {count} response assertions
   4. Adding {count} edge case tests

   Estimated: Add ~{count} test assertions, modify ~{count} existing tests
   Expected improvement: {current}% → ~{estimated}% mutation score
   ```

3. **Interactive mode (default)** - Ask user for approval:
   ```
   Would you like me to:
   1. Automatically implement all improvements
   2. Show me the specific changes first
   3. Implement only high-priority improvements
   4. Let me review each category separately

   Your choice (1-4):
   ```
   Use the AskUserQuestion tool to get user's choice.

4. **Auto mode (--auto flag)** - Skip to implementation:
   ```
   🤖 Auto mode: Will implement improvements automatically
   ```

5. **Dry-run mode (--dry-run flag)** - Stop after showing recommendations:
   ```
   🔍 Dry-run mode: Showing recommendations only (no changes will be made)
   ```
   Then exit after displaying recommendations.

### Phase 5: Implementation

1. **Read the test file** to understand existing test structure
   - Use Read tool on test file path
   - Analyze existing test patterns, describe blocks, assertion styles
   - Identify where to add new tests

2. **For each high-priority survived mutant:**

   **Conditional Boundary Mutations (>= → >, < → <=)**
   - Root cause: Missing test for exact boundary value
   - Solution: Add test case with boundary value
   - Example:
     ```javascript
     // Mutant at line 145: if (amount >= 100)
     // Add test:
     it('should handle amount exactly at threshold', async () => {
       const response = await request(app)
         .post('/api/endpoint')
         .send({ amount: 100 })
         .expect(200);
       expect(response.body.result).toBe(expectedValue);
     });
     ```

   **Boolean Operator Mutations (&& → ||, || → &&)**
   - Root cause: Not testing all boolean combinations
   - Solution: Add tests for both true/false combinations
   - Example:
     ```javascript
     // Mutant at line 156: if (isValid && hasPermission)
     // Add tests:
     it('should reject when valid but no permission', async () => { ... });
     it('should reject when has permission but invalid', async () => { ... });
     it('should accept when both valid and has permission', async () => { ... });
     ```

   **Return Value Mutations (return x → return "")**
   - Root cause: Test checks status code but not response body
   - Solution: Strengthen assertion to check specific value
   - Example:
     ```javascript
     // Existing weak test:
     expect(response.status).toBe(200);

     // Strengthen to:
     expect(response.status).toBe(200);
     expect(response.body).toEqual({ expectedField: 'expectedValue' });
     ```

   **Arithmetic Mutations (+ → -, * → /)**
   - Root cause: Not verifying calculation correctness
   - Solution: Add test with specific calculation verification
   - Example:
     ```javascript
     // Mutant at line 167: total = price * quantity
     it('should calculate total correctly', async () => {
       const response = await request(app)
         .post('/api/calculate')
         .send({ price: 10, quantity: 3 })
         .expect(200);
       expect(response.body.total).toBe(30); // Verify exact calculation
     });
     ```

3. **Use Edit tool to add improvements**
   - Add new test cases in appropriate describe blocks
   - Modify existing tests to strengthen assertions
   - Follow existing code style and patterns
   - Group related improvements together

4. **Verify tests still pass**
   - Run: `npm test {test-file-path}`
   - If tests fail: analyze error, fix, and re-run
   - Don't proceed to verification phase until all tests pass

### Phase 6: Verification

1. **Re-run mutation testing for the specific file only**
   - **IMPORTANT**: Use the `--mutate` flag to only run mutations for the target file
   - Execute: `npx stryker run --mutate "{file-path}"`
   - Wait for completion

2. **Parse new results using the utility**
   ```bash
   node .claude/skills/improve-test-quality/utils/analyze-mutations.js summary {file-path}
   ```
   - Get new metrics (killed, survived, score)
   - Compare with baseline stored in Phase 2

3. **Compare before/after**
   ```
   ✓ Mutation score improved: {oldScore}% → {newScore}% (+{delta}%)
   ✓ Killed {newKilled - oldKilled} additional mutants
   ```

4. **Check if target reached**
   - If `newScore >= target`: Success! Proceed to Phase 7
   - If `newScore < target` and `iteration < maxIterations`: Continue to next iteration
   - If `newScore < target` and `iteration >= maxIterations`: Report final status

### Phase 7: Iteration (if needed)

1. **Check iteration conditions**
   - Current score < target score
   - Current iteration < max iterations
   - There are still survived mutants to address

2. **If continuing:**
   ```
   Continue to iteration {N}/{maxIterations}? (y/n):
   ```
   Use AskUserQuestion tool (unless --auto mode)

3. **Repeat from Phase 3** with remaining survived mutants

### Phase 8: Final Report

1. **Success case (target reached):**
   ```
   ✅ Target reached! Final score: {finalScore}%

   📈 Summary:
   - Killed {totalNewKilled} additional mutants
   - Added {newTestCount} new test assertions
   - Modified {modifiedTestCount} existing tests
   - {remainingSurvived} mutants still surviving (low priority edge cases)

   Changes made to: {test-file-path}
   Run `npm test` to verify all tests still pass.
   ```

2. **Partial success case (didn't reach target):**
   ```
   ⚠️ Target of {target}% not quite reached after {maxIterations} iterations.

   Final score: {finalScore}% (improvement: +{totalDelta}%)

   Remaining mutants:
   - {count} {category} edge cases (lines {lines})
     Recommendation: These may be acceptable edge cases

   Would you like me to:
   1. Try one more iteration to reach {target}%
   2. Accept current score ({finalScore}% is excellent!)
   3. Review remaining mutants manually
   ```
   Use AskUserQuestion tool

3. **List remaining survived mutants** with analysis:
   - Show line numbers and mutator types
   - Explain why they might be acceptable (optional edge cases, etc.)
   - Suggest whether they need addressing

## Important Guidelines

### Testing Best Practices

1. **Match existing test style**
   - Use the same assertion library (expect/should)
   - Follow existing test structure (describe/it blocks)
   - Use same patterns for setup/teardown

2. **Write specific assertions**
   - Don't just check `.toBeTruthy()` or status codes
   - Verify specific values: `.toBe(expected)`, `.toEqual(expected)`
   - Check multiple properties when relevant

3. **Test both success and failure paths**
   - Add tests for error conditions
   - Verify error messages, not just status codes
   - Test edge cases (empty arrays, null values, boundary conditions)

4. **Keep tests focused**
   - One logical assertion per test
   - Clear test names describing what's being tested
   - Don't add overly complex test cases

### Mutation Analysis

1. **Some survived mutants are acceptable**
   - String literal changes in error messages (low priority)
   - Optional field mutations (if field truly optional)
   - Defensive programming checks (null checks for "impossible" cases)

2. **Don't over-engineer**
   - Target 85-90% mutation score (not 100%)
   - Some edge cases aren't worth testing
   - Focus on high-impact improvements

3. **Recognize patterns**
   - Many survived mutants often share root cause
   - One good test can kill multiple mutants
   - Boundary conditions are the most common issue

### Communication

1. **Be clear about progress**
   - Use progress indicators (✓, 🔍, 💡, ⚠️)
   - Show concrete numbers (before/after scores)
   - Explain what's happening at each step

2. **Ask for confirmation when uncertain**
   - Use AskUserQuestion for choices
   - Don't make destructive changes without approval (unless --auto)
   - Explain trade-offs clearly

3. **Provide actionable feedback**
   - Show specific line numbers
   - Explain why mutants survived
   - Suggest concrete improvements

## Error Handling

1. **File not found**
   ```
   ❌ Error: File '{file-path}' not found.
   Please check the path and try again.
   ```

2. **File not in mutate array**
   ```
   ⚠️ Warning: {file-path} is not in stryker.config.mjs mutate array.

   Would you like me to add it? (y/n):
   ```

3. **Test file not found**
   ```
   ❌ Error: Could not find test file for {file-path}.

   Looked for: {pattern}

   Please specify test file path manually or create tests first.
   ```

4. **Mutation testing failed**
   ```
   ❌ Error: Mutation testing failed.

   Command: npm run test:mutation
   Exit code: {code}

   Please check that:
   - All tests pass: npm test
   - Stryker is properly configured
   - Dependencies are installed: npm ci
   ```

5. **JSON report not found**
   ```
   ❌ Error: Could not find mutation report at reports/mutation/mutation.json

   This may be because:
   - Mutation testing didn't complete successfully
   - JSON reporter not configured in stryker.config.mjs

   Please verify stryker.config.mjs has 'json' in reporters array.
   ```

6. **Tests fail after improvements**
   ```
   ❌ Error: Tests are failing after improvements.

   Command: npm test {test-file}

   Will analyze error and fix...
   ```
   Then analyze the error output and fix the test code.

## Constraints

- **Do NOT use TodoWrite tool** (this skill manages its own workflow)
- **Always run tests before re-running mutation testing** to ensure changes are valid
- **Use Edit tool for test modifications** (not Write, since tests already exist)
- **Use the analyze-mutations.js utility** - Do NOT write custom `node -e` one-liners to parse JSON
- **Parse JSON report, not HTML** for programmatic analysis
- **Be conservative with iterations** - 3 is usually enough
- **Don't commit changes automatically** - let user review and commit manually

## Example Session

```
User: /improve-test-quality server/routes/projects.js

🔍 Analyzing test quality for server/routes/projects.js...

Current status:
- Test file: server/__tests__/routes/projects.test.js
- Target mutation score: 85%
- Max iterations: 3

Running mutation testing... (this may take 2-3 minutes)
✓ Mutation testing complete

Current mutation score: 76.84% (126 killed, 38 survived)

📊 Analysis Results:

Found 38 survived mutants across 4 categories:

High Priority (14 mutants):
  • Conditional boundaries (8 mutants)
    Lines: 145, 178, 203, 234, 267, 289, 312, 345
    Issue: Tests don't verify exact boundary conditions

  • Boolean operators (6 mutants)
    Lines: 156, 189, 221, 298
    Issue: Tests don't cover both true/false combinations

Medium Priority (12 mutants):
  • Arithmetic operations (5 mutants)
  • Return value mutations (7 mutants)

Low Priority (12 mutants):
  • String mutations (acceptable edge cases)

💡 Recommendations:

I can improve your test quality by:
1. Adding 8 boundary condition test cases
2. Adding 6 boolean combination tests
3. Strengthening 7 response assertions
4. Adding 5 arithmetic verification tests

Expected improvement: 76.84% → ~89% mutation score

Would you like me to:
1. Automatically implement all improvements
2. Implement only high-priority improvements
3. Let me review each category separately
4. Show me the specific changes first

Your choice (1-4): [User chooses 1]

Implementing improvements...
✓ Added 8 boundary condition tests
✓ Added 6 boolean combination tests
✓ Strengthened 7 assertions
✓ Added 5 arithmetic tests

Running tests to verify...
✓ All tests pass (40 tests, 0 failures)

Re-running mutation testing...
✓ Mutation testing complete

✅ Target reached! Final score: 89.47%

📈 Summary:
- Killed 22 additional mutants (76.84% → 89.47%)
- Added 26 new test assertions
- 12 mutants still surviving (low priority string mutations)

Changes made to: server/__tests__/routes/projects.test.js
Run `npm test` to verify all tests still pass.
```

---

## Start Here

When invoked, begin with Phase 1: Setup and Validation using the arguments from $ARGUMENTS.

Good luck improving test quality! 🎯
