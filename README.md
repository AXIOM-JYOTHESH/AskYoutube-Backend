# AskYoutube Backend

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.2+-green.svg)](https://fastapi.tiangolo.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-red.svg)](https://www.pinecone.io/)
[![Mistral AI](https://img.shields.io/badge/MistralAI-LLM-purple.svg)](https://mistral.ai/)

A lightweight, robust Retrieval-Augmented Generation (RAG) backend service that enables AI-powered question answering on YouTube video transcripts. Built with FastAPI, Pinecone vector database, and Mistral AI, this system provides accurate, context-aware responses to questions about YouTube video content with zero bloat.

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
  - [Load Video Transcripts](#load-video-transcripts)
  - [Ask Questions](#ask-questions)
  - [Error Response Format](#error-response-format)
- [Architecture & Components](#architecture--components)
- [Performance & Optimization](#performance--optimization)
- [Folder Structure](#folder-structure)
- [Contact / Credits](#contact--credits)

---

## Features

- **YouTube Transcript Processing**: Automatically fetch and process video transcripts from YouTube
- **Multi-Language Support**: Supports English, Hindi, and Gujarati language transcripts
- **Vector Database Storage**: Efficient storage and retrieval using Pinecone vector database
- **AI-Powered Q&A**: Use Mistral AI LLM for generating accurate answers based on video content
- **Advanced Retrieval**: Multi-query retrieval with LangChain for better context finding
- **Metadata Management**: MongoDB storage for video processing status and metadata
- **FastAPI Backend**: High-performance async API with automatic OpenAPI documentation
- **Text Chunking**: Intelligent text splitting for optimal vector embeddings
- **Error Handling**: Comprehensive error handling with structured responses
- **Scalable Architecture**: Modular design supporting easy extension and scaling

---

## Technology Stack

- **Language:** Python 3.13+
- **Framework:** FastAPI (async web framework)
- **AI/ML:**
  - Mistral AI (LLM and embeddings)
  - Pinecone (Vector database)
- **Database:** MongoDB (metadata storage)
- **APIs:** YouTube Transcript API
- **Other:** Pydantic (data validation), Uvicorn (ASGI server)

---

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) (v3.13 or higher)
- [MongoDB](https://www.mongodb.com/) (local or cloud instance like MongoDB Atlas)
- [Pinecone](https://www.pinecone.io/) account and API key
- [Mistral AI](https://mistral.ai/) API key

### Installation

```bash
git clone https://github.com/AXIOM-JYOTHESH/AskYoutube-Backend.git
cd AskYoutube-Backend
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/youtube_rag

# Mistral AI Configuration
MISTRAL_API_KEY=your_mistral_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
```

| Variable         | Description                    | Required |
| ---------------- | ------------------------------ | -------- |
| MONGO_URI        | MongoDB connection string      | Yes      |
| MISTRAL_API_KEY  | Mistral AI API key             | Yes      |
| PINECONE_API_KEY | Pinecone API key               | Yes      |

### Running the Project

```bash
# Activate virtual environment (if not already activated)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`.

---

## API Documentation

The API provides two main endpoints for loading video transcripts and asking questions.

### Load Video Transcripts

- **POST** `/api/load`
- **Description:** Load and process transcripts for a YouTube video, storing them in the vector database for future queries.
- **Request Body:**
  ```json
  {
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "success": true,
    "message": "Transcripts Available"
  }
  ```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/load" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Ask Questions

- **GET** `/api/ask`
- **Description:** Ask a question about one or more YouTube videos and receive an AI-generated answer based on their transcripts.
- **Query Parameters:**
  - `url`: Array of YouTube URLs (can be multiple videos)
  - `question`: The question to ask about the video content
- **Request Example:**
  ```
  GET /api/ask?url=https://www.youtube.com/watch?v=VIDEO_ID1&url=https://www.youtube.com/watch?v=VIDEO_ID2&question=What is the main topic discussed?
  ```
- **Response:** `200 OK`
  ```json
  {
    "success": true,
    "message": "This video discusses the fundamentals of machine learning, covering topics like supervised and unsupervised learning algorithms, neural networks, and practical applications in various industries."
  }
  ```

**Example Request:**

```bash
curl "http://localhost:8000/api/ask?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&question=What is this video about?"
```

### Error Response Format

All errors follow a consistent structure:

```json
{
  "success": false,
  "message": "Error message describing what went wrong"
}
```

---

## Architecture & Components

### Core Components

- **Transcript Loader**: Fetches YouTube transcripts using the YouTube Transcript API
- **Text Splitter**: Intelligently chunks transcript text for optimal embedding
- **Vector Store**: Pinecone-based storage for semantic search
- **LLM Integration**: Mistral AI for question answering
- **Multi-Query Retrieval**: Enhances search by generating multiple query variations
- **Metadata Database**: MongoDB for tracking processed videos

### Data Flow

1. **Video Loading**: User provides YouTube URL -> Transcript fetched -> Text chunked -> Embeddings created -> Stored in Pinecone
2. **Question Answering**: User asks question -> Semantic search in Pinecone -> Relevant chunks retrieved -> Context passed to Mistral LLM -> Answer generated

### Supported Languages

- English (en)
- Hindi (hi)
- Gujarati (gu)

---

## Performance & Optimization

- **FastAPI Async Core**: Async architecture for high concurrency and low latency
- **Direct Native SDKs**: Zero LangChain bloat for maximum performance and reliability
- **Pinecone Serverless Index**: Fast cosine similarity search across 1024-dimension vectors
- **Batch Embeddings & Retry**: Automatic chunk batching and backoff against rate limits
- **MongoDB Atlas Storage**: Lightweight metadata persistence and duplicate index avoidance
- **Interactive Web UI**: Standalone dashboard with live video player and chat interface

---

## Folder Structure

```text
AskYoutube-Backend/
|-- main.py                          # FastAPI application entry point & UI host
|-- pyproject.toml                   # Project configuration and dependencies
|-- requirements.txt                 # Python dependencies
|-- README.md                        # Project documentation
|-- .env.example                     # Example environment variables
|-- static/
|   `-- index.html                   # Interactive web dashboard UI
|-- app/
|   |-- components/                  # Core RAG components
|   |   |-- models.py                # Mistral AI LLM and embedding integration
|   |   |-- pinecone.py              # Pinecone vector index management
|   |   |-- prompt.py                # RAG prompt templates
|   |   |-- textsplitter.py          # Intelligent text chunking
|   |   |-- utils.py                 # URL parsing (youtu.be, watch, shorts)
|   |   |-- vector_store.py          # Pinecone upsert & similarity search
|   |   |-- youtube_transcripts_loader.py  # YouTube transcript extractor
|   |   `-- output_parser.py         # Response parsing
|   |-- db/
|   |   `-- config.py                # MongoDB Atlas configuration
|   |-- models/
|   |   `-- schemas.py               # Pydantic request/response models
|   |-- routes/
|   |   `-- api.py                   # API routes (/api/load, /api/ask)
|   `-- services/
|       `-- youtube.py               # Business logic for YouTube operations
|-- __pycache__/                     # Python bytecode cache
`-- .venv/                           # Virtual environment
```

---
## Contact / Credits

- **Author:** [Kodem Jyothesh Kumar Dora](mailto:humblemeetup@gmail.com)
- **GitHub:** [AXIOM-JYOTHESH](https://github.com/AXIOM-JYOTHESH)
- **LinkedIn:** [linkedin.com/in/jyotheshkumar](https://www.linkedin.com/in/jyotheshkumar/)

---