# Native and external provider modes

## Binding and configuration model

Each logical bucket has an explicit provider binding. The tenant/workspace default selects the profile for **new** bindings only. Changing a default neither migrates existing objects nor rewrites existing URLs. Backend changes require the [migration protocol](migration.md).

| Configuration | Purpose and rule |
|---|---|
| Provider ID and adapter/profile version | `native`, `aws-s3-general`, or a qualified S3-compatible profile; exact releases and test evidence recorded |
| Tenant/workspace and logical bucket ID | Authoritative Falcone scope; never derived from an arbitrary client header |
| Backend bucket and optional prefix | Stable physical mapping. Dedicated backend bucket is the normal allocation model; shared-prefix adoption is constrained |
| Ownership | `managed` permits explicitly granted lifecycle actions; `adopted` initially probes read-only and preserves customer configuration |
| Endpoint, region and addressing | Internal/public endpoints, path/virtual-host mode, TLS trust and approved network destination policy |
| Credential reference or workload role | References only; no secret values in bindings, logs, exports or public API responses |
| Access mode | Governed proxy default; direct read/upload must be explicitly enabled and compatible with the chosen policy |
| Capabilities | `satisfied`, `partially_satisfied`, `unsatisfied`, with constraints, evidence and expiry/revalidation rules aligned to current Falcone contracts |
| Policy/residency/encryption | IAM resource mapping, region boundary, retention and provider/native key profile |
| Writer epoch and migration state | Fence jobs and route changes; no automatic data-provider failover |

The operator registers allowed endpoints/profiles. A tenant administrator can bind only profiles permitted by Falcone entitlements and IAM; bring-your-own storage requires validated ownership and scope. Endpoint registration is not arbitrary HTTP proxy permission.

## Qualification matrix

All cells describe the **target**, not implemented support. `Gate` means the feature stays unavailable until its dedicated story and provider tests pass.

| Capability | Native baseline/HA target | Amazon S3 general-purpose adapter | Other S3-compatible endpoint |
|---|---|---|---|
| Bucket/object CRUD, HEAD, byte ranges | Required | Required | Required for baseline qualification |
| Content type, user metadata, separate integrity checksum | Required | Qualified checksum mapping | Profile-specific algorithms; no ETag-as-MD5 assumption |
| ListObjectsV2, prefix/delimiter, opaque pagination | Required | Delegate and scope tokens | Verify ordering, continuation and scope boundaries |
| Conditional GET/PUT/delete/copy variants | Operation/header-specific gate | Test actual SDK and API variants | Reject unsupported variants; never emulate CAS with HEAD+write |
| Multipart/resume/abort/copy | Required tested subset | Required tested subset | Gate limits, checksums, part ordering and copy behavior |
| SigV4 and presigned GET/PUT | Required tested forms | SDK-based signing | Qualify signing/addressing differences |
| Versioning/delete markers | P2 gate; required before migrating in-use versions | Delegate with ID mapping | Capability-specific, not assumed |
| Bucket policy | Bounded Falcone policy projection | Intersection with provider IAM/bucket policy | Reject unrepresentable conditions |
| Lifecycle, tags and CORS | P2/profile gates | Delegate only with ownership rights | Test semantics and configuration scope |
| Retention/Object Lock/legal hold | P2 independent qualification | Preserve authoritative provider retention | Unsupported providers cannot host retention-required bindings |
| Encryption | Native envelope encryption | SSE-S3/SSE-KMS profile and access checks | Provider-specific, never relabeled as native envelope guarantees |
| Notifications | Atomic native outbox | SQS/EventBridge bridge plus reconciliation | Polling/bridge only where qualified; disclose completeness/lag |
| Quota admission | Governed proxy; atomic native reservation target | Proxy reservations plus reconciliation | Depends on external writers and access mode |
| Backup/restore and disaster recovery | Native coordinated metadata/bytes/keys | Version/backup policy plus tested recovery | No universal S3 backup API; profile-specific evidence |

Unknown capability is unavailable. Capability probes must be non-destructive by default; test-bucket writes require explicit ownership and configured scope. Requalify after provider/SDK changes. For SeaweedFS, qualify the deployed source version and the latest two stable releases at qualification time; pin the actual versions and image digests then, rather than treating “latest” as a reproducible release.

## Amazon S3 path

Prefer short-lived AWS role credentials through an approved workload identity/federation path. A Falcone OIDC token is not automatically an AWS credential: AWS trust, audience, subject and policy must explicitly permit the exchange. Where that is unavailable, use scoped access keys managed and rotated by falcone-secrets. Do not give the tenant the broad backend signing credential.

Presign against the externally reachable endpoint with the correct region and signed headers. Enforce an expiry bounded by both requested TTL and credential lifetime. Expired or revoked temporary credentials can invalidate a URL earlier. Falcone policy revocation alone does not necessarily revoke an already issued provider URL. Avoid fixed promises of instantaneous revocation or strict arbitrary upload-size enforcement for presigned PUT.

Configure notification ingestion using an authenticated AWS queue/EventBridge path with least-privilege queue access and verified origin. Preserve existing bucket notification rules when permitted; do not overwrite an adopted bucket's configuration. Record egress, request, KMS and retention cost drivers without embedding unverified prices in quotas.

## Adopted buckets and direct access

Adoption must distinguish read-only, read/write and lifecycle ownership. A scoped prefix does not provide independent bucket-level versioning, notification, CORS, lifecycle or retention configuration. A managed Falcone bucket-delete operation must never delete unrelated adopted data or a customer's entire bucket. If the requested existing Falcone lifecycle contract cannot be safely met, reject that binding/profile or require a separately exposed constrained adoption API.

Public anonymous access is disabled by default. Direct access is an opt-in contract: audit covers URL issuance and whatever provider logs/events are configured; external request visibility, quotas and revocation are bounded accordingly. Quota-strict workloads require a fully governed write path and exclusion of uncontrolled external writers. Even a proxy cannot enforce hard quotas against writes made using independent provider credentials.

## Extension contract

Adapters implement capability discovery, scoped CRUD/list/conditional operations, multipart, presign, health, credential refresh, optional configuration/events and outcome reconciliation. Provider errors map to the existing Falcone taxonomy while preserving safe retry/uncertainty metadata. Adapter code is trusted platform code, shipped with reviewed releases; tenant-supplied in-process plugins are out of scope.
