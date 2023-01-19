def to_long_address(address: str):
    address_without_0x = address[2:]
    return f"0x000000000000000000000000{address_without_0x.lower()}"
