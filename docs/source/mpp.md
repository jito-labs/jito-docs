# 👨🏻‍🍳 Maker Priority (MPP)

The BAM Maker Priority Plugin (MPP) is a dedicated, priority transaction ingress path for
enrolled market makers. It provides top-of-batch scheduling for market maker transactions,
without interfering with standard transaction or bundle handling.

**Full documentation:** [bam.dev — Maker Plugin](https://bam.dev/docs/bam/maker-plugin/how-it-works/)

## How it works

Makers send pre-signed price-update transactions to a separate UDP endpoint on each BAM
Node, the **Plugin TPU (PTPU)**. Every transaction on that path is:

- **Validated** against the node's enrollment config: one enrolled signer, enrolled market
  accounts, allowed programs only, a minimum compute-unit price, and a sequence number at
  the enrolled offset.
- **Coalesced**, so only the newest update per market account per auction round reaches
  the validator.
- **Scheduled first** in every auction batch, ahead of all bundles and regular
  transactions. No tip or priority fee can move other transactions ahead of it.

MPP transactions are standard Solana transactions. They need no Jito tip, but they must pay
at least **1 lamport per compute unit**.

## Who it is for

MPP is for market makers who update on-chain market state at high frequency. Enrollment is
managed by Jito; there is no self-serve registration. To enroll, fill out the
[MPP enrollment form](https://forms.gle/b4eTh2tD97rTnA2x9). Each BAM Node publishes its live
enrollment config at `/api/v1/mpp/config`.

## Learn more

- [How it works](https://bam.dev/docs/bam/maker-plugin/how-it-works/): scheduling,
  validation rules and coalescing
- [Getting started](https://bam.dev/docs/bam/maker-plugin/getting-started/): enrollment,
  endpoints and regions
- [FAQs](https://bam.dev/docs/bam/maker-plugin/faqs/)
- [jito-foundation/bam-plugins](https://github.com/jito-foundation/bam-plugins/tree/master/maker-priority):
  onboarding resources and PTPU endpoints
