import os
import pickle
import logging
import numpy as np
import requests
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "setfit_finance")
_HEAD_PATH = os.path.join(_MODEL_PATH, "model_head.pkl")
_HF_MODEL_ID = "Mazen619/hope-setfit-finance"
_HF_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{_HF_MODEL_ID}"
_CONFIDENCE_THRESHOLD = 0.75

AGENTS = ["profitability_agent", "liquidity_agent", "product_agent", "knowledge_agent"]


@dataclass
class ClassificationResult:
    agent: str
    confidence: float


_head_cache = None

def _load_head():
    global _head_cache
    if _head_cache is None:
        if not os.path.exists(_HEAD_PATH):
            raise RuntimeError(f"model_head.pkl not found at {_HEAD_PATH}")
        size = os.path.getsize(_HEAD_PATH)
        logger.info(f"[classifier] model_head.pkl: {size:,} bytes")
        if size < 1024:
            raise RuntimeError(f"model_head.pkl is only {size} bytes — looks like an LFS pointer.")
        with open(_HEAD_PATH, "rb") as f:
            _head_cache = pickle.load(f)
    return _head_cache


def _get_embedding(text: str) -> np.ndarray:
    token = os.getenv("HF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.post(
        _HF_API_URL,
        headers=headers,
        json={"inputs": text, "options": {"wait_for_model": True}},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    # HF feature-extraction returns [[[token_embeddings]]] — mean pool to sentence vector
    arr = np.array(data)
    if arr.ndim == 3:
        arr = arr.mean(axis=1)   # mean pool over tokens
    if arr.ndim == 2:
        arr = arr[0]             # unwrap batch dim
    return arr


def classify(sub_query: str) -> ClassificationResult:
    head = _load_head()
    embedding = _get_embedding(sub_query).reshape(1, -1)

    proba_order = list(head.classes_)
    agent = str(head.predict(embedding)[0])
    probs = head.predict_proba(embedding)[0]
    confidence = float(probs[proba_order.index(agent)])

    if confidence < _CONFIDENCE_THRESHOLD:
        logger.warning(
            f"[classifier] Low confidence ({confidence:.3f}) for query: {sub_query!r} -> {agent}"
        )

    return ClassificationResult(agent=agent, confidence=confidence)
