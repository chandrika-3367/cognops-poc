from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Incident(BaseModel):
    number: str
    title: str
    body: str
    url: str
    created_at: Optional[str] = None


class MCPContext(BaseModel):
    input: Dict[str, Any]
    source: str = Field(default="user")
    agent: str
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat())


class MCPMetadata(BaseModel):
    version: str = "1.0"
    format: str = "MCP"


class MCPPayload(BaseModel):
    context: MCPContext
    meta: MCPMetadata


class AgentOutput(BaseModel):
    raw: str
    summary: Optional[str] = None
    reasoning_trace: Optional[str] = None
