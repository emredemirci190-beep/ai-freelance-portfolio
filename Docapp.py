import streamlit as st
from google import genai
from google.genai import types
import time

# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(page_title="Document Assistant", page_icon="📄")
st.title("📄 Document Q&A Assistant")
st.caption("Upload a text file and ask questions about it.")

# ── API CONNECTION ────────────────────────────
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# ── FILE UPLOADER ─────────────────────────────
uploaded_file = st.file_uploader("Select a text file (.txt)", type="txt")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    content = content.replace("\r\n", "\n")
    sections = [s.strip() for s in content.split("\n\n") if len(s.strip()) > 50]
    st.success(f"✓ File loaded — {len(sections)} sections found.")

    # ── QUESTION INPUT ────────────────────────
    question = st.text_input("Type your question:")

    if st.button("Ask") and question:
        # RAG: find relevant sections
        question_words = question.lower().split()
        scores = []
        for section in sections:
            score = sum(1 for word in question_words if word in section.lower())
            scores.append((score, section))
        scores.sort(reverse=True)
        selected = [s for score, s in scores[:2] if score > 0]

        if not selected:
            st.warning("This information is not found in the document.")
        else:
            context = "\n\n".join(selected)
            system = f"""Answer the question using only the text below.
If the answer is not in the text, say 'This information is not in the document.'

TEXT:
{context}"""

            with st.spinner("Generating answer..."):
                time.sleep(5)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=question,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0.1
                    )
                )

            st.markdown("### Answer")
            st.write(response.text)

            with st.expander("Which sections were used?"):
                for i, s in enumerate(selected, 1):
                    st.text(f"Section {i}:\n{s[:200]}...")