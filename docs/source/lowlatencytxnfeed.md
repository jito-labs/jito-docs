# ➤ Low Latency Transaction Feed (Shredstream)

Jito's ShredStream service delivers the lowest latency shreds from leaders on the Solana network, optimizing performance for high-frequency trading, validation, and RPC operations. ShredStream ensures minimal latency for receiving shreds, which can save hundreds of milliseconds during trading on Solana—a critical advantage in high-frequency trading environments. Additionally, it provides a redundant shred path for servers in remote locations, enhancing reliability and performance for users operating in less connected regions. This makes ShredStream particularly valuable for traders, validators, and node operators who require the fastest and most reliable data to maintain a competitive edge.

## Shreds

Shreds are fragments of data used in the Solana blockchain to represent parts of transactions before they are assembled into a full block. When a validator processes transactions, it breaks them down into smaller units called shreds. These shreds are distributed across the network to other validators and nodes, which then reassemble them to form complete blocks.

Shreds help in fast and efficient data propagation, maintaining Solana's high throughput and low latency. They also provide redundancy and fault tolerance, ensuring that even if some data is lost or delayed during transmission, the network can still reconstruct the necessary information. Shreds are crucial for enabling Solana’s rapid block times and overall network performance.

## Setup


## Troubleshooting

Ensure ShredStream is running correctly by configuring the `SOLANA_METRICS_CONFIG` in your RPC setup. Refer to [Solana Clusters Documentation](https://docs.solana.com/clusters) for details.

To verify, query the number of packets received before and after configuring ShredStream using:

```sql
SELECT shred_count FROM "shred_fetch" WHERE time > now() - 1h
