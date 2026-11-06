# 💼 Bundles

A bundle is a group of up to five transactions that execute sequentially and atomically:
all of them land, in order, or none do. Bundles give you MEV protection, fast landing and
revert protection.

There are two ways to send a bundle:

| | Direct Bundle Ingest (DBI) | Block Engine |
|---|---|---|
| Path | Straight to a BAM Node | Through the Block Engine |
| Leaders served | BAM leaders only | BAM and non-BAM leaders |
| Access | Allowlisted; separate DBI credentials | Authorized Block Engine key, or none |
| To BAM leaders | Direct | Authorized key: forwarded, no BE auction |
| Without a key | Not available | 1 request/s per IP; BE auction first |
| Docs | This page and [bam.dev](https://bam.dev/docs/bam/dbi/) | [Block Engine bundles](#be-sendbundle-api) |

## Direct Bundle Ingest (DBI)

DBI lets an approved searcher or application send bundles straight to a BAM Node over
JSON-RPC or QUIC, removing the Block Engine hop for the shortest path to BAM leader slots.

**Full documentation:** [bam.dev — DBI](https://bam.dev/docs/bam/dbi/)

:::{figure} ../images/dbi-flow.svg
:class: diagram
:alt: Bundle flow. With DBI, a searcher sends a bundle over JSON-RPC or QUIC straight to a BAM Node. With an authorized Block Engine key, the Block Engine forwards the bundle to the upcoming BAM leader's BAM Node, skipping the Block Engine auction. Without a Block Engine key, sends are limited to 1 request per second and the bundle goes through the Block Engine auction first; winners go to the BAM Node if the leader is BAM, or to the leader itself if not. The BAM Node verifies signatures, simulates, and runs its auction before sending the winning bundle to the BAM leader as one atomic batch.

How a bundle reaches the leader: directly with DBI, forwarded by the Block Engine with an authorized key, or through the Block Engine auction without one.
:::

### What happens to a DBI bundle

1. You submit one to five fully signed transactions, in bundle order.
2. The BAM Node verifies the signature on every transaction.
3. The bundle is simulated. Only bundles in which every transaction succeeds move forward.
4. Survivors enter BAM's auction, ranked by total fees (priority fees and Jito tips) per
   compute unit.
5. Winners go to the current BAM leader as one atomic batch. If any transaction fails at
   execution, the whole bundle reverts.

### Key points

- **Access is allowlisted.** Apply with the
  [DBI access form](https://form.typeform.com/to/tQDIpkYh). A Block Engine UUID does not
  grant DBI access.
- **Two transports, two credentials.** JSON-RPC uses a Jito-issued UUID; QUIC uses an
  allowlisted Ed25519 keypair. Neither works for the other.
- **No minimum tip, but tips win.** BAM ranks bundles by reward per compute unit, so a
  bundle that pays nothing will not land when there is competition.
- **Keep the Block Engine as your fallback.** DBI serves BAM leader slots only and pauses
  during BAM Node maintenance.
- **Check landing yourself.** DBI bundles don't appear in the bundle explorer. Confirm
  with `getSignatureStatuses` on your own RPC.

### Learn more

- [DBI on bam.dev](https://bam.dev/docs/bam/dbi/): endpoints, rate limits, transaction
  versions and troubleshooting
- [jito-labs/bam-dbi](https://github.com/jito-labs/bam-dbi): Rust reference clients for
  JSON-RPC and QUIC

## Block Engine bundles

To send bundles through the Block Engine with `sendBundle`, which also reaches non-BAM
leaders, see [Low Latency Transaction Send → Bundles](#be-sendbundle-api).
