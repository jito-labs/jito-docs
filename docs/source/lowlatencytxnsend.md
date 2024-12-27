# ⚡ Low Latency Transaction Send

Jito provides Solana MEV users with superior transaction execution through fast landing, MEV protection, and revert protection, available for both single transactions and multiple transactions(bundles) via gRPC and JSON-RPC services, ensuring optimal performance in the highly competitive Solana ecosystem."
:::{figure} ../images/matrixtxnsv4.png
:class: diagram
:::

---

## System Overview

:::{figure} ../images/systemdiagramv2.png
:class: diagram
:::

### 🌐 How does the system work?
- Validators run a modified Agave validator client called Jito-Solana that enables higher value capture for them and their stakers
  - The validator then connects to the Jito Block-Engine and Jito-Relayer
  - The Block-Engine submits profitable bundles to the validator
  - The Relayer acts as a proxy to filter and verify transactions for validators
- Searchers, dApps, Telegram bots and others connect to the Block-Engine and submit transactions & bundles.
  - Submissions can be over gRPC or JSON-RPC
  - Bundles have tips bids associated with them; these bids are then redistributed to the validators and their stakers

### 💼 What are bundles?
- Bundles are groups of transactions (max 5) bundled together
- The transactions are executed sequentially and atomically meaning all-or-nothing
- Bundles enable complex MEV strategies like atomic arbitrage
- Bundles compete against other bundles on tips to the validator

### 📬 How do Bundles work?
- Traders submit bundle to block engines
- Block engines simulate bundles to determine the most profitable combinations
- Winning bundles are sent to validators to include in blocks
- Validators execute bundles atomically and collect tips
- MEV rewards from bundles are distributed to validators and stakers

### ⚖️ What is the auction?
- Bundles submitted by traders are put through a priority auction
  - An auction is needed since opportunities and blockspace are scarce
  - The auction creates a stream of bundles that maximizes tips in a block.
    Parallelism in locking patterns is leveraged where possible to allow for local state auctions.
- Parallel auctions are run at 200ms ticks
  - Bundles with intersecting locking patterns on a particular account [(w, w) or (r, w) or (w, r)] are run in a single auction.
  - Bundles that do not touch the same accounts are run in separate auctions, as well as bundles that have non-intersecting locking patterns (r, r) on accounts.
  - Bundle orderings within a single auction are prioritized in the auction based on requested tip/cus-requested efficiency.
- Jito submits the highest paying combination of bundles to the validator up to some CU limit

---

## API
You can send JSON-RPC requests to any Block Engine using the following URLs. To route to a specific region, specify the desired region:

| Location                | Block Engine URL                                  | Shred Receiver        | Relayer URL                                      | NTP Server               |
|-------------------------|---------------------------------------------------|-----------------------|--------------------------------------------------|--------------------------|
| 🌍 🌎 🌏 **Mainnet**    | `https://mainnet.block-engine.jito.wtf`           | -                     | -                                                | -                        |
| 🇳🇱 **Amsterdam**      | `https://amsterdam.mainnet.block-engine.jito.wtf` | `74.118.140.240:1002` | `http://amsterdam.mainnet.relayer.jito.wtf:8100` | `ntp.amsterdam.jito.wtf` |
| 🇩🇪 **Frankfurt**      | `https://frankfurt.mainnet.block-engine.jito.wtf` | `64.130.50.14:1002`   | `http://frankfurt.mainnet.relayer.jito.wtf:8100` | `ntp.frankfurt.jito.wtf` |
| 🇺🇸 **New York**       | `https://ny.mainnet.block-engine.jito.wtf`        | `141.98.216.96:1002`  | `http://ny.mainnet.relayer.jito.wtf:8100`        | `ntp.dallas.jito.wtf`    |
| 🇯🇵 **Tokyo**          | `https://tokyo.mainnet.block-engine.jito.wtf`     | `202.8.9.160:1002`    | `http://tokyo.mainnet.relayer.jito.wtf:8100`     | `ntp.tokyo.jito.wtf`     |
| 🇺🇸 **Salt Lake City** | `https://slc.mainnet.block-engine.jito.wtf`       | `64.130.53.8:1002`    | `http://slc.mainnet.relayer.jito.wtf:8100`       | `ntp.slc.jito.wtf`       |
|                         |                                                   |                       |                                                  |                          |
| 🌍 🌎 🌏 **Testnet**    | `https://testnet.block-engine.jito.wtf`           | -                     | -                                                | -                        |
| 🇺🇸 **Dallas**         | `https://dallas.testnet.block-engine.jito.wtf`    | `141.98.218.45:1002`  | `http://dallas.testnet.relayer.jito.wtf:8100`    | `ntp.dallas.jito.wtf`    |
| 🇺🇸 **New York**       | `https://ny.testnet.block-engine.jito.wtf`        | `141.98.216.132:1002` | `http://ny.testnet.relayer.jito.wtf:8100`        | `ntp.dallas.jito.wtf`    |


