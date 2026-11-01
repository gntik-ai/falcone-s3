# Security and credential boundaries

## Identity and isolation

Falcone IAM authenticates and authorizes users/workloads. Verify issuer, audience, expiry and delegated resource/action scope. Storage independently enforces tenant/workspace/bucket/prefix ownership; forwarded headers, guest IDs, object metadata and Kubernetes labels are not authority. Policy grants intersect with backend privileges; backend overprivilege never expands a Falcone grant. Deny wins and unsupported policy conditions are rejected.

Management identities, data-plane keys, migration credentials and emergency operator permissions are separate. List, count, presign, metadata, version, multipart and notification APIs all need scoped checks, not only GET/PUT. Use the existing product error precedence and cross-tenant concealment fixtures. A proposed maximum cached authorization age is 30 seconds; expired/stale decisions deny new protected operations. In-flight streams and direct external URLs require explicit cancellation/revocation limits.

S3 SigV4 uses a symmetric signing secret. Unlike a password/API-token verifier, its server-side verification generally needs recoverable secret material or a restricted signing/HMAC service. Store access-key metadata separately from encrypted/recoverable material in falcone-secrets; do not claim a one-way hash is sufficient for S3 verification. Generate actual keys with a CSPRNG; deterministic builder fixtures in the current code are not credential issuance.

Expose secrets only at controlled issuance where required, never through list APIs. Scope keys by tenant/workspace, bucket/prefix, actions and expiry; audit creation/rotation/revocation and bound caches. Short-lived execution grants are preferred for functions. Never inject a broad platform S3 root credential into arbitrary tenant code.

## Encryption and accepted secrets integration

Native chunks use authenticated envelope encryption with per-object/version keys, approved algorithms and unambiguous framing. AAD binds tenant, binding, object version and chunk position; immutable data cannot be transplanted across scopes. falcone-secrets manages wrapping-key references, rotation and permitted unwrap operations. Do not invent cryptography or a new root-custody hierarchy inside storage. Scrubbing can verify stored ciphertext integrity without keeping every plaintext key resident; full decrypt verification is a distinct controlled operation.

Key rotation retains required old key versions until live objects, replicas, retained versions and recoverable backups are rewrapped or expired. Emergency key disable has explicit availability impact. Native envelope encryption is distinct from an external provider's SSE-S3/SSE-KMS features; test the applicable provider/KMS access and recovery behavior. Client-side encryption is an optional separate profile because it changes range/copy/checksum and key-recovery handling.

The owner accepted all falcone-secrets open-point proposals on 2026-11-01. Its independent root-custody preference and conditional recovery profiles remain authoritative. The only database credential, unlock key, TLS bootstrap identity or recovery copy must not live solely in an S3 bucket that needs this service and those keys to start. Restore metadata, blob data and key custody as a coordinated dependency set.

## Network and hostile input

External endpoints are registered under an operator-controlled allowlist including approved private networks. Block arbitrary schemes, redirects to unapproved hosts, metadata/control endpoints and DNS-rebinding escapes; reevaluate connections after resolution. Corporate private endpoints remain possible through explicit policy, not a blanket “public IP only” rule. Validate TLS hostname/CA, signing host and region; never log presigned query strings.

Use non-root arbitrary-UID containers, read-only root filesystem where practical, writable approved volumes, dropped capabilities, scoped service accounts, NetworkPolicies and restricted egress. Tenant code is not loaded into the storage gateway or workers. Ordinary containers alone are not a hostile-code sandbox, and cluster administrators remain part of the infrastructure trust model.

Enforce XML/JSON/header size limits, bounded decompression, parser entity restrictions, upload deadlines and multipart resource limits. Defend authorization on CopyObject source and destination, malicious metadata, oversized list filters, bad Unicode/encoding and request smuggling. Provider adapters are reviewed platform code.

## Audit, retention and review

Durably record native mutation audit intent with commit; external operations use an operation journal and reconcile uncertain outcomes. Direct external access needs provider logs to make per-request audit claims. Redact credentials, signed URLs, payloads and sensitive object names; use bounded-cardinality metrics and controlled audit access. Object keys can contain personal data.

Object Lock/retention is a dedicated capability with all mutation paths tested, including lifecycle, cleanup, replication and restore. A database flag is not a WORM certification. No administrator bypass is inferred for compliance retention, and a copied object may not preserve original legal semantics. Independent security and durability review is required before production trust moves from SeaweedFS to the native engine.
