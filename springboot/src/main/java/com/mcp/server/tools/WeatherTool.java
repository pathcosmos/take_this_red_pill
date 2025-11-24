package com.mcp.server.tools;

import com.mcp.server.service.WeatherService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

import java.util.Map;

@Component
@RequiredArgsConstructor
public class WeatherTool {

    private final WeatherService weatherService;

    public String getName() {
        return "get_weather";
    }

    public String getDescription() {
        return "Get current weather information for a specific city.";
    }

    public Map<String, Object> getInputSchema() {
        return Map.of(
            "type", "object",
            "properties", Map.of(
                "city", Map.of(
                    "type", "string",
                    "description", "Name of the city (e.g., 'Seoul', 'London')"
                )
            ),
            "required", new String[]{"city"}
        );
    }

    public Mono<String> execute(Map<String, Object> arguments) {
        String city = (String) arguments.get("city");
        
        return weatherService.getWeatherData(city)
            .map(data -> {
                Map<String, Object> weather = ((java.util.List<Map<String, Object>>) data.get("weather")).get(0);
                Map<String, Object> main = (Map<String, Object>) data.get("main");
                
                String description = (String) weather.get("description");
                Object temp = main.get("temp");
                Object humidity = main.get("humidity");
                
                return String.format("Weather in %s: %s, Temperature: %s°C, Humidity: %s%%",
                    city, description, temp, humidity);
            })
            .onErrorResume(e -> Mono.just("Error fetching weather: " + e.getMessage()));
    }
}
