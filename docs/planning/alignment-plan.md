# Auto Poly standard alignment

Auto Luno keeps its Flask application, exchange-read workflows, and paper bot
while adopting the reusable template's infrastructure boundaries and Auto Poly's
deny-by-default progression. No exchange mutation is authorized by this plan.

## Phases

1. **Operational safety baseline**: typed settings; injectable required Mongo
   boundary; honest liveness/readiness; safe setup separated from startup;
   operator protection and append-only audit for settings/bot lifecycle changes;
   provider-neutral AI with Ollama default; legacy Node quarantined.
2. **Paper ledger**: normalized intent IDs, guard/risk validation, immutable fills,
   positions rebuilt from fills, reconciliation, and deterministic paper PnL.
3. **Read-only operations**: refresh run history, snapshot freshness, scheduler
   status, incident/recovery docs, and longer paper soaks with operator review.
4. **Architecture consolidation**: move exchange/database SDK details behind ports
   and adapters, finish legacy data verification, then remove the inactive Node
   runtime in a dedicated reviewed change.
5. **Production review**: keep orders, withdrawals, and fund movements blocked
   until secrets, monitoring, kill switch, limits, incidents, and staged human
   approval pass a formal review.

Phase 1 is complete when tests prove Mongo-gated readiness, dependency injection,
mutation authorization/audit, disabled-provider behavior, safe setup/startup, and
the existing frontend exposes diagnostic state without losing product screens.
