# test_planner_agent.py

from agents.planner_agent import run_planner
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    mock_analysis = {
        "analysis": {
            "root_cause": "Database connection timeout",
            "severity": "high",
            "service": "User Auth API",
            "symptoms": ["Login failure", "500 errors"]
        }
    }

    result = run_planner(mock_analysis)
    print("🧠 Planner Output:\n", result)
