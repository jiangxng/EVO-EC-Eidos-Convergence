# EC-21 Enterprise Function Pack Package Management

Implemented v0.2 reference operations:

```text
backup → checksum manifest → verify → install → CURRENT/PREVIOUS pointers → rollback
```

The `.ecpack` file is a ZIP transport format with `BACKUP.json` and `payload/*`.

This is a reference manager, not yet a production registry/signature service. Production evolution should add signatures, dependency solver, policy approval, migrations, transactional install and durable audit storage.
