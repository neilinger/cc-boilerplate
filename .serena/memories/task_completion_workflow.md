# Task Completion Workflow

## When Task is Completed

1. **Test the Implementation**
   ```bash
   # Run any relevant tests
   uv run test_script.py  # If tests exist
   python -m pytest      # If using pytest
   ```

2. **Validate Hook Functionality** 
   ```bash
   # Check hook logs for proper execution
   cat logs/user_prompt_submit.json | jq '.'
   cat logs/pre_tool_use.json | jq '.'
   cat logs/post_tool_use.json | jq '.'
   ```

3. **Code Quality Checks**
   - Follow KISS/YAGNI principles
   - Ensure functions do one job only
   - Verify error handling is graceful
   - Check that names are descriptive

4. **Git Operations** (using gh CLI as required)
   ```bash
   git status
   git add .
   git commit -m "descriptive commit message"
   gh pr create --title "Title" --body "Description"
   ```

5. **Documentation Updates** (only if structure changed)
   - Update README.md project structure if directories added/removed
   - Check for broken links if files moved/deleted
   - Don't create documentation unless explicitly requested

6. **Environment Cleanup**
   - No virtual environments to manage (UV handles dependencies)
   - Check that sensitive data isn't committed
   - Verify .gitignore covers logs and temporary files

## Quality Gates
- Code must pass KISS test: explainable in one breath
- No more than 3 moving parts per function
- Must handle errors gracefully without blocking core functionality
- All hook scripts must be UV-compatible with embedded dependencies