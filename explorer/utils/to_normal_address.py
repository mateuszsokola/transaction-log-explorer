def to_normal_address(address: str):
    address_without_0x = address[len("0x000000000000000000000000") :]
    return f"0x{address_without_0x.lower()}"
