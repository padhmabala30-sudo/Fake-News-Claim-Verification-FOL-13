import streamlit as st
from knowledge_base import KnowledgeBase
from claim_processor import ClaimProcessor
from inference_engine import FOLInferenceEngine
from xai_explainer import XAIExplainer

# Page config
st.set_page_config(
    page_title="Fake News Claim Verification System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for neat dashboard look
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    .consistent {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 2px solid #28a745;
    }
    .inconsistent {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 2px solid #dc3545;
    }
    .unknown {
        background: linear-gradient(135deg, #fff3cd, #ffeeba);
        color: #856404;
        border: 2px solid #ffc107;
    }
    .fact-card {
        background: #f8f9fa;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        border-left: 4px solid #007bff;
    }
    .contradict-card {
        background: #fff5f5;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        border-left: 4px solid #dc3545;
    }
    .step-box {
        background: #f0f4ff;
        padding: 0.7rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #4a6cf7;
    }
    .kb-fact {
        background: #e8f5e9;
        padding: 0.5rem 0.8rem;
        border-radius: 6px;
        margin: 0.25rem 0;
        font-family: monospace;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase()
if "processor" not in st.session_state:
    st.session_state.processor = ClaimProcessor()
if "engine" not in st.session_state:
    st.session_state.engine = FOLInferenceEngine(st.session_state.kb)
if "explainer" not in st.session_state:
    st.session_state.explainer = XAIExplainer(st.session_state.kb)

# Header
st.markdown('<p class="main-header">🔍 Fake News Claim Verification System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">First-Order Logic (FOL) Based • Knowledge-Driven • Explainable AI</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size:0.9rem;'>K. Ramakrishnan College of Engineering • Department of AI & Data Science</p>", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.caption(f"Advanced FOL KB • {st.session_state.kb.total_facts()} facts • {len(st.session_state.kb.rules)} rules")
    
    kb = st.session_state.kb
    for pred in sorted(kb.predicates()):
        facts = kb.get_fact_objects(pred)
        with st.expander(f"**{pred}** ({len(facts)} facts)"):
            for f in facts[:8]:
                st.markdown(
                    f'<div class="kb-fact">{f.as_fol()}<br><small>{f.category.value} | conf={f.confidence:.2f} | {f.source}</small></div>',
                    unsafe_allow_html=True
                )
            if len(facts) > 8:
                st.caption(f"... and {len(facts)-8} more facts")
    
    st.divider()
    st.subheader("🧪 Sample Claims")
    samples = [
        "The 2024 Olympics occurred in Chennai",
        "Paris hosted the 2024 Olympics",
        "Delhi is the capital of France",
        "Tokyo is the capital city of Japan",
        "Narendra Modi is the chief minister of India",
        "Narendra Modi is the Prime Minister of India",
        "Gravity was discovered by Einstein",
        "Newton discovered gravity",
        "ISRO is the space agency of India",
        "Capital of Tamil Nadu is Chennai",
        "IIT Madras is located in Chennai",
        "Google headquarters is in USA",
        "Infosys is based in India",
        "Taj Mahal is located in Agra",
        "Sachin Tendulkar holds the record for most international runs",
        "COVID-19 started in Wuhan",
        "National animal of India is Tiger",
        "Currency of India is Indian Rupee"
    ]
    for s in samples:
        if st.button(s, key=s, use_container_width=True):
            st.session_state.sample_claim = s

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✍️ Enter News Claim")
    
    default_claim = st.session_state.get("sample_claim", "")
    claim = st.text_area(
        "Type or paste a claim to verify:",
        value=default_claim,
        height=100,
        placeholder="Type any claim here... e.g. Delhi is the capital of France / Gravity was discovered by Einstein / Paris hosted the 2024 Olympics"
    )
    
    verify_btn = st.button("🔎 Verify Claim", type="primary", use_container_width=True)

with col2:
    st.subheader("ℹ️ How it works")
    st.markdown("""
    1. **Type any claim** in free-form English  
    2. System extracts entities & FOL predicates  
    3. Checks against the advanced Knowledge Base  
    4. Returns **Consistent / Inconsistent / Unknown**  
    5. **Explainable AI** shows why, counterfactuals & fact importance  
    """)
    st.success("Includes full XAI report: plain-English explanation, logical rules, counterfactuals, and confidence.")

# Verification logic
if verify_btn and claim.strip():
    st.divider()
    
    processor = st.session_state.processor
    engine = st.session_state.engine
    kb = st.session_state.kb
    
    claim_info = processor.extract_entities_and_predicates(claim)
    
    # ---- Free-form mapping ----
    user_predicate, user_args = processor.try_map_to_fol(claim_info, kb)
    
    # Fallback to old hard-coded rules if free-form fails
    if user_predicate is None:
        claim_lower = claim.lower()
        if "olympics" in claim_lower and "chennai" in claim_lower:
            user_predicate, user_args = "EventOccurred", ("Olympics2024", "Chennai")
        elif "olympics" in claim_lower and "paris" in claim_lower:
            user_predicate, user_args = "EventOccurred", ("Olympics2024", "Paris")
        elif "modi" in claim_lower and "prime minister" in claim_lower:
            user_predicate, user_args = "PersonIs", ("NarendraModi", "PrimeMinisterOfIndia")
        elif "delhi" in claim_lower and "capital" in claim_lower:
            user_predicate, user_args = "IsCapitalOf", ("Delhi", "India")
    
    if user_predicate is None:
        st.markdown('<div class="status-box unknown">🟡 UNKNOWN</div>', unsafe_allow_html=True)
        st.warning("Not enough matching facts in the knowledge base to fully verify this claim.")
        
        st.markdown("#### 📌 What the system understood")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Entities detected:**")
            if claim_info["entities"]:
                for e in claim_info["entities"]:
                    st.code(e)
            else:
                st.write("_No known entities found_")
        with c2:
            st.write("**Possible predicates:**")
            if claim_info["suggested_predicates"]:
                for p in claim_info["suggested_predicates"]:
                    st.code(p)
            else:
                st.write("_No clear logical relation detected_")
        
        st.info("""
        **Tips for better results:**
        - Mention known people (Modi, Biden, Einstein, Musk…)
        - Mention places or capitals (Delhi, Paris, Tokyo, London…)
        - Mention events (Olympics, World Cup, Chandrayaan, COVID…)
        - Mention discoveries, space agencies, landmarks, etc.
        - Use clear sentences like: "X is the capital of Y" or "X was discovered by Y"
        """)
        
        st.markdown("#### 🧠 Reasoning")
        st.markdown('<div class="step-box">1. Claim received and parsed</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-box">2. Entities and possible predicates extracted</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-box">3. No strong match found in the Knowledge Base</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-box">4. Conclusion → UNKNOWN (insufficient evidence)</div>', unsafe_allow_html=True)
    else:
        result = engine.check_consistency(claim_info, user_predicate, user_args)
        
        # Status banner
        status = result["status"]
        if status == "CONSISTENT":
            st.markdown('<div class="status-box consistent">🟢 CONSISTENT</div>', unsafe_allow_html=True)
            st.success("The claim agrees with the verified knowledge base.")
        elif status == "INCONSISTENT":
            st.markdown('<div class="status-box inconsistent">🔴 INCONSISTENT</div>', unsafe_allow_html=True)
            st.error("The claim contradicts verified facts.")
        else:
            st.markdown('<div class="status-box unknown">🟡 UNKNOWN</div>', unsafe_allow_html=True)
            st.warning("Not enough information in the knowledge base to decide.")
        
        # Three columns for details
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("#### 📌 Extracted Info")
            st.write("**Entities:**")
            if claim_info["entities"]:
                for e in claim_info["entities"]:
                    st.code(e)
            else:
                st.write("_None detected_")
            
            st.write("**FOL Representation:**")
            st.code(f"{user_predicate}{user_args}")
        
        with c2:
            st.markdown("#### ✅ Supporting Facts")
            if result["supporting_facts"]:
                for f in result["supporting_facts"]:
                    st.markdown(f'<div class="fact-card">{f}</div>', unsafe_allow_html=True)
            else:
                st.info("No supporting facts found")
        
        with c3:
            st.markdown("#### ❌ Contradicting Facts")
            if result["contradicting_facts"]:
                for f in result["contradicting_facts"]:
                    st.markdown(f'<div class="contradict-card">{f}</div>', unsafe_allow_html=True)
            else:
                st.info("No contradicting facts found")
        
        # ========== EXPLAINABLE AI (XAI) PANEL ==========
        explainer = st.session_state.explainer
        xai = explainer.generate_full_explanation(
            claim, claim_info, user_predicate, user_args, result
        )

        st.divider()
        st.markdown("## 🔍 Explainable AI (XAI) Report")

        # Natural language narrative
        st.markdown("### 📖 Explanation in Plain English")
        st.info(xai["natural_language"])

        # Why this decision
        st.markdown("### ❓ Why this decision?")
        for reason in xai["why"]:
            st.markdown(f"- {reason}")

        # Metadata metrics
        st.markdown("### 📊 Verification Metadata")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Confidence", f"{xai['confidence_breakdown']['score']:.2f}")
        with m2:
            st.metric("Confidence Level", xai['confidence_breakdown']['level'])
        with m3:
            st.metric("Logical Rule", xai['logical_rule']['name'])
        with m4:
            st.metric("Category", xai['confidence_breakdown']['category'])

        st.caption(f"Source: {xai['confidence_breakdown']['source']} — {xai['confidence_breakdown']['interpretation']}")

        # Fact importance
        st.markdown("### ⚖️ Fact Importance (Attribution)")
        for item in xai["fact_importance"]:
            icon = "✅" if item["role"] == "Supporting" else ("❌" if item["role"] == "Contradicting" else "➖")
            st.markdown(
                f"{icon} **{item['fact']}**  \n"
                f"Role: {item['role']} | Importance: {item['importance']:.1f} | {item['contribution']}"
            )

        # Counterfactuals
        st.markdown("### 🔄 Counterfactual Explanations")
        st.caption("What would need to change for a different decision?")
        for cf in xai["counterfactuals"]:
            st.markdown(f"- {cf}")

        # Logical rule detail
        st.markdown("### 📐 Logical Rule Applied")
        st.code(f"{xai['logical_rule']['name']}: {xai['logical_rule']['description']}")

        # Step-by-step FOL reasoning
        with st.expander("🧠 Full Step-by-Step FOL Reasoning", expanded=False):
            for step in result["reasoning_steps"]:
                st.markdown(f'<div class="step-box">{step}</div>', unsafe_allow_html=True)

        # Limitations
        with st.expander("⚠️ Explanation Limitations"):
            for lim in xai["limitations"]:
                st.markdown(f"- {lim}")

elif verify_btn:
    st.warning("Please enter a claim first.")


# Footer
st.divider()
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.85rem; padding:1rem 0;">
    <b>Fake News Claim Verification System</b> using First-Order Logic<br>
    Presented by: Padhma Bala.K • Rakshana Manikandan • Sumithra.S<br>
    ADI1221 – Principles of Artificial Intelligence
</div>
""", unsafe_allow_html=True)
