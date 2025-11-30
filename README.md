# 🤖 Study Assistant Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://studyassistantpro.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-Powered Dual-Server Study Assistant with Multi-Modal Analysis and RAG**

Transform your study materials into actionable insights with advanced AI models. Upload PDFs, audio, or video files and get instant summaries, analysis, or answers to your questions.

## 🚀 Live Demo

**[Try it now →](https://studyassistantpro.streamlit.app/)**

---

## ✨ Features

### 📊 Multi-Mode Analysis (Kaggle Server)
Powered by **Mistral AI** and **Whisper**, offering 6 different analysis modes:

- **📝 Brief Summary** - Quick 2-3 sentence overview
- **📚 Detailed Analysis** - Comprehensive breakdown with themes and conclusions
- **🎯 Main Topics** - Extract and explain key topics
- **🔑 Keywords Focus** - Analyze based on your specific keywords
- **📌 Bullet Points** - Concise key points in list format
- **❓ Q&A Format** - Summary structured as questions and answers

### 💡 RAG Question Answering (Colab Server)
Powered by **TinyLlama** with FAISS vector search:

- Ask specific questions about your documents
- Get contextually accurate answers
- View source excerpts used for answers
- Efficient semantic search through your content

### 📁 Multi-Format Support
- **PDF Documents** - Extract and analyze text
- **Audio Files** - Transcribe and analyze (MP3, WAV, M4A, OGG)
- **Video Files** - Extract audio, transcribe, and analyze (MP4, AVI, MOV, MKV)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                     │
│              (User Interface & Control)                  │
└────────────────┬─────────────────┬──────────────────────┘
                 │                 │
        ┌────────▼────────┐   ┌───▼──────────────┐
        │ Kaggle Server   │   │  Colab Server    │
        │ (Analysis +     │   │  (RAG + Q&A)     │
        │  Extraction)    │   │                  │
        ├─────────────────┤   ├──────────────────┤
        │ • Mistral AI    │   │ • TinyLlama      │
        │ • Whisper       │   │ • FAISS          │
        │ • 6 Modes       │   │ • Embeddings     │
        └─────────────────┘   └──────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit** - Interactive web interface
- **Python 3.8+** - Core programming language

### Backend Servers

**Kaggle Server:**
- **Mistral Nemo Instruct** - Advanced text analysis
- **Whisper (Tiny)** - Audio/video transcription
- **PyPDF** - PDF text extraction
- **FFmpeg** - Video audio extraction
- **FastAPI** - REST API framework
- **ngrok** - Secure tunneling

**Colab Server:**
- **TinyLlama** (via Ollama) - Question answering
- **Sentence Transformers** - Text embeddings
- **FAISS** - Vector similarity search
- **FastAPI** - REST API framework
- **ngrok** - Secure tunneling

---

## 📋 Setup Guide

### Prerequisites
- 2 ngrok accounts/tokens ([Get them here](https://dashboard.ngrok.com))
- Kaggle account (with GPU enabled)
- Google Colab account (with GPU enabled)
- Python 3.8+ (for local Streamlit)

### Step 1: Setup Kaggle Server

1. Open the `study-assistant-pro-kanalysis.ipynb` notebook in Kaggle
2. Enable GPU: Settings → Accelerator → GPU T4
3. Enable Internet: Settings → Internet → On
4. Update the ngrok token in the notebook:
   ```python
   NGROK_TOKEN = "your_first_ngrok_token_here"
   ```
5. Run all cells
6. Copy the generated Kaggle URL (looks like `https://xxxx.ngrok-free.app`)

### Step 2: Setup Colab Server

1. Open the `Study_Assistant_pro_C_Answer.ipynb` notebook in Google Colab
2. Enable GPU: Runtime → Change runtime type → GPU
3. Update the ngrok token in the notebook:
   ```python
   NGROK_TOKEN = "your_second_ngrok_token_here"
   ```
4. Run all cells
5. Copy the generated Colab URL (looks like `https://yyyy.ngrok-free.app`)

### Step 3: Run Streamlit App

#### Option A: Use Deployed Version
Simply visit **[https://studyassistantpro.streamlit.app/](https://studyassistantpro.streamlit.app/)**

#### Option B: Run Locally
```bash
# Clone the repository
git clone https://github.com/yourusername/study-assistant-pro.git
cd study-assistant-pro

# Install dependencies
pip install streamlit requests

# Run the app
streamlit run app.py
```

### Step 4: Configure the App

1. In the sidebar, paste your Kaggle URL
2. Paste your Colab URL
3. Enter the API key (default: `123456`)
4. Click "Test Kaggle" and "Test Colab" to verify connections
5. Start using the app! 🎉

---

## 💻 Usage Examples

### Example 1: Analyze a PDF with Keywords
```
1. Select "Analysis" tab
2. Choose "PDF" as file type
3. Upload your PDF document
4. Select "Keywords Focus" analysis mode
5. Enter keywords: "climate change, sustainability"
6. Click "Analyze"
```

### Example 2: Transcribe and Summarize a Lecture
```
1. Select "Analysis" tab
2. Choose "Audio" as file type
3. Upload your lecture recording (MP3/WAV)
4. Select "Detailed Analysis" mode
5. Click "Analyze"
```

### Example 3: Ask Questions About Your Document
```
1. Select "RAG" tab
2. Upload a file OR paste text
3. Enter your question: "What are the main conclusions?"
4. Click "Get Answer"
5. View answer with source references
```

---

## 📊 Analysis Modes Explained

| Mode | Best For | Output Length | Use Case |
|------|----------|---------------|----------|
| **Brief** | Quick overviews | 2-3 sentences | When you need a fast summary |
| **Detailed** | Deep understanding | ~600 tokens | Comprehensive analysis needed |
| **Main Topics** | Content structure | ~500 tokens | Understanding document organization |
| **Keywords Focus** | Targeted analysis | ~500 tokens | Looking for specific information |
| **Bullet Points** | Key takeaways | ~400 tokens | Easy-to-scan summaries |
| **Q&A Format** | Study materials | ~500 tokens | Creating study guides |

---

## 🔒 Security & Privacy

- **API Authentication**: All requests require API key authentication
- **Secure Tunneling**: ngrok provides encrypted connections
- **No Data Storage**: Files are processed in memory and immediately deleted
- **Session Isolation**: Each user session is independent

---

## 📝 API Endpoints

### Kaggle Server

```http
GET /health
# Check server status

POST /extract
# Extract text from files
Content-Type: multipart/form-data
Authorization: Bearer {API_KEY}

POST /analyze
# Analyze extracted text
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {API_KEY}
```

### Colab Server

```http
GET /health
# Check server status

POST /rag
# Answer questions using RAG
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {API_KEY}
```

---

## 🐛 Troubleshooting

### Server Connection Issues
- **Problem**: "Server Offline" message
- **Solution**: 
  - Verify ngrok tokens are correct
  - Ensure GPU is enabled in notebooks
  - Re-run the server cells
  - Check if URLs are copied correctly

### Analysis Taking Too Long
- **Problem**: Processing times out
- **Solution**:
  - Use shorter audio/video files (<10 minutes)
  - For PDFs, try documents <50 pages
  - Choose "Brief" mode for faster results

### Empty or Strange Outputs
- **Problem**: Analysis seems incomplete
- **Solution**:
  - Try a different analysis mode
  - Ensure file uploaded correctly
  - Check if text extraction succeeded

---

## 🚧 Limitations

- **Session Duration**: ngrok free tier has session limits (~8 hours)
- **File Size**: Large files (>100MB) may cause timeouts
- **GPU Availability**: Depends on Kaggle/Colab GPU availability
- **Concurrent Users**: Servers handle one request at a time
- **Language**: Currently optimized for English content

---

## 🗺️ Roadmap

- [ ] Support for more languages
- [ ] Document comparison feature
- [ ] Export to various formats (Word, Markdown)
- [ ] Batch processing for multiple files
- [ ] Custom model fine-tuning
- [ ] Premium tier with persistent servers
- [ ] Mobile app version

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Mistral AI** for the powerful Mistral Nemo model
- **OpenAI** for Whisper transcription
- **Meta AI** for TinyLlama
- **Streamlit** for the amazing web framework
- **Hugging Face** for model hosting
- **ngrok** for secure tunneling

---

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/yourusername/study-assistant-pro/issues)
- Check existing [Discussions](https://github.com/yourusername/study-assistant-pro/discussions)
- Email: your.email@example.com

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/study-assistant-pro&type=Date)](https://star-history.com/#yourusername/study-assistant-pro&Date)

---

**Made with ❤️ by [Your Name]**

**[🚀 Try the App Now](https://studyassistantpro.streamlit.app/)** | **[📖 Documentation](#)** | **[🐛 Report Bug](https://github.com/yourusername/study-assistant-pro/issues)**
