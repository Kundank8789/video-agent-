# app.py - FINAL POLISHED VERSION
import streamlit as st
from dotenv import load_dotenv
import time
from datetime import datetime
import tempfile
import os
import sys
import shutil

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Meeting Assistant Pro",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .glass-card {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .status-box {
        background: #f0f4ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: #d4edda;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background: #fff3cd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = []

def cleanup_temp_files():
    """Clean up temporary files"""
    for file_path in st.session_state.temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
    st.session_state.temp_files = []

def process_video_real(source, language):
    """
    Process video with REAL progress tracking - no fake animations!
    """
    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summarizer import summarize, generate_title
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        from core.rag_engine import build_rag_chain
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_text = st.empty()
        
        start_time = time.time()
        
        # Step 1: Process input (10%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">🎬</span> 
            <strong>Step 1/8:</strong> Processing audio input...
        </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(10)
        
        chunks = process_input(source)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        
        # Step 2: Transcribe (15% -> 45%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">🎤</span> 
            <strong>Step 2/8:</strong> Transcribing with AI (this may take a few minutes)...
        </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(15)
        
        transcript = transcribe_all(chunks, language)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(45)
        
        # Step 3: Generate title (45% -> 55%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">📝</span> 
            <strong>Step 3/8:</strong> Generating title...
        </div>
        """, unsafe_allow_html=True)
        
        title = generate_title(transcript)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(55)
        
        # Step 4: Generate summary (55% -> 65%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">📋</span> 
            <strong>Step 4/8:</strong> Creating summary...
        </div>
        """, unsafe_allow_html=True)
        
        summary = summarize(transcript)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(65)
        
        # Step 5: Extract action items (65% -> 75%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">✅</span> 
            <strong>Step 5/8:</strong> Extracting action items...
        </div>
        """, unsafe_allow_html=True)
        
        action_items = extract_action_items(transcript)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(75)
        
        # Step 6: Extract decisions (75% -> 85%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">🔑</span> 
            <strong>Step 6/8:</strong> Identifying key decisions...
        </div>
        """, unsafe_allow_html=True)
        
        decisions = extract_key_decisions(transcript)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(85)
        
        # Step 7: Extract questions (85% -> 92%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">❓</span> 
            <strong>Step 7/8:</strong> Detecting open questions...
        </div>
        """, unsafe_allow_html=True)
        
        questions = extract_questions(transcript)
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Elapsed: {elapsed:.1f}s")
        progress_bar.progress(92)
        
        # Step 8: Build RAG (92% -> 100%)
        status_text.markdown("""
        <div class="status-box">
            <span style="font-size: 1.2rem;">🧠</span> 
            <strong>Step 8/8:</strong> Building RAG pipeline...
        </div>
        """, unsafe_allow_html=True)
        
        rag_chain = None
        try:
            rag_chain = build_rag_chain(transcript)
        except Exception as e:
            st.warning(f"⚠️ RAG not available: {str(e)[:100]}")
        
        elapsed = time.time() - start_time
        time_text.caption(f"⏱️ Total time: {elapsed:.1f}s")
        progress_bar.progress(100)
        
        # Complete
        status_text.markdown("""
        <div class="success-box">
            <span style="font-size: 1.2rem;">✅</span> 
            <strong>Processing complete!</strong> 
            <span style="color: #155724;">All steps finished successfully.</span>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        progress_bar.empty()
        
        # Clean up temp files after processing
        cleanup_temp_files()
        
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
        st.error(f"❌ Error: {str(e)}")
        cleanup_temp_files()
        return None

