# Live Integration Gaps — explicit, not hidden

## EVO

Observed upstream baseline: `1.0.0-alpha.2`.

Available reference HTTP boundaries include health, dashboard, AI catalog, sales-order approval, production completion, shipment, cost recalculation and replay.

The APM reference decision requires:

```text
procurement.use-alternate-supplier
```

That capability is not observed in the current upstream reference API. v0.2 therefore does not claim a real upstream procurement execution that does not exist.

## Eidos

Observed upstream baseline: `1.3.0-teach-and-grow.1`.

Eidos exposes TypeScript contracts and deterministic validators, not an EC HTTP service. v0.2 outputs the exact outer `EcExperienceProposalV010` shape and includes `tools/verify-eidos.mjs` to run the proposal through a built real Eidos repository.

## v0.3 target

Adopt the candidate contracts into their owning repos and add the actual EVO procurement Command. At that point the same APM scenario can run without the Reference EVO Adapter.
