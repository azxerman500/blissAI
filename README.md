# ✨ Bliss AI

Bliss AI is a lightweight, high-performance AI assistant built with **Python** and **NVIDIA's Nemotron** model. It features a modern dark-mode web interface and is designed to be deployed as a serverless application on Vercel with **zero pip dependencies**.

## 🚀 Features

-   **NVIDIA Powered:** Uses the `nemotron-3-super-free` model for intelligent, fast responses.
-   **Zero-Install Backend:** Built using Python's standard `urllib` and `http.server` libraries—no `pip install` required.
-   **Modern UI:** A responsive, dark-themed chat interface.
-   **Serverless Ready:** Optimized for deployment on Vercel's Edge/Serverless functions.
-   **Cost-Effective:** Utilizes OpenRouter's free-tier models.

## 🛠️ Project Structure

```
bliss-ai/
├── api/
│   └── chat.py      # Python Serverless Function (The Brain)
├── index.html       # Frontend Chat Interface (The Face)
└── README.md        # Documentation
