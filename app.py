import streamlit as st
import os
try:
    from dotenv import load_dotenv
except Exception:
    # Allow app to start even if python-dotenv is not installed in the environment.
    def load_dotenv(*args, **kwargs):
        return None
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Import backend modules
from backend.response_generator import ResponseGenerator
from backend.mood_tracker import MoodTracker
from utils.helpers import (
    get_daily_wellness_tip,
    get_time_based_greeting,
    generate_session_id,
    get_emotion_suggestion,
    format_timestamp
)

# Import new feature modules
try:
    from utils.voice_handler import VoiceHandler, SUPPORTED_LANGUAGES
    VOICE_AVAILABLE = True
except Exception:
    VOICE_AVAILABLE = False
    print("Voice features unavailable - install SpeechRecognition and PyAudio")

try:
    from utils.translator import TranslationHandler, LANGUAGE_EMOJIS
    TRANSLATION_AVAILABLE = True
except Exception:
    TRANSLATION_AVAILABLE = False
    print("Translation features unavailable - install googletrans")

from utils.journal_exporter import JournalExporter

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="MindfulCompanion - AI Wellness Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #F5F5F5;
        margin-right: 2rem;
    }
    .emotion-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .wellness-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #4A90E2;
    }
    .quick-button {
        margin: 0.25rem;
    }
    .crisis-alert {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []
    st.session_state.session_id = generate_session_id()
    st.session_state.mood_tracker = MoodTracker()
    
    # Get API key from environment or user input
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    st.session_state.response_generator = ResponseGenerator(api_key)
    
    st.session_state.daily_tip = get_daily_wellness_tip()
    
    # Initialize feature modules
    st.session_state.journal_exporter = JournalExporter(st.session_state.mood_tracker)
    
    if VOICE_AVAILABLE:
        st.session_state.voice_handler = VoiceHandler()
    else:
        st.session_state.voice_handler = None
    
    if TRANSLATION_AVAILABLE:
        st.session_state.translator = TranslationHandler()
    else:
        st.session_state.translator = None
    
    # Feature flags
    st.session_state.voice_enabled = VOICE_AVAILABLE
    st.session_state.translation_enabled = TRANSLATION_AVAILABLE
    st.session_state.user_language = "en"
    st.session_state.show_dashboard = False

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 MindfulCompanion")
    st.markdown("---")
    
    # API Key input (if not in environment)
    if not os.getenv("HUGGINGFACE_API_KEY"):
        api_key_input = st.text_input(
            "Hugging Face API Key (Optional)",
            type="password",
            help="Enter your Hugging Face API key for better responses. Get one at https://huggingface.co/settings/tokens"
        )
        if api_key_input:
            st.session_state.response_generator = ResponseGenerator(api_key_input)
            st.success("✅ API key configured!")
    else:
        st.success("✅ API key loaded from environment")
    
    st.markdown("---")
    
    # 🌍 LANGUAGE SELECTOR
    if st.session_state.translation_enabled:
        st.markdown("### 🌍 Language / Idioma")
        languages = st.session_state.translator.get_popular_languages()
        
        selected_lang = st.selectbox(
            "Select your language:",
            options=list(languages.keys()),
            index=0,
            key="language_selector"
        )
        
        st.session_state.user_language = languages[selected_lang]
        
        if st.session_state.user_language != "en":
            lang_emoji = LANGUAGE_EMOJIS.get(st.session_state.user_language, "🌐")
            st.info(f"{lang_emoji} Translation enabled for {selected_lang}")
        
        st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    
    # Display mood statistics
    mood_stats = st.session_state.mood_tracker.get_mood_statistics(days=7)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Chats", mood_stats.get("total_entries", 0))
    with col2:
        dominant = mood_stats.get("dominant_emotion", "neutral")
        st.metric("Main Mood", dominant.title())
    
    # View mood history button
    if st.button("📈 View Mood History", use_container_width=True):
        st.session_state.show_dashboard = True
    
    # 📥 EXPORT JOURNAL SECTION
    st.markdown("---")
    st.markdown("### 📥 Export Journal")
    
    if st.session_state.journal_exporter is not None:
        export_format = st.selectbox(
            "Export format:",
            ["JSON", "CSV", "Text Report", "Conversation Log"],
            key="export_format"
        )
        
        if st.button("📥 Export My Journal", use_container_width=True, type="primary"):
            with st.spinner("Preparing export..."):
                if export_format == "JSON":
                    data = st.session_state.journal_exporter.export_json(days=30)
                    filename = st.session_state.journal_exporter.get_export_filename("json")
                    st.download_button(
                        "💾 Download JSON",
                        data=data,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )
                
                elif export_format == "CSV":
                    data = st.session_state.journal_exporter.export_csv(days=30)
                    filename = st.session_state.journal_exporter.get_export_filename("csv")
                    st.download_button(
                        "💾 Download CSV",
                        data=data,
                        file_name=filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                
                elif export_format == "Text Report":
                    data = st.session_state.journal_exporter.export_text_report(days=30)
                    filename = st.session_state.journal_exporter.get_export_filename("txt")
                    st.download_button(
                        "💾 Download Report",
                        data=data,
                        file_name=filename,
                        mime="text/plain",
                        use_container_width=True
                    )
                
                elif export_format == "Conversation Log":
                    data = st.session_state.journal_exporter.export_conversation_log(
                        st.session_state.messages
                    )
                    filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    st.download_button(
                        "💾 Download Conversation",
                        data=data,
                        file_name=filename,
                        mime="text/plain",
                        use_container_width=True
                    )
    else:
        st.info("📥 Export feature unavailable")
    
    # Reset conversation
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.response_generator.reset_conversation()
        st.session_state.session_id = generate_session_id()
        st.rerun()
    
    st.markdown("---")
    
    # 🎤 VOICE INPUT SECTION
    if st.session_state.voice_enabled:
        st.markdown("### 🎤 Voice Input")
        
        # Language selection for voice
        voice_lang_name = st.selectbox(
            "Voice language:",
            list(SUPPORTED_LANGUAGES.keys()),
            key="voice_language"
        )
        voice_lang_code = SUPPORTED_LANGUAGES[voice_lang_name]
        
        # Microphone test
        if st.button("🔊 Test Microphone", use_container_width=True):
            success, msg = st.session_state.voice_handler.test_microphone()
            if success:
                st.success(msg)
            else:
                st.error(msg)
        
        st.markdown("---")
    
    st.markdown("### ⚕️ Important")
    st.info("""
    **This is NOT a replacement for professional mental health care.**
    
    If you're in crisis:
    - Call 988 (Suicide & Crisis Lifeline)
    - Text HOME to 741741 (Crisis Text Line)
    - Call 911 for emergencies
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    MindfulCompanion is an AI-powered wellness chatbot designed to provide:
    - Emotional support
    - Active listening
    - Wellness tips
    - Mood tracking
    
    *Not medical advice*
    """)

# Main content area
if 'show_dashboard' in st.session_state and st.session_state.show_dashboard:
    # Mood Dashboard View
    st.markdown("<h1 class='main-header'>📊 Mood Dashboard</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Chat"):
        st.session_state.show_dashboard = False
        st.rerun()
    
    # Get mood data
    mood_stats = st.session_state.mood_tracker.get_mood_statistics(days=30)
    mood_trends = st.session_state.mood_tracker.get_mood_trends(days=30)
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <h3>{mood_stats.get('total_entries', 0)}</h3>
            <p>Total Entries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        dominant = mood_stats.get('dominant_emotion', 'neutral')
        st.markdown(f"""
        <div class='stat-card'>
            <h3>{dominant.title()}</h3>
            <p>Dominant Emotion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_conf = mood_stats.get('average_confidence', 0)
        st.markdown(f"""
        <div class='stat-card'>
            <h3>{avg_conf}</h3>
            <p>Avg Confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        trend = mood_trends.get('trend', 'stable')
        st.markdown(f"""
        <div class='stat-card'>
            <h3>{trend.title()}</h3>
            <p>Trend</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emotion Distribution")
        emotion_dist = mood_stats.get('emotion_distribution', {})
        if emotion_dist:
            fig = px.pie(
                names=list(emotion_dist.keys()),
                values=list(emotion_dist.values()),
                title="Emotions Over Last 30 Days"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Breakdown")
        sentiment_dist = mood_stats.get('sentiment_distribution', {})
        if sentiment_dist:
            fig = px.bar(
                x=list(sentiment_dist.keys()),
                y=list(sentiment_dist.values()),
                title="Sentiment Distribution",
                labels={'x': 'Sentiment', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("---")
    st.subheader("💡 Insights")
    insights = mood_trends.get('insights', [])
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("Keep chatting to generate personalized insights!")
    
    # Recent mood history
    st.markdown("---")
    st.subheader("📜 Recent Mood Logs")
    recent_moods = st.session_state.mood_tracker.get_recent_moods(days=30, limit=20)
    if not recent_moods.empty:
        st.dataframe(
            recent_moods[['date', 'time', 'emotion', 'sentiment', 'intensity', 'message_preview']],
            use_container_width=True
        )
    else:
        st.info("No mood data yet. Start chatting to track your mood!")

else:
    # Chat Interface View
    st.markdown("<h1 class='main-header'>🧠 MindfulCompanion</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Your AI-powered mental wellness companion</p>", unsafe_allow_html=True)
    
    # Daily wellness tip card
    st.markdown(f"""
    <div class='wellness-card'>
        <h3>💡 Daily Wellness Tip</h3>
        <p>{st.session_state.daily_tip}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            # Welcome message
            greeting = get_time_based_greeting()
            st.markdown(f"""
            <div class='chat-message bot-message'>
                <strong>MindfulCompanion</strong> <span style='color: #999;'>{format_timestamp()}</span><br>
                {greeting} I'm here to listen and support you. How are you feeling today?
            </div>
            """, unsafe_allow_html=True)
        
        # Display conversation history
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>You</strong> <span style='color: #999;'>{message.get('timestamp', '')}</span><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                emotion = message.get('emotion', 'neutral')
                emoji = message.get('emoji', '💭')
                color = message.get('color', '#808080')
                
                st.markdown(f"""
                <div class='chat-message bot-message'>
                    <strong>MindfulCompanion</strong> <span style='color: #999;'>{message.get('timestamp', '')}</span>
                    <span class='emotion-badge' style='background-color: {color}20; color: {color};'>
                        {emoji} {emotion.title()}
                    </span><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Quick suggestion buttons
    st.markdown("### 💬 Quick Responses")
    if st.session_state.messages:
        last_emotion = st.session_state.messages[-1].get('emotion', 'neutral')
    else:
        last_emotion = 'neutral'
    
    suggestions = st.session_state.response_generator.get_suggestions(last_emotion)
    
    cols = st.columns(len(suggestions))
    for idx, suggestion in enumerate(suggestions):
        with cols[idx]:
            if st.button(suggestion, key=f"suggestion_{idx}", use_container_width=True):
                # Trigger the suggestion as user input
                user_input = suggestion
                
                # Process the message (same logic as below)
                st.session_state.messages.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': format_timestamp()
                })
                
                with st.spinner("Thinking..."):
                    response_data = st.session_state.response_generator.generate(
                        user_message=user_input,
                        conversation_context=st.session_state.messages
                    )
                    
                    # Log mood
                    st.session_state.mood_tracker.log_mood(
                        emotion=response_data['emotion'],
                        confidence=response_data['emotion_confidence'],
                        sentiment=response_data['sentiment'],
                        intensity=response_data['intensity'],
                        message=user_input,
                        session_id=st.session_state.session_id
                    )
                    
                    # Add bot response
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': response_data['response'],
                        'emotion': response_data['emotion'],
                        'emoji': response_data['emoji'],
                        'color': response_data['color'],
                        'timestamp': format_timestamp()
                    })
                
                st.rerun()
    
    st.markdown("---")
    
    # Voice input section with fallback
    st.markdown("### 💬 Chat Input")
    
    input_col1, input_col2 = st.columns([4, 1])
    
    with input_col1:
        user_input = st.chat_input("Type your message here...")
    
    with input_col2:
        if st.session_state.voice_enabled and st.button("🎤", help="Voice input (text fallback if PyAudio not installed)", use_container_width=True):
            with st.spinner("🎤 Listening..."):
                # Get the selected voice language
                voice_lang_name = st.session_state.get("voice_language", "English (US)")
                voice_lang_code = SUPPORTED_LANGUAGES.get(voice_lang_name, "en-US")
                
                # Attempt voice recognition
                success, text, message = st.session_state.voice_handler.listen(language=voice_lang_code)
                
                if success and text:
                    # Use recognized text as input
                    user_input = text
                    st.success(f"✅ Heard: {text}")
                else:
                    # Show error and provide text fallback option
                    if "PyAudio" in message:
                        st.warning(message)
                        st.info("💡 PyAudio is required for voice input on Windows. For now, please type your message in the chat box above.")
                    else:
                        st.error(message)
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': format_timestamp()
        })
        
        # Generate response
        with st.spinner("Thinking..."):
            response_data = st.session_state.response_generator.generate(
                user_message=user_input,
                conversation_context=st.session_state.messages
            )
            
            # Check if crisis detected
            if response_data.get('metadata', {}).get('is_crisis', False):
                st.markdown("""
                <div class='crisis-alert'>
                    <h4>⚠️ Crisis Resources</h4>
                    <p>It seems you might be going through a crisis. Please reach out to professional help immediately.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Log mood
            st.session_state.mood_tracker.log_mood(
                emotion=response_data['emotion'],
                confidence=response_data['emotion_confidence'],
                sentiment=response_data['sentiment'],
                intensity=response_data['intensity'],
                message=user_input,
                session_id=st.session_state.session_id
            )
            
            # Add bot response
            st.session_state.messages.append({
                'role': 'assistant',
                'content': response_data['response'],
                'emotion': response_data['emotion'],
                'emoji': response_data['emoji'],
                'color': response_data['color'],
                'timestamp': format_timestamp()
            })
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.85rem;'>
    <p>Made with ❤️ for mental wellness | Not a substitute for professional care</p>
    <p>If you're in crisis, call 988 (US) or your local emergency services</p>
</div>
""", unsafe_allow_html=True)
