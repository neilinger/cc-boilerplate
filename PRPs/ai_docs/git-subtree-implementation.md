# Git Subtree Implementation Guide for Boilerplate Management

## Quick Reference

### Essential Commands

```bash
# Initial setup - add boilerplate to project
git subtree add --prefix=.claude/boilerplate https://github.com/org/cc-boilerplate.git main --squash

# Update - pull latest changes
git subtree pull --prefix=.claude/boilerplate https://github.com/org/cc-boilerplate.git main --squash

# With remote (cleaner)
git remote add cc-boilerplate https://github.com/org/cc-boilerplate.git
git subtree add --prefix=.claude/boilerplate cc-boilerplate main --squash
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash
```

## Squash Mode Operations

### Why Always Use --squash for Boilerplates

1. **Clean History**: Each update is a single commit
2. **Easy Rollback**: Can revert entire update with one commit
3. **No Pollution**: Boilerplate's history doesn't mix with project
4. **Performance**: Fewer commits to process

### Handling Squash Mode Conflicts

When using --squash, Git "forgets" previous merges, leading to potential conflicts. Solutions:

```bash
# Method 1: Force strategy
git fetch cc-boilerplate main
git merge -s subtree -X theirs FETCH_HEAD  # Accept upstream
git merge -s subtree -X ours FETCH_HEAD   # Keep local

# Method 2: Manual resolution
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash
# If conflicts occur:
git status  # See conflicted files
git checkout --theirs .claude/boilerplate/conflicted-file  # Accept upstream
git checkout --ours .claude/boilerplate/conflicted-file    # Keep local
git add .claude/boilerplate/conflicted-file
git commit

# Method 3: Re-pull pattern (prevents future conflicts)
git subtree push --prefix=.claude/boilerplate cc-boilerplate feature-branch
git subtree pull --prefix=.claude/boilerplate cc-boilerplate feature-branch --squash
```

## Advanced Patterns

### Version-Based Updates

```bash
# Tag-based updates for stability
git fetch cc-boilerplate --tags
git subtree pull --prefix=.claude/boilerplate cc-boilerplate v1.2.0 --squash

# Branch-based for continuous updates
git subtree pull --prefix=.claude/boilerplate cc-boilerplate stable --squash
```

### Subtree with Sparse Checkout

If you only need specific directories:

```bash
# Not directly supported, but workaround:
# 1. Add full subtree
git subtree add --prefix=temp cc-boilerplate main --squash

# 2. Move only needed parts
mkdir -p .claude/boilerplate
mv temp/hooks .claude/boilerplate/
mv temp/agents .claude/boilerplate/
rm -rf temp

# 3. Commit the structure
git add .claude/boilerplate
git commit -m "Add selective boilerplate components"
```

### Tracking Multiple Subtrees

Create `.gittrees` file:

```ini
[subtree "boilerplate-core"]
    url = https://github.com/org/cc-boilerplate.git
    path = .claude/boilerplate
    branch = main

[subtree "shared-utils"]
    url = https://github.com/org/shared-utils.git
    path = lib/utils
    branch = stable
```

Helper script to update all:

```bash
#!/bin/bash
while IFS= read -r line; do
    if [[ $line =~ path[[:space:]]*=[[:space:]]*(.*) ]]; then
        path="${BASH_REMATCH[1]}"
    elif [[ $line =~ url[[:space:]]*=[[:space:]]*(.*) ]]; then
        url="${BASH_REMATCH[1]}"
    elif [[ $line =~ branch[[:space:]]*=[[:space:]]*(.*) ]]; then
        branch="${BASH_REMATCH[1]}"
        echo "Updating $path from $url#$branch"
        git subtree pull --prefix="$path" "$url" "$branch" --squash
    fi
done < .gittrees
```

## Conflict Resolution Strategies

### Strategy 1: Automated Resolution

```bash
#!/bin/bash
# auto-resolve-subtree.sh
PREFIX=".claude/boilerplate"
REMOTE="cc-boilerplate"
BRANCH="main"

# Attempt pull
if ! git subtree pull --prefix="$PREFIX" "$REMOTE" "$BRANCH" --squash 2>/dev/null; then
    echo "Conflicts detected, attempting auto-resolution..."

    # Get list of conflicted files
    CONFLICTS=$(git diff --name-only --diff-filter=U)

    for file in $CONFLICTS; do
        if [[ $file == $PREFIX/* ]]; then
            # For boilerplate files, prefer upstream
            git checkout --theirs "$file"
        else
            # For project files, keep local
            git checkout --ours "$file"
        fi
        git add "$file"
    done

    # Complete the merge
    git commit -m "Auto-resolved subtree conflicts"
fi
```

