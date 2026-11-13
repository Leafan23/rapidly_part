
def format_number(value: float, max_decimals: int = 3) -> str:
    """100.5 -> '100,5'; 100.0 -> '100'."""
    s = str(round(value, max_decimals)).replace(".", ",")
    if s.endswith(",0"):
        s = s[:-2]
    return s

