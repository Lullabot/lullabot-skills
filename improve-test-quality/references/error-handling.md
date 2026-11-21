# Mutation testing error handling

Use these examples to report actual failures. Missing dependencies require separate reviewed setup; do not install them automatically.


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
