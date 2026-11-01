# Native consistency, durability and recovery

## Profiles and limits

| Profile | Intended use | Commit rule and failure behavior |
|---|---|---|
| `native-dev` | Synthetic local development only | One durable blob location plus metadata; no HA or production durability claim |
| `native-ha` | Qualified single-region production target | Three durable encrypted copies across three verified independent failure domains plus durable metadata commit; strict writes stop if the required copies cannot acknowledge |
| External | Qualified managed or customer S3 | Provider-documented guarantees under tested configuration; Falcone journal and external object state are not atomic |

Three pods or PVCs on one shared storage array are **not** three independent failure domains. The storage class, filesystem flush behavior, mount permissions, database replication and infrastructure failure topology must be qualified. If only one common storage failure domain is available, describe delegated storage durability honestly and do not enable the independent-replica profile. No numerical “nines” durability claim is inferred from replica count.

Native metadata is authoritative PostgreSQL state. To claim no loss of acknowledged writes under the specified single-domain failure, metadata must use a verified synchronous durable replication/failover configuration as well as durable blob replicas. Asynchronous database replication cannot justify that claim. Availability during reduced replica count is a separate policy: the initial strict profile may serve valid reads but rejects writes until three qualified durable locations are available. A later quorum policy needs its own acknowledgement and failure proof.

## Commit protocol

1. Authorize, resolve binding and writer epoch, check conditions that can be checked early and reserve governed/temp capacity. Create a leased staging manifest.
2. Stream immutable chunks to selected locations. Validate length and integrity, encrypt using reviewed chunk framing/AEAD with unique nonces and object/version/chunk authenticated context. Workers durably flush payload and required metadata before acknowledging. Final parameters are benchmarked, not chosen to imply a performance guarantee.
3. Validate replica receipts, lease/placement generation and complete manifest. In one database transaction, recheck writer epoch and conditions, allocate/update the object version and current pointer, finalize quota delta, audit acceptance and outbox event. Serialize conflicting key changes with database locks/CAS.
4. Commit metadata before returning success. Reads use only committed manifests and verified data. A failed transaction leaves invisible orphan chunks, handled by GC after safe grace and reference checks.

There is no transaction across the database and blob filesystem. Ordering makes pre-commit orphans safe; a premature or false byte acknowledgement makes committed data unsafe. Test crashes at every boundary. Placement-generation updates, worker replacement and failover cannot make stale workers publish data or GC decisions.

## Multipart, copy and deletion

Upload parts remain invisible and quota-accounted until completion. Part replacement updates staged accounting safely; abandoned/expired/aborted parts are reclaimed only after in-flight leases cannot commit. Completion is a state machine with one winner and a persistent completion result. Verify ordered part identifiers, checksums and size limits for the selected protocol; reserve final capacity without double counting staged and committed logical bytes.

Native copy may reuse immutable data only when authorization, encryption context, retention and reference accounting permit it; cross-scope copies normally re-encrypt into the destination context. Conditional source/destination checks must be tested. External server-side copy is capability-gated and never assumed to work across accounts/providers.

Unversioned delete changes the authoritative namespace; physical reclamation is asynchronous. Versioned delete may create a marker. Retained versions, legal holds, workflow pins and backup references block reclamation according to policy. Product recursive deletion must expose blocked/incomplete cleanup and must not bypass retention through an alternate API or administrative path.

## Repair and garbage collection

Read failures/checksum mismatches try qualified replicas within a deadline and enqueue repair. Scrubbing traverses committed manifests, verifies media integrity and reports missing copies. Repair copies verified data under a placement lease, records new durable placement before retiring old placement, and is bandwidth-limited to protect foreground work.

GC must check live manifests, in-flight uploads, pending commits, retention, job leases, workflow pins and backup epochs. Use conservative mark/sweep with a safety horizon and revalidation under a current fence; age alone is not proof of orphanhood. A worker must not delete data using an unbounded stale reference snapshot. Tombstones and lifecycle jobs are idempotent and cannot resurrect deleted objects.

## Consistency and testing

Native target: atomic per-object replace, strongly consistent committed GET/HEAD and namespace listing from the authoritative primary, with defined pagination under concurrent mutation. No cross-object transaction, atomic recursive deletion or globally ordered event stream. Read replicas require explicit lag/consistency handling and are not silently used for strong reads.

Verify power/process loss, delayed flush, disk full, broken PVC, corrupted chunk, database failover, network partitions, duplicated/reordered requests, expired job leases, lost success responses and interrupted repair. Use an operation history checker for per-key behavior and a recovery oracle comparing acknowledged objects/versions against manifests and checksums. The native engine is not a production option until the failure model and restore evidence match the advertised profile.
