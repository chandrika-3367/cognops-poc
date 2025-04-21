from agents.retriever_agent import run_retriever
from agents.analyzer_agent import run_analyzer
from agents.planner_agent import run_planner
from agents.reporter_agent import run_reporter


def run_cognops_crew(issue_description: str, all_issues: list) -> dict:
    """
    Simulates full CognOps crew execution with sequential agent coordination.
    """
    crew_result = {
        "retriever_result": {},
        "analyzer_result": {},
        "planner_result": {},
        "reporter_result": {}
    }

    try:
        # Step 1: Retriever Agent
        retriever_result = run_retriever(issue_description, all_issues)
        crew_result["retriever_result"] = retriever_result

        # Step 2: Analyzer Agent
        analyzer_result = run_analyzer(retriever_result)
        crew_result["analyzer_result"] = analyzer_result

        # Step 3: Planner Agent
        planner_result = run_planner(analyzer_result)
        crew_result["planner_result"] = planner_result

        # Step 4: Reporter Agent
        reporter_result = run_reporter(planner_result)
        crew_result["reporter_result"] = reporter_result

        return crew_result

    except Exception as e:
        crew_result["error"] = f"[Crew Execution ERROR] {str(e)}"
        return crew_result
