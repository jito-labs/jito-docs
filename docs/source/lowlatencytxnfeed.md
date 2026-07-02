# ➤ Low Latency Block Updates (Shredstream)

> **🚨 Jito ShredStream Deprecation Notice 🚨**
>
> Jito ShredStream will be deprecated in 60 days (effective **September 5, 2026**).
>
> To ensure uninterrupted access to Solana shreds, we recommend transitioning to **DoubleZero Edge** as the path forward. DoubleZero has put together a comprehensive transition guide specifically for our users. Eligible existing Jito ShredStream validators have access to a **90-day free trial**, so we encourage you to check it out and begin migrating soon.
>
> 🔗 Full details on the migration, performance benchmarks, and how to claim your free trial can be found here: [DoubleZero migration guide](TODO-INSERT-DOUBLEZERO-URL).
>
> If you need any support getting set up, head over to the **#jito-shredstream** channel in the DoubleZero Discord.

Jito's ShredStream service delivers the lowest latency shreds from leaders on the Solana network, optimizing performance for high-frequency trading, validation, and RPC operations. ShredStream ensures minimal latency for receiving shreds, which can save hundreds of milliseconds during trading on Solana—a critical advantage in high-frequency trading environments. Additionally, it provides a redundant shred path for servers in remote locations, enhancing reliability and performance for users operating in less connected regions. This makes ShredStream particularly valuable for traders, validators, and node operators who require the fastest and most reliable data to maintain a competitive edge.

## Shreds

Shreds are fragments of data used in the Solana blockchain to represent parts of transactions before they are assembled into a full block. When a validator processes transactions, it breaks them down into smaller units called shreds. These shreds are distributed across the network to other validators and nodes, which then reassemble them to form complete blocks.

Shreds help in fast and efficient data propagation, maintaining Solana's high throughput and low latency. They also provide redundancy and fault tolerance, ensuring that even if some data is lost or delayed during transmission, the network can still reconstruct the necessary information. Shreds are crucial for enabling Solana’s rapid block times and overall network performance.

## Setup

## Jito ShredStream Proxy

The proxy client connects to the Jito Block Engine and authenticates using the provided keypair. It sends a heartbeat to keep shreds flowing. Received shreds are distributed to all `DEST_IP_PORTS`. We recommend running a proxy instance for each region where you have RPCs.

## Preparation

