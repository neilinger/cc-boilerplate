# Start Release Journey - This Is The Way

**"This is the way."** - Guide engineers through the proper Release Flow process, picking up at any step.

## Journey Guidance

$ARGUMENTS

## The Way - Release Flow Process

Based on ADR-001, our workflow follows: `feature/* → release/* → main`

### 🧭 **Journey Navigation - Where Are You?**

```bash
# Auto-detect current state and guide next steps
CURRENT_BRANCH=$(git branch --show-current)
HAS_UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
CURRENT_STATE="unknown"

echo "🧭 Release Journey Navigator"
echo "============================"
echo "Current branch: $CURRENT_BRANCH"
echo "Uncommitted changes: $HAS_UNCOMMITTED"
echo ""

# Determine journey state
case $CURRENT_BRANCH in
  main)
    if [[ $HAS_UNCOMMITTED -gt 0 ]]; then
      CURRENT_STATE="main-dirty"
    else
      CURRENT_STATE="main-clean"
    fi
    ;;
  feature/*)
    if [[ $HAS_UNCOMMITTED -gt 0 ]]; then
      CURRENT_STATE="feature-developing"
    else
      CURRENT_STATE="feature-ready"
    fi
    ;;
  release/*)
    if [[ $HAS_UNCOMMITTED -gt 0 ]]; then
      CURRENT_STATE="release-stabilizing"
    else
      CURRENT_STATE="release-ready"
    fi
    ;;
  hotfix/*)
    CURRENT_STATE="hotfix-active"
    ;;
  *)
    CURRENT_STATE="off-path"
    ;;
esac

echo "🎯 Journey State: $CURRENT_STATE"
echo ""
```

### 🗺️ **State-Based Journey Guide**

