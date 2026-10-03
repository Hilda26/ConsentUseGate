# ConsentUseGate

ConsentUseGate is a GenLayer Intelligent Contract for consent-governed access to
data or controlled resources. A steward publishes fixed consent terms and a
review/access fee. Applicants escrow that exact fee with a natural-language
intended use. GenLayer validators decide whether the intended use is compatible
with the consent terms. Compatible requests are approved and pay the steward;
incompatible requests are rejected and refunded.

## Why this needs GenLayer

Consent compatibility is semantic. A deterministic contract can check that a
request paid the right fee, but it cannot reliably decide whether an applicant's
described purpose, retention window, onward-sharing plan, and sensitive-group
risk fit the actual consent language. ConsentUseGate uses GenLayer for that
judgment while keeping every consequence deterministic.

## What makes it distinct

This is not a sealed-bid procurement auction, redaction bounty, milestone
escrow, prediction market, oracle, source consensus checker, or dispute arbiter.
It is an access-control and consent-governance primitive: the output is an
on-chain approval status for a specific applicant under a specific policy, plus
deterministic fee routing.

## Safety properties

- The model cannot choose the payout recipient or amount. Approval pays the
  policy's stored steward the request's stored fee; rejection refunds the stored
  applicant.
- Verdicts are finite and equivalence-bound: validators compare both `approved`
  and `reason_code`.
- Untrusted consent terms and intended-use text are JSON-encoded as evidence and
  explicitly treated as data, not instructions.
- Malformed or inconsistent verdicts mark the request `ERRORED` without paying
  anyone; the request can be retried.
- Pending or errored requests have a permissionless refund path after their
  fixed refund deadline.
- Settlement revalidates policy/request state after the judged round.
- The consensus timestamp is parsed and checked so it cannot precede policy
  creation.

## Main methods

- `create_policy(resource_description, consent_terms, review_fee, request_window_seconds, refund_grace_seconds)`
- `request_access(policy_id, intended_use)`
- `review_request(request_id)`
- `refund_expired_request(request_id)`
- `close_policy(policy_id)`
- `is_approved(policy_id, applicant)`

## Verification

```powershell
genvm-lint check contracts\consent_use_gate.py --json
pytest tests\direct\ -v
```

Current local result:

- GenVM lint: passed.
- Direct tests: 13 passed.

## Deployment

- StudioNet contract address: `0x7eaB5ABB2A9675D7f219Ca0355363C298E3c8120`
- Deployment transaction: `0x538912de94635509db04ecca6717e348a678afcd3b7f566dc572817a8f5f5a5b`
- Deployment receipt: `FINALIZED`, `MAJORITY_AGREE`, leader execution `SUCCESS`,
  `stderr=""`, `raw_error=null`.
- `genlayer schema 0x7eaB5ABB2A9675D7f219Ca0355363C298E3c8120` succeeded.
- `genlayer code 0x7eaB5ABB2A9675D7f219Ca0355363C298E3c8120` returned the
  deployed source.
- `genlayer call 0x7eaB5ABB2A9675D7f219Ca0355363C298E3c8120 policy_count`
  returned `0`.
- `genlayer call 0x7eaB5ABB2A9675D7f219Ca0355363C298E3c8120 request_count_total`
  returned `0`.
- `pytest tests\integration\ -v --network=studionet` passed against the deployed
  address with `CONSENTUSEGATE_ADDRESS` set.
