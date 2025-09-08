import logging
from typing import List, Dict
from transformers import pipeline

logger = logging.getLogger("sentiment_model")
MODEL_ID = "distilbert-base-uncased-finetuned-sst-2-english"

# pipeline object (lazy loaded)
nlp = None

def load_model():
    """Charge le pipeline HF (CPU). Idempotent."""
    global nlp
    if nlp is None:
        logger.info("Loading model %s ...", MODEL_ID)
        # device=-1 => CPU (compatible avec Spaces CPU)
        nlp = pipeline("sentiment-analysis", model=MODEL_ID, device=-1)
        logger.info("Model loaded.")
    return nlp

def analyze(text: str) -> List[Dict]:
    """Retourne la sortie du pipeline: [{'label':..., 'score':...}]"""
    nlp = load_model()
    return nlp(text)