```bash
case $CURRENT_STATE in
  "main-dirty")
    echo "🚀 Starting New Development Journey"
    echo "=================================="
    echo "You're on main with uncommitted changes."
    echo ""
    echo "This is the way:"
    echo "1. Create feature branch for your work"
    echo "2. Commit your changes to feature branch"
    echo "3. Continue development in feature branch"
    echo ""
    echo "📋 Commands to get back on path:"
    echo "   git checkout -b feature/your-feature-name"
    echo "   git add -A && git commit -m 'feat: your feature description'"
    echo ""
    echo "⚠️  Never commit directly to main (this violates The Way)"
    ;;

  "main-clean")
    echo "🌟 Ready to Begin New Journey"
    echo "============================="
    echo "Perfect starting point! You're on main with a clean state."
    echo ""
    echo "This is the way:"
    echo "1. Create feature branch for new work"
    echo "2. Develop feature following KISS/YAGNI"
    echo "3. Merge to release branch"
    echo "4. Release to main"
    echo ""
    echo "📋 Next steps:"
    echo "   git checkout -b feature/meaningful-name"
    echo "   # Start development..."
    echo ""
    echo "🎯 Or choose your journey:"
    echo "   • New feature development"
    echo "   • Bug fix"
    echo "   • Documentation update"
    echo "   • Release preparation"
    ;;

  "feature-developing")
    echo "⚒️  Active Development Journey"
    echo "============================="
    echo "You're actively developing in a feature branch."
    echo ""
    echo "This is the way:"
    echo "1. Continue development following KISS/YAGNI"
    echo "2. Commit regularly with conventional commit format"
    echo "3. Run tests frequently"
    echo "4. When ready, prepare for release integration"
    echo ""
    echo "📋 Development commands:"
    echo "   git add -A && git commit -m 'feat: description'"
    echo "   ./scripts/run_tests.sh"
    echo "   python3 tests/test_safety_hooks.py"
    echo ""
    echo "🚨 Warning: You have $HAS_UNCOMMITTED uncommitted changes"
    echo "   Save your work: git add -A && git commit -m 'wip: save progress'"
    ;;

  "feature-ready")
    echo "🎯 Feature Ready for Release Integration"
    echo "======================================="
    echo "Your feature branch is clean and ready for the next step."
    echo ""
    echo "This is the way:"
    echo "1. Push feature branch"
    echo "2. Create/identify target release branch"
    echo "3. Create PR from feature → release"
    echo "4. Review and merge"
    echo ""
    echo "📋 Next commands:"
    echo "   git push -u origin HEAD"
    echo "   /git-ops:create-pull-request \"Your PR title\""
    echo ""
    echo "🔍 Available release branches:"
    git branch -r | grep "origin/release/" | sed 's/origin\///' || echo "   No existing release branches"
    echo ""
    echo "💡 Create new release if needed:"
    echo "   git checkout -b release/v1.X.X"
    echo "   git push -u origin release/v1.X.X"
    ;;

  "release-stabilizing")
    echo "🔧 Release Stabilization Journey"
    echo "==============================="
    echo "You're in a release branch with uncommitted changes."
    echo ""
    echo "This is the way:"
    echo "1. Stabilize the release (bug fixes, polish)"
    echo "2. No new features (only critical fixes)"
    echo "3. Test thoroughly"
    echo "4. Prepare for main merge"
    echo ""
    echo "📋 Stabilization commands:"
    echo "   git add -A && git commit -m 'fix: stabilization change'"
    echo "   ./scripts/run_tests.sh --comprehensive"
    echo "   python3 tests/test_safety_hooks.py"
    echo ""
    echo "⚠️  Release branch rules:"
    echo "   • Only bug fixes and polish"
    echo "   • No new features"
    echo "   • Thorough testing required"
    ;;

  "release-ready")
    echo "🚀 Release Ready for Production"
    echo "==============================="
    echo "Release branch is stabilized and ready for main merge."
    echo ""
    echo "This is the way:"
    echo "1. Create PR from release → main"
    echo "2. Complete release checklist"
    echo "3. Merge to main"
    echo "4. Tag release"
    echo "5. Clean up branches"
    echo ""
    echo "📋 Release commands:"
    echo "   /git-ops:create-pull-request \"Release $(echo $CURRENT_BRANCH | sed 's/release\///')\""
    echo ""
    echo "📊 Release preview:"
    git log --oneline main..HEAD
    echo ""
    echo "🏷️  After merge, tag as:"
    echo "   git tag $(echo $CURRENT_BRANCH | sed 's/release\///')"
    echo "   git push origin $(echo $CURRENT_BRANCH | sed 's/release\///')"
    ;;

  "hotfix-active")
    echo "🚨 Emergency Hotfix Journey"
    echo "==========================="
    echo "You're in hotfix mode - emergency repairs."
    echo ""
    echo "This is the way:"
    echo "1. Minimal changes only"
    echo "2. Thorough testing"
    echo "3. Fast-track to main"
    echo "4. Notify stakeholders"
    echo ""
    echo "📋 Hotfix commands:"
    echo "   git add -A && git commit -m 'fix: critical hotfix description'"
    echo "   ./scripts/run_tests.sh --critical"
    echo "   /git-ops:create-pull-request \"HOTFIX: critical issue\""
    echo ""
    echo "⚠️  Hotfix rules:"
    echo "   • Minimal scope changes"
    echo "   • Emergency approval process"
    echo "   • Immediate stakeholder notification"
    ;;

  "off-path")
    echo "🧭 Off The Known Path"
    echo "====================="
    echo "Branch '$CURRENT_BRANCH' doesn't follow our naming convention."
    echo ""
    echo "This is the way back:"
    echo "1. Understand what you're building"
    echo "2. Rename branch to follow convention"
    echo "3. Continue proper journey"
    echo ""
    echo "📋 Naming conventions:"
    echo "   feature/meaningful-name  - New development"
    echo "   release/v1.2.3          - Release preparation"
    echo "   hotfix/critical-fix     - Emergency fixes"
    echo ""
    echo "🔄 Rename current branch:"
    echo "   git branch -m feature/$(echo $CURRENT_BRANCH | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"
    ;;
esac
```

### 🎯 **Journey Destination Selector**

