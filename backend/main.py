from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from instagram_algorithm import ContentItem, InteractionHistory, InstagramStyleRanker, UserProfile

app = FastAPI(
    title="Instagram Algorithm Simulator API",
    description="Educational API for experimenting with Instagram-style content ranking signals.",
    version="1.0.0",
)

class RankRequest(BaseModel):
    user_id: str = "demo-user"
    hour: int = Field(default=19, ge=0, le=23)
    minute: int = Field(default=0, ge=0, le=59)
    followed_creators: list[str] = []
    topic_affinity: dict[str, float] = {}
    creator_affinity: dict[str, float] = {}
    interactions: dict[str, dict[str, float]] = {}
    content: list[dict[str, Any]] = []

def build_history(interactions: dict[str, dict[str, float]]) -> InteractionHistory:
    fields = {
        "watch_ratio": {}, "completion_ratio": {}, "like_rate": {},
        "comment_rate": {}, "share_rate": {}, "save_rate": {},
        "profile_visit_rate": {}, "follow_rate": {}, "skip_rate": {}, "hide_rate": {}
    }
    for item_id, values in interactions.items():
        for field_name in fields:
            if field_name in values:
                fields[field_name][item_id] = values[field_name]
    return InteractionHistory(**fields)

@app.get("/")
def root():
    return {
        "name": "Instagram Algorithm Simulator API",
        "status": "online",
        "docs": "/docs",
        "disclaimer": "Educational simulator; not Instagram's private production algorithm."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rank")
def rank(request: RankRequest):
    now = datetime(2026, 9, 28, request.hour, request.minute, tzinfo=timezone.utc).replace(tzinfo=None)

    user = UserProfile(
        id=request.user_id,
        followed_creators=set(request.followed_creators),
        topic_affinity=request.topic_affinity,
        creator_affinity=request.creator_affinity,
    )
    history = build_history(request.interactions)

    items = [
        ContentItem(
            id=item["id"],
            creator_id=item["creator_id"],
            topic=item.get("topic", "general"),
            format=item.get("format", "reel"),
            duration_s=item.get("duration_s", 30.0),
            quality=item.get("quality", 0.7),
            originality=item.get("originality", 0.8),
            language_match=item.get("language_match", 1.0),
            created_at=None,
        )
        for item in request.content
    ]

    return {
        "hour": request.hour,
        "results": InstagramStyleRanker().rank(user, history, items, now),
        "note": "Morning/evening behavior is an explicit experiment, not a claim about Instagram's internal production model."
    }
