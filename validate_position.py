# vehicle start and end position is a tuple (longitude, latitude)
def is_position_range_valid(lon_range, lat_range, position):
    lon, lat = position
    if (lon_range[0] <= lon <= lon_range[1]) and (lat_range[0] <= lat <= lat_range[1]):
        return True
    else:
        return False


def is_position_has_a_valid_coordinates(lon_range: tuple[float, float], lat_range: tuple[float, float],
                                        vehicle_start_pos: tuple[float, float], vehicle_end_pos: tuple[float, float]):
    return (is_position_range_valid(lon_range, lat_range, vehicle_start_pos)
            and is_position_range_valid(lon_range, lat_range, vehicle_end_pos))


is_position_valid = is_position_has_a_valid_coordinates((-180.0, 180.0), (-90.0, 90.0),
                                                        (54.23423424, 32.9879345), (32.23423423, 54.09802347))
print(is_position_valid)
