# EC-22 Two-EC Knowledge Merge

v0.2 includes an executable reference merge engine with two modes:

- `COPY_MERGE`
- `NEW_BRAIN_MERGE`

Rules:

- never blind-overwrite conflicting knowledge;
- preserve source EC and provenance;
- preserve different tenant/industry scope;
- preserve time differences;
- deduplicate exact semantic duplicates while keeping provenance;
- emit unresolved conflicts for governance.

`BIDIRECTIONAL_MERGE` is intentionally not implemented in v0.2 because it needs durable sync cursors, authorization and conflict-resolution protocols rather than a one-shot file merge.
