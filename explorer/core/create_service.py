from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet

from explorer.core.explorer import Explorer


def create_service(ethereum_api: str, token_address: str) -> Explorer:
    async_web3 = Web3(
        AsyncHTTPProvider(ethereum_api),
        modules={
            "eth": (AsyncEth,),
            "net": (AsyncNet,),
        },
        middlewares=[],
    )

    return Explorer(async_web3=async_web3, token_address=token_address)
