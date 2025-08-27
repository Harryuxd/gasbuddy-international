import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Alert,
  ActivityIndicator
} from 'react-native';

const GasPriceScreen = () => {
  const [location, setLocation] = useState('');
  const [country, setCountry] = useState('');
  const [gasPrices, setGasPrices] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [locationType, setLocationType] = useState('city'); // 'city', 'postal', 'coordinates'

  // Replace with your actual API URL
  const API_BASE_URL = 'http://your-server-ip:5000';

  const formatPostalCode = (text) => {
    // Auto-format Canadian postal codes (e.g., L6Y4V3 -> L6Y 4V3)
    const cleaned = text.replace(/\s/g, '').toUpperCase();
    if (cleaned.length >= 3) {
      return `${cleaned.slice(0, 3)} ${cleaned.slice(3, 6)}`;
    }
    return cleaned;
  };

  const fetchGasPrices = async () => {
    if (!location.trim()) {
      Alert.alert('Error', 'Please enter a location');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let url = `${API_BASE_URL}/api/gas-prices?`;

      if (locationType === 'postal') {
        url += `postal_code=${encodeURIComponent(location)}`;
      } else if (locationType === 'city') {
        url += `city=${encodeURIComponent(location)}`;
        if (country) {
          url += `&country=${encodeURIComponent(country)}`;
        }
      } else {
        url += `location=${encodeURIComponent(location)}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      if (data.success) {
        setGasPrices(data);
      } else {
        setError(data.error || 'Failed to fetch gas prices');
      }
    } catch (err) {
      setError('Network error. Please check your connection.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return `$${price.toFixed(3)}`;
  };

  const getFuelTypeName = (fuelType) => {
    const names = {
      'regular_gas': 'Regular',
      'midgrade_gas': 'Midgrade',
      'premium_gas': 'Premium',
      'diesel': 'Diesel'
    };
    return names[fuelType] || fuelType;
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>⛽ International Gas Prices</Text>
      <Text style={styles.subtitle}>Find gas prices anywhere in the world</Text>

      <View style={styles.inputContainer}>
        <Text style={styles.label}>Location Type:</Text>
        <View style={styles.locationTypeContainer}>
          {['city', 'postal', 'coordinates'].map((type) => (
            <TouchableOpacity
              key={type}
              style={[styles.typeButton, locationType === type && styles.typeButtonActive]}
              onPress={() => setLocationType(type)}
            >
              <Text style={[styles.typeButtonText, locationType === type && styles.typeButtonTextActive]}>
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>
          {locationType === 'city' ? 'City Name:' :
           locationType === 'postal' ? 'Postal Code:' : 'Location/Address:'}
        </Text>
        <TextInput
          style={styles.input}
          value={location}
          onChangeText={setLocation}
          placeholder={
            locationType === 'city' ? 'e.g., New York, NY' :
            locationType === 'postal' ? 'e.g., L6Y 4V3 or 90210' : 'e.g., 1600 Pennsylvania Ave, Washington DC'
          }
          autoCapitalize="words"
        />

        {locationType === 'city' && (
          <>
            <Text style={styles.label}>Country Code (Optional):</Text>
            <TextInput
              style={styles.input}
              value={country}
              onChangeText={setCountry}
              placeholder="e.g., US, CA, GB, AU"
              maxLength={2}
              autoCapitalize="characters"
            />
          </>
        )}

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={fetchGasPrices}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>🔍 Find Gas Prices</Text>
          )}
        </TouchableOpacity>
      </View>

      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>❌ {error}</Text>
        </View>
      )}

      {gasPrices && gasPrices.success && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>
            ⛽ Gas Prices for {gasPrices.location}
          </Text>
          <Text style={styles.resultsSubtitle}>
            Found {gasPrices.count} gas stations in {gasPrices.country}
          </Text>
          <Text style={styles.sourceText}>
            Data source: {gasPrices.source}
          </Text>

          {gasPrices.stations.map((station, index) => (
            <View key={station.station_id || index} style={styles.stationCard}>
              <Text style={styles.stationTitle}>
                {station.name || `Station #${index + 1}`}
              </Text>
              <Text style={styles.stationId}>
                ID: {station.station_id}
                {station.distance && ` • ${station.distance}km away`}
              </Text>

              {Object.entries(station.prices).map(([fuelType, fuelData]) => (
                <View key={fuelType} style={styles.priceRow}>
                  <Text style={styles.fuelType}>
                    {getFuelTypeName(fuelType)}:
                  </Text>
                  <Text style={styles.price}>
                    {formatPrice(fuelData.price)}/{station.currency === 'USD' ? 'gal' : 'L'}
                  </Text>
                  <Text style={styles.user}>
                    by {fuelData.user}
                  </Text>
                </View>
              ))}
            </View>
          ))}

          <Text style={styles.note}>
            💡 Prices shown in {gasPrices.stations[0]?.currency || 'local currency'} per {gasPrices.stations[0]?.currency === 'USD' ? 'gallon' : 'liter'}
          </Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#2c3e50',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
    color: '#7f8c8d',
  },
  inputContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#2c3e50',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 15,
    backgroundColor: '#f9f9f9',
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#bdc3c7',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  errorContainer: {
    backgroundColor: '#fee',
    padding: 15,
    borderRadius: 8,
    marginBottom: 20,
    borderLeftWidth: 4,
    borderLeftColor: '#e74c3c',
  },
  errorText: {
    color: '#e74c3c',
    fontSize: 14,
  },
  resultsContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#2c3e50',
  },
  resultsSubtitle: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 20,
  },
  stationCard: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  stationTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  stationId: {
    fontSize: 12,
    color: '#7f8c8d',
    marginBottom: 10,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 5,
  },
  fuelType: {
    fontSize: 14,
    color: '#2c3e50',
    flex: 2,
  },
  price: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#27ae60',
    flex: 1,
    textAlign: 'center',
  },
  user: {
    fontSize: 12,
    color: '#7f8c8d',
    flex: 2,
    textAlign: 'right',
  },
  note: {
    fontSize: 12,
    color: '#7f8c8d',
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: 15,
  },
  locationTypeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  typeButton: {
    flex: 1,
    padding: 10,
    marginHorizontal: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
    alignItems: 'center',
  },
  typeButtonActive: {
    backgroundColor: '#3498db',
    borderColor: '#3498db',
  },
  typeButtonText: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  typeButtonTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
  sourceText: {
    fontSize: 12,
    color: '#7f8c8d',
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: 10,
  },
});

export default GasPriceScreen;
