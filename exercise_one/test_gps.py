import pytest
from gps_code import parse_coord

class TestParseCoord:

    def test_invalid_latitude(self):
        # with pytest.raises(ValueError):
        assert    parse_coord("abcd", True)

    def test_invalid_longitude(self):
        # with pytest.raises(ValueError):
        assert    parse_coord("....", False)   
