from rapidly_part.models import Deviation, Dimension
from rapidly_part.formatting import format_deviation_pair

def test_format_deviation_pair_symmetric():
    # +0.1 и -0.1 должны стать ±0,1
    upper = Deviation(0.1, '+')
    lower = Deviation(0.1, '-')
    assert format_deviation_pair(upper, lower) == "±0,1"

def test_format_deviation_pair_asymmetric():
    # +0.1 и -0.05 должны стать $m+0,1;-0,05$
    upper = Deviation(0.1, '+')
    lower = Deviation(0.05, '-')
    assert format_deviation_pair(upper, lower) == "$m+0,1;-0,05$"
