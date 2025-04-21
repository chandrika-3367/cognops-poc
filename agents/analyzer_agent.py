from tools.llm import call_llm


def run_analyzer(retriever_result: dict) -> dict:
    context = "\n".join(retriever_result.get("context_snippets", []))
    issue_summary = retriever_result.get("summary", "")

    prompt = f"""
You are an incident analysis agent. Extract structured insight from the GitHub incident description and context.

### Incident Summary:
{issue_summary}

### Retrieved Context:
{context}

Extract the following as JSON:
{{
  "root_cause": "...",
  "severity": "...", 
  "service": "...", 
  "symptoms": ["...", "..."]
}}
Only respond with valid JSON.
"""

    try:
        response = call_llm(prompt)
        return {"analysis": response}
    except Exception as e:
        return {"analysis": f"[Analyzer ERROR] {str(e)}"}
