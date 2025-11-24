package com.mcp.server.handler;

import com.mcp.server.tools.WeatherTool;
import com.mcp.server.tools.TemperatureTool;
import com.mcp.server.tools.AirQualityTool;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

import java.util.*;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class McpHandler {

    private final WeatherTool weatherTool;
    private final TemperatureTool temperatureTool;
    private final AirQualityTool airQualityTool;
    
    private List<Object> getRegisteredTools() {
        List<Object> tools = new ArrayList<>();
        tools.add(weatherTool);
        tools.add(temperatureTool);
        tools.add(airQualityTool);
        return tools;
    }

    public Mono<Map<String, Object>> handleRequest(Map<String, Object> request) {
        String method = (String) request.get("method");
        Object id = request.get("id");
        Map<String, Object> params = (Map<String, Object>) request.get("params");

        if ("initialize".equals(method)) {
            return Mono.just(createResponse(id, Map.of(
                "protocolVersion", "0.1.0",
                "serverInfo", Map.of("name", "springboot-mcp-server", "version", "0.1.0"),
                "capabilities", Map.of("tools", Map.of())
            )));
        } else if ("tools/list".equals(method)) {
            List<Map<String, Object>> toolsList = getRegisteredTools().stream()
                .map(tool -> {
                    if (tool instanceof WeatherTool) {
                        WeatherTool wt = (WeatherTool) tool;
                        return Map.of(
                            "name", wt.getName(),
                            "description", wt.getDescription(),
                            "inputSchema", wt.getInputSchema()
                        );
                    } else if (tool instanceof TemperatureTool) {
                        TemperatureTool tt = (TemperatureTool) tool;
                        return Map.of(
                            "name", tt.getName(),
                            "description", tt.getDescription(),
                            "inputSchema", tt.getInputSchema()
                        );
                    } else if (tool instanceof AirQualityTool) {
                        AirQualityTool aqt = (AirQualityTool) tool;
                        return Map.of(
                            "name", aqt.getName(),
                            "description", aqt.getDescription(),
                            "inputSchema", aqt.getInputSchema()
                        );
                    }
                    return Map.<String, Object>of();
                })
                .collect(Collectors.toList());
            
            return Mono.just(createResponse(id, Map.of("tools", toolsList)));
        } else if ("tools/call".equals(method)) {
            if (params == null || !params.containsKey("name")) {
                return Mono.just(createErrorResponse(id, -32602, "Invalid params: 'name' is required"));
            }
            
            String toolName = (String) params.get("name");
            Map<String, Object> arguments = (Map<String, Object>) params.getOrDefault("arguments", Map.of());
            
            return executeToolByName(toolName, arguments)
                .map(result -> createResponse(id, Map.of(
                    "content", List.of(Map.of("type", "text", "text", result))
                )))
                .onErrorResume(e -> Mono.just(createErrorResponse(id, -32000, "Tool execution error: " + e.getMessage())));
        } else {
            return Mono.just(createErrorResponse(id, -32601, "Method not found"));
        }
    }
    
    private Mono<String> executeToolByName(String toolName, Map<String, Object> arguments) {
        for (Object tool : getRegisteredTools()) {
            if (tool instanceof WeatherTool && "get_weather".equals(toolName)) {
                return ((WeatherTool) tool).execute(arguments);
            } else if (tool instanceof TemperatureTool && "get_temperature".equals(toolName)) {
                return ((TemperatureTool) tool).execute(arguments);
            } else if (tool instanceof AirQualityTool && "get_air_quality".equals(toolName)) {
                return ((AirQualityTool) tool).execute(arguments);
            }
        }
        return Mono.error(new RuntimeException("Tool not found: " + toolName));
    }

    private Map<String, Object> createResponse(Object id, Object result) {
        Map<String, Object> response = new HashMap<>();
        response.put("jsonrpc", "2.0");
        response.put("id", id);
        response.put("result", result);
        return response;
    }

    private Map<String, Object> createErrorResponse(Object id, int code, String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("jsonrpc", "2.0");
        response.put("id", id);
        response.put("error", Map.of("code", code, "message", message));
        return response;
    }
}
