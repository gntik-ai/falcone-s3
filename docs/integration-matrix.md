# Integration with the Falcone stack

No sibling repository or deployment is modified by this S3 planning package. Each integration below requires a reviewed implementation handoff and pinned contract fixtures.

| Falcone system | Contract and ownership | Required acceptance evidence |
|---|---|---|
| Main control plane, API gateway/APISIX | Existing `/v1/storage/*`, authentication/error order, registry and external/public URL behavior | Existing console/SDK fixtures, path/host preservation and safe errors |
| Console and developer SDKs | Existing bucket/object flows plus provider/binding capabilities and freshness | Choose approved native/external profiles; unsupported operations disabled with a reason; no credential leakage |
| `falcone-iam` / transitional Keycloak | Users, roles, workload identity, policy decisions and tenant/workspace lifecycle | Deny cross-scope actions, expired grants and unsupported policy clauses; SAML/OIDC/LDAP/AD/SCIM stay in IAM |
| `falcone-secrets` / transitional OpenBao | External credentials, SigV4 key custody, wrapping-key operations and rotation | Accepted secrets ADR 0002; bounded caches, independent bootstrap and recovery, old-version key availability |
| `falcone-serverless` | Scoped artifact reads, outputs/checkpoints and object event triggers | Immutable digest/version references; host/shim grants where required; no platform backend key passed to guest code |
| `falcone-workflow` / transitional Temporal activities | Storage activities and large payload/result references | Write/verify object before committing durable reference; attempt-scoped grants, reference pins and orphan cleanup after grace |
| Eventing / Kafka-compatible boundary | Normalized object events, routing, schema evolution and DLQ | Native outbox/external inbox, deduplication, safe replay and bounded trigger loops |
| Governance and quotas | Existing plans/overrides, tenant byte and bucket limits, usage dimensions | Preserve approved fail-open governance behavior; strict mode explicit; physical disk admission always safe |
| Data analysis and application services | Large datasets, exports/imports and provider-scoped reads/writes | Streaming/range/multipart qualification; do not route large files through an unbounded base64 allocation |
| Backup/status and recovery | Current S3 backup adapter is a stub | Real provider-specific snapshot/inventory, restore status and end-to-end decrypt/read verification |
| Deployment, telemetry and operations | Ordinary workloads, existing platform services, ownership/runbooks | Namespaced RBAC, approved PVC/DNS/egress prerequisites, no assumed operator permission |

## Event contract

Versioned envelope fields: event ID/schema version, trusted tenant/workspace/binding ID, source provider, event type, key, version/delete marker if available, size/checksum if verified, occurrence/observation time, correlation/causation ID and source sequence if supplied. No secret, signed URL or object payload in the event. Preserve current `object.created`, `object.deleted` and `multipart.completed` mappings or provide a versioned compatibility adapter. A completed multipart upload must not cause two workflow invocations just because both a generic creation and completion observation exist.

Native mutation and outbox intent commit together; delivery is at least once. External notification ingestion authenticates the source, stores the inbox event before acknowledgement, deduplicates on documented provider identity and reconciles missing/uncertain observations. Ordering is per key/version where a provider supplies usable sequence information, never global. A provider event without a reliable identity needs a conservative deduplication strategy and documented limits.

Existing code models `kafka_topic` and legacy `openwhisk_action` destinations. The deployed notification configuration has not been inspected. Inventory actual rules, filters, credentials and consumers before renaming/removing destinations. Map to current Falcone workflow/serverless trigger contracts; do not deploy another OpenWhisk runtime or assume the legacy label is already obsolete.

Notification bridges require separate scope and credentials from arbitrary application webhooks. On broker failure, retain durable backlog, expose lag and apply bounded backpressure. Replay preserves original event identity. Trigger policies cap recursion when a function writes back to its own source bucket. Events indicate object changes, not exactly-once side effects or unambiguous access to a subsequently overwritten unversioned object.

## Durable references and lifecycle

Store references as logical binding ID, opaque key, immutable version or unique immutable key, checksum/algorithm, size and ownership. Provider version IDs are not portable; migration maintains a translation map and updates pinned consumers safely. A filename alone is insufficient for workflow replay or verified runtime artifacts.

Writing bytes and committing a workflow row are separate transactions. Verify upload completion before persisting the reference; quarantine failed/retried upload orphans until no in-flight job can publish them. Lifecycle cleanup honors active run/checkpoint/backup pins. End-to-end restore must recover referenced object versions and their decryption keys before declaring workflow/serverless recovery successful.
