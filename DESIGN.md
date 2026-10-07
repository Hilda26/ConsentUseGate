# ConsentUseGate Design Notes

## Flow

1. A steward creates a consent policy with fixed resource description, consent
   terms, review fee, request window, and refund grace period.
2. An applicant submits an intended use and escrows exactly the review fee.
3. Anyone may call `review_request` on a pending or errored request.
4. A single GenLayer consensus round judges semantic compatibility with the
   consent terms.
5. If approved, the applicant is recorded in `approvals` and the fee is paid to
   the steward.
6. If rejected, the applicant is refunded.
7. If the request remains pending or errored after its refund deadline, anyone
   may trigger a refund to the applicant. After that deadline, `review_request`
   is no longer allowed to settle approval or rejection.

## Bounded verdict

The judged output is intentionally small:

```json
{"approved": true, "reason_code": "CONSENT_COMPATIBLE"}
```

or:

```json
{"approved": false, "reason_code": "<finite rejection code>"}
```

Allowed reason codes:

- `CONSENT_COMPATIBLE`
- `PURPOSE_NOT_ALLOWED`
- `RETENTION_TOO_LONG`
- `SHARING_NOT_ALLOWED`
- `SENSITIVE_GROUP_RISK`
- `INSUFFICIENT_DETAIL`
- `MALFORMED_REQUEST`

The equivalence principle binds both fields. There is no unbound free-form
reason text that could differ between validators while still affecting stored
state.

## Consequence boundary

Consensus never supplies an address, amount, policy id, request id, or access
record directly. The accepted boolean only controls which deterministic branch
runs for the already-selected request. The payout and approval record read:

- `request.applicant`
- `request.fee`
- `policy.steward`
- `request.policy_id`

all of which are committed before the judged round starts.

## Deadline boundary

Each access request has a fixed `refund_deadline` computed when the applicant
escrows the review fee. `review_request` checks that deadline before starting
consensus, and checks it again after consensus before any approval state or
steward payment can be written. Once the deadline has passed, the only allowed
state-changing path for a pending or errored request is
`refund_expired_request`.

## Untrusted input handling

The resource description, consent terms, and intended use are user-authored and
may contain prompt-injection text. They are placed into a JSON evidence object
with `json.dumps(..., sort_keys=True)`, and the prompt/equivalence principle both
instruct validators to treat field values as data only.

## Review corrections carried forward

- Finite equivalence-bound payload.
- No model-controlled transfers.
- JSON evidence framing for untrusted text.
- Retryable errored verdicts.
- Permissionless timeout refund.
- Refund-only path after the request refund deadline.
- Post-consensus state and deadline revalidation.
- Consensus timestamp parsing and lower bound.
