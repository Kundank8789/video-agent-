# app.py - Premium UI Version
import streamlit as st
from dotenv import load_dotenv
import time
from datetime import datetime
import tempfile
import os
import base64

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Video Assistant Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with animations and gradients
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Animated gradient header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        padding: 1rem 0;
        animation: gradientShift 3s ease-in-out infinite;
        background-size: 200% 200%;
        text-align: center;
        letter-spacing: -1px;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 1rem 0;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
    }
    
    /* Premium button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        width: 100%;
        font-size: 1rem;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Metrics with icons */
    .metric-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .metric-container:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Chat bubbles with avatars */
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
        animation: slideInRight 0.3s ease;
    }
    
    .chat-assistant {
        background: white;
        color: #2d3748;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Custom sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f7fafc;
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.3);
    }
    
    /* Progress bar animation */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #edf2f7;
    }
    
    /* File uploader styling */
    .uploaded-file {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-success {
        background: #48bb78;
        color: white;
    }
    
    .status-processing {
        background: #ed8936;
        color: white;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #ebf4ff 0%, #e0e7ff 100%);
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

def process_video(source, language):
    """Process video with enhanced progress tracking"""
    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summarizer import summarize, generate_title
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        from core.rag_engine import build_rag_chain
        
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        # Enhanced progress steps with icons
        steps = [
            (5, "🔍 Analyzing input source..."),
            (15, "🎬 Extracting audio from video..."),
            (30, "🎤 Transcribing with AI..."),
            (45, "📝 Generating intelligent title..."),
            (55, "📋 Creating comprehensive summary..."),
            (70, "✅ Extracting actionable items..."),
            (80, "🔑 Identifying key decisions..."),
            (90, "❓ Detecting open questions..."),
            (95, "🧠 Building RAG knowledge base..."),
            (100, "✨ Processing complete!")
        ]
        
        for progress, status in steps:
            status_placeholder.markdown(f"<div style='text-align: center; padding: 1rem;'><span style='font-size: 1.2rem;'>{status}</span></div>", unsafe_allow_html=True)
            progress_bar.progress(progress / 100)
            time.sleep(0.3)
        
        # Actual processing
        chunks = process_input(source)
        transcript = transcribe_all(chunks, language)
        title = generate_title(transcript)
        summary = summarize(transcript)
        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)
        rag_chain = build_rag_chain(transcript)
        
        # Clear progress indicators
        status_placeholder.empty()
        progress_bar.empty()
        
        return {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain": rag_chain,
        }
    except Exception as e:
        st.error(f"❌ {str(e)}")
        return None

def main():
    # Animated Header
    st.markdown('<div class="main-header">🎬 AI Video Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #718096; font-size: 1.1rem; margin-top: -0.5rem;">Transform your videos into actionable insights with AI</p>', unsafe_allow_html=True)
    
    # Sidebar with premium design
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div style="font-size: 2.5rem;">⚡</div>
            <div style="font-weight: 700; font-size: 1.2rem; margin-top: 0.5rem;">AI Studio</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">v2.0 Pro</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Input Source")
        
        input_type = st.radio(
            "Select source type",
            ["🌐 YouTube URL", "📁 Local File"],
            index=0,
            label_visibility="collapsed"
        )
        
        source = None
        if "YouTube" in input_type:
            source = st.text_input(
                "YouTube URL",
                placeholder="https://youtube.com/watch?v=...",
                label_visibility="collapsed"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload video/audio",
                type=['mp4', 'mp3', 'wav', 'avi', 'mov', 'm4a', 'mkv'],
                label_visibility="collapsed"
            )
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name}")
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                    tmp.write(uploaded_file.read())
                    source = tmp.name
        
        st.markdown("### 🌍 Language")
        language = st.selectbox(
            "Select language",
            ["English", "Hinglish", "Hindi", "Spanish", "French"],
            index=0
        )
        
        st.markdown("---")
        
        process_btn = st.button(
            "🚀 Process Video",
            use_container_width=True,
            disabled=not source or st.session_state.processing
        )
        
        st.markdown("---")
        
        # Quick stats in sidebar
        if st.session_state.processed and st.session_state.result:
            st.markdown("### 📊 Quick Stats")
            result = st.session_state.result
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Words", len(result['transcript'].split()))
            with col2:
                st.metric("Duration", f"{len(result['transcript'].split()) // 150}m")
        
        st.markdown("---")
        st.caption("🔒 100% Local Processing")
        st.caption(f"⏱️ {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content area
    if process_btn and source:
        st.session_state.processing = True
        st.session_state.processed = False
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🚀 Processing Your Video")
            st.markdown("This might take a few moments...")
            
            result = process_video(source, language)
            
            if result:
                st.session_state.result = result
                st.session_state.processed = True
                st.balloons()
                st.success("✅ Video processed successfully!")
                st.markdown(f"**🎯 Title:** {result['title']}")
            else:
                st.error("❌ Processing failed. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.session_state.processing = False
    
    # Display results with premium UI
    if st.session_state.processed and st.session_state.result:
        result = st.session_state.result
        
        # Status banner
        st.markdown(f"""
        <div class="info-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-weight: 600; font-size: 1.1rem;">🎯 {result['title']}</span>
                </div>
                <div>
                    <span class="status-badge status-success">✅ Complete</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Summary & Stats",
            "📊 Extracted Items",
            "📝 Full Transcript",
            "💬 AI Chat"
        ])
        
        with tab1:
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 📋 AI Summary")
                st.markdown(result['summary'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Analytics")
                
                # Premium metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="font-size: 2.5rem;">📝</div>
                        <div class="metric-value">{}</div>
                        <div class="metric-label">Total Words</div>
                    </div>
                    """.format(len(result['transcript'].split())), unsafe_allow_html=True)
                
                with col_b:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="font-size: 2.5rem;">⏱️</div>
                        <div class="metric-value">{:.1f}</div>
                        <div class="metric-label">Est. Minutes</div>
                    </div>
                    """.format(len(result['transcript'].split()) / 150), unsafe_allow_html=True)
                
                # More metrics
                col_c, col_d = st.columns(2)
                with col_c:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="font-size: 2.5rem;">✅</div>
                        <div class="metric-value">{}</div>
                        <div class="metric-label">Action Items</div>
                    </div>
                    """.format(len(result['action_items'].split('\n')) - 1), unsafe_allow_html=True)
                
                with col_d:
                    st.markdown("""
                    <div class="metric-container">
                        <div style="font-size: 2.5rem;">🔑</div>
                        <div class="metric-value">{}</div>
                        <div class="metric-label">Key Decisions</div>
                    </div>
                    """.format(len(result['key_decisions'].split('\n')) - 1), unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("✅ Action Items", expanded=True):
                    st.markdown('<div style="background: #f0fff4; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">', unsafe_allow_html=True)
                    st.markdown(result['action_items'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("❓ Open Questions", expanded=True):
                    st.markdown('<div style="background: #fef3c7; padding: 1rem; border-radius: 10px; border-left: 4px solid #ed8936;">', unsafe_allow_html=True)
                    st.markdown(result['open_questions'])
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                with st.expander("🔑 Key Decisions", expanded=True):
                    st.markdown('<div style="background: #ebf4ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;">', unsafe_allow_html=True)
                    st.markdown(result['key_decisions'])
                    st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            with st.expander("📝 View Full Transcript", expanded=False):
                st.text_area("", result['transcript'], height=500, key="transcript_full", label_visibility="collapsed")
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("📋 Copy", use_container_width=True):
                        st.success("✅ Copied!")
                with col2:
                    if st.button("⬇️ Download", use_container_width=True):
                        st.download_button(
                            label="Download",
                            data=result['transcript'],
                            file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
        
        with tab4:
            st.markdown("### 💬 Chat with Your Content")
            st.markdown("Ask questions about the video content using AI")
            
            # Chat container
            chat_container = st.container()
            
            with chat_container:
                if not st.session_state.chat_history:
                    st.info("💡 Ask questions about the video content. Example: 'What were the main points discussed?'")
                
                for msg in st.session_state.chat_history:
                    if msg['role'] == 'user':
                        st.markdown(f"""
                        <div class="chat-user">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.2rem;">👤</span>
                                <span>{msg['content']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chat-assistant">
                            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                                <span style="font-size: 1.2rem;">🤖</span>
                                <span>{msg['content']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Chat input area
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    question = st.text_input(
                        "Ask a question",
                        key="chat_input",
                        placeholder="💬 What would you like to know?",
                        label_visibility="collapsed"
                    )
                with col2:
                    ask_btn = st.button("Send", use_container_width=True)
            
            if ask_btn and question:
                if st.session_state.result.get('rag_chain'):
                    from core.rag_engine import ask_question
                    st.session_state.chat_history.append({'role': 'user', 'content': question})
                    
                    with st.spinner("🤔 Analyzing and generating response..."):
                        answer = ask_question(st.session_state.result['rag_chain'], question)
                    
                    st.session_state.chat_history.append({'role': 'assistant', 'content': answer})
                    st.rerun()
                else:
                    st.warning("⚠️ RAG system not available. Please process a video first.")
            
            if st.session_state.chat_history:
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("🗑️ Clear Chat", use_container_width=True):
                        st.session_state.chat_history = []
                        st.rerun()
                with col2:
                    if st.button("💾 Save Chat", use_container_width=True):
                        chat_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.chat_history])
                        st.download_button(
                            label="Download",
                            data=chat_text,
                            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

if __name__ == "__main__":
    main()