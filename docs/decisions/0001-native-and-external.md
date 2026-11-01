# ADR 0001 — One Falcone storage contract, native and external engines

Date: 2026-11-01. Status: **proposed technical baseline**. The owner confirmed custom Falcone integration and support for external S3, including Amazon S3. The detailed native failure model and deployment profiles still require evidence.

## Decision

Implement a first-party control/protocol layer with explicit per-bucket provider bindings. Preserve Falcone APIs and IAM/governance contracts. Supply a native immutable-blob engine with transactional PostgreSQL metadata and a separately qualified S3 protocol façade. Support external Amazon S3 general-purpose buckets and qualified S3-compatible providers without requiring native byte workers.

Use accepted falcone-secrets decisions for key operations and provider-credential custody. Use existing Falcone event contracts with native outbox/external inbox. Retain one authoritative writer per binding and never hide missing provider semantics. Native replication precedes optional EC/compaction; no custom consensus or crypto is planned.

## Options and trade-offs

| Option | Scale and developer experience | Operations | Compatibility and decision |
|---|---|---|---|
| Shared Falcone façade, native and external adapters | One product contract; each backend has visible capabilities | Own adapter qualification and native durability engineering | Recommended target; supports the explicit external-provider requirement |
| External-first delivery while native engine matures | Early API/integration validation; managed storage can handle large demand | Retains cloud/provider cost and service dependence | Recommended staging, not cancellation of native work |
| Custom façade over SeaweedFS only | Low initial implementation work | Retains master/filer/volume upgrades and quirks | Transitional path, insufficient final scope |
| Fork/rebrand an existing object store | Reuse broad features, inherit behavior | Patch/merge/license burden and original operational model | Consider only justified components, not the default |
| Replication before erasure coding | More predictable initial repair/read paths, higher raw capacity cost | Simpler initial qualification; three independent copies still require real topology | Recommended native start; EC needs a separate later ADR and failure suite |
| Managed external storage only | Less storage-engine work, provider-specific latency/features | Network, egress, provider IAM/KMS and account operations remain | Supported deployment mode, not the only product architecture |
| Direct presigned data access | Less gateway bandwidth, familiar client uploads | Weaker synchronous Falcone quota/revocation and audit visibility | Opt-in binding capability; unsuitable where policy requires every request through Falcone |
| PostgreSQL metadata sharding | Can distribute namespace pressure | More restore/routing/transaction complexity | Defer until measured bottlenecks; choose shard boundaries explicitly |
| Cross-region active-active | Regional locality and resilience potential | Conflicts, version ordering, replication lag and residency complexity | Out of initial scope; no automatic multi-provider write failover |

## Release rule

A feature is supported only when its operation, provider/profile, ownership mode and failure semantics have passing evidence. No “100% S3 compatibility” claim, numerical durability claim, global transaction, instant direct-URL revocation or inherited upstream security certification is implied.
