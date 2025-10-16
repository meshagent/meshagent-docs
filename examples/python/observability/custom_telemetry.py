import os
import asyncio
import httpx
import logging
from meshagent.api.services import ServiceHost
from meshagent.tools import Tool, ToolContext, RemoteToolkit
from meshagent.otel import otel_config
from opentelemetry import trace

# Configure OpenTelemetry
otel_config(service_name="weather_tools")
service = ServiceHost()
log = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class WeatherTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_weather",
            title="Weather Tool",
            description="Get current weather for a city using wttr.in API",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["city", "units"],
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "units": {"type": "string", "enum": ["metric", "imperial"], "description":"Units the temperature will be returned in"}
                },
            },
        )
        # Simple in-memory cache for demonstration
        self.cache = {}

    async def execute(self, context: ToolContext, *, city: str, units:str):
        """
        This shows custom instrumentation that meshagent doesn't do automatically:
        1. Separate spans for validation, cache check, API call, parsing
        2. Custom attributes (cache status, API endpoint, response size)
        3. Events for important moments (cache hit/miss, rate limits)
        4. Error handling with span status
        """
        
        # Custom span for input validation
        with tracer.start_as_current_span("validate_input") as span:
            span.set_attribute("city", city)
            
            if not city or len(city) < 2:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Invalid city name"))
                span.add_event("validation_failed", {"reason": "city too short"})
                return {"error": "City name must be at least 2 characters"}
            
            span.add_event("validation_passed")
        
        # Custom span for cache check
        cache_key = f"{city.lower()}"
        with tracer.start_as_current_span("check_cache") as span:
            span.set_attribute("cache_key", cache_key)
            
            if cache_key in self.cache:
                span.set_attribute("cache_hit", True)
                span.add_event("cache_hit", {"ttl_remaining": "5m"})
                return self.cache[cache_key]
            else:
                span.set_attribute("cache_hit", False)
                span.add_event("cache_miss")
        
        # Custom span for external API call (this is what meshagent can't instrument)
        with tracer.start_as_current_span("fetch_weather_api") as span:
            # Add attributes about the API call
            api_url = f"https://wttr.in/{city}?format=j1"
            span.set_attribute("http.url", api_url)
            span.set_attribute("http.method", "GET")
            span.set_attribute("api.provider", "wttr.in")
            
            span.add_event("api_request_start")
            
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(api_url)
                    
                    # Record response attributes
                    span.set_attribute("http.status_code", response.status_code)
                    span.set_attribute("http.response_size", len(response.content))
                    
                    if response.status_code == 429:
                        span.add_event("rate_limit_exceeded")
                        span.set_status(trace.Status(trace.StatusCode.ERROR, "Rate limited"))
                        return {"error": "Rate limit exceeded, try again later"}
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    span.add_event("api_request_success", {
                        "data_keys": list(data.keys()),
                    })
                    
            except httpx.TimeoutException:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "API timeout"))
                span.add_event("api_timeout")
                return {"error": "Weather service timeout"}
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                span.add_event("api_error", {"error_type": type(e).__name__})
                return {"error": f"Failed to fetch weather: {str(e)}"}
        
        # Custom span for parsing and formatting
        with tracer.start_as_current_span("parse_response") as span:
            try:
                current = data['current_condition'][0]
                location = data['nearest_area'][0]
                
                if units == "metric":
                    temperature = current["temp_C"]
                    degrees_in = "°C"
                elif units == "imperial":
                    temperature = current["temp_F"]
                    degrees_in = "°F"
                else:
                    log.warning(f"Units {units} is not a valid unit. Must use metric or imperial")
                    return "Invalid units"

                result = {
                    "city": location['areaName'][0]['value'],
                    "country": location['country'][0]['value'],
                    "temperature": temperature,
                    "units": degrees_in,
                    "description": current['weatherDesc'][0]['value'],
                    "humidity": current['humidity'],
                    "wind_speed": current['windspeedKmph'],
                }
                
                # Record what we parsed
                span.set_attribute("parsed_fields", len(result))
                span.add_event("parse_success")
                
                # Cache the result
                with tracer.start_as_current_span("cache_result") as cache_span:
                    self.cache[cache_key] = result
                    cache_span.set_attribute("cache_key", cache_key)
                    cache_span.add_event("cached", {"entry_count": len(self.cache)})
                
                return result
                
            except (KeyError, IndexError) as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Parse failed"))
                span.add_event("parse_error", {"error": str(e)})
                return {"error": "Failed to parse weather data"}


@service.path(path="/weather", identity="weather-toolkit")
class WeatherToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="weather-toolkit",
            title="Weather Toolkit",
            description="Tools for getting weather information",
            tools=[WeatherTool()],
        )

asyncio.run(service.run())