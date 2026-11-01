# Functional requirements

Baseline: 2026-11-01. Target requirements, not implemented features. Each statement maps to one story. Read with [architecture](architecture.md), [protocol](protocol-profile.md), [providers](providers-and-capabilities.md) and [security](security.md).

## Falcone contracts and first-party scope

| ID | Requirement | Story |
|---|---|---|
| FR-S3-CON-001-1 | The project must inventory every current storage route, client, bucket binding, credential path and notification configuration against a pinned Falcone revision and actual deployment evidence. | S3-CON-001 |
| FR-S3-CON-001-2 | The compatibility suite must preserve approved Falcone response schemas, status/error precedence, ownership checks and legacy aliases. | S3-CON-001 |
| FR-S3-CON-002-1 | Each logical bucket must bind to one explicit native or external provider with trusted tenant/workspace ownership and a versioned writer epoch. | S3-CON-002 |
| FR-S3-CON-002-2 | The service must retain IAM policy, secrets custody, workflow execution and quota definitions under their existing Falcone owners. | S3-CON-002 |
| FR-S3-CON-003-1 | Component selection must record maintained dependencies, license provenance, supported versions and measured control/data-plane behavior. | S3-CON-003 |
| FR-S3-CON-003-2 | Native capacity planning must measure storage demand and verify actual PVC/media and metadata failure domains before claiming HA. | S3-CON-003 |

## Provider registry and external S3

| ID | Requirement | Story |
|---|---|---|
| FR-S3-PROV-001-1 | The management API must register approved providers and create authorized bucket bindings with region, endpoint, ownership, credential reference and access mode. | S3-PROV-001 |
| FR-S3-PROV-001-2 | Every binding must expose capability state, constraints and qualification evidence, and reject operations with missing required capabilities. | S3-PROV-001 |
| FR-S3-PROV-002-1 | The Amazon adapter must support qualified bucket/object, conditional, list, multipart and presign operations for general-purpose buckets through maintained SDKs. | S3-PROV-002 |
| FR-S3-PROV-002-2 | External object state must remain authoritative at the provider, with uncertain writes recorded and reconciled instead of assuming a local atomic commit. | S3-PROV-002 |
| FR-S3-PROV-003-1 | Generic S3 adapters must qualify endpoint, region, addressing, TLS, operation semantics and limits for each supported product/release. | S3-PROV-003 |
| FR-S3-PROV-003-2 | Adopted storage must preserve unrelated data and bucket configuration and must expose any restrictions on lifecycle, quotas and audit. | S3-PROV-003 |

## Falcone API and S3 protocol

| ID | Requirement | Story |
|---|---|---|
| FR-S3-API-001-1 | The façade must preserve approved JSON/base64 and binary upload, read/range, metadata, presign, multipart and bucket lifecycle contracts. | S3-API-001 |
| FR-S3-API-001-2 | Every request must apply the existing authentication, ownership and error-precedence rules before exposing backend state. | S3-API-001 |
| FR-S3-API-002-1 | The raw S3 endpoint must implement its published operation profile, status/headers/XML errors and explicit unsupported-operation responses. | S3-API-002 |
| FR-S3-API-002-2 | SigV4 validation must bind canonical path/query/headers, payload mode, credential scope, session token and expiry without unsafe normalization. | S3-API-002 |
| FR-S3-API-003-1 | Each claimed S3 capability must have provider/profile-specific tests using pinned Falcone and mainstream SDK/client versions. | S3-API-003 |
| FR-S3-API-003-2 | The release must publish operation, header, checksum, limit and error differences instead of a blanket full-S3 claim. | S3-API-003 |

## Identity, credentials and tenant isolation

| ID | Requirement | Story |
|---|---|---|
| FR-S3-AUTH-001-1 | All storage operations must authenticate callers and authorize trusted tenant/workspace, resource, action, prefix and delegated scope through Falcone IAM. | S3-AUTH-001 |
| FR-S3-AUTH-001-2 | Cached authorization must have a configured freshness bound and deny protected operations when required authority cannot be established. | S3-AUTH-001 |
| FR-S3-AUTH-002-1 | The service must issue CSPRNG-generated access keys with scoped actions, resources, expiry and audited rotation/revocation. | S3-AUTH-002 |
| FR-S3-AUTH-002-2 | SigV4 secret material must use recoverable protected custody or a qualified signing service, separate from public key metadata. | S3-AUTH-002 |
| FR-S3-AUTH-003-1 | External provider access must use qualified workload-role exchange where available or scoped credentials resolved from falcone-secrets. | S3-AUTH-003 |
| FR-S3-AUTH-003-2 | Backend permissions and Falcone policy must intersect, with unsupported conditions rejected and adopted-bucket rights limited to granted ownership. | S3-AUTH-003 |

