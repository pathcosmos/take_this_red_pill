#!/usr/bin/env python3
import sys
import json
import asyncio
import logging

# Setup logging to stderr (stdout is used for MCP communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import MCP handler logic
from src.tool_registry import tools_registry
import src.tools.weather_tool
import src.tools.temperature_tool
import src.tools.air_quality_tool

async def handle_request(request_data):
    """Handle MCP request and return response as dict"""
    method = request_data.get("method")
    params = request_data.get("params", {})
    request_id = request_data.get("id")
    
    logger.info(f"Handling request: {method}")
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "python-mcp-server",
                        "version": "0.1.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            }

        elif method == "notifications/initialized":
            # Client notification - no response needed
            return None
        
        elif method == "tools/list":
            tools_list = [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"]
                }
                for tool in tools_registry.values()
            ]
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools_list
                }
            }
        
        elif method == "tools/call":
            if not params or "name" not in params:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32602, "message": "Invalid params: 'name' is required"}
                }
            
            tool_name = params["name"]
            arguments = params.get("arguments", {})
            
            if tool_name not in tools_registry:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}
                }
            
            tool = tools_registry[tool_name]
            try:
                result = await tool["func"](**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": str(result)
                            }
                        ]
                    }
                }
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": f"Tool execution error: {str(e)}"}
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": "Method not found"}
            }
    
    except Exception as e:
        logger.error(f"Internal error: {str(e)}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

async def main():
    """MCP stdio server - reads from stdin, writes to stdout"""
    logger.info("MCP stdio server starting...")
    
    while True:
        try:
            # Blocking read from stdin
            line = sys.stdin.readline()
            
            # Empty line means EOF
            if not line:
                logger.info("stdin closed (EOF), exiting")
                break
            
            line = line.strip()
            if not line:
                # Skip empty lines
                continue
            
            logger.info(f"Received request: method={json.loads(line).get('method')}")
            request_data = json.loads(line)
            
            # Process request
            response = await handle_request(request_data)

            # Write response to stdout (skip for notifications)
            if response is not None:
                response_json = json.dumps(response)
                print(response_json, flush=True)
                logger.info(f"Sent response for id={response.get('id')}")
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(error_response), flush=True)
        except KeyboardInterrupt:
            logger.info("Received interrupt, exiting")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            # Continue processing on errors
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

