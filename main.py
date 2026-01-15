from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI(title="Feedback Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./feedback.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FeedbackDB(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    productId = Column(String)
    rating = Column(Integer)
    review = Column(String)
    sentiment = Column(String)
    themes = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

POSITIVE_WORDS = {
    "shiny", "elegant", "premium", "beautiful", "comfortable",
    "sturdy", "durable", "perfect", "loved", "great", "nice"
}
NEGATIVE_WORDS = {
    "tarnish", "dull", "broke", "broken", "heavy", "uncomfortable",
    "cheap", "poor", "bad", "scratch", "fragile"
}

THEMES = {
    "comfort": ["light", "heavy", "fit", "wearable", "comfortable", "size", "tight", "loose"],
    "durability": ["broke", "broken", "strong", "quality", "fragile", "snap", "sturdy", "tarnish"],
    "appearance": ["shiny", "dull", "design", "polish", "beautiful", "look", "color"],
}

class Feedback(BaseModel):
    productId: str
    rating: int
    review: str

def analyze_sentiment(text: str) -> str:
    pos = neg = 0
    words = text.lower().replace(".", "").replace(",", "").split()

    for w in words:
        if w in POSITIVE_WORDS:
            pos += 1
        if w in NEGATIVE_WORDS:
            neg += 1

    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"

def detect_themes(text: str) -> List[str]:
    text = text.lower()
    found = []
    for theme, keys in THEMES.items():
        if any(k in text for k in keys):
            found.append(theme)
    return found

@app.post("/feedback")
def submit_feedback(fb: Feedback, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(fb.review)
    themes = detect_themes(fb.review)

    record = FeedbackDB(
        productId=fb.productId,
        rating=fb.rating,
        review=fb.review,
        sentiment=sentiment,
        themes=",".join(themes)
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Feedback stored successfully"}

@app.get("/reviews/{product_id}")
def get_reviews(product_id: str, db: Session = Depends(get_db)):
    return db.query(FeedbackDB).filter(FeedbackDB.productId == product_id).all()

@app.get("/dashboard/{product_id}")
def dashboard(product_id: str, db: Session = Depends(get_db)):
    rows = db.query(FeedbackDB).filter(FeedbackDB.productId == product_id).all()

    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
    theme_count = {"comfort": 0, "durability": 0, "appearance": 0}

    total_reviews = len(rows)

    for r in rows:
        if r.sentiment in sentiment_count:
            sentiment_count[r.sentiment] += 1

        if r.themes:
            for t in r.themes.split(","):
                if t in theme_count:
                    theme_count[t] += 1

    insights = []
    if total_reviews > 0:
        if (theme_count["durability"] / total_reviews) > 0.3:
            insights.append("Warning: High volume of durability mentions.")

        if (theme_count["comfort"] / total_reviews) > 0.3:
            insights.append("Comfort is a key topic. Consider checking sizing/weight.")

        if sentiment_count["Negative"] > sentiment_count["Positive"]:
            insights.append("Critical: Negative sentiment outweighs positive.")

    return {
        "sentimentCount": sentiment_count,
        "themeCount": theme_count,
        "insights": insights
    }
