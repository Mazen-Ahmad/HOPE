import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

with open(os.path.join(os.path.dirname(__file__), "taxonomy.json")) as f:
    _TAXONOMY = json.load(f)

_SYSTEM_PROMPT = (
    "You are a financial query analysis engine. "
    "Given a finance sub-query, extract structured metadata. "
    f"query_type MUST be one of: {_TAXONOMY['query_types']}. "
    f"financial_terms should be drawn from these signal groups where relevant: {json.dumps(_TAXONOMY['signal_groups'])}. "
    "Respond with ONLY valid JSON in this exact shape, no markdown, no explanation: "
    '{"financial_terms": ["string", "..."], "query_type": "string"}'
)


def extract(sub_query: str) -> dict:
    response = _client.chat.completions.create(
        model="inclusionai/ling-3.0-flash-fin:free",
        temperature=0,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": sub_query},
        ],
    )
    text = response.choices[0].message.content.strip()
    parsed = json.loads(text)
    return {
        "financial_terms": parsed.get("financial_terms", []),
        "query_type": parsed.get("query_type", "general"),
    }
