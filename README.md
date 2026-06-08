# HADS Validator Action

[![HADS](https://img.shields.io/badge/HADS-1.0.0-4A90E2?style=for-the-badge&logo=markdown&logoColor=white)](https://github.com/catcam/hads)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/catcam/hads-action)
[![License](https://img.shields.io/github/license/catcam/hads-action?style=for-the-badge)](LICENSE)

Validate Markdown files against the [Human-AI Document Standard](https://github.com/catcam/hads) in your CI pipeline.

---

## Quick start

```yaml
- uses: catcam/hads-action@v1
```

That's it. Add it to any workflow step and it validates all `**/*.md` files in your repo.

---

## Full example

```yaml
# .github/workflows/hads.yml
name: HADS Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: catcam/hads-action@v1
        with:
          paths: "**/*.md"
          fail_on_violation: "true"
```

---

## Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `paths` | Glob pattern of files to validate | `**/*.md` |
| `fail_on_violation` | Fail CI if any violations are found | `true` |
| `add_badge` | Auto-insert HADS badge into README on success | `true` |

Set `fail_on_violation: "false"` to run in report-only mode — violations are printed but CI passes.

### Automatic badge

When `add_badge: "true"` (default), the action automatically inserts this badge into your `README.md` the first time validation passes:

[![HADS Optimized](https://img.shields.io/badge/docs-HADS%20optimized-4A90E2?style=flat-square&logo=markdown&logoColor=white)](https://github.com/catcam/hads)

The commit message includes `[skip ci]` so it won't trigger another workflow run. Requires `permissions: contents: write` in your workflow:

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: catcam/hads-action@v1
```

---

## What it checks

| Check | Description |
|-------|-------------|
| H1 title | Document must have a top-level `# Title` heading |
| Version | `**Version X.Y.Z**` declaration required near the top |
| AI manifest | `AI READING INSTRUCTION` section must be present before content |
| `[BUG]` fields | Every `**[BUG]**` block must contain `symptom` and `fix` fields |
| Tag formatting | Warns on unformatted tags that should use `**[TAG]**` syntax |

---

## About HADS

HADS (Human-AI Document Standard) is a lightweight Markdown convention that makes technical documentation work equally well for humans and AI language models.

- [Specification](https://github.com/catcam/hads/blob/main/SPEC.md)
- [Examples](https://github.com/catcam/hads/tree/main/examples)
- [Full documentation](https://catcam.github.io/hads/)
- [Position paper](https://doi.org/10.5281/zenodo.19288202) — DOI: 10.5281/zenodo.19288202

---

## License

MIT
