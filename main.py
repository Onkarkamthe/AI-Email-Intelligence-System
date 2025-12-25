import streamlit as st
from textblob import TextBlob
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Email Intelligence",
    page_icon="📧",
    layout="centered",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #e5e7eb;
}
.subtitle {
    color: #9ca3af;
    font-size: 1rem;
}
.label {
    font-weight: 600;
    color: #e5e7eb;
}
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def summarize_text(text, sentence_count=3):
    blob = TextBlob(text)
    sentences = blob.sentences
    if not sentences:
        return "Summary could not be generated."
    return " ".join(str(s) for s in sentences[:sentence_count])

def classify_priority(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.2:
        return "HIGH 🔴", abs(polarity)
    elif polarity > 0.2:
        return "LOW 🟢", polarity
    else:
        return "MEDIUM 🟡", abs(polarity)

# ---------------- HEADER ----------------
st.markdown("""
<div class="card">
    <div class="title">📧 AI Email Intelligence System</div>
    <div class="subtitle">
        Smart email analysis using NLP to summarize content and detect priority instantly.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="label">Paste Email Content</div>', unsafe_allow_html=True)

email_text = st.text_area(
    "",
    height=220,
    placeholder="Paste your email here..."
)

analyze = st.button("🚀 Analyze Email", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROCESS ----------------
if analyze:
    if email_text.strip() == "":
        st.warning("Please paste an email to analyze.")
    else:
        cleaned = clean_text(email_text)
        summary = summarize_text(cleaned)
        priority, confidence = classify_priority(cleaned)

        # SUMMARY CARD
        st.markdown("""
        <div class="card">
            <div class="label">📝 AI Generated Summary</div>
        </div>
        """, unsafe_allow_html=True)
        st.success(summary)

        # METRICS
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="card">
                <div class="label">🚦 Priority Level</div>
            </div>
            """, unsafe_allow_html=True)
            st.info(priority)

        with col2:
            st.markdown("""
            <div class="card">
                <div class="label">📊 Confidence Score</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(confidence, 1.0))
            st.write(f"Score: **{round(confidence, 2)}**")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <br>
    Built by <b>Onkar Kamthe</b> · AI · NLP · Streamlit  
    <br>
    Future-ready for Gmail API, ML models & enterprise dashboards
</div>
""", unsafe_allow_html=True)
