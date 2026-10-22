import math
import datetime
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from agents.core import get_role_llm


@tool
def get_current_time() -> str:
    """Mengembalikan tanggal dan waktu saat ini secara akurat (format YYYY-MM-DD HH:MM:SS)."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def kalkulator(ekspresi: str) -> str:
    """Hitung ekspresi matematika (misal: '25 * 4', '100 / 2 + 15', 'math.sqrt(144)', '2**10').
    Mendukung fungsi matematika standar seperti sqrt, pow, sin, cos, tan, log, exp, pi, e, abs, round.
    """
    safe_dict = {
        "math": math,
        "sqrt": math.sqrt,
        "pow": math.pow,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
    }
    # Blokir attribute traversal berbahaya
    if "__" in ekspresi or "import" in ekspresi or "eval" in ekspresi or "exec" in ekspresi:
        return "Error: Ekspresi mengandung perintah tidak diizinkan."

    try:
        res = eval(ekspresi, {"__builtins__": None}, safe_dict)
        return str(res)
    except Exception as e:
        return f"Error: {e}"


def create_general_agent():
    """Agent Asisten Umum yang cerdas, cepat, dan serbaguna.
    Ditenagai model AntiGravityModel (Gemini 3.8 Flash High) dengan 1M konteks dan respons kilat.
    """
    tools = [get_current_time, kalkulator]
    llm = get_role_llm("general").bind_tools(tools)

    system_prompt = SystemMessage(
        content=(
            "Anda adalah General Assistant cerdas yang ditenagai model AntiGravity 9Router. "
            "Anda mampu menjawab berbagai pertanyaan umum, mengeksekusi perhitungan presisi, "
            "dan memberikan bantuan dengan cepat, ramah, dan akurat dalam bahasa Indonesia."
        )
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