## Native object metadata and namespace

| ID | Requirement | Story |
|---|---|---|
| FR-S3-OBJ-001-1 | Native PUT/GET/HEAD/DELETE must operate on committed manifests and preserve bytes, size, content type and approved user metadata. | S3-OBJ-001 |
| FR-S3-OBJ-001-2 | Native per-key replacement must publish one complete version atomically after the declared durable-byte acknowledgements. | S3-OBJ-001 |
| FR-S3-OBJ-002-1 | Native conditional operations must evaluate their approved predicates atomically with mutation, and range reads must return the qualified bytes/statuses. | S3-OBJ-002 |
| FR-S3-OBJ-002-2 | Listing must filter authorized scope before pagination and use opaque query/binding-scoped continuation tokens with documented ordering. | S3-OBJ-002 |
| FR-S3-OBJ-003-1 | The versioning capability must define enable/suspend behavior, immutable version IDs, delete markers and authorized version enumeration/read/delete. | S3-OBJ-003 |
| FR-S3-OBJ-003-2 | Durable references must identify a version or immutable key plus binding, size and checksum rather than relying on a mutable filename. | S3-OBJ-003 |

## Large objects, multipart and transfer

| ID | Requirement | Story |
|---|---|---|
| FR-S3-MPU-001-1 | Multipart sessions must bind caller scope, object, provider and writer epoch, with durable part/checksum state and bounded staging capacity. | S3-MPU-001 |
| FR-S3-MPU-001-2 | Part upload must stream with bounded memory, enforce declared limits and account for replacements without leaking data across sessions. | S3-MPU-001 |
| FR-S3-MPU-002-1 | Multipart completion must have one durable terminal result and publish only a verified complete manifest or provider-confirmed outcome. | S3-MPU-002 |
| FR-S3-MPU-002-2 | Abort and expiry must release reservations and reclaim safe staged parts without deleting committed or in-flight referenced data. | S3-MPU-002 |
| FR-S3-MPU-003-1 | Copy and signed URL operations must authorize source/destination, bind required request fields and limit expiry to policy and credential lifetime. | S3-MPU-003 |
| FR-S3-MPU-003-2 | Direct external transfers must be explicit binding capabilities with declared quota, audit and revocation limits. | S3-MPU-003 |

## Native durability, repair and garbage collection

| ID | Requirement | Story |
|---|---|---|
| FR-S3-DATA-001-1 | Native writes must verify durable byte receipts before atomically committing manifest, current pointer, quota delta, audit intent and outbox state. | S3-DATA-001 |
| FR-S3-DATA-001-2 | Every publish/cleanup operation must validate its writer epoch, lease and placement generation to reject stale workers. | S3-DATA-001 |
| FR-S3-DATA-002-1 | The native HA profile must require its configured durable-copy count across verified independent domains before acknowledging writes. | S3-DATA-002 |
| FR-S3-DATA-002-2 | The system must detect corrupt/missing replicas, serve only verified data and repair under fenced placement updates with observable progress. | S3-DATA-002 |
| FR-S3-DATA-003-1 | Garbage collection must exclude live manifests, in-flight uploads/commits, retention, workflow pins and backup references under a current fence. | S3-DATA-003 |
| FR-S3-DATA-003-2 | Deletion jobs must be idempotent, retryable and observable and must not treat age alone as proof of orphanhood. | S3-DATA-003 |

## Version lifecycle, retention and configuration

