import logging
from datetime import datetime
from typing import Any, Dict

# Configure a base logger
logging.basicConfig(
    filename="agent_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_agent_event(agent_name: str, stage: str, payload: Dict[str, Any]) -> None:
    """Log agent inputs/outputs/errors by stage."""
    log_entry = {
        "agent": agent_name,
        "stage": stage,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }
    logging.info(log_entry)


def log_error(agent_name: str, error: Exception) -> None:
    """Log agent-level error."""
    logging.error(f"{agent_name} encountered an error: {str(error)}")