1. Get your Solana [public key approved](https://discord.com/channels/938287290806042626/1336799632898134037)

2. Ensure your firewall is open.
    - Default port for incoming unicast shreds is `20000/udp`.
    - NAT connections currently not supported.
    - If you use a firewall, see the firewall configuration section

3. Find your TVU port
    - Run get_tvu_port.sh to find your port
    - Example on machine with Solana RPC: 
      ```bash
      export LEDGER_DIR=MY_LEDGER_DIR; bash -c "$(curl -fsSL https://raw.githubusercontent.com/jito-labs/shredstream-proxy/master/scripts/get_tvu_port.sh)"
      ```
    - Example on remote machine (port may differ): 
      ```bash
      export HOST=http://1.2.3.4:8899; bash -c "$(curl -fsSL https://raw.githubusercontent.com/jito-labs/shredstream-proxy/master/scripts/get_tvu_port.sh)"
      ```

4. Run via docker or natively and set the following parameters
    - `BLOCK_ENGINE_URL`: https://mainnet.block-engine.jito.wtf
    - `DESIRED_REGIONS`: Comma-delimited regions you want to receive shreds from, maximum of 2 regions, anything in excess will be ignored. [Same regions as for Block Engine](#api)
    - `DEST_IP_PORTS`: Comma-delimited IP:Port combinations to receive shreds on
    - Note: these examples will receive shreds from `amsterdam` and `ny` regions


### 🦾 Running Natively

```bash
git clone https://github.com/jito-labs/shredstream-proxy.git --recurse-submodules

RUST_LOG=info cargo run --release --bin jito-shredstream-proxy -- shredstream \
    --block-engine-url https://mainnet.block-engine.jito.wtf \
    --auth-keypair my_keypair.json \
    --desired-regions amsterdam,ny \
    --dest-ip-ports 127.0.0.1:8001,10.0.0.1:8001
```

## Running via Docker

View logs with `docker logs -f jito-shredstream-proxy`

### 🐳 Host Networking (Recommended)

This exposes all ports, bypassing Docker NAT.

```bash
docker run -d \
--name jito-shredstream-proxy \
--rm \
--env RUST_LOG=info \
--env BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf \
--env AUTH_KEYPAIR=my_keypair.json \
--env DESIRED_REGIONS=amsterdam,ny \
--env DEST_IP_PORTS=127.0.0.1:8001,10.0.0.1:8001 \
--network host \
-v $(pwd)/my_keypair.json:/app/my_keypair.json \
jitolabs/jito-shredstream-proxy shredstream
```

### 🚝 Bridge Networking

Use bridge networking in environments where Docker host networking is unavailable. Note: This setup requires manual exposure of `SRC_BIND_PORT`. For shred listeners running locally on the Docker host, use Docker's bridge IP (typically `172.17.0.1`). For non-local endpoints, use their regular IP addresses. Note that Docker's bridge IP can vary, so confirm it by running: `ip -brief address show dev docker0`.

```bash
docker run -d \
--name jito-shredstream-proxy \
--rm \
--env RUST_LOG=info \
--env BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf \
--env AUTH_KEYPAIR=my_keypair.json \
--env DESIRED_REGIONS=amsterdam,ny \
--env SRC_BIND_PORT=20000 \
--env DEST_IP_PORTS=172.17.0.1:8001,10.0.0.1:8001 \
--network bridge \
-p 20000:20000/udp \
-v $(pwd)/my_keypair.json:/app/my_keypair.json \
jitolabs/jito-shredstream-proxy shredstream
```

### Decoding Shreds

Decoding shreds lets you access transactions without running a full Solana node. Add `GRPC_SERVICE_PORT=<PORT>` environment variable or `--grpc-service-port <PORT>` arg to start the gRPC server which streams out transactions to gRPC clients. See the [Entry type](https://github.com/jito-labs/mev-protos/blob/master/shredstream.proto#L48) of the protobuf for more details. A sample client implementation is available in the [deshred](https://github.com/jito-labs/shredstream-proxy/blob/master/examples/deshred.rs) example.

### 📛 Firewall Configuration

If you use a firewall, allow access to the following IPs:

| Location            | IP Addresses                                                                                                                                                                           |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🇳🇱 Amsterdam      | `74.118.140.240`, `202.8.8.174`, `64.130.42.228`, `64.130.43.92`, `64.130.55.26`, `64.130.42.227`, `64.130.43.19`, `64.130.55.28`, `63.254.166.12`, `198.13.134.208`, `198.13.134.231` |
| 🇮🇪 Dublin         | `64.130.61.138`, `64.130.61.139`, `64.130.61.140`                                                                                                                                      |
| 🇩🇪 Frankfurt      | `64.130.50.14`, `198.13.137.137`, `64.130.40.25`, `64.130.47.93`, `64.130.57.171`, `64.130.40.23`, `64.130.40.22`, `64.130.40.21`, `64.130.40.26`, `64.130.40.24`                      |
| 🇬🇧 London         | `64.130.46.153`, `64.130.46.71`, `64.130.63.195`, `64.130.46.72`, `64.130.63.196`, `64.130.46.73`                                                                                     |
| 🇺🇸 New York       | `141.98.216.96`, `64.130.51.60`, `64.130.34.186`, `64.130.34.143`, `64.130.34.142`, `64.130.34.189`, `64.130.34.190`, `64.130.34.141`                                                  |
| 🇺🇸 Salt Lake City | `64.130.53.8`, `64.130.53.57`, `64.130.53.81`, `64.130.53.90`, `64.130.53.82`, `64.130.33.181`, `64.130.33.88`                                                                         |
| 🇸🇬 Singapore      | `202.8.11.224`, `202.8.11.173`, `202.8.11.102`, `202.8.11.103`, `202.8.11.104`                                                                                                         |
| 🇯🇵 Tokyo          | `202.8.9.160`, `202.8.9.187`, `63.254.162.35`, `64.130.49.109`, `208.91.109.102`, `198.13.133.123`                                                                                     |

## Troubleshooting
1. Confirm shreds are reaching your server by inspecting packet flow (default `SRC_BIND_PORT` is `20000`, adjust accordingly):
```bash
sudo tcpdump 'udp and dst port 20000'
```
You should see many shreds of ~1200 bytes being received.

2. Ensure your firewall allows UDP packets on your `SRC_BIND_PORT`

3. Ensure your RPC is receiving shreds by configuring the `SOLANA_METRICS_CONFIG` in your systemd unit/startup script. Refer to [Solana Clusters Documentation](https://docs.solana.com/clusters) for details.
To verify, query the number of packets received by your RPC before and after configuring ShredStream in InfluxDB:
```sql
SELECT shred_count FROM "shred_fetch" WHERE time > now() - 1h
```