### 📨 Transactions(`/api/v1/transactions`)

For single transaction-related methods, use the URL path `/api/v1/transactions`

For example: `https://mainnet.block-engine.jito.wtf/api/v1/transactions`

#### sendTransaction

This method acts as a direct proxy to the Solana sendTransaction RPC method, but forwards your transaction directly to the validator. By default, it submits the transaction with providing MEV protection.

Please note that Jito enforces a minimum tip of 1000 lamports for bundles. During high-demand periods, this minimum tip might not be sufficient to successfully navigate the auction, so it’s crucial to set both a priority fee and an additional Jito tip to optimize your transaction's chances. Please see [Tip Amounts](#tip-amount)

For cost efficiency, you can enable revert protection by setting the query parameter bundleOnly=true. With this setting, the transaction is sent exclusively as a single transaction bundle.

Additionally, this method always sets skip_preflight=true, which means the transaction won't be simulated in the RPC before being sent to the leader.

##### Request

| Parameter  | Type   | Description                                                                                                                   |
|------------|--------|-------------------------------------------------------------------------------------------------------------------------------|
| `params`   | string | **REQUIRED**: First Transaction Signature embedded in the transaction, as base58 (slow, DEPRECATED) or base64 encoded string. |
| `encoding` | string | **OPTIONAL**: Encoding used for the transaction data. Values: `base58` (slow, DEPRECATED) or `base64`. Default: `base58`      |

##### Request Example base64
```bash
curl https://mainnet.block-engine.jito.wtf/api/v1/transactions -X POST -H "Content-Type: application/json" -d '
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "sendTransaction",
  "params": [
    "AVXo5X7UNzpuOmYzkZ+fqHDGiRLTSMlWlUCcZKzEV5CIKlrdvZa3/2GrJJfPrXgZqJbYDaGiOnP99tI/sRJfiwwBAAEDRQ/n5E5CLbMbHanUG3+iVvBAWZu0WFM6NoB5xfybQ7kNwwgfIhv6odn2qTUu/gOisDtaeCW1qlwW/gx3ccr/4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvsInicc+E3IZzLqeA+iM5cn9kSaeFzOuClz1Z2kZQy0BAgIAAQwCAAAAAPIFKgEAAAA=",
    {
      "encoding": "base64"
    }
  ]
}'
```

##### Request Example base58

```bash
curl https://mainnet.block-engine.jito.wtf/api/v1/transactions -X POST -H "Content-Type: application/json" -d '
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendTransaction",
  "params": [
    "4hXTCkRzt9WyecNzV1XPgCDfGAZzQKNxLXgynz5QDuWWPSAZBZSHptvWRL3BjCvzUXRdKvHL2b7yGrRQcWyaqsaBCncVG7BFggS8w9snUts67BSh3EqKpXLUm5UMHfD7ZBe9GhARjbNQMLJ1QD3Spr6oMTBU6EhdB4RD8CP2xUxr2u3d6fos36PD98XS6oX8TQjLpsMwncs5DAMiD4nNnR8NBfyghGCWvCVifVwvA8B8TJxE1aiyiv2L429BCWfyzAme5sZW8rDb14NeCQHhZbtNqfXhcp2tAnaAT"
  ]
}'
```


##### Response

