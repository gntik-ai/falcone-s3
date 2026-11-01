# Compatibility and protocol profile

## Two interfaces, two contracts

| Operation | Existing Falcone façade to preserve | Raw S3 target |
|---|---|---|
| Object upload | `/v1/storage/*`; primary `contentBase64`, accepted legacy content/encoding envelope and raw binary path; content type and metadata preserved | PUT with streaming bytes and S3 headers; no JSON/base64 wrapper |
| Object read | JSON `contentBase64`, `encoding`, size/content type and IDs; avoid lossy UTF-8 conversion | Raw byte body, S3 response headers and SDK-readable errors |
| Empty content | Empty byte upload succeeds; malformed/explicit empty JSON request rejected as contracted | Zero-byte object PUT is valid |
| Range | Existing 206 JSON partial-body envelope; mapped 416 `STORAGE_RANGE_NOT_SATISFIABLE` | Qualified HTTP Range behavior and S3 errors; multiple-range behavior explicitly specified |
| Bucket ownership failure | Authenticate and scope-check before provider lookup/body validation where current contract requires; cross-scope `BUCKET_NOT_FOUND` | S3 authorization/error rules with tested anti-enumeration boundary |
| Delete bucket | Product API recursively removes owned objects and registry state, returning its existing envelope | DeleteBucket rejects a nonempty bucket; no implicit recursive delete |
| Multipart completion | Current façade validates nonempty, ordered, gap-free parts starting at 1 | S3 profile follows its own part-number/checksum rules; do not impose façade-only constraints |
| Presign | Existing endpoint and default 3600/max 604800-second clamp; effective expiry may be shorter | SigV4 query signature bound to host, key, method, headers and credential lifetime |

Fixture source: pinned storage handlers, object-I/O document and storage OpenAPI family. Resolve code/document discrepancies in S3-CON-001 before treating them as release contracts. New streaming APIs are versioned additions; don't silently replace JSON responses or introduce arbitrary smaller limits for existing clients.

## Required first S3 profile

Bucket create/head/list/delete where authorized; PutObject, GetObject, HeadObject, DeleteObject, ListObjectsV2; approved CopyObject and multipart operations; metadata/content type; qualified checksum algorithms, range and conditional variants; presigned GET/PUT. Versioning, tags, policy, CORS, lifecycle, retention and notification APIs are separate gates. ListBuckets must filter authorized logical buckets before returning names; it must never enumerate a shared backend credential's full account.

Unsupported operations fail explicitly using documented S3 XML errors and status codes; do not return success for ignored headers or policy clauses. Match namespace handling, request IDs, error XML, empty bodies and HEAD responses. Distinguish a transient provider failure from access denied, absent objects and an uncertain write outcome. Check SDK error behavior even when an HTTP status alone appears successful, such as streaming completion/copy response handling.

## Signature correctness

Use the AWS SigV4 specification and maintained components, with official test vectors and independent SDK checks. Verify signed host/port, query duplicates and encoding, signed headers, payload hash, credential scope/date/region/service, session tokens and expiration. Reject algorithm downgrade and ambiguous signed/unsigned header combinations.

Raw S3 object keys are opaque protocol names. Preserve repeated slashes, percent encoding, spaces, plus signs, Unicode and dot segments according to S3 signing rules. Do not normalize them as filesystem paths or let an ingress rewrite the signed path/host. Decode once at the correct protocol layer; AWS notification key encoding is a different transport contract. The Falcone legacy key-layout helper may reject/normalize its own inputs; it is not a raw S3 canonicalizer.

The profile must explicitly test header signing, query signing, unsigned payload over TLS where permitted, `aws-chunked`, streaming signatures and checksum trailers required by selected SDK versions. Unsupported streaming variants must fail before mutation. Do not advertise generic current-SDK compatibility after testing only a small unsigned PUT.

## ETags, checksums and retries

ETag is an opaque entity validator under a documented provider/profile algorithm, not a universal MD5 or content-integrity proof. Expose an independent checksum with its algorithm and full-object/composite scope. Honor server-side encryption and multipart differences. Reject mismatched declared sizes/checksums and make corrupt bytes unavailable until repair.

Native façade requests may use an explicitly versioned idempotency contract with scope and request fingerprint. Raw S3 retries retain S3 semantics: repeating a versioned PUT can create another version, and a random custom idempotency header does not make Amazon S3 deduplicate. Track lost responses and reconcile external outcomes conservatively. Conditional requests must be serialized/atomic in native metadata or delegated to a provider supporting that exact operation.

Pagination tokens are opaque and bound to caller scope, binding/provider revision, prefix and query options. They cannot become reusable capabilities across tenants. A multi-page listing under concurrent writes is not a snapshot unless the profile explicitly implements one. Document ordering and modification behavior rather than promising a global snapshot.

## Qualification matrix

Test Falcone SDK/console fixtures, AWS SDK for JavaScript v3, AWS SDK for Go v2, boto3 and the chosen AWS CLI release. Pin versions; include their default checksums and addressing modes. Compare protocol traces against Amazon S3 general-purpose buckets and pinned compatible providers in isolated test buckets. Include UTF-8/binary/zero-byte/large objects, failed signatures, expiry, cancellations, duplicate requests, partial streams, ranges, condition races and tenant-scoped list operations. Gate each claimed capability with results, not a single overall “S3-compatible” badge.
