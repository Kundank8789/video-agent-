# 🎥 Video Agent

An AI-powered Video Agent that transforms videos into actionable insights by automatically extracting audio, generating transcripts, creating summaries, identifying key decisions, extracting action items, and enabling question answering through Retrieval-Augmented Generation (RAG).

## 🚀 Overview

Video Agent helps users quickly understand long-form videos such as meetings, lectures, interviews, podcasts, and YouTube content. It automates the entire pipeline—from video ingestion to AI-powered analysis—making it easier to search, summarize, and interact with video content.

## ✨ Features

* 🎥 Process YouTube videos and local video files
* 🎙️ Automatic audio extraction
* 📝 AI-powered speech-to-text transcription
* 📄 Intelligent video summarization
* 📌 Action item extraction
* 💡 Key decision detection
* ❓ Question extraction
* 🔍 RAG-based question answering over video transcripts
* 📚 Vector database for semantic search
* 🌐 Interactive Streamlit interface
* ⚡ Fast and scalable processing pipeline

## 🛠️ Tech Stack

### AI & Machine Learning

* LangChain
* Mistral AI / Google Gemini
* Hugging Face Embeddings
* Whisper (Speech-to-Text)

### Backend

* Python

### Vector Database

* ChromaDB

### Frontend

* Streamlit

### Utilities

* yt-dlp
* FFmpeg
* pydub

## 📂 Project Structure

```bash
video-agent/
│
├── app.py
├── pipeline.py
├── agents/
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   ├── audio_processor.py
│   └── helpers.py
│
├── data/
├── requirements.txt
└── README.md
```

## 🚀 Workflow

```text
Video/YouTube URL
        │
        ▼
Audio Extraction
        │
        ▼
Speech Transcription
        │
        ▼
Chunking & Embeddings
        │
        ▼
Store in ChromaDB
        │
        ▼
Generate Summary
        │
        ▼
Extract:
• Action Items
• Key Decisions
• Questions
        │
        ▼
Ask Questions with RAG
```

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/Kundank8789/video-agent-.git
```

### Navigate to the Project

```bash
cd video-agent-
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key
GEMINI_API_KEY=your_api_key
```

## ▶️ Run the Application

Launch the Streamlit interface:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 📸 Screenshots

### Upload Video

```md
![Upload](./screenshots/upload.png)
```

### AI Summary

```md
![Summary](./screenshots/summary.png)
```

### Chat with Video

```md
![Chat](./screenshots/chat.png)
```

## 🌟 Future Enhancements

* Multi-video conversations
* Speaker diarization
* Timestamped citations
* PDF & DOCX report export
* Live meeting transcription
* Video chapter generation
* Multi-language transcription
* Cloud storage integration

## 📈 Learning Outcomes

* AI-powered speech processing
* Retrieval-Augmented Generation (RAG)
* Vector databases with ChromaDB
* LangChain pipelines
* LLM integration
* Streamlit application development
* End-to-end AI workflow orchestration

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Kundan Kumar**

GitHub: https://github.com/Kundank8789

---

⭐ If you found this project useful, please consider giving it a star on GitHub.
