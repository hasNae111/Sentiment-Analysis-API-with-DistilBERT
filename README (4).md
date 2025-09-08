# Sentiment Analysis API

## Description
Ce projet est un **microservice d’analyse de sentiments** basé sur le modèle Hugging Face :  
[`distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english).

Il permet de **détecter automatiquement si un texte est positif ou négatif** avec un score de confiance.  
L’API est développée en **FastAPI**, conteneurisée avec **Docker**, et déployée sur **Hugging Face Spaces**.

---

## User Stories
- En tant qu’utilisateur, j’envoie un texte à l’API et j’obtiens le **sentiment** (positif/négatif) et un **score**.  
- En tant qu’utilisateur, je peux tester l’API via **Swagger** (`/docs`) et une **page web simple** (`/`).  
- En tant que développeur, je peux lancer l’API localement via **Docker** ou **Uvicorn**.  
- En tant que formateur/apprenant, j’accède à une version déployée publiquement sur **Hugging Face Spaces**.

---

## Installation et Exécution Locale

### 1. Cloner le projet
```bash
git clone https://github.com/<ton-compte>/sentiment-analysis-api.git
cd sentiment-analysis-api
```

### 2. Installer les dépendances
#### Option A – Sans Docker (local avec Python)
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```
API dispo sur [http://localhost:7860/docs](http://localhost:7860/docs)
#### Option B – Avec Docker
```bash
docker build -t sentiment-api .
docker run -d -p 7860:7860 --name sentiment-container sentiment-api
```

---

## Endpoints de l’API

### 🔹 1. Health Check
```
GET /health
```
Réponse :
```json
{"status": "ok"}
```

### 🔹 2. Prédiction
```
POST /predict
```
Exemple requête :
```json
{
  "text": "I love this product, it is amazing!"
}
```
Exemple réponse :
```json
{
  "sentiment": "POSITIVE",
  "score": 0.9985
}
```

### 🔹 3. Swagger
```
GET /docs
```
👉 Interface interactive de test.

### 🔹 4. Page HTML
```
GET /
```
 Une page web simple pour tester rapidement l’API.

---

## Déploiement Hugging Face

Le projet est déployé sur **Hugging Face Spaces** avec Docker.  
Lien public :  
https://huggingface.co/spaces/<ton-nom>/sentiment-analysis-api  

---

## Captures d’écran
- Swagger UI (`/docs`)  
- Page HTML de test (`/`)  

*(à insérer après ton test avec `PrintScreen`)*

---

## Tests Unitaires

Exemple de tests inclus :
- **/health** → retourne `{"status":"ok"}`  
- **/predict** avec texte positif → sentiment = POSITIVE  
- **/predict** avec texte vide → erreur 422  

Pour lancer les tests :
```bash
pytest
```

---

## Mini-Benchmark

| Modèle                                      | Latence (ms) | Justesse approx |
|---------------------------------------------|--------------|-----------------|
| distilbert-base-uncased-finetuned-sst-2     | ~50-70       | haute (90%+) |
| bert-base-uncased (non optimisé CPU)        | ~120-150     | similaire    |

On constate que **DistilBERT** est plus rapide et adapté au déploiement CPU.

---

## Structure du projet
```
.
│── app/
│   ├── main.py          # Code API (FastAPI)
│   ├── model.py 
│   ├── schema.py 
│   ├── __init__.py 
│── static/
│   ├── index.html       # Page web de test
│── app/
│   ├── test_errors.py         
│   ├── test_health.py 
│   ├── test_predict.py 
│── requirements.txt     # Dépendances
│── Dockerfile           # Déploiement
│── README.md            # Documentation
```

---

- Projet réalisé dans le cadre d’un apprentissage **IA / DevOps / Cloud**  

