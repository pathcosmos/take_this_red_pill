package com.mcp.server.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Map;

@Service
public class WeatherService {

    private static final String BASE_URL = "https://api.openweathermap.org/data/2.5/weather";
    
    @Value("${mcp.api-key.openweathermap}")
    private String apiKey;
    
    private final WebClient.Builder webClientBuilder;

    public WeatherService(WebClient.Builder webClientBuilder) {
        this.webClientBuilder = webClientBuilder;
    }

    public Mono<Map<String, Object>> getWeatherData(String city) {
        return webClientBuilder.build()
            .get()
            .uri(uriBuilder -> uriBuilder
                .scheme("https")
                .host("api.openweathermap.org")
                .path("/data/2.5/weather")
                .queryParam("q", city)
                .queryParam("appid", apiKey)
                .queryParam("units", "metric")
                .build())
            .retrieve()
            .bodyToMono(Map.class)
            .map(map -> (Map<String, Object>) map)
            .onErrorMap(e -> new RuntimeException("Failed to fetch weather data: " + e.getMessage(), e));
    }

    public Mono<Map<String, Object>> getAirQualityData(double lat, double lon) {
        return webClientBuilder.build()
            .get()
            .uri(uriBuilder -> uriBuilder
                .scheme("http")
                .host("api.openweathermap.org")
                .path("/data/2.5/air_pollution")
                .queryParam("lat", lat)
                .queryParam("lon", lon)
                .queryParam("appid", apiKey)
                .build())
            .retrieve()
            .bodyToMono(Map.class)
            .map(map -> (Map<String, Object>) map)
            .onErrorMap(e -> new RuntimeException("Failed to fetch air quality data: " + e.getMessage(), e));
    }
}
