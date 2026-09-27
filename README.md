# Algorithm Instagram

Educational, research-informed simulator for an Instagram-style recommendation and ranking system.

## What it models

User signals:
- watch ratio and completion
- likes, comments, shares and saves
- skips and hide/negative feedback
- creator affinity and follows
- topic affinity

Content/context:
- quality
- originality
- language match
- freshness/content age
- experimental morning/evening context

Pipeline:

`user events -> feature aggregation -> candidate score -> context/freshness -> quality/originality gates -> ranked feed`

## Important

This project is **not Instagram's private production algorithm**. Meta does not publish the complete production formula or exact model weights. The time-of-day component is explicitly an experiment, not a claim that Instagram uses fixed morning/evening multipliers.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python examples/demo.py
```

The original implementation is now connected here from the RR-Studios project.

Sources:
- https://about.fb.com/news/2023/06/how-ai-ranks-content-on-facebook-and-instagram/
- https://about.fb.com/news/2023/04/instagram-reels-trending-audio-and-gifts-updates/
- https://about.fb.com/news/2025/09/in-india-instagram-debuts-a-reels-first-experience-for-its-mobile-app/
- https://about.fb.com/news/2026/01/2026-ai-drives-performance/
