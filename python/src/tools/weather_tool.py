from typing import Any, Dict
from src.services.weather_service import weather_service
from src.tool_registry import register_tool

@register_tool(
    name="get_weather",
    description="Get current weather information for a specific city.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city (e.g., 'Seoul', 'London')"
            }
        },
        "required": ["city"]
    }
)
async def get_weather(city: str) -> str:
    try:
        data = await weather_service.get_weather_data(city)
        
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        return f"Weather in {city}: {weather_desc}, Temperature: {temp}°C, Humidity: {humidity}%"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
