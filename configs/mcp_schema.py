from datetime import datetime
from typing import Dict, Any


def build_mcp_context(input_data: Dict[str, Any], agent_name: str, source: str = "user") -> Dict[str, Any]:
    """
    Builds a standard MCP payload to send to tools (e.g., LLM).
    """
    return {
        "context": {
            "input": input_data,
            "source": source,
            "agent": agent_name,
            "timestamp": datetime.utcnow().isoformat()
        },
        "meta": {
            "version": "1.0",
            "format": "MCP"
        }
    }


def parse_mcp_output(raw_response: str) -> Dict[str, Any]:
    """
    Parses raw LLM output and attaches traceable summary.
    """
    return {
        "raw": raw_response.strip(),
        "summary": raw_response.strip().split("\n")[0] if "\n" in raw_response else raw_response.strip(),
        "reasoning_trace": raw_response.strip()
    }
