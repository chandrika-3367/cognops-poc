# === TEMP: Commented until tools are available ===
# from crew.run_cognops_crew import run_cognops_crew
# from agents.reporter.reporter_agent import run_reporter
# from agents.planner.planner_agent import run_planner

import streamlit as st
import requests
import builtins
from typing import List
from agents.retriever_agent import run_retriever
from tools.rag import dynamic_rag_qa
from tools.log_utils import log_agent_event, log_error
from tools.llm import call_llm
from agents.analyzer_agent import run_analyzer

# UI Setup
st.set_page_config(page_title="CognOps – AI Ops Panel", layout="wide")
st.title(" CognOps – AI Incident Response Mesh")
st.markdown(
    "Empowering agents to triage, reason, plan and report using real GitHub incidents.")

# GitHub API: Fetch Incidents


def get_all_issues():
    owner = "kubernetes"
    repo = "kubernetes"
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    issue_list = []
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            if not issue.get("pull_request"):
                title = issue['title']
                body = issue.get('body', '')
                full_text = f"{title}\n{body}"
                issue_list.append((title, full_text))
    return issue_list


# === Incident Selection UI ===
all_issues = get_all_issues()
titles = [title for title, _ in all_issues]

with st.expander("🔍 Select & Preview Incident", expanded=True):
    selected_title = st.selectbox("Pick a live GitHub Incident", titles)
    query = builtins.next(
        (full for title, full in all_issues if title == selected_title), "")
    st.session_state["issue_description"] = query

    if st.button("Preview Incident"):
        st.code(query, language="text")

# === Agent UI Layout ===
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Agent Actions")
    with st.container(border=True):
        if st.button("Run Retriever Agent"):
            with st.spinner("Running Retriever Agent..."):
                st.session_state["retriever_result"] = run_retriever(
                    st.session_state.get("issue_description", ""),
                    all_issues
                )

        if st.button("Run Analyzer Agent"):
            with st.spinner("Running Analyzer Agent..."):
                st.session_state["analyzer_result"] = run_analyzer(
                    st.session_state.get("retriever_result", {})
                )

        if st.button("Run Planner Agent"):
            with st.spinner("Running Planner Agent..."):
                st.session_state["planner_result"] = run_planner(
                    st.session_state.get("analyzer_result", {})
                )

        if st.button("Run Reporter Agent"):
            with st.spinner("Running Reporter Agent..."):
                st.session_state["reporter_result"] = run_reporter(
                    st.session_state.get("planner_result", {})
                )

    # 🔍 Ask Questions Chatbox (always present)
    st.markdown("---")
    st.subheader("Chat with CognOps")
    # Ask Questions Chatbox
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

    if "retriever_result" in st.session_state:
        result = st.session_state["retriever_result"]

        st.subheader("🧠 Incident Summary")
        st.markdown(result.get("summary", "No summary available."))

        snippets = result.get("context_snippets", [])
        sources = result.get("sources", [])
        scores = result.get("confidence_scores", [])

        if snippets:
            st.subheader("📚 Retrieved Contexts")
            for i, (snippet, source, score) in enumerate(zip(snippets, sources, scores), start=1):
                st.markdown(
                    f"**{i}. Source:** `{source}` — **Confidence:** `{score:.2f}`")
                st.code(snippet[:300] + ("..." if len(snippet) > 300 else ""))

        st.markdown("---")
        if result.get("extra_info"):
            st.subheader("🧾 Anything else we need to know?")
            st.markdown(result["extra_info"])

    if "analyzer_result" in st.session_state:
        st.subheader("🔍 Analysis")
        analysis_json = st.session_state["analyzer_result"].get(
            "analysis", "{}")
        try:
            import json
            parsed = json.loads(analysis_json)
            st.json(parsed)
        except:
            st.markdown(analysis_json)

    if "planner_result" in st.session_state:
        st.subheader("🛠️ Plan of Action")
        st.markdown(st.session_state["planner_result"].get(
            "plan", "No plan available."))

    if "reporter_result" in st.session_state:
        st.subheader("📢 Incident Report")
        st.markdown(st.session_state["reporter_result"].get(
            "report", "No report available."))
