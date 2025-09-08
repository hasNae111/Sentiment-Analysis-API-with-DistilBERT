import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import model as sentiment_model
from .schemas import PredictRequest, PredictResponse

# App
app = FastAPI(title="Sentiment API", version="0.1.0")

# Logging simple
logger = logging.getLogger("sentiment_api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Serve static files (page de test)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    """Renvoie la page static/index.html"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return HTMLResponse("<h3>Index not found</h3>", status_code=404)

@app.on_event("startup")
def startup_event():
    skip = os.getenv("SKIP_MODEL_LOAD", "0").lower() in ("1", "true", "yes")
    if skip:
        logger.info("SKIP_MODEL_LOAD set — skipping model preload.")
    else:
        logger.info("Startup: preloading model (may take a few seconds).")
        try:
            sentiment_model.load_model()
        except Exception as e:
            logger.exception("Model preload failed: %s", e)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    text = payload.text
    if not isinstance(text, str) or text.strip() == "":
        # texte vide => 400 explicite
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    logger.info("Predict request (first 120 chars): %s", text[:120])
    try:
        result = sentiment_model.analyze(text)
        # result expected like [{'label':'POSITIVE','score':0.999}]
        first = result[0]
        label = first.get("label")
        score = float(first.get("score", 0.0))
        return PredictResponse(sentiment=label, confidence=score)
    except Exception as e:
        logger.exception("Prediction error: %s", e)
        raise HTTPException(status_code=500, detail="Prediction failed")
