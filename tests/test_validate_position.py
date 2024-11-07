import pytest

from validate_position import is_position_has_a_valid_coordinates as is_valid_position

# latitude between -90 and 90, longitude between -180 and 180
lon_range = (-180.0, 180.0)
lat_range = (-90.0, 90.0)

# (longitude, latitude)
valid_position = (53.123413, 34.34098)

upper_valid_limits_of_position = (180.0, 90.0)
lower_valid_limits_of_position = (-180.0, -90.0)

upper_invalid_lon_limits_of_position = (180.00000001, 90.0)
lower_invalid_lon_limits_of_position = (-180.000000001, -90.0)

upper_invalid_lat_limits_of_position = (180.0, 90.000000001)
lower_invalid_lat_limits_of_position = (-180.0, -90.00000000001)

lon_invalid_position = (192.2235, 34.2938742)
lat_invalid_position = (53.4353252, -91.34532345)

@pytest.mark.parametrize('valid_pos', [valid_position, upper_valid_limits_of_position, lower_valid_limits_of_position])
def test_position_in_range_is_valid(valid_pos):
    assert is_valid_position(lon_range, lat_range, valid_pos, valid_pos)

@pytest.mark.parametrize('lon_invalid_pos', [upper_invalid_lon_limits_of_position, lower_invalid_lon_limits_of_position, lon_invalid_position])
def test_position_with_invalid_longitude_return_false(lon_invalid_pos):
    assert not is_valid_position(lon_range, lat_range, lon_invalid_pos, lon_invalid_pos)

@pytest.mark.parametrize('lat_invalid_pos', [upper_invalid_lat_limits_of_position, lower_invalid_lat_limits_of_position, lat_invalid_position])
def test_position_with_invalid_latitude_return_false(lat_invalid_pos):
    assert not is_valid_position(lon_range, lat_range, lat_invalid_pos, lat_invalid_pos)