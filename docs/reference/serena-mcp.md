# Serena MCP Integration

**Serena** is a semantic coding MCP (Model Context Protocol) server that provides intelligent code understanding and manipulation tools. This boilerplate integrates with serena-mcp to enable sophisticated codebase analysis and maintenance.

## Overview

Serena-mcp transforms how Claude Code interacts with codebases by providing:

- **Semantic Code Understanding**: Navigate code by symbols, not just text
- **Intelligent File Operations**: Search and manipulate code based on structure
- **Memory System**: Persistent knowledge about project architecture
- **Token-Efficient Reading**: Read only what's needed, when needed

## Key Capabilities

### Symbol-Based Navigation

Instead of reading entire files, serena enables precise symbol targeting:

```bash
# Find a specific class method
find_symbol "UserService/authenticate"

# Get class overview without implementation details
find_symbol "UserService" depth=1 include_body=false

# Find all references to a function
find_referencing_symbols "validateInput" relative_path="src/utils.py"
```

### Smart Code Search

Pattern-based searching with context awareness:

```bash
# Search for regex patterns with file type filtering
search_for_pattern "async def.*login" paths_include_glob="**/*.py"

# Restrict search to specific directories
search_for_pattern "class.*Controller" relative_path="src/controllers"
```

### Project Memory

Serena maintains persistent memory about your codebase:

```bash
# Store architectural decisions
write_memory "authentication_flow" "JWT tokens with refresh mechanism"

# Retrieve project knowledge
read_memory "database_schema"

# List available memories
list_memories
```

### Intelligent File Operations

Structure-aware file exploration:

```bash
# Get high-level overview of file symbols
get_symbols_overview "src/main.py"

# Recursive directory listing
list_dir "src" recursive=true

# Find files by pattern
find_file "*.test.js" "tests"
```

## Integration with Claude Code

### Command Integration

The `prime_tts.md` command specifically leverages serena:

```markdown
- Run `serena`-mcp to understand the codebase structure and file organization
- Code Index and Memory: `serena`-MCP
```

### Boilerplate Maintenance

Serena enables this boilerplate to maintain itself through:

1. **Structure Analysis**: Understanding file organization patterns
2. **Documentation Sync**: Keeping docs aligned with code changes
3. **Pattern Detection**: Identifying architectural inconsistencies
4. **Automated Refactoring**: Structure-aware code modifications

## Best Practices

### Efficient Code Reading

**DO:**

```bash
# Start with overview
get_symbols_overview "complex_file.py"

# Then target specific symbols
find_symbol "ComplexClass/important_method" include_body=true
```

**DON'T:**

```bash
# Avoid reading entire large files unless necessary
read_file "large_implementation.py"  # Use sparingly
```

### Memory Management

**Store Important Context:**

- Architectural decisions
- Complex business logic explanations
- Integration patterns
- Performance considerations

**Example Memory Entries:**

```bash
write_memory "api_design" "REST endpoints follow OpenAPI 3.0 spec with JWT auth"
write_memory "testing_strategy" "Unit tests with pytest, integration with testcontainers"
```

### Search Optimization

**Use Specific Patterns:**

```bash
# Good: Specific and targeted
search_for_pattern "class.*Service" paths_include_glob="src/**/*.py"

# Better: Even more targeted
search_for_pattern "class.*Service" relative_path="src/services"
```

## Configuration

### Project Setup

Serena requires the `.serena/` directory for project-specific configuration and memories:

```text
.serena/
├── memories/           # Project knowledge storage
├── config.json        # Serena-specific settings
└── patterns/          # Custom search patterns
```

### Memory Organization

Organize memories by domain:

- `architecture_*`: High-level system design
- `patterns_*`: Code patterns and conventions
- `integration_*`: External service integrations
- `performance_*`: Optimization insights
- `security_*`: Security implementations

## Troubleshooting

### Common Issues

**Symbol Not Found:**

- Check symbol name path syntax: `Class/method` not `Class.method`
- Use `substring_matching=true` for partial matches
- Verify file is in searchable location

**Memory Access:**

- Ensure `.serena/memories/` directory exists
- Check memory file naming conventions
- Verify write permissions

**Search Performance:**

- Use `relative_path` to narrow scope
- Apply appropriate `paths_include_glob` filters
- Prefer symbol-based over pattern-based search when possible

## Advanced Usage

### Custom Search Patterns

Create reusable search patterns for common code structures:

```bash
# Find all API endpoints
search_for_pattern "@app\.route\(.*\)" paths_include_glob="**/*.py"

# Locate database models
search_for_pattern "class.*Model.*:" paths_include_glob="models/**/*.py"
```

### Integration Workflows

**New Feature Development:**

1. `list_memories` - Review existing architecture
2. `search_for_pattern` - Find similar implementations
3. `find_symbol` - Understand integration points
4. `write_memory` - Document new patterns

**Bug Investigation:**

1. `find_referencing_symbols` - Trace usage patterns
2. `search_for_pattern` - Look for similar issues
3. `get_symbols_overview` - Understand context
4. `write_memory` - Document solution

**Refactoring:**

1. `find_symbol` - Identify target structures
2. `find_referencing_symbols` - Map dependencies
3. `search_for_pattern` - Find affected code
4. Use symbolic editing tools for precise changes

This integration makes serena-mcp a powerful tool for maintaining and evolving the cc-boilerplate itself, enabling intelligent automation and reducing manual maintenance overhead.
