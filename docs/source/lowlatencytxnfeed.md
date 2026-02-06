# ➤ Low Latency Block Updates (Shredstream)

Jito's ShredStream service delivers the lowest latency shreds from leaders on the Solana network, optimizing performance for high-frequency trading, validation, and RPC operations. ShredStream ensures minimal latency for receiving shreds, which can save hundreds of milliseconds during trading on Solana—a critical advantage in high-frequency trading environments. Additionally, it provides a redundant shred path for servers in remote locations, enhancing reliability and performance for users operating in less connected regions. This makes ShredStream particularly valuable for traders, validators, and node operators who require the fastest and most reliable data to maintain a competitive edge.

## Shreds

Shreds are fragments of data used in the Solana blockchain to represent parts of transactions before they are assembled into a full block. When a validator processes transactions, it breaks them down into smaller units called shreds. These shreds are distributed across the network to other validators and nodes, which then reassemble them to form complete blocks.

Shreds help in fast and efficient data propagation, maintaining Solana's high throughput and low latency. They also provide redundancy and fault tolerance, ensuring that even if some data is lost or delayed during transmission, the network can still reconstruct the necessary information. Shreds are crucial for enabling Solana’s rapid block times and overall network performance.

## Setup

## Jito ShredStream Proxy

The proxy client connects to the Jito Block Engine and authenticates using the provided keypair. It sends a heartbeat to keep shreds flowing. Received shreds are distributed to all `DEST_IP_PORTS`. We recommend running a proxy instance for each region where you have RPCs.

## Preparation

1. Get your Solana [public key approved](https://web.miniextensions.com/WV3gZjFwqNqITsMufIEp)

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

Use bridge networking in environments where Docker host networking is unavailable. Note: This does **not** work with Multicast. This setup requires manual exposure of `SRC_BIND_PORT`. For shred listeners running locally on the Docker host, use Docker's bridge IP (typically `172.17.0.1`). For non-local endpoints, use their regular IP addresses. Note that Docker's bridge IP can vary, so confirm it by running: `ip -brief address show dev docker0`.

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


### DoubleZero Multicast Setup (Coming Soon!)

- Multicast shreds are sent over `20001/udp`.
- Note: this does **not** work with Docker bridge networking

1. Install DoubleZero CLI: https://docs.malbeclabs.com/setup/#steps
2. Get authorization from DoubleZero (todo!)
3. Connect to Shredstream multicast group

   `doublezero connect multicast subscriber jito-shredstream-mainnet`
4.  Verify shreds are being received
    
   ```bash
   IP=$(doublezero multicast group list --json | jq -r '.[] | select(.code|startswith("jito-shredstream-mainnet")) | .multicast_ip')
   socat UDP4-RECVFROM:20001,ip-add-membership=${IP}:doublezero1 -
   ```
5. Start Shredstream Proxy using native or host networking mode (**not** bridge networking), grepping the logs for `Multicast`

### Decoding Shreds

Decoding shreds lets you access transactions without running a full Solana node. Add `GRPC_SERVICE_PORT=<PORT>` environment variable or `--grpc-service-port <PORT>` arg to start the gRPC server which streams out transactions to gRPC clients. See the [Entry type](https://github.com/jito-labs/mev-protos/blob/master/shredstream.proto#L48) of the protobuf for more details. A sample client implementation is available in the [deshred](https://github.com/jito-labs/shredstream-proxy/blob/master/examples/deshred.rs) example.

### 📛 Firewall Configuration

If you use a firewall, allow access to the following IPs:

| Location            | IP Addresses                                                                                                                                                    |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🇳🇱 Amsterdam      | `74.118.140.240`, `202.8.8.174`, `64.130.42.228`, `64.130.43.92`, `64.130.55.26`, `64.130.42.227`, `64.130.43.19`, `64.130.55.28`, `63.254.166.12`, `198.13.134.208`, `198.13.134.231` |
| 🇮🇪 Dublin         | `64.130.61.138`, `64.130.61.139`, `64.130.61.140`                                                                                                               |
| 🇩🇪 Frankfurt      | `64.130.50.14`, `64.130.57.46`, `64.130.40.25`, `64.130.57.99`, `64.130.57.171`, `64.130.40.23`, `64.130.40.22`, `64.130.40.21`, `64.130.40.26`, `64.130.40.24` |
| 🇬🇧 London         | `142.91.127.175`, `64.130.46.71`, `64.130.63.195`, `64.130.46.72`, `64.130.63.196`, `64.130.46.73`                                                              |
| 🇺🇸 New York       | `141.98.216.96`, `64.130.51.60`, `64.130.34.186`, `64.130.34.143`, `64.130.34.142`, `64.130.34.189`, `64.130.34.190`, `64.130.34.141`                           |
| 🇺🇸 Salt Lake City | `64.130.53.8`, `64.130.53.57`, `64.130.53.81`, `64.130.53.90`, `64.130.53.82`, `64.130.33.181`, `64.130.33.88`                                                  |
| 🇸🇬 Singapore      | `202.8.11.224`, `202.8.11.173`, `202.8.11.102`, `202.8.11.103`, `202.8.11.104`                                                                                  |
| 🇯🇵 Tokyo          | `202.8.9.160`, `202.8.9.187`, `63.254.162.35`, `64.130.49.109`, `208.91.109.102`, `198.13.133.123`                                                              |

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
