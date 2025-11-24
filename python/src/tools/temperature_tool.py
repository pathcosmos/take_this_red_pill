from typing import Any, Dict
from src.services.weather_service import weather_service
from src.tool_registry import register_tool

@register_tool(
    name="get_temperature",
    description="Get detailed temperature information for a specific city, including feels like, min, and max temperatures.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city (e.g., 'Seoul', 'New York')"
            }
        },
        "required": ["city"]
    }
)
async def get_temperature(city: str) -> str:
    try:
        data = await weather_service.get_weather_data(city)
        
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        
        return (f"Temperature in {city}:\n"
                f"- Current: {temp}°C\n"
                f"- Feels Like: {feels_like}°C\n"
                f"- Min: {temp_min}°C\n"
                f"- Max: {temp_max}°C")
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error fetching temperature: {str(e)}"
