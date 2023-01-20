# Transaction Log Explorer

Creates a list of all transactions related to token and wallet. This script was used on Ethereum only but it can support all EVM blockchains as well.

# Example outputs

* [Incoming DAI transactions to wallet 0xd5e73f9199E67b6Ff8DFACE1767A1BDAdf1A7242](./examples/incoming.csv)
* [Outgoing DAI transactions to wallet 0xd5e73f9199E67b6Ff8DFACE1767A1BDAdf1A7242](./examples/outgoing.csv)

## Dependencies
* python3 version 3.10.

## Quickstart

Install dependencies

```bash
pip install --upgrade pip setuptools -r requirements.txt
```

> If you run into problems during installation, you might have a broken environment. Try setting up a clean environment.

To run the script you need to provide parameters such as Ethereum API, token address, wallet address and starting block (optional). Your command should like that one:

```
python -m explorer --ethereum-api $$ETHEREUM_API_URL$$ --token-address 0x6B175474E89094C44Da98b954EedeAC495271d0F --wallet-address 0xd5e73f9199E67b6Ff8DFACE1767A1BDAdf1A7242 --from-block 13352962
```

You need to provide Ethereum API. If you don’t have your own node, you get a free API url with key on one of those websites:

* https://www.infura.io/
* https://moralis.io/
* https://www.quicknode.com/

## Need help?

Feel free to [start a discussion](https://github.com/mateuszsokola/token-transaction-log-explorer/discussions) or [ping me on Twitter](https://twitter.com/msokola).