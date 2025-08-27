#!/usr/bin/env python3
"""
Gas Price API Server for React Native App
=========================================

This Flask server provides a REST API that your React Native app can call
to get gas prices by postal code using the py-gasbuddy package.
"""

from flask import Flask, request, jsonify
import asyncio
import gasbuddy
import requests
import json
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Enable proxy fix for hosting services that use reverse proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def geocode_location(location: str, country_code: str = None) -> tuple[float, float] | None:
    """
    Convert location string to coordinates.
    Supports postal codes, city names, addresses for any country.

    Args:
        location: Location string (postal code, city, address)
        country_code: Optional 2-letter country code (e.g., 'CA', 'US', 'GB')

    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    # Clean up the location string
    location = location.strip()

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }

    # Add country code if specified
    if country_code:
        params["countrycodes"] = country_code.upper()

    headers = {"User-Agent": "GasBuddy-International-API/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except requests.RequestException as e:
        print(f"Geocoding error: {e}")
    except (ValueError, KeyError) as e:
        print(f"Data parsing error: {e}")

    return None


async def get_gas_prices_async(lat: float, lon: float, location: str, country: str = None):
    """
    Get gas prices using coordinates.
    Works internationally where GasBuddy data is available.
    """
    client = gasbuddy.GasBuddy()

    try:
        # Get nearby gas stations (limit to 10 for performance)
        nearby_prices = await client.price_lookup_service(lat=lat, lon=lon, limit=10)

        if nearby_prices and nearby_prices.get('results'):
            results = nearby_prices.get('results', [])
            stations = []

            for station in results:
                station_data = {
                    "station_id": station.get("station_id"),
                    "name": station.get("name", "Unknown Station"),
                    "prices": {},
                    "currency": station.get("currency", "USD"),
                    "distance": station.get("distance", None)
                }

                # Extract prices for each fuel type
                for fuel_type in ['regular_gas', 'midgrade_gas', 'premium_gas', 'diesel']:
                    fuel_data = station.get(fuel_type, {})
                    if fuel_data and fuel_data.get('price'):
                        # Convert cents to dollars (GasBuddy uses cents per liter)
                        price_per_liter = fuel_data.get('price', 0) / 100
                        station_data["prices"][fuel_type] = {
                            "price": price_per_liter,
                            "user": fuel_data.get('credit', 'Unknown'),
                            "last_updated": fuel_data.get('last_updated', None)
                        }

                if station_data["prices"]:
                    stations.append(station_data)

            return {
                "success": True,
                "location": location,
                "country": country or "Unknown",
                "coordinates": {"lat": lat, "lon": lon},
                "stations": stations,
                "count": len(stations),
                "source": "GasBuddy"
            }
        else:
            return {
                "success": False,
                "error": f"No gas stations found near {location}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching gas prices: {str(e)}"
        }


@app.route('/api/gas-prices', methods=['GET'])
async def get_gas_prices():
    """
    API endpoint for gas prices by location.
    Supports postal codes, city names, addresses for any country.
    """
    # Get parameters - support multiple location formats
    location = request.args.get('location')  # Generic location parameter
    postal_code = request.args.get('postal_code')  # Legacy support
    city = request.args.get('city')  # City name
    country_code = request.args.get('country')  # 2-letter country code
    lat = request.args.get('lat')  # Direct latitude
    lon = request.args.get('lon')  # Direct longitude

    # Determine the location string to use
    if location:
        location_string = location
    elif postal_code:
        location_string = postal_code
    elif city:
        location_string = city
    elif lat and lon:
        # Direct coordinates provided
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            # Use reverse geocoding to get location name
            location_string = f"{lat_float},{lon_float}"
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid latitude or longitude values"
            }), 400
    else:
        return jsonify({
            "success": False,
            "error": "Please provide one of: location, postal_code, city, or lat/lon coordinates"
        }), 400

    # Get coordinates
    if lat and lon:
        # Direct coordinates provided
        try:
            coordinates = (float(lat), float(lon))
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid latitude or longitude values"
            }), 400
    else:
        # Geocode the location
        coordinates = geocode_location(location_string, country_code)

    if not coordinates:
        return jsonify({
            "success": False,
            "error": f"Could not find coordinates for location: {location_string}"
        }), 404

    lat_coord, lon_coord = coordinates

    try:
        # Get gas prices asynchronously
        result = await get_gas_prices_async(lat_coord, lon_coord, location_string, country_code)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "GasBuddy International API",
        "version": "2.0",
        "supported_features": ["International geocoding", "Multiple location formats", "Real-time gas prices"]
    })


@app.route('/', methods=['GET'])
def home():
    """API documentation."""
    return jsonify({
        "name": "GasBuddy International API",
        "description": "Get gas prices by location for any country",
        "version": "2.0",
        "endpoints": {
            "/api/gas-prices?location=New York, NY": "Get gas prices by city/state",
            "/api/gas-prices?postal_code=L6Y4V3": "Get gas prices by postal code",
            "/api/gas-prices?city=London&country=GB": "Get gas prices by city and country",
            "/api/gas-prices?lat=40.7128&lon=-74.0060": "Get gas prices by coordinates",
            "/api/health": "Health check"
        },
        "supported_countries": ["US", "CA", "GB", "AU", "DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH"],
        "examples": [
            "GET /api/gas-prices?location=New York, NY",
            "GET /api/gas-prices?city=Toronto&country=CA",
            "GET /api/gas-prices?postal_code=90210",
            "GET /api/gas-prices?lat=51.5074&lon=-0.1278"
        ],
        "note": "GasBuddy data availability varies by country and region"
    })


# For local development testing only
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
