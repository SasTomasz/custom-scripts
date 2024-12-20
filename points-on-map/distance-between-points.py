import json

# Load your JSON data
json_data = '''{
"distances": [[0.0, 301.6, 561.3, 1008.2, 1133.7, 27183.4, 27089.2, 27183.4], [287.5, 0.0, 517.3, 964.1, 1089.7, 27139.4, 27145.2, 27139.4], [561.3, 502.8, 0.0, 446.9, 572.4, 26622.1, 27419.1, 26622.1], [683.3, 624.7, 122.0, 0.0, 529.0, 26578.7, 27541.0, 26578.7], [1174.6, 1116.0, 613.3, 491.3, 0.0, 26666.5, 28032.3, 26666.5], [28772.7, 28714.2, 28211.4, 28089.4, 28288.3, 0.0, 15245.2, 0.0], [27247.0, 27317.2, 27576.9, 28023.8, 28149.3, 14852.2, 0.0, 14852.2], [28772.7, 28714.2, 28211.4, 28089.4, 28288.3, 0.0, 15245.2, 0.0]]
}'''

points_order = (5, 4, 3, 2, 1, 0, 6, 5)

# Convert the number to a string without thousands separator
# and replace the decimal point with a comma
def convert_number_to_string(number):
    number_str = f"{number:.2f}"
    number_formatted = number_str.replace(",", "") # Remove any existing commas
    return number_formatted.replace(".", ",")


def get_distance_between_points(matrix, point_a, point_b):
    return matrix[point_a][point_b]

def compute_distances(distance_matrix, l_points_order: tuple):
    for idx, point in enumerate(l_points_order):
        if idx == 0:
            continue
        previous_point_idx = points_order[idx - 1]
        current_point_idx = points_order[idx]
        distance = get_distance_between_points(distance_matrix, previous_point_idx, current_point_idx)
        print(convert_number_to_string(distance))


# Parse the JSON
data = json.loads(json_data)

# Access the distances matrix
distances = data["distances"]

compute_distances(distances, points_order)

