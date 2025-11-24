# Python MCP Server

FastAPI-based MCP server providing weather and air quality information.

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key:

```
OPENWEATHERMAP_API_KEY=your_api_key_here
PORT=8000
DEBUG=true
```

### 4. Run Server

```bash
uvicorn src.main:app --port 8000

# Or with reload for development
uvicorn src.main:app --port 8000 --reload
```

Server will start at `http://localhost:8000`

## Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather-python": {
      "command": "/Volumes/T72TB/show_must_go_on/take_this_red_pill/python/venv/bin/python",
      "args": ["/Volumes/T72TB/show_must_go_on/take_this_red_pill/python/mcp_stdio_server.py"],
      "cwd": "/Volumes/T72TB/show_must_go_on/take_this_red_pill/python",
      "env": {
        "OPENWEATHERMAP_API_KEY": "your_api_key_here",
        "PYTHONPATH": "/Volumes/T72TB/show_must_go_on/take_this_red_pill/python"
      }
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

## Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### MCP Initialize

```bash
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1}'
```

### List Tools

```bash
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### Call Weather Tool

```bash
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Seoul"}},"id":1}'
```

### Call Temperature Tool

```bash
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_temperature","arguments":{"city":"Tokyo"}},"id":1}'
```

### Call Air Quality Tool

```bash
curl -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_air_quality","arguments":{"city":"London"}},"id":1}'
```

## Available Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `get_weather` | `city` (string) | Current weather conditions |
| `get_temperature` | `city` (string) | Detailed temperature info |
| `get_air_quality` | `city` (string) | AQI and pollutant data |

## Project Structure

```
python/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── mcp_handler.py       # MCP protocol handler
│   ├── tool_registry.py     # Tool registration system
│   ├── services/
│   │   └── weather_service.py  # OpenWeatherMap API client
│   └── tools/
│       ├── weather_tool.py
│       ├── temperature_tool.py
│       └── air_quality_tool.py
├── requirements.txt
└── .env.example
```

## Dependencies

- `fastapi>=0.100.0` - Web framework
- `uvicorn[standard]>=0.22.0` - ASGI server
- `httpx>=0.24.0` - HTTP client
- `pydantic>=2.0.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management
- `python-dotenv>=1.0.0` - Environment variable loading

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### API Key Issues

- Ensure your OpenWeatherMap API key is valid
- Check that `.env` file is in the `python/` directory
- Verify the key is activated (may take a few hours for new keys)

### Import Errors

```bash
# Ensure you're in the virtual environment
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```
