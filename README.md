# 🎥 SummarAIze – YouTube Video Summarization API

**SummarAIze** is a lightweight and powerful API built with **FastAPI** that extracts transcripts from YouTube videos, translates them into English, and generates concise summaries using **Gemini 2.0**.

Ideal for developers, students, and researchers, this project helps you save time by turning long video content into quick, readable insights.

---

## 🚀 Features

- 🎮️ **Transcript Extraction** – Fetch transcripts from any public YouTube video  
- 🌍 **Multilingual Support** – Translate transcripts from any language to English  
- 🧠 **AI Summaries** – Generate human-readable summaries using **Gemini 2.0**  
- ⚡ **FastAPI-Powered** – High-speed, beginner-friendly API framework  
- 🔗 **Real URL Support** – Test with actual YouTube video links

---

## 🔧 Tech Stack

- Python 3.11+  
- FastAPI  
- Gemini 2.0 (via API)  
- YouTube Transcript API  
- Uvicorn (for local server)

---

## ▶️ Getting Started

```bash
git clone https://github.com/your-username/SummarAIze.git
cd SummarAIze
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to try the API.

---

## 📄 Example Request

```json
POST /summarize
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

---

## 🙌 Special Thanks

Thanks to **AI Wallah** for the inspiration and support in building this project.

---

## 📄 License

MIT License

