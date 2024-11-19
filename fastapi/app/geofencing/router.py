from http import HTTPStatus

from pyodbc import Row
from fastapi import APIRouter, HTTPException
from loguru import logger
from shapely import Polygon, Point

from app.database import pool
from app.geofencing.common import GeolocationRequestModel, GeoFenceModelRequestModel
from app.geofencing.locations import locations
from app.geofencing.models import Geofence, Geolocation
from app.geofencing.process import insert_geofence, insert_geolocations, verify_geofence


router = APIRouter()


@router.post("/validate-location")
async def send_current_location(model: GeolocationRequestModel):
    logger.info(f"Received location: {model.model_dump()}")
    point = Point(model.latitude, model.longitude)

    location_name = "Ambedkar Dseu Shakarpur Campus - 1"
    location_shape = next(
        (
            location["shape"]
            for location in locations
            if location["name"] == location_name
        )
    )

    ploygon = Polygon(location_shape)
    if ploygon.contains(point):
        logger.info(f"Location is within the {location_name} geofence")
        return {"message": f"Location is within the {location_name} geofence"}

    logger.info(f"Location is outside the {location_name} geofence")
    return {"message": f"Location is outside the {location_name} geofence"}


@router.post("/add-location")
async def add_location(geofence: GeoFenceModelRequestModel):
    try:
        logger.info(f"Received location: {geofence.model_dump()}")

        conn = await pool.acquire()
        cursor = await conn.cursor()

        try:
            geofence_id = await insert_geofence(cursor, geofence.name)
            if not geofence_id:
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Geofence ID not found even after insertion",
                )

            await insert_geolocations(cursor, geofence_id, geofence.shape)
            await conn.commit()

            if not await verify_geofence(cursor, geofence_id, len(geofence.shape)):
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Mismatch between expected and inserted geolocations",
                )

            logger.info(f"Geofence added successfully with ID: {geofence_id}")
            return {"message": "Geofence added successfully"}

        finally:
            await cursor.close()

    except Exception as e:
        logger.exception("Error while adding geofence")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get-locations")
async def get_locations():
    try:
        conn = await pool.acquire()
        cursor = await conn.cursor()

        try:
            await cursor.execute(
                """
                SELECT cg.name AS name, 
                    g.latitude AS latitude, 
                    g.longitude AS longitude
                FROM CampusGeofences cg
                LEFT JOIN Geolocations g ON cg.id = g.geofence_id
            """
            )
            records = []
            rows = await cursor.fetchall()
            for row in rows:
                if not len(row) == 3:
                    raise HTTPException(
                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                        detail="Invalid number of columns in the result set",
                    )

                geofence_name, latitude, longitude = row
                shape = [Geolocation(latitude=latitude, longitude=longitude)]
                records.append({"name": geofence_name, "shape": shape})
            return {
                "message": "Locations fetched successfully",
                "content": records,
            }
        finally:
            await cursor.close()

    except Exception as e:
        logger.exception("Error while fetching locations")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
