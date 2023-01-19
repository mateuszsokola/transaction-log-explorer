from pydantic import BaseModel


class Tx(BaseModel):
    block_number: int
    tx_hash: str
    tx_index: int
    log_index: int
    sender: str
    receiver: str
    value: str
