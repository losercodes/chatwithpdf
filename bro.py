import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import random

# Initialize Gemini API
genai.configure(api_key='AIzaSyBNYRyd3WKy3M_pEcGo_pY5VUAkmH1tJVo')
gemini = genai.GenerativeModel('gemini-pro')

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def generate_mcqs(text, num_questions=10):
    """Generate multiple-choice questions from the text."""
    questions = []
    for _ in range(num_questions):
        prompt = f"Generate a multiple-choice question based on the following text:\n{text}"
        response = gemini.generate_content(prompt)
        questions.append(response.text)
    return questions

def main():
    st.title("PDF Chat and MCQ Generator")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        st.text_area("PDF Text", pdf_text, height=300)

        # Chat with PDF
        st.header("Chat with PDF")
        user_input = st.text_input("Ask a question about the PDF")
        if user_input:
            prompt = f"Based on the following text, answer the question: '{user_input}'\n{pdf_text}"
            response = gemini.generate_content(prompt)
            st.write("Answer:", response.text)

        # Generate MCQs
        st.header("Generate MCQs")
        if st.button("Create 10 MCQs"):
            mcqs = generate_mcqs(pdf_text)
            for i, mcq in enumerate(mcqs, start=1):
                st.write(f"Question {i}: {mcq}")

if __name__ == "__main__":
    main()
