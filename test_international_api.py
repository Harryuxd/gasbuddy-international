#!/usr/bin/env python3
"""
Test script for the International GasBuddy API
Tests various location formats and international functionality
"""

import requests
import json

def test_api_endpoint(base_url="http://localhost:5000"):
    """Test the API with various international locations"""

    test_cases = [
        {
            "name": "New York City (City)",
            "params": {"city": "New York", "country": "US"}
        },
        {
            "name": "London (City)",
            "params": {"city": "London", "country": "GB"}
        },
        {
            "name": "Toronto (City)",
            "params": {"city": "Toronto", "country": "CA"}
        },
        {
            "name": "US Postal Code",
            "params": {"postal_code": "90210"}
        },
        {
            "name": "Canadian Postal Code",
            "params": {"postal_code": "L6Y4V3"}
        },
        {
            "name": "Coordinates (London)",
            "params": {"lat": "51.5074", "lon": "-0.1278"}
        },
        {
            "name": "Full Address",
            "params": {"location": "1600 Pennsylvania Avenue, Washington DC"}
        }
    ]

    print("🌍 Testing International GasBuddy API")
    print("=" * 50)

    for test_case in test_cases:
        print(f"\n📍 Testing: {test_case['name']}")
        print(f"   Parameters: {test_case['params']}")

        try:
            response = requests.get(f"{base_url}/api/gas-prices", params=test_case['params'], timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ Success! Found {data.get('count', 0)} stations")
                    print(f"   📊 Location: {data.get('location', 'Unknown')}")
                    print(f"   🌎 Country: {data.get('country', 'Unknown')}")
                    if data.get('stations'):
                        station = data['stations'][0]
                        print(f"   ⛽ First station: {station.get('name', 'Unknown')}")
                        print(f"   💰 Currency: {station.get('currency', 'Unknown')}")
                else:
                    print(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")

        except requests.RequestException as e:
            print(f"   ❌ Network Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected Error: {e}")

def test_health_endpoint(base_url="http://localhost:5000"):
    """Test the health endpoint"""
    print("
🏥 Testing Health Endpoint"    print("-" * 30)

    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'Unknown')}")
            print(f"   📝 Service: {data.get('service', 'Unknown')}")
            print(f"   🔢 Version: {data.get('version', 'Unknown')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_documentation_endpoint(base_url="http://localhost:5000"):
    """Test the documentation endpoint"""
    print("
📚 Testing API Documentation"    print("-" * 35)

    try:
        response = requests.get(base_url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Name: {data.get('name', 'Unknown')}")
            print(f"   🔢 Version: {data.get('version', 'Unknown')}")
            print(f"   🌍 Description: {data.get('description', 'Unknown')}")
            print(f"   📍 Supported Countries: {', '.join(data.get('supported_countries', [])[:5])}...")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    import sys

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"

    print(f"🔗 Testing API at: {base_url}")

    test_health_endpoint(base_url)
    test_documentation_endpoint(base_url)
    test_api_endpoint(base_url)

    print("
🎉 Testing complete!"    print("\n💡 Note: Some locations may not have GasBuddy data available")
    print("   GasBuddy coverage varies by country and region")
