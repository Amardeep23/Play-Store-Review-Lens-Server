from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import scrape
import model
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AppRequest(BaseModel):
    app_name: str

@app.post("/fetch_reviews/")
async def fetch_reviews(request: AppRequest):
    try:
        
        review_data = scrape.fetch_google_play_reviews(request.app_name)
        
        
        df, avg_pol, category_counts, word_freq, avg_length, length_distribution = await model.analyze_sentiment_from_json(review_data)

        # Categorize overall sentiment based on average polarity
        if avg_pol >= 0.5:
            overall_sentiment = "Very positive"
        elif avg_pol >= 0.1:
            overall_sentiment = "Positive"
        elif avg_pol > -0.1:
            overall_sentiment = "Neutral"
        elif avg_pol > -0.5:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Very negative"

        
        result = {
            "message": "Reviews fetched and analyzed successfully.",
            "summary": {
                "average_polarity": avg_pol,
                "overall_sentiment": overall_sentiment,
                "category_counts": category_counts
            },
            "analytics": {
                "most_common_words": word_freq,
                "average_review_length": avg_length,
                "length_distribution": length_distribution
            },
            "reviews": df.to_dict(orient='records')
        }

        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred.")