| ID | Requirement | Story |
|---|---|---|
| FR-S3-LIFE-001-1 | Lifecycle, tags and CORS APIs must validate supported rules and ownership before applying native or provider configuration. | S3-LIFE-001 |
| FR-S3-LIFE-001-2 | Lifecycle execution must be resumable and observe current writer authority, versions and reference/retention constraints. | S3-LIFE-001 |
| FR-S3-LIFE-002-1 | Retention-required bindings must use a qualified capability enforcing retention and legal hold on every deletion, overwrite and cleanup path. | S3-LIFE-002 |
| FR-S3-LIFE-002-2 | The service must preserve provider retention restrictions and reject unsupported or unrepresentable lock policies before enabling a binding. | S3-LIFE-002 |
| FR-S3-LIFE-003-1 | Storage cleanup must honor authorized live workflow/artifact/backup pins and their explicit expiry/release policies. | S3-LIFE-003 |
| FR-S3-LIFE-003-2 | Reference publication and release must reconcile interrupted cross-service operations without assuming a distributed transaction. | S3-LIFE-003 |

## Object events and Falcone triggers

| ID | Requirement | Story |
|---|---|---|
| FR-S3-EVENT-001-1 | Native mutation and versioned event intent must commit atomically, with at-least-once delivery and stable event identity. | S3-EVENT-001 |
| FR-S3-EVENT-001-2 | Events must carry trusted scope, binding, key/version and safe correlation metadata without payloads or credentials. | S3-EVENT-001 |
| FR-S3-EVENT-002-1 | External notifications must authenticate their source and persist a scoped inbox record before acknowledging provider delivery. | S3-EVENT-002 |
| FR-S3-EVENT-002-2 | The bridge must tolerate duplicate/out-of-order events and expose reconciliation coverage and freshness for missed or uncertain changes. | S3-EVENT-002 |
| FR-S3-EVENT-003-1 | Storage subscriptions must use Falcone routing, authorization and quota contracts with supported prefix/suffix filters and versioned destinations. | S3-EVENT-003 |
| FR-S3-EVENT-003-2 | Trigger delivery must support retries, dead letters and replay while preserving identity and preventing unbounded self-trigger loops. | S3-EVENT-003 |

## Falcone quotas, usage and fairness

| ID | Requirement | Story |
|---|---|---|
| FR-S3-QUOTA-001-1 | Admission must consume Falcone quota definitions and preserve the approved compatibility fail-open behavior for governance lookup failures. | S3-QUOTA-001 |
| FR-S3-QUOTA-001-2 | Strict native admission must atomically reserve capacity for concurrent writes/bucket creation and always enforce physical safety limits. | S3-QUOTA-001 |
| FR-S3-QUOTA-002-1 | Usage must distinguish current logical bytes, retained versions, multipart/staging, physical replication and transfer/request dimensions. | S3-QUOTA-002 |
| FR-S3-QUOTA-002-2 | External usage reports must include observation freshness, pending/uncertain operations and reconciliation results for out-of-band changes. | S3-QUOTA-002 |
| FR-S3-QUOTA-003-1 | A binding requiring strict per-request Falcone governance must reject access paths or independent writers that bypass its enforcement guarantees. | S3-QUOTA-003 |
| FR-S3-QUOTA-003-2 | Gateway and background workers must apply configurable tenant fairness, concurrency, bandwidth and queue limits from Falcone policy. | S3-QUOTA-003 |

## Encryption, secret custody and network security

| ID | Requirement | Story |
|---|---|---|
| FR-S3-KEY-001-1 | Native encryption must use reviewed AEAD framing and unique nonce/key handling with authenticated tenant/object/version/chunk context. | S3-KEY-001 |
| FR-S3-KEY-001-2 | Key rotation and retirement must preserve decryptability of all authorized live versions and recoverable backups until their required key dependencies expire. | S3-KEY-001 |
| FR-S3-KEY-002-1 | Bindings and access-key metadata must store secret references rather than provider secret values, with bounded protected resolution caches. | S3-KEY-002 |
| FR-S3-KEY-002-2 | Storage bootstrap and recovery must have independent access to required root custody, database/TLS identity and recovery material. | S3-KEY-002 |
| FR-S3-KEY-003-1 | Provider connections must enforce registered endpoint/TLS/egress policy including redirect and DNS-rebinding checks and approved private-network exceptions. | S3-KEY-003 |
| FR-S3-KEY-003-2 | Parsers, logs and audit paths must enforce resource limits and redact payloads, credentials and sensitive signed URL data. | S3-KEY-003 |

## Falcone consumer integration

