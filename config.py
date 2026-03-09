# ── Database Configuration ────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",        # ← change to your MySQL username
    "password": "password",    # ← change to your MySQL password
    "database": "aptitude_ai"
}

# ── LLM Configuration ─────────────────────────────────────────────────────────
# Supported providers: "openai" | "anthropic" | "ollama"
LLM_PROVIDER = "openai"

OPENAI_API_KEY  = "sk-..."          # ← paste your OpenAI key
ANTHROPIC_API_KEY = "sk-ant-..."    # ← paste your Anthropic key

# If using local Ollama
OLLAMA_URL      = "http://localhost:11434/api/generate"
OLLAMA_MODEL    = "mistral"
