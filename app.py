import streamlit as st
from core_logic import get_text_from_youtube, get_text_from_article, generate_lesson

# --- App Layout ---
st.set_page_config(layout="wide", page_title="AI Virtual Coach")

st.title("🧠 AI Virtual Coach")
st.write("Load knowledge from a YouTube video or web article and learn from a personalized AI teacher.")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("Settings")
    
    # Input for the API Key
    api_key = st.text_input("Enter your Gemini API Key", type="password", help="Get your key from Google AI Studio.")
    
    # Persona selection dropdown
    persona = st.selectbox(
        "1. Choose your coach's persona:",
        ("The Professor", "The Drill Sergeant", "The Dark Humorist", "The Enthusiast")
    )

    # Content URL input
    source_url = st.text_input("2. Enter a YouTube or article URL:")

    # Generate button
    generate_button = st.button("Generate Lesson", use_container_width=True)

# --- Main Content Area ---
if generate_button:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not source_url:
        st.error("Please enter a URL in the sidebar.")
    else:
        # Show a spinner while processing
        with st.spinner("Analyzing content and preparing your lesson... This may take a moment."):
            
            # Step 1: Ingest the data based on URL type
            if "youtube.com" in source_url or "youtu.be" in source_url:
                content = get_text_from_youtube(source_url)
            else:
                content = get_text_from_article(source_url)
            
            # Check if ingestion was successful
            if content.startswith("Error"):
                st.error(content)
            else:
                # Step 2: Generate the lesson with the persona
                lesson = generate_lesson(persona, content, api_key)
                
                # Step 3: Display the output
                if lesson.startswith("Error"):
                    st.error(lesson)
                else:
                    st.subheader(f"Your Lesson from {persona}")
                    st.markdown(lesson)

else:
    st.info("Enter your API key and a URL in the sidebar, then click 'Generate Lesson' to begin.")
