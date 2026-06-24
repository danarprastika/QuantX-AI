---
status: Approved
owner: Engineering Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/41_GIT_WORKFLOW.md
depends_on:
  - docs/42_BRANCHING_STRATEGY.md
  - docs/43_CODING_STANDARD.md
related_documents:
  - docs/42_BRANCHING_STRATEGY.md
  - docs/43_CODING_STANDARD.md
---
# QuantX AI - Git Workflow

## Overview

This document defines the Git workflow for QuantX AI development, including branching strategy, commit conventions, pull request process, and release tagging.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Git Workflow                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   main (production)                                                    │
│   ├── releases/v1.2.3                                                 │
│   └── develop                                                         │
│       ├── feature/trading-enhancement                                   │
│       ├── feature/ml-model-improvements                                 │
│       ├── hotfix/critical-bug-fix                                       │
│       └── release/v1.3.0                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/{description}` | `feature/add-rsi-strategy` |
| Bugfix | `fix/{description}` | `fix/order-slippage` |
| Hotfix | `hotfix/{description}` | `hotfix/critical-crash` |
| Release | `release/{version}` | `release/v1.2.0` |
| Chore | `chore/{description}` | `chore/update-deps` |

## Commit Message Format
```
type(scope): subject

[optional body]

[optional footer]
```

### Types
- `feature`: New functionality
- `fix`: Bug fixes
- `chore`: Maintenance tasks
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `break`: Breaking changes

## Pull Request Process

### Requirements
1. All tests pass
2. Code coverage maintained
3. Lint checks pass
4. At least 1 approval
5. Security scan clean

### PR Template
```markdown
## Description
[Summary of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows conventions
- [ ] Documentation updated
- [ ] Tests added
```

## Related Documents
- [42_BRANCHING_STRATEGY.md](42_BRANCHING_STRATEGY.md)
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Engineering Team*
*Source of Truth: docs/41_GIT_WORKFLOW.md*
*Depends On: 42_BRANCHING_STRATEGY.md, 43_CODING_STANDARD.md*
*Related Documents: 42_BRANCHING_STRATEGY.md, 43_CODING_STANDARD.md*
*Phase: Operations*
