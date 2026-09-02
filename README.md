# AskYoutube Backend

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.2+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.13+-orange.svg)](https://www.langchain.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-red.svg)](https://www.pinecone.io/)
[![Mistral AI](https://img.shields.io/badge/MistralAI-LLM-purple.svg)](https://mistral.ai/)

A robust, scalable Retrieval-Augmented Generation (RAG) backend service that enables AI-powered question answering on YouTube video transcripts. Built with FastAPI, LangChain, Pinecone vector database, and Mistral AI, this system provides accurate, context-aware responses to questions about YouTube video content.

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
  - LangChain (RAG pipeline orchestration)
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

1. **Video Loading**: User provides YouTube URL â†’ Transcript fetched â†’ Text chunked â†’ Embeddings created â†’ Stored in Pinecone
2. **Question Answering**: User asks question â†’ Multiple queries generated â†’ Relevant chunks retrieved â†’ Context passed to LLM â†’ Answer generated

### Supported Languages

- English (en)
- Hindi (hi)
- Gujarati (gu)

---

## Performance & Optimization

- **Async Processing**: FastAPI's async capabilities for high concurrency
- **Vector Search**: Efficient similarity search with Pinecone
- **Text Chunking**: Optimized chunk sizes for better retrieval
- **Multi-Query Retrieval**: Improved accuracy through query expansion
- **Caching**: Built-in LangChain caching for repeated queries
- **Database Indexing**: MongoDB indexing for fast metadata lookups

---

## Folder Structure

```
AskYoutube-Backend/
â”œâ”€â”€ main.py                          # FastAPI application entry point
â”œâ”€â”€ pyproject.toml                   # Project configuration and dependencies
â”œâ”€â”€ requirements.txt                 # Python dependencies
â”œâ”€â”€ README.md                        # Project documentation
â”œâ”€â”€ .env                             # Environment variables (create this)
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ components/                  # Core RAG components
â”‚   â”‚   â”œâ”€â”€ models.py                # LLM and embedding model configuration
â”‚   â”‚   â”œâ”€â”€ pinecone.py              # Vector database setup
â”‚   â”‚   â”œâ”€â”€ prompt.py                # Question-answering prompt templates
â”‚   â”‚   â”œâ”€â”€ textsplitter.py          # Text chunking configuration
â”‚   â”‚   â”œâ”€â”€ utils.py                 # Utility functions
â”‚   â”‚   â”œâ”€â”€ vector_store.py          # Vector store wrapper
â”‚   â”‚   â”œâ”€â”€ youtube_transcripts_loader.py  # YouTube transcript fetching
â”‚   â”‚   â””â”€â”€ output_parser.py         # Response parsing
â”‚   â”œâ”€â”€ db/
â”‚   â”‚   â””â”€â”€ config.py                # MongoDB configuration
â”‚   â”œâ”€â”€ models/
â”‚   â”‚   â””â”€â”€ schemas.py               # Pydantic data models
â”‚   â”œâ”€â”€ routes/
â”‚   â”‚   â””â”€â”€ api.py                   # API route definitions
â”‚   â””â”€â”€ services/
â”‚       â””â”€â”€ youtube.py               # Business logic for YouTube operations
â”œâ”€â”€ __pycache__/                     # Python bytecode cache
â””â”€â”€ .venv/                           # Virtual environment (create this)
```

---
## Contact / Credits

- **Author:** [Kodem Jyothesh Kumar Dora](mailto:humblemeetup@gmail.com)
- **GitHub:** [AXIOM-JYOTHESH](https://github.com/AXIOM-JYOTHESH)
- **LinkedIn:** [linkedin.com/in/jyotheshkumar](https://www.linkedin.com/in/jyotheshkumar/)

---