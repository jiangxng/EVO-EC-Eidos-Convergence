# EVO minimal adoption target

Do not import Convergence internals. Adopt only owning contracts/ports.

1. Publish `EvoIntelligenceFeedV010` from governed query/event boundaries.
2. Publish a procurement capability/Command for `procurement.use-alternate-supplier`.
3. Accept authorized requests only through normal EVO Command execution.
4. Emit `EvoOutcomeV010` correlated to the proposal/Command.
5. Preserve existing idempotency, actor authorization, lineage and replay invariants.
