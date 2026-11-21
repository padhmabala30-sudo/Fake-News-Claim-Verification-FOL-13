"""
Chatbot Interface for Fake News Claim Verification System
Uses Streamlit chat UI + FOL inference + Explainable AI
"""

import streamlit as st
from knowledge_base import KnowledgeBase
from claim_processor import ClaimProcessor
from inference_engine import FOLInferenceEngine
from xai_explainer import XAIExplainer

st.set_page_config(
    page_title="Fake News Verification Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .status-consistent { color: #155724; font-weight: 700; }
    .status-inconsistent { color: #721c24; font-weight: 700; }
    .status-unknown { color: #856404; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ---------- Init session state ----------
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase()
if "processor" not in st.session_state:
    st.session_state.processor = ClaimProcessor()
if "engine" not in st.session_state:
    st.session_state.engine = FOLInferenceEngine(st.session_state.kb)
if "explainer" not in st.session_state:
    st.session_state.explainer = XAIExplainer(st.session_state.kb)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am the **Fake News Claim Verification Chatbot**.\n\n"
                "I use **First-Order Logic (FOL)** and an advanced Knowledge Base "
                f"({st.session_state.kb.total_facts()} facts, {len(st.session_state.kb.rules)} rules) "
                "to check if a claim is **Consistent**, **Inconsistent**, or **Unknown**.\n\n"
                "Type any claim in English, for example:\n"
                "- *Narendra Modi is the chief minister of India*\n"
                "- *Paris hosted the 2024 Olympics*\n"
                "- *Delhi is the capital of France*\n"
                "- *Taj Mahal is located in Agra*\n\n"
                "I will also give you a full **Explainable AI** report."
            )
        }
    ]

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🤖 Verification Chatbot")
    st.caption("FOL + Explainable AI")
    st.metric("Knowledge Base Facts", st.session_state.kb.total_facts())
    st.metric("Logical Rules", len(st.session_state.kb.rules))
    st.metric("Predicates", len(st.session_state.kb.predicates()))

    st.divider()
    st.subheader("Quick claims")
    quick = [
        "Narendra Modi is the chief minister of India",
        "Paris hosted the 2024 Olympics",
        "Delhi is the capital of France",
        "Tokyo is the capital of Japan",
        "Gravity was discovered by Einstein",
        "ISRO is the space agency of India",
        "Taj Mahal is located in Agra",
        "Google headquarters is in China",
        "Capital of Tamil Nadu is Chennai",
    ]
    for q in quick:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.pending_claim = q

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.caption("K. Ramakrishnan College of Engineering\nAI & Data Science")

# ---------- Header ----------
st.markdown('<p class="main-title">🤖 Fake News Claim Verification Chatbot</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">First-Order Logic • Explainable AI • Knowledge-Driven Verification</p>',
    unsafe_allow_html=True
)

# ---------- Helper: verify one claim ----------
def verify_claim(claim: str) -> str:
    processor = st.session_state.processor
    engine = st.session_state.engine
    explainer = st.session_state.explainer
    kb = st.session_state.kb

    claim_info = processor.extract_entities_and_predicates(claim)
    pred, args = processor.try_map_to_fol(claim_info, kb)

    if pred is None:
        entities = ", ".join(claim_info["entities"]) if claim_info["entities"] else "none"
        return (
            "🟡 **UNKNOWN**\n\n"
            "I could not map this claim strongly to known FOL predicates.\n\n"
            f"**Entities detected:** {entities}\n\n"
            "Try mentioning known people, places, events, capitals, landmarks, companies, or discoveries.\n"
            "Example: *Narendra Modi is the Prime Minister of India*"
        )

    result = engine.check_consistency(claim_info, pred, args)
    xai = explainer.generate_full_explanation(claim, claim_info, pred, args, result)

    status = result["status"]
    if status == "CONSISTENT":
        badge = "🟢 **CONSISTENT**"
    elif status == "INCONSISTENT":
        badge = "🔴 **INCONSISTENT**"
    else:
        badge = "🟡 **UNKNOWN**"

    lines = [
        f"{badge}\n",
        f"**Claim:** {claim}",
        f"**FOL form:** `{pred}{args}`\n",
        "### 📖 Explanation",
        xai["natural_language"],
        "\n### ❓ Why this decision?",
    ]
    for r in xai["why"]:
        lines.append(f"- {r}")

    lines.append("\n### ⚖️ Key evidence")
    if xai["key_evidence"]["supporting"]:
        for f in xai["key_evidence"]["supporting"]:
            lines.append(f"- ✅ Supporting: `{f}`")
    if xai["key_evidence"]["contradicting"]:
        for f in xai["key_evidence"]["contradicting"]:
            lines.append(f"- ❌ Contradicting: `{f}`")
    if not xai["key_evidence"]["supporting"] and not xai["key_evidence"]["contradicting"]:
        lines.append("- No decisive fact found")

    lines.append("\n### 🔄 Counterfactuals")
    for cf in xai["counterfactuals"]:
        lines.append(f"- {cf}")

    rule = xai["logical_rule"]
    conf = xai["confidence_breakdown"]
    lines.append(f"\n### 📐 Logical rule")
    lines.append(f"**{rule['name']}** — {rule['description']}")
    lines.append(f"\n**Confidence:** {conf['score']:.2f} ({conf['level']}) | **Category:** {conf['category']}")
    lines.append(f"**Source:** {conf['source']}")

    return "\n".join(lines)

# ---------- Show chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Handle quick-button claim ----------
if "pending_claim" in st.session_state:
    claim = st.session_state.pending_claim
    del st.session_state.pending_claim

    st.session_state.messages.append({"role": "user", "content": claim})
    with st.chat_message("user"):
        st.markdown(claim)

    reply = verify_claim(claim)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# ---------- Chat input ----------
if prompt := st.chat_input("Type a news claim to verify..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Verifying with FOL + XAI..."):
            reply = verify_claim(prompt)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
