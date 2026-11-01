#!/usr/bin/env python3
"""Generate the S3 planning backlog. Does not implement storage or publish issues."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'gntik-ai/falcone-s3'
DATE = '2026-11-01'
BASELINE = 'ed04fe7269d32f3f3e3cbc434ab5168389153ed6'
EPICS = []

def epic(code, title, outcome):
    e = dict(id=f'S3-{code}', category=code.lower(), title=title, outcome=outcome, stories=[])
    EPICS.append(e)
    return e

def story(e, title, persona, want, benefit, phase, effort, deps, requirements, acceptance):
    sid = f"{e['id']}-{len(e['stories'])+1:03d}"
    e['stories'].append(dict(id=sid, title=title, description=want[0].upper()+want[1:]+'.',
        story=f'As {persona}, I want {want}, so that {benefit}.', phase=phase, effort=effort,
        dependencies=deps, requirements=[dict(id=f'FR-{sid}-{i+1}', statement=r) for i,r in enumerate(requirements)],
        acceptance=acceptance))

e=epic('CON','Falcone contracts and first-party scope','Freeze existing behavior and ownership before replacing the storage backend.')
story(e,'Freeze storage API and deployment contract fixtures','a Falcone maintainer','a pinned inventory of storage consumers and behaviors','the replacement preserves existing applications','P0','M',[],[
 'The project must inventory every current storage route, client, bucket binding, credential path and notification configuration against a pinned Falcone revision and actual deployment evidence.',
 'The compatibility suite must preserve approved Falcone response schemas, status/error precedence, ownership checks and legacy aliases.'
],[ 'Cover console, SDK, workflow activities, runtime artifacts, presign, multipart, quotas and recursive product bucket deletion.', 'Resolve per-workspace versus per-bucket identity and tenant-versus-workspace quota documentation discrepancies using source fixtures and deployed evidence.', 'Record exact SeaweedFS/SDK versions, public/internal endpoints and any direct S3 users; identify unimplemented backup and capability-builder stubs.' ])
story(e,'Define storage ownership and provider binding contracts','a platform architect','one authority for each bucket, object, policy and key','native and external modes integrate with Falcone','P0','M',['S3-CON-001'],[
 'Each logical bucket must bind to one explicit native or external provider with trusted tenant/workspace ownership and a versioned writer epoch.',
 'The service must retain IAM policy, secrets custody, workflow execution and quota definitions under their existing Falcone owners.'
],[ 'Publish binding and ownership schemas including managed/adopted modes and capabilities; changing a default affects new buckets only.', 'Use accepted falcone-secrets ADR 0002; do not create a second IdP, secret manager or quota-policy database.', 'Map provider changes to the migration protocol; no automatic fallback to an unrelated backend or shared-prefix allocation default.' ])
story(e,'Qualify components, capacity assumptions and licenses','a maintainer','reviewed implementation choices and realistic demand measurements','the design fits restricted infrastructure','P0','L',['S3-CON-001'],[
 'Component selection must record maintained dependencies, license provenance, supported versions and measured control/data-plane behavior.',
 'Native capacity planning must measure storage demand and verify actual PVC/media and metadata failure domains before claiming HA.'
],[ 'Evaluate TypeScript control and Go streaming paths with representative objects; do not infer S3 load from 100k event messages or 10000 deployed functions.', 'Identify approved storage classes, flush semantics, topology, database replication and namespace permissions; flag shared underlying storage.', 'Record MinIO archive status, other reference licenses and project-license decision before code distribution; copy no unreviewed upstream code.' ])

e=epic('PROV','Provider registry and external S3','Make native and external storage permanent selectable Falcone options.')
story(e,'Implement provider profiles and scoped storage bindings','a tenant administrator','approved native and external storage choices','each workspace uses the appropriate backend','P1','L',['S3-CON-002'],[
 'The management API must register approved providers and create authorized bucket bindings with region, endpoint, ownership, credential reference and access mode.',
 'Every binding must expose capability state, constraints and qualification evidence, and reject operations with missing required capabilities.'
],[ 'Reuse or version existing Falcone provider-profile contracts and satisfied/partial/unsatisfied states; unknown means unavailable.', 'Only authorized operators register network endpoints; tenant selection is limited by IAM and entitlements.', 'External-only installation needs no native workers or SeaweedFS; a default change leaves existing bindings and object location unchanged.' ])
story(e,'Implement Amazon S3 general-purpose bucket adapter','an application owner','Amazon S3 as a Falcone storage backend','I can use managed object storage without changing Falcone APIs','P1','L',['S3-PROV-001','S3-AUTH-003','S3-KEY-002'],[
 'The Amazon adapter must support qualified bucket/object, conditional, list, multipart and presign operations for general-purpose buckets through maintained SDKs.',
 'External object state must remain authoritative at the provider, with uncertain writes recorded and reconciled instead of assuming a local atomic commit.'
],[ 'Test region, virtual-host addressing, temporary credential refresh, SSE profile and scoped permissions in isolated buckets.', 'Cover throttling, lost responses, provider commit followed by local failure and versioned retry duplication; never emulate conditional writes with HEAD then PUT.', 'Publish exact supported SDK/API variants; Express/directory buckets, tables and archival retrieval remain separate profiles.' ])
story(e,'Implement qualified S3 adapters and safe bucket adoption','a customer storage administrator','existing S3-compatible buckets connected safely','Falcone can coexist with my storage ownership','P1','L',['S3-PROV-001','S3-AUTH-003','S3-KEY-002'],[
 'Generic S3 adapters must qualify endpoint, region, addressing, TLS, operation semantics and limits for each supported product/release.',
 'Adopted storage must preserve unrelated data and bucket configuration and must expose any restrictions on lifecycle, quotas and audit.'
],[ 'Qualify current SeaweedFS first and maintain an evidence-based two-stable-release test matrix; other providers require their own results.', 'Read-only probes by default; shared-prefix adoption cannot claim independent bucket versioning, CORS, policy, notifications or retention.', 'Reject incompatible recursive-delete ownership contracts; never delete the whole adopted bucket or rewrite unrelated rules as a side effect.' ])

e=epic('API','Falcone API and S3 protocol','Provide correct product and wire contracts without conflating their semantics.')
story(e,'Implement the compatible Falcone storage façade','a Falcone application developer','the existing storage API on the new routing layer','my code and console continue to work','P1','L',['S3-CON-001','S3-PROV-001','S3-AUTH-001'],[
 'The façade must preserve approved JSON/base64 and binary upload, read/range, metadata, presign, multipart and bucket lifecycle contracts.',
 'Every request must apply the existing authentication, ownership and error-precedence rules before exposing backend state.'
],[ 'Test primary contentBase64 versus legacy input, zero-byte objects, malformed JSON, 206 envelopes and mapped 416 errors.', 'Keep recursive product DeleteBucket distinct from nonempty raw S3 DeleteBucket rejection and honor retention/adoption restrictions.', 'Stream or bound allocations without silently breaking existing accepted payload sizes; version any new streaming API.' ])
story(e,'Implement S3 routing, XML errors and SigV4 verification','an S3 client developer','a defined S3 protocol endpoint','standard tools can access authorized Falcone storage','P1','L',['S3-AUTH-002','S3-CON-003','S3-PROV-001'],[
 'The raw S3 endpoint must implement its published operation profile, status/headers/XML errors and explicit unsupported-operation responses.',
 'SigV4 validation must bind canonical path/query/headers, payload mode, credential scope, session token and expiry without unsafe normalization.'
],[ 'Test official signing vectors and hostile encodings, duplicate query parameters, signed host/port, clock skew and path rewriting at ingress.', 'Preserve raw object keys including repeated slashes and dot segments; use internal IDs for native filesystem paths.', 'Qualify streaming signatures, aws-chunked and checksum trailers required by selected SDKs; reject unsupported modes before mutation.' ])
story(e,'Publish and enforce SDK compatibility profiles','an integration maintainer','versioned interoperability evidence','supported S3 capabilities are predictable across providers','P2','L',['S3-API-001','S3-API-002','S3-PROV-002','S3-PROV-003','S3-MPU-002','S3-OBJ-002'],[
 'Each claimed S3 capability must have provider/profile-specific tests using pinned Falcone and mainstream SDK/client versions.',
 'The release must publish operation, header, checksum, limit and error differences instead of a blanket full-S3 claim.'
],[ 'Run JS v3, Go v2, boto3 and chosen AWS CLI cases for zero/binary/large objects, addressing, default checksums, ranges and expiration.', 'Cover unsupported policy clauses, HEAD errors, stream truncation and completion/copy error bodies, not just happy-path status codes.', 'Make capability flags follow passing evidence; requalify changed SDK/provider versions and publish incompatibilities.' ])

e=epic('AUTH','Identity, credentials and tenant isolation','Enforce Falcone ownership on every management and object operation.')
story(e,'Integrate IAM authorization and policy freshness','a workspace owner','storage enforcement of Falcone identities and grants','data cannot cross tenant boundaries','P1','L',['S3-CON-002'],[
 'All storage operations must authenticate callers and authorize trusted tenant/workspace, resource, action, prefix and delegated scope through Falcone IAM.',
 'Cached authorization must have a configured freshness bound and deny protected operations when required authority cannot be established.'
],[ 'Test wrong issuer/audience, forged scope headers, expired/cancelled execution grants and cross-tenant same-name buckets.', 'Separate policy administration, metadata listing, read/write/delete, credentials and migration rights; deny wins.', 'Apply the proposed 30-second new-request bound or record a reviewed replacement; document in-flight and direct-URL limitations.' ])
story(e,'Implement scoped S3 access-key lifecycle','a developer','scoped expiring S3 credentials','tools can access only approved objects','P1','L',['S3-AUTH-001','S3-KEY-002'],[
 'The service must issue CSPRNG-generated access keys with scoped actions, resources, expiry and audited rotation/revocation.',
 'SigV4 secret material must use recoverable protected custody or a qualified signing service, separate from public key metadata.'
],[ 'Never implement SigV4 verification using only a one-way password hash or deterministic fixture-derived secrets.', 'Test dual-key rotation windows, revoked cache entries, key-ID tenant mapping and no secret retrieval from list/export/log APIs.', 'List/presign/multipart/version and copy-source operations enforce scope; tenants never receive a platform-wide backend key.' ])
story(e,'Implement external identity and least-privilege policy projection','a security engineer','narrow backend credentials and explicit policy intersections','provider access cannot widen Falcone permissions','P1','L',['S3-AUTH-001','S3-PROV-001'],[
 'External provider access must use qualified workload-role exchange where available or scoped credentials resolved from falcone-secrets.',
 'Backend permissions and Falcone policy must intersect, with unsupported conditions rejected and adopted-bucket rights limited to granted ownership.'
],[ 'Validate AWS trust subject/audience and role scope; a Falcone OIDC token alone is not an AWS credential.', 'Test prefix, object, bucket-list and configuration permissions against real provider policy; no silent dropping of deny conditions.', 'Exercise rotated/expired provider credentials and independent external writers; report governance limits instead of claiming exclusive control.' ])

e=epic('OBJ','Native object metadata and namespace','Make committed object state atomic, scoped and readable with stable semantics.')
story(e,'Implement native CRUD and immutable metadata manifests','an application developer','atomic object storage with preserved metadata','readers never observe partially written objects','P1','L',['S3-DATA-001','S3-AUTH-002'],[
 'Native PUT/GET/HEAD/DELETE must operate on committed manifests and preserve bytes, size, content type and approved user metadata.',
 'Native per-key replacement must publish one complete version atomically after the declared durable-byte acknowledgements.'
],[ 'Test zero-byte, binary and interrupted uploads; no success or object visibility before metadata commit.', 'Bind encryption and integrity metadata to immutable object/version identity; never store object payloads in PostgreSQL.', 'Lost success responses follow documented retry semantics; a failed conditional or database transaction leaves only invisible staged data.' ])
story(e,'Implement conditional operations, ranges and scoped listing','an SDK user','consistent metadata and concurrency controls','I can update and browse objects safely','P1','L',['S3-OBJ-001'],[
 'Native conditional operations must evaluate their approved predicates atomically with mutation, and range reads must return the qualified bytes/statuses.',
 'Listing must filter authorized scope before pagination and use opaque query/binding-scoped continuation tokens with documented ordering.'
],[ 'Race concurrent If-Match/create-only operations and verify one valid winner without HEAD-then-write emulation.', 'Test prefixes/delimiters, Unicode, zero-length ranges, unsatisfiable ranges and foreign/reused/tampered tokens.', 'Treat ETags as validators and checksums as separately typed integrity evidence; document non-snapshot behavior under concurrent multi-page changes.' ])
story(e,'Implement versioning, delete markers and version references','a workflow owner','immutable object versions','replay and recovery use the exact original artifact','P2','L',['S3-OBJ-002'],[
 'The versioning capability must define enable/suspend behavior, immutable version IDs, delete markers and authorized version enumeration/read/delete.',
 'Durable references must identify a version or immutable key plus binding, size and checksum rather than relying on a mutable filename.'
],[ 'Test overwrite/delete/suspended-version edge cases and permission checks for historical data.', 'Publish capability only after tests pass; migration of in-use source versions is blocked until an equivalent destination profile exists.', 'Provider version IDs remain provider-specific; supply explicit translation for migrated workflow/artifact references.' ])

e=epic('MPU','Large objects, multipart and transfer','Transfer large analysis artifacts safely with bounded memory and resumable state.')
story(e,'Implement scoped multipart sessions and part upload','a data-analysis user','resumable large uploads','network interruptions do not restart entire datasets','P1','L',['S3-OBJ-001','S3-QUOTA-001'],[
 'Multipart sessions must bind caller scope, object, provider and writer epoch, with durable part/checksum state and bounded staging capacity.',
 'Part upload must stream with bounded memory, enforce declared limits and account for replacements without leaking data across sessions.'
],[ 'Test unauthorized upload IDs, repeated part replacement, cancellation and concurrent part uploads under reservations.', 'Track expiry and lease state; no part is visible as a completed object.', 'Expose profile-specific part/size/checksum limits and keep provider upload IDs inside the authorized binding.' ])
story(e,'Implement atomic completion, abort and orphan cleanup','an upload client','deterministic multipart completion and cleanup','retries cannot publish incomplete objects or leak capacity','P1','L',['S3-MPU-001','S3-DATA-003'],[
 'Multipart completion must have one durable terminal result and publish only a verified complete manifest or provider-confirmed outcome.',
 'Abort and expiry must release reservations and reclaim safe staged parts without deleting committed or in-flight referenced data.'
],[ 'Preserve gap-free ordered parts for the Falcone façade while implementing the distinct qualified raw S3 rules.', 'Inject simultaneous complete/abort, lost completion responses, provider ambiguity and crashes; do not blindly duplicate versioned completion effects.', 'Test final size/checksum, temporary-versus-logical accounting and safe cleanup after lease expiry.' ])
story(e,'Implement copy, presign and controlled streaming access','an application developer','efficient scoped copy and signed transfers','large files avoid unnecessary application buffering','P1','L',['S3-MPU-001','S3-AUTH-003','S3-QUOTA-003'],[
 'Copy and signed URL operations must authorize source/destination, bind required request fields and limit expiry to policy and credential lifetime.',
 'Direct external transfers must be explicit binding capabilities with declared quota, audit and revocation limits.'
],[ 'Presign using the reachable public host/region; test signed headers, expiry, short-lived credentials and no URL query logging.', 'Reject unsupported cross-provider copy; native reuse requires compatible scope/encryption/retention and safe reference accounting.', 'Preserve existing TTL clamps while reporting shorter effective expiry; do not claim instant revocation or strict arbitrary-size enforcement for external presigned PUT.' ])

e=epic('DATA','Native durability, repair and garbage collection','Make storage acknowledgements and recovery trustworthy under the declared failure model.')
story(e,'Implement the staged-byte and transactional commit protocol','a storage engineer','explicit durable commit ordering','acknowledged objects survive the supported failures','P1','L',['S3-CON-003','S3-KEY-001','S3-QUOTA-001'],[
 'Native writes must verify durable byte receipts before atomically committing manifest, current pointer, quota delta, audit intent and outbox state.',
 'Every publish/cleanup operation must validate its writer epoch, lease and placement generation to reject stale workers.'
],[ 'Inject failure before/after byte flush and database commit; readers see only committed complete manifests.', 'Verify actual filesystem/PVC flush and PostgreSQL synchronous durability assumptions; never equate a network ACK with persistent data.', 'Use leased staging records and checksum-verified immutable chunks; no custom consensus protocol or cross-resource transaction claim.' ])
story(e,'Implement qualified replication, scrubbing and repair','an SRE','replicas placed across proven failure domains','media corruption and component loss can be repaired','P2','L',['S3-DATA-001','S3-OPS-001'],[
 'The native HA profile must require its configured durable-copy count across verified independent domains before acknowledging writes.',
 'The system must detect corrupt/missing replicas, serve only verified data and repair under fenced placement updates with observable progress.'
],[ 'Qualify the proposed three-copy strict profile plus synchronous metadata durability; shared-array PVCs do not count as independent domains.', 'Test domain loss, network partition, corrupt bytes, replacement worker and interrupted repair; reject writes when required acknowledgements are unavailable.', 'Rate-limit repair and scrub, alert on degraded redundancy and verify a replacement before retiring a good copy; publish no unsupported durability nines.' ])
story(e,'Implement reference-safe native garbage collection','an operator','safe reclamation of obsolete blobs and uploads','cleanup cannot destroy live or recoverable data','P1','L',['S3-DATA-001'],[
 'Garbage collection must exclude live manifests, in-flight uploads/commits, retention, workflow pins and backup references under a current fence.',
 'Deletion jobs must be idempotent, retryable and observable and must not treat age alone as proof of orphanhood.'
],[ 'Use a conservative safety horizon plus reference revalidation; test delayed commits, stale scans and lease expiry races.', 'Crash and resume GC without deleting a newly referenced chunk or resurrecting a tombstoned object.', 'Provide a dry-run/evidence mode and metrics for reclaimable, blocked and actually reclaimed bytes.' ])

e=epic('LIFE','Version lifecycle, retention and configuration','Manage storage lifecycle without bypassing application references or provider rules.')
story(e,'Implement capability-gated lifecycle, tags and CORS','a workspace administrator','predictable object lifecycle and browser configuration','storage can be managed through Falcone','P2','L',['S3-OBJ-003','S3-PROV-003'],[
 'Lifecycle, tags and CORS APIs must validate supported rules and ownership before applying native or provider configuration.',
 'Lifecycle execution must be resumable and observe current writer authority, versions and reference/retention constraints.'
],[ 'Test expiry of current/noncurrent objects and abort-incomplete-upload rules independently; unsupported transitions fail explicitly.', 'Adopted-prefix bindings cannot overwrite whole-bucket rules or unrelated CORS/notifications.', 'Keep migration-generated changes and lifecycle events auditable; expose partially applied external configuration for reconciliation.' ])
story(e,'Qualify Object Lock, retention and legal hold','a compliance administrator','enforced retention for approved storage profiles','protected objects cannot be silently deleted','P2','L',['S3-LIFE-001','S3-KEY-001'],[
 'Retention-required bindings must use a qualified capability enforcing retention and legal hold on every deletion, overwrite and cleanup path.',
 'The service must preserve provider retention restrictions and reject unsupported or unrepresentable lock policies before enabling a binding.'
],[ 'Test façade recursive deletion, raw S3, lifecycle, version deletion, GC, restore and administrative actions against retention.', 'Define time authority, governance/compliance distinctions and bypass permissions; no universal admin bypass or WORM certification claim.', 'Block migrations that cannot preserve required legal semantics; publish independent review evidence before advertising native Object Lock.' ])
story(e,'Implement workflow, artifact and backup reference pins','a workflow maintainer','lifecycle-aware storage references','running and recoverable executions retain their required objects','P2','M',['S3-OBJ-003','S3-DATA-003'],[
 'Storage cleanup must honor authorized live workflow/artifact/backup pins and their explicit expiry/release policies.',
 'Reference publication and release must reconcile interrupted cross-service operations without assuming a distributed transaction.'
],[ 'Verify object completion/checksum before publishing a durable workflow reference; quarantine unpublished orphans for a safe grace period.', 'Test run retry/cancellation, delayed pin release, backup failure and restoration of pinned object versions.', 'Prevent unauthorized tenants from pinning others data; surface retention-caused cleanup blocks and associated usage.' ])

e=epic('EVENT','Object events and Falcone triggers','Route native and external changes durably into existing Falcone execution systems.')
story(e,'Implement native transactional event outbox','an event-driven developer','durable object change events','successful mutations can reliably trigger Falcone work','P1','M',['S3-DATA-001','S3-CON-002'],[
 'Native mutation and versioned event intent must commit atomically, with at-least-once delivery and stable event identity.',
 'Events must carry trusted scope, binding, key/version and safe correlation metadata without payloads or credentials.'
],[ 'Preserve current object.created, object.deleted and multipart.completed mappings or publish a compatibility adapter.', 'Inject broker outage, relay crash and duplicate delivery; replay preserves original identity.', 'Report backlog and backpressure; do not claim global ordering or exactly-once external effects.' ])
story(e,'Implement external notifications and reconciliation bridge','an external-storage user','provider events entering Falcone safely','external writes can drive the same automations','P2','L',['S3-PROV-002','S3-PROV-003','S3-EVENT-001'],[
 'External notifications must authenticate their source and persist a scoped inbox record before acknowledging provider delivery.',
 'The bridge must tolerate duplicate/out-of-order events and expose reconciliation coverage and freshness for missed or uncertain changes.'
],[ 'Qualify AWS SQS/EventBridge ingestion and each compatible-provider bridge, preserving unrelated adopted-bucket rules.', 'Decode provider keys correctly and compare usable per-key sequence/version information; never invent a global order.', 'Test delayed events after overwrite/delete, missing metadata, reconnect and duplicate multipart observations; avoid duplicate workflow effects.' ])
story(e,'Integrate event subscriptions, filtering and trigger safety','a Falcone automation author','scoped storage subscriptions','functions and workflows react without new execution infrastructure','P2','M',['S3-EVENT-002','S3-INT-001','S3-INT-002'],[
 'Storage subscriptions must use Falcone routing, authorization and quota contracts with supported prefix/suffix filters and versioned destinations.',
 'Trigger delivery must support retries, dead letters and replay while preserving identity and preventing unbounded self-trigger loops.'
],[ 'Inventory legacy kafka_topic/openwhisk_action configuration and map it through reviewed current workflow/serverless contracts.', 'Test two tenants with matching keys and filters; rejected subscriptions never leak event existence.', 'Exercise DLQ replay, event causation and recursion limits when a function writes to its own source bucket.' ])

e=epic('QUOTA','Falcone quotas, usage and fairness','Keep storage governance in Falcone with honest enforcement across access modes.')
story(e,'Implement Falcone quota admission and reservations','a platform administrator','storage admission using Falcone plan limits','concurrent users share governed capacity','P1','L',['S3-CON-002','S3-AUTH-001'],[
 'Admission must consume Falcone quota definitions and preserve the approved compatibility fail-open behavior for governance lookup failures.',
 'Strict native admission must atomically reserve capacity for concurrent writes/bucket creation and always enforce physical safety limits.'
],[ 'Resolve current tenant-byte versus legacy bucket-limit behavior in fixtures; security denials never fail open.', 'Test concurrent admissions, overwrite deltas, expired reservations and database rollback without double counting.', 'Make strict mode an explicit versioned policy; disk-full or unsafe temporary capacity always rejects writes regardless of business quota mode.' ])
story(e,'Implement usage accounting and provider reconciliation','a tenant owner','accurate scoped storage usage','I can understand limits and retention costs','P1','L',['S3-QUOTA-001','S3-PROV-001'],[
 'Usage must distinguish current logical bytes, retained versions, multipart/staging, physical replication and transfer/request dimensions.',
 'External usage reports must include observation freshness, pending/uncertain operations and reconciliation results for out-of-band changes.'
],[ 'Define Falcone treatment of failed attempts, retries, abandoned parts, migration copies and retained objects; do not create independent billing policy.', 'Test overwrite/delete/version transitions and repeated event delivery without double-counting committed logical objects.', 'Reconcile against provider truth and report drift; never compensate an overflow by blindly deleting an existing overwritten object.' ])
story(e,'Enforce direct-access policy and tenant fairness','an operator','explicit access-mode guarantees and bounded queues','one tenant cannot exhaust shared storage resources','P1','M',['S3-QUOTA-001','S3-PROV-001'],[
 'A binding requiring strict per-request Falcone governance must reject access paths or independent writers that bypass its enforcement guarantees.',
 'Gateway and background workers must apply configurable tenant fairness, concurrency, bandwidth and queue limits from Falcone policy.'
],[ 'Direct presigned upload/read is opt-in with quota/revocation/audit limitations shown; delayed provider events are not hard admission.', 'Exercise slow clients, large uploads, request floods and lifecycle/repair contention without unbounded memory or queue growth.', 'Use safe backpressure and scoped metrics; limits and exemptions remain managed in Falcone.' ])

e=epic('KEY','Encryption, secret custody and network security','Protect stored bytes and provider credentials using accepted Falcone security boundaries.')
story(e,'Implement native envelope encryption and key lifecycle','a security engineer','authenticated encryption rooted in falcone-secrets','media access cannot reveal or relocate tenant objects','P1','L',['S3-CON-003','S3-AUTH-001'],[
 'Native encryption must use reviewed AEAD framing and unique nonce/key handling with authenticated tenant/object/version/chunk context.',
 'Key rotation and retirement must preserve decryptability of all authorized live versions and recoverable backups until their required key dependencies expire.'
],[ 'Use accepted secrets custody APIs and maintained crypto libraries; no custom root trust or plaintext key fields in metadata/WAL.', 'Test tampered ciphertext/context, wrong key, cross-tenant substitution, partial range decrypt and lost key-provider access.', 'Qualify rewrap/re-encryption behavior and recovery of old keys; native encryption and provider SSE profiles remain distinct.' ])
story(e,'Integrate recoverable provider credentials and independent bootstrap','a secrets custodian','storage credentials with managed rotation and recovery','storage does not create an unlock dependency cycle','P1','M',['S3-CON-002','S3-AUTH-001'],[
 'Bindings and access-key metadata must store secret references rather than provider secret values, with bounded protected resolution caches.',
 'Storage bootstrap and recovery must have independent access to required root custody, database/TLS identity and recovery material.'
],[ 'Use falcone-secrets accepted ADR 0002 without reopening its proposals; preserve its existing qualification gates.', 'Test provider key rotation and expiry while operations are active; redact secrets and signed URL queries from diagnostics.', 'Prove the only unlock key or recovery copy is not in the S3 service it unlocks; test a cold restore with independent custodians.' ])
story(e,'Harden endpoint access, parsing and audit boundaries','a security reviewer','defense against hostile requests and endpoints','storage cannot become an SSRF or tenant-exfiltration service','P1','L',['S3-KEY-002','S3-API-002'],[
 'Provider connections must enforce registered endpoint/TLS/egress policy including redirect and DNS-rebinding checks and approved private-network exceptions.',
 'Parsers, logs and audit paths must enforce resource limits and redact payloads, credentials and sensitive signed URL data.'
],[ 'Test metadata-service targets, unapproved redirects, DNS changes, malicious XML/entities, request smuggling and oversized metadata.', 'Verify narrow service accounts, NetworkPolicies, arbitrary UID and no execution of tenant code/plugins inside storage workers.', 'Native mutation audit intent is durable; external uncertainty and direct-access audit coverage are explicitly reported.' ])

e=epic('INT','Falcone consumer integration','Make all Falcone systems use the same scoped storage contracts.')
story(e,'Integrate serverless artifacts, results and checkpoints','a runtime maintainer','scoped immutable storage artifacts','functions execute and resume using verified data','P2','L',['S3-API-001','S3-OBJ-003','S3-MPU-003','S3-LIFE-003'],[
 'Runtime artifact/output/checkpoint access must use tenant/workspace/attempt-scoped grants and verified immutable references.',
 'Runtime integration must work with qualified native and external providers without exposing broad backend credentials to tenant code.'
],[ 'Test existing and custom runtime paths, cancellation, wrong-attempt grants, altered digests and expired access.', 'Respect the serverless host/shim boundary and checkpoint contracts; storage does not replace hostile-code isolation.', 'Validate artifact retrieval after provider migration/version translation and restore, with signed handoff fixtures in the sibling repository.' ])
story(e,'Integrate workflow storage activities and large payloads','a workflow author','provider-neutral durable payload references','long-running workflows can replay and recover safely','P2','L',['S3-API-001','S3-OBJ-003','S3-LIFE-003'],[
 'Existing storage activities and custom falcone-workflow consumers must preserve their response/error contracts across selected providers.',
 'Large workflow payloads must be uploaded and verified before committing durable references with lifecycle pins and recoverable version mapping.'
],[ 'Test base64 small-payload compatibility and large streamed references without assuming a cross-service transaction.', 'Exercise retry/cancellation, missing object/key version, orphan cleanup and complete workflow-plus-storage restore.', 'Do not introduce a storage-owned workflow scheduler or independent retry policy conflicting with Falcone execution contracts.' ])
story(e,'Integrate console, analytics and platform backup status','a Falcone operator','consistent storage management and truthful recovery status','all users see the selected provider and its limits','P2','M',['S3-API-001','S3-PROV-003','S3-QUOTA-002','S3-OPS-003'],[
 'Console/SDK/data-service flows must expose allowed provider selection, capability limits and usage freshness while preserving existing storage operations.',
 'The backup-status adapter must report real provider-specific support and verified backup/restore results instead of replacing the existing stub with assumed success.'
],[ 'Test browser CORS, signed upload, metadata, multipart and recursive-delete confirmation with native and external profiles.', 'Keep provider credentials and implementation-only details out of tenant UI; show actionable unsupported-operation reasons.', 'Record integration handoffs for main Falcone and siblings; this planning repository alone does not deploy changes to them.' ])

e=epic('OPS','Deployment, observability and recovery','Operate storage safely in restricted Kubernetes and OpenShift.')
story(e,'Package restricted and external-only deployments','a platform operator','ordinary namespaced installation profiles','Falcone storage fits corporate permissions','P1','L',['S3-CON-003','S3-PROV-001'],[
 'Baseline installation must use ordinary workloads/PVCs and namespace-scoped permissions without new operators, CRDs, privileged containers or custom SCC prerequisites.',
 'External-only mode must omit native byte workers and storage volumes while retaining the same Falcone management/security interfaces.'
],[ 'Test arbitrary UID, read-only root where practical, dropped capabilities, TLS and approved volume permissions without chown-as-root init containers.', 'Record approved CSI, ingress, PostgreSQL and eventing prerequisites separately from namespace permissions.', 'Publish exact qualified Kubernetes/OpenShift versions and rolling schema/image upgrade/rollback procedures; dev durability cannot be mislabeled HA.' ])
story(e,'Implement storage SLOs, telemetry and incident runbooks','an SRE','measured reliability and actionable signals','I can diagnose failures before data safety is threatened','P2','M',['S3-OPS-001','S3-QUOTA-002','S3-EVENT-001'],[
 'Telemetry must report provider/operation availability, latency, capacity, integrity, repair debt, credential health and event/reconciliation lag without unbounded sensitive labels.',
 'The release must publish measured SLOs, capacity assumptions, dependency failure behavior and assigned on-call/patch responsibilities.'
],[ 'Benchmark proposed 99.95% availability and latency targets using stated load/object sizes; publish end-to-end and gateway overhead separately.', 'Exercise provider throttling, disk full, broker/key/IAM outage and noisy neighbors with bounded backpressure.', 'Provide runbooks and alerts for uncertain writes, degraded replicas, corruption, stale usage and stuck migrations; objectives are not untested SLA claims.' ])
story(e,'Implement coordinated backup and disaster recovery','a recovery operator','restorable metadata, bytes and keys','a storage disaster does not strand Falcone workflows','P2','L',['S3-OPS-001','S3-KEY-001','S3-LIFE-003','S3-DATA-002'],[
 'Native backup must capture a recoverable metadata point and all referenced blobs/key versions while protecting them from premature GC.',
 'Every supported production provider profile must have a tested restore procedure with measured RPO/RTO and required workflow/artifact verification.'
],[ 'Test cold restoration after metadata/media loss, including independent secrets bootstrap and historical encrypted versions.', 'Distinguish replica safety from backup and disaster RPO; account for full dataset transfer bandwidth rather than promising universal one-hour recovery.', 'External adapters report real backup/retention capabilities and restore evidence; versioning alone is not sufficient proof of disaster recovery.' ])

e=epic('MIG','Migration, cutover and SeaweedFS retirement','Move selected bindings without data loss or competing writers.')
story(e,'Implement inventory and resumable verified transfers','a migration operator','complete source inventory and validated copies','I can identify incompatibilities before cutover','P2','L',['S3-CON-001','S3-PROV-001'],[
 'Migration inventory must include bytes, versions/delete markers, metadata/tags, retention, credentials, consumers, active uploads and notification rules.',
 'Transfers must be resumable, scoped and checksum-verified with provider version/reference translation and visible unsupported features.'
],[ 'Test source/destination differences including ETag algorithms, key encoding, metadata and retained objects; no plaintext credentials in reports.', 'Support SeaweedFS-to-native, SeaweedFS-to-external and later provider-to-provider transfers through the same capability checks.', 'Reject missing required retention/version capabilities; never pretend multipart upload IDs or raw signed URLs are portable.' ])
story(e,'Implement fenced canary cutover and reconciled rollback','a rollout owner','one writer and an auditable handoff','migration cannot lose post-cutover writes','P3','L',['S3-MIG-001','S3-DEV-003','S3-INT-001','S3-INT-002','S3-INT-003'],[
 'Cutover must quiesce/fence writers, verify final differences and atomically update the authoritative binding epoch and routing.',
 'Rollback must reconcile post-cutover writes, versions, deletions, retention and reference mappings before returning authority to the old provider.'
],[ 'Drain/expire presigned writes and multipart sessions; independently controlled external writers require provider-side fencing or verified quiescence.', 'Canary every enabled consumer, credentials, events, quotas and restore path; apply only gates relevant to the selected profile.', 'No blind dual-write, automatic failover to stale data or simple old-snapshot rollback; expose blocked and uncertain operations.' ])
story(e,'Retire migrated SeaweedFS dependencies with evidence','a product owner','controlled source-service retirement','the custom service becomes supported without orphaned consumers','P3','M',['S3-MIG-002','S3-OPS-003'],[
 'SeaweedFS retirement must require all affected bindings/consumers and rollback dependencies to pass their migration and recovery gates.',
 'Retirement must remove obsolete credentials, routes and infrastructure only after approved retention and recovery obligations are met.'
],[ 'Retain external S3 as a supported permanent option and leave unmigrated bindings operational.', 'Obtain separately reviewed deployment changes in Falcone/siblings; this plan is not authorization to delete production infrastructure now.', 'Archive sanitized inventory and validation evidence with owners, residual exceptions and key/source-retention dates.' ])

e=epic('DEV','Developer tooling and independent qualification','Make the service implementable, interoperable and reviewable before production trust changes.')
story(e,'Publish versioned schemas, SDK examples and local fixtures','an integration developer','clear APIs and synthetic environments','I can implement consumers without production credentials','P1','M',['S3-CON-001','S3-PROV-001'],[
 'The repository must publish versioned management/event/binding schemas and SDK examples distinguishing Falcone REST and raw S3.',
 'Local fixtures must include multiple tenants, native development storage and mock/isolated external profiles with no real credentials.'
],[ 'Document capability detection, retry uncertainty, presign expiry and large-object references in TypeScript/Go examples.', 'Production startup rejects development trust/durability bypasses; synthetic fixtures do not constitute provider qualification.', 'Keep generated backlog IDs, parent/dependency references and issue mapping reproducible and validated.' ])
story(e,'Implement secure builds and maintenance policy','a maintainer','attributable releases and owned dependencies','the service can be patched safely over time','P1','M',['S3-CON-003'],[
 'Releases must pin dependencies/images, publish SBOM and signed provenance and review licenses and security updates.',
 'The project must define supported versions, vulnerability reporting, patch ownership and compatibility/schema-upgrade gates.'
],[ 'Scan for secrets, unsafe image permissions and vulnerable dependencies with owned time-limited exceptions.', 'Select a repository license explicitly and retain notices for reused components; archived upstream code needs explicit maintenance ownership.', 'Verify rollback/schema compatibility and publish provider/SDK matrix changes with each release.' ])
story(e,'Qualify protocol, isolation and durability independently','an independent reviewer','adversarial and fault-injection evidence','production data moves only after the chosen profile proves its guarantees','P2','L',['S3-API-003','S3-KEY-003','S3-DATA-002','S3-OPS-003','S3-EVENT-002','S3-DEV-002'],[
 'Production candidates must pass profile-specific protocol, cross-tenant, credential, retention, failure and recovery qualification with reviewable evidence.',
 'Native qualification must verify acknowledged-write recovery and per-key consistency under crashes, partitions, corruption and stale-worker races.'
],[ 'Use operation histories and recovery checksums, not only implementation-shaped unit tests; exercise lost responses and concurrent conditions.', 'Review IAM bypass, forged signatures, SSRF, data leaks and retained-version deletion paths independently.', 'Separate external-only release evidence from native HA evidence; record residual risks and no inherited upstream certification.' ])

def generate():
    mapping_path = ROOT/'docs/github-issues.json'
    mapping = json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
    by_id = {s['id']:s for e in EPICS for s in e['stories']}
    assert len(by_id) == sum(len(e['stories']) for e in EPICS)
    assert len({e['id'] for e in EPICS}) == len(EPICS)
    seen=set()
    def visit(sid, stack):
        assert sid not in stack, f'Dependency cycle: {stack} -> {sid}'
        if sid in seen: return
        for d in by_id[sid]['dependencies']:
            assert d in by_id, f'Unknown dependency {d}'
            visit(d, stack+[sid])
        seen.add(sid)
    for sid in by_id: visit(sid, [])
    def link(sid):
        n=mapping.get(sid,{}).get('number')
        return f'[{sid}](https://github.com/{REPO}/issues/{n})' if n else sid
    req=['# Functional requirements\n',f'Baseline: {DATE}. Target requirements, not implemented features. Each statement maps to one story. Read with [architecture](architecture.md), [protocol](protocol-profile.md), [providers](providers-and-capabilities.md) and [security](security.md).\n']
    backlog=['# Epics and user stories\n','Generated by `python3 tools/build_docs.py`. S/M/L means small/medium/large relative complexity, not a calendar estimate. P0 = discovery/qualification; P1 = core; P2 = integrations/hardening; P3 = migration. Phase is earliest start, subject to dependencies.\n','Dependencies describe the complete target program. An external-only release uses its applicable profile gates; it does not require advertising or shipping unqualified native capabilities. Epic task lists and parent links express hierarchy; no native sub-issues or GitHub Project board is implied.\n']
    issues=[];rows=[];req_ids=set()
    for e in EPICS:
        req += [f"## {e['title']}\n",'| ID | Requirement | Story |','|---|---|---|']
        backlog += [f"- **{link(e['id'])}: {e['title']}** — {e['outcome']}\n"]
        body=f"<!-- falcone-s3:{e['id']} -->\n\n## Outcome\n\n{e['outcome']}\n\n## Scope\n\nCustom Falcone storage with native and external S3 options, preserving Falcone contracts and ownership. See [architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) and [requirements](https://github.com/{REPO}/blob/main/docs/requirements.md).\n\n## Stories\n\n"
        body+=''.join(f"- [ ] {link(s['id'])}: {s['title']}\n" for s in e['stories'])
        body+='\n## Exit criteria\n\nAll child acceptance criteria have linked evidence and applicable provider, security and recovery review. Planning publication is not implementation completion.\n'
        issues.append(dict(id=e['id'],title=f"[Epic][{e['id']}] {e['title']}",body=body,labels=['type:epic',f"area:{e['category']}"]))
        rows.append(dict(ID=e['id'],Type='Epic',Title=e['title'],Parent='',Phase='',Effort='',Dependencies='',URL=mapping.get(e['id'],{}).get('url','')))
        for s in e['stories']:
            assert len(s['requirements'])==2 and len(s['acceptance'])>=3
            body=f"<!-- falcone-s3:{s['id']} -->\n\nParent: {link(e['id'])}\n\n## User story\n\n{s['story']}\n\n## Description\n\n{s['description']}\n\nPhase: {s['phase']} · Effort: {s['effort']}\n\n## Requirements\n\n"
            for r in s['requirements']:
                assert r['id'] not in req_ids
                req_ids.add(r['id'])
                req.append(f"| {r['id']} | {r['statement']} | {link(s['id'])} |")
                body+=f"- **{r['id']}**: {r['statement']}\n"
            body+='\n## Acceptance criteria\n\n'+''.join(f'- [ ] {a}\n' for a in s['acceptance'])
            body+='\n## Dependencies\n\n'+(', '.join(link(d) for d in s['dependencies']) or 'None; discovery can begin independently.')+'\n'
            body+=f'\n## Design references\n\n[Architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) · [Providers](https://github.com/{REPO}/blob/main/docs/providers-and-capabilities.md) · [Integration matrix](https://github.com/{REPO}/blob/main/docs/integration-matrix.md) · [Security](https://github.com/{REPO}/blob/main/docs/security.md).\n'
            issues.append(dict(id=s['id'],title=f"[{s['id']}] {s['title']}",body=body,labels=['type:story',f"area:{e['category']}",f"phase:{s['phase'].lower()}",f"effort:{s['effort'].lower()}"]))
            backlog += [f"  - **{link(s['id'])}: {s['title']}** ({s['phase']}, {s['effort']})",f"    - {s['story']}",f"    - Description: {s['description']}",f"    - Requirements: {', '.join(r['id'] for r in s['requirements'])}",f"    - Dependencies: {', '.join(link(d) for d in s['dependencies']) or 'None'}"]
            backlog += [f"    - Acceptance: {a}" for a in s['acceptance']]+['']
            rows.append(dict(ID=s['id'],Type='Story',Title=s['title'],Parent=e['id'],Phase=s['phase'],Effort=s['effort'],Dependencies=';'.join(s['dependencies']),URL=mapping.get(s['id'],{}).get('url','')))
        req.append('')
    assert len(req_ids)==90 and len(by_id)==45 and len(issues)==60
    assert set(mapping)<=set(x['id'] for x in issues)
    (ROOT/'docs/requirements.md').write_text('\n'.join(req)+'\n')
    (ROOT/'docs/backlog.md').write_text('\n'.join(backlog)+'\n')
    (ROOT/'docs/backlog.json').write_text(json.dumps(dict(schema_version=1,date=DATE,baseline=BASELINE,epics=EPICS),indent=2)+'\n')
    (ROOT/'docs/issue-payloads.json').write_text(json.dumps(issues,indent=2)+'\n')
    out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'docs/backlog.csv').write_text(out.getvalue())
    print(json.dumps(dict(epics=len(EPICS),stories=len(by_id),requirements=len(req_ids),issues=len(issues),mapped=len(mapping))))

if __name__=='__main__': generate()
