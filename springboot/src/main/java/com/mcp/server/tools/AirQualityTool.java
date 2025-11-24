package com.mcp.server.tools;

import com.mcp.server.service.WeatherService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

@Component
@RequiredArgsConstructor
public class AirQualityTool {

    private final WeatherService weatherService;

    public String getName() {
        return "get_air_quality";
    }

    public String getDescription() {
        return "Get air quality information for a specific city, including AQI and pollutant concentrations (PM2.5, PM10).";
    }

    public Map<String, Object> getInputSchema() {
        return Map.of(
            "type", "object",
            "properties", Map.of(
                "city", Map.of(
                    "type", "string",
                    "description", "Name of the city (e.g., 'Seoul', 'Tokyo')"
                )
            ),
            "required", new String[]{"city"}
        );
    }

    public Mono<String> execute(Map<String, Object> arguments) {
        String city = (String) arguments.get("city");
        
        return weatherService.getWeatherData(city)
            .flatMap(weatherData -> {
                Map<String, Object> coord = (Map<String, Object>) weatherData.get("coord");
                double lat = ((Number) coord.get("lat")).doubleValue();
                double lon = ((Number) coord.get("lon")).doubleValue();
                
                return weatherService.getAirQualityData(lat, lon);
            })
            .map(aqData -> {
                List<Map<String, Object>> list = (List<Map<String, Object>>) aqData.get("list");
                if (list == null || list.isEmpty()) {
                    return "No air quality data available.";
                }
                
                Map<String, Object> mainData = list.get(0);
                Map<String, Object> main = (Map<String, Object>) mainData.get("main");
                Map<String, Object> components = (Map<String, Object>) mainData.get("components");
                
                int aqi = ((Number) main.get("aqi")).intValue();
                String aqiStatus = getAqiStatus(aqi);
                
                Object pm25 = components.get("pm2_5");
                Object pm10 = components.get("pm10");
                Object co = components.get("co");
                Object no2 = components.get("no2");
                Object o3 = components.get("o3");
                
                return String.format("Air Quality in %s:\n- AQI: %d (%s)\n- PM2.5: %s μg/m3\n- PM10: %s μg/m3\n- CO: %s μg/m3\n- NO2: %s μg/m3\n- O3: %s μg/m3",
                    city, aqi, aqiStatus, pm25, pm10, co, no2, o3);
            })
            .onErrorResume(e -> Mono.just("Error fetching air quality: " + e.getMessage()));
    }
    
    private String getAqiStatus(int aqi) {
        return switch (aqi) {
            case 1 -> "Good";
            case 2 -> "Fair";
            case 3 -> "Moderate";
            case 4 -> "Poor";
            case 5 -> "Very Poor";
            default -> "Unknown";
        };
    }
}
