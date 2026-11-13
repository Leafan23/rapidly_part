from rapidly_part.models import Deviation

def test_deviation_str_plus():
    assert str(Deviation(0.1, '+')) == "+0,1"

def test_deviation_neg():
    assert (-Deviation(0.1, '-')).sign == '+'

def test_deviation_str_minus():
    assert str(Deviation(-0.1, '+')) == "-0,1"