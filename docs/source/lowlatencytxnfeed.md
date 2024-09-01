# ➤ Low Latency Block Updates (Shredstream)

Jito's ShredStream service delivers the lowest latency shreds from leaders on the Solana network, optimizing performance for high-frequency trading, validation, and RPC operations. ShredStream ensures minimal latency for receiving shreds, which can save hundreds of milliseconds during trading on Solana—a critical advantage in high-frequency trading environments. Additionally, it provides a redundant shred path for servers in remote locations, enhancing reliability and performance for users operating in less connected regions. This makes ShredStream particularly valuable for traders, validators, and node operators who require the fastest and most reliable data to maintain a competitive edge.

## Shreds

Shreds are fragments of data used in the Solana blockchain to represent parts of transactions before they are assembled into a full block. When a validator processes transactions, it breaks them down into smaller units called shreds. These shreds are distributed across the network to other validators and nodes, which then reassemble them to form complete blocks.

Shreds help in fast and efficient data propagation, maintaining Solana's high throughput and low latency. They also provide redundancy and fault tolerance, ensuring that even if some data is lost or delayed during transmission, the network can still reconstruct the necessary information. Shreds are crucial for enabling Solana’s rapid block times and overall network performance.

## Setup

## Jito ShredStream Proxy

The proxy client connects to the Jito Block Engine and authenticates using the provided keypair. It sends a heartbeat to keep shreds flowing. Received shreds are distributed to all DEST_IP_PORTS. We recommend running a proxy instance for each region where you have validators or RPCs.

## Preparation

1. Get your Solana pubic key approved

2. Ensure your firewall is open.
    - Default port for incoming shreds is 20000/udp.
    - NAT connections currently not supported.
    - If you use a firewall, see the firewall configuration section

3. Find your TVU port
    - Run get_tvu_port.sh to find your port
    - Example on machine with solana validator: 
      ```bash
      export LEDGER_DIR=MY_LEDGER_DIR; bash -c "$(curl -fsSL https://raw.githubusercontent.com/jito-labs/shredstream-proxy/master/scripts/get_tvu_port.sh)"
      ```
    - Example on remote machine (port may differ): 
      ```bash
      export HOST=http://1.2.3.4:8899; bash -c "$(curl -fsSL https://raw.githubusercontent.com/jito-labs/shredstream-proxy/master/scripts/get_tvu_port.sh)"
      ```

4. Run via docker or natively and set the following parameters
    - `BLOCK_ENGINE_URL`: set to the closest region to your validator/RPC node
    - `DESIRED_REGIONS`: set to regions you want to receive shreds from. Same regions as for Block Engine
    - `DEST_IP_PORTS`: IP:Port combinations to receive shreds on
    - Note: these examples will receive shreds from amsterdam and ny, and directly connect to ny region

## Running via Docker

View logs with `docker logs -f jito-shredstream-proxy`

### 🐳 Host Networking (Recommended)

This exposes all ports, bypassing Docker NAT.

```bash
docker run -d \
--name jito-shredstream-proxy \
--rm \
--env RUST_LOG=info \
--env BLOCK_ENGINE_URL=https://ny.mainnet.block-engine.jito.wtf \
--env AUTH_KEYPAIR=my_keypair.json \
--env DESIRED_REGIONS=amsterdam,ny \
--env DEST_IP_PORTS=127.0.0.1:8001,10.0.0.1:8001 \
--network host \
-v $(pwd)/my_keypair.json:/app/my_keypair.json \
jitolabs/jito-shredstream-proxy shredstream
```

### 🚝 Bridge Networking

Use bridge networking in environments where Docker host networking is unavailable. This setup requires manual exposure of each destination. For shred listeners running locally on the Docker host, use Docker's bridge IP (typically `172.17.0.1`). For non-local endpoints, use their regular IP addresses. Note that Docker's bridge IP can vary, so confirm it by running: `ip -brief address show dev docker0`.

```bash
docker run -d \
--name jito-shredstream-proxy \
--rm \
--env RUST_LOG=info \
--env BLOCK_ENGINE_URL=https://ny.mainnet.block-engine.jito.wtf \
--env AUTH_KEYPAIR=my_keypair.json \
--env DESIRED_REGIONS=amsterdam,ny \
--env SRC_BIND_PORT=20000 \
--env DEST_IP_PORTS=172.17.0.1:8001,10.0.0.1:8001 \
--network bridge \
-p 20000:20000/udp \
-v $(pwd)/my_keypair.json:/app/my_keypair.json \
jitolabs/jito-shredstream-proxy shredstream
```

### 🦾 Running Natively


```bash
git clone https://github.com/jito-labs/shredstream-proxy.git --recurse-submodules

RUST_LOG=info cargo run --release --bin jito-shredstream-proxy -- shredstream \
    --block-engine-url https://ny.mainnet.block-engine.jito.wtf \
    --auth-keypair my_keypair.json \
    --desired-regions amsterdam,ny \
    --dest-ip-ports 127.0.0.1:8001,10.0.0.1:8001
```

### 📛 Firewall Configuration

If you use a firewall, allow access to the following IPs:

| Location        | IP Addresses                                     |
|-----------------|--------------------------------------------------|
| 🇳🇱 Amsterdam       | `74.118.140.240`, `202.8.8.174`                  |
| 🇩🇪 Frankfurt       | `145.40.93.84`, `145.40.93.41`                   |
| 🇺🇸 New York        | `141.98.216.96`, `64.130.48.56`                  |
| 🇺🇸 Salt Lake City  | `64.130.53.8`, `64.130.53.57`                    |
| 🇯🇵 Tokyo           | `202.8.9.160`, `202.8.9.19`                      |

## Troubleshooting

Ensure ShredStream is running correctly by configuring the `SOLANA_METRICS_CONFIG` in your RPC setup. Refer to [Solana Clusters Documentation](https://docs.solana.com/clusters) for details.

To verify, query the number of packets received before and after configuring ShredStream using:

```sql
SELECT shred_count FROM "shred_fetch" WHERE time > now() - 1h
```
