from sqlalchemy import Table, Column, Integer, Text

from app.database import metadata

# Define the table schema manually
campus_geofences = Table(
    "CampusGeofences",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
)

geolocations = Table(
    "Geolocations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("geofence_id", Integer),
    Column("latitude", Text),
    Column("longitude", Text),
)
