import json
from tools.llm import call_llm

def run_analyzer(retriever_output: dict) -> dict:
    """
    This function analyzes the retriever output and returns a structured JSON analysis.
    """

    context = retriever_output.get("summary", "")

    if not context:
        return {"analysis": "[Analyzer ERROR] No context provided"}

    prompt = f"""
    You are an incident analysis AI.

    Analyze the following incident context carefully:
    -----
    {context}
    -----

    Extract these fields into a JSON object:

    {{
      "root_cause": "short reason",
      "severity": "low | medium | high",
      "service": "which service is impacted",
      "symptoms": ["list", "of", "main", "symptoms"]
    }}

    Respond ONLY with a valid JSON object. No explanation.
    """

    try:
        response = call_llm(prompt)
        analysis_json = json.loads(response)  # Validate JSON
        return {"analysis": analysis_json}
    except Exception as e:
        return {"analysis": f"[Analyzer ERROR] {str(e)}"}