from agents.general import create_general_agent
from agents.coder import create_coder_agent
from agents.researcher import create_researcher_agent

# Registry Agent yang tersedia
AGENTS_REGISTRY = {
    "general": {
        "description": "Asisten umum untuk berbagai tugas, percakapan, dan perhitungan dasar.",
        "factory": create_general_agent,
    },
    "coder": {
        "description": "Spesialis software engineering, penulisan kode, refactor, dan debugging.",
        "factory": create_coder_agent,
    },
    "researcher": {
        "description": "Spesialis analisis mendalam, riset komparatif, dan perbandingan solusi.",
        "factory": create_researcher_agent,
    },
}


def list_agents() -> dict:
    """Mengembalikan daftar agent yang tersedia beserta deskripsinya."""
    return {name: info["description"] for name, info in AGENTS_REGISTRY.items()}


def get_agent(name: str):
    """Mengambil instance agent yang sudah di-compile berdasarkan namanya."""
    name_clean = name.lower().strip()
    if name_clean not in AGENTS_REGISTRY:
        available = ", ".join(AGENTS_REGISTRY.keys())
        raise ValueError(
            f"Agent '{name}' tidak ditemukan. Agent yang tersedia: {available}"
        )
    return AGENTS_REGISTRY[name_clean]["factory"]()
