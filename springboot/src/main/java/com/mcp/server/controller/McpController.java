package com.mcp.server.controller;

import com.mcp.server.handler.McpHandler;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.Map;

@RestController
@RequiredArgsConstructor
public class McpController {

    private final McpHandler mcpHandler;

    @PostMapping("/mcp")
    public Mono<Map<String, Object>> handleMcpRequest(@RequestBody Map<String, Object> request) {
        return mcpHandler.handleRequest(request);
    }
}
