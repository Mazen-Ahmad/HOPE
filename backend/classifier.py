import os
import json
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from setfit import SetFitModel, Trainer, TrainingArguments
from datasets import Dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "setfit_finance")
_SPLIT_PATH = os.path.join(os.path.dirname(__file__), "models", "split_indices.json")
_CSV_PATH = os.path.join(os.path.dirname(__file__), "finance_query_classification_dataset.csv")
_BASE_MODEL = "BAAI/bge-small-en-v1.5"
_CONFIDENCE_THRESHOLD = 0.75
_RANDOM_SEED = 42

AGENTS = ["profitability_agent", "liquidity_agent", "product_agent", "knowledge_agent"]


@dataclass
class ClassificationResult:
    agent: str
    confidence: float


# ── Training ──────────────────────────────────────────────────────────────────

def train():
    df = pd.read_csv(_CSV_PATH)

    train_df, val_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df["correct_agent"],
        random_state=_RANDOM_SEED,
    )

    os.makedirs(os.path.dirname(_SPLIT_PATH), exist_ok=True)
    with open(_SPLIT_PATH, "w") as f:
        json.dump({"train": train_df.index.tolist(), "val": val_df.index.tolist()}, f)

    logger.info(f"Train size: {len(train_df)} | Val size: {len(val_df)}")
    logger.info(f"Train label distribution:\n{train_df['correct_agent'].value_counts().to_string()}")
    logger.info(f"Val label distribution:\n{val_df['correct_agent'].value_counts().to_string()}")

    train_dataset = Dataset.from_dict({
        "text": train_df["sub_query"].tolist(),
        "label": train_df["correct_agent"].tolist(),
    })

    model = SetFitModel.from_pretrained(_BASE_MODEL, labels=AGENTS)

    args = TrainingArguments(
        num_epochs=3,
        batch_size=16,
        seed=_RANDOM_SEED,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
    )
    trainer.train()

    os.makedirs(_MODEL_PATH, exist_ok=True)
    model.save_pretrained(_MODEL_PATH)
    logger.info(f"Model saved to {_MODEL_PATH}")

    _evaluate(model, val_df)


# ── Evaluation ────────────────────────────────────────────────────────────────

def _evaluate(model, val_df: pd.DataFrame):
    texts = val_df["sub_query"].tolist()
    true_labels = val_df["correct_agent"].tolist()

    # predict_proba columns follow head.classes_ (alphabetical), not model.labels
    proba_order = list(model.model_head.classes_)
    pred_labels = list(model.predict(texts))
    probs = np.array(model.predict_proba(texts))
    confidences = np.array([
        float(probs[i][proba_order.index(pred_labels[i])])
        for i in range(len(pred_labels))
    ])

    label_order = model.labels
    acc = accuracy_score(true_labels, pred_labels)
    report = classification_report(true_labels, pred_labels, target_names=label_order)
    cm = confusion_matrix(true_labels, pred_labels, labels=label_order)

    logger.info(f"\n{'='*60}")
    logger.info(f"Validation Accuracy: {acc:.4f}")
    logger.info(f"\nClassification Report:\n{report}")
    logger.info(f"\nConfusion Matrix (rows=true, cols=pred):")
    logger.info(f"Labels: {label_order}")
    logger.info(f"\n{cm}")

    pi = label_order.index("profitability_agent")
    li = label_order.index("liquidity_agent")
    logger.info(f"\nProfitability->Liquidity confusion: {cm[pi][li]}")
    logger.info(f"Liquidity->Profitability confusion:  {cm[li][pi]}")

    correct_mask = np.array(pred_labels) == np.array(true_labels)
    logger.info(f"\nConfidence (correct)   — mean: {confidences[correct_mask].mean():.3f}  min: {confidences[correct_mask].min():.3f}")
    if (~correct_mask).any():
        logger.info(f"Confidence (incorrect) — mean: {confidences[~correct_mask].mean():.3f}  max: {confidences[~correct_mask].max():.3f}")
    else:
        logger.info("Confidence (incorrect) — none (perfect val accuracy)")
    logger.info(f"Current threshold: {_CONFIDENCE_THRESHOLD}")
    logger.info(f"{'='*60}\n")


# ── Inference ─────────────────────────────────────────────────────────────────

_model_cache = None

def _load_model() -> SetFitModel:
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(_MODEL_PATH):
            raise RuntimeError(
                f"No trained model found at {_MODEL_PATH}. Run classifier.train() first."
            )
        _model_cache = SetFitModel.from_pretrained(_MODEL_PATH)
    return _model_cache


def classify(sub_query: str) -> ClassificationResult:
    model = _load_model()
    proba_order = list(model.model_head.classes_)
    agent = str(model.predict([sub_query])[0])
    probs = np.array(model.predict_proba([sub_query]))[0]
    confidence = float(probs[proba_order.index(agent)])

    if confidence < _CONFIDENCE_THRESHOLD:
        logger.warning(
            f"[classifier] Low confidence ({confidence:.3f}) for query: {sub_query!r} -> {agent}"
        )

    return ClassificationResult(agent=agent, confidence=confidence)


if __name__ == "__main__":
    train()
