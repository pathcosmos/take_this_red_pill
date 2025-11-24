from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
import logging
from src.tool_registry import tools_registry
# Import tools to register them
import src.tools.weather_tool
import src.tools.temperature_tool
import src.tools.air_quality_tool

router = APIRouter()
logger = logging.getLogger(__name__)

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None
    id: Optional[Union[str, int]] = None

class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[str, int]] = None

@router.post("/mcp")
async def handle_mcp_request(request: JsonRpcRequest):
    logger.info(f"Received MCP request: {request.method}")
    
    try:
        if request.method == "initialize":
            return JsonRpcResponse(
                id=request.id,
                result={
                    "protocolVersion": "0.1.0",
                    "serverInfo": {
                        "name": "python-mcp-server",
                        "version": "0.1.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            )
        
        elif request.method == "tools/list":
            tools_list = [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"]
                }
                for tool in tools_registry.values()
            ]
            return JsonRpcResponse(
                id=request.id,
                result={
                    "tools": tools_list
                }
            )
            
        elif request.method == "tools/call":
            if not request.params or "name" not in request.params:
                 return JsonRpcResponse(
                    id=request.id,
                    error={"code": -32602, "message": "Invalid params: 'name' is required"}
                )
            
            tool_name = request.params["name"]
            arguments = request.params.get("arguments", {})
            
            if tool_name not in tools_registry:
                return JsonRpcResponse(
                    id=request.id,
                    error={"code": -32601, "message": f"Tool not found: {tool_name}"}
                )
            
            tool = tools_registry[tool_name]
            try:
                # Execute the tool function
                result = await tool["func"](**arguments)
                return JsonRpcResponse(
                    id=request.id,
                    result={
                        "content": [
                            {
                                "type": "text",
                                "text": str(result)
                            }
                        ]
                    }
                )
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                return JsonRpcResponse(
                    id=request.id,
                    error={"code": -32000, "message": f"Tool execution error: {str(e)}"}
                )

        else:
            return JsonRpcResponse(
                id=request.id,
                error={"code": -32601, "message": "Method not found"}
            )
            
    except Exception as e:
        logger.error(f"Internal error: {str(e)}")
        return JsonRpcResponse(
            id=request.id,
            error={"code": -32603, "message": "Internal error"}
        )
