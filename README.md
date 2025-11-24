# MCP Weather & Air Quality Servers

Python and SpringBoot implementations of MCP (Model Context Protocol) servers providing weather, temperature, and air quality information using OpenWeatherMap API.

## Features

- **Weather Information**: Get current weather conditions for any city
- **Temperature Details**: Current, feels like, min, and max temperatures
- **Air Quality Data**: AQI and pollutant concentrations (PM2.5, PM10, CO, NO2, O3)
- **Dual Implementation**: Both Python (FastAPI) and SpringBoot versions
- **MCP Protocol**: JSON-RPC 2.0 compatible with Claude Desktop

## Quick Start

### Python Server

```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key
uvicorn src.main:app --port 8000
```

### SpringBoot Server

```bash
cd springboot
export OPENWEATHERMAP_API_KEY=your_api_key_here
export JAVA_HOME=/path/to/java-21
./gradlew bootRun
```

## Available Tools

All servers provide these MCP tools:

| Tool | Description |
|------|-------------|
| `get_weather` | Get current weather for a city |
| `get_temperature` | Get detailed temperature information |
| `get_air_quality` | Get air quality index and pollutants |

## Documentation

- [Python Setup Guide](python/README.md)
  - [SpringBoot Setup Guide](springboot/README.md)
- [API Key Setup](docs/API_KEY_SETUP.md)
- [Claude Desktop Integration](docs/CLAUDE_DESKTOP_INTEGRATION.md)

## Claude Desktop Integration

To use these MCP servers with Claude Desktop:

1. **Configure Claude Desktop** by editing `claude_desktop_config.json`
2. **Add server configuration** (see example configs in `python/` and `springboot/`)
3. **Restart Claude Desktop**
4. **Test the integration** by asking Claude about weather or air quality

See [Claude Desktop Integration Guide](docs/CLAUDE_DESKTOP_INTEGRATION.md) for detailed instructions.

## License

### Python
- Python 3.9+
- Dependencies in `requirements.txt`

### SpringBoot
- Java 21
- Gradle 8.10+

### API Key
- OpenWeatherMap API key (free tier works)
- Get yours at: https://openweathermap.org/api

## Testing

Test the server with curl:

```bash
# Python (port 8000)
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Seoul"}},"id":1}'

# SpringBoot (port 8080)
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Seoul"}},"id":1}'
```

## Project Structure

```
.
├── python/              # Python FastAPI implementation
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── mcp_handler.py
│   │   ├── tool_registry.py
│   │   ├── services/
│   │   └── tools/
│   └── requirements.txt
├── springboot/          # SpringBoot implementation
│   ├── src/main/java/com/mcp/server/
│   │   ├── McpServerApplication.java
│   │   ├── config/
│   │   ├── controller/
│   │   ├── handler/
│   │   ├── service/
│   │   └── tools/
│   └── build.gradle
└── docs/                # Documentation
```

## License

MIT
