"""
Weather information tool (mock implementation).
"""

from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    # This is a mock implementation - in a real app, you'd call a weather API
    weather_data = {
        "new york": "Sunny, 22°C",
        "london": "Cloudy, 15°C", 
        "tokyo": "Rainy, 18°C",
        "paris": "Partly cloudy, 20°C"
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city}: {weather_data[city_lower]}"
    else:
        return f"Weather data not available for {city}. Available cities: {', '.join(weather_data.keys())}"
