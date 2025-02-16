from django.core.management.base import BaseCommand, CommandError
from core.models import Trip
import gpxpy
import time
import requests
from geopy.distance import geodesic

class Command(BaseCommand):
    help = 'Simulate GPS for a truck based on a GPX route'

    def add_arguments(self, parser):
        # Define required positional arguments
        parser.add_argument('truck_id', type=str)
        parser.add_argument('gpx_file_path', type=str)

    def handle(self, *args, **options):
        truck_id = options['truck_id']
        gpx_file_path = options['gpx_file_path']
        
        try:
            # Get the active trip for this truck
            trip = Trip.objects.get(truck_id=truck_id, simulation_active=True)
            
            # Load the GPX file
            with open(gpx_file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)

            # Set simulation speed
            speed_kmh = 60
            speed_mps = speed_kmh * 1000 / 3600

            # Extract waypoints
            waypoints = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        waypoints.append((point.latitude, point.longitude))

            print(f"Found {len(waypoints)} waypoints")

            # Simulate movement
            for i in range(len(waypoints) - 1):
                trip.refresh_from_db()
                if not trip.simulation_active:
                    print("Simulation stopped - trip ended")
                    break

                start = waypoints[i]
                end = waypoints[i + 1]

                # Calculate distance and time
                distance_meters = geodesic(start, end).meters
                travel_time_seconds = distance_meters / speed_mps

                try:
                    # Send location update
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
                    response.raise_for_status()
                    
                    print(f"Waypoint {i+1}/{len(waypoints)-1}")
                    print(f"Location sent: {start}")
                    time.sleep(travel_time_seconds)

                except requests.RequestException as e:
                    print(f"Failed to send location update: {e}")
                    continue

        except Trip.DoesNotExist:
            raise CommandError(f"No active trip found for truck {truck_id}")
        except FileNotFoundError:
            raise CommandError(f"GPX file not found: {gpx_file_path}")
        except Exception as e:
            raise CommandError(f"Simulation error: {str(e)}")
        finally:
            print("Simulation ended")