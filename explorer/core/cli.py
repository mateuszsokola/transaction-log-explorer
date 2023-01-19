import asyncio
import typer

from asyncio import CancelledError
from explorer.core.create_service import create_service
from explorer.models.tx_type import TxType


main_app = typer.Typer()


@main_app.command()
def main(
    ethereum_api: str = typer.Option(..., help="Ethereum API URL"),
    token_address: str = typer.Option(..., help="Token smart contract address"),
    wallet_address: str = typer.Option(..., help="Wallet address"),
    from_block: int = typer.Option(0, help="Starting block"),
):
    async def main():
        main_service = create_service(
            ethereum_api=ethereum_api, token_address=token_address
        )
        try:
            await asyncio.gather(
                main_service.process(
                    address=wallet_address,
                    from_block=from_block,
                    tx_type=TxType.incoming,
                    output_file="./incoming.csv",
                ),
                main_service.process(
                    address=wallet_address,
                    from_block=from_block,
                    tx_type=TxType.outcoming,
                    output_file="./outcoming.csv",
                ),
            )
            print("Completed!")
        except CancelledError:
            pass
        except Exception as e:
            print("Something went wrong", e)

    asyncio.run(main())
