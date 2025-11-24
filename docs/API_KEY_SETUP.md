# OpenWeatherMap API Key Setup

This guide explains how to obtain and configure your OpenWeatherMap API key for the MCP servers.

## Getting Your API Key

### 1. Create an Account

1. Visit [OpenWeatherMap](https://openweathermap.org/)
2. Click "Sign In" → "Create an Account"
3. Fill in your details and verify your email

### 2. Generate API Key

1. Log in to your account
2. Navigate to [API Keys page](https://home.openweathermap.org/api_keys)
3. Your default API key is automatically created
4. Or click "Generate" to create a new key
5. Copy your API key (format: `aff5d42d94e7e836a0d8045d4c1e35b9`)

### 3. Activate Your Key

- **Important**: New API keys may take up to 2 hours to activate
- Test your key before using it in production

## Testing Your API Key

Test if your key is working:

```bash
# Replace YOUR_API_KEY with your actual key
curl "https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=YOUR_API_KEY"
```

Expected response:

```json
{
  "coord": {"lon": 126.9778, "lat": 37.5683},
  "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds"}],
  ...
}
```

## Configuring the Servers

### Python Server

1. Copy the example file:

```bash
cd python
cp .env.example .env
```

2. Edit `.env`:

```env
OPENWEATHERMAP_API_KEY=your_actual_api_key_here
PORT=8000
DEBUG=true
```

3. The server will load this automatically on startup

### SpringBoot Server

Option 1: Environment Variable (Recommended)

```bash
export OPENWEATHERMAP_API_KEY=your_actual_api_key_here
./gradlew bootRun
```

Option 2: Edit `application.yml`

```yaml
mcp:
  api-key:
    openweathermap: your_actual_api_key_here
```

**Note**: Don't commit your API key to version control!

## API Usage Limits

### Free Tier

- **60 calls/minute**
- **1,000,000 calls/month**
- Current weather data
- 5-day forecast
- Air pollution data

This is sufficient for development and testing.

### Paid Tiers

If you need more:
- Visit [OpenWeatherMap Pricing](https://openweathermap.org/price)
- Choose a plan that fits your needs

## Security Best Practices

1. **Never commit** API keys to Git
   - `.env` is in `.gitignore`
   - Always use environment variables

2. **Rotate keys** periodically
   - Generate new keys in your dashboard
   - Delete old unused keys

3. **Monitor usage**
   - Check your [statistics](https://home.openweathermap.org/statistics)
   - Set up alerts for high usage

4. **Use different keys** for dev/prod
   - Generate separate keys
   - Track usage independently

## Troubleshooting

### "Invalid API key" Error

- Verify the key is correctly copied (no extra spaces)
- Check if key is activated (wait up to 2 hours for new keys)
- Ensure key hasn't been deleted from your account

### Rate Limit Exceeded

```json
{
  "cod": 429,
  "message": "Your account is temporary blocked due to exceeding of requests limitation"
}
```

Solution:
- Wait for the rate limit to reset (1 minute)
- Upgrade to a paid plan
- Implement caching in your application

### 401 Unauthorized

```json
{
  "cod": 401,
  "message": "Invalid API key"
}
```

Solution:
- Double-check your API key
- Ensure environment variables are set correctly
- Restart your server after changing the key

## API Endpoints Used

This project uses:

1. **Current Weather**
   - `https://api.openweathermap.org/data/2.5/weather`
   - Used by: `get_weather`, `get_temperature`

2. **Air Pollution**
   - `http://api.openweathermap.org/data/2.5/air_pollution`
   - Used by: `get_air_quality`

## Additional Resources

- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [FAQ](https://openweathermap.org/faq)
- [Support](https://openweathermap.org/support)
