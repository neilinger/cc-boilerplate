# Execute PRP - Feature Branch Implementation

## Arguments: PRP File Path

$ARGUMENTS

## Mission: One-Pass Implementation Success

Execute a PRP (Product Requirement Prompt) in a proper feature branch following Release Flow branching strategy, with automatic status tracking.

**Workflow**: `feature/prp-{number}-{slug}` → `release/*` → `main`

PRPs enable working code on the first attempt through:

- **Context Completeness**: Everything needed, nothing guessed
- **Progressive Validation**: 4-level gates catch errors early
- **Pattern Consistency**: Follow existing codebase approaches
- **Status Tracking**: Automatic status updates from PROPOSED to IN_PROGRESS

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

### Step 2: Parse PRP File and Update Status

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

# UPDATE STATUS: Change Status: PROPOSED to Status: IN_PROGRESS
# Update Status_Date: to today's date
# Add Status_Note: Implementation started
echo "📝 Updating PRP status to IN_PROGRESS..."

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

### Step 4: Load PRP Context & Plan

```bash
echo ""
echo "📖 PRP CONTENT OVERVIEW"
echo "========================================"
echo ""

# Extract key sections from PRP
echo "🎯 FEATURE GOAL:"
grep -A 3 "^## Feature Goal" "$PRP_FILE" | tail -n +2 || grep -A 3 "^\*\*Feature Goal\*\*" "$PRP_FILE" | tail -n +2

echo ""
echo "📦 DELIVERABLE:"
grep -A 3 "^## Deliverable" "$PRP_FILE" | tail -n +2 || grep -A 3 "^\*\*Deliverable\*\*" "$PRP_FILE" | tail -n +2

echo ""
echo "✅ SUCCESS DEFINITION:"
grep -A 3 "^## Success Definition" "$PRP_FILE" | tail -n +2 || grep -A 3 "^\*\*Success Definition\*\*" "$PRP_FILE" | tail -n +2
```

### Step 5: Execute Implementation

**Your Goal**: Transform the PRP into working code that passes all validation gates.

1. **ULTRATHINK & Plan**
   - Create comprehensive implementation plan following the PRP's task order
   - Break down into clear todos using TodoWrite tool
   - Use subagents for parallel work when beneficial
   - Follow the patterns referenced in the PRP

2. **Execute Implementation**
   - Follow the PRP's Implementation Tasks sequence
   - Use the patterns and examples referenced in the PRP
   - Create files in locations specified by the desired codebase tree
   - Apply naming conventions from the task specifications

3. **Progressive Validation**
   - **Level 1**: Run syntax & style validation commands from PRP
   - **Level 2**: Execute unit test validation from PRP
   - **Level 3**: Run integration testing commands from PRP
   - **Level 4**: Execute specified validation from PRP

   **Each level must pass before proceeding to the next.**

4. **Completion Verification**
   - Work through the Final Validation Checklist in the PRP
   - Verify all Success Criteria from the "What" section are met
   - Confirm all Anti-Patterns were avoided
   - Implementation is ready and working

### Step 6: Implementation Ready

```bash
echo ""
echo "🚀 READY TO IMPLEMENT"
echo "========================================"
echo ""
echo "✅ Environment prepared:"
echo "   - Working directory is clean"
echo "   - Feature branch created: $FEATURE_BRANCH"
echo "   - PRP status updated to IN_PROGRESS"
echo "   - PRP context loaded: $PRP_FILE"
echo ""
echo "💡 Next steps:"
echo "   1. Follow the Implementation Tasks above"
echo "   2. Use /git-ops:smart-commit for commits"
echo "   3. Use /git-ops:create-pull-request when ready"
echo "   4. Use /prp:review when implementation complete"
echo ""
echo "📋 Remember:"
echo "   - Follow KISS/YAGNI principles"
echo "   - Write tests for new functionality"
echo "   - Update documentation as needed"
echo "   - Complete Final Validation Checklist"
echo ""
```

**Failure Protocol**: When validation fails, use the patterns and gotchas from the PRP to fix issues, then re-run validation until passing.

## KISS Principles

- **Single Purpose**: Automate feature branch creation and status tracking for PRP execution
- **No Magic**: Clear step-by-step process with user confirmation
- **Safe Defaults**: Validates environment before making changes
- **User Control**: Prompts for confirmation on key decisions
- **Status Tracking**: Automatic PRP lifecycle management

## Integration with Existing Workflow

This command bridges the gap between PRP creation and implementation:

1. **PRP Creation**: `/prp:create` → Creates PRP document (Status: PROPOSED)
2. **PRP Execution**: `/prp:execute` → Creates feature branch, updates status to IN_PROGRESS
3. **Development**: Standard development with `/git-ops:smart-commit`
4. **PR Creation**: `/git-ops:create-pull-request` → Creates feature→release PR
5. **PRP Review**: `/prp:review` → Updates status to COMPLETED after validation

## Example Usage

```bash
# After creating PRP
/prp:execute PRPs/prp-003-user-authentication.md
```

This will:

- Validate environment (clean git, on main branch)
- Update PRP status from PROPOSED to IN_PROGRESS
- Create `feature/prp-003-user-authentication` branch
- Display PRP context and tasks
- Prepare for implementation following Release Flow
