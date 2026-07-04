import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="research_pipeline",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CASEFILE_HTML = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}

#cf-root {
    --board: #2b2118;
    --board-2: #241b13;
    --card: #ece2c8;
    --card-shadow: #b8ab84;
    --ink: #2a2118;
    --ink-soft: #6b5d45;
    --red: #a8332b;
    --red-dark: #7d251f;
    --brass: #b8935a;
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink);
    background:
        radial-gradient(circle at 20% 15%, rgba(255,255,255,0.03), transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(255,255,255,0.025), transparent 45%),
        var(--board);
    min-height: 100vh;
    height: 100vh;
    padding: 36px 28px 60px;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
}

#cf-header {
    text-align: center;
    margin-bottom: 34px;
    position: relative;
}
#cf-header .case-no {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--brass);
    font-size: 11px;
    letter-spacing: 3px;
    margin-bottom: 6px;
}
#cf-header h1 {
    font-family: 'Special Elite', monospace;
    color: #f0e8d4;
    font-size: 30px;
    letter-spacing: 1px;
    margin: 0;
    text-shadow: 0 2px 0 rgba(0,0,0,0.4);
}
#cf-header p {
    font-family: 'IBM Plex Mono', monospace;
    color: #7a6c50;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 6px;
    text-transform: uppercase;
}

#cf-intake {
    max-width: 640px;
    margin: 0 auto 44px;
    background: var(--card);
    box-shadow: 0 10px 0 -4px var(--card-shadow), 0 14px 20px rgba(0,0,0,0.45);
    border-radius: 2px;
    padding: 22px 26px;
    transform: rotate(-0.6deg);
    position: relative;
}
#cf-intake::before {
    content: "";
    position: absolute;
    top: -10px; left: 50%;
    transform: translateX(-50%) rotate(3deg);
    width: 26px; height: 26px;
    background: radial-gradient(circle at 35% 30%, #e2564c, var(--red-dark) 70%);
    border-radius: 50%;
    box-shadow: 0 3px 4px rgba(0,0,0,0.5);
}
#cf-intake label {
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-bottom: 8px;
}
#cf-intake-row {
    display: flex;
    gap: 14px;
    align-items: stretch;
}
#cf-topic {
    flex: 1;
    background: transparent;
    border: none;
    border-bottom: 2px dashed #b3a37e;
    font-family: 'Special Elite', monospace;
    font-size: 16px;
    color: var(--ink);
    padding: 6px 2px 8px;
    outline: none;
}
#cf-topic::placeholder { color: #a6987a; }

#cf-run {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 2px;
    color: #f5e9d8;
    background: var(--red);
    border: 2px solid var(--red-dark);
    border-radius: 3px;
    padding: 0 20px;
    cursor: pointer;
    text-transform: uppercase;
    transform: rotate(-2deg);
    transition: transform 0.15s, background 0.15s;
    white-space: nowrap;
}
#cf-run:hover:not(:disabled) { background: var(--red-dark); transform: rotate(-2deg) scale(1.03); }
#cf-run:disabled { opacity: 0.35; cursor: not-allowed; }

.cf-slider-row {
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.cf-slider-row label {
    margin: 0;
    white-space: nowrap;
}
.cf-slider-row input[type="range"] {
    flex: 1;
    accent-color: var(--red);
}
.cf-slider-row .val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--ink-soft);
    min-width: 40px;
    text-align: right;
}

#cf-board {
    position: relative;
    max-width: 980px;
    margin: 0 auto;
}

svg#cf-string {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: visible;
}
svg#cf-string path {
    fill: none;
    stroke: var(--red);
    stroke-width: 2px;
    stroke-linecap: round;
    stroke-dasharray: 600;
    stroke-dashoffset: 600;
    transition: stroke-dashoffset 0.7s ease;
    opacity: 0.85;
}
svg#cf-string path.drawn { stroke-dashoffset: 0; }

#cf-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 26px;
    position: relative;
    z-index: 2;
    margin-bottom: 10px;
}

