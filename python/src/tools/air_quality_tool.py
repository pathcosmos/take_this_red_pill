from typing import Any, Dict
from src.services.weather_service import weather_service
from src.tool_registry import register_tool

@register_tool(
    name="get_air_quality",
    description="Get air quality information for a specific city, including AQI and pollutant concentrations (PM2.5, PM10).",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city (e.g., 'Seoul', 'Tokyo')"
            }
        },
        "required": ["city"]
    }
)
async def get_air_quality(city: str) -> str:
    try:
        # First, get coordinates from weather data
        weather_data = await weather_service.get_weather_data(city)
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]
        
        # Then get air quality data
        aq_data = await weather_service.get_air_quality_data(lat, lon)
        
        if not aq_data["list"]:
             return "No air quality data available."
             
        main_data = aq_data["list"][0]
        aqi = main_data["main"]["aqi"]
        components = main_data["components"]
        
        # Map AQI to readable status
        aqi_status = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }.get(aqi, "Unknown")
        
        return (f"Air Quality in {city}:\n"
                f"- AQI: {aqi} ({aqi_status})\n"
                f"- PM2.5: {components.get('pm2_5', 'N/A')} μg/m3\n"
                f"- PM10: {components.get('pm10', 'N/A')} μg/m3\n"
                f"- CO: {components.get('co', 'N/A')} μg/m3\n"
                f"- NO2: {components.get('no2', 'N/A')} μg/m3\n"
                f"- O3: {components.get('o3', 'N/A')} μg/m3")
                
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error fetching air quality: {str(e)}"
