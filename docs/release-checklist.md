# First Release Checklist

Use this checklist before creating the first local milestone tag.

## Source and Licensing

- source classifications in [source-policy.md](source-policy.md) are current
- blocked-source fallbacks are still valid
- no shipped artifact relies on undocumented licensing assumptions

## Validation

- all items in [validation-checklist.md](validation-checklist.md) are complete
- current validation reports reflect the reviewed baseline
- glTF validation is clean

## Known Gaps and Fidelity

- measured-vs-proxy status is explicit for current spectral inputs
- known measurement backlog items are reviewed and still accurate
- release notes mention the remaining proxy and measurement gaps

## Git and Release Readiness

- working tree is clean
- release-relevant changes are merged into `main`
- changelog reflects the release baseline
- tag name follows `v0.x.y`
- no remote-specific workflow is assumed

## Suggested Local Tag Flow

```bash
git switch main
git status --short
git tag -a v0.x.y -m "Local milestone v0.x.y"
```
