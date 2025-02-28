# Virtual Research Assistant for Academic Papers

An AI-powered assistant designed to help researchers efficiently process and extract insights from academic papers and PDF documents.

## 📚 Overview

The Virtual Research Assistant is a modular, AI-powered tool that ingests academic papers and provides:

- Comprehensive summaries
- Key topic annotations
- Automatic keyword extraction
- Interactive Q&A based on document content
- Audio summaries for enhanced accessibility

Perfect for researchers, students, and academics who need to quickly digest and analyze complex scholarly content.

## 🔧 Key Features

- **PDF Parsing & Document Ingestion:** Extract and preprocess text from PDF documents
- **Smart Summarization:** Generate concise, informative summaries of lengthy academic papers
- **Keyword Extraction:** Automatically identify important terms and concepts
- **Interactive Q&A:** Query specific details and receive context-aware answers
- **Audio Summaries:** Convert text summaries to natural-sounding audio for accessibility
- **Modular Architecture:** Built with LangChain to enable easy extension and integration

## 🛠️ Technology Stack

- **PDF Processing:** PyPDF2/pdfminer.six
- **Natural Language Processing:** HuggingFace Transformers (BART/T5)
- **Orchestration:** LangChain for workflow management
- **Text-to-Speech:** ElevenLabs API
- **User Interface:** Streamlit/Gradio
- **Deployment:** Docker, Cloud-ready

## 📊 Use Cases

- **Literature Reviews:** Quickly digest multiple research papers
- **Research Assistance:** Extract key information without reading entire documents
- **Accessibility:** Access research content via audio for visually impaired users
- **Academic Collaboration:** Share summaries and insights with peers
- **Educational Support:** Create study guides and lecture materials efficiently

## 🚀 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/virtual-research-assistant.git
cd virtual-research-assistant

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 📋 Project Structure

```
virtual-research-assistant/
├── app.py                      # Main Streamlit/Gradio application
├── modules/
│   ├── pdf_processor.py        # PDF extraction and preprocessing
│   ├── summarizer.py           # Document summarization
│   ├── keyword_extractor.py    # Keyword and topic extraction
│   ├── qa_engine.py            # Question answering functionality
│   └── audio_generator.py      # Text-to-speech conversion
├── utils/
│   ├── langchain_utils.py      # LangChain integration helpers
│   └── preprocessing.py        # Text cleaning utilities
├── tests/                      # Unit and integration tests
├── Dockerfile                  # Container configuration
└── requirements.txt            # Project dependencies
```

## 📝 Usage Example

```python
from modules.pdf_processor import extract_text
from modules.summarizer import generate_summary
from modules.keyword_extractor import extract_keywords
from modules.qa_engine import answer_question
from modules.audio_generator import text_to_audio

# Process a PDF file
pdf_text = extract_text("academic_paper.pdf")
cleaned_text = preprocess_text(pdf_text)

# Generate insights
summary = generate_summary(cleaned_text)
keywords = extract_keywords(cleaned_text)
answer = answer_question(cleaned_text, "What is the main contribution?")
audio_file = text_to_audio(summary, api_key)

print(f"Summary: {summary}")
print(f"Keywords: {', '.join(keywords)}")
print(f"Q&A: {answer}")
print(f"Audio summary saved to: {audio_file}")
```

## 🔄 Development Roadmap

- **Phase 1:** Requirements Analysis & Architecture Design
- **Phase 2:** Data Ingestion & Preprocessing
- **Phase 3:** Document Summarization
- **Phase 4:** Keyword Extraction & Q&A
- **Phase 5:** Audio Summary Generation
- **Phase 6:** Workflow Orchestration
- **Phase 7:** User Interface & Deployment
- **Phase 8:** Testing, Evaluation & Iteration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) for workflow orchestration
- [HuggingFace Transformers](https://github.com/huggingface/transformers) for NLP capabilities
- [ElevenLabs](https://elevenlabs.io/) for text-to-speech conversion
- [Streamlit](https://streamlit.io/) for the user interface