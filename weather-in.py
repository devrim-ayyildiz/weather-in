"""Weather in - Get current weather information for any city.

This script fetches and displays current weather information for a specified city
using the OpenWeatherMap API. It requires an API key stored in ~/.apikey

Usage:
    python weather-in.py <city name>
    python weather-in.py --help

Examples:
    python weather-in.py London
    python weather-in.py New York
    python weather-in.py "Los Angeles"

Output includes:
    - City name and country
    - Geographic coordinates (latitude/longitude)
    - Current temperature and feels like temperature
    - Humidity percentage
    - Wind speed
    - Weather conditions and description

Dependencies:
    - requests: For making HTTP requests to OpenWeatherMap API
"""

import sys
import requests
from pathlib import Path

API_KEY_FILE = Path.home() / ".apikey"
GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall"


def load_api_key(api_key_file=API_KEY_FILE):
    """Load API key from file.

    Args:
        api_key_file: Path to the API key file

    Returns:
        str: The API key

    Raises:
        FileNotFoundError: If API key file doesn't exist
        ValueError: If API key file is empty
    """
    if not api_key_file.exists():
        raise FileNotFoundError(f"API key file not found: {api_key_file}")

    api_key = api_key_file.read_text().strip()

    if not api_key:
        raise ValueError("API key file is empty")

    return api_key


def get_city_coordinates(city, api_key):
    """Get coordinates for a city using OpenWeatherMap Geocoding API.

    Args:
        city: Name of the city
        api_key: OpenWeatherMap API key

    Returns:
        dict: Dictionary with keys 'name', 'country', 'lat', 'lon'

    Raises:
        requests.HTTPError: If API request fails
        ValueError: If city not found
    """
    geo_params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    geo_response = requests.get(GEO_URL, params=geo_params)
    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data:
        raise ValueError(f"City not found: {city}")

    return {
        "name": geo_data[0]["name"],
        "country": geo_data[0]["country"],
        "lat": geo_data[0]["lat"],
        "lon": geo_data[0]["lon"]
    }


def get_weather_data(lat, lon, api_key):
    """Get weather data for given coordinates using OpenWeatherMap API.

    Args:
        lat: Latitude
        lon: Longitude
        api_key: OpenWeatherMap API key

    Returns:
        dict: Weather data from API

    Raises:
        requests.HTTPError: If API request fails
    """
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    weather_response = requests.get(WEATHER_URL, params=weather_params)
    weather_response.raise_for_status()

    return weather_response.json()


def get_weather(city, api_key=None):
    """Get weather information for a city.

    Args:
        city: Name of the city
        api_key: OpenWeatherMap API key (optional, loads from file if not provided)

    Returns:
        dict: Dictionary containing city info and weather data

    Raises:
        FileNotFoundError: If API key file doesn't exist
        ValueError: If API key is empty or city not found
        requests.HTTPError: If API request fails
    """
    if api_key is None:
        api_key = load_api_key()

    city_info = get_city_coordinates(city, api_key)
    weather_data = get_weather_data(city_info["lat"], city_info["lon"], api_key)

    return {
        "city": city_info,
        "weather": weather_data
    }


def print_weather_info(weather_info):
    """Print weather information in a formatted way.

    Args:
        weather_info: Dictionary returned by get_weather()
    """
    city = weather_info["city"]
    weather = weather_info["weather"]

    print(f"City: {city['name']}")
    print(f"Country: {city['country']}")
    print(f"Latitude: {city['lat']}")
    print(f"Longitude: {city['lon']}")
    print(f"Current temp: {weather['current']['temp']} °C")
    print(f"Feels like: {weather['current']['feels_like']} °C")
    print(f"Humidity: {weather['current']['humidity']}")
    print(f"Wind Speed: {weather['current']['wind_speed']}")
    print(f"Main: {weather['current']['weather'][0]['main']}")
    print(f"Description: {weather['current']['weather'][0]['description']}")


def main():
    """Main function for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python weather-in.py <city name>")
        sys.exit(1)

    if sys.argv[1] == "--help":
        print("Weather in - Get current weather information for any city")
        print()
        print("Usage:")
        print("  python weather-in.py <city name>")
        print("  python weather-in.py --help")
        print()
        print("Description:")
        print("  Fetches and displays current weather information for a specified city")
        print("  using the OpenWeatherMap API. The script requires an API key stored")
        print(f"  in {API_KEY_FILE}")
        print()
        print("Examples:")
        print("  python weather-in.py London")
        print("  python weather-in.py New York")
        print("  python weather-in.py \"Los Angeles\"")
        print()
        print("Output includes:")
        print("  - City name and country")
        print("  - Geographic coordinates (latitude/longitude)")
        print("  - Current temperature and feels like temperature")
        print("  - Humidity percentage")
        print("  - Wind speed")
        print("  - Weather conditions and description")
        sys.exit(0)

    city = " ".join(sys.argv[1:])

    try:
        weather_info = get_weather(city)
        print_weather_info(weather_info)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.HTTPError as e:
        print(f"API Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()