import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="research_pipeline",
    page_icon="//",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background-color: #0d0d0d !important;
    color: #00ff88 !important;
}

.stApp { background-color: #0d0d0d !important; }

section[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid #1a1a1a !important;
}
section[data-testid="stSidebar"] * { color: #00ff88 !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #2a8a5a !important; font-size: 11px !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
    color: #00ff88 !important; letter-spacing: 2px !important; font-size: 13px !important;
}

.stTextInput > div > div > input {
    background-color: #080808 !important;
    border: 1px solid #1f3a2a !important;
    color: #00ff88 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 4px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 1px #00ff88 !important;
}
.stTextInput label { color: #2a8a5a !important; font-size: 11px !important; letter-spacing: 1px !important; }

.stButton > button {
    background-color: #003a1a !important;
    border: 1px solid #00ff88 !important;
    color: #00ff88 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
    padding: 10px 24px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background-color: #005a28 !important; }
.stButton > button:disabled { opacity: 0.3 !important; cursor: not-allowed !important; }

.stSlider > div > div > div > div { background-color: #00ff88 !important; }
.stSlider label { color: #2a8a5a !important; font-size: 11px !important; letter-spacing: 1px !important; }

.stStatus {
    background-color: #080808 !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 6px !important;
    color: #00ff88 !important;
}
.stStatus [data-testid="stStatusLabel"] { color: #00ff88 !important; font-size: 12px !important; }

.stExpander {
    background-color: #080808 !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 6px !important;
}
.stExpander summary { color: #2a8a5a !important; font-size: 11px !important; }

.stMarkdown h1 { color: #00ff88 !important; font-size: 22px !important; letter-spacing: 2px !important; margin-bottom: 4px !important; }
.stMarkdown h2 { color: #00cc66 !important; font-size: 14px !important; letter-spacing: 1px !important; border-bottom: 1px solid #1a3a2a !important; padding-bottom: 6px !important; }
.stMarkdown p, .stMarkdown li { color: #009944 !important; font-size: 12px !important; line-height: 1.8 !important; }
.stMarkdown code { background: #080808 !important; color: #00ff88 !important; border: 1px solid #1a3a2a !important; font-size: 11px !important; }

.stSuccess {
    background-color: #001a0a !important;
    border: 1px solid #00ff88 !important;
    border-radius: 4px !important;
    color: #00ff88 !important;
}

div[data-testid="stDownloadButton"] button {
    background-color: #080808 !important;
    border: 1px solid #1f3a2a !important;
    color: #2a8a5a !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
div[data-testid="stDownloadButton"] button:hover { border-color: #00ff88 !important; color: #00ff88 !important; }

hr { border-color: #1a1a1a !important; }

.terminal-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #1a4a2a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 24px;
}
.step-card {
    background: #080808;
    border: 1px solid #1a1a1a;
    border-radius: 6px;
    padding: 12px;
}
.step-card.done { border-color: #00ff88; }
.step-num { font-size: 9px; color: #1a4a2a; letter-spacing: 1px; margin-bottom: 4px; }
.step-name { font-size: 12px; color: #00ff88; margin-bottom: 2px; }
.step-desc { font-size: 10px; color: #1a4a2a; }
</style>
""", unsafe_allow_html=True)


def extract_text(result):
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


with st.sidebar:
    st.markdown("### // research_pipeline")
    st.markdown("multi-agent pipeline v2.0")
    st.divider()
    st.markdown("""
**01** `search_agent` — finds sources  
**02** `reader_agent` — scrapes best source  
**03** `writer_chain` — drafts report  
**04** `critic_chain` — reviews output  
""")
    st.divider()
    scrape_chars = st.slider("context window (chars)", 200, 2000, 800, 100)


st.markdown("# > research_pipeline")
st.markdown('<p style="color:#1a5a2a;font-size:11px;letter-spacing:1px;margin-bottom:20px">enter topic and execute pipeline_</p>', unsafe_allow_html=True)

topic = st.text_input("$ topic:", placeholder="e.g. impact of AI on global chip supply chains")
run_clicked = st.button("[ run pipeline ]", type="primary", disabled=not topic.strip())

if "step_done" not in st.session_state:
    st.session_state.step_done = [False, False, False, False]

def render_pipeline_grid(done):
    steps = [
        ("STEP 01", "search", "web query execution"),
        ("STEP 02", "reader", "url scraping"),
        ("STEP 03", "writer", "report synthesis"),
        ("STEP 04", "critic", "quality review"),
    ]
    cols = st.columns(4)
    for i, (num, name, desc) in enumerate(steps):
        cls = "step-card done" if done[i] else "step-card"
        indicator = "▣" if done[i] else "▢"
        cols[i].markdown(f"""
<div class="{cls}">
  <div class="step-num">{num}</div>
  <div class="step-name">{name}</div>
  <div class="step-desc">{desc}</div>
  <div style="margin-top:8px;font-size:14px;color:{'#00ff88' if done[i] else '#1a4a2a'}">{indicator}</div>
</div>""", unsafe_allow_html=True)

render_pipeline_grid(st.session_state.step_done)

if run_clicked:
    state = {}
    st.session_state.step_done = [False, False, False, False]

    with st.status("[ step 01 ] search_agent running...", expanded=True) as status:
        try:
            search_agent = get_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = extract_text(search_result)
            st.code(state["search_results"], language=None)
            st.session_state.step_done[0] = True
            status.update(label="[ step 01 ] search_agent — done ✓", state="complete")
        except Exception as e:
            status.update(label="[ step 01 ] search_agent — error ✗", state="error")
            st.exception(e)
            st.stop()

    with st.status("[ step 02 ] reader_agent scraping...", expanded=True) as status:
        try:
            reader_agent = get_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:scrape_chars]}",
                )]
            })
            state["scraped_content"] = extract_text(reader_result)
            st.code(state["scraped_content"], language=None)
            st.session_state.step_done[1] = True
            status.update(label="[ step 02 ] reader_agent — done ✓", state="complete")
        except Exception as e:
            status.update(label="[ step 02 ] reader_agent — error ✗", state="error")
            st.exception(e)
            st.stop()

    with st.status("[ step 03 ] writer_chain drafting...", expanded=True) as status:
        try:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            report_result = writer_chain.invoke({"topic": topic, "research": research_combined})
            state["report"] = extract_text(report_result)
            st.markdown(state["report"])
            st.session_state.step_done[2] = True
            status.update(label="[ step 03 ] writer_chain — done ✓", state="complete")
        except Exception as e:
            status.update(label="[ step 03 ] writer_chain — error ✗", state="error")
            st.exception(e)
            st.stop()

    with st.status("[ step 04 ] critic_chain reviewing...", expanded=True) as status:
        try:
            feedback_result = critic_chain.invoke({"report": state["report"]})
            state["feedback"] = extract_text(feedback_result)
            st.markdown(state["feedback"])
            st.session_state.step_done[3] = True
            status.update(label="[ step 04 ] critic_chain — done ✓", state="complete")
        except Exception as e:
            status.update(label="[ step 04 ] critic_chain — error ✗", state="error")
            st.exception(e)
            st.stop()

    st.success("// pipeline complete. all agents finished.")
    render_pipeline_grid(st.session_state.step_done)

    st.markdown("## // final report")
    st.markdown(state["report"])

    st.markdown("## // critic feedback")
    st.markdown(state["feedback"])

    st.download_button(
        "[ download report.md ]",
        data=state["report"],
        file_name=f"{topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
    )

    with st.expander("// raw search output"):
        st.code(state["search_results"], language=None)
    with st.expander("// raw scraped content"):
        st.code(state["scraped_content"], language=None)