```bash
echo ""
echo "🗺️  Where do you want to go?"
echo "=========================="
echo ""
echo "Available journeys:"
echo "1. 🚀 Start new feature development"
echo "2. 🐛 Create bug fix"
echo "3. 📝 Update documentation"
echo "4. 🏷️  Prepare release"
echo "5. 🚨 Emergency hotfix"
echo "6. 🧹 Clean up after release"
echo "7. 📊 Check release status"
echo ""

read -p "Choose your journey (1-7) or press Enter to continue current path: " JOURNEY_CHOICE

case $JOURNEY_CHOICE in
  1)
    echo ""
    echo "🚀 Starting Feature Development Journey"
    echo "======================================"
    read -p "Feature name (will become feature/NAME): " FEATURE_NAME

    if [[ -z "$FEATURE_NAME" ]]; then
      echo "❌ Feature name required"
      exit 1
    fi

    BRANCH_NAME="feature/$(echo $FEATURE_NAME | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"

    echo "Creating branch: $BRANCH_NAME"
    git checkout main
    git pull origin main
    git checkout -b "$BRANCH_NAME"

    echo "✅ Ready for development!"
    echo "This is the way: develop → commit → test → release → main"
    ;;

  2)
    echo ""
    echo "🐛 Starting Bug Fix Journey"
    echo "==========================="
    read -p "Bug description (will become feature/fix-DESCRIPTION): " BUG_DESC

    if [[ -z "$BUG_DESC" ]]; then
      echo "❌ Bug description required"
      exit 1
    fi

    BRANCH_NAME="feature/fix-$(echo $BUG_DESC | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"

    echo "Creating branch: $BRANCH_NAME"
    git checkout main
    git pull origin main
    git checkout -b "$BRANCH_NAME"

    echo "✅ Ready for bug fixing!"
    echo "This is the way: diagnose → fix → test → release → main"
    ;;

  3)
    echo ""
    echo "📝 Starting Documentation Journey"
    echo "================================"
    read -p "Documentation update (will become feature/docs-DESCRIPTION): " DOC_DESC

    if [[ -z "$DOC_DESC" ]]; then
      echo "❌ Documentation description required"
      exit 1
    fi

    BRANCH_NAME="feature/docs-$(echo $DOC_DESC | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"

    echo "Creating branch: $BRANCH_NAME"
    git checkout main
    git pull origin main
    git checkout -b "$BRANCH_NAME"

    echo "✅ Ready for documentation!"
    echo "💡 Consider using the smart-doc-generator agent"
    echo "This is the way: write → review → release → main"
    ;;

  4)
    echo ""
    echo "🏷️  Starting Release Preparation Journey"
    echo "======================================="
    read -p "Release version (e.g., v1.2.3): " RELEASE_VERSION

    if [[ -z "$RELEASE_VERSION" ]]; then
      echo "❌ Release version required"
      exit 1
    fi

    # Ensure version starts with 'v'
    if [[ ! $RELEASE_VERSION == v* ]]; then
      RELEASE_VERSION="v$RELEASE_VERSION"
    fi

    BRANCH_NAME="release/$RELEASE_VERSION"

    echo "Creating release branch: $BRANCH_NAME"
    git checkout main
    git pull origin main
    git checkout -b "$BRANCH_NAME"
    git push -u origin "$BRANCH_NAME"

    echo "✅ Release branch created!"
    echo "This is the way: stabilize → test → merge → tag"
    echo ""
    echo "📋 Next steps:"
    echo "1. Merge feature branches into this release"
    echo "2. Stabilize and test"
    echo "3. Create PR to main when ready"
    ;;

  5)
    echo ""
    echo "🚨 Starting Emergency Hotfix Journey"
    echo "==================================="
    read -p "Critical issue description: " HOTFIX_DESC

    if [[ -z "$HOTFIX_DESC" ]]; then
      echo "❌ Hotfix description required"
      exit 1
    fi

    BRANCH_NAME="hotfix/$(echo $HOTFIX_DESC | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"

    echo "Creating hotfix branch: $BRANCH_NAME"
    git checkout main
    git pull origin main
    git checkout -b "$BRANCH_NAME"

    echo "🚨 Emergency mode activated!"
    echo "This is the way: minimal fix → test → fast-track to main"
    echo ""
    echo "⚠️  Hotfix rules:"
    echo "   • Minimal changes only"
    echo "   • Thorough testing required"
    echo "   • Immediate stakeholder notification"
    ;;

  6)
    echo ""
    echo "🧹 Post-Release Cleanup Journey"
    echo "==============================="
    echo "Cleaning up merged branches..."

    # Show merged branches
    echo "🔍 Checking for merged branches..."
    git branch --merged main | grep -v "main" | grep -v "*" | while read branch; do
      echo "   Merged: $branch"
    done

    echo ""
    read -p "Delete merged branches? (y/N): " DELETE_CONFIRM

    if [[ $DELETE_CONFIRM == "y" || $DELETE_CONFIRM == "Y" ]]; then
      git branch --merged main | grep -v "main" | grep -v "*" | xargs -n 1 git branch -d
      echo "✅ Local cleanup complete!"

      echo ""
      read -p "Delete remote merged branches too? (y/N): " DELETE_REMOTE

      if [[ $DELETE_REMOTE == "y" || $DELETE_REMOTE == "Y" ]]; then
        echo "🔄 Cleaning remote branches..."
        git remote prune origin
        echo "✅ Remote cleanup complete!"
      fi
    fi
    ;;

  7)
    echo ""
    echo "📊 Release Status Check"
    echo "======================"

    echo "🌟 Main branch status:"
    git log --oneline -5 main

    echo ""
    echo "🚀 Active release branches:"
    git branch -r | grep "origin/release/" | sed 's/origin\///' || echo "   No active releases"

    echo ""
    echo "🔧 Active feature branches:"
    git branch -r | grep "origin/feature/" | sed 's/origin\///' | head -10 || echo "   No active features"

    echo ""
    echo "🏷️  Recent releases:"
    git tag --sort=-version:refname | head -5 || echo "   No tags found"

    echo ""
    echo "📈 Repository health:"
    echo "   Total branches: $(git branch -r | wc -l | tr -d ' ')"
    echo "   Total commits: $(git rev-list --count HEAD)"
    echo "   Latest commit: $(git log -1 --pretty=format:'%h - %s (%cr)')"
    ;;

  "")
    echo "📍 Continuing current journey..."
    echo "Use the guidance above to proceed with The Way."
    ;;

  *)
    echo "❌ Invalid choice. This is not the way."
    echo "Choose 1-7 or press Enter to continue current path."
    ;;
esac
```

