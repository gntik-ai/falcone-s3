# Open-source references and feature selection

Research checked 2026-11-01 against [primary sources](sources.md). This is a focused architecture survey, not a claim to enumerate every object store. Feature availability must be pinned to an edition, release and configured profile. None of the advertised performance figures substitutes for a Falcone benchmark.

| Reference | Features and scaling model | Extension/integration pattern | Strengths for Falcone | Costs or gaps to avoid | License/status evidence |
|---|---|---|---|---|---|
| **SeaweedFS** | Blob volumes, separate filer metadata and S3 gateway; distribute volumes and gateways, with replication and configurable metadata stores | Multiple protocols, metadata backends and notification integrations | Current integration baseline; useful separation of namespace and byte storage | Multi-component operations; provider/version-specific S3 behavior; current per-bucket SQL/provisioning quirks need not be copied | Apache-2.0 core; distinguish enterprise additions |
| **MinIO** | S3-focused API, distributed erasure coding, versioning, lifecycle, object locking and events in historical releases | Identity/KMS/event integrations and S3 tooling | Rich compatibility and negative-test reference; existing customer installations can be adapter targets | Upstream `minio/minio` is archived and says it is no longer maintained; security ownership must be explicit for existing deployments | AGPL-3.0; archived April 2026. Commercial AIStor is a separate offering |
| **Ceph RGW** | S3/Swift gateway over RADOS; independent gateways, placement pools, replication/EC and multisite | Gateway APIs, identity integrations, eventing and backend storage policies | Mature model for data placement, repair and tenancy; good external endpoint candidate | Full Ceph cluster is operationally substantial; ordinary namespace access does not grant disk/operator capabilities | Mixed component licenses, including LGPL-family/GPL-family terms; inspect chosen files and distribution |
| **OpenStack Swift** | Distributed object/container/account services, rings, replication or EC; S3 via middleware | WSGI middleware, auth integration and storage policies | Reference for repair, audit, independent scaling and backend abstraction | S3 compatibility is an added layer; consistency and operation support require testing, not assuming Amazon semantics | Apache-2.0 project |
| **Garage** | Distributed S3 subset, replicated metadata/data and topology-aware placement | S3 and administrative APIs; deployment/topology configuration | Smaller operational footprint; useful topology and explicit-compatibility documentation | Partial S3 feature surface; do not advertise unsupported IAM, retention or versioning semantics | AGPL-3.0; check canonical project and pinned release |
| **Apache Ozone** | Object namespace manager, storage container management, datanodes and S3 gateway | S3/Hadoop interfaces, separate metadata and storage services | Useful namespace/data separation and scale-out design reference | More infrastructure and concepts than Falcone's restricted baseline; Hadoop integration is not a Falcone requirement | Apache-2.0 |
| **RustFS** | Rust S3-compatible distributed storage; distributed layout, erasure coding and storage-management features | S3 clients, console and deployment integrations | Permissive reference for native object-engine implementation and modern SDK behavior | Newer operational history than Ceph/Swift; qualify a pinned release and security fixes. Upstream GA announcement is not Falcone production evidence | Apache-2.0; upstream announced 1.0 GA in September 2026 |
| **Scality CloudServer** | S3 API server with metadata/data backend separation and multiple backend options | Pluggable backend/auth integrations | Strong reference for separating S3 protocol behavior from storage placement | Gateway behavior does not by itself supply native durability; deployment-specific backend semantics remain | Apache-2.0 project; distinguish commercial Scality products |
| **S3Proxy** | S3 façade translating requests to backend blob stores | jclouds-backed provider adapters | Useful external-provider abstraction and compatibility-matrix pattern | Translation cannot create missing atomicity, retention or consistent listing; not a native distributed storage engine | Apache-2.0 |

## Functional lessons to adopt

| Capability | Reference lessons | Falcone implementation decision |
|---|---|---|
| Core S3 | MinIO, Ceph, CloudServer expose the value of stable protocol behavior | Explicit SDK-tested operation profiles; preserve Falcone REST separately |
| Metadata/data separation | SeaweedFS, Ozone and CloudServer separate responsibilities | PostgreSQL binding/native metadata plus immutable byte workers; external provider remains object authority |
| Durability | Ceph, Swift and distributed stores make failure-domain placement and repair first-class | Qualify durable acknowledgements, checksums, repair and restore before a native HA claim |
| Storage efficiency | EC and compact storage can lower raw capacity cost | Replication first; defer custom EC, pack-file compaction and cross-tenant deduplication |
| Multi-tenancy | Projects differ in accounts, IAM and bucket policies | Falcone tenant/workspace and IAM are authoritative; least-privilege backend projection |
| Encryption | KMS integrations separate keys from storage media | Use accepted falcone-secrets boundary and independent root recovery; provider KMS remains a capability |
| Events | Bucket notifications are useful but do not make consumers transactional | Native outbox, external durable inbox, idempotent triggers and reconciliation |
| Provider adapters | S3Proxy and CloudServer show how one product can reach multiple stores | Explicit binding and qualification per provider; never silently weaken semantics |

## Amazon S3 as a supported external service

Amazon S3 is a proprietary managed service, **not an open-source reference**. The initial adapter targets general-purpose buckets with SigV4, scoped access and qualified basic/multipart operations. AWS documents strong object read/write and listing consistency; that does not imply cross-object transactions or atomic updates to Falcone's database. Notifications can duplicate and arrive out of order. Direct access needs separate governance and audit expectations. Directory/Express buckets, access points, archival restore, tables and vendor-specific features require distinct later profiles.

## Recommendation and trade-offs

Build a custom Falcone control/protocol layer with native and external adapters. Shipping the external path first reduces the time to validate Falcone contracts while native storage undergoes failure testing. A façade over SeaweedFS alone is a useful migration step, but does not satisfy the requested native replacement. Forking an entire storage project inherits its operational, licensing and patch surface. Reusing maintained protocol/crypto/client libraries is preferable to inventing cryptography or consensus.

Replication uses more storage than erasure coding but makes the first native recovery protocol simpler to validate. PostgreSQL limits the initial metadata scale but offers transactions, fencing and operational familiarity. Split metadata by an explicit shard key only after measured contention; do not add a custom consensus system speculatively.
