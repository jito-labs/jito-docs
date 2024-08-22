# API

## Transactions
  sendTransaction

Have more code examples for json-rpc sendTransaction
Link to APIs
Do we offer mev-protection here?

      Header Field: Include the API key in the x-jito-auth header.

        Example: x-jito-auth: <uuid>

    Query Parameter: Include the API key as a query parameter.

        Example: api/v1/bundles?uuid=<uuid>

## Bundles

Bundles are a list of up to 5 transactions that execute sequentially and atomically, ensuring an all-or-nothing outcome. Here’s what that means:

    Sequentially: Transactions in a bundle are guaranteed to execute in the order they are listed.

    Atomically: Bundles execute within the same slot(e.g. a bundle cannot cross slot boundaries). If the entire bundle executes successfully, all transactions are committed to the chain.

    All-or-Nothing: Bundles can only contain successful transactions. If any transaction in a bundle fails, none of the transactions in the bundle will be committed to the chain.

This guarantees that all transactions in a bundle are executed in sequence and either all succeed or none are executed.

For bundle-related methods, use the URL path /api/v1/bundles. Refer to the documentation to see the available JSON-RPC endpoints for bundles.

  sendBundle
  getBundleStatus
  getTipAccounts
  getInflightBundleStatuses
## Tips
  REST API endpoint showing most recent tip amounts: http://bundles-api-rest.jito.wtf/api/v1/bundles/tip_floor

  WebSocket showing tip amounts: ws://bundles-api-rest.jito.wtf/api/v1/bundles/tip_stream

## Rate limits
What are the defaults?
5 requests per second per IP per region

How do they work?
You no longer need an approved auth key for default sends

What happens if the rate limit is exceeded?
429 or rate limit error indicating what you hit

Put signup form here
Please ensure to provide valid contact information so we can send you a starter UUID

https://forms.gle/8jZmKX1KZA71jXp38