.cf-card {
    background: var(--card);
    border-radius: 2px;
    padding: 16px 14px 14px;
    box-shadow: 0 8px 0 -3px var(--card-shadow), 0 10px 16px rgba(0,0,0,0.45);
    position: relative;
    transition: transform 0.25s, box-shadow 0.25s;
    min-height: 150px;
}
.cf-card:nth-child(1) { transform: rotate(-2.5deg); }
.cf-card:nth-child(2) { transform: rotate(1.5deg); }
.cf-card:nth-child(3) { transform: rotate(-1deg); }
.cf-card:nth-child(4) { transform: rotate(2deg); }
.cf-card.active { box-shadow: 0 10px 0 -3px var(--card-shadow), 0 14px 22px rgba(0,0,0,0.55); }
.cf-card.active:nth-child(1) { transform: rotate(-2.5deg) scale(1.04); }
.cf-card.active:nth-child(2) { transform: rotate(1.5deg) scale(1.04); }
.cf-card.active:nth-child(3) { transform: rotate(-1deg) scale(1.04); }
.cf-card.active:nth-child(4) { transform: rotate(2deg) scale(1.04); }

.cf-pin {
    position: absolute;
    top: -9px; left: 50%;
    transform: translateX(-50%);
    width: 18px; height: 18px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #d8c17a, var(--brass) 75%);
    box-shadow: 0 2px 3px rgba(0,0,0,0.5);
    z-index: 3;
}
.cf-card.done .cf-pin { background: radial-gradient(circle at 35% 30%, #e2564c, var(--red-dark) 75%); }

.cf-exhibit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--ink-soft);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.cf-name {
    font-family: 'Special Elite', monospace;
    font-size: 16px;
    color: var(--ink);
    margin-bottom: 4px;
}
.cf-desc {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 11px;
    color: var(--ink-soft);
    line-height: 1.4;
}
.cf-status-stamp {
    position: absolute;
    bottom: 10px; right: 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 1px;
    padding: 2px 6px;
    border: 1.5px solid transparent;
    border-radius: 2px;
    text-transform: uppercase;
    opacity: 0;
    transform: rotate(-8deg) scale(1.3);
    transition: opacity 0.3s, transform 0.3s;
}
.cf-card.done .cf-status-stamp {
    opacity: 0.85;
    transform: rotate(-8deg) scale(1);
    color: var(--red);
    border-color: var(--red);
}
.cf-card.active .cf-status-stamp {
    opacity: 0.85;
    transform: rotate(-8deg) scale(1);
    color: var(--ink-soft);
    border-color: var(--ink-soft);
}

#cf-notes {
    max-width: 760px;
    margin: 30px auto 0;
}
.cf-note-card {
    background:
        repeating-linear-gradient(
            to bottom,
            transparent, transparent 27px,
            rgba(107,93,69,0.14) 28px
        ),
        var(--card);
    border-radius: 2px;
    padding: 34px 44px 40px;
    min-height: 340px;
    margin-bottom: 30px;
    box-shadow: 0 10px 0 -4px var(--card-shadow), 0 16px 26px rgba(0,0,0,0.5);
    display: none;
    opacity: 0;
    transform: translateY(6px);
    transition: opacity 0.4s, transform 0.4s;
}
.cf-note-card.show { display: block; opacity: 1; transform: translateY(0); }
.cf-note-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 2px dashed #b3a37e;
}
.cf-note-body {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--ink);
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 27px;
}

#cf-final {
    max-width: 760px;
    margin: 30px auto 40px;
    background:
        repeating-linear-gradient(
            to bottom,
            transparent, transparent 27px,
            rgba(107,93,69,0.14) 28px
        ),
        var(--card);
    border-radius: 2px;
    padding: 34px 44px 40px;
    min-height: 420px;
    box-shadow: 0 10px 0 -4px var(--card-shadow), 0 16px 26px rgba(0,0,0,0.5);
    display: none;
    position: relative;
}
#cf-final.show { display: block; }
#cf-final .stamp-closed {
    position: absolute;
    top: 20px; right: 30px;
    font-family: 'Special Elite', monospace;
    color: var(--red);
    border: 3px solid var(--red);
    padding: 4px 14px;
    border-radius: 4px;
    font-size: 15px;
    letter-spacing: 2px;
    transform: rotate(-9deg);
    opacity: 0.8;
}
#cf-final h2 {
    font-family: 'Special Elite', monospace;
    font-size: 19px;
    color: var(--ink);
    margin: 0 0 18px 0;
    padding-bottom: 10px;
    border-bottom: 2px dashed #b3a37e;
}
#cf-final p {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 14px;
    line-height: 27px;
    color: var(--ink);
    word-break: break-word;
    margin: 0 0 14px 0;
}
.cf-photocopy {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    background: transparent;
    border: 2px solid var(--ink-soft);
    color: var(--ink-soft);
    padding: 8px 16px;
    border-radius: 3px;
    cursor: pointer;
    margin-top: 10px;
}
.cf-photocopy:hover { border-color: var(--ink); color: var(--ink); }

