# Claude Desktop Integration Guide

This guide explains how to integrate the MCP servers with Claude Desktop.

## Prerequisites

- Claude Desktop installed
- Python or SpringBoot MCP server running
- OpenWeatherMap API key configured

## Configuration

Claude Desktop uses a JSON configuration file to connect to MCP servers. The location varies by OS:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Python Server Configuration

### 1. Setup Python Environment

```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather-python": {
      "command": "/absolute/path/to/python/venv/bin/python",
      "args": ["/absolute/path/to/python/mcp_stdio_server.py"],
      "cwd": "/absolute/path/to/python",
      "env": {
        "OPENWEATHERMAP_API_KEY": "your_api_key_here",
        "PYTHONPATH": "/absolute/path/to/python"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/python` with the actual path to your Python directory.

**Note**: The Python server uses stdio transport and starts automatically when Claude Desktop launches. No need to start the server manually.

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the new configuration.

## SpringBoot Server Configuration

### 1. Build SpringBoot Server

```bash
cd springboot
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home
./gradlew build
```

### 2. Configure Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather-springboot": {
      "command": "java",
      "args": [
        "-jar",
        "build/libs/mcp-server-0.0.1-SNAPSHOT.jar"
      ],
      "cwd": "/absolute/path/to/springboot",
      "env": {
        "OPENWEATHERMAP_API_KEY": "your_api_key_here",
        "JAVA_HOME": "/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home"
      }
    }
  }
}
```

**Important**: 
- Replace `/absolute/path/to/springboot` with the actual path
- Update `JAVA_HOME` to match your Java installation

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the new configuration.

## Running Both Servers

You can run both Python and SpringBoot servers simultaneously:

```json
{
  "mcpServers": {
    "weather-python": {
      "command": "/path/to/python/venv/bin/python",
      "args": ["/path/to/python/mcp_stdio_server.py"],
      "cwd": "/path/to/python",
      "env": {
        "OPENWEATHERMAP_API_KEY": "your_api_key_here",
        "PYTHONPATH": "/path/to/python"
      }
    },
    "weather-springboot": {
      "command": "java",
      "args": ["-jar", "build/libs/mcp-server-0.0.1-SNAPSHOT.jar"],
      "cwd": "/path/to/springboot",
      "env": {
        "OPENWEATHERMAP_API_KEY": "your_api_key_here",
        "JAVA_HOME": "/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home"
      }
    }
  }
}
```

## Testing the Integration

### 1. Verify Server Connection

In Claude Desktop, check if the MCP server is connected:
- Look for the MCP indicator in the UI
- Tools should be available in the chat interface

### 2. Test Weather Tool

Ask Claude:

```
What's the weather like in Seoul?
```

Claude should use the `get_weather` tool to provide current weather information.

### 3. Test Temperature Tool

Ask Claude:

```
What's the temperature in Tokyo right now? Include feels like temperature.
```

Claude should use the `get_temperature` tool to provide detailed temperature data.

### 4. Test Air Quality Tool

Ask Claude:

```
How's the air quality in London today?
```

Claude should use the `get_air_quality` tool to provide AQI and pollutant information.

## Example Queries

Try these queries to test all features:

1. **Simple weather**: "What's the weather in Paris?"
2. **Temperature details**: "How cold is it in New York? Give me all temperature details."
3. **Air quality**: "Is the air quality good in Beijing?"
4. **Multiple cities**: "Compare the weather in London, Tokyo, and Sydney."
5. **Complex query**: "What's the weather, temperature, and air quality in Seoul?"

## Troubleshooting

### Server Not Connecting

1. **Check configuration**:
   - Verify JSON syntax is correct
   - Ensure paths are absolute, not relative
   - Check that API key is set

2. **Check server logs**:
   - Python: Look at uvicorn output
   - SpringBoot: Check application logs

3. **Verify server is running**:
   ```bash
   # Python
   curl http://localhost:8000/health
   
   # SpringBoot
   curl -X POST http://localhost:8080/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"initialize","id":1}'
   ```

### Tools Not Appearing

1. **Restart Claude Desktop** completely
2. **Check MCP server logs** for errors
3. **Verify tool registration**:
   ```bash
   curl -X POST http://localhost:8000/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
   ```

### API Key Errors

- Ensure the key is activated (may take 2 hours for new keys)
- Verify the key is correct in the configuration
- Check rate limits haven't been exceeded

## Alternative: HTTP Server Mode

If you prefer to run the server as HTTP endpoint instead of stdio:

### Python

1. Start server in terminal:
   ```bash
   cd python
   source venv/bin/activate
   uvicorn src.main:app --port 8000
   ```

2. Configure Claude Desktop to connect to existing server:
   ```json
   {
     "mcpServers": {
       "weather-python": {
         "url": "http://localhost:8000/mcp"
       }
     }
   }
   ```

**Note**: HTTP mode requires the server to be running before Claude Desktop starts.

### SpringBoot

1. Start server in terminal:
   ```bash
   cd springboot
   export OPENWEATHERMAP_API_KEY=your_key
   export JAVA_HOME=/path/to/java-21
   ./gradlew bootRun
   ```

2. Configure Claude Desktop:
   ```json
   {
     "mcpServers": {
       "weather-springboot": {
         "url": "http://localhost:8080/mcp"
       }
     }
   }
   ```

## Security Notes

- Never commit your API keys to version control
- Use environment variables for sensitive data
- Consider using different API keys for development and production
- Monitor your API usage at https://home.openweathermap.org/statistics

## Additional Resources

- [Claude Desktop Documentation](https://claude.ai/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [OpenWeatherMap API Docs](https://openweathermap.org/api)
