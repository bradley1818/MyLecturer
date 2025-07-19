import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

def get_text_from_youtube(url):
    """Extracts the full text transcript from a YouTube video URL."""
    try:
        # Extracts the video ID from a standard YouTube URL
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        # Extracts the video ID from a short YouTube URL
        elif "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
        else:
            return "Error: Invalid YouTube URL format."

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        return f"Error fetching YouTube transcript: {e}"

def get_text_from_article(url):
    """Extracts the main paragraph text from a web article URL."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = " ".join([p.get_text() for p in paragraphs])
        if not article_text:
            return "Error: Could not find any paragraph text on this page."
        return article_text
    except Exception as e:
        return f"Error fetching article content: {e}"

def generate_lesson(persona, text_content, api_key):
    """Generates a lesson from a given persona and text content using the Gemini API."""
    if not text_content or text_content.startswith("Error"):
        return text_content

    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert teacher. Your current persona is "{persona}".
        Your task is to explain the following content in your persona's voice.
        Make it clear, engaging, and insightful. Break it down into key points using markdown for formatting.
        Use headings, bold text, and bullet points to structure your lesson.

        Here is the content to teach:
        ---
        {text_content}
        ---

        Now, please provide your lesson as {persona}:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with the AI model: {e}"