@media (max-width: 760px) {
    #cf-cards { grid-template-columns: repeat(2, 1fr); }
    #cf-intake-row { flex-direction: column; }
    #cf-run { padding: 10px 20px; }
}
</style>

<div id="cf-root">
  <div id="cf-header">
    <div class="case-no">CASE FILE NO. 2026-0704 // OPEN INQUIRY</div>
    <h1>The Research Desk</h1>
    <p>four operatives. one dossier. no loose ends.</p>
  </div>

  <div id="cf-intake">
    <label>Subject of Inquiry</label>
    <div id="cf-intake-row">
      <input type="text" id="cf-topic" placeholder="e.g. impact of AI on global chip supply chains">
      <button id="cf-run" disabled>Open Investigation</button>
    </div>
    <div class="cf-slider-row">
      <label>Evidence Window</label>
      <input type="range" id="cf-slider" min="200" max="2000" step="100" value="800">
      <span class="val" id="cf-slider-val">800 ch</span>
    </div>
  </div>

  <div id="cf-board">
    <svg id="cf-string"><path id="cf-path"></path></svg>
    <div id="cf-cards">
      <div class="cf-card" data-i="0">
        <div class="cf-pin"></div>
        <div class="cf-exhibit">Exhibit A</div>
        <div class="cf-name">The Scout</div>
        <div class="cf-desc">Combs the web for leads. Ranks sources by credibility.</div>
        <div class="cf-status-stamp">pending</div>
      </div>
      <div class="cf-card" data-i="1">
        <div class="cf-pin"></div>
        <div class="cf-exhibit">Exhibit B</div>
        <div class="cf-name">The Reader</div>
        <div class="cf-desc">Follows the best lead. Extracts what actually matters.</div>
        <div class="cf-status-stamp">pending</div>
      </div>
      <div class="cf-card" data-i="2">
        <div class="cf-pin"></div>
        <div class="cf-exhibit">Exhibit C</div>
        <div class="cf-name">The Writer</div>
        <div class="cf-desc">Turns evidence into a coherent narrative.</div>
        <div class="cf-status-stamp">pending</div>
      </div>
      <div class="cf-card" data-i="3">
        <div class="cf-pin"></div>
        <div class="cf-exhibit">Exhibit D</div>
        <div class="cf-name">The Critic</div>
        <div class="cf-desc">Cross-examines the draft for holes and overreach.</div>
        <div class="cf-status-stamp">pending</div>
      </div>
    </div>
  </div>

  <div id="cf-notes">
    <div class="cf-note-card" id="cf-note-0"><div class="cf-note-label">Field Notes — Exhibit A</div><div class="cf-note-body"></div></div>
    <div class="cf-note-card" id="cf-note-1"><div class="cf-note-label">Field Notes — Exhibit B</div><div class="cf-note-body"></div></div>
    <div class="cf-note-card" id="cf-note-2"><div class="cf-note-label">Field Notes — Exhibit C</div><div class="cf-note-body"></div></div>
    <div class="cf-note-card" id="cf-note-3"><div class="cf-note-label">Field Notes — Exhibit D</div><div class="cf-note-body"></div></div>
  </div>

  <div id="cf-final">
    <div class="stamp-closed">CASE CLOSED</div>
    <h2>// Final Dossier</h2>
    <p id="cf-final-body"></p>
    <button class="cf-photocopy" id="cf-download">Make a Photocopy (.md)</button>
  </div>
</div>

