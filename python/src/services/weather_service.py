import httpx
from typing import Dict, Any, Optional
from src.config import settings

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather_data(self, city: str) -> Dict[str, Any]:
        if not settings.OPENWEATHERMAP_API_KEY:
             raise ValueError("OpenWeatherMap API Key is missing")

        params = {
            "q": city,
            "appid": settings.OPENWEATHERMAP_API_KEY,
            "units": "metric" # Celsius
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ValueError(f"City not found: {city}")
                raise Exception(f"OpenWeatherMap API error: {e.response.status_code}")
            except Exception as e:
                raise Exception(f"Failed to fetch weather data: {str(e)}")

    async def get_air_quality_data(self, lat: float, lon: float) -> Dict[str, Any]:
        if not settings.OPENWEATHERMAP_API_KEY:
             raise ValueError("OpenWeatherMap API Key is missing")

        url = "http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.OPENWEATHERMAP_API_KEY
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise Exception(f"Failed to fetch air quality data: {str(e)}")

weather_service = WeatherService()
