# Open questions and working proposals

The owner confirmed a custom Falcone storage service **and** external S3 options. The following evidence is still needed at implementation gates; it does not block this architecture/backlog package. Accepted falcone-secrets proposals are reused without reopening them.

| Question | Working proposal | Gate |
|---|---|---|
| What data volume, object count/size distribution, growth and read/write/list bandwidth must we support? | Measure separately from deployed functions and event traffic; use operations.md targets as initial benchmarks | P0 sizing |
| Which storage classes and independent media/failure domains are available in restricted OpenShift? | PVC-only native baseline; three qualified domains for the proposed native HA profile, otherwise disclose delegated storage limits | Native durability |
| Which exact Kubernetes/OpenShift builds and namespaced permissions are approved? | Qualify latest two Kubernetes releases and the actual corporate OpenShift build; no new operator or privileged runtime | Deployment |
| Is TypeScript control plane plus Go data plane acceptable? | Align product APIs with Falcone TypeScript; qualify Go for streaming/native workers before commitment | P0 components |
| Which first external providers/accounts/regions must be certified? | Amazon S3 general-purpose buckets and current SeaweedFS first; other S3-compatible products through individually tested profiles | External release |
| Is external-only deployment a supported product edition? | Yes: no native workers/PVCs required; same Falcone control/auth layer | Packaging |
| May tenants adopt existing buckets and retain independent writers? | Support explicit ownership modes; show quota/audit limits and do not mutate unrelated bucket configuration | Provider binding |
| Are direct presigned reads and uploads allowed for every workload? | Proxy by default; explicit opt-in, with weaker immediate revocation and hard-quota guarantees disclosed | Governance/security |
| Which source versioning, retention, lifecycle, CORS, policy and notification features are actually used? | Inventory deployed configuration; required features block migration until equivalent destination evidence exists | Compatibility |
| Which notifications still use the legacy OpenWhisk destination model? | Preserve current configuration until a reviewed trigger adapter replaces it | Event migration |
| Must strict quota admission replace the existing fail-open governance behavior? | Preserve compatibility mode; add strict mode explicitly, keep physical-capacity safety unconditional | Product policy |
| What retention, residency, legal-hold and cryptographic qualification is required? | No WORM/compliance claim without evidence; use accepted secrets custody boundaries and provider-specific encryption profiles | Production security |
| What real availability, RPO and RTO commitments are required? | Single-region HA initially; proposed measured objectives in operations.md, full dataset recovery estimated from actual capacity | SLO/recovery |
| Which components/teams own native media, PostgreSQL, cloud accounts and on-call? | Split storage maintainers, SRE, security, IAM/governance and secrets custody responsibilities; assign named owners | Readiness |
| Which repository license should be selected? | Select explicitly before implementation-code distribution; no upstream runtime code copied in this package | Supply chain |
| What cutover window, URL expiry/drain period and rollback retention are acceptable? | Per-binding single writer, resumable verified copy, explicit external-writer fencing and reconciled rollback | P3 migration |

The highest-risk dependency is **durable native storage under the actual corporate storage failure model**. A namespace-only installation can consume approved durable storage, but cannot create independent physical failure domains. External-provider mode remains a fully supported path where native qualification or capacity is unavailable.
