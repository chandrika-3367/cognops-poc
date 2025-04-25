import json
from tools.llm import call_llm


def run_planner(analysis_result: dict) -> dict:
    """
    This function receives analyzer output and generates a structured plan.
    It is designed to be invoked by CrewAI PlannerAgent.
    """
    raw_analysis = analysis_result.get("analysis", {})
    if isinstance(raw_analysis, str):
        try:
            raw_analysis = json.loads(raw_analysis)
        except Exception as e:
            return {"plan": f"[Planner ERROR] Invalid JSON from analyzer: {str(e)}"}


    # Extract context for reasoning
    root_cause = raw_analysis.get("root_cause", "")
    severity = raw_analysis.get("severity", "")
    service = raw_analysis.get("service", "")
    symptoms = raw_analysis.get("symptoms", [])

    prompt = f"""
    You are an operations planner AI agent responsible for deciding the next best step based on incident analysis.

    Incident Context:
    Root cause: {root_cause}
    Severity: {severity}
    Service: {service}
    Symptoms: {', '.join(symptoms)}

    Think step-by-step and return a plan in this format:
    {{
        "next_step": "fetch_more_info" | "generate_summary" | "escalate",
        "reason": "Why this step is important",
        "optional_tags": ["tag1", "tag2"],
        "risk": "low" | "medium" | "high",
        "eta": "e.g. 10min, 1h, unknown"
    }}

    Rules:
    - If severity is high → escalate
    - If root cause is unclear → fetch_more_info
    - If everything is resolved → generate_summary
    - Add optional_tags like "priority:high" or "team:network" if relevant
    - Be concise. Think carefully. Only respond with valid JSON.
    """

    try:
        response = call_llm(prompt)
        print("\n🧠 Raw LLM Response:\n", response)  # DEBUG LINE
        plan = json.loads(response)  # Validate JSON
        return {"plan": plan}
    except Exception as e:
        return {"plan": f"[Planner ERROR] {str(e)}"}
