"""
ENHANCED STREAMLIT APP - RUN LOCALLY
Save as: app.py
Run with: streamlit run app.py

Requirements:
pip install streamlit requests
"""

import streamlit as st
import requests
import json
import time

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="Study Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# CUSTOM CSS
# ========================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .result-box {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .analysis-mode-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# SESSION STATE
# ========================
if 'kaggle_url' not in st.session_state:
    st.session_state.kaggle_url = ""
if 'colab_url' not in st.session_state:
    st.session_state.colab_url = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = "123456"
if 'history' not in st.session_state:
    st.session_state.history = []

# ========================
# HELPER FUNCTIONS
# ========================
def check_server(url: str) -> bool:
    """Check if server is online"""
    try:
        r = requests.get(f"{url}/health", timeout=5)
        return r.status_code == 200
    except:
        return False

def extract_text(kaggle_url: str, api_key: str, input_type: str, file) -> dict:
    """Extract text using Kaggle"""
    try:
        with st.spinner('📄 Extracting text...'):
            r = requests.post(
                f"{kaggle_url}/extract",
                files={'file': (file.name, file, file.type)},
                data={'input_type': input_type},
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=300
            )
        return r.json() if r.status_code == 200 else {"status": "error", "message": r.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze(kaggle_url: str, api_key: str, text: str, analysis_type: str, keywords: str = "") -> dict:
    """Analyze text using Kaggle with specified mode"""
    try:
        with st.spinner(f'🔍 Analyzing with {analysis_type} mode...'):
            r = requests.post(
                f"{kaggle_url}/analyze",
                data={
                    'text': text,
                    'analysis_type': analysis_type,
                    'keywords': keywords
                },
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=300
            )
        return r.json() if r.status_code == 200 else {"status": "error", "message": r.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def rag_query(colab_url: str, api_key: str, text: str, question: str) -> dict:
    """Answer question using Colab RAG"""
    try:
        with st.spinner('💡 Finding answer with TinyLlama...'):
            r = requests.post(
                f"{colab_url}/rag",
                data={'text': text, 'question': question},
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=300
            )
        return r.json() if r.status_code == 200 else {"status": "error", "message": r.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Kaggle URL
    st.markdown("### 🔵 Kaggle Server")
    st.caption("Analysis + File Processing")
    kaggle_url = st.text_input(
        "Kaggle URL",
        st.session_state.kaggle_url,
        placeholder="https://xxxx.ngrok-free.app"
    )
    st.session_state.kaggle_url = kaggle_url
    
    # Colab URL
    st.markdown("### 🟢 Colab Server")
    st.caption("RAG with TinyLlama")
    colab_url = st.text_input(
        "Colab URL",
        st.session_state.colab_url,
        placeholder="https://yyyy.ngrok-free.app"
    )
    st.session_state.colab_url = colab_url
    
    # API Key
    st.markdown("### 🔑 API Key")
    api_key = st.text_input(
        "API Key (same for both)",
        st.session_state.api_key,
        type="password"
    )
    st.session_state.api_key = api_key
    
    st.divider()
    
    # Test buttons
    st.markdown("### 🧪 Test Connections")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Kaggle", use_container_width=True):
            if kaggle_url:
                if check_server(kaggle_url):
                    st.success("✅ Online")
                else:
                    st.error("❌ Offline")
            else:
                st.warning("Enter URL")
    
    with col2:
        if st.button("Test Colab", use_container_width=True):
            if colab_url:
                if check_server(colab_url):
                    st.success("✅ Online")
                else:
                    st.error("❌ Offline")
            else:
                st.warning("Enter URL")
    
    st.divider()
    
    # Status
    st.markdown("### 📡 Status")
    k_status = "🟢" if kaggle_url and check_server(kaggle_url) else "🔴"
    c_status = "🟢" if colab_url and check_server(colab_url) else "🔴"
    st.markdown(f"**Kaggle:** {k_status} | **Colab:** {c_status}")
    
    st.divider()
    
    # Guide
    with st.expander("📖 Setup Guide"):
        st.markdown("""
        **1. Get 2 ngrok tokens:**
        - Visit: https://dashboard.ngrok.com
        - Get your first token
        - Create second token
        
        **2. Run Kaggle:**
        - Paste first token
        - Copy the URL
        
        **3. Run Colab:**
        - Paste second token
        - Copy the URL
        
        **4. Configure here:**
        - Paste both URLs
        - Test connections
        - Start using!
        """)
    
    # Analysis Modes Info
    with st.expander("🎯 Analysis Modes"):
        st.markdown("""
        **Brief** - Quick 2-3 sentence summary
        
        **Detailed** - Comprehensive analysis with themes, evidence, and conclusions
        
        **Main Topics** - Identify and explain key topics discussed
        
        **Keywords Focus** - Analyze based on your specified keywords
        
        **Bullet Points** - Concise key points in list format
        
        **Q&A Format** - Summary structured as questions and answers
        """)
    
    # Stats
    if st.session_state.history:
        st.divider()
        st.markdown("### 📈 Stats")
        st.metric("Total", len(st.session_state.history))
        
        analysis = sum(1 for h in st.session_state.history if h['type'] == 'analysis')
        rag = sum(1 for h in st.session_state.history if h['type'] == 'rag')
        
        col1, col2 = st.columns(2)
        col1.metric("Analysis", analysis)
        col2.metric("RAG", rag)
        
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ========================
# MAIN CONTENT
# ========================
st.markdown("<h1 class='main-header'>🤖 Study Assistant Pro</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;margin-bottom:2rem;'>
<strong>Dual-Server Architecture:</strong> Kaggle (Mistral + Multi-Mode Analysis) + Colab (TinyLlama RAG)
</div>
""", unsafe_allow_html=True)

# Status banner
col1, col2 = st.columns(2)
with col1:
    if kaggle_url and check_server(kaggle_url):
        st.success("🔵 Kaggle: Ready (6 Analysis Modes)")
    else:
        st.warning("🔵 Kaggle: Not Connected")

with col2:
    if colab_url and check_server(colab_url):
        st.success("🟢 Colab: Ready")
    else:
        st.warning("🟢 Colab: Not Connected")

st.divider()

# ========================
# TABS
# ========================
tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💡 RAG", "📜 History"])

# ========================
# TAB 1: ENHANCED ANALYSIS
# ========================
with tab1:
    st.markdown("### 📊 Multi-Mode Analysis with Mistral")
    
    if not kaggle_url:
        st.error("⚠️ Configure Kaggle URL in sidebar")
    else:
        # File upload section
        col1, col2 = st.columns([3, 1])
        with col1:
            input_type = st.selectbox("File Type", ["pdf", "audio", "video"])
        with col2:
            st.info("Uses Kaggle")
        
        file_types = {
            'pdf': ['pdf'],
            'audio': ['mp3', 'wav', 'm4a', 'ogg'],
            'video': ['mp4', 'avi', 'mov', 'mkv']
        }
        
        file = st.file_uploader(
            f"Upload {input_type.upper()}",
            type=file_types[input_type]
        )
        
        st.markdown("### 🎯 Analysis Configuration")
        
        # Analysis mode selection
        analysis_modes = {
            "brief": "📝 Brief Summary",
            "detailed": "📚 Detailed Analysis",
            "main_topics": "🎯 Main Topics",
            "keywords_focus": "🔑 Keywords Focus",
            "bullet_points": "📌 Bullet Points",
            "question_answer": "❓ Q&A Format"
        }
        
        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.selectbox(
                "Analysis Mode",
                options=list(analysis_modes.keys()),
                format_func=lambda x: analysis_modes[x]
            )
        
        with col2:
            # Show mode description
            mode_descriptions = {
                "brief": "Quick 2-3 sentence overview",
                "detailed": "Comprehensive analysis",
                "main_topics": "Extract key topics",
                "keywords_focus": "Focus on your keywords",
                "bullet_points": "Key points as bullets",
                "question_answer": "Q&A summary format"
            }
            st.info(mode_descriptions[analysis_type])
        
        # Keywords input
        keywords = st.text_input(
            "Keywords (optional, recommended for 'Keywords Focus' mode)",
            placeholder="e.g., AI, machine learning, climate change",
            help="Separate multiple keywords with commas"
        )
        
        # Display selected mode
        st.markdown(f"<div class='analysis-mode-card'>Selected: {analysis_modes[analysis_type]}</div>", 
                   unsafe_allow_html=True)
        
        if st.button("🚀 Analyze", type="primary"):
            if not file:
                st.error("❌ Upload a file first")
            else:
                # Extract text
                result = extract_text(kaggle_url, api_key, input_type, file)
                if result['status'] == 'success':
                    text = result['text']
                    st.success(f"✅ Extracted {len(text):,} characters")
                    
                    # Show preview
                    with st.expander("📄 Text Preview"):
                        st.text(text[:500] + "..." if len(text) > 500 else text)
                    
                    # Analyze with selected mode
                    result = analyze(kaggle_url, api_key, text, analysis_type, keywords)
                    if result['status'] == 'success':
                        st.markdown("### 📊 Analysis Results")
                        
                        # Display mode used
                        st.info(f"**Mode Used:** {analysis_modes[analysis_type]}" + 
                               (f" | **Keywords:** {keywords}" if keywords else ""))
                        
                        # Display analysis
                        st.markdown(f"<div class='result-box'>{result['analysis']}</div>", 
                                   unsafe_allow_html=True)
                        
                        # Download button
                        download_data = {
                            "analysis": result['analysis'],
                            "mode": analysis_type,
                            "keywords": keywords,
                            "file": file.name,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "text_length": result.get('text_length', len(text))
                        }
                        
                        st.download_button(
                            "📥 Download Analysis",
                            json.dumps(download_data, indent=2),
                            f"analysis_{analysis_type}_{int(time.time())}.json",
                            "application/json"
                        )
                        
                        # Save to history
                        st.session_state.history.append({
                            'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'analysis',
                            'mode': analysis_type,
                            'keywords': keywords,
                            'file': file.name,
                            'data': result
                        })
                        
                        st.success("✅ Analysis saved to history!")
                    else:
                        st.error(f"❌ Analysis failed: {result['message']}")
                else:
                    st.error(f"❌ Extraction failed: {result['message']}")

# ========================
# TAB 2: RAG (unchanged)
# ========================
with tab2:
    st.markdown("### 💡 Question Answering with TinyLlama")
    
    if not colab_url:
        st.error("⚠️ Configure Colab URL in sidebar")
    else:
        source = st.radio(
            "Text Source",
            ["📄 Upload File", "✍️ Paste Text"],
            horizontal=True
        )
        
        text_input = ""
        
        if source == "📄 Upload File":
            if not kaggle_url:
                st.warning("⚠️ Need Kaggle for file extraction")
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    file_type = st.selectbox("Type", ["pdf", "audio", "video"], key="rag_type")
                with col2:
                    st.info("Uses Kaggle")
                
                rag_file = st.file_uploader("Upload", type=['pdf','mp3','wav','m4a','mp4','avi','mov'], key="rag_file")
                
                if rag_file and st.button("Extract"):
                    result = extract_text(kaggle_url, api_key, file_type, rag_file)
                    if result['status'] == 'success':
                        st.session_state.rag_text = result['text']
                        st.success(f"✅ {len(result['text']):,} chars")
                    else:
                        st.error(result['message'])
                
                if 'rag_text' in st.session_state:
                    text_input = st.session_state.rag_text
                    with st.expander("View Text"):
                        st.text(text_input[:500] + "...")
        else:
            text_input = st.text_area("Paste Text", height=200)
        
        question = st.text_area("Your Question", height=100)
        
        if st.button("💡 Get Answer", type="primary"):
            if not text_input:
                st.error("❌ Provide text")
            elif not question:
                st.error("❌ Enter question")
            else:
                result = rag_query(colab_url, api_key, text_input, question)
                if result['status'] == 'success':
                    st.markdown("### Answer")
                    st.markdown(f"<div class='result-box'>{result['answer']}</div>", 
                               unsafe_allow_html=True)
                    
                    with st.expander("📚 Sources"):
                        for i, s in enumerate(result['sources'], 1):
                            st.markdown(f"**Source {i}:**")
                            st.text(s[:300] + "...")
                            st.divider()
                    
                    st.info(f"Searched {result['num_chunks']} chunks")
                    
                    st.download_button(
                        "📥 Download",
                        json.dumps(result, indent=2),
                        f"rag_{int(time.time())}.json"
                    )
                    
                    st.session_state.history.append({
                        'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'type': 'rag',
                        'data': result
                    })
                else:
                    st.error(result['message'])

# ========================
# TAB 3: ENHANCED HISTORY
# ========================
with tab3:
    if not st.session_state.history:
        st.info("📭 No history yet")
    else:
        st.markdown(f"### 📋 History ({len(st.session_state.history)} items)")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.selectbox("Filter by type", ["All", "Analysis", "RAG"])
        with col2:
            sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
        
        # Apply filters
        filtered = st.session_state.history
        if filter_type == "Analysis":
            filtered = [h for h in filtered if h['type'] == 'analysis']
        elif filter_type == "RAG":
            filtered = [h for h in filtered if h['type'] == 'rag']
        
        # Apply sorting
        if sort_order == "Oldest First":
            filtered = list(filtered)
        else:
            filtered = list(reversed(filtered))
        
        # Display history
        for i, entry in enumerate(filtered, 1):
            with st.expander(f"#{i} - {entry['type'].upper()} - {entry['time']}"):
                if entry['type'] == 'analysis':
                    st.info(f"**Mode:** {entry.get('mode', 'N/A')}" + 
                           (f" | **Keywords:** {entry.get('keywords', 'None')}" if entry.get('keywords') else "") +
                           (f" | **File:** {entry.get('file', 'N/A')}" if entry.get('file') else ""))
                    st.markdown("**Analysis:**")
                    st.markdown(entry['data']['analysis'])
                else:
                    st.info(f"**Question:** {entry['data'].get('question', 'N/A')}")
                    st.success(f"**Answer:** {entry['data']['answer']}")
                
                st.download_button(
                    "📥 Download",
                    json.dumps(entry['data'], indent=2),
                    f"history_{i}.json",
                    key=f"dl{i}"
                )

# ========================
# FOOTER
# ========================
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#666;padding:1rem;'>
<p><strong>🤖 Study Assistant Pro v2.0</strong></p>
<p style='font-size:0.9rem;'>🔵 Kaggle: Mistral + Whisper (6 Analysis Modes) | 🟢 Colab: TinyLlama + FAISS</p>
<p style='font-size:0.8rem;'>Features: Brief, Detailed, Main Topics, Keywords Focus, Bullet Points, Q&A Format</p>
</div>
""", unsafe_allow_html=True)