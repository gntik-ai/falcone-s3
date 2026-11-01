# falcone-s3

**Falcone's custom object-storage service and provider integration layer.** It will replace Falcone's dependency on SeaweedFS when the native engine is qualified, while also allowing Amazon S3 and other qualified S3-compatible providers to remain permanent storage choices.

**Status: architecture and delivery plan; no storage runtime implemented or production data migrated.** The owner requested native and external-provider options. Detailed implementation choices below are recommendations pending the stated qualification gates.

Research date: 2026-11-01. Falcone source baseline: [`ed04fe7`](https://github.com/gntik-ai/falcone/tree/ed04fe7269d32f3f3e3cbc434ab5168389153ed6). This repository preserves Falcone interfaces, tenant/workspace isolation and product governance. It does not introduce a competing IAM, secrets manager, workflow engine or billing system.

## Architecture at a glance

Falcone APIs and an explicitly qualified S3 API share storage bindings and authorization. Each logical bucket selects **native Falcone storage** or **an external provider**. Native storage uses immutable blobs, transactional PostgreSQL metadata and qualified replication. External storage uses scoped provider credentials, capability-specific adapters and reconciliation. Provider selection never silently moves existing data.

## Documentation

| Document | Contents |
|---|---|
| [Scope and observed contracts](docs/scope-and-baseline.md) | Existing routes, code evidence and compatibility boundaries |
| [Open-source survey](docs/open-source-survey.md) | SeaweedFS, MinIO, Ceph, Swift, Garage, Ozone, RustFS, CloudServer and S3Proxy |
| [Architecture](docs/architecture.md) | Modules, diagrams, technology choices and data flows |
| [Providers and capabilities](docs/providers-and-capabilities.md) | Native, Amazon S3, generic S3, adopted buckets and direct access |
| [Protocol profile](docs/protocol-profile.md) | Falcone REST versus raw S3, signatures and SDK qualification |
| [Durability and consistency](docs/durability-and-consistency.md) | Commit protocol, replication, repair, multipart and garbage collection |
| [Security](docs/security.md) | IAM, credentials, encryption, isolation and SSRF |
| [Integration matrix](docs/integration-matrix.md) | IAM, secrets, serverless, workflows, eventing, console, data and backups |
| [Operations](docs/operations.md) | Restricted OpenShift deployment, objectives, sizing and ownership |
| [Migration](docs/migration.md) | SeaweedFS and external-provider transfers, cutover and rollback |
| [Requirements](docs/requirements.md) | 90 testable requirements |
| [Epics and user stories](docs/backlog.md) | 15 epics, 45 stories, acceptance criteria, dependencies and effort |
| [Architecture decision](docs/decisions/0001-native-and-external.md) | Baseline proposal and alternatives |
| [Open questions](docs/open-questions.md) | Focused implementation and production evidence gaps |
| [Sources](docs/sources.md) | Primary references and pinned Falcone contracts |

## Delivery order

1. **P0:** freeze Falcone contracts, provider capabilities, storage failure domains and ownership.
2. **P1:** shared façade, authorization and bindings; external Amazon S3 and existing SeaweedFS adapters; development native engine.
3. **P2:** qualify native replication/recovery, advanced capabilities and every Falcone consumer. External mode can release independently once its applicable gates pass.
4. **P3:** migrate selected buckets with a single writer, reconcile, rehearse rollback and retire SeaweedFS only where all dependencies are cleared. External providers remain supported choices.

## Backlog use

[GitHub issues](https://github.com/gntik-ai/falcone-s3/issues) use stable S3 IDs, epic task lists, parent links and dependencies. [CSV](docs/backlog.csv), [JSON](docs/backlog.json), [issue payloads](docs/issue-payloads.json) and [issue mapping](docs/github-issues.json) are included. These files support project-board population; no GitHub Project board, native sub-issue relationship or universal CSV importer is implied.

Edit `tools/build_docs.py`, then run `python3 tools/build_docs.py` to regenerate requirements and backlog. It checks IDs, requirement coverage and dependency cycles; it does not publish changes automatically. Architecture documents are maintained directly.

No upstream implementation source was copied. Select the repository license before distributing implementation code; references have different license and maintenance obligations.