| ID | Requirement | Story |
|---|---|---|
| FR-S3-INT-001-1 | Runtime artifact/output/checkpoint access must use tenant/workspace/attempt-scoped grants and verified immutable references. | S3-INT-001 |
| FR-S3-INT-001-2 | Runtime integration must work with qualified native and external providers without exposing broad backend credentials to tenant code. | S3-INT-001 |
| FR-S3-INT-002-1 | Existing storage activities and custom falcone-workflow consumers must preserve their response/error contracts across selected providers. | S3-INT-002 |
| FR-S3-INT-002-2 | Large workflow payloads must be uploaded and verified before committing durable references with lifecycle pins and recoverable version mapping. | S3-INT-002 |
| FR-S3-INT-003-1 | Console/SDK/data-service flows must expose allowed provider selection, capability limits and usage freshness while preserving existing storage operations. | S3-INT-003 |
| FR-S3-INT-003-2 | The backup-status adapter must report real provider-specific support and verified backup/restore results instead of replacing the existing stub with assumed success. | S3-INT-003 |

## Deployment, observability and recovery

| ID | Requirement | Story |
|---|---|---|
| FR-S3-OPS-001-1 | Baseline installation must use ordinary workloads/PVCs and namespace-scoped permissions without new operators, CRDs, privileged containers or custom SCC prerequisites. | S3-OPS-001 |
| FR-S3-OPS-001-2 | External-only mode must omit native byte workers and storage volumes while retaining the same Falcone management/security interfaces. | S3-OPS-001 |
| FR-S3-OPS-002-1 | Telemetry must report provider/operation availability, latency, capacity, integrity, repair debt, credential health and event/reconciliation lag without unbounded sensitive labels. | S3-OPS-002 |
| FR-S3-OPS-002-2 | The release must publish measured SLOs, capacity assumptions, dependency failure behavior and assigned on-call/patch responsibilities. | S3-OPS-002 |
| FR-S3-OPS-003-1 | Native backup must capture a recoverable metadata point and all referenced blobs/key versions while protecting them from premature GC. | S3-OPS-003 |
| FR-S3-OPS-003-2 | Every supported production provider profile must have a tested restore procedure with measured RPO/RTO and required workflow/artifact verification. | S3-OPS-003 |

## Migration, cutover and SeaweedFS retirement

| ID | Requirement | Story |
|---|---|---|
| FR-S3-MIG-001-1 | Migration inventory must include bytes, versions/delete markers, metadata/tags, retention, credentials, consumers, active uploads and notification rules. | S3-MIG-001 |
| FR-S3-MIG-001-2 | Transfers must be resumable, scoped and checksum-verified with provider version/reference translation and visible unsupported features. | S3-MIG-001 |
| FR-S3-MIG-002-1 | Cutover must quiesce/fence writers, verify final differences and atomically update the authoritative binding epoch and routing. | S3-MIG-002 |
| FR-S3-MIG-002-2 | Rollback must reconcile post-cutover writes, versions, deletions, retention and reference mappings before returning authority to the old provider. | S3-MIG-002 |
| FR-S3-MIG-003-1 | SeaweedFS retirement must require all affected bindings/consumers and rollback dependencies to pass their migration and recovery gates. | S3-MIG-003 |
| FR-S3-MIG-003-2 | Retirement must remove obsolete credentials, routes and infrastructure only after approved retention and recovery obligations are met. | S3-MIG-003 |

## Developer tooling and independent qualification

| ID | Requirement | Story |
|---|---|---|
| FR-S3-DEV-001-1 | The repository must publish versioned management/event/binding schemas and SDK examples distinguishing Falcone REST and raw S3. | S3-DEV-001 |
| FR-S3-DEV-001-2 | Local fixtures must include multiple tenants, native development storage and mock/isolated external profiles with no real credentials. | S3-DEV-001 |
| FR-S3-DEV-002-1 | Releases must pin dependencies/images, publish SBOM and signed provenance and review licenses and security updates. | S3-DEV-002 |
| FR-S3-DEV-002-2 | The project must define supported versions, vulnerability reporting, patch ownership and compatibility/schema-upgrade gates. | S3-DEV-002 |
| FR-S3-DEV-003-1 | Production candidates must pass profile-specific protocol, cross-tenant, credential, retention, failure and recovery qualification with reviewable evidence. | S3-DEV-003 |
| FR-S3-DEV-003-2 | Native qualification must verify acknowledged-write recovery and per-key consistency under crashes, partitions, corruption and stale-worker races. | S3-DEV-003 |

