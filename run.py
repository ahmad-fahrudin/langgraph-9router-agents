#!/usr/bin/env python3
import sys
import argparse
from langchain_core.messages import HumanMessage
from agents import get_agent, list_agents


def main():
    parser = argparse.ArgumentParser(
        description="Runner untuk Agent LangGraph dengan model 9Router Combo."
    )
    parser.add_argument(
        "agent",
        nargs="?",
        default="general",
        help="Nama agent (contoh: general, coder, researcher).",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Instruksi atau pertanyaan untuk agent.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Tampilkan daftar semua agent yang tersedia.",
    )

    args = parser.parse_args()

    # Jika hanya meminta list agent
    if args.list:
        print("Daftar Agent LangGraph yang Tersedia:")
        for name, desc in list_agents().items():
            print(f"  • {name:<12} : {desc}")
        return

    # Validasi prompt
    if not args.prompt:
        print("Penggunaan:")
        print("  python3 run.py <nama_agent> \"<perintah>\"")
        print("\nContoh:")
        print("  python3 run.py general \"Berapa 125 * 8?\"")
        print("  python3 run.py coder \"Buatkan fungsi Python untuk membalik string\"")
        print("  python3 run.py researcher \"Bandingkan PostgreSQL vs MySQL\"")
        print("\nUntuk melihat daftar agent:")
        print("  python3 run.py --list")
        sys.exit(1)

    try:
        agent_app = get_agent(args.agent)
        result = agent_app.invoke({"messages": [HumanMessage(content=args.prompt)]})
        final_message = result["messages"][-1]
        print(final_message.content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
