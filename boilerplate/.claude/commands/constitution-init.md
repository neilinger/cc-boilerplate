# Constitution Initialization Command

## Purpose

Initialize a project-specific constitution by analyzing existing governance patterns and synthesizing them into spec-kit compatible constitutional content.

## Usage

```bash
/constitution-init
```

## Implementation

This command analyzes existing project governance patterns from:

1. **CLAUDE.md** - KISS/YAGNI principles, agent orchestration, validation protocols
2. **ADRs** - Architectural decisions, especially ADR-007 (agent system) and ADR-008 (cognitive load allocation)
3. **README.md** - Project values, security features, and development standards
4. **PRPs/** - Product Requirements Process patterns and methodology

Then synthesizes these patterns into a complete constitution at `.specify/memory/constitution.md`.

## Expected Output

The command will:

1. **Analyze existing governance sources**
2. **Extract core principles** from documented patterns
3. **Generate project-specific constitution** with no placeholder tokens
4. **Validate constitutional completeness**
5. **Report synthesis results**

The generated constitution will reflect CC-Boilerplate's established governance while providing spec-kit integration capability.

## Agent Selection

**RECOMMENDATION**: Use `smart-doc-generator` agent for this task as it specializes in:
- Document analysis and synthesis
- Constitutional content generation
- Template population with extracted patterns
- Validation of documentation completeness

This agent has the appropriate tools and expertise for governance document creation.