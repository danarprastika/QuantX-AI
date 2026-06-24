---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/DOCUMENTATION_VALIDATION.md
depends_on: ["docs/DOCUMENTATION_RULES.md"]
related_documents: []
---

# QuantX AI - Documentation Validation Rules

## 1. Purpose

This document defines the automated and manual validation rules applied to all QuantX AI documentation. Validation ensures correctness, consistency, and completeness of the documentation system.

## 2. Validation Scope

Validation is applied to every `.md` file in the repository that is part of the official documentation set.

## 3. Automated Validation Rules

### 3.1 Broken Links

| Rule | Description | Severity |
|------|-------------|----------|
| Internal link existence | Every internal `[text](path)` link must resolve to an existing file. | Error |
| Relative path validity | Links must be relative (no `/docs/` absolute paths within the docs folder). | Warning |
| Heading anchors | Links to headings within the same file must reference an existing heading. | Warning |

### 3.2 Duplicate Content Detection

| Rule | Description | Severity |
|------|-------------|----------|
| Duplicate documents | Two files must not cover the same topic without one linking to the other as source of truth. | Error |
| Duplicate sections | Identical or near-identical section headings must not appear in multiple docs for the same topic. | Warning |
| Duplicate tables | Exact duplicate tables across documents are prohibited unless one is a copy of the other for historical reasons. | Warning |

### 3.3 Metadata Validation

| Rule | Description | Severity |
|------|-------------|----------|
| YAML front matter present | Every file must begin with `---` delimited YAML front matter. | Error |
| Required fields present | `status`, `owner`, `version`, `last_updated`, `source_of_truth`, `depends_on`, `related_documents` must all be present. | Error |
| Valid status value | `status` must be one of: `Draft`, `In Review`, `Approved`, `Deprecated`, `Archived`. | Error |
| Valid date format | `last_updated` must be ISO 8601 (`YYYY-MM-DD`). | Error |
| Valid semver | `version` must match `MAJOR.MINOR.PATCH` (e.g., `1.0.0`). | Error |
| Source of truth exists | The file referenced in `source_of_truth` must exist. | Error |
| Depends on exists | Every file in `depends_on` must exist. | Error |
| Related docs exist | Every file in `related_documents` must exist. | Warning |

### 3.4 Content Validation

| Rule | Description | Severity |
|------|-------------|----------|
| Single H1 | Each file must have exactly one `# ` heading. | Error |
| No empty sections | Sections (`##` or `###`) must not be empty. | Error |
| No TODOs | Unresolved `TODO` markers are prohibited. | Error |
| No placeholder text | Placeholders like `Add content here` or `TODO` are prohibited. | Error |

### 3.5 Folder Placement

| Rule | Description | Severity |
|------|-------------|----------|
| Correct folder | Files must be located in `docs/` at repository root. | Error |
| No stray markdown | No `.md` files should exist outside `docs/` except governance templates. | Warning |
| Filename format | Filenames must match `\\d{2}_.+\\.md` or `[A-Z_]+.md` (governance files). | Error |

### 3.6 Orphan Document Detection

| Rule | Description | Severity |
|------|-------------|----------|
| Referenced elsewhere | Every documentation file should appear in at least one `related_documents` list or in the `SOURCE_OF_TRUTH.md` matrix. | Warning |
| No orphan governance | Governance files (`DOCUMENTATION_RULES.md`, etc.) must appear in `SOURCE_OF_TRUTH.md`. | Error |

## 4. Manual Validation Rules

### 4.1 Consistency Review

- Term capitalization matches the glossary in `01_PROJECT_OVERVIEW.md`.
- Numeric values (versions, ports, percentages) are consistent across documents.
- Date formats are consistent (`YYYY-MM-DD`).
- Table column alignment follows `DOCUMENTATION_RULES.md`.

### 4.2 Traceability Review

- Every ADR reference includes a status and date.
- Every cross-reference is bidirectional where appropriate.
- Deprecated documents still link to their replacement.

## 5. Validation Execution

### 5.1 Automated Checks (CI/CD)

Validation runs on every PR that modifies documentation:

```bash
# Example validation script entry points
- check_yaml_front_matter
- check_broken_links
- check_metadata_fields
- check_single_h1
- check_no_empty_sections
- check_no_todos
- check_filename_format
- check_orphan_docs
- check_duplicate_tables
```

### 5.2 Manual Checks (Scheduled)

The Architecture Team performs a full documentation review quarterly:

1. Run all automated checks.
2. Review every `In Review` document.
3. Verify `SOURCE_OF_TRUTH.md` is up to date.
4. Review `DOCUMENTATION_CHANGELOG.md` for completeness.
5. Validate all cross-references resolve correctly.

## 6. Remediation

| Severity | Action |
|----------|--------|
| Error | Must be fixed before merge or approval. |
| Warning | Should be fixed before merge; requires owner sign-off if deferred. |

## Related Documents

- [DOCUMENTATION_RULES.md](DOCUMENTATION_RULES.md)
- [DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md)
- [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/DOCUMENTATION_VALIDATION.md*
*Depends On: DOCUMENTATION_RULES.md*
*Related Documents: *
*Phase: Foundation*
