"""
Streamlit UI for the multi-agent research pipeline.

Drop this file in your project root (same folder as agents.py, pipeline.py,
tools.py) and run:

    streamlit run streamlit_app.py
"""

import os
import sys

import streamlit as st

# Make sure local modules (agents.py, tools.py) are importable regardless
# of where streamlit is launched from.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


st.set_page_config(page_title="Multi-Agent Research Pipeline", page_icon="🔎", layout="wide")


def extract_text(result):
    """Pull plain text out of whatever an agent/chain hands back.

    LangGraph agents usually return {"messages": [...]} where the last
    message has a .content attribute. Chains built with LCEL often return
    either a plain string or an object with .content. This helper handles
    all of those without caring which one you actually get.
    """
    if result is None:
        return ""
    if hasattr(result, "content"):
        return result.content
    if isinstance(result, dict):
        if "messages" in result:
            return extract_text(result["messages"][-1])
        if "content" in result:
            return result["content"]
    return str(result)


@st.cache_resource(show_spinner=False)
def get_search_agent():
    return build_search_agent()


@st.cache_resource(show_spinner=False)
def get_reader_agent():
    return build_reader_agent()


# ---------------------------------------------------------------- sidebar --
with st.sidebar:
    st.title("🔎 Multi-Agent Research")
    st.markdown(
        "This app runs a 4-agent pipeline:\n\n"
        "1. **Search Agent** – finds sources\n"
        "2. **Reader Agent** – scrapes the best source\n"
        "3. **Writer** – drafts a report\n"
        "4. **Critic** – reviews the report\n"
    )
    st.divider()
    scrape_chars = st.slider(
        "Search context passed to the reader agent (chars)", 200, 2000, 800, 100
    )

# ------------------------------------------------------------------- main --
st.title("Multi-Agent Research Pipeline")

topic = st.text_input(
    "Research topic", placeholder="e.g. Impact of oil prices on global shipping"
)
run_clicked = st.button("Run pipeline", type="primary", disabled=not topic.strip())

if run_clicked:
    state = {}

    # ---- Step 1: Search -----------------------------------------------
    with st.status("Step 1 — Search agent is working...", expanded=True) as status:
        try:
            search_agent = get_search_agent()
            search_result = search_agent.invoke(
                {
                    "messages": [
                        ("user", f"Find recent, reliable and detailed information about: {topic}")
                    ]
                }
            )
            state["search_results"] = extract_text(search_result)
            st.write(state["search_results"])
            status.update(label="Step 1 — Search complete", state="complete")
        except Exception as e:
            status.update(label="Step 1 — Search failed", state="error")
            st.exception(e)
            st.stop()

    # ---- Step 2: Reader -------------------------------------------------
    with st.status("Step 2 — Reader agent is scraping the top source...", expanded=True) as status:
        try:
            reader_agent = get_reader_agent()
            reader_result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Based on the following search results about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{state['search_results'][:scrape_chars]}",
                        )
                    ]
                }
            )
            state["scraped_content"] = extract_text(reader_result)
            st.write(state["scraped_content"])
            status.update(label="Step 2 — Scraping complete", state="complete")
        except Exception as e:
            status.update(label="Step 2 — Scraping failed", state="error")
            st.exception(e)
            st.stop()

    # ---- Step 3: Writer --------------------------------------------------
    with st.status("Step 3 — Writer is drafting the report...", expanded=True) as status:
        try:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            report_result = writer_chain.invoke({"topic": topic, "research": research_combined})
            state["report"] = extract_text(report_result)
            st.markdown(state["report"])
            status.update(label="Step 3 — Report drafted", state="complete")
        except Exception as e:
            status.update(label="Step 3 — Writing failed", state="error")
            st.exception(e)
            st.stop()

    # ---- Step 4: Critic ---------------------------------------------------
    with st.status("Step 4 — Critic is reviewing the report...", expanded=True) as status:
        try:
            feedback_result = critic_chain.invoke({"report": state["report"]})
            state["feedback"] = extract_text(feedback_result)
            st.markdown(state["feedback"])
            status.update(label="Step 4 — Review complete", state="complete")
        except Exception as e:
            status.update(label="Step 4 — Review failed", state="error")
            st.exception(e)
            st.stop()

    st.success("Pipeline finished!")

    st.subheader("📄 Final Report")
    st.markdown(state["report"])

    st.subheader("🧐 Critic Feedback")
    st.markdown(state["feedback"])

    st.download_button(
        "Download report (Markdown)",
        data=state["report"],
        file_name=f"{topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
    )

    with st.expander("Raw search results"):
        st.write(state["search_results"])
    with st.expander("Raw scraped content"):
        st.write(state["scraped_content"])