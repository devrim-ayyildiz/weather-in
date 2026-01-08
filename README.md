# weather-in
Weather in - Get current weather information for any city.

This script fetches and displays current weather information for a specified city using the OpenWeatherMap API. It requires an API key stored in ~/.apikey

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
