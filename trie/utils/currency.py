def to_fixed(d, places=2):
    """Decimal to fixed a fixed value."""
    return d.quantize(places)
