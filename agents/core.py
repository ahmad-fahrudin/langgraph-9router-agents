import os
import json
from functools import lru_cache
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
DEFAULT_MODEL = os.getenv("ROUTER_MODEL", "AntiGravityModel")
DEFAULT_TEMPERATURE = float(os.getenv("ROUTER_TEMPERATURE", "0.7"))

# Pemetaan Model Spesialis Berdasarkan Kepintaran & Domain Tugas
ROLE_CONFIG = {
    "coder": {
        "model": os.getenv("ROUTER_CODER_MODEL", "FreeGptCODEX"),
        "temperature": float(os.getenv("ROUTER_CODER_TEMPERATURE", "0.1")),
    },
    "researcher": {
        "model": os.getenv("ROUTER_RESEARCHER_MODEL", "FreeKiroAI"),
        "temperature": float(os.getenv("ROUTER_RESEARCHER_TEMPERATURE", "0.3")),
    },
    "general": {
        "model": os.getenv("ROUTER_GENERAL_MODEL", "AntiGravityModel"),
        "temperature": float(os.getenv("ROUTER_GENERAL_TEMPERATURE", "0.5")),
    },
    "team": {
        "model": os.getenv("ROUTER_TEAM_MODEL", "AntiGravityModel"),
        "temperature": float(os.getenv("ROUTER_TEAM_TEMPERATURE", "0.1")),
    },
}

# Cache pool untuk instance LLM agar eksekusi instan tanpa inisialisasi ulang
_LLM_CACHE: dict[str, ChatOpenAI] = {}


def _create_raw_llm(model: str, temperature: float, streaming: bool = False) -> ChatOpenAI:
    if not API_KEY:
        raise ValueError("API Key 9Router belum disetel. Isi ROUTER_API_KEY di .env.")

    return ChatOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
        model=model,
        temperature=temperature,
        streaming=streaming,
        timeout=60.0,
        max_retries=2,
    )


def get_llm(
    model: str = None,
    temperature: float = None,
    streaming: bool = False,
    with_fallback: bool = True,
) -> ChatOpenAI:
    """Inisialisasi LLM 9Router dengan automatic fallback dan caching untuk performa tinggi."""
    selected_model = model or DEFAULT_MODEL
    selected_temp = temperature if temperature is not None else DEFAULT_TEMPERATURE

    cache_key = f"{selected_model}:{selected_temp}:{streaming}:{with_fallback}"
    if cache_key in _LLM_CACHE:
        return _LLM_CACHE[cache_key]

    primary_llm = _create_raw_llm(selected_model, selected_temp, streaming=streaming)

    # Jika bukan default model dan with_fallback aktif, pasang fallback ke DEFAULT_MODEL
    if with_fallback and selected_model != DEFAULT_MODEL:
        fallback_llm = _create_raw_llm(DEFAULT_MODEL, selected_temp, streaming=streaming)
        llm = primary_llm.with_fallbacks([fallback_llm])
    else:
        llm = primary_llm

    _LLM_CACHE[cache_key] = llm
    return llm


def get_role_llm(
    role: str,
    temperature: float = None,
    streaming: bool = False,
) -> ChatOpenAI:
    """Mengambil LLM optimal yang telah disesuaikan dengan kepintaran role agent."""
    role_key = role.lower().strip()
    cfg = ROLE_CONFIG.get(
        role_key,
        {"model": DEFAULT_MODEL, "temperature": DEFAULT_TEMPERATURE},
    )

    target_model = cfg["model"]
    target_temp = temperature if temperature is not None else cfg["temperature"]

    return get_llm(
        model=target_model,
        temperature=target_temp,
        streaming=streaming,
        with_fallback=True,
    )
