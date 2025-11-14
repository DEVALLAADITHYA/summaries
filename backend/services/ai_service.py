import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# GEMINI_API_KEY should be set in backend/.env
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

if not GEMINI_API_KEY:
    print('WARNING: GEMINI_API_KEY not set. Place key in backend/.env')

# Choose model - you can change this to gemini-2.5 or other available model in AI Studio
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')

def build_payload(text):
    # limit text length to avoid huge requests
    snippet = text[:25000]
    payload = {
        "contents": [
            {
                "parts": [
                    { "text": f"You are an assistant that extracts concise summaries and key points from a document.\n\nDocument:\n\n{snippet}\n\nRespond only with a JSON object with keys: short, medium, long, key_points.\n- short: ~50-100 words.\n- medium: ~150-300 words.\n- long: ~400-700 words.\n- key_points: array of 6-12 concise key points.\nEnsure output is valid JSON." }
                ]
            }
        ]
    }
    return payload

def call_gemini(payload):
    # REST endpoint for generateContent (Gemini API / Google GenAI)
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        # API key is sent via x-goog-api-key header per docs
        "x-goog-api-key": GEMINI_API_KEY
    }
    resp = requests.post(endpoint, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    return resp.json()

def generate_summaries(text):
    payload = build_payload(text)
    data = call_gemini(payload)

    # The quickstart response structure: data['candidates'][0]['content']['parts'][0]['text']
    try:
        candidates = data.get('candidates') or data.get('output') or []
        # Try common locations for text
        if candidates and isinstance(candidates, list):
            first = candidates[0]
            # nested structure used by some responses
            content = first.get('content', {})
            parts = content.get('parts') if isinstance(content, dict) else None
            if parts and len(parts) > 0:
                text = parts[0].get('text', '')
            else:
                # fallback: if candidate is string-like
                text = first.get('text') or ''
        else:
            # fallback: if top-level 'text' exists
            text = data.get('text', '') or json.dumps(data)
    except Exception:
        text = json.dumps(data)

    # Attempt to parse JSON out of the returned text
    try:
        parsed = json.loads(text)
    except Exception:
        # try to extract JSON substring
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        if first_brace != -1 and last_brace != -1:
            try:
                parsed = json.loads(text[first_brace:last_brace+1])
            except Exception:
                parsed = {'short': text[:200], 'medium': text, 'long': text, 'key_points': []}
        else:
            parsed = {'short': text[:200], 'medium': text, 'long': text, 'key_points': []}

    # Ensure keys exist
    parsed.setdefault('short', parsed.get('short', ''))
    parsed.setdefault('medium', parsed.get('medium', ''))
    parsed.setdefault('long', parsed.get('long', ''))
    parsed.setdefault('key_points', parsed.get('key_points', []))

    return parsed
