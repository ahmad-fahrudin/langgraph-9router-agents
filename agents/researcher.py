from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from agents.core import get_role_llm


def create_researcher_agent():
    """Agent Spesialis Riset Mendalam, Analisis Komparatif, dan Arsitektur Konseptual.
    Ditenagai model FreeKiroAI (DeepSeek 3.2 / Qwen3) dengan kemampuan penalaran analitis mendalam.
    """
    llm = get_role_llm("researcher")

    system_prompt = SystemMessage(
        content=(
            "Anda adalah Senior Research Scientist & Enterprise Solutions Architect. "
            "Keahlian Anda adalah melakukan riset mendalam, analisis komparatif objektif (pro-kontra, trade-offs), "
            "eksplorasi skenario batas (edge cases), dan perumusan rekomendasi teknologi strategis.\n\n"
            "Pedoman Kerja:\n"
            "1. Sajikan analisis terstruktur dengan poin-poin jelas, tabel perbandingan jika relevan, dan rekomendasi berbasis data/prinsip rekayasa.\n"
            "2. Identifikasi potensi bottleneck, aspek skalabilitas, keamanan, dan efisiensi sumber daya.\n"
            "3. Berikan sintesis yang langsung ke inti permasalahan tanpa pengulangan kata yang tidak perlu.\n"
            "4. Gunakan bahasa Indonesia yang analitis, lugas, dan akurat."
        )
    )

    def call_model(state: MessagesState):
        messages = [system_prompt] + list(state["messages"])
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_edge(START, "agent")

    return graph.compile()
