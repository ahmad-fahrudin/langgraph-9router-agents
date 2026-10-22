from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from agents.core import get_role_llm
from agents.general import create_general_agent
from agents.coder import create_coder_agent
from agents.researcher import create_researcher_agent


class TeamState(TypedDict):
    """State bersama untuk koordinasi kolaboratif multi-agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    task: str
    route: str
    research_insights: str
    code_solution: str


def _get_last_user_message(state: TeamState) -> str:
    """Mengambil teks pesan user terakhir dari state."""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage) or getattr(msg, "type", "") == "human":
            return msg.content
    return ""


def create_team_agent(force_collaborate: bool = False):
    """Membuat Multi-Agent LangGraph Team di mana agent-agent berpikir bersama:
    - Researcher (FreeKiroAI): Menganalisa arsitektur, trade-offs, dan edge cases.
    - Coder (FreeGptCODEX): Mengembangkan implementasi kode produksi yang solid & modular.
    - Supervisor / Synthesizer (AntiGravityModel): Mengarahkan dan mensintesis hasil akhir menjadi solusi definitif.
    """
    router_llm = get_role_llm("team", temperature=0.0)
    researcher_llm = get_role_llm("researcher")
    coder_llm = get_role_llm("coder")
    synthesizer_llm = get_role_llm("team", temperature=0.2)

    # Inisialisasi sub-graph untuk mode direct jika diperlukan
    general_subagent = create_general_agent()
    coder_subagent = create_coder_agent()
    researcher_subagent = create_researcher_agent()

    def router_node(state: TeamState) -> dict:
        """Menganalisa kompleksitas tugas dan menentukan alur kerja."""
        if force_collaborate:
            return {"route": "collaborate"}

        user_text = _get_last_user_message(state)
        router_prompt = [
            SystemMessage(
                content=(
                    "Anda adalah Router Cerdas untuk sistem Multi-Agent.\n"
                    "Analisa instruksi pengguna dan pilih salah satu kategori rute berikut:\n"
                    "- 'general': Pertanyaan percakapan santai, salam, cek waktu, atau perhitungan matematika murni.\n"
                    "- 'coder': Tugas penulisan fungsi/kode sederhana tunggal tanpa memerlukan analisis arsitektur.\n"
                    "- 'researcher': Pertanyaan teori atau riset murni tanpa memerlukan implementasi kode.\n"
                    "- 'collaborate': Tugas rekayasa software kompleks, arsitektur sistem, refactoring besar, "
                    "perbandingan teknis + implementasi, pembuatan aplikasi, atau problem solving multi-tahap.\n\n"
                    "Balas HANYA dengan satu kata: 'general', 'coder', 'researcher', atau 'collaborate'."
                )
            ),
            HumanMessage(content=user_text),
        ]
        decision = router_llm.invoke(router_prompt).content.strip().lower()
        valid_routes = {"general", "coder", "researcher", "collaborate"}
        route = decision if decision in valid_routes else "collaborate"
        return {"route": route}

    def route_decision(state: TeamState) -> Literal["general_sub", "coder_sub", "researcher_sub", "collaborate_flow"]:
        route = state.get("route", "collaborate")
        if route == "general":
            return "general_sub"
        elif route == "coder":
            return "coder_sub"
        elif route == "researcher":
            return "researcher_sub"
        return "collaborate_flow"

    # --- Node Rute Langsung (Fast Single-Agent) ---
    def direct_general_node(state: TeamState) -> dict:
        res = general_subagent.invoke({"messages": state["messages"]})
        return {"messages": [res["messages"][-1]]}

    def direct_coder_node(state: TeamState) -> dict:
        res = coder_subagent.invoke({"messages": state["messages"]})
        return {"messages": [res["messages"][-1]]}

    def direct_researcher_node(state: TeamState) -> dict:
        res = researcher_subagent.invoke({"messages": state["messages"]})
        return {"messages": [res["messages"][-1]]}

    # --- Node Kolaboratif (Berpikir Bareng-bareng) ---
    def collaborative_research_node(state: TeamState) -> dict:
        """Fase 1: Researcher menelaah problem space, arsitektur, dan prinsip rekayasa."""
        user_text = _get_last_user_message(state)
        research_prompt = [
            SystemMessage(
                content=(
                    "Anda adalah Senior Research Scientist & Enterprise Solutions Architect.\n"
                    "Lakukan analisis mendalam untuk permintaan user berikut.\n"
                    "Tugas Anda:\n"
                    "1. Analisa kebutuhan inti dan pertimbangan arsitektur teknis.\n"
                    "2. Identifikasi potensi edge cases, trade-offs performa, dan aspek keamanan.\n"
                    "3. Rancang blueprint struktur dan rekomendasi implementasi konkrit untuk Coder.\n"
                    "Sajikan secara ringkas, berbobot, dan to-the-point."
                )
            ),
            HumanMessage(content=user_text),
        ]
        res = researcher_llm.invoke(research_prompt)
        return {"research_insights": res.content}

    def collaborative_coder_node(state: TeamState) -> dict:
        """Fase 2: Coder merekayasa kode produksi berdasarkan panduan arsitektur Researcher."""
        user_text = _get_last_user_message(state)
        research_notes = state.get("research_insights", "")

        coder_prompt = [
            SystemMessage(
                content=(
                    "Anda adalah Senior Principal Software Engineer.\n"
                    "Tugas Anda adalah menulis implementasi kode tingkat produksi (production-ready) "
                    "berdasarkan permintaan pengguna dan rekomendasi arsitektur dari tim Researcher.\n\n"
                    "Kriteria Kode:\n"
                    "- Kode bersih, efisien, modular, type-safe, dan memiliki penanganan error yang kuat.\n"
                    "- Mengatasi seluruh edge cases yang diidentifikasi Researcher.\n"
                    "- Sertakan contoh penggunaan atau pengujian singkat yang langsung dapat dijalankan."
                )
            ),
            HumanMessage(
                content=(
                    f"Permintaan Pengguna:\n{user_text}\n\n"
                    f"Rekomendasi Arsitektur & Edge Cases dari Researcher:\n{research_notes}"
                )
            ),
        ]
        res = coder_llm.invoke(coder_prompt)
        return {"code_solution": res.content}

    def collaborative_synthesis_node(state: TeamState) -> dict:
        """Fase 3: Supervisor mensintesis hasil kolaborasi Tim menjadi output final berkualitas tinggi."""
        user_text = _get_last_user_message(state)
        research_notes = state.get("research_insights", "")
        code = state.get("code_solution", "")

        synthesis_prompt = [
            SystemMessage(
                content=(
                    "Anda adalah Lead Orchestrator Multi-Agent.\n"
                    "Tugas Anda adalah merangkai dan memvalidasi hasil kolaborasi tim (Researcher + Coder) "
                    "menjadi jawaban akhir yang kohesif, profesional, dan langsung dapat dieksekusi.\n\n"
                    "Format Respons:\n"
                    "1. **Analisis & Arsitektur Singkat**: Poin penting dari riset & keputusan desain.\n"
                    "2. **Implementasi Solusi / Kode**: Kode lengkap dan siap pakai dari Coder.\n"
                    "3. **Panduan & Verifikasi**: Cara menjalankan, validasi, dan catatan teknis penting.\n\n"
                    "Jawab dalam bahasa Indonesia yang lugas, terstruktur, dan elegan."
                )
            ),
            HumanMessage(
                content=(
                    f"Pertanyaan Pengguna:\n{user_text}\n\n"
                    f"Hasil Telaah Researcher:\n{research_notes}\n\n"
                    f"Implementasi Coder:\n{code}"
                )
            ),
        ]
        res = synthesizer_llm.invoke(synthesis_prompt)
        return {"messages": [AIMessage(content=res.content)]}

    # Bangun Graf LangGraph
    builder = StateGraph(TeamState)

    builder.add_node("router", router_node)
    builder.add_node("general_sub", direct_general_node)
    builder.add_node("coder_sub", direct_coder_node)
    builder.add_node("researcher_sub", direct_researcher_node)
    builder.add_node("collaborative_research", collaborative_research_node)
    builder.add_node("collaborative_coder", collaborative_coder_node)
    builder.add_node("collaborative_synthesis", collaborative_synthesis_node)

    # Edges
    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "general_sub": "general_sub",
            "coder_sub": "coder_sub",
            "researcher_sub": "researcher_sub",
            "collaborate_flow": "collaborative_research",
        },
    )

    # Direct nodes ke END
    builder.add_edge("general_sub", END)
    builder.add_edge("coder_sub", END)
    builder.add_edge("researcher_sub", END)

    # Collaborative pipeline
    builder.add_edge("collaborative_research", "collaborative_coder")
    builder.add_edge("collaborative_coder", "collaborative_synthesis")
    builder.add_edge("collaborative_synthesis", END)

    return builder.compile()


def create_collaborative_team_agent():
    """Selalu jalankan pipeline kolaborasi penuh multi-agent (berpikir bareng-bareng)."""
    return create_team_agent(force_collaborate=True)
