import gpxpy
import time
import requests
from geopy.distance import geodesic
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Simulate GPS for a truck based on a GPX route'

    def add_arguments(self, parser):
        parser.add_argument('truck_id', type=str, help='Truck ID')
        parser.add_argument('gpx_file_path', type=str, help='Path to the GPX file')

    def handle(self, *args, **kwargs):
        truck_id = kwargs['truck_id']
        gpx_file_path = kwargs['gpx_file_path']

        try:
            # Load the GPX file
            with open(gpx_file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

            # Set the simulation speed (e.g., 60 km/h)
            speed_kmh = 60  # Change this for different speeds
            speed_mps = speed_kmh * 1000 / 3600  # Convert to meters per second

            # Extract all waypoints from the GPX file
            waypoints = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        waypoints.append((point.latitude, point.longitude))

            print(f"Found {len(waypoints)} waypoints")

            # Simulate movement
            for i in range(len(waypoints) - 1):
                start = waypoints[i]
                end = waypoints[i + 1]

                # Calculate distance between waypoints
                distance_meters = geodesic(start, end).meters
                travel_time_seconds = distance_meters / speed_mps

                # Send location update to Django backend
                try:
                    response = requests.post(
                        f"http://127.0.0.1:8000/update_location/{truck_id}/",
                        json={
                            "latitude": float(start[0]),
                            "longitude": float(start[1])
                        },
                        headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }
                    )

                    print(f"Waypoint {i+1}/{len(waypoints)-1}")
                    print(f"Sent location: {start}")
                    print(f"Distance to next point: {distance_meters:.2f}m")
                    print(f"Travel time: {travel_time_seconds:.2f}s")
                    print(f"Response status: {response.status_code}")
                    print(f"Response content: {response.text}")
                    print("-" * 50)

                    # Wait before sending next update
                    time.sleep(travel_time_seconds)

                except requests.exceptions.RequestException as e:
                    print(f"Failed to send location update: {e}")
                    continue

        except FileNotFoundError:
            print(f"Error: GPX file not found at {gpx_file_path}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to Django server at http://127.0.0.1:8000")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            print("Simulation ended")