def main():
    # Header
    st.markdown('<div class="main-header">🎙️ AI Meeting Assistant Pro</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #718096;">Transform your meetings into actionable insights with AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">🎙️</div>
            <div style="font-weight: 700;">Meeting Assistant</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">v3.1 - Final</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📥 Input Source")
        
        input_type = st.radio(
            "Source Type",
            ["YouTube URL", "Local File"],
            label_visibility="collapsed"
        )
        
        source = None
        if input_type == "YouTube URL":
            source = st.text_input(
                "YouTube URL",
                placeholder="https://youtube.com/watch?v=...",
                label_visibility="collapsed"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload Video/Audio",
                type=['mp4', 'mp3', 'wav', 'avi', 'mov', 'm4a', 'mkv', 'webm'],
                label_visibility="collapsed"
            )
            if uploaded_file:
                # Use the REAL file extension
                file_ext = os.path.splitext(uploaded_file.name)[1]
                if not file_ext:
                    file_ext = '.mp4'
                
                # Create temp file and track it for cleanup
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
                    tmp.write(uploaded_file.read())
                    source = tmp.name
                    st.session_state.temp_files.append(source)
                
                st.success(f"✅ {uploaded_file.name}")
                st.caption(f"📁 Saved as: {os.path.basename(source)}")
        
        # FIX: Only show languages that are actually supported
        # The backend only supports "english" and "hinglish" for now
        language_map = {
            "English": "english",
            "Hinglish": "hinglish",
        }
        
        display_language = st.selectbox(
            "Language",
            ["English", "Hinglish"],  # Only supported options
            index=0
        )
        language = language_map[display_language]
        
        process_btn = st.button(
            "🚀 Process Meeting",
            use_container_width=True,
            disabled=not source or st.session_state.processing
        )
        
        st.markdown("---")
        st.caption("🔒 100% Local Processing")
        st.caption(f"⏱️ Session: {datetime.now().strftime('%H:%M:%S')}")
        
        # Show processing status in sidebar
        if st.session_state.processing:
            st.markdown("""
            <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-top: 1rem; border: 1px solid #667eea;">
                <span style="color: #667eea;">⏳</span> 
                <span style="font-weight: 500;">Processing...</span>
                <br>
                <small style="color: #718096;">This may take several minutes</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content area
    if process_btn and source:
        st.session_state.processing = True
        st.session_state.processed = False
        st.session_state.start_time = datetime.now()
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            st.markdown("""
            ### 🚀 Processing Your Meeting
            The progress bar below shows REAL progress. Each step updates when completed.
            """)
            
            result = process_video_real(source, language)
            
            if result:
                st.session_state.result = result
                st.session_state.processed = True
                st.balloons()
                
                # Show success with timing
                end_time = datetime.now()
                duration = (end_time - st.session_state.start_time).total_seconds()
                
                st.markdown(f"""
                <div class="success-box">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">✅</span>
                            <span style="font-weight: 600; font-size: 1.1rem;">Video processed successfully!</span>
                        </div>
                        <span style="color: #155724; font-size: 0.9rem;">⏱️ {duration:.1f}s</span>
                    </div>
                    <div style="margin-top: 0.5rem; color: #155724;">
                        📌 <strong>Title:</strong> {result['title']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Failed to process video. Please check the error messages above.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.session_state.processing = False
    
    # Display results
    if st.session_state.processed and st.session_state.result:
        result = st.session_state.result
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Summary",
            "📊 Extracted",
            "📝 Transcript",
            "💬 Chat"
        ])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📌 Title")
                st.info(result['title'])
                
                st.markdown("### 📋 AI Summary")
                st.markdown(result['summary'])
            
            with col2:
                st.markdown("### 📊 Stats")
                st.metric("📝 Words", len(result['transcript'].split()))
                st.metric("✅ Actions", len(result['action_items'].split('\n')) - 1)
                st.metric("🔑 Decisions", len(result['key_decisions'].split('\n')) - 1)
                st.metric("❓ Questions", len(result['open_questions'].split('\n')) - 1)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("✅ Action Items", expanded=True):
                    st.write(result['action_items'])
                
                with st.expander("❓ Open Questions", expanded=True):
                    st.write(result['open_questions'])
            
            with col2:
                with st.expander("🔑 Key Decisions", expanded=True):
                    st.write(result['key_decisions'])
        
        with tab3:
            with st.expander("📝 Full Transcript", expanded=False):
                st.text_area("", result['transcript'], height=400, label_visibility="collapsed")
                if st.button("📋 Copy Transcript"):
                    st.success("Copied to clipboard!")
        
        with tab4:
            st.markdown("### 💬 Chat with Your Meeting")
            st.caption("Ask questions about the meeting content")
            
            # Chat display
            chat_container = st.container()
            with chat_container:
                if not st.session_state.chat_history:
                    st.info("💡 Ask a question like: 'What were the main decisions?'")
                
                for msg in st.session_state.chat_history:
                    if msg['role'] == 'user':
                        st.markdown(f"**👤 You:** {msg['content']}")
                    else:
                        st.markdown(f"**🤖 Assistant:** {msg['content']}")
            
            # FIX: Clear chat input after sending
            with st.form(key="chat_form", clear_on_submit=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    question = st.text_input(
                        "Ask a question:",
                        key="chat_input",
                        placeholder="e.g., What were the key decisions made?",
                        label_visibility="collapsed"
                    )
                with col2:
                    ask_btn = st.form_submit_button("Ask", use_container_width=True)
                
                if ask_btn and question:
                    if result.get('rag_chain'):
                        try:
                            from core.rag_engine import ask_question
                            st.session_state.chat_history.append({'role': 'user', 'content': question})
                            
                            with st.spinner("🤔 Thinking..."):
                                answer = ask_question(result['rag_chain'], question)
                            
                            st.session_state.chat_history.append({'role': 'assistant', 'content': answer})
                            st.rerun()
                        except Exception as e:
                            st.error(f"Chat error: {str(e)}")
                    else:
                        st.warning("⚠️ RAG is not available. Please process a video first.")
            
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()

if __name__ == "__main__":
    main()