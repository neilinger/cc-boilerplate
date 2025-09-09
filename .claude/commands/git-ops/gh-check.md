# GitHub Maintenance Check

Check GitHub issues and PRs for maintenance needs. Reports what requires attention without making any changes.

## Usage

Simply run the command to get a maintenance status report:

```bash
gh-check
```

## What It Checks

1. **Issues needing triage** (no labels)
2. **Stale issues** (open 30+ days without activity)
3. **PRs awaiting review**
4. **Draft PRs** (ready for review?)
5. **Approved PRs** (ready to merge?)

## Implementation

```bash
# Check for dependencies
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Install with: brew install gh"
    exit 1
fi

# Check GitHub authentication
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI not authenticated. Run: gh auth login"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "❌ Not in a Git repository"
    exit 1
fi

echo "🔍 GitHub Maintenance Check Report"
echo "================================="
echo ""

# Check for all open issues (maintenance needed regardless of labels)
OPEN_ISSUES=$(gh issue list --json number | jq '. | length')
if [ "$OPEN_ISSUES" -gt 0 ]; then
    echo "📋 Open issues: $OPEN_ISSUES"
    gh issue list --json number,title,labels --jq '.[] | "  - #\(.number): \(.title)" + (if (.labels | length) > 0 then " [" + (.labels | map(.name) | join(", ")) + "]" else " [unlabeled]" end)'
    echo ""
fi

# Check for unlabeled issues specifically
UNLABELED=$(gh issue list --json number,title,labels --jq '.[] | select(.labels | length == 0) | .number' | wc -l | xargs)
if [ "$UNLABELED" -gt 0 ]; then
    echo "🏷️ Issues needing labels: $UNLABELED"
    echo ""
fi

# Check for stale issues (30+ days)
STALE_DATE=$(date -d '30 days ago' '+%Y-%m-%d' 2>/dev/null || date -v-30d '+%Y-%m-%d')
STALE=$(gh issue list --json number,title,updatedAt --jq ".[] | select(.updatedAt < \"$STALE_DATE\") | .number" | wc -l | xargs)
if [ "$STALE" -gt 0 ]; then
    echo "🕒 Stale issues (30+ days): $STALE"
    gh issue list --json number,title,updatedAt --jq ".[] | select(.updatedAt < \"$STALE_DATE\") | \"  - #\(.number): \(.title)\""
    echo ""
fi

# Check PRs awaiting review
AWAITING_REVIEW=$(gh pr list --json number,title,reviewDecision --jq '.[] | select(.reviewDecision == null) | .number' | wc -l | xargs)
if [ "$AWAITING_REVIEW" -gt 0 ]; then
    echo "👀 PRs awaiting review: $AWAITING_REVIEW"
    gh pr list --json number,title,reviewDecision --jq '.[] | select(.reviewDecision == null) | "  - #\(.number): \(.title)"'
    echo ""
fi

# Check draft PRs
DRAFTS=$(gh pr list --json number,title,isDraft --jq '.[] | select(.isDraft == true) | .number' | wc -l | xargs)
if [ "$DRAFTS" -gt 0 ]; then
    echo "📝 Draft PRs: $DRAFTS"
    gh pr list --json number,title,isDraft --jq '.[] | select(.isDraft == true) | "  - #\(.number): \(.title)"'
    echo ""
fi

# Check approved PRs ready to merge
APPROVED=$(gh pr list --json number,title,reviewDecision --jq '.[] | select(.reviewDecision == "APPROVED") | .number' | wc -l | xargs)
if [ "$APPROVED" -gt 0 ]; then
    echo "✅ Approved PRs ready to merge: $APPROVED"
    gh pr list --json number,title,reviewDecision --jq '.[] | select(.reviewDecision == "APPROVED") | "  - #\(.number): \(.title)"'
    echo ""
fi

# Summary
TOTAL_ITEMS=$((OPEN_ISSUES + STALE + AWAITING_REVIEW + DRAFTS + APPROVED))
if [ "$TOTAL_ITEMS" -eq 0 ]; then
    echo "🎉 All clean! No maintenance items found."
else
    echo "📊 Total maintenance items: $TOTAL_ITEMS"
fi

echo ""
echo "💡 Tip: Use 'gh issue list' and 'gh pr list' for detailed views"
```

## KISS Principles

- **Single responsibility**: Just check and report
- **No automation**: Shows what needs doing, doesn't do it
- **Simple output**: Human-readable status
- **Uses existing tools**: Only `gh` CLI commands
- **No state**: Runs fresh each time

## Next Steps

After running this check, you can:

1. **Label issues**: `gh issue edit <number> --add-label "bug"`
2. **Review PRs**: `gh pr review <number>`
3. **Close stale issues**: `gh issue close <number>`
4. **Merge approved PRs**: `gh pr merge <number>`

All actions remain manual and intentional.
