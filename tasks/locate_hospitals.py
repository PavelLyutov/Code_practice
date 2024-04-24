import math
from itertools import combinations
import matplotlib.pyplot as plt


city_coordinates_test = [(400, 150), (350, 123), (432, 322), (400, 400), (500, 500),
                         (600, 600), (700, 700), (800, 800), (999, 998), (999, 999)]


def validate_city_data(city_coordinates):
    # Check if there are exactly 10 cities
    if len(city_coordinates) != 10:
        raise ValueError("There must be exactly 10 cities.")

    unique_coordinates = set(city_coordinates)
    if len(unique_coordinates) != len(city_coordinates):
        raise ValueError("City coordinates must be unique.")

    for x, y in city_coordinates:
        if not (0 <= x <= 999 and 0 <= y <= 999):
            raise ValueError("Coordinates must be within the range (0,0) and (999,999).")


# Function that calculates the distance between two cities
def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Function that makes the main logic
def place_hospitals(city_coordinates):
    n = len(city_coordinates)

    # Step 1: Calculate all pairwise distances in one go
    city_distances = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        distance = calculate_distance(city_coordinates[i], city_coordinates[j])
        city_distances[i][j] = distance
        city_distances[j][i] = distance  # Symmetric distances

    # Step 2: Calculate the total distance from each city to all other cities
    city_total_distances = [
        sum(city_distances[i]) for i in range(n)
    ]

    # Step 3: Find the two cities with the largest total distances
    hospital_indices = sorted(
        range(n), key=lambda i: city_total_distances[i], reverse=False
    )[:2]

    # Step 4: Return the coordinates of these two cities
    hospital_coordinates = [city_coordinates[i] for i in hospital_indices]

    return hospital_coordinates


def plot_cities_with_hospitals(city_coordinates, hospital_coordinates):
    """
    Create a scatter plot of city coordinates with specified hospitals.
     Args:
    - city_coordinates (list of tuples): Coordinates of cities.
    - hospital_coordinates (list of tuples): Coordinates of hospitals.
    """


    # Create a scatter plot with different markers for cities and hospitals
    plt.figure(figsize=(6, 6))

    # Plot the city coordinates (as blue dots)
    plt.scatter([x for x, y in city_coordinates], [y for x, y in city_coordinates], color='blue', label='Cities')

    # Plot the hospital coordinates (as red stars)
    plt.scatter([x for x, y in hospital_coordinates], [y for x, y in hospital_coordinates], color='red', marker='*', s=100,
                label='Hospitals')

    # Label the hospitals for easy identification
    for i, (x, y) in enumerate(hospital_coordinates):
        plt.text(x, y, f"Hospital {i + 1}", fontsize=8, ha='center', va='bottom', color='red')

    # Set plot titles and labels
    plt.title("City Coordinates with Hospitals")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)

    # Set axis limits based on the coordinate range
    plt.xlim(min(city_coordinates, key=lambda c: c[0])[0] - 50, max(city_coordinates, key=lambda c: c[0])[0] + 50)
    plt.ylim(min(city_coordinates, key=lambda c: c[1])[1] - 50, max(city_coordinates, key=lambda c: c[1])[1] + 50)

    # Add a legend to identify cities and hospitals
    plt.legend()
    plt.show()


if __name__ == '__main__':
    validate_city_data(city_coordinates_test)
    hospitals = place_hospitals(city_coordinates_test)
    print("Hospital coordinates:", hospitals)
    plot_cities_with_hospitals(city_coordinates_test,hospitals)
