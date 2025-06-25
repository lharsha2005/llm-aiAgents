import streamlit as st
import tempfile
from graph import graph 
import os

st.set_page_config(page_title="Banking Chatbot", layout="centered")
st.title("🏦 Banking Assistant")

user_input = st.text_input("Ask a banking-related question:")
uploaded_image = st.file_uploader("Or upload a scanned image (JPEG/PNG):", type=["png", "jpg", "jpeg"])

if st.button("Submit"):
    with st.spinner("Processing..."):

        img_path = None
        if uploaded_image:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(uploaded_image.read())
            img_path = temp_file.name

        state = {
            "question": user_input,
            "img_path": img_path,
            "ocr_text": None,
            "answer": None
        }

        result = graph.invoke(state)

        st.markdown(f"**Answer:** {result['answer']}")
