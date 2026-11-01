# Operations, quotas and release objectives

## Restricted Kubernetes/OpenShift deployment

Use ordinary Deployments for APIs/gateways/workers and StatefulSets/PVCs for native byte workers. Provide Helm/manifests with namespace-scoped RBAC, arbitrary-UID-compatible permissions, dropped capabilities and no privileged init container, host mount, new operator, CRD or custom SCC requirement. Consume approved PostgreSQL, ingress, TLS, eventing and CSI storage. Cluster-level prerequisites remain platform-admin responsibilities; the service cannot manufacture a storage class or failure domain from namespace access.

Qualify the latest two Kubernetes releases at each release gate and the actual corporate OpenShift build associated with the requested Kubernetes 1.33.12 baseline. Record exact versions/digests and permissions then; the patch number alone does not prove an available OpenShift support profile. External-only mode must install without native PVC workers or SeaweedFS. Native dev mode must be visibly unsafe for production until HA qualification passes.

## Quotas and admission

Falcone remains the source of plans, overrides and limits. Existing current byte admission delegates to tenant governance; legacy bucket/env helpers and documentation need fixture reconciliation. Preserve the approved governance fail-open behavior for the compatibility profile and emit its reason. An optional strict profile is a versioned product decision, not a silent compatibility change. Security authorization failures never become quota fail-open exceptions.

Native strict mode uses transactional reservations for concurrent uploads and bucket creation, accounted overwrite deltas and leases for uncertain in-flight work. Track logical current bytes, noncurrent retained bytes, multipart/staging bytes, physical replicated bytes, operation rate and egress as distinct dimensions. A retry must not double-charge a logical committed object, but it can consume physical/transfer resources. Define how aborted uploads, failed attempts, retention and migration copies affect billing/governance in Falcone.

External mode can enforce proxy admission for known operations, but must reconcile provider truth. Out-of-band writes and direct presigned uploads prevent a universal hard real-time cap. Show observed usage time and pending reservations/uncertain outcomes. Never fake strict enforcement using delayed notifications or compensating deletion that could destroy an overwritten existing object. Physical capacity protection always rejects unsafe native writes, even if business-quota governance is unavailable.

## Proposed objectives to validate

These are initial engineering targets, not an SLA commitment. Benchmark with object-size distribution, concurrency, failure mode and dependency latency reported.

| Measure | Initial target | Conditions and evidence |
|---|---|---|
| Governed API availability | 99.95% monthly successful eligible requests | Publish denominator and include dependency-caused failures in end-to-end reporting; separate native and each provider |
| Gateway overhead | p95 ≤20 ms, p99 ≤50 ms for small metadata requests | Measure incremental gateway/auth/routing work in-region, separately from backend/network transfer latency |
| Native HEAD/small-object first byte | p95 ≤100 ms for hot ≤64 KiB objects | No overload, qualified media and metadata; cold media/key paths reported separately |
| Native event visibility | p95 ≤5 seconds from commit to event-bus acceptance | Healthy broker; measure backlog and outage catch-up separately |
| External event visibility | Observe provider delay plus bridge delay; bridge p95 ≤5 seconds after receipt | No promise that AWS/provider delivery always arrives within five seconds |
| New-request authorization freshness | ≤30 seconds for gateway caches | Direct URLs and already-open streams have distinct revocation contracts |
| Native acknowledged-write safety | No acknowledged-data loss under the qualified single-domain failure | Requires verified blob and synchronous metadata durability; not a general disaster RPO |
| Metadata backup RPO / recovery target | ≤5-minute recoverable WAL gap; metadata service RTO ≤60 minutes initially | Independent verified backups; full object recovery adds data transfer, key recovery and validation time |
| Full storage recovery | Defined per dataset/profile after rehearsal | Lower bound is bytes to restore divided by sustained recovery bandwidth, plus metadata/key validation; no universal one-hour dataset promise |

Capacity inputs: total/current/noncurrent bytes, object count, size percentiles, bucket count, read/write/list mix, requests/sec, ingress/egress bandwidth, multipart concurrency, retention, growth and lifecycle churn. Native three-copy replication needs roughly three times stored encrypted bytes before backup, staging and operating headroom; measure actual overhead. The previous 100k messages/sec is not an S3 throughput commitment.

## Monitoring and incident behavior

Report availability/latency by operation and provider, inflight bytes, reservations, low space, degraded replica count, repair debt, integrity errors, DB contention/WAL lag, IAM/key latency, event/inbox lag, credential expiry and migration drift. Avoid object keys or unbounded tenant labels in metric series. Audit can retain scoped identifiers under access policy; traces and support bundles redact secrets and signed URLs.

Runbooks cover disk full, missing/corrupt replicas, metadata failover, key-provider loss, external throttling/outage, expired credentials, event backlog, stuck multipart, accidental deletion and restore. Use backpressure and per-tenant fairness rather than unbounded queues. Background repair/GC/migration must not starve foreground requests.

## Backup and ownership

Back up a consistent native manifest/metadata point plus all referenced blobs and required key versions. Pin those references against GC until snapshot completion and retention expiry. Test restored objects, not just database start-up. Replication is not a backup against logical deletion or compromised credentials. External providers require actual configured version/backup/retention and restore evidence; S3 API compatibility does not imply a backup API.

Platform/storage maintainers own the runtime, dependency patches and metadata format. SRE/DevOps own capacity, deploy/rollback, on-call and recovery drills. Security engineers review isolation, key use, supply chain and retention boundaries; secrets custodians own root recovery. IAM/governance owners approve policy and quota changes. Product owners approve scope/SLOs and migration gates. Name actual people/rotations during readiness; writing these roles does not establish on-call coverage.
