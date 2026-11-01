# Migration and rollout

## Stages

1. **Inventory:** record current SeaweedFS releases, bucket/workspace bindings, credentials, all consumers, object/version counts, sizes/checksums, metadata/tags, multipart sessions, retained objects, lifecycle/policy/CORS and notification rules. Include public endpoint names and issued URL lifetimes. Check source docs versus deployed reality.
2. **Contract façade:** qualify existing SeaweedFS through the new provider boundary while retaining one authoritative backend. Test Falcone console/SDK/workflow/serverless paths and exposed S3 SDK operations. This phase changes no object authority by itself.
3. **Destination qualification:** choose native HA or an approved external profile per binding. Verify residency, capacity, checksums, version/retention/key capabilities, caller scope, backups and rollback mechanics. Unsupported required capabilities block that binding's migration.
4. **Copy and verify:** resumably copy to isolated destination keys/buckets under scoped credentials, recording source/destination identity and version mapping. Validate byte integrity with an appropriate checksum, metadata, tags, conditions and retention. Provider ETags are not a universal equality check. Encrypt data in transit; reports contain no credentials or sensitive object content.
5. **Single-writer handoff:** quiesce writers, revoke/drain outstanding write grants and uploads, reconcile final differences, then update the authoritative binding/writer epoch and routing. External independent writers require provider-side restriction or verified coordination; a Falcone database flag cannot fence them.
6. **Canary and expand:** verify reads/writes/deletes, workflows, runtime artifacts, event delivery, usage, key rotation and restore for selected scopes. Expand after measurable gates, not just a successful bucket listing.
7. **Retire selectively:** remove SeaweedFS only after every dependent binding/consumer and rollback need is resolved. Amazon S3 and other external providers remain supported permanent choices.

## Compatibility traps

Existing version IDs, multipart upload IDs and signed URLs are backend-specific. Keep a scoped version translation map for durable workflow/artifact references; don't invent the same raw S3 version ID on a new provider. Drain/abort multipart under an approved plan; do not move an in-progress upload ID between engines. Existing presigned URLs may require the old endpoint and credentials until expiry, or an explicit invalidation window. They cannot generally be transparently rewritten after signing.

Object Lock/legal hold and provider-specific retention may prevent copying or deletion. Preserve or formally block migration; a destination timestamp is not automatically equivalent legal retention. Any notification-rule changes must preserve unrelated adopted bucket rules and prevent duplicate trigger effects during overlapping source/destination observation. Record causation and migration-generated events rather than firing application workflows unintentionally.

No automatic dual-write baseline: independent providers have no shared atomic commit and can diverge after one successful write. Shadow reads/metadata comparisons are useful; duplicate application mutations are not safe validation. If future dual-write is needed, it requires an explicit repair log, conflict rules and visible partial outcomes.

## Rollback and exit

Rollback after destination writes is a new reconciled authority transfer. Freeze, copy/reconcile new versions, deletions, policy/retention and reference mappings, verify, then fence and switch. Pointing clients at an old source snapshot would lose post-cutover writes. Retain source only for the approved window with access restricted; retained data and old keys remain part of the security/data-retention inventory.

Native production cutover requires protocol/contract, tenant-isolation, independent security, durability, corruption-repair, quota, event, consumer and disaster-recovery evidence. External releases require the applicable provider, credential, recovery and consumer gates, not proof of an unused native engine. Retirement of a live service is a separate operational rollout decision; publishing this plan performs no deployment or data migration.
