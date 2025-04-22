from tools.llm_wrapper import GroqLLM
from agents.retriever_agent import run_retriever
from agents.analyzer_agent import run_analyzer
# from agents.planner_agent import run_planner
# from agents.reporter_agent import run_reporter
import json


def run_cognops_crew(issue_description: str, all_issues: list) -> dict:
    print("⚙️ RUNNING BASIC AGENT FLOW (No CrewAI)")

    crew_result = {
        "retriever_result": {},
        "analyzer_result": {},
        # "planner_result": {},
        # "reporter_result": {},
    }

    try:
        crew_result["retriever_result"] = retriever_output or {}
        crew_result["analyzer_result"] = analyzer_output or {}
        # crew_result["planner_result"] = planner_output or {}
        # crew_result["reporter_result"] = reporter_output or {}

        return crew_result

    except Exception as e:
        print("❌ Agent Flow Error:", str(e))
        crew_result["error"] = f"[Agent Execution ERROR] {str(e)}"
        return crew_result


# Need to implement the actual CrewAI framework once all the agents are implemented


# # ✅ Load your Groq-based LLM
# llm = GroqLLM(groq_api_key="your-groq-api-key")


# def run_cognops_crew(issue_description: str, all_issues: list) -> dict:
#     print("⚙️ RUNNING CREWAI AGENT FLOW")

#     crew_result = {
#         "retriever_result": {},
#         "analyzer_result": {},
#         "planner_result": {},
#         "reporter_result": {},
#     }

#     try:
#         # === CrewAgent Definitions ===
#         retriever = CrewAgent(
#             name="RetrieverAgent",
#             role="Context Collector",
#             goal="Find relevant past GitHub incidents from context",
#             backstory="This agent looks for similarities in incidents to help reasoning.",
#             llm=llm
#         )

#         analyzer = CrewAgent(
#             name="AnalyzerAgent",
#             role="Root Cause Extractor",
#             goal="Analyze incidents to extract structured insights like root cause, service impacted, severity, etc.",
#             backstory="This agent interprets incidents into structured diagnostics.",
#             llm=llm
#         )

#         planner = CrewAgent(
#             name="PlannerAgent",
#             role="Remediation Strategist",
#             goal="Create an actionable resolution plan based on incident analysis",
#             backstory="Plans how to fix the problem in stages.",
#             llm=llm
#         )

#         reporter = CrewAgent(
#             name="ReporterAgent",
#             role="Incident Summarizer",
#             goal="Summarize the incident, root cause, and remediation into a user-facing report",
#             backstory="Prepares the final report for management or DevOps review.",
#             llm=llm
#         )

#         # === Tasks for each agent ===
#         retriever_task = Task(
#             description="Fetch top 5 similar GitHub incidents.",
#             expected_output="Context snippets, confidence scores, and summary",
#             agent=retriever,
#             function=lambda: run_retriever(issue_description, all_issues)
#         )

#         analyzer_task = Task(
#             description="Extract root cause, severity, and service from incident context.",
#             expected_output="JSON string with root_cause, severity, service",
#             agent=analyzer,
#             function=lambda: run_analyzer(retriever_task.result)
#         )

#         planner_task = Task(
#             description="Plan remediation steps based on analysis.",
#             expected_output="Markdown-formatted plan of action",
#             agent=planner,
#             function=lambda: run_planner(analyzer_task.result)
#         )

#         reporter_task = Task(
#             description="Write an incident report from planner output.",
#             expected_output="Human-readable summary of issue and resolution",
#             agent=reporter,
#             function=lambda: run_reporter(planner_task.result)
#         )

#         # === Crew Orchestration ===
#         crew = Crew(
#             agents=[retriever, analyzer, planner, reporter],
#             tasks=[retriever_task, analyzer_task, planner_task, reporter_task],
#             verbose=True
#         )

#         crew.kickoff()

#         # === Collect Results ===
#         crew_result["retriever_result"] = retriever_task.result or {}
#         crew_result["analyzer_result"] = analyzer_task.result or {}
#         crew_result["planner_result"] = planner_task.result or {}
#         crew_result["reporter_result"] = reporter_task.result or {}

#         return crew_result

#     except Exception as e:
#         print("❌ Crew Execution Error:", str(e))
#         crew_result["error"] = f"[Crew Execution ERROR] {str(e)}"
#         return crew_result
