# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## MANDATORY VALIDATION PROTOCOL

**CRITICAL**: Being "nice" by not challenging ideas WASTES user time and money. Harsh validation is kindness.

Before ANY plan or implementation:

1. Use sequential thinking to challenge EVERY step against KISS/YAGNI, Ultra-Think on this
2. Reason EVERY step explicitly against what value add is provided. If you cannot reason a specific value add, it is not needed
3. Show certainty percentage - KILL anything <95% certain
4. KILL all "nice to have" features - only build what's needed NOW
5. When user requests a feature/change that lacks clear scope:
   - SUGGEST: "This could benefit from PRP structure. Shall I run TINA clarification to prevent scope creep?"
   - Use Claude command `/prp-step0-clarify_intent` if accepted

**Remember**: Every unchallenged complexity costs 100x more to fix later.

## ADR vs PRP Guidelines

### When to use ADR (Architecture Decision Record)

- Significant technical choices affecting system structure
- Technology selection (frameworks, databases, patterns)
- Cross-cutting concerns (security, performance strategies)
- Design constraints and principles
- Focus: WHY and WHAT decisions

### When to use PRP (Product Requirements Process)

- Feature implementation planning
- Migration and refactoring tasks
- Step-by-step execution plans
- Resource allocation and timelines
- Focus: HOW and WHEN to implement

### MANDATORY: Keep them separate

- ADRs are immutable decision records
- PRPs are living implementation documents
- ADR references PRP for implementation
- PRP references ADR for rationale
- When in doubt: "Is this architectural (ADR) or tactical (PRP)?"

### Available Commands

- Use `/adr-creator` for architectural decisions
- Use `/prp-step0-clarify_intent` for implementation planning

## Documentation Maintenance

**MANDATORY** when changing structure:

- Delete/move directories → Update README.md Project Structure tree
- Delete/move files → Check README.md for broken links
- Otherwise → Don't touch documentation

## Two Golden Rules - MANDATORY WORKING PRINCIPLE

- **KISS – Keep It Simple, Stupid:**
  Use the **easiest** way that works. Fewer parts. Short words. Short functions.
- **YAGNI – You Aren’t Gonna Need It:**
  Don’t build extra stuff “just in case.” Build it **only** when someone actually needs it **now**.

## How to Work (tiny steps)

1. **Say the goal in one short sentence.**
   “I need a function that adds two numbers.”
2. **Pick the simplest path.**
   Use built-in tools first. No new library unless there’s a clear, current need.
3. **Make a tiny plan (3 steps max).**
   List the steps in plain words.
4. **Build the smallest piece that solves today’s need.**
5. **Test with one tiny example.**
   If it works, you’re done. If not, fix the smallest thing.
6. **Show the result and the test.**
7. **Stop.** Don’t add features unless asked.

## Design Rules (think like toy blocks)

- One function = **one job**. Keep it short and clear.
- Prefer simple data (numbers, strings, lists, dicts) over fancy patterns.
- Name things so a child can guess what they do.
- Names should explain "what" not "how" (getUserById not fetchUserFromDatabase).
- Avoid clever tricks. Clear beats clever.
- No general frameworks, layers, or abstractions until they're truly needed.

## YAGNI Guardrails (when to say “not now”)

- ❌ “Maybe we’ll need logging, caching, plugins, or config later.”
  ✅ “Add it only when the current task requires it.”
- ❌ “Let’s support every edge case.”
  ✅ “Handle the cases we actually have.”
- ❌ "Let's make it super fast first."
  ✅ "Make it correct and simple. Optimize only if it's too slow **now**."
- ✅ "Found a small bug while working? Fix it now (Boy Scout Rule)"

## KISS Checks (quick self-test)

- Can you explain the code in **one breath**? If not, simplify.
- More than **3 moving parts**? Split or remove one.
- Needs a new library? Prove the built-in won’t do.
- A loop + an if is fine; a maze of patterns is not.

## Tiny Examples

**KISS (Good):**

```py
def add(a, b):
    return a + b
# test
assert add(2, 3) == 5
```

Not KISS (Too fancy):

```py
class Adder:
def **init**(self, strategy=None): ...
```

## Unneeded classes/strategy for simple addition

## YAGNI (Good)

- “We only need CSV read? Use Python’s csv module.”

## Not YAGNI (Too much)

- “Let’s build a full data pipeline with plugins, caching, and a dashboard”—when we only need to read one CSV once.

## When You're Stuck (Systematic Debug)

1. **Reproduce**: Create minimal failing test case
2. **Gather**: Collect error messages and context
3. **Hypothesize**: Form ONE theory about the cause
4. **Test**: Change ONE thing, verify result
5. **Binary Search**: Eliminate half the problem space each step

If still stuck:

- Make it smaller. Ship a slice that works.
- Remove one part and try again.
- Write the test first, then the smallest code to pass it.

**Remember:** Small + clear + working now > big + clever + maybe useful later.

## GitHub Claude Review Integration

**MANDATORY**: When assisting with git operations, always surface GitHub review options without forcing them.

### When to Mention GitHub Claude Review

1. **During Commits** (`/smart-commit`):
   - Run local security tests first (fast feedback)
   - Show GitHub review commands for comprehensive validation
   - Let user decide timing (now vs after PR)

2. **After PR Creation** (`/create-pull-request`):
   - Always provide copy-paste @claude commands
   - Offer comprehensive and focused review options
   - Reference our ADRs and KISS/YAGNI principles

3. **In General Dialogue**:
   - When user says "pushed changes" → mention PR enables GitHub review
   - When user asks "is this ready?" → suggest both local tests and GitHub validation
   - For releases → recommend both local AND GitHub comprehensive review

### GitHub Review Command Templates

**Comprehensive:**
`@claude Please review this PR comprehensively for security, KISS/YAGNI compliance, and architectural alignment`

**Security Focus:**
`@claude Review for security vulnerabilities and safety`

**Architectural:**
`@claude Check adherence to ADR-001 through ADR-005`

**Quick:**
`@claude Quick review please`

### Integration Guidelines

- **Always provide options, never force**
- **Local first for speed, GitHub for comprehensiveness**
- **Show exact commands to copy-paste**
- **Mention benefits: security validation, KISS/YAGNI compliance, ADR adherence**
- **Respect user choice - some prefer local, some prefer GitHub delegation**

This ensures comprehensive validation options are always available without adding complexity to the workflow.
