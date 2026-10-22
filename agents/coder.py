from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from agents.core import get_llm


def create_coder_agent():
    """Agent Spesialis Coding, Arsitektur Software, dan Debugging."""
    llm = get_llm(temperature=0.2)

    system_prompt = SystemMessage(
        content=(
            "Anda adalah Senior Software Engineer AI. Anda ahli dalam menulis kode yang bersih, "
            "efisien, modular, serta memberikan penjelasan teknis yang mendalam dan mudah dipahami."
        )
    )

    def call_model(state: MessagesState):
        messages = [system_prompt] + list(state["messages"])
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_edge(START, "agent")

    return graph.compile()
