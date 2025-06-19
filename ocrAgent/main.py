import streamlit as st
from graph import graph
import tempfile
import os

st.set_page_config(page_title="OCR Query System", layout="centered")

st.title("Bank Statement Q&A")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
question = st.text_input("Ask a question", placeholder="e.g. Give transactions on 30/05/2020")

if uploaded_file and question:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.write(uploaded_file.read())
    temp_path = temp_file.name
    temp_file.close() 

    with st.spinner("Processing..."):
        output = graph.invoke({
            "img_path": temp_path,
            "question": question,
            "answer": "Conditions not satisfied",
            "corrected_data": ""
        })

    st.subheader("Final Answer:")
    st.success(output["answer"])

    with st.expander("Debug Info"):
        st.json(output)

else:
    st.info("Upload an image and enter your question to begin.")
