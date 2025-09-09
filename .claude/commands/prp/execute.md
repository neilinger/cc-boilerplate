# Execute PRP - Feature Branch Implementation

## Arguments: PRP File Path

$ARGUMENTS

## Mission

Execute a PRP (Product Requirement Prompt) in a proper feature branch following Release Flow branching strategy.

**Workflow**: `feature/prp-{number}-{slug}` → `release/*` → `main`

## Implementation Process

### Step 1: Validate Environment

```bash
# Check we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "❌ Not in a Git repository"
    exit 1
fi

# Check git status is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  You have uncommitted changes:"
    git status --short
    echo ""
    echo "Please commit or stash changes before executing PRP"
    exit 1
fi

# Ensure we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  Currently on branch: $CURRENT_BRANCH"
    echo "PRP execution should start from main branch"
    echo ""
    read -p "Switch to main branch? (y/N): " SWITCH_MAIN
    if [[ "$SWITCH_MAIN" =~ ^[Yy]$ ]]; then
        git checkout main
        git pull origin main
    else
        echo "Proceeding on current branch: $CURRENT_BRANCH"
    fi
fi
```

### Step 2: Parse PRP File and Extract Details

```bash
# Validate PRP file exists
PRP_FILE="$ARGUMENTS"
if [[ -z "$PRP_FILE" ]]; then
    echo "❌ No PRP file specified"
    echo "Usage: /prp:execute PRPs/prp-XXX-feature-name.md"
    exit 1
fi

if [[ ! -f "$PRP_FILE" ]]; then
    echo "❌ PRP file not found: $PRP_FILE"
    exit 1
fi

echo "📋 Executing PRP: $PRP_FILE"

# Extract PRP number and title from filename
PRP_FILENAME=$(basename "$PRP_FILE")
PRP_NUMBER=$(echo "$PRP_FILENAME" | sed -n 's/prp-\([0-9]\{3\}\).*/\1/p')
PRP_SLUG=$(echo "$PRP_FILENAME" | sed -n 's/prp-[0-9]\{3\}-\(.*\)\.md/\1/p')

if [[ -z "$PRP_NUMBER" ]] || [[ -z "$PRP_SLUG" ]]; then
    echo "❌ Invalid PRP filename format"
    echo "Expected: prp-XXX-feature-name.md"
    exit 1
fi

FEATURE_BRANCH="feature/prp-$PRP_NUMBER-$PRP_SLUG"
echo "🌿 Feature branch: $FEATURE_BRANCH"
```

### Step 3: Create Feature Branch

```bash
# Check if branch already exists
if git show-ref --verify --quiet refs/heads/$FEATURE_BRANCH; then
    echo "⚠️  Branch $FEATURE_BRANCH already exists"
    echo ""
    read -p "Switch to existing branch? (y/N): " SWITCH_EXISTING
    if [[ "$SWITCH_EXISTING" =~ ^[Yy]$ ]]; then
        git checkout "$FEATURE_BRANCH"
        echo "✅ Switched to existing branch: $FEATURE_BRANCH"
    else
        echo "❌ Cancelled PRP execution"
        exit 1
    fi
else
    # Create and switch to new feature branch
    git checkout -b "$FEATURE_BRANCH"
    echo "✅ Created and switched to branch: $FEATURE_BRANCH"
fi
```

### Step 4: Display PRP Context

```bash
# Show PRP content for reference
echo ""
echo "📖 PRP CONTENT OVERVIEW"
echo "========================================"
echo ""

# Extract key sections from PRP
echo "🎯 FEATURE GOAL:"
grep -A 3 "^## Feature Goal" "$PRP_FILE" | tail -n +2 || echo "Not specified"

echo ""
echo "📦 DELIVERABLE:"
grep -A 3 "^## Deliverable" "$PRP_FILE" | tail -n +2 || echo "Not specified"

echo ""
echo "✅ SUCCESS DEFINITION:"
grep -A 3 "^## Success Definition" "$PRP_FILE" | tail -n +2 || echo "Not specified"

echo ""
echo "🔧 IMPLEMENTATION TASKS:"
echo "----------------------------------------"
# Extract task list from PRP
sed -n '/^## Implementation Tasks/,/^## /p' "$PRP_FILE" | head -n -1 | tail -n +2

echo ""
echo "✅ FINAL VALIDATION CHECKLIST:"
echo "----------------------------------------"
# Extract validation checklist
sed -n '/^## Final Validation Checklist/,/^## /p' "$PRP_FILE" | head -n -1 | tail -n +2
```

### Step 5: Start Implementation

```bash
echo ""
echo "🚀 READY TO IMPLEMENT"
echo "========================================"
echo ""
echo "✅ Environment prepared:"
echo "   - Working directory is clean"
echo "   - Feature branch created: $FEATURE_BRANCH"
echo "   - PRP context loaded: $PRP_FILE"
echo ""
echo "💡 Next steps:"
echo "   1. Follow the Implementation Tasks above"
echo "   2. Use /git-ops:smart-commit for commits"
echo "   3. Use /git-ops:create-pull-request when ready"
echo "   4. Feature branch will target appropriate release branch"
echo ""
echo "📋 Remember:"
echo "   - Follow KISS/YAGNI principles"
echo "   - Write tests for new functionality"
echo "   - Update documentation as needed"
echo "   - Complete Final Validation Checklist"
echo ""
```

### Step 6: Implementation Ready

At this point, the environment is prepared and the user can begin implementing the PRP following the tasks and validation checklist. The feature branch ensures proper isolation and review workflow.

## KISS Principles

- **Single Purpose**: Automate feature branch creation for PRP execution
- **No Magic**: Clear step-by-step process with user confirmation
- **Safe Defaults**: Validates environment before making changes
- **User Control**: Prompts for confirmation on key decisions
- **Standard Flow**: Integrates with existing git-ops commands

## Success Criteria

- [x] Validates clean git environment
- [x] Creates feature branch following naming convention
- [x] Displays PRP context for implementation reference
- [x] Integrates with existing Release Flow branching strategy
- [x] Provides clear next steps for user

## Integration with Existing Workflow

This command bridges the gap between PRP creation and implementation:

1. **PRP Creation**: `/prp:create` → Creates PRP document
2. **PRP Execution**: `/prp:execute` → **NEW** Creates feature branch and starts implementation
3. **Development**: Standard development with `/git-ops:smart-commit`
4. **PR Creation**: `/git-ops:create-pull-request` → Creates feature→release PR

## Example Usage

```bash
# After creating PRP
/prp:execute PRPs/prp-003-user-authentication.md
```

This will:

- Validate environment (clean git, on main branch)
- Create `feature/prp-003-user-authentication` branch
- Display PRP context and tasks
- Prepare for implementation following Release Flow
