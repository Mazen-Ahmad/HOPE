import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from extractor import extract
from classifier import classify

load_dotenv()
logger = logging.getLogger(__name__)

_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

_SYSTEM_PROMPT = (
    "You are a query decomposition engine. "
    "Split a user query into atomic sub-queries ONLY if it contains multiple clearly distinct, independent questions about different topics. "
    "Do NOT split a single question that asks for a trend, comparison, time range, or breakdown — those are one atomic query. "
    "Preserve the original wording of each sub-query exactly — do not paraphrase, rephrase, or rewrite. "
    "If the query is a single question, output a list with exactly one item. "
    "Respond with ONLY valid JSON in this exact shape, no markdown, no explanation: "
    '{"sub_queries": ["...", "..."]}'
)


def decompose_query(raw_query: str) -> list[str]:
    response = _client.chat.completions.create(
        model="inclusionai/ling-3.0-flash-fin:free",
        temperature=0,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": raw_query},
        ],
    )
    text = response.choices[0].message.content.strip()
    parsed = json.loads(text)
    return parsed["sub_queries"]


def route_query(raw_query: str) -> dict:
    sub_queries = decompose_query(raw_query)
    result = []

    for q in sub_queries:
        # Stage 2 — structured extraction (logging/debug only, not fed into classifier)
        extraction = extract(q)
        logger.info(
            f"[extractor] {q!r} -> terms={extraction['financial_terms']}  type={extraction['query_type']}"
        )

        # Stage 3 — SetFit classification
        classification = classify(q)
        logger.info(
            f"[classifier] {q!r} -> agent={classification.agent}  confidence={classification.confidence:.3f}"
        )

        result.append({
            "query": q,
            "agent": classification.agent,
            "confidence": round(classification.confidence, 4),
            "extraction": extraction,
        })

    return {"sub_queries": result}
