from typing import Dict, Any, List, Tuple
from tools.log_utils import log_agent_event, log_error
from tools.rag import dynamic_rag_qa

# OPTIONAL: If the Groq endpoint is flaky or fails, replace with local model call here.
# from tools.local_llm import call_llm
from tools.llm import call_llm  # Using Groq for now


def run_retriever(issue_context: str, all_issues: list) -> Dict[str, Any]:
    agent_name = "RetrieverAgent"
    try:
        log_agent_event(agent_name, "start", {"issue_context": issue_context})

        # Step 1: Summarize current issue using LLM
        summary_prompt = f"""
        Summarize the following GitHub issue in a single concise paragraph.
        Include only technical details and root cause hints if available.

        Issue:
        {issue_context}
        """
        llm_summary = call_llm(summary_prompt)

        # Step 2: Run Dynamic RAG to retrieve similar incidents
        context_snippets, sources, confidence_scores = dynamic_rag_qa(
            issue_context, all_issues)

        result = {
            "summary": llm_summary,
            "context_snippets": context_snippets,
            "sources": sources,
            "confidence_scores": confidence_scores
        }

        log_agent_event(agent_name, "complete", result)
        return result

    except Exception as e:
        log_error(agent_name, e)
        return {
            "error": str(e),
            "raw_response": call_llm(issue_context),
            "rag_error": f"{type(e).__name__}: {str(e)}"
        }
