#!/usr/bin/env python3
import sys
import os
import argparse
from langchain_core.messages import HumanMessage
from agents import get_agent, list_agents, AGENTS_REGISTRY


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Runner untuk Agent LangGraph Multi-Agent dengan model 9Router (AntiGravity, FreeGptCODEX, FreeKiroAI)."
    )
    parser.add_argument(
        "first_arg",
        nargs="?",
        default=None,
        help="Nama agent (team, auto, coder, researcher, general) ATAU langsung prompt/instruksi.",
    )
    parser.add_argument(
        "prompt_arg",
        nargs="?",
        default=None,
        help="Instruksi atau pertanyaan (jika argumen pertama adalah nama agent).",
    )
    parser.add_argument(
        "--agent",
        "-a",
        default=None,
        help="Nama agent spesifik jika ingin eksplisit.",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="Tampilkan daftar semua agent dan kepintaran model masing-masing.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Output bersih tanpa banner/log progres (ideal untuk integrasi OpenCode/otomatisasi).",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        default=True,
        help="Aktifkan streaming token hasil akhir (default: True).",
    )
    parser.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Matikan streaming, tunggu seluruh output selesai.",
    )

    args = parser.parse_args()
    return args


def show_agent_list():
    print("================================================================================")
    print("      Daftar LangGraph Multi-Agent 9Router (Sesuai Kepintaran Model)           ")
    print("================================================================================")
    for name, desc in list_agents().items():
        print(f"\n  • \033[1m{name.upper()}\033[0m :")
        print(f"    {desc}")
    print("\n--------------------------------------------------------------------------------")
    print("Contoh Penggunaan:")
    print("  python3 run.py \"Bandingkan Redis vs Kafka dan buatkan implementasinya\"   # Auto / Team")
    print("  python3 run.py team \"Buatkan arsitektur microservices clean architecture\" # Berpikir Bareng")
    print("  python3 run.py coder \"Buatkan decorator retry di Python\"                # Spesialis Coder")
    print("  python3 run.py researcher \"Kelebihan dan kekurangan ACID vs BASE\"       # Spesialis Riset")
    print("  python3 run.py general \"Berapa 125 * 32?\"                               # Asisten Umum")
    print("================================================================================")


def main():
    args = parse_arguments()

    if args.list:
        show_agent_list()
        return

    # Penentuan cerdas agent dan prompt
    first = args.first_arg
    second = args.prompt_arg
    explicit_agent = args.agent

    if explicit_agent:
        selected_agent = explicit_agent.lower().strip()
        prompt = first or second
    elif first and first.lower() in AGENTS_REGISTRY:
        selected_agent = first.lower()
        prompt = second
    elif first and not second:
        # User langsung memasukkan prompt: python3 run.py "instruksi..."
        # Default otomatis ke 'team' (berpikir bareng-bareng)
        selected_agent = "team"
        prompt = first
    elif first and second:
        # Kasus nama agent tidak dikenali, gabungkan jadi prompt
        selected_agent = "team"
        prompt = f"{first} {second}"
    else:
        prompt = None
        selected_agent = "team"

    if not prompt:
        print("Penggunaan Cepat:")
        print("  python3 run.py \"<pertanyaan / tugas kompleks>\"")
        print("  python3 run.py <team|auto|coder|researcher|general> \"<pertanyaan>\"")
        print("\nUntuk melihat daftar agent lengkap:")
        print("  python3 run.py --list")
        sys.exit(1)

    is_tty = sys.stdout.isatty() and not args.quiet

    try:
        if is_tty:
            print(f"\033[36m⚡ [9Router Multi-Agent]\033[0m Memproses dengan agent '\033[1m{selected_agent}\033[0m'...", file=sys.stderr)
            if selected_agent in ("team", "auto"):
                print("\033[33m🧠 [Kolaborasi Aktif]\033[0m Researcher (FreeKiroAI) + Coder (FreeGptCODEX) berpikir bareng-bareng...", file=sys.stderr)

        agent_app = get_agent(selected_agent)
        
        # Eksekusi graf LangGraph
        result = agent_app.invoke({"messages": [HumanMessage(content=prompt)]})
        final_message = result["messages"][-1]
        
        # Output hasil akhir
        if is_tty:
            print("\033[32m✔ [Selesai]\033[0m\n", file=sys.stderr)

        print(final_message.content)

    except KeyboardInterrupt:
        print("\nOperasi dihentikan oleh pengguna.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error pada agent '{selected_agent}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
