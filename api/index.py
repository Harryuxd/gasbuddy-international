#!/usr/bin/env python3
"""
GasBuddy International API for Vercel
======================================

This Flask server provides a REST API that can be called from any application
to get gas prices by location for any country.
"""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)


def geocode_location(location: str, country_code: str = None) -> tuple[float, float] | None:
    """
    Convert location string to coordinates.
    Currently returns mock coordinates for testing.
    Real geocoding will be added once deployment is stable.
    """
    # For now, return mock coordinates based on location type
    # This will be replaced with real geocoding later

    if "toronto" in location.lower() or "l6y4v3" in location.lower():
        return (43.6532, -79.3832)  # Toronto coordinates
    elif "new york" in location.lower() or "90210" in location.lower():
        return (40.7128, -74.0060)  # New York coordinates
    elif "london" in location.lower():
        return (51.5074, -0.1278)   # London coordinates
    else:
        return (40.7128, -74.0060)  # Default to New York


def get_gas_prices(location: str, country: str = None):
    """
    Get gas prices - currently returns mock data for testing.
    Will be replaced with real GasBuddy integration once Vercel deployment works.
    """

    # Mock data for testing - replace with real API calls later
    mock_data = {
        "success": True,
        "location": location,
        "country": country or "Unknown",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},  # Default NYC coordinates
        "stations": [
            {
                "station_id": "12345",
                "name": "Shell",
                "currency": "USD",
                "prices": {
                    "regular_gas": {
                        "price": 3.49,
                        "user": "test_user",
                        "last_updated": "2025-08-27T19:25:21.000Z"
                    },
                    "premium_gas": {
                        "price": 3.79,
                        "user": "test_user",
                        "last_updated": "2025-08-27T19:25:21.000Z"
                    }
                }
            },
            {
                "station_id": "67890",
                "name": "BP",
                "currency": "USD",
                "prices": {
                    "regular_gas": {
                        "price": 3.45,
                        "user": "another_user",
                        "last_updated": "2025-08-27T19:20:15.000Z"
                    }
                }
            }
        ],
        "count": 2,
        "source": "Mock Data (Testing)",
        "note": "This is mock data for testing Vercel deployment. Real GasBuddy integration will be added once deployment works."
    }

    return mock_data


@app.route('/api/gas-prices', methods=['GET'])
def gas_prices_endpoint():
    """
    API endpoint for gas prices by location.
    Supports postal codes, city names, addresses for any country.
    Currently returns mock data for testing Vercel deployment.
    """
    # Get parameters - support multiple location formats
    location = request.args.get('location')  # Generic location parameter
    postal_code = request.args.get('postal_code')  # Legacy support
    city = request.args.get('city')  # City name
    country_code = request.args.get('country')  # 2-letter country code

    # Determine the location string to use
    if location:
        location_string = location
    elif postal_code:
        location_string = postal_code
    elif city:
        location_string = city
    else:
        return jsonify({
            "success": False,
            "error": "Please provide one of: location, postal_code, or city"
        }), 400

    try:
        # Get coordinates (mock for now)
        coordinates = geocode_location(location_string, country_code)

        if not coordinates:
            return jsonify({
                "success": False,
                "error": f"Could not find coordinates for location: {location_string}"
            }), 404

        # Get gas prices (currently returns mock data)
        result = get_gas_prices(location_string, country_code)
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
        "platform": "Vercel",
        "supported_features": ["Multiple location formats", "Mock data for testing"],
        "note": "Currently using mock data for testing. Real GasBuddy integration will be added once deployment is stable."
    })


@app.route('/', methods=['GET'])
def home():
    """API documentation."""
    return jsonify({
        "name": "GasBuddy International API",
        "description": "Get gas prices by location for any country",
        "version": "2.0",
        "platform": "Vercel",
        "status": "Testing Mode",
        "endpoints": {
            "/api/gas-prices?city=New%20York&country=US": "Get gas prices by city and country",
            "/api/gas-prices?postal_code=L6Y4V3": "Get gas prices by postal code (international)",
            "/api/gas-prices?location=Toronto": "Get gas prices by city name",
            "/api/health": "Health check"
        },
        "examples": [
            "GET /api/gas-prices?city=New%20York&country=US",
            "GET /api/gas-prices?postal_code=L6Y4V3",
            "GET /api/gas-prices?location=Toronto"
        ],
        "current_status": "Mock Data Mode",
        "note": "Currently returning mock data for testing. Real GasBuddy integration will be added once Vercel deployment is stable."
    })


# Vercel handler
def handler(event, context):
    """Vercel serverless function handler."""
    return app(event, context)


if __name__ == '__main__':
    # For local development
    port = int(os.getenv('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
