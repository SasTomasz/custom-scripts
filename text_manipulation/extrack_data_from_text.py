import re

def extract_unique_ids_from_file(filepath):
    # patter looking below lines without particular data and object number, then print every unique nmber
    # 2025-07-29 11:30:44 - Obiekt (25113) nie figuruje na liście obiektów.
    pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - Obiekt \((\d+)\) nie figuruje na liście obiektów\.')
    unique_ids = set()
    different_objects_number = 0

    with open(filepath, 'r', encoding='windows-1250') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                unique_ids.add(match.group(1))

    for obj_id in sorted(unique_ids, key=int):
        print(obj_id)
        different_objects_number += 1

    print(f"Total number of different object is {different_objects_number}")

# Example usage:
extract_unique_ids_from_file(r'D:\PROJEKTY\ICHI\Mapa ICHI\Przydatne narzędzia\cbar\Gps.log')
