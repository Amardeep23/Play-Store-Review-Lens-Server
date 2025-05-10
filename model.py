import json
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from transformers import pipeline
from collections import Counter
import asyncio

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    return_all_scores=True
)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [tok for tok in text.split() if tok not in stop_words]
    return ' '.join(tokens)

async def analyze_sentiment_for_review(text: str, semaphore):
    # Use semaphore to limit concurrent processing
    async with semaphore:
        out = sentiment_pipeline(text[:512])[0]
        neg = next(x['score'] for x in out if x['label'] == 'NEGATIVE')
        pos = next(x['score'] for x in out if x['label'] == 'POSITIVE')
        pol = pos - neg

        if pol >= 0.5:
            cat = "Very positive"
        elif pol >= 0.1:
            cat = "Positive"
        elif pol > -0.1:
            cat = "Neutral"
        elif pol > -0.5:
            cat = "Negative"
        else:
            cat = "Very negative"

        return pol, cat

async def analyze_sentiment_from_json(data: dict):
    sentences = [r['snippet'] for r in data.get('reviews', [])]
    df = pd.DataFrame({'text': sentences})
    df['clean'] = df['text'].apply(clean_text)

    
    semaphore = asyncio.Semaphore(10)  
    tasks = [analyze_sentiment_for_review(txt, semaphore) for txt in df['clean']]
    

    sentiment_results = await asyncio.gather(*tasks)
    
    
    df['polarity'], df['category'] = zip(*sentiment_results)

    avg_pol = df['polarity'].mean()
    category_counts = df['category'].value_counts().to_dict()

   
    word_freq = Counter(' '.join(df['clean']).split()).most_common(10)
    avg_length = df['clean'].str.split().apply(len).mean()
    length_distribution = df['clean'].str.split().apply(len).value_counts().to_dict()

    return df, avg_pol, category_counts, word_freq, avg_length, length_distribution
