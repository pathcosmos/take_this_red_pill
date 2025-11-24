package com.mcp.server.tools;

import com.mcp.server.service.WeatherService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

import java.util.Map;

@Component
@RequiredArgsConstructor
public class TemperatureTool {

    private final WeatherService weatherService;

    public String getName() {
        return "get_temperature";
    }

    public String getDescription() {
        return "Get detailed temperature information for a specific city, including feels like, min, and max temperatures.";
    }

    public Map<String, Object> getInputSchema() {
        return Map.of(
            "type", "object",
            "properties", Map.of(
                "city", Map.of(
                    "type", "string",
                    "description", "Name of the city (e.g., 'Seoul', 'New York')"
                )
            ),
            "required", new String[]{"city"}
        );
    }

    public Mono<String> execute(Map<String, Object> arguments) {
        String city = (String) arguments.get("city");
        
        return weatherService.getWeatherData(city)
            .map(data -> {
                Map<String, Object> main = (Map<String, Object>) data.get("main");
                
                Object temp = main.get("temp");
                Object feelsLike = main.get("feels_like");
                Object tempMin = main.get("temp_min");
                Object tempMax = main.get("temp_max");
                
                return String.format("Temperature in %s:\n- Current: %s°C\n- Feels Like: %s°C\n- Min: %s°C\n- Max: %s°C",
                    city, temp, feelsLike, tempMin, tempMax);
            })
            .onErrorResume(e -> Mono.just("Error fetching temperature: " + e.getMessage()));
    }
}
