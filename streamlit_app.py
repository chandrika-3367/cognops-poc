import streamlit as st
import requests
import builtins
import json

from agents.retriever_agent import run_retriever
from agents.analyzer_agent import run_analyzer
# from agents.planner_agent import run_planner
# from agents.reporter_agent import run_reporter
from tools.llm import call_llm
from crew.run_cognops_crew import run_cognops_crew

st.set_page_config(page_title="CognOps – AI Ops Panel", layout="wide")
st.title(" CognOps – AI Incident Response Mesh")
st.markdown(
    "Empowering agents to triage, reason, plan and report using real GitHub incidents.")

# === GitHub API: Fetch Incidents ===


def get_all_issues():
    owner = "kubernetes"
    repo = "kubernetes"
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100"
    headers = {"Accept": "application/vnd.github.v3+json"}
    issue_list = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        issues = response.json()
        for issue in issues:
            if not issue.get("pull_request"):
                title = issue.get("title", "")
                body = issue.get("body", "")
                full_text = f"{title}\n{body}"
                issue_list.append((title, full_text))
    except requests.exceptions.RequestException as e:
        st.error(f"GitHub fetch failed: {e}")
    return issue_list


all_issues = get_all_issues()
titles = [title for title, _ in all_issues]

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🔍 Select & Preview Incident")
    selected_title = st.selectbox("Pick a GitHub Issue", titles)
    issue_description = next(
        (full for title, full in all_issues if title == selected_title), "")
    st.session_state["issue_description"] = issue_description

    if st.button("Preview Incident"):
        st.code(issue_description)

    st.markdown("### Agent Actions")
    with st.container(border=True):

        if st.button("Run Retriever Agent", use_container_width=True):
            with st.spinner("Running Retriever Agent..."):
                st.session_state["retriever_result"] = run_retriever(
                    issue_description, all_issues)

        if st.button("Run Analyzer Agent", use_container_width=True):
            with st.spinner("Running Analyzer Agent..."):
                st.session_state["analyzer_result"] = run_analyzer(
                    st.session_state.get("retriever_result", {}))

        if st.button("Run Planner Agent", use_container_width=True):
            with st.spinner("Running Planner Agent..."):
                st.session_state["planner_result"] = run_planner(
                    st.session_state.get("analyzer_result", {}))

        if st.button("Run Reporter Agent", use_container_width=True):
            with st.spinner("Running Reporter Agent..."):
                st.session_state["reporter_result"] = run_reporter(
                    st.session_state.get("planner_result", {}))

        if st.button("🚀 Run CognOps Crew", use_container_width=True):
            st.session_state["crew_done"] = False
            st.session_state["crew_error"] = None
            with st.spinner("Running Full CognOps Crew..."):
                try:
                    results = run_cognops_crew(issue_description, all_issues)
                    if results:
                        for k, v in results.items():
                            st.session_state[k] = v
                        st.session_state["crew_done"] = True
                except Exception as e:
                    st.session_state["crew_error"] = str(e)

    st.markdown("---")
    st.subheader("Chat with CognOps")
    user_question = st.text_input(
        "What do you want to ask?", placeholder="e.g., What went wrong with DNS?")
    if user_question:
        with st.spinner("Thinking..."):
            rag_context = st.session_state.get(
                "retriever_result", {}).get("context_snippets", [])
            analyzer_context = [st.session_state.get(
                "analyzer_result", {}).get("analysis", "")]
            all_context = rag_context + analyzer_context
            prompt_input = user_question + "\n\n" + \
                "\n".join([f"Context: {c}" for c in all_context])
            try:
                rag_response = call_llm(prompt_input)
                st.success("RAG + LLM Answer")
                st.markdown(rag_response)
            except Exception as e:
                st.error(f"Error during LLM call: {e}")

with col2:
    st.markdown("### 📄 Agent Outputs")

    if st.session_state.get("crew_error"):
        st.error(f"❌ Crew failed: {st.session_state['crew_error']}")
    elif st.session_state.get("crew_done"):
        st.success("✅ Crew execution complete!")

    if "retriever_result" in st.session_state:
        result = st.session_state["retriever_result"]
        st.subheader("🧫 Incident Summary")
        st.markdown(result.get("summary", "No summary available."))
        snippets = result.get("context_snippets", [])
        sources = result.get("sources", [])
        scores = result.get("confidence_scores", [])
        if snippets:
            with st.expander("ℹ️ How to interpret confidence scores", expanded=False):
                st.markdown("""
                                **Confidence Score Interpretation **

                                > *Note: These scores are based on vector similarity(lower=more similar) *

                                - **0.0 – 0.4 ** → 🔥 **Very High Relevance **
                                Strong semantic overlap with your issue description.

                                - **0.41 – 0.6 ** → ✅ **High Relevance **
                                Conceptually aligned with partial keyword/context match.

                                - **0.61 – 0.8 ** → ⚠️ **Moderate Relevance **
                                Some connection, but may differ in scope or cause.

                                - **0.81 – 1.0 ** → ❓ **Low Relevance **
                                Potentially related but with weak similarity.

                                - ** > 1.0 ** → 🚫 **Very Low Relevance **
                                Likely unrelated or semantically distant.

                                These scores come from semantic embeddings(MiniLM) and represent distance in vector space. Lower is better.
                                """)
            st.subheader("📚 Retrieved Contexts")
            for i, (snippet, source, score) in enumerate(zip(snippets, sources, scores), start=1):
                st.markdown(
                    f"**{i}. Source:** `{source}` — **Confidence:** `{score:.2f}`")
                st.code(snippet[:300] + ("..." if len(snippet) > 300 else ""))
        if result.get("extra_info"):
            st.subheader("🧾 Anything else we need to know?")
            st.markdown(result["extra_info"])

    if "analyzer_result" in st.session_state:
        st.subheader("🔍 Analysis")
        analysis_json = st.session_state["analyzer_result"].get(
            "analysis", "{}")
        try:
            parsed = json.loads(analysis_json)
            st.json(parsed)
        except:
            st.markdown(analysis_json)

    if "planner_result" in st.session_state:
        st.subheader("Plan of Action")
        st.markdown(st.session_state["planner_result"].get(
            "plan", "No plan available."))

    if "reporter_result" in st.session_state:
        st.subheader("Incident Report")
        st.markdown(st.session_state["reporter_result"].get(
            "report", "No report available."))
