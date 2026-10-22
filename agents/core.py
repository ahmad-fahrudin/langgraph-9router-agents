import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Muat variabel dari .env
load_dotenv()


def _get_fallback_opencode_config() -> tuple[str, str]:
    """Mengambil config 9router dari OpenCode jika .env kosong."""
    cfg_file = os.path.expanduser("~/.config/opencode/opencode.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                opts = data.get("provider", {}).get("9router", {}).get("options", {})
                return opts.get("baseURL", ""), opts.get("apiKey", "")
        except Exception:
            pass
    return "", ""


_fallback_url, _fallback_key = _get_fallback_opencode_config()

BASE_URL = os.getenv("ROUTER_BASE_URL") or _fallback_url or "http://localhost:20128/v1"
API_KEY = os.getenv("ROUTER_API_KEY") or _fallback_key
MODEL_NAME = os.getenv("ROUTER_MODEL", "AntiGravityModel")
TEMPERATURE = float(os.getenv("ROUTER_TEMPERATURE", "0.7"))


def get_llm(model: str = None, temperature: float = None) -> ChatOpenAI:
    """Inisialisasi LLM 9Router Combo."""
    if not API_KEY:
        raise ValueError(
            "API Key 9Router belum disetel. Isi ROUTER_API_KEY di .env."
        )

    return ChatOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
        model=model or MODEL_NAME,
        temperature=temperature if temperature is not None else TEMPERATURE,
    )