### Strategy 2: Three-Way Merge Helper

```bash
#!/bin/bash
# three-way-merge.sh
PREFIX=".claude/boilerplate"

# Create temporary branch for merge
git checkout -b temp-merge

# Get the base (common ancestor)
BASE=$(git merge-base HEAD cc-boilerplate/main)

# Get three versions
git show HEAD:"$PREFIX" > local_version
git show cc-boilerplate/main:. > remote_version
git show "$BASE":"$PREFIX" > base_version

# Use three-way merge tool
git merge-file local_version base_version remote_version

# Apply result
cp local_version "$PREFIX"
git add "$PREFIX"
git commit -m "Three-way merge of subtree"
```

## Error Recovery

### Corrupted Subtree History

```bash
# Symptoms: "fatal: ambiguous argument" errors

# Fix: Re-initialize subtree
git rm -rf .claude/boilerplate
git commit -m "Remove corrupted subtree"
git subtree add --prefix=.claude/boilerplate cc-boilerplate main --squash
```

### Undo Failed Update

```bash
# Save current state
git tag before-update

# Attempt update
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash

# If failed, rollback
git reset --hard before-update
git tag -d before-update
```

### Fix "Unrelated Histories" Error

```bash
# Add --allow-unrelated-histories flag
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash --allow-unrelated-histories

# Or merge with strategy
git fetch cc-boilerplate main
git merge -s subtree -Xsubtree=".claude/boilerplate" FETCH_HEAD --allow-unrelated-histories
```

## Performance Optimization

### Shallow Clone for Large Repositories

```bash
# Initial shallow add (Git 2.9+)
git fetch --depth=1 cc-boilerplate main
git subtree add --prefix=.claude/boilerplate FETCH_HEAD --squash

# Updates with shallow fetch
git fetch --depth=1 cc-boilerplate main
git subtree merge --prefix=.claude/boilerplate FETCH_HEAD --squash
```

### Cache Remote References

```bash
# Pre-fetch all remotes
git remote update

# Use local references
git subtree pull --prefix=.claude/boilerplate cc-boilerplate main --squash --no-fetch
```

## Debugging

### Inspect Subtree History

```bash
# View subtree commits
git log --oneline --graph -- .claude/boilerplate

# Find subtree merge commits
git log --grep="git-subtree-dir: .claude/boilerplate"

# Show subtree split point
git subtree split --prefix=.claude/boilerplate --annotate='(split) '
```

### Verify Subtree Integrity

```bash
#!/bin/bash
# verify-subtree.sh
PREFIX=".claude/boilerplate"
REMOTE="cc-boilerplate"

# Get current subtree commit
LOCAL=$(git subtree split --prefix="$PREFIX" HEAD)

# Get remote commit
REMOTE_COMMIT=$(git ls-remote "$REMOTE" main | cut -f1)

echo "Local subtree: $LOCAL"
echo "Remote HEAD: $REMOTE_COMMIT"

# Check if up to date
git fetch "$REMOTE"
if git merge-base --is-ancestor "$REMOTE_COMMIT" "$LOCAL"; then
    echo "Subtree is up to date"
else
    echo "Updates available"
fi
```

## Migration Scenarios

### From Submodule to Subtree

```bash
# Save submodule info
SUBMODULE_URL=$(git config --file .gitmodules submodule..claude/boilerplate.url)
SUBMODULE_BRANCH=$(git config --file .gitmodules submodule..claude/boilerplate.branch)

# Remove submodule
git submodule deinit .claude/boilerplate
git rm .claude/boilerplate
rm -rf .git/modules/.claude/boilerplate
git commit -m "Remove boilerplate submodule"

# Add as subtree
git subtree add --prefix=.claude/boilerplate "$SUBMODULE_URL" "$SUBMODULE_BRANCH" --squash
```

### From Manual Copy to Subtree

```bash
# Backup current version
mv .claude/boilerplate .claude/boilerplate.backup

# Add subtree at same location
git subtree add --prefix=.claude/boilerplate cc-boilerplate main --squash

# Merge custom changes
cp -r .claude/boilerplate.backup/* .claude/boilerplate/
git add .claude/boilerplate
git commit -m "Restore customizations after subtree conversion"

# Clean up
rm -rf .claude/boilerplate.backup
```

## Best Practices Summary

1. **Always use --squash** for boilerplate repositories
2. **Tag before updates** for easy rollback
3. **Use remotes** instead of URLs for cleaner commands
4. **Document subtrees** in .gittrees or README
5. **Separate concerns** - never mix subtree and project changes in one commit
6. **Test updates** in feature branches first
7. **Automate** with scripts for consistency
8. **Monitor** for updates regularly (monthly/quarterly)
