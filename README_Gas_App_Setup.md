# 🌍 International Gas Price App Setup Guide

This guide shows you how to set up a React Native app where users can find gas prices anywhere in the world using the GasBuddy International API.

## 🏗️ Architecture Overview

```
React Native App (Frontend - Any Country)
          ↓ HTTP Requests
Python Flask API Server (Backend)
          ↓ py-gasbuddy
GasBuddy GraphQL API (Global Data Source)
```

**🌍 Now supports users from any country!**

## 📋 Prerequisites

- Python 3.10+ with pip
- Node.js and npm/yarn
- React Native development environment
- Flask (`pip install flask requests`)

## 🚀 Quick Start

### 1. Set Up Python Backend API

```bash
# Install required packages
pip install flask requests gasbuddy

# Run the API server
python gas_price_api.py
```

The API will be available at: `http://localhost:5000`

### 2. Test the API

```bash
# Test with different location formats:

# By city and country
curl "http://localhost:5000/api/gas-prices?city=New%20York&country=US"

# By postal code (works internationally)
curl "http://localhost:5000/api/gas-prices?postal_code=90210"

# By coordinates
curl "http://localhost:5000/api/gas-prices?lat=51.5074&lon=-0.1278"

# By full address
curl "http://localhost:5000/api/gas-prices?location=1600%20Pennsylvania%20Ave%2C%20Washington%20DC"

# Expected response:
{
  "success": true,
  "location": "New York",
  "country": "US",
  "coordinates": {"lat": 40.7128, "lon": -74.0060},
  "stations": [
    {
      "station_id": "1963",
      "name": "Shell",
      "currency": "USD",
      "prices": {
        "regular_gas": {"price": 3.49, "user": "gasuser123"},
        "midgrade_gas": {"price": 3.79, "user": "buddy456"}
      }
    }
  ],
  "count": 8,
  "source": "GasBuddy"
}
```

### 3. Set Up React Native App

```bash
# Create new React Native project
npx react-native init GasPriceApp
cd GasPriceApp

# Install dependencies
npm install @react-native-async-storage/async-storage
# For HTTP requests (built into React Native)
```

### 4. Add the GasPriceScreen Component

Copy `GasPriceScreen.js` to your React Native project's components folder and update your navigation.

### 5. Configure API Endpoint

Update the `API_BASE_URL` in `GasPriceScreen.js`:

```javascript
// For development (local computer)
const API_BASE_URL = 'http://10.0.2.2:5000';  // Android emulator
// OR
const API_BASE_URL = 'http://localhost:5000';   // iOS simulator

// For production, use your server URL:
// const API_BASE_URL = 'https://your-api-server.com';
```

## 📱 React Native Integration

### Basic Usage

```javascript
import GasPriceScreen from './components/GasPriceScreen';

// In your navigation
<Stack.Screen name="GasPrices" component={GasPriceScreen} />
```

### API Response Format

The API returns data in this format:

```javascript
{
  "success": true,
  "postal_code": "L6Y4V3",
  "coordinates": {"lat": 43.7315, "lon": -79.7624},
  "stations": [
    {
      "station_id": "1963",
      "prices": {
        "regular_gas": {"price": 1.379, "user": "gasuser123"},
        "midgrade_gas": {"price": 1.589, "user": "buddy456"},
        "premium_gas": {"price": 1.689, "user": "premium_user"},
        "diesel": {"price": 1.389, "user": "diesel_guy"}
      }
    }
  ],
  "count": 5
}
```

## 🔧 Backend Deployment Options

### Option 1: Local Development
```bash
python gas_price_api.py
# Access via http://localhost:5000
```

### Option 2: Heroku (Free)
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
# Your API will be at: https://your-app-name.herokuapp.com
```

### Option 3: DigitalOcean/VPS
```bash
# Install gunicorn for production
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 gas_price_api:app
```

## 📊 Features Included

✅ **Multiple Location Formats** - City names, postal codes, addresses, coordinates
✅ **International Support** - Works in any country with GasBuddy data
✅ **Real-time Gas Prices** - From global gas stations
✅ **Multiple Fuel Types** - Regular, Midgrade, Premium, Diesel
✅ **Global Stations** - Shell, Esso, BP, Petro-Canada, and more
✅ **Price Comparison** - Multiple stations for best deals
✅ **Error Handling** - Network errors, invalid locations
✅ **Loading States** - User feedback during API calls
✅ **Multi-Currency Support** - USD, CAD, EUR, GBP, and more
✅ **Location Intelligence** - Shows distance and station names

## 🎯 API Endpoints

### Gas Price Endpoints
- `GET /api/gas-prices?city=New%20York&country=US` - Get gas prices by city and country
- `GET /api/gas-prices?postal_code=90210` - Get gas prices by postal code (international)
- `GET /api/gas-prices?location=1600%20Pennsylvania%20Ave` - Get gas prices by address
- `GET /api/gas-prices?lat=40.7128&lon=-74.0060` - Get gas prices by coordinates
- `GET /api/gas-prices?city=London&country=GB` - Get gas prices by city and country code

### Utility Endpoints
- `GET /api/health` - Health check
- `GET /` - API documentation with examples

## 🔒 Security Considerations

- Consider adding API key authentication for production
- Implement rate limiting to prevent abuse
- Use HTTPS in production
- Validate postal codes server-side

## 🚨 Rate Limiting

GasBuddy has rate limiting. Consider:
- Client-side caching (AsyncStorage)
- Server-side caching (Redis/memcached)
- Rate limiting your API endpoints
- Error messages for rate limited requests

## 🐛 Troubleshooting

### Common Issues:

1. **"Could not find coordinates"**
   - Check postal code format (should be A1A1A1)
   - Verify it's a valid Canadian postal code

2. **Network errors**
   - Ensure Flask server is running
   - Check API_BASE_URL configuration
   - Verify firewall settings

3. **Rate limiting errors**
   - Wait a few minutes between requests
   - Implement caching in your app

## 📞 Support

The API uses:
- **py-gasbuddy**: Python wrapper for GasBuddy GraphQL API
- **OpenStreetMap Nominatim**: Free geocoding service
- **Flask**: Lightweight Python web framework

## 🎉 Success!

You now have a complete international React Native app that can:
- Accept location inputs from users worldwide
- Support multiple location formats (city, postal code, address, coordinates)
- Fetch real-time gas prices from any country
- Display them in a user-friendly interface with local currency
- Show station names and distances

The app works with global gas station data from GasBuddy including major brands like Shell, Esso, BP, Petro-Canada, and many more! 🌍⛽

### 🌐 Supported Countries
GasBuddy data is available in: **US, CA, GB, AU, DE, FR, IT, ES, NL, BE, AT, CH** and many more regions.

**Note:** Data availability varies by country and region. Some areas may have limited station coverage.
