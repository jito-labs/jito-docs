<!-- Source: jito-foundation/jito-omnidocs PR #87 + #90 (fullsend/), copied at 8c0278c. Re-sync from omnidocs if those PRs change before merge. -->

# 🌪️ FullSend

FullSend is ultra low-latency transaction sending, essential for applications on Solana with
high volume, throughput, and privacy needs.

**Get access:** complete the [FullSend access form](https://form.typeform.com/to/Sbp2rwtT) and
the team will reach out.

(fs-overview)=
## Overview

FullSend provides a Solana JSON-RPC compatible `sendTransaction` interface for low-latency SWQOS direct-to-leader sends with 100% land rates. It is designed to serve applications that want fast, reliable execution and control over who interacts, handles, or sees your transactions.

### Features and Benefits

- **Low-latency**: Direct-to-leader TPU transaction delivery
- **Easy adoption**: Solana-compatible sendTransaction API
- **Browser-optimized**: fast CORS-safe sending
- **Direct regional endpoints**: Send directly to servers in New York, Frankfurt, and Tokyo
- **Secure client side integration**: API-key and authorized-signer authentication
- **Greater control over MEV exposure**: Apply default and custom MEV-protection blacklists

### Endpoint

- Base URL: `https://mainnet.hudson.jito.wtf`

Add your API key as a query parameter:

```text
https://mainnet.hudson.jito.wtf/?api_key=<YOUR_API_KEY>
```

Both MEV protection lists are enabled by default.
Only include query params in the URL if you want to turn one off:

```text
https://mainnet.hudson.jito.wtf/?api_key=<YOUR_API_KEY>&mev_protection_custom=false
```

Continue to [sendTransaction](#fs-send-transaction) for integration examples.


(fs-pricing)=
## Pricing

Every FullSend transaction must include a tip payment to one of the FullSend tip addresses. The amount depends on your TPS rate limit. For example, if your rate limit is 5 TPS, you must pay 1M lamports per transaction. If your rate limit is 25 TPS, you must pay 10k lamports per transaction. Otherwise, your transaction will get dropped.

| **TPS** | **Tip (lamports)** | **Tip (SOL)** |
|---:|---:|---:|
| 5 | 1,000,000 | 0.001 |
| 10 | 100,000 | 0.0001 |
| 25 | 10,000 | 0.00001 |

Tip payments use the standard Solana system transfer instruction and are conditional upon successful execution. If the transaction fails, the tip is not transferred.

### Tip Addresses

We will provide the tip addresses upon access.


(fs-send-transaction)=
## sendTransaction

The service accepts Solana JSON-RPC `sendTransaction` requests, so standard Solana RPC clients work with the service URL.

### Endpoint

Send the request to either path. They accept the same JSON-RPC body and behave the same way:

- `POST /`: the root of the service URL. This is where standard Solana RPC clients send requests when you set the service URL as their RPC URL.
- `POST /api/v1/sendTransaction`: the same `sendTransaction` call at an explicit path, for clients that build the request themselves.

For most clients, set RPC URL to:

```text
https://mainnet.hudson.jito.wtf/?api_key=<YOUR_API_KEY>
```

Both the default MEV blacklist and your customer-specific MEV blacklist are enabled by default.
Only add `mev_protection_default=false` and/or `mev_protection_custom=false` if you want to disable one.


### Authentication

Pass your API key as a query parameter on the RPC URL:

```text
https://mainnet.hudson.jito.wtf/?api_key=<YOUR_API_KEY>
```

If you need to expose the send URL from client-side apps (browser/mobile), use the [Authorized Signers API](#fs-authorized-signers), or reach out to Jito for another auth model (for example IP allowlisting).

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendTransaction",
  "params": [
    "<encoded_tx>",
    { "encoding": "base64", "minContextSlot": 123 }
  ]
}
```

- `params[0]`: required encoded signed transaction
- `params[1]`: optional send config

### Rust Example (`solana_client`)

```rust
use solana_client::rpc_client::RpcClient;
use solana_sdk::signature::Signature;
use solana_sdk::transaction::VersionedTransaction;

pub fn create_client(
    api_key: &str,
) -> RpcClient {
    let rpc_url = format!("https://mainnet.hudson.jito.wtf/?api_key={api_key}");
    RpcClient::new(rpc_url)
}

pub fn send_transaction(
    client: &RpcClient,
    tx: &VersionedTransaction,
) -> anyhow::Result<Signature> {
    // This "Jito send client" is just a normal Solana RPC client with the service URL.
    // Commitment/simulation/confirmation semantics are not provided by the service.
    // This endpoint accepts the signed tx and forwards it to leaders.
    Ok(client.send_transaction(tx)?)
}
```

### TypeScript Example (`@solana/web3.js`)

```ts
import { Connection, VersionedTransaction } from "@solana/web3.js";

export function createClient(
  apiKey: string
): Connection {
  const rpcUrl =
    `https://mainnet.hudson.jito.wtf/?api_key=${encodeURIComponent(apiKey)}`;
  return new Connection(rpcUrl, "confirmed");
}

export async function sendTransaction(
  client: Connection,
  signedTx: VersionedTransaction
): Promise<string> {
  // This "Jito send client" is just a normal Solana RPC client with the service URL.
  // Commitment/simulation/confirmation semantics are not provided by the service.
  // This endpoint accepts the signed tx and forwards it to leaders.
  return client.sendTransaction(signedTx, {
    skipPreflight: true,
    maxRetries: 0,
  });
}
```

### Send Controls

`sendTransaction` behavior can be controlled with:

- [MEV Protection API](#fs-mev-protection): manage your custom blacklist and/or use the default blacklist.
- [Authorized Signers API](#fs-authorized-signers): submit from client-side apps without exposing API keys.

### Compatibility Notes

The service is wire-compatible with Solana JSON-RPC `sendTransaction` request/response format.

Service behavior is intentionally focused on landing:

- Accepts your JSON-RPC encoded signed transaction and immediately forwards to current/upcoming leaders.
- Does not run transaction simulation.
- Does not provide confirmation tracking or commitment-level processing.

(fs-send-transaction-web)=
## Send from the browser (sendTransactionWeb)

Low-latency, browser-optimized transaction submission. Eliminates CORS preflight overhead and JSON-RPC parsing by accepting raw base64 as `text/plain`, and returns CORS headers so browser code can read the response cross-origin.

### Why Use This Endpoint

Browser clients sending transactions via the standard JSON-RPC `sendTransaction` endpoint incur extra latency:

1. **CORS preflight** — `Content-Type: application/json` is not a [CORS-safelisted](https://developer.mozilla.org/en-US/docs/Glossary/CORS-safelisted_request_header) content type, so browsers send an `OPTIONS` preflight request before every `POST`. That's an extra round trip on every transaction.
2. **JSON-RPC overhead** — encoding the transaction inside a JSON-RPC envelope and parsing the response adds unnecessary work for browser clients that just need to fire a transaction.

`sendTransactionWeb` removes both:

- Uses **`text/plain`** content type — a CORS simple request, so browsers skip the preflight entirely.
- Accepts the **raw base64-encoded transaction** as the body — no JSON-RPC wrapper needed.
- Returns **HTTP status codes** only — no response body to parse.
- Returns **`Access-Control-Allow-Origin: *`** on every response, so browser code can read the status directly.

### Endpoint

```text
POST /api/v1/sendTransactionWeb
```

### Authentication

This endpoint authenticates via [Authorized Signers](#fs-authorized-signers). The fee payer (first signer) of the transaction must be registered as an authorized signer. No API key is passed in the request, which makes it safe to call directly from browser/mobile clients.

The authorized signer must map to an enabled API key with available rate limit capacity.

See [Setup](#fs-setup) below for how to register your signer.

### Request Format

Send the **base64-encoded signed transaction** as the raw request body with `Content-Type: text/plain`.

```text
POST /api/v1/sendTransactionWeb?mev_protection_default=true
Content-Type: text/plain

<base64_encoded_transaction>
```

#### Query Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mev_protection_default` | bool | `true` | Enable default MEV protection blacklist |
| `mev_protection_custom` | bool | `true` | Enable your custom MEV protection blacklist |

### Response

Returns an HTTP status code with an empty body.

All responses include:

```text
Access-Control-Allow-Origin: *
```

That lets cross-origin browser code inspect `response.ok` and `response.status`.

| Status | Meaning |
|---|---|
| `200 OK` | Transaction queued successfully |
| `400 Bad Request` | Invalid body (empty, not valid UTF-8, base64 decode failure, transaction too large, or deserialization failure) |
| `401 Unauthorized` | Fee payer is not a registered authorized signer, or the backing API key is disabled |
| `429 Too Many Requests` | Backing API key is rate-limited |
| `500 Internal Server Error` | Failed to queue the transaction internally |

### TypeScript Example

```ts
import { VersionedTransaction } from "@solana/web3.js";

const ENDPOINT = "https://mainnet.hudson.jito.wtf/api/v1/sendTransactionWeb";

export async function sendTransactionWeb(
  signedTx: VersionedTransaction,
  mevProtectionDefault = true,
  mevProtectionCustom = true
): Promise<void> {
  const serialized = signedTx.serialize();
  const base64Tx = btoa(String.fromCharCode(...serialized));

  const url = new URL(ENDPOINT);
  url.searchParams.set("mev_protection_default", String(mevProtectionDefault));
  url.searchParams.set("mev_protection_custom", String(mevProtectionCustom));

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: base64Tx,
  });

  if (!response.ok) {
    throw new Error(`sendTransactionWeb failed: ${response.status}`);
  }
}
```

### Connection Warm-Up

If you want to warm a connection before submitting a transaction, use [`GET /api/v1/ping`](#fs-ping).

(fs-setup)=
### Setup

Register your fee-payer pubkey as an authorized signer using the [Authorized Signers API](#fs-authorized-signers). Once registered, your browser client can call `sendTransactionWeb` directly with no API key.

### Comparison with sendTransaction

| | `sendTransaction` | `sendTransactionWeb` |
|---|---|---|
| Optimized for | Server-side / general purpose | Browser clients |
| Content type | `application/json` (JSON-RPC) | `text/plain` (raw base64) |
| CORS preflight | Yes (`application/json` triggers preflight) | No for simple requests (`text/plain` body, no custom headers) |
| Response format | JSON-RPC envelope | HTTP status code only |
| Browser-readable cross-origin response | Not intended for direct browser use | Yes |
| Encoding | Base58 (default) or base64 | Base64 only |
| Auth | API key or authorized signer | Authorized signer only |

(fs-regional-direct)=
## Regional direct endpoints

Direct regional endpoints for server-to-server transaction submission.

**Requirements:**
- Your server IPs must be whitelisted (contact Jito)
- Server-side only — not for browser/web clients
- Self-signed TLS — disable certificate verification in your HTTP client

### Regional Endpoints

| Region | Endpoint |
|--------|----------|
| New York | `https://ewr1.mainnet.fullsend.jito.wtf:8443` |
| Frankfurt | `https://fra1.mainnet.fullsend.jito.wtf:8443` |
| Tokyo | `https://tyo1.mainnet.fullsend.jito.wtf:8443` |

### Request Format

POST to `/api/v1/sendTransaction` with JSON-RPC payload:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendTransaction",
  "params": [
    "<base64_encoded_tx>",
    { "encoding": "base64" }
  ]
}
```

### Rust Example

Build your own HTTP client with TLS verification disabled:

```rust
use anyhow::{anyhow, Result};
use reqwest::Client;
use serde_json::{json, Value};
use solana_sdk::signature::Signature;
use solana_sdk::transaction::VersionedTransaction;
use std::str::FromStr;
use std::time::Duration;

const TIMEOUT_MS: u64 = 1_000;

const ENDPOINTS: &[&str] = &[
    "https://ewr1.mainnet.fullsend.jito.wtf:8443",
    "https://fra1.mainnet.fullsend.jito.wtf:8443",
    "https://tyo1.mainnet.fullsend.jito.wtf:8443",
];

fn build_client() -> Result<Client> {
    Client::builder()
        .danger_accept_invalid_certs(true)
        .timeout(Duration::from_millis(TIMEOUT_MS))
        .build()
        .map_err(|e| anyhow!("Failed to build client: {e}"))
}

async fn send_transaction(
    client: &Client,
    endpoint: &str,
    tx: &VersionedTransaction,
) -> Result<Signature> {
    let tx_bytes = bincode::serialize(tx)?;
    let tx_base64 = base64::Engine::encode(
        &base64::engine::general_purpose::STANDARD,
        &tx_bytes,
    );

    let request = json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [tx_base64, { "encoding": "base64" }]
    });

    let url = format!("{endpoint}/api/v1/sendTransaction");
    let response = client
        .post(&url)
        .header("Content-Type", "application/json")
        .json(&request)
        .send()
        .await?;

    let body: Value = response.json().await?;

    if let Some(error) = body.get("error") {
        return Err(anyhow!("JSON-RPC error: {error}"));
    }

    let sig = body
        .get("result")
        .and_then(|v| v.as_str())
        .ok_or_else(|| anyhow!("Missing result in response"))?;

    Signature::from_str(sig).map_err(|e| anyhow!("Invalid signature: {e}"))
}

/// Send with failover to next region on timeout/error
async fn send_with_failover(
    client: &Client,
    tx: &VersionedTransaction,
) -> Result<Signature> {
    for endpoint in ENDPOINTS {
        match send_transaction(client, endpoint, tx).await {
            Ok(sig) => return Ok(sig),
            Err(e) => eprintln!("Failed {endpoint}: {e}"),
        }
    }
    Err(anyhow!("All regional endpoints failed"))
}
```

### Failover Strategy

The client must manage failover manually:

1. Set an aggressive timeout (1000ms recommended)
2. On timeout or error, retry with the next closest regional endpoint
3. Order endpoints by proximity to your server location

Example ordering for a US-East server:
1. `ewr1` (New York) — primary
2. `fra1` (Frankfurt) — fallback
3. `tyo1` (Tokyo) — last resort

(fs-ping)=
## Ping

Lightweight keepalive endpoint. Use this to warm the HTTP/TCP connection before making requests to the service.

### Endpoint

```text
GET /api/v1/ping
```

### Authentication

No auth is required.

### Response

Always returns:

```text
200 OK
Access-Control-Allow-Origin: *
Content-Type: text/plain; charset=utf-8

ok
```

### TypeScript Example

```ts
const ENDPOINT = "https://mainnet.hudson.jito.wtf/api/v1/ping";

export async function warmConnection(): Promise<void> {
  const response = await fetch(ENDPOINT, {
    method: "GET",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`ping failed: ${response.status}`);
  }
}
```

(fs-mev-protection)=
## MEV protection

To protect transactions from malicious MEV, FullSend by default automatically applies an MEV-aware blacklist that will skip validators with a history of frontrunning or other types of negative MEV.

Use these endpoints to manage your customer-specific MEV blacklist and/or inspect the default blacklist.

Both lists are applied to `sendTransaction` requests by default.
Set `mev_protection_default=false` and/or `mev_protection_custom=false` on the send URL only when you want to disable one.


### Authentication

Customer-list endpoints require `api_key`.

```text
?api_key=<YOUR_API_KEY>
```

### Add to Custom MEV Blacklist

- Endpoint: `POST /mev-protection/custom-blacklist`
- Auth: required

Request:

```text
POST /mev-protection/custom-blacklist?api_key=<YOUR_API_KEY>
Content-Type: application/json

{
  "validator_vote_accounts": [
    "<vote_account_pubkey_1>",
    "<vote_account_pubkey_2>"
  ]
}
```

Response:

```json
{
  "success": true,
  "inserted": ["<vote_account_pubkey_1>"],
  "already_present": ["<vote_account_pubkey_2>"],
  "message": "Inserted 1 of 2 pubkeys (1 already present)"
}
```

### Remove from Custom MEV Blacklist

- Endpoint: `DELETE /mev-protection/custom-blacklist`
- Auth: required

Request:

```text
DELETE /mev-protection/custom-blacklist?api_key=<YOUR_API_KEY>
Content-Type: application/json

{
  "validator_vote_accounts": [
    "<vote_account_pubkey_1>",
    "<vote_account_pubkey_2>"
  ]
}
```

Response:

```json
{
  "success": true,
  "removed": ["<vote_account_pubkey_1>"],
  "not_present": ["<vote_account_pubkey_2>"],
  "message": "Removed 1 pubkeys (1 were not present)"
}
```

### Get Custom MEV Blacklist

- Endpoint: `GET /mev-protection/custom-blacklist`
- Auth: required

Request:

```text
GET /mev-protection/custom-blacklist?api_key=<YOUR_API_KEY>
```

Response:

```json
{
  "success": true,
  "validator_vote_accounts": ["<vote_account_pubkey_1>", "<vote_account_pubkey_2>"]
}
```

### Get Default MEV Blacklist

- Endpoint: `GET /mev-protection/default-blacklist`
- Auth: required

Request:

```text
GET /mev-protection/default-blacklist?api_key=<YOUR_API_KEY>
```

Response:

```json
{
  "success": true,
  "validator_vote_accounts": []
}
```

(fs-authorized-signers)=
## Authorized signers

Authorized signers are recommended when you need client-side transaction submission without exposing your API key.

### Why Use Authorized Signers

If you expose a raw service URL containing `api_key` in client code, the key can be extracted and your rate limit can be abused.

A safer pattern is:

1. Keep API key private on backend.
2. Have backend sign transactions as fee-payer.
3. Register those signer pubkeys as authorized signers.
4. Let client submit signed transactions without embedding API key.

Today, fallback auth for `sendTransaction` uses the first signer (fee payer). If you want to use this feature without signing as fee payer reach out and we can implement that.

### Authentication

All endpoints here require `api_key`.

```text
?api_key=<YOUR_API_KEY>
```

### Add Authorized Signers

- Endpoint: `POST /authorized-signers`

Request:

```text
POST /authorized-signers?api_key=<YOUR_API_KEY>
Content-Type: application/json

{
  "signers": [
    "<signer_pubkey_1>",
    "<signer_pubkey_2>"
  ]
}
```

Response:

```json
{
  "success": true,
  "inserted": ["<signer_pubkey_1>"],
  "already_present": ["<signer_pubkey_2>"],
  "message": "Inserted 1 of 2 signers (1 already present)"
}
```

### Remove Authorized Signers

- Endpoint: `DELETE /authorized-signers`

Request:

```text
DELETE /authorized-signers?api_key=<YOUR_API_KEY>
Content-Type: application/json

{
  "signers": [
    "<signer_pubkey_1>",
    "<signer_pubkey_2>"
  ]
}
```

Response:

```json
{
  "success": true,
  "removed": ["<signer_pubkey_1>"],
  "not_present": ["<signer_pubkey_2>"],
  "message": "Removed 1 signers (1 were not present)"
}
```

### Get Authorized Signers

- Endpoint: `GET /authorized-signers`

Request:

```text
GET /authorized-signers?api_key=<YOUR_API_KEY>
```

Response:

```json
{
  "success": true,
  "signers": ["<signer_pubkey_1>", "<signer_pubkey_2>"]
}
```
