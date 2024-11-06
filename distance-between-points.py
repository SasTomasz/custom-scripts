import json

# Load your JSON data
json_data = '''{
    "distances": [[0.0, 301.6, 561.3, 1008.2, 1133.7, 26958.9, 31679.0, 26958.9], [287.5, 0.0, 517.3, 964.2, 1089.7, 26914.9, 31735.1, 26914.9], [561.3, 502.8, 0.0, 446.9, 572.4, 26397.6, 32008.9, 26397.6], [683.3, 624.7, 122.0, 0.0, 529.0, 26354.2, 32130.9, 26354.2], [1174.6, 1116.0, 613.3, 491.3, 0.0, 26442.0, 32622.2, 26442.0], [28749.7, 28691.1, 28188.3, 28066.4, 28265.2, 0.0, 23645.3, 0.0], [32916.1, 32986.3, 33246.1, 33692.9, 33818.5, 24263.6, 0.0, 24263.6], [28749.7, 28691.1, 28188.3, 28066.4, 28265.2, 0.0, 23645.3, 0.0]]
}'''

# Parse the JSON
data = json.loads(json_data)

# Access the distances matrix
distances = data["distances"]

# Get the distance between the first and second point
distance_first_to_second = distances[1][0]

print(f"Distance between the first and second point: {distance_first_to_second:.2f} meters")
