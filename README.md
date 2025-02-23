# Document-Chatbot-with-RAG
Document Chatbot with RAG
# 📄 Document Chatbot with RAG

## 🚀 Overview
This Streamlit app allows you to upload documents (PDF, DOCX, TXT) and chat with them using Retrieval-Augmented Generation (RAG). It leverages FAISS for semantic search and Ollama's DeepSeek LLM for question answering.

---

## 🏗️ Features
- Upload multiple documents (.pdf, .docx, .txt)
- Extract text using different libraries (pdfminer.six, docx, plain text)
- Perform semantic search with FAISS
- Generate answers via DeepSeek LLM
- Retain chat history and context

---

## 📚 Requirements
Ensure you have Python installed (>=3.8) and set up a virtual environment:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

### Required Libraries

- **Streamlit**: For building the chatbot UI
- **Sentence-Transformers**: For generating text embeddings
- **FAISS**: For fast vector similarity search
- **pdfminer.six**: For extracting text from PDFs
- **python-docx**: For extracting text from DOCX files
- **Ollama**: For interacting with DeepSeek LLM

### Optional PDF Libraries
If you want to use other methods to process PDFs, install these additional libraries:

```bash
# PyMuPDF (fitz)
pip install pymupdf

# PDFPlumber
pip install pdfplumber

# PyPDF2
pip install PyPDF2

# Camelot (for table extraction)
pip install camelot-py[base]

# Tesseract OCR (for scanned PDFs)
pip install pytesseract
```

For Tesseract OCR, install the engine as well:

- **Windows**: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux/macOS**:

```bash
sudo apt-get install tesseract-ocr
```

---

## 🏃‍♂️ Running the App
Launch the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📂 File Structure

```
.
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

---

## 🔥 Usage
1. Run the app using the command above.
2. Upload your documents.
3. Type your questions in the chat.
4. View AI-generated answers based on document context.

---

## 🌟 Future Enhancements
- Add support for more file formats (e.g., CSV, PPTX)
- Improve chunking strategy for larger documents
- Enhance UI/UX with custom themes

---

## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.
---

Happy chatting with your documents! 🤖

