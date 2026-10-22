import datetime
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from agents.core import get_llm


@tool
def get_current_time() -> str:
    """Mengembalikan tanggal dan waktu saat ini."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def kalkulator(ekspresi: str) -> str:
    """Hitung ekspresi matematika sederhana (misal: '25 * 4', '100 / 2 + 15')."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in ekspresi):
        return "Error: Ekspresi mengandung karakter tidak valid."
    try:
        return str(eval(ekspresi, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {e}"


def create_general_agent():
    """Agent Asisten Umum yang siap membantu tugas sehari-hari dan perhitungan."""
    tools = [get_current_time, kalkulator]
    llm = get_llm().bind_tools(tools)

    system_prompt = SystemMessage(
        content="Anda adalah General Assistant cerdas yang ditenagai model Combo 9Router. Jawab dengan ramah, akurat, dan gunakan bahasa Indonesia yang jelas."
    )

    def call_model(state: MessagesState):
        messages = [system_prompt] + list(state["messages"])
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()
