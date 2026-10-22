from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from agents.core import get_role_llm


def create_coder_agent():
    """Agent Spesialis Coding, Arsitektur Software, Refactoring, dan Algoritma.
    Ditenagai model FreeGptCODEX (GPT-6 Luna) dengan kemampuan code synthesis ultra cepat & presisi.
    """
    llm = get_role_llm("coder")

    system_prompt = SystemMessage(
        content=(
            "Anda adalah Senior Principal Software Engineer & Code Architect kelas dunia. "
            "Keahlian Anda mencakup arsitektur sistem, penulisan kode tingkat produksi (production-ready), "
            "optimasi performa, refactoring, dan debugging mendalam.\n\n"
            "Pedoman Kerja:\n"
            "1. Tulis kode yang bersih, modular, type-safe, dan memiliki error handling yang komprehensif.\n"
            "2. Langsung berikan solusi dan implementasi kode utama tanpa basa-basi pengantar.\n"
            "3. Sertakan contoh penggunaan atau pengujian ringkas jika relevan.\n"
            "4. Jelaskan keputusan arsitektur dan trade-off teknis secara padat dan berbobot.\n"
            "5. Gunakan bahasa Indonesia yang jelas dan profesional untuk penjelasan teks."
        )
    )

    def call_model(state: MessagesState):
        messages = [system_prompt] + list(state["messages"])
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_edge(START, "agent")

    return graph.compile()