### 🛡️ **The Way - Core Principles**

```bash
echo ""
echo "🛡️  The Way - Core Principles"
echo "==========================="
echo ""
echo "1. 🎯 KISS/YAGNI: Keep it simple, build only what's needed"
echo "2. 🔒 Security: Never commit secrets, validate all changes"
echo "3. 🧪 Testing: Test early, test often, test thoroughly"
echo "4. 📝 Documentation: Update docs with every change"
echo "5. 🔄 Small commits: Atomic, logical, well-described changes"
echo "6. 🚀 Release flow: feature → release → main (never skip steps)"
echo "7. 🤖 Agent system: Use specialized agents for domain tasks"
echo "8. 📋 ADR compliance: Follow architectural decisions"
echo ""
echo "This is the way."
```

### 🚨 **Emergency Procedures**

```bash
# Emergency resets if things go wrong
if [[ "$ARGUMENTS" == *"emergency"* || "$ARGUMENTS" == *"reset"* ]]; then
  echo ""
  echo "🚨 Emergency Procedures"
  echo "======================"
  echo ""
  echo "If you're lost and need to get back on The Way:"
  echo ""
  echo "1. 🏠 Return to safety (main branch):"
  echo "   git stash"
  echo "   git checkout main"
  echo "   git pull origin main"
  echo ""
  echo "2. 🧹 Clean up if needed:"
  echo "   git stash list  # See your stashed work"
  echo "   git stash pop   # Restore work if needed"
  echo ""
  echo "3. 🔄 Start fresh journey:"
  echo "   /git-ops:start-release-journey"
  echo ""
  echo "4. 🆘 Last resort - abort everything:"
  echo "   git reset --hard origin/main"
  echo "   git clean -fd"
  echo "   ⚠️  WARNING: This destroys all local changes!"
  echo ""
  echo "Remember: This is the way. Trust the process."
fi
```

## 🎯 **Success Metrics**

- ✅ Following proper branch naming conventions
- ✅ No direct commits to main branch
- ✅ All features go through release stabilization
- ✅ Tests pass at every step
- ✅ Documentation stays current
- ✅ Clean, atomic commits
- ✅ Proper PR templates used
- ✅ Agent system utilized appropriately

## 📚 **Reference Documentation**

- **ADR-001**: [Branching Strategy](../../docs/adr/adr-001-branching-strategy.md)
- **ADR-007**: [Agent System Architecture](../../docs/adr/adr-007-agent-system-architecture.md)
- **Branch Protection**: [Guide](../../docs/guides/branch-protection.md)
- **Agent System**: [Reference](../../docs/reference/agent-system.md)

---

**"This is the way."** - Follow the path, trust the process, deliver excellence.