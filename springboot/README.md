# SpringBoot MCP Server

Spring Boot-based MCP server providing weather and air quality information.

## Setup

### 1. Prerequisites

- Java 21 (Zulu, OpenJDK, or Oracle JDK)
- Gradle 8.10+ (wrapper included)

Check Java version:

```bash
java -version
```

Set JAVA_HOME (if needed):

```bash
# macOS with Homebrew
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home

# Linux
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk

# Verify
echo $JAVA_HOME
```

### 2. Configure Environment

Set the OpenWeatherMap API key:

```bash
export OPENWEATHERMAP_API_KEY=your_api_key_here
```

Or edit `src/main/resources/application.yml`:

```yaml
mcp:
  api-key:
    openweathermap: ${OPENWEATHERMAP_API_KEY:your_default_key}
```

### 3. Build Project

```bash
./gradlew build
```

### 4. Run Server

```bash
./gradlew bootRun
```

Or build and run JAR:

```bash
./gradlew build
java -jar build/libs/mcp-server-0.0.1-SNAPSHOT.jar
```

Server will start at `http://localhost:8080`

## Testing

### MCP Initialize

```bash
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1}'
```

### List Tools

```bash
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### Call Weather Tool

```bash
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Seoul"}},"id":1}'
```

### Call Temperature Tool

```bash
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_temperature","arguments":{"city":"Tokyo"}},"id":1}'
```

### Call Air Quality Tool

```bash
curl -X POST http://localhost:8080/mcp \
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
springboot/
├── src/main/
│   ├── java/com/mcp/server/
│   │   ├── McpServerApplication.java  # Main application
│   │   ├── config/
│   │   │   └── AppConfig.java         # WebClient configuration
│   │   ├── controller/
│   │   │   └── McpController.java     # MCP endpoint
│   │   ├── handler/
│   │   │   └── McpHandler.java        # Protocol handler
│   │   ├── service/
│   │   │   └── WeatherService.java    # API integration
│   │   └── tools/
│   │       ├── WeatherTool.java
│   │       ├── TemperatureTool.java
│   │       └── AirQualityTool.java
│   └── resources/
│       └── application.yml            # Configuration
├── build.gradle
├── settings.gradle
└── gradlew                            # Gradle wrapper
```

## Dependencies

- Spring Boot 3.2.0
- Spring Web
- Spring WebFlux (for WebClient)
- Lombok
- Jackson (JSON processing)

## Troubleshooting

### Java Version Issues

If you see "Unsupported class file major version" error:

```bash
# Use Java 21
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-21.jdk/Contents/Home
./gradlew clean build
```

### Port Already in Use

Change port in `application.yml`:

```yaml
server:
  port: 8081
```

Or set via environment variable:

```bash
SERVER_PORT=8081 ./gradlew bootRun
```

### Gradle Issues

```bash
# Clean build
./gradlew clean build

# Refresh dependencies
./gradlew build --refresh-dependencies
```

### API Key Issues

- Verify environment variable is set: `echo $OPENWEATHERMAP_API_KEY`
- Ensure the key is valid and activated
- Check `application.yml` configuration

## Running Tests

```bash
./gradlew test
```

## Building for Production

```bash
./gradlew build
# JAR will be in build/libs/
java -jar build/libs/mcp-server-0.0.1-SNAPSHOT.jar
```
