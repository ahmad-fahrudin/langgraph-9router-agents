from agents.general import create_general_agent
from agents.coder import create_coder_agent
from agents.researcher import create_researcher_agent
from agents.team import create_team_agent, create_collaborative_team_agent

# Registry Agent yang tersedia
AGENTS_REGISTRY = {
    "team": {
        "description": "Multi-agent kolaboratif (Researcher + Coder + Supervisor) yang berpikir bareng-bareng menghasilkan solusi arsitektur & kode definitif.",
        "factory": create_collaborative_team_agent,
    },
    "auto": {
        "description": "Smart Router otomatis yang mengevaluasi tugas: delegasi cepat untuk tugas ringan, atau kolaborasi berpikir bareng-bareng untuk tugas kompleks.",
        "factory": lambda: create_team_agent(force_collaborate=False),
    },
    "coder": {
        "description": "Spesialis software engineering, kode produksi, modularitas, dan algoritma (FreeGptCODEX).",
        "factory": create_coder_agent,
    },
    "researcher": {
        "description": "Spesialis analisis mendalam, riset komparatif, trade-offs, dan arsitektur (FreeKiroAI).",
        "factory": create_researcher_agent,
    },
    "general": {
        "description": "Asisten umum untuk percakapan, cek waktu, dan kalkulator matematika (AntiGravityModel).",
        "factory": create_general_agent,
    },
}


def list_agents() -> dict:
    """Mengembalikan daftar agent yang tersedia beserta deskripsinya."""
    return {name: info["description"] for name, info in AGENTS_REGISTRY.items()}


def get_agent(name: str = "team"):
    """Mengambil instance agent yang sudah di-compile berdasarkan namanya (default: 'team')."""
    name_clean = name.lower().strip() if name else "team"
    if name_clean not in AGENTS_REGISTRY:
        available = ", ".join(AGENTS_REGISTRY.keys())
        raise ValueError(
            f"Agent '{name}' tidak ditemukan. Agent yang tersedia: {available}"
        )
    return AGENTS_REGISTRY[name_clean]["factory"]()
