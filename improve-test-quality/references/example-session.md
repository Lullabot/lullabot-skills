# Example mutation-testing session

Illustrative output only; actual scores and counts must come from the current report.


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
