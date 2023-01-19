import asyncio
import csv
from typing import List
from web3 import Web3
from explorer.models.tx import Tx
from explorer.models.tx_type import TxType
from explorer.utils.to_long_address import to_long_address
from explorer.utils.to_normal_address import to_normal_address


class Explorer:
    def __init__(
        self,
        async_web3: Web3,
        token_address: str,
    ):
        self.async_web3 = async_web3
        self.token_address = Web3.toChecksumAddress(token_address)

    async def process(
        self,
        address: str,
        from_block: int = 0,
        tx_type: TxType = TxType.incoming,
        output_file: str = "",
    ):
        tx_list: List[Tx] = await self._fetch_all_logs(
            address=address, from_block=from_block, tx_type=tx_type
        )

        await self._write_csv(tx_list=tx_list, output_file=output_file)

    async def _bulk_process_logs(
        self, from_block: int, to_block: int, address: str, tx_type=TxType.incoming
    ):
        logs = await self._get_transfer_logs(
            from_block=from_block, to_block=to_block, address=address, tx_type=tx_type
        )
        result: List[Tx] = []

        for log in logs:
            tx = Tx(
                block_number=int(log["blockNumber"]),
                tx_hash=log["transactionHash"].hex(),
                tx_index=log["transactionIndex"],
                log_index=log["logIndex"],
                sender=to_normal_address(log["topics"][1].hex()),
                receiver=to_normal_address(log["topics"][2].hex()),
                value=str(Web3.toInt(hexstr=log["data"])),
            )
            result.append(tx)

        return result

    async def _fetch_all_logs(
        self, address: str, from_block: int = 0, tx_type: TxType = TxType.incoming
    ):
        current_block = await self.async_web3.eth.get_block("latest")
        start_block = from_block
        result: List[Tx] = []

        while start_block < current_block.number:
            end_block = start_block + 5000

            chunk = await self._bulk_process_logs(
                tx_type=tx_type,
                address=address,
                from_block=start_block,
                to_block=end_block,
            )

            result = [*result, *chunk]
            start_block = end_block + 1

        return result

    async def _get_transfer_logs(
        self,
        from_block: int,
        to_block: int,
        address: str,
        tx_type: TxType = TxType.incoming,
    ):
        if tx_type.value == TxType.outcoming.value:
            topics = [
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                to_long_address(address),
                None,
            ]
        else:
            topics = [
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                None,
                to_long_address(address),
            ]

        logs = await self.async_web3.eth.get_logs(
            {
                "fromBlock": from_block,
                "toBlock": to_block,
                "address": self.token_address,
                "topics": topics,
            }
        )

        return logs

    async def _write_csv(self, tx_list: List[Tx], output_file: str = ""):
        with open(output_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)
            # header
            writer.writerow(
                [
                    "Transaction hash",
                    "Block number",
                    "Transaction index",
                    "Log index",
                    "Sender",
                    "Receiver",
                    "Value",
                ]
            )

            for tx in tx_list:
                writer.writerow(
                    [
                        tx.tx_hash,
                        tx.block_number,
                        tx.tx_index,
                        tx.log_index,
                        tx.sender,
                        tx.receiver,
                        tx.value,
                    ]
                )

            await asyncio.sleep(0)
