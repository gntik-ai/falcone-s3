# Scope and current Falcone baseline

## Product intent

Build a first-party Falcone service for object bytes, metadata, bucket lifecycle and provider routing. Both a native engine and permanently supported external providers are required. Compatibility concerns **Falcone's public APIs, URLs, data contracts, workspace ownership and application behavior**. The separately exposed S3 endpoint has a documented operation/profile matrix, not a promise to implement every Amazon S3 service.

Corporate deployment must work on Kubernetes and restricted OpenShift with ordinary namespaced workloads, pre-provisioned storage classes and no new operator, custom SCC, host access, raw-device access or CRD prerequisite. Existing cluster services can be consumed with approved permissions. Hostile tenant functions receive scoped storage grants through their runtime boundary; storage does not solve their missing sandbox.

The earlier estimates of 20 tenants, 10,000 **deployed functions**, and 100k event/WebSocket messages per second are not object count, S3 request rate or storage bandwidth measurements. Storage requires separate sizing.

## Source evidence

Inspected Falcone commit: `ed04fe7269d32f3f3e3cbc434ab5168389153ed6`. Paths below are linked in [sources](sources.md). No live cluster, credentials, object inventory or production configuration was inspected.

| Evidence | Observed behavior | Design consequence |
|---|---|---|
| `docs-site/architecture/seaweedfs.md` | SeaweedFS 4.33 image/digest pin, master/volume/filer/S3 layers, dedicated PostgreSQL filer database | Preserve source compatibility; qualify actual deployed version rather than assuming latest |
| `apps/control-plane/storage-handlers.mjs` | `/v1/storage/*`, workspace authorization, S3 internal/public endpoints and legacy MINIO aliases | Keep façade routes and host-aware presigning; avoid permanent vendor-named configuration |
| `storage-object-io.md` | Base64 JSON envelopes, binary upload, ranges, multipart, presign and recursive product bucket deletion | Freeze fixtures independently from raw S3 semantics |
| `seaweedfs-identity.mjs` | Per-bucket scoped identities and credential application using Kubernetes Jobs | Replace vendor provisioning mechanism with provider adapters; do not grant broad bucket access |
| `storage-tenant-context.mjs` | Tenant/workspace lifecycle, plan metrics and bucket bindings | Extend the existing registry; no independent tenant hierarchy |
| `storage-provider-profile.mjs`, `storage-provider-verification.mjs` | Existing capability and verification models | Reuse/version contracts; builder output alone is not qualification evidence |
| `storage-programmatic-credentials.mjs`, `storage-access-policy.mjs` | Scoped credentials, action/prefix policy and TTL modeling | Implement secure credential lifecycle and deny unsupported policy clauses |
| `storage-event-notifications.mjs` | Object created/deleted and multipart completed, filters; destination models include Kafka and legacy OpenWhisk | Inventory deployed configuration and migrate through Falcone's event/trigger contracts |
| `storage-quota.mjs` | Tenant byte admission via governance `max_storage_bytes`; legacy bucket/environment helpers; governance errors fail open | Preserve current behavior through fixtures; introduce stricter modes explicitly |
| `storage-logical-organization.mjs` | Bucket-per-workspace registry is canonical; legacy prefixes only organize keys inside a bucket | Never reintroduce prefix-per-tenant as the allocation default |
| Workflow `activities/storage-get.mjs` | Storage activity uses Falcone service contracts | Use the same façade and scoped references for existing workflow consumers |
| `packages/backup-status/src/adapters/s3.adapter.ts` | Backup adapter is explicitly a stub with unsupported operations | Implement real backup status and evidence; no existing recovery guarantee can be inferred |

Some docs lag code: the SeaweedFS runbook describes per-workspace identities while current code provisions per-bucket identities; older quota docs emphasize workspace/environment limits while current byte admission uses tenant governance. P0 must resolve these using source fixtures plus actual deployment evidence. These are compatibility investigation tasks, not permission to silently change behavior.

## Boundaries

- Falcone IAM owns identity, federation, roles and authorization policy. The confirmed SAML/OIDC/LDAP/AD/SCIM requirement stays there.
- Falcone secrets owns provider credentials, native wrapping-key operations and their rotation. Its open-point proposals were accepted without changes on 2026-11-01; see its ADR 0002.
- Falcone owns quota definitions, entitlements and product accounting. Storage supplies admission reservations and usage facts.
- Falcone workflow owns durable execution; serverless owns execution/runtime grants. Storage owns durable artifacts and scoped retrieval, not scheduling.
- Existing SeaweedFS is retained during qualification. Its filer schema, master protocol and volume layout need not become native Falcone internals.
- No full AWS IAM policy language, cross-object transaction, POSIX filesystem, global active-active engine, Glacier retrieval service or S3 Tables implementation is included in the first release.

Provider neutrality applies to Falcone contracts. Provider-specific durability, retention, conditional operations, credential revocation and event lag remain visible capabilities.
