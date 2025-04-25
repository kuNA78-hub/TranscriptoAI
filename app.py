from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import asyncio
import aiohttp
import google.generativeai as genai
import json
import re

# Configure Gemini API with your key
GEMINI_API_KEY = "PUT_YOUR_GEMNI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Transcript Summarizer",
    description="API to fetch and summarize YouTube video transcripts using Gemini.",
    version="1.0.0"
)

# Function to extract video ID from YouTube URL
def extract_youtube_id(url: str) -> str:
    if "youtube.com/watch?v=" in url:
        return url.split("=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL")

# Async function to fetch video title
async def fetch_video_title(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                html = await response.text()
                match = re.search(r"<title>(.*?)</title>", html)
                if match:
                    title = match.group(1).replace(" - YouTube", "").strip()
                    return title
                return "Unknown Title"
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown Title"

# Async function to fetch transcript
async def fetch_youtube_transcript(video_id: str):
    try:
        transcript_list = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: YouTubeTranscriptApi.list_transcripts(video_id)
        )
        transcript = None
        for t in transcript_list:
            transcript = t
            break
        if not transcript:
            raise Exception("No transcript found for this video.")

        original_transcript = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: transcript.fetch()
        )
        return original_transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# Function to process transcript with Gemini API
def summarize_transcript_with_gemini(transcript):
    try:
        transcript_text = "\n".join([f"{entry.start:.2f}s: {entry.text}" for entry in transcript])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze the following YouTube video transcript and provide a concise summary of its key points as a JSON object.
        The JSON should have a "summary" field containing an array of key points.
        Ensure the response is valid JSON without code block markers or extra formatting.
        Example format:
        {{
            "summary": [
                "First key point",
                "Second key point"
            ]
        }}
        Transcript:
        {transcript_text}
        """
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        response_text = re.sub(r'^```json\s*|\s*```$', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r'\n\s*\n', '\n', response_text).strip()
        
        try:
            summary_json = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            summary_json = {"summary": [response.text.strip()]}

        return summary_json
    except Exception as e:
        print(f"Error processing with Gemini: {e}")
        return {"summary": []}

# FastAPI endpoint to summarize YouTube transcript
@app.get("/summarize")
async def get_summary(url: str):
    try:
        video_id = extract_youtube_id(url)
        transcript = await fetch_youtube_transcript(video_id)
        if transcript:
            title = await fetch_video_title(video_id)
            summary = summarize_transcript_with_gemini(transcript)
            return {
                "video_id": video_id,
                "title": title,
                "summary": summary
            }
        else:
            return {"error": "Transcript not found"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Internal server error: {e}"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
