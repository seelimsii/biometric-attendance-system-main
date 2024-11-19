from typing import List

from app.geofencing.models import Geolocation


async def insert_geofence(cursor, name: str) -> int:
    insert_query = "INSERT INTO CampusGeofences (name) VALUES (?)"
    await cursor.execute(insert_query, (name,))
    await cursor.execute("SELECT @@IDENTITY")
    row = await cursor.fetchone()
    return row[0] if row else None


async def insert_geolocations(cursor, geofence_id: int, locations: List[Geolocation]):
    insert_query = """
    INSERT INTO Geolocations (geofence_id, latitude, longitude) 
    VALUES (?, ?, ?)
    """
    for location in locations:
        await cursor.execute(
            insert_query, (geofence_id, location.latitude, location.longitude)
        )


async def verify_geofence(cursor, geofence_id: int, expected_count: int) -> bool:
    verify_query = "SELECT COUNT(*) FROM Geolocations WHERE geofence_id = ?"
    await cursor.execute(verify_query, (geofence_id,))
    result = await cursor.fetchone()
    return result[0] == expected_count
