from typing import Dict, Any

# Tool registry
tools_registry = {}

def register_tool(name: str, description: str, parameters: Dict[str, Any]):
    def decorator(func):
        tools_registry[name] = {
            "name": name,
            "description": description,
            "inputSchema": parameters,
            "func": func
        }
        return func
    return decorator
