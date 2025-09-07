---
name: commit
description: Analyze changes and create a smart git commit
arguments: "Additional instructions for the commit"
---

additional instructions = $ARGUMENTS

type = "feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"

# Smart Git CommitPRPs/ai_docs

Please help me create a git commit by:

1. First, check the current git status and analyze what changed:

```bash
git status
git diff --staged
```

2. If no files are staged, show me the changes and help me decide what to stage:

```bash
git diff
git status -s
```

3. Based on the changes, suggest:

- The appropriate commit type (feat/fix/docs/style/refactor/perf/test/chore)
- A concise, descriptive commit message following conventional commits
- If the changes are complex, suggest breaking into multiple commits

4. The commit format should be:

$type: description for simple commits
For complex changes, include a body explaining what and why

5. After showing me the suggested commit message, ask if I want to:

- Use it as-is
- Modify it
- Add more details to the body
- Stage different files

6. Before committing, run quick local validation:

```bash
# Security validation (required per workflow)
python tests/test_safety_hooks.py

# Optional: Run basic tests
./scripts/run_tests.sh
```

If tests pass: ✅ Local checks completed

**GitHub Review Options**: After creating PR, you can request comprehensive review:

```text
@claude Review this commit for security vulnerabilities and KISS/YAGNI compliance
```

Or for specific areas:

```text
@claude Check this change for potential security issues
@claude Validate this follows our architectural decisions (ADRs)
```

7. Once approved and checks pass, create the commit and show me the result.

8. Finally, ask if I want to:

- Push now (enables GitHub review after PR)
- Create PR immediately (for GitHub Claude review)
- Stay local for more changes
