# API Reference
## GET Method Endpoints
### `GET /mine` 
Mines new block using unverified transaction list. We first resolve conflicts to make sure we are mining on the longest valid chain. And we clear unverified transaction list for all the nodes. There should be at least 2 transactions in the unverified list to mine a block.
#### Response
```json
{
    "message" : "Mining complete. All transactions mined successfully"
}
```
```json
{
    "message" : "You need at least 2 transactions to mine a block"
}
```
#### Success status code : `200`
#### Error status code : `400`

### `GET /chain`
Shows the current blockchain as list of block_dict
#### Response
```json
{
    "length": 2,
    "chain": [
        {
            "num": 0,
            "timestamp": "2021-09-25 17:09:35.534832",
            "data": "Genesis",
            "prev_hash": null,
            "hash": "33d5a4981c2c038b10c9a26d79da8d6bb6e31ca83d87770f51a276639d65abc9",
            "nonce": 19200
        },
        {
            "num": 1,
            "timestamp": "2021-09-25 17:10:25.708142",
            "data": [
                {
                    "timestamp": "2021-09-25 17:10:07.629038",
                    "customer": "A",
                    "amount": 10,
                    "item": "item1",
                    "quantity": 1
                },
                {
                    "timestamp": "2021-09-25 17:10:18.241977",
                    "customer": "B",
                    "amount": 20,
                    "item": "item1",
                    "quantity": 2
                }
            ],
            "prev_hash": "33d5a4981c2c038b10c9a26d79da8d6bb6e31ca83d87770f51a276639d65abc9",
            "hash": "e8eb34062c2c975e2e7eb85f44ea7b2f382e90cd74c51a20e133e93bfce811ce",
            "nonce": 43260
        }
    ]
}
```
#### Success status code : `200`
#### Error status code : `400`

### `GET /transactions/unverified`
Shows all the unverifeid transactions added by any node on the network.
#### Response
```json
{
    "length": 2,
    "unverified_transactions": [
        {
            "timestamp": "2021-09-25 17:14:52.393185",
            "customer": "A",
            "amount": 10,
            "item": "item1",
            "quantity": 1
        },
        {
            "timestamp": "2021-09-25 17:15:09.789443",
            "customer": "B",
            "amount": 20,
            "item": "item1",
            "quantity": 2
        }
    ]
}
```
#### Success status code : `200`
#### Error status code : `400`

### `GET /transactions/unverified/clear`
Clears the unverified transactions.
#### Response
```json
{
    "message": "Unvarified transactions list cleared"
}
```
#### Success status code : `200`
#### Error status code : `400`

### `GET /nodes/resolve`
Resovle the conflicts between nodes by updating the current nodes chain with the longest valid chain.
#### Response
```json
{
    "message": "Our chain is longest valid chain"
}
```
```json
{
    "message": "Our chain got replaced with longest valid chain",
    "new_chain": [
        {
            "num": 0,
            "timestamp": "2021-09-25 17:31:56.008985",
            "data": "Genesis",
            "prev_hash": null,
            "hash": "2e8ab4bd24f99f2dcf63089103a50cea35279f187ec882cd0a3131b3bdad263d",
            "nonce": 19200
        },
        {
            "num": 1,
            "timestamp": "2021-09-25 17:33:55.689319",
            "data": [
                {
                    "timestamp": "2021-09-25 17:33:05.535029",
                    "customer": "A",
                    "amount": 10,
                    "item": "item1",
                    "quantity": 1
                },
                {
                    "timestamp": "2021-09-25 17:33:28.138076",
                    "customer": "B",
                    "amount": 20,
                    "item": "item1",
                    "quantity": 2
                }
            ],
            "prev_hash": "2e8ab4bd24f99f2dcf63089103a50cea35279f187ec882cd0a3131b3bdad263d",
            "hash": "758aaa4b4921187a8a6df6fcfe576b8d6d1fcfe27835cd9b9c8c335a8cd5b25d",
            "nonce": 43635
        }
    ]
}
```
#### Success status code : `200`
#### Error status code : `400`

## POST Method Endpoints
### `POST /nodes/register`
Register all the neighbourning nodes
#### Request Data
```json
{
    "nodes": ["http://localhost:5001"]
}
```
#### Response
```json
{
    "message": "New nodes have been added",
    "total_nodes": [
        "localhost:5001"
    ]
}
```
#### Success status code : `201`
#### Error status code : `400`

### `POST /transaction/add`
Add transaction to the unverified transaction list. We add the transaction to every other node using `POST /transaction/add_dict` request internally.
#### Request Data
```json
{
    "customer": "A",
    "amount": 10,
    "item": "item1",
    "quantity": 1
}
```
#### Response
```json
{
    "message": "Transaction is added to the unverified transactions list"
}
```
#### Success status code : `201`
#### Error status code : `400`

### `POST /transaction/add_dict`
Add transaction to the unverified transaction list. This endpoint is called internally for all nodes everytime we call `POST /transaction/add`
#### Request Data
```json
{
    "t_dict": {
        "customer": "A",
        "amount": 10,
        "item": "item1",
        "quantity": 1
    }
}
```
#### Response
```json
{
    "message": "Transaction is added to the unverified transactions list"
}
```
#### Success status code : `201`
#### Error status code : `400`