| Field    | Type   | Description                                                                                                                                                                                                                                          |
|----------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `result` | string | The result will be the same as described in the [Solana RPC documentation](https://solana.com/docs/rpc/http/sendtransaction). If sending as a bundle was successful, you can get the `bundle_id` from the `x-bundle-id` HTTP header in the response. |

##### Response Example

```json
{
  "jsonrpc": "2.0",
  "result": "2id3YC2jK9G5Wo2phDx4gJVAew8DcY5NAojnVuao8rkxwPYPe8cSwE5GzhEgJA2y8fVjDEo6iR6ykBvDxrTQrtpb",
  "id": 1
}
```

#### JSON-RPC Authentication (UUID):

Please include the following when authenticating with a URL using a UUID:

    Header Field: Include the API key in the x-jito-auth header.

        Example: x-jito-auth: <uuid>

    Query Parameter: Include the API key as a query parameter.

        Example: api/v1/bundles?uuid=<uuid>

### 💼 Bundles (`/api/v1/bundles`)

Bundles are a list of up to 5 transactions that execute sequentially and atomically, ensuring an all-or-nothing outcome. Here’s what that means:

  - **Sequentially:** Transactions in a bundle are guaranteed to execute in the order they are listed.
  - **Atomically:** Bundles execute within the same slot(e.g. a bundle cannot cross slot boundaries). If the entire bundle executes successfully, all transactions are committed to the chain.
  - **All-or-Nothing:** Bundles can only contain successful transactions. If any transaction in a bundle fails, none of the transactions in the bundle will be committed to the chain.

This guarantees that all transactions in a bundle are executed in sequence and either all succeed or none are executed.

For bundle-related methods, use the URL path `/api/v1/bundles`. Refer to the documentation to see the available JSON-RPC endpoints for bundles.

#### sendBundle

Submits a bundled list of signed transactions to the cluster for processing. The transactions are atomically processed in order, meaning if any transaction fails, the entire bundle is rejected (all or nothing). This method relays the bundle created by clients to the leader without any modifications. If the bundle is set to expire after the next Jito-Solana leader, this method immediately returns a success response with a `bundle_id`, indicating the bundle has been received. This does not guarantee the bundle will be processed or land on-chain. To check the bundle status, use `getBundleStatuses` with the `bundle_id`.

A tip is necessary for the bundle to be considered. The tip can be any instruction, top-level or CPI, that transfers SOL to one of the 8 tip accounts. Clients should ensure they have sufficient balance and state assertions allowing the tip to go through conditionally, especially if tipping as a separate transaction. If the tip is too low, the bundle might not be selected during the auction. Use `getTipAccounts` to retrieve the tip accounts. Ideally, select one of the accounts at random to reduce contention.

##### Request

| Parameter  | Type          |   | Description                                                                                                                 |
|------------|---------------|:--|-----------------------------------------------------------------------------------------------------------------------------|
| `params`   | array[string] |   | **REQUIRED**: Fully-signed transactions, as base58 (slow, DEPRECATED) or base64 encoded strings. Maximum of 5 transactions. |
| `encoding` | string        |   | **OPTIONAL**: Encoding used for the transaction data. Values: `base58` (slow, DEPRECATED) or `base64`. Default: `base58`    |

##### Request Example base64

```bash
curl https://mainnet.block-engine.jito.wtf:443/api/v1/bundles -X POST -H "Content-Type: application/json" -d '
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendBundle",
  "params": [
    [
      "AbKi19sammgVRlYLdvIwJ8DGEBCk5TmwgRmwWw+IAlkmIqvIXBfY/qYxrFwQGJZq4UvBXDAqmCTkDvQueLsJGAUBAAECZAJMcn3luKBgXdzj8FTKBu8ndFClGLdh/38acclb7JwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5VmqzBOi86PgXATWyyLk9tLPT8SstEH1LaVXnHY/BoAQECAAAMAgAAAAAAAAAAAAAA",
      "AbJIDFwE1L4b0XraibdKWtKm3gJrGUhrdnfaSJnj9r0QVx3gGjwFB8ZkwWDcg0JXU6BH9ELCuU1uK98Ndud7wwQBAAECZAJMcn3luKBgXdzj8FTKBu8ndFClGLdh/38acclb7JwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5VmqzBOi86PgXATWyyLk9tLPT8SstEH1LaVXnHY/BoAQECAAAMAgAAAAEAAAAAAAAA",
      "AWfyRMfbDTJWbhCX4I8LGTarxXhQbPXw4qkwEMlNwb6fyjll6oEd0pdChDyjKFhz0zPZh/W8avZ7e3sX0O0OHAYBAAECZAJMcn3luKBgXdzj8FTKBu8ndFClGLdh/38acclb7JwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5VmqzBOi86PgXATWyyLk9tLPT8SstEH1LaVXnHY/BoAQECAAAMAgAAAAIAAAAAAAAA",
      "AW1qg6ac61EwnsaV05CC1wk84EDUWR75wUzKLRArGy2oA6DFQffpS9mfmxBsYaoJQXZQPkxDYj7H0YdUjcAGuwIBAAECZAJMcn3luKBgXdzj8FTKBu8ndFClGLdh/38acclb7JwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5VmqzBOi86PgXATWyyLk9tLPT8SstEH1LaVXnHY/BoAQECAAAMAgAAAAMAAAAAAAAA",
      "AfrPPQSnIBDrEXHWUV8l7rMa7Whibfdj69/d12d44PaLxhfQtROXz/x7obKe5M3oJK/fMiMlzoKLU8tno4D4MwYBAAEDZAJMcn3luKBgXdzj8FTKBu8ndFClGLdh/38acclb7Jx4Uhyxec67hYm1VqLV7JTSSYaC/fm7KvWtZOSRzEFT2gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzlWarME6Lzo+BcBNbLIuT20s9PxKy0QfUtpVecdj8GgBAgIAAQwCAAAAAAAAAAAAAAA="
    ],
    {
      "encoding": "base64"
    }
  ]
}'
```

##### Request Example base58

```bash
curl https://mainnet.block-engine.jito.wtf:443/api/v1/bundles -X POST -H "Content-Type: application/json" -d '{                        
  "id": 1,
  "jsonrpc": "2.0",
  "method": "sendBundle",
  "params": [
    [
      "AKkzFdN4gPSEKhWoavYAEg7uGiKmuAwsMEVJ5uM8jxP27c86GERzygxbzGMWDQiPhKKmkwtZh9s8LdeBvuXLY8TEjxtsn7AnZ6JYJP8hsnbNAEprxFVfP4FpVRJM2n35u3DGX4pXsAVQ2ABxGuoRkDQTADCQExcQYf7BzLPFKgyd79MyuHwUBHr3mLbTpLsrRt1Hh5xuuZzuS6dKUSEaH1zWcxNAV57p2yQDnbL21ZQVPijcqgYutCVe7",
      "APtbdutAzvCRteQbcARea4yG88mxABQzzhuyzQYDYtXGjhqdnucwC2VBZhx7ebvnUDsMpU6tBZRzZzwF7C7Qd3GfbgNCgcqoyckRfazUUqWkPHGTtYZsi17tdJAwC2ptHtR7Rt3rnKCBog16tERmu2AJbezFdFnPfDTvH2YTWnzycgkah4u8Y2d5CJZewd8fyQxyWHWARfBmhrxtaC5gALvyYDUKyiehkN2VLNnKH3zwVoBJvRGhe8bPM",
      "DXPV292U8Q3kzS1BVroCWd563WG4yvMCZYcHfbTitkSDEPt49u2ivX2fpYag82MqekNn7E8KD2eM3Uy1whqEU6nNbpMPtkGZn4ukq9arsCdTB5QGR5h1vsWJA7ho8fmzbsrLBDNaV1SeqyeWo85v43YzVyjyv8WDF2ki46Wzvd1BYJ4gu9WJVNryMLknjq747oKsq8xT4tUSDSZNVcfzHN99d3FevzU8FHjyg7paSYdHW8HsDj16Hezzj",
      "HbyLbLGUai4zgdFm1FDq9qXRHjTC4kneK8UsoFDpi447SsJiL7Xr9i4wG6iEzEvGT2MdGXrqzAHHxojQRGKCsbfFNKpQMnZ2BDih9He5XD5ViTQGLQ6fYyF9mCpPkZn91vRAeBbWjPoxdcj5UYjJpKS4zRCfPFnYrRCW2y9k9GdA6N2Rcr9S9kgg96WQoiG4drtoiiYAmx3WqckQs4X3dbe4DV6SAH3ZmZJR8gi87DCSfb8xCerwsXeeT",
      "4kSrVZjKnonsMTFqJwaV7riKfLnxvek5RtF4WuyQGGoUqWVqqLveGjZivVZyn3NGseo6TvFfG1dZPA45V6rjvmKeBuVJdZztaoqifwnYxXH2H6LMMwvz89dHN74kjM5D9Ky7cvNSfEW6uVkiLkXi1aMmSP5gicZf2bWVQk9xA2Ab8WSqaDqEoNEQkTN2ULyxt1N1b9UqqDBQGp4XHrtwnXex6fbWQYkp8ji1gY1NKmz8W7E4KWhCM38ZE21qyzXjivtrny7mK5WbHP2ZM1BPhyNB2qo7fdGYVmhRq"
    ]
  ]
}'
```

##### Response

| Field    | Type   | Description                                                                                                |
|----------|--------|------------------------------------------------------------------------------------------------------------|
| `result` | string | A bundle ID, used to identify the bundle. This is the SHA-256 hash of the bundle's transaction signatures. |

##### Response Example

```json
{
    "jsonrpc": "2.0",
    "result": "2id3YC2jK9G5Wo2phDx4gJVAew8DcY5NAojnVuao8rkxwPYPe8cSwE5GzhEgJA2y8fVjDEo6iR6ykBvDxrTQrtpb",
    "id": 1
}
```

#### getBundleStatuses

Returns the status of submitted bundle(s). This function operates similarly to the Solana RPC method `getSignatureStatuses`. If a `bundle_id` is not found or has not landed, it returns `null`. If found and processed, it returns context information including the slot at which the request was made and results with the `bundle_id(s)` and the transactions along with their slot and confirmation status.

We use `getSignatureStatuses` with the default value of `searchTransactionHistory` set to `false` to check transaction statuses on-chain. This means the RPC call will search only its recent history, including all recent slots plus up to `MAX_RECENT_BLOCKHASHES` rooted slots for the transactions. Currently, `MAX_RECENT_BLOCKHASHES` is 300.

##### Request

| Parameter | Type          | Description                                                    |
|-----------|---------------|----------------------------------------------------------------|
| `params`  | array[string] | **REQUIRED**: An array of bundle IDs to confirm. Maximum of 5. |

##### Request Example

```bash
curl https://mainnet.block-engine.jito.wtf/api/v1/bundles -X POST -H "Content-Type: application/json" -d '
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBundleStatuses",
    "params": [
      [
        "892b79ed49138bfb3aa5441f0df6e06ef34f9ee8f3976c15b323605bae0cf51d"
      ]
    ]
}
'
```

##### Response

| Field    | Type   | Description                                                            |
|----------|--------|------------------------------------------------------------------------|
| `null`   | null   | If the bundle is not found.                                            |
| `object` | object | If the bundle is found, an array of objects with the following fields: |

###### Object Fields

- **bundle_id**: `string`  
  - Bundle ID

- **transactions**: `array[string]`  
  - A list of base-58 encoded signatures applied by the bundle. The list will not be empty.

- **slot**: `u64`  
  - The slot this bundle was processed in.

- **confirmationStatus**: `string`  
  - The bundle transaction's cluster confirmation status; either `processed`, `confirmed`, or `finalized`. See Commitment for more on optimistic confirmation.

- **err**: `object`  
  - This will show any retryable or non-retryable error encountered when getting the bundle status. If retryable, please query again.

##### Response Example

```json
{
  "jsonrpc": "2.0",
  "result": {
    "context": {
      "slot": 242806119
    },
    "value": [
      {
        "bundle_id": "892b79ed49138bfb3aa5441f0df6e06ef34f9ee8f3976c15b323605bae0cf51d",
        "transactions": [
          "3bC2M9fiACSjkTXZDgeNAuQ4ScTsdKGwR42ytFdhUvikqTmBheUxfsR1fDVsM5ADCMMspuwGkdm1uKbU246x5aE3",
          "8t9hKYEYNbLvNqiSzP96S13XF1C2f1ro271Kdf7bkZ6EpjPLuDff1ywRy4gfaGSTubsM2FeYGDoT64ZwPm1cQUt"
        ],
        "slot": 242804011,
        "confirmation_status": "finalized",
        "err": {
          "Ok": null
        }
      }
    ]
  },
  "id": 1
}
```

#### getTipAccounts

Retrieves the tip accounts designated for tip payments for bundles. The tip accounts have remained constant and can also be found [here](#response-example-tips).

##### Request

| Parameter | Type | Description |
|-----------|------|-------------|
| None      | None | None        |

##### Request Example

```bash
curl https://mainnet.block-engine.jito.wtf/api/v1/bundles -X POST -H "Content-Type: application/json" -d '
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTipAccounts",
    "params": []
}
'
```

##### Response

| Field   | Type  | Description                        |
|---------|-------|------------------------------------|
| `result` | array | Tip accounts as a list of strings. |

(response-example-tips)=
##### Response Example

```json
{    
    "jsonrpc": "2.0",
    "result": [
        "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5",
        "HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe",
        "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY",
        "ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49",
        "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh",
        "ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt",
        "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL",
        "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT"
    ],
    "id": 1
}
```


#### getInflightBundleStatuses

Returns the status of submitted bundles within the last five minutes, allowing up to five bundle IDs per request. 

- **Failed**: Indicates that all regions have marked the bundle as failed, and it has not been forwarded.
- **Pending**: Indicates the bundle has not failed, landed, or been deemed invalid.
- **Landed**: Signifies the bundle has successfully landed on-chain, verified through RPC or the `bundles_landed` table.
- **Invalid**: Means the bundle is no longer in the system.

##### Request

| Parameter | Type          | Description                                                             |
|-----------|---------------|-------------------------------------------------------------------------|
| `params`  | array[string] | **REQUIRED**: An array of bundle IDs to confirm (up to a maximum of 5). |

##### Request Example

```bash
curl https://mainnet.block-engine.jito.wtf/api/v1/getInflightBundleStatuses -X POST -H "Content-Type: application/json" -d '
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getInflightBundleStatuses",
  "params": [
    [
      "b31e5fae4923f345218403ac1ab242b46a72d4f2a38d131f474255ae88f1ec9a",
      "e3c4d7933cf3210489b17307a14afbab2e4ae3c67c9e7157156f191f047aa6e8",
      "a7abecabd9a165bc73fd92c809da4dc25474e1227e61339f02b35ce91c9965e2",
      "e3934d2f81edbc161c2b8bb352523cc5f74d49e8d4db81b222c553de60a66514",
      "2cd515429ae99487dfac24b170248f6929e4fd849aa7957cccc1daf75f666b54" 
    ]
  ]
}
'
```

##### Response

| Field    | Type   | Description                                                            |
|----------|--------|------------------------------------------------------------------------|
| `null`   | null   | If the bundle(s) is not found.                                         |
| `object` | object | If the bundle is found, an array of objects with the following fields: |

###### Object Fields

- **bundle_id**: `string`  
  - Bundle ID

- **status**: `string`  
  - `Invalid`: Bundle ID not in our system (5 minute look back).
  - `Pending`: Not failed, not landed, not invalid.
  - `Failed`: All regions that have received the bundle have marked it as failed and it hasn't been forwarded.
  - `Landed`: Landed on-chain (determined using RPC or `bundles_landed` table).

- **landed_slot**: `u64`  
  - The slot this bundle landed in, otherwise `null` if it is `Invalid`.

##### Response Example

```json
{
  "jsonrpc": "2.0",
  "result": {
    "context": {
      "slot": 280999028
    },
    "value": [
      {
        "bundle_id": "b31e5fae4923f345218403ac1ab242b46a72d4f2a38d131f474255ae88f1ec9a",
        "status": "Invalid",
        "landed_slot": null
      },
      {
        "bundle_id": "e3c4d7933cf3210489b17307a14afbab2e4ae3c67c9e7157156f191f047aa6e8",
        "status": "Invalid",
        "landed_slot": null
      },
      {
        "bundle_id": "a7abecabd9a165bc73fd92c809da4dc25474e1227e61339f02b35ce91c9965e2",
        "status": "Invalid",
        "landed_slot": null
      },
      {
        "bundle_id": "e3934d2f81edbc161c2b8bb352523cc5f74d49e8d4db81b222c553de60a66514",
        "status": "Invalid",
        "landed_slot": null
      },
      {
        "bundle_id": "2cd515429ae99487dfac24b170248f6929e4fd849aa7957cccc1daf75f666b54",
        "status": "Invalid",
        "landed_slot": null
      }
    ]
  },
  "id": 1
}
```

## Getting Started

Welcome to the Jito MEV ecosystem! If you're looking to integrate Jito's advanced MEV solutions into your projects, we have a suite of developer tools designed to make your journey seamless, no matter your preferred language.

<div class="language-card">
    <div class="language-icon">
        <i class="fab fa-python"></i>
    </div>
    <div class="language-content">
        <h3>Python Developers</h3>
        <p>The <a href="https://github.com/jito-labs/jito-py-rpc">Jito Py JSON-RPC</a> library provides a robust SDK for interacting with Jito's Block Engine, allowing you to send transactions, bundles, and more directly from your Python applications.</p>
    </div>
</div>

<div class="language-card">
    <div class="language-icon">
        <i class="fab fa-js"></i>
    </div>
    <div class="language-content">
        <h3>JavaScript/TypeScript Developers</h3>
        <p>The <a href="https://github.com/jito-labs/jito-js-rpc">Jito JS JSON-RPC</a> library offers similar capabilities tailored for Node.js and browser environments, optimized for efficient MEV interactions.</p>
    </div>
</div>

<div class="language-card">
    <div class="language-icon">
        <i class="fab fa-rust" style="color: #14F195;"></i>
    </div>
    <div class="language-content">
        <h3>Rust Developers</h3>
        <p>Explore the <a href="https://github.com/jito-labs/jito-rust-rpc">Jito Rust JSON-RPC</a>, a performant SDK designed to leverage the power of Rust for interacting with Jito's infrastructure on Solana.</p>
    </div>
</div>

<div class="language-card">
    <div class="language-icon">
        <i class="fab fa-golang"></i>
    </div>
    <div class="language-content">
        <h3>Go Developers</h3>
        <p>The <a href="https://github.com/jito-labs/jito-go-rpc">Jito Go JSON-RPC</a> library provides a Go-based SDK that brings the same low-latency, high-performance MEV solutions to your Go applications.</p>
    </div>
</div>

### Key Endpoints Supported by These Libraries:
**Bundles**
- `get_inflight_bundle_statuses`: Retrieve the status of in-flight bundles.
- `get_bundle_statuses`: Fetch the statuses of submitted bundles.
- `get_tip_accounts`: Get accounts eligible for tips.
- `send_bundle`: Submit bundles to the Jito Block Engine.

**Transactions**
- `send_transaction`: Submit transactions with enhanced priority and speed.

These endpoints are specifically designed to optimize your MEV strategies, offering precise control over bundle and transaction management on Solana. Dive into the repos to get started, explore detailed documentation, and discover how you can integrate these powerful tools into your MEV workflows.

## Tips

**Best Practices for Tipping:**

1. Integrate tip instructions within your main transaction alongside core logic.
2. If transaction space is constrained, implement post-transaction checks or add assertions in a separate tipping transaction to verify expected states.
3. Exercise caution when sending tips as standalone transactions in bundles, as this may increase vulnerability to uncle bandit scenarios.

> ⚠️ **Warning**  
> When tipping make sure to not use Address Lookup Tables for the tip accounts. Tips do not prioritize transactions for validators that are not Jito-Solana leaders, so tipping in these cases will be ineffective and a waste of money

(tip-amount)=
### 🪙 Tip Amount

#### sendTransaction
When using `sendTransaction`, it is recommended to use a 70/30 split between priority fee and jito tip(e.g.):

```
    Priority Fee (70%): 0.7 SOL
    +
    Jito Tip (30%): 0.3 SOL
    ===========================
    Total Fee: 1.0 SOL
```

So, when using sendTransaction:

    You would allocate 0.7 SOL as the priority fee.
    And 0.3 SOL as the Jito tip.

#### sendBundle
When using `sendBundle`, only the Jito tip matters.

(get-tip-information)=
### 💸 Get Tip Information
#### REST API endpoint showing most recent tip amounts:<br>
```
curl https://bundles.jito.wtf/api/v1/bundles/tip_floor
```
Response:
```
[
  {
    "time": "2024-09-01T12:58:00Z",
    "landed_tips_25th_percentile": 6.001000000000001e-06,
    "landed_tips_50th_percentile": 1e-05,
    "landed_tips_75th_percentile": 3.6196500000000005e-05,
    "landed_tips_95th_percentile": 0.0014479055000000002,
    "landed_tips_99th_percentile": 0.010007999,
    "ema_landed_tips_50th_percentile": 9.836078125000002e-06
  }
]
```

#### WebSocket showing tip amounts:
```
wscat -c ws://bundles-api-rest.jito.wtf/api/v1/bundles/tip_stream
```

#### Tip Dashboard
To view dashboard please [click here](https://jito-labs.metabaseapp.com/public/dashboard/016d4d60-e168-4a8f-93c7-4cd5ec6c7c8d) .

## Rate Limits

### Default Limits
**Q: What are the defaults?**

5 requests per second per IP per region.

### Rate Limit Operation
**Q: How do they work?**

You no longer need an approved auth key for default sends.

### Exceeding Limits
**Q: What happens if the rate limit is exceeded?**

429 or rate limit error indicating what you hit.

### Authorization Issues
**Q: What happens if I see `The supplied pubkey is not authorized to generate a token`?**

This indicates that you're either using the auth-key parameter or your keypair variable is being set to check for this key unnecessarily. In most cases, you can simply use Null or None for these fields. Many of the new SDKs will have this built-in by default, so you won't need to specify it manually.

## Rate Limits Form

Please ensure to provide valid contact information so we can send you acknowledgment [submit form](https://forms.gle/8jZmKX1KZA71jXp38)


## Troubleshooting

### Priority Fee
**Q: How to know how much to set priority fee?**

Please see [Tip Amount for sendTransaction](#tip-amount)

### Tip Amount
**Q: How to know how much to set a tip?**

The minimum tips is 1000 lamports

### Bundle Landing
**Q: My bundle/transaction is not landing, how do I check?**

If this is your first time using bundles, please ensure you transaction are valid through `simulateTransaction`, and Jito-Solana RPC should support `simulateBundle` to verify bundles.

If you have the `bundleID`, you can look over [Jito explorer](https://explorer.jito.wtf/), otherwise you can see basic inflight knowledge **within the last 5 minutes** through `getInflightBundleStatuses`.

The minimum tip is 1000 lamports, but if you're targeting a highly competitive MEV opportunity, you'll need to be strategic with your tip. Consider adjusting your tip amount, based on the [current pricing](#get-tip-information) of tips in the system, and also take into account the latency to each component you're interacting with to maximize your chances of success.

### Failed Transactions
**Q: Why is my transaction/bundle failing, but lands on explorers?**

#### Uncled Blocks

As more users have been starting to send bundles through Jito's block engine, we think it would be important to highlight uncled blocks on Solana and why some of you may be seeing your bundles landing as transactions that may fail.

Solana has skipped slots, this is where a block is built by a leader and not accepted by the supermajority. These are known as uncled blocks. When this happens, any party that received these blocks may rebroadcast any of these transactions and get them landed/reverted on chain. It's important to note this has always been an issue on Solana and most other blockchains.

So in the case of bundles, imagine transactions from a bundle end up on an uncled block and some party rebroadcasts some or all of the bundle transactions. Those transactions will hit the normal banking stage which does not respect the bundle atomicity and reversion protection rules.

#### Mitigations

We're working through some solutions; however, given the complexity of the network and this problem, it may take some time to fully get there. In the meantime it's extremely important that:

1. You protect yourself from bundles being 'unbundled'. This means having pre/post account checks and other safeguards that'll protect you in the case your bundle is rebroadcasted.

2. Make sure you minimize your bundles from being leaked; if you send to Jito you are never going to be explicitly leaked by Jito. However, be aware that during uncled block situations you are exposed to this.

3. Always make sure your Jito tip transaction is in the same transaction that is running the MEV strategy; this way if the transaction fails, you don't pay the Jito tip:

   - Ideally, include your tip instruction in the same transaction as your main logic, along with appropriate post-transaction checks.
   - If space is limited in your main transaction, consider adding assertions in your tipping transaction to verify the expected state (e.g., slot check, balance check).
   - Be aware that sending tips as standalone transactions in bundles may increase exposure to uncle bandit situations.
