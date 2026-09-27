"""Streamlit interface for the multi-agent research pipeline.

Run from the project root with:
    streamlit run main.py
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import streamlit as st

try:
    from src.pipelines.pipelines import research_pipeline
except ModuleNotFoundError as exc:
    # Keep the page usable enough to explain setup when dependencies are absent.
    research_pipeline = None
    missing_package = exc.name
else:
    missing_package = None


st.set_page_config(
    page_title="Multi-Agent Research",
    page_icon="🔎",
    layout="wide",
)


def as_text(value: Any) -> str:
    """Normalize LangChain output objects and plain strings for display."""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        return str(value.content)
    return str(value)


def report_download(topic: str, result: dict[str, Any]) -> str:
    """Create a portable Markdown record of a completed research run."""
    sections = [
        f"# Research report: {topic}",
        f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "## Final report",
        as_text(result.get("report", "")),
        "## Critic review",
        as_text(result.get("feedback", "")),
        "## Selected sources",
        as_text(result.get("search_results", "")),
        "## Scraped research",
        as_text(result.get("scraped_content", "")),
    ]
    return "\n\n".join(sections)


def show_results(topic: str, result: dict[str, Any]) -> None:
    """Render the result from each stage of the research pipeline."""
    st.success("Research run complete.")

    report, critique, sources, scraped = st.tabs(
        ["Research Report", "Critic Review", "Selected Sources", "Scraped Content"]
    )
    with report:
        st.markdown(as_text(result.get("report", "No report was returned.")))
    with critique:
        st.markdown(as_text(result.get("feedback", "No critique was returned.")))
    with sources:
        st.text(as_text(result.get("search_results", "No search results were returned.")))
    with scraped:
        st.text_area(
            "Content gathered by the scraping agent",
            value=as_text(result.get("scraped_content", "No scraped content was returned.")),
            height=420,
            disabled=True,
            label_visibility="collapsed",
        )

    markdown_record = report_download(topic, result)
    st.download_button(
        "Download research as Markdown",
        data=markdown_record,
        file_name="research-report.md",
        mime="text/markdown",
    )
    with st.expander("Raw pipeline response"):
        st.code(json.dumps({key: as_text(value) for key, value in result.items()}, indent=2))


st.title("🔎 Multi-Agent Research System")
st.caption("Search, scrape, write, and critique a research report in one run.")

if missing_package:
    st.error(f"Missing Python package: `{missing_package}`")
    st.info(
        "Install this project's dependencies into the same Python environment "
        "that runs Streamlit, then restart the app."
    )

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Search agent finds credible sources.\n"
        "2. Scraping agent gathers deeper context.\n"
        "3. Writer produces a structured report.\n"
        "4. Critic reviews the result."
    )

topic = st.text_area(
    "What would you like to research?",
    placeholder="Example: The latest developments in renewable energy storage",
    height=110,
)

if st.button("Start research", type="primary", use_container_width=True, disabled=missing_package is not None):
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        st.warning("Enter a research topic before starting.")
    else:
        try:
            with st.status("Agents are researching your topic…", expanded=True) as status:
                st.write("Searching for credible sources and gathering detailed content.")
                result = research_pipeline(cleaned_topic)
                st.write("Writing the report and reviewing it for quality.")
                status.update(label="Research complete", state="complete", expanded=False)
            st.session_state.latest_research = {"topic": cleaned_topic, "result": result}
        except Exception as exc:
            st.error("The research run could not be completed.")
            st.exception(exc)

if saved_run := st.session_state.get("latest_research"):
    st.divider()
    show_results(saved_run["topic"], saved_run["result"])