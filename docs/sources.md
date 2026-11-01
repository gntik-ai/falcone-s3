# Sources and evidence register

Checked 2026-11-01. Prefer these primary sources to secondary comparison tables. Upstream capability claims are reference material, not Falcone qualification. Architecture choices, priorities and proposed SLOs are this project's recommendations. No third-party runtime source was copied into this plan.

## Open-source and protocol references

| Source | Used for |
|---|---|
| [SeaweedFS repository](https://github.com/seaweedfs/seaweedfs) and [architecture](https://github.com/seaweedfs/seaweedfs/wiki/SeaweedFS_Architecture.pdf) | Component separation, storage design and Apache-2.0 core; distinguish enterprise additions |
| [MinIO repository/README](https://github.com/minio/minio) and [commit history](https://github.com/minio/minio/commits/master/) | Historical S3 feature reference, AGPL and present archived/unmaintained upstream status; do not substitute AIStor terms |
| [Ceph Object Gateway](https://docs.ceph.com/en/latest/radosgw/) and [source S3 compatibility documentation](https://github.com/ceph/ceph/blob/main/doc/radosgw/s3.rst) | Gateway/RADOS architecture and per-operation S3 compatibility |
| [Ceph repository license](https://github.com/ceph/ceph/blob/main/COPYING) | Mixed component license review; no blanket permissive-license assumption |
| [OpenStack Swift repository](https://github.com/openstack/swift) and [middleware reference](https://docs.openstack.org/swift/latest/middleware.html) | Object-storage architecture and the s3api compatibility middleware |
| [Garage canonical project](https://git.deuxfleurs.fr/Deuxfleurs/garage), [mirror](https://github.com/deuxfleurs-org/garage) and [S3 compatibility](https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/) | Distributed subset and explicit operation constraints; its comparisons to other products require independent checking |
| [Apache Ozone architecture](https://ozone.apache.org/docs/core-concepts/architecture/) and [S3 gateway](https://ozone.apache.org/docs/core-concepts/architecture/s3-gateway/) | Namespace/storage management and S3 gateway separation |
| [RustFS repository](https://github.com/rustfs/rustfs), [releases](https://github.com/rustfs/rustfs/releases) and [GA announcement](https://rustfs.com/blog/announcing-rustfs-1-0-0-ga/) | Rust implementation, Apache-2.0, distributed engine and September 2026 upstream GA status; no performance/certification inference |
| [Scality CloudServer](https://github.com/scality/cloudserver) | S3 frontend and backend adapters, Apache-2.0 project |
| [S3Proxy](https://github.com/gaul/s3proxy) | S3-to-backend translation and capability limitations, Apache-2.0 |
| [Amazon S3 consistency](https://aws.amazon.com/s3/consistency/) | Strong object and listing consistency; not a Falcone/provider distributed transaction |
| [AWS SigV4 header signing](https://docs.aws.amazon.com/AmazonS3/latest/developerguide/sig-v4-header-based-auth.html), [query signing](https://docs.aws.amazon.com/AmazonS3/latest/developerguide/sigv4-query-string-auth.html), [streaming](https://docs.aws.amazon.com/AmazonS3/latest/developerguide/sigv4-streaming.html) and [trailers](https://docs.aws.amazon.com/AmazonS3/latest/developerguide/sigv4-streaming-trailers.html) | Canonicalization, payload variants and presign contract |
| [AWS notification destinations/order](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html) and [event structure](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html) | At-least-once unordered delivery, per-key sequencer and encoded keys |

Amazon S3 is included as an external service/protocol reference, not an open-source project. Licenses are intake observations, not a legal conclusion about a future combined distribution. Pin selected dependency versions and review their actual files/notices before reuse.

## Pinned Falcone implementation baseline

All following paths were inspected at `gntik-ai/falcone@ed04fe7269d32f3f3e3cbc434ab5168389153ed6`:

- [SeaweedFS runbook](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs-site/architecture/seaweedfs.md).
- [Object I/O contract](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs/reference/architecture/storage-object-io.md) and [capacity/quota document](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs/reference/architecture/storage-capacity-quotas.md).
- [Runtime storage handlers](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/storage-handlers.mjs), [quota helper](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/storage-quota.mjs) and [SeaweedFS identities](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/seaweedfs-identity.mjs).
- [Storage OpenAPI family](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane-executor/openapi/families/storage.openapi.json).
- [Provider profiles](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-provider-profile.mjs) and [verification builders](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-provider-verification.mjs).
- [Tenant context](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-tenant-context.mjs) and [logical key organization](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-logical-organization.mjs).
- [Programmatic credentials](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-programmatic-credentials.mjs) and [access policies](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-access-policy.mjs).
- [Multipart/presign models](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-multipart-presigned.mjs) and [notification models](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/adapters/src/storage-event-notifications.mjs).
- [Provisioning compatibility matrix](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/provisioning-orchestrator/src/config/seaweedfs-compat-matrix.json).
- [Workflow storage activity](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/workflow-worker/src/activities/storage-get.mjs) and [S3 backup adapter stub](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/backup-status/src/adapters/s3.adapter.ts).

Source-only inspection cannot establish live versions, actual notification destinations, storage capacity, infrastructure permissions or recoverability. Those are explicit backlog gates.

## Sibling-service baselines and owner decisions

| Service | Inspected baseline | Interpretation |
|---|---|---|
| [IAM architecture](https://github.com/gntik-ai/falcone-iam/blob/7e3ad9f772494a67d06674a2fea7081417dc7d3d/docs/architecture.md) | `7e3ad9f` | Identity/policy authority; SAML/OIDC/LDAP/AD/SCIM confirmed by owner |
| [Secrets architecture](https://github.com/gntik-ai/falcone-secrets/blob/f9e078211fe58ad25c1490ff74ed13f9af5cd808/docs/architecture.md) and [accepted decisions](https://github.com/gntik-ai/falcone-secrets/blob/b3f5688e12e6e9db9588601075e85aa8f1580431/docs/decisions/0002-owner-acceptance.md) | `f9e0782`, acceptance `b3f5688` | Owner accepted all proposals without changes on 2026-11-01; existing qualification gates remain |
| [Workflow architecture](https://github.com/gntik-ai/falcone-workflow/blob/b26c6e777211629f41ad3f251bf0059de8003219/docs/architecture.md) | `b26c6e7` | Durable reference, upload/commit and retention integration; not a running implementation claim |
| [Serverless contract inventory](https://github.com/gntik-ai/falcone-serverless/blob/0e41c6768e1eccf3ac85d22dbdd4914bac63760b/docs/contracts/falcone-contract-inventory.md) | `0e41c67` | Runtime artifact/checkpoint and scope handoffs; preserve each decision's status |

This plan does not silently promote proposed sibling contracts to production guarantees. Integration changes require cross-repository fixtures and reviewed rollout evidence.
