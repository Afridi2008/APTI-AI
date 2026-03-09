import requests
from config import LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, OLLAMA_URL, OLLAMA_MODEL

PROMPT_TEMPLATE = """You are an aptitude tutor. A student got this question wrong.
Explain the solution clearly in 3-5 simple steps. Be encouraging and concise.

Question: {question}
Correct Answer: {answer}

Give a step-by-step explanation."""


def get_explanation(question: str, correct_answer: str) -> str:
    prompt = PROMPT_TEMPLATE.format(question=question, answer=correct_answer)

    if LLM_PROVIDER == "openai":
        return _call_openai(prompt)
    elif LLM_PROVIDER == "anthropic":
        return _call_anthropic(prompt)
    elif LLM_PROVIDER == "ollama":
        return _call_ollama(prompt)
    else:
        return "Explanation not available. Please configure a valid LLM_PROVIDER in config.py"


def _call_openai(prompt: str) -> str:
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 400
            },
            timeout=15
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Could not fetch explanation: {str(e)}"


def _call_anthropic(prompt: str) -> str:
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 400,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        return data["content"][0]["text"]
    except Exception as e:
        return f"Could not fetch explanation: {str(e)}"


def _call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        return response.json().get("response", "No response from Ollama.")
    except Exception as e:
        return f"Could not fetch explanation: {str(e)}"
