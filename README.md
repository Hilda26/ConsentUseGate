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
- Once a request's refund deadline has passed, `review_request` is blocked and
  the request is refund-only; approval can no longer pay the steward.
- Settlement revalidates policy/request state after the judged round.
- Settlement also rechecks the refund deadline after the judged round before
  recording approval or routing any fee.
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
- Direct tests: 14 passed.
- Regression test added: `test_review_after_refund_deadline_is_refund_only`.

## Deployment

- StudioNet contract address: `0x3656415cD2E128CFDE2601fA34D0b3f27CAD3BcC`
- Deployment transaction: `0xa488561a380c07d1eb30aa99a7227d4b8decdb7093cf0e6b1d1191c4b2048e05`
- Deployment receipt: `FINALIZED`, `MAJORITY_AGREE`, leader execution `SUCCESS`,
  `stderr=""`, `raw_error=null`.
- `genlayer schema 0x3656415cD2E128CFDE2601fA34D0b3f27CAD3BcC` succeeded.
- `genlayer code 0x3656415cD2E128CFDE2601fA34D0b3f27CAD3BcC` returned deployed
  source containing `_refund_deadline_passed` and
  `refund deadline has passed; refund only`.
- `genlayer call 0x3656415cD2E128CFDE2601fA34D0b3f27CAD3BcC policy_count`
  returned `0`.
- `genlayer call 0x3656415cD2E128CFDE2601fA34D0b3f27CAD3BcC request_count_total`
  returned `0`.
- `pytest tests\integration\ -v --network=studionet` passed against the deployed
  address with `CONSENTUSEGATE_ADDRESS` set.
