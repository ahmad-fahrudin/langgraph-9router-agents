from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from agents.core import get_llm


def create_researcher_agent():
    """Agent Spesialis Riset, Analisis Data, dan Perbandingan Konsep."""
    llm = get_llm(temperature=0.5)

    system_prompt = SystemMessage(
        content=(
            "Anda adalah Research Analyst AI. Fokus Anda adalah melakukan analisis mendalam, "
            "memberikan perbandingan objektif pro-kontra, sintesis informasi, dan rangkuman poin-poin penting."
        )
    )

    def call_model(state: MessagesState):
        messages = [system_prompt] + list(state["messages"])
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_edge(START, "agent")

    return graph.compile()
