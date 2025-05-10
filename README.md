# Google Play Store Review Sentiment Analyzer

This project fetches reviews for any app from the Google Play Store and performs sentiment analysis using a modern NLP model. It exposes a FastAPI backend for fetching and analyzing reviews and provides endpoints for integration with a frontend dashboard.

## Features

- Fetches reviews of any app from the Google Play Store

- Cleans and preprocesses review text

- Performs sentiment analysis using a transformer model

- Categorizes reviews as Very Positive, Positive, Neutral, Negative, or Very Negative

- Provides analytics such as most common words and review length distribution

- REST API with FastAPI

## Tech Stack

- Backend: Python, FastAPI

- NLP: HuggingFace Transformers, NLTK

- Scraping: serpapi, google-play-scraper

- Data Processing: pandas

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.8+

- SerpAPI API Key (for fetching Google Play reviews)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/play-store-sentiment-analyzer.git

2. Navigate to the project directory:
   ```bash
   cd play-store-sentiment-analyzer
  
3. Create and activate a virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
5. Create a .env file in the root directory and configure:
    ```bash
    SerpAPI_Key=your_serpapi_key_here

## Running the App

Start the server:

    uvicorn server:app --reload



The API will be available at http://localhost:8000.

### API Usage
POST /fetch_reviews/

- Body: { "app_name": "app name here" }

- Response: JSON with sentiment summary, analytics, and reviews

Example Request:

    curl -X POST "http://localhost:8000/fetch_reviews/" -H 
    "Content-Type: application/json" -d '{"app_name": "Instagram"}'


## Error Handling
The API uses consistent error handling with proper HTTP status codes:

- **400 Bad Request**: Invalid input or missing required fields.
- **404 Not Found**: App not found or no reviews available
- **500 Internal Server Error**: An unexpected error occurred on the server.
- **502 Bad Gateway** - Errors communicating with external APIs.
- **503 Service Unavailable**: The server is temporarily unavailable (e.g., under maintenance).



## License
This project is licensed under the MIT License. See the LICENSE file for details.