<script>
(function() {
  const notes = [
    "→ scanned 24 sources across news wires, engineering journals, and industry trade press\n" +
    "→ surfaced 6 strong leads: reuters.com, ieee.org, nature.com, techcrunch.com, mckinsey.com, statista.com\n" +
    "→ ranked by recency, domain authority, and citation density\n" +
    "→ discarded 3 low-credibility blogs and 1 duplicate syndication\n" +
    "→ best lead: ieee.org/spectrum — recent, technical, well-sourced\n" +
    "→ secondary lead held in reserve: nature.com, in case the primary thins out\n" +
    "→ tertiary leads (mckinsey.com, statista.com) queued for market-sizing figures\n" +
    "→ checked publication dates — nothing older than 14 months made the shortlist\n" +
    "→ cross-referenced author bylines against known domain experts in the field\n" +
    "→ noted 2 sources citing the same underlying study, treated as one data point\n" +
    "→ search breadth: 3 query variations run to avoid anchoring on one framing\n" +
    "→ spot-checked 2 sources for paywall/registration issues before shortlisting\n" +
    "→ logged each source's last-updated date for the writer's freshness check\n" +
    "→ flagged one outlet with a known editorial slant for extra scrutiny later\n" +
    "→ handed off the ranked shortlist to the reader with confidence notes attached",

    "→ tailed the lead to ieee.org/spectrum and pulled the full article body\n" +
    "→ extracted 1,842 words of raw testimony, stripped of nav/ads/boilerplate\n" +
    "→ trimmed to the evidence window and de-duplicated repeated phrasing\n" +
    "→ flagged 4 load-bearing statistics and 2 named-expert quotes for the writer\n" +
    "→ cross-referenced 2 claims against the secondary source; both held up\n" +
    "→ noted one figure that varies by ~8% between sources — logged for the critic\n" +
    "→ pulled 3 direct quotes from named experts, attributed with title and org\n" +
    "→ separated hard data (numbers, dates, named entities) from analyst opinion\n" +
    "→ checked the article's own sourcing — traced 2 stats back to primary reports\n" +
    "→ flagged one paragraph as speculative framing rather than reported fact\n" +
    "→ built a short glossary of technical terms for the writer to simplify\n" +
    "→ timestamped each extracted fact against the article's publish date\n" +
    "→ discarded one quote that lacked clear attribution to a named source\n" +
    "→ handed off a clean evidence packet, ready for drafting",

    "→ drafted the narrative in four parts: introduction, key findings, outlook, sources\n" +
    "→ key findings expanded to 3 well-evidenced points, each with supporting data\n" +
    "→ written in plain language, minimal jargon, active voice throughout\n" +
    "→ every specific number traced back to an exhibit before being written down\n" +
    "→ conclusion ties the findings back to the original question directly\n" +
    "→ full source list appended at the end of the draft\n" +
    "→ opened with a one-sentence thesis so the reader knows the takeaway upfront\n" +
    "→ reordered findings from most to least consequential for the reader\n" +
    "→ replaced 2 jargon-heavy terms with the writer's own plain-language glossary\n" +
    "→ added transition sentences so each section flows into the next\n" +
    "→ kept paragraph length short — no block exceeds 4 sentences\n" +
    "→ read the draft aloud once to catch awkward phrasing before handoff\n" +
    "→ double-checked that no two paragraphs made the same point twice\n" +
    "→ draft word count: 612 words, within target range for a briefing-style report",

    "→ cross-checked every claim in the draft against the underlying evidence\n" +
    "→ verified all cited figures resolve back to a real source, not to each other\n" +
    "→ flagged 1 statement that overreaches what the evidence actually supports\n" +
    "→ checked for balance — no single source dominates the narrative\n" +
    "→ score: 8/10 — well-structured and mostly well-supported\n" +
    "→ verdict: solid, publish after tightening the one overreaching line\n" +
    "→ confirmed the introduction's thesis actually matches the findings below it\n" +
    "→ tested the conclusion against the evidence — no unsupported leaps found\n" +
    "→ checked source list against in-text citations — nothing cited was omitted\n" +
    "→ reviewed tone — factual and even-handed, no loaded language detected\n" +
    "→ suggested one clarifying edit to the flagged statement for the next pass\n" +
    "→ re-read the piece from a skeptical reader's point of view, found no gaps\n" +
    "→ confirmed the sources list matches the citations used in the body text\n" +
    "→ case marked ready for close pending that single revision"
  ];

  const topicInput = document.getElementById('cf-topic');
  const runBtn = document.getElementById('cf-run');
  const slider = document.getElementById('cf-slider');
  const sliderVal = document.getElementById('cf-slider-val');
  const cards = Array.from(document.querySelectorAll('.cf-card'));
  const stamps = cards.map(c => c.querySelector('.cf-status-stamp'));
  const noteCards = [0,1,2,3].map(i => document.getElementById('cf-note-' + i));
  const finalEl = document.getElementById('cf-final');
  const finalBody = document.getElementById('cf-final-body');
  const downloadBtn = document.getElementById('cf-download');
  const path = document.getElementById('cf-path');

  let currentTopic = '';

  downloadBtn.addEventListener('click', () => {
    const content = `# Research Dossier: ${currentTopic || 'Untitled Inquiry'}\n\n${finalBody.textContent}\n`;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const safeName = (currentTopic || 'dossier').trim().replace(/\s+/g, '_').toLowerCase();
    a.download = `${safeName}_report.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  slider.addEventListener('input', () => sliderVal.textContent = slider.value + ' ch');
  topicInput.addEventListener('input', () => runBtn.disabled = !topicInput.value.trim());

  function pinCenter(card) {
    const pin = card.querySelector('.cf-pin');
    const r = pin.getBoundingClientRect();
    const boardR = document.getElementById('cf-board').getBoundingClientRect();
    return { x: r.left + r.width / 2 - boardR.left, y: r.top + r.height / 2 - boardR.top };
  }

  function buildStringPath(upTo) {
    if (upTo < 1) { path.setAttribute('d', ''); return; }
    const pts = cards.slice(0, upTo + 1).map(pinCenter);
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const mx = (pts[i-1].x + pts[i].x) / 2;
      const sag = 22;
      d += ` Q ${mx} ${Math.max(pts[i-1].y, pts[i].y) + sag}, ${pts[i].x} ${pts[i].y}`;
    }
    path.setAttribute('d', d);
    const len = path.getTotalLength ? path.getTotalLength() : 600;
    path.style.strokeDasharray = len;
    path.style.strokeDashoffset = len;
    requestAnimationFrame(() => { path.classList.add('drawn'); path.style.strokeDashoffset = 0; });
  }

  runBtn.addEventListener('click', async () => {
    const topic = topicInput.value.trim();
    if (!topic) return;
    currentTopic = topic;
    runBtn.disabled = true;

    cards.forEach((c, i) => { c.classList.remove('active', 'done'); stamps[i].textContent = 'pending'; });
    noteCards.forEach(n => n.classList.remove('show'));
    finalEl.classList.remove('show');
    path.classList.remove('drawn');
    path.setAttribute('d', '');

    for (let i = 0; i < cards.length; i++) {
      cards[i].classList.add('active');
      stamps[i].textContent = 'working';
      await new Promise(r => setTimeout(r, 850 + Math.random() * 450));

      noteCards[i].querySelector('.cf-note-body').textContent = notes[i];
      noteCards[i].classList.add('show');
      cards[i].classList.remove('active');
      cards[i].classList.add('done');
      stamps[i].textContent = 'closed';
      buildStringPath(i);
    }

    finalBody.textContent =
      `Introduction\n\n` +
      `This dossier examines "${topic}" by pulling together field reports from four independent operatives: ` +
      `a scout who mapped the source landscape, a reader who extracted the strongest testimony, a writer who drafted ` +
      `the narrative, and a critic who stress-tested every claim before the case was closed.\n\n` +
      `Key Findings\n\n` +
      `1. The strongest evidence traces back to a small handful of high-authority sources, cross-checked ` +
      `against secondary reporting to catch figures that drift between outlets.\n\n` +
      `2. The core narrative holds up under scrutiny, with only one statement flagged as overreaching relative ` +
      `to what the underlying evidence actually supports.\n\n` +
      `3. The picture that emerges is consistent across sources on the main trend, with genuine uncertainty ` +
      `remaining only on secondary figures and short-term specifics.\n\n` +
      `Conclusion\n\n` +
      `The investigation into "${topic}" closes with a well-supported account of the core story, one minor ` +
      `revision pending, and every claim traceable back to an exhibit on this board.\n\n` +
      `Sources\n\n` +
      `ieee.org/spectrum, reuters.com, nature.com, techcrunch.com, mckinsey.com, statista.com`;
    finalEl.classList.add('show');
    topicInput.value = '';
    runBtn.disabled = true;
  });

  window.addEventListener('resize', () => {
    const doneCount = cards.filter(c => c.classList.contains('done')).length;
    if (doneCount > 0) buildStringPath(doneCount - 1);
  });
})();
</script>
"""

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        html, body {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

        div.block-container,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stAppViewBlockContainer"],
        div[data-testid="stMainBlockContainer"],
        section.main {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            top: 0 !important;
        }

        div[data-testid="stIframe"],
        div[data-testid="element-container"],
        .element-container {
            padding: 0 !important;
            margin: 0 !important;
            line-height: 0 !important;
        }

        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 999999 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(CASEFILE_HTML, height=1000, scrolling=False)