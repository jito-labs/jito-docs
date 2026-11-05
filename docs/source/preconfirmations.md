# ⚡ Preconfirmations

BAM Preconfirmations are a stream of the transactions a BAM-connected leader has
**committed to executing**, published before those transactions are shredded and
propagated across the network. Subscribers see what the slot is building on further
upstream than any shred-based feed. Early testing with distribution partners measured a
**p50 advantage of 5–10 ms** over their existing shred streams.

**Full documentation:** [bam.dev — Preconfirmations](https://bam.dev/docs/bam/preconfirmations/)

## What a preconfirmation is, and is not

- **A commitment, not a prediction.** A transaction appears only after the leader has
  committed to executing the batch that contains it.
- **Not finality.** The leader can still skip its slot, or the block can land on a fork.
- **BAM leaders only.** Non-BAM leaders, and BAM validators that have opted out, produce
  no preconfirmations.

## How to get access

The stream is distributed through Jito's partners, who handle pricing, onboarding and
support. You do not need an account with Jito.

- **Helius:** [pre-confirmations documentation](https://www.helius.dev/docs/pre-confirmations/overview)
- **Triton:** [customer onboarding](https://customers.triton.one/onboarding/)

## Learn more

- [Preconfirmations for searchers](https://bam.dev/docs/bam/preconfirmations/searchers/):
  what each update contains, and the wire format
- [Preconfirmations for validators](https://bam.dev/docs/bam/preconfirmations/validators/):
  how BAM validators earn from the stream
- [`preconf/preconf.proto`](https://github.com/jito-foundation/bam-plugins/blob/master/preconf/preconf.proto):
  the gRPC service definition
