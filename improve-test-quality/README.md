# Improve Test Quality Skill

A Claude Code slash command skill that automates mutation testing analysis and test quality improvement.

## What It Does

This skill helps you improve test quality by:
1. Running Stryker mutation testing on a specific file
2. Analyzing survived mutants to identify weak spots in tests
3. Suggesting targeted test improvements
4. Implementing the improvements (with your approval)
5. Verifying improvements by re-running mutation testing
6. Iterating until target mutation score is reached

## Prerequisites

- Stryker mutation testing must be configured (`stryker.config.mjs`)
- The file you want to test must have existing tests
- JSON reporter must be enabled in Stryker config (already configured)

## Usage

### Basic Usage

```bash
/improve-test-quality server/routes/projects.js
```

This will:
- Run mutation testing on `server/routes/projects.js`
- Analyze survived mutants
- Show recommendations
- Ask for your approval before making changes
- Target 85% mutation score by default

### Auto Mode

```bash
/improve-test-quality server/routes/projects.js --auto
```

Automatically implements improvements without asking for approval at each step.

### Custom Target Score

```bash
/improve-test-quality server/routes/projects.js --target 90
```

Set a custom target mutation score (default is 85%).

### Limit Iterations

```bash
/improve-test-quality server/routes/projects.js --max-iterations 5
```

Set maximum number of improvement cycles (default is 3).

### Dry Run

```bash
/improve-test-quality server/routes/projects.js --dry-run
```

Show recommendations without making any changes.

### Combining Options

```bash
/improve-test-quality server/routes/projects.js --auto --target 90 --max-iterations 5
```

## Workflow

1. **You:** Write initial tests to get ~60-70% coverage
2. **You:** Run `/improve-test-quality <file-path>`
3. **Skill:** Runs mutation testing and analyzes results
4. **Skill:** Shows you recommendations categorized by priority
5. **You:** Approve improvements (or skill auto-implements with `--auto`)
6. **Skill:** Adds test cases and strengthens assertions
7. **Skill:** Re-runs mutation testing to verify
8. **Skill:** Reports improvement (e.g., "76% → 89%")
9. **Repeat** if target not reached and iterations remaining

## What Gets Improved

The skill targets common mutation testing issues:

### High Priority
- **Boundary conditions**: Tests for exact threshold values (>= vs >)
- **Boolean combinations**: Tests for all true/false combinations (&& vs ||)
- **Weak assertions**: Strengthens status-only checks to verify response bodies

### Medium Priority
- **Arithmetic operations**: Verifies calculation correctness (+ vs -)
- **Return values**: Checks specific return values, not just truthiness
- **Block statements**: Tests both branches of conditionals

### Low Priority
- **String literals**: Often acceptable edge cases
- **Optional fields**: May not need testing if truly optional

## Example Session

```bash
$ /improve-test-quality server/routes/projects.js

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

Your choice (1-4): 1

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

## Benefits

- **Time savings**: 1-2 hours of manual work → 10 minutes mostly automated
- **Better insights**: AI understands mutation patterns and suggests targeted fixes
- **Higher quality**: Systematic approach catches edge cases you might miss
- **Learning tool**: See patterns in mutation testing and improve your testing skills
- **Consistency**: Same high standard applied across all files

## Limitations

- Requires Stryker mutation testing to be configured
- Works best with files that already have 60%+ test coverage
- Targets 85-90% mutation score (100% is rarely necessary or practical)
- Some survived mutants may be acceptable edge cases
- Mutation testing is slow (2-3 minutes per run)

## Tips

1. **Start with good coverage**: Get to 60-70% line coverage before using this skill
2. **Review changes**: Even in auto mode, review the changes before committing
3. **Iterate carefully**: 85-90% is usually sufficient; don't chase 100%
4. **Commit frequently**: Commit after each successful improvement cycle
5. **Learn patterns**: Pay attention to what mutants survive to improve your testing habits

## Troubleshooting

### "File not in mutate array"
The skill will offer to add the file to `stryker.config.mjs` for you.

### "Test file not found"
Make sure your test file follows conventions:
- `server/routes/file.js` → `server/__tests__/routes/file.test.js`

### "Mutation testing failed"
Ensure all tests pass first: `npm test`

### "JSON report not found"
The skill configuration should have already added the JSON reporter to `stryker.config.mjs`.

## Configuration

The skill uses these defaults (overridable with flags):
- Target mutation score: 85%
- Max iterations: 3
- Mode: Interactive (ask before implementing)

## Files Modified

This skill may modify:
- Your test file (adds tests, strengthens assertions)
- `stryker.config.mjs` (if file not in mutate array)

It will NOT:
- Modify your source code
- Commit changes automatically (you control commits)
- Run in CI/CD (it's a development tool)

## Future Enhancements

Potential future features:
- Multi-file support
- Git auto-commit with descriptive messages
- Coverage improvement suggestions
- CI/CD integration recommendations
- Learning from past improvements

## See Also

- [Stryker Mutation Testing](https://stryker-mutator.io/)

