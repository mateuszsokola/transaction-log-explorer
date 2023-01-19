from enum import Enum


class TxType(str, Enum):
    incoming = "incoming"
    outcoming = "outcoming"
