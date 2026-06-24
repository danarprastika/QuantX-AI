# QuantX AI - Branching Strategy

## Overview

This document defines the branching strategy for QuantX AI development using GitFlow adapted for continuous deployment.

## Branching Model

### Primary Branches
| Branch | Purpose | Protection |
|--------|---------|------------|
| main | Production code | Required reviews, status checks |
| develop | Integration branch | Required reviews |
| staging | Pre-production | Auto-deploy to staging |

### Supporting Branches
| Type | Lifetime | Merge Target |
|------|----------|--------------|
| feature/* | Short-lived | develop |
| fix/* | Short-lived | develop |
| release/* | Long-lived | main, develop |
| hotfix/* | Short-lived | main, develop |

## Branch Protection Rules

### Main Branch
- Required status checks: CI (tests, lint, security)
- Required reviews: 2 approvals
- Dismiss stale reviews: true
- Require branches up-to-date: true

### Develop Branch
- Required status checks: CI
- Required reviews: 1 approval

## Release Process

### Version Bump
1. Create release branch
2. Update version numbers
3. Run release tests
4. Merge to main with tag
5. Merge back to develop

### Hotfix Process
1. Branch from main
2. Fix and test
3. Merge to main with patch version
4. Merge to develop
5. No feature freeze needed

## Merge Strategies

### Feature Merges
- Squash and merge
- Clean history
- Linear progression

### Release Merges
- Merge commit
- Preserve history
- Clear milestone

## Related Documents
- [40_CI_CD.md](40_CI_CD.md)
- [51_VERSIONING.md](51_VERSIONING.md)
- [50_RELEASE_PROCESS.md](50_RELEASE_PROCESS.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Operations*