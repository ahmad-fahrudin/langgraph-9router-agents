---
name: my-agents
description: >-
  LangGraph 9Router collaborative multi-agent reasoning and execution engine.
  Use this skill AUTOMATICALLY for complex problem solving, coding, refactoring,
  debugging, architecture design, in-depth research, algorithmic challenges,
  or whenever specialized AI agents (Coder on FreeGptCODEX, Researcher on FreeKiroAI,
  General Assistant on AntiGravityModel) should collaborate and think together
  ('berpikir bareng-bareng') to produce high-speed, authoritative results.
---

# 9Router LangGraph Collaborative Multi-Agent System

Sistem Multi-Agent LangGraph yang ditenagai oleh model-model spesialis 9Router Combo:
- **`team`** (Default / Rekomendasi): Multi-agent kolaboratif penuh di mana **Researcher (FreeKiroAI)** dan **Coder (FreeGptCODEX)** berpikir bareng-bareng untuk menghasilkan rancangan arsitektur dan kode produksi terlengkap, disintesis oleh **Supervisor (AntiGravityModel)**.
- **`coder`**: Spesialis software engineering tingkat produksi, penulisan kode modular, refactoring, dan algoritma (FreeGptCODEX).
- **`researcher`**: Spesialis riset mendalam, analisis komparatif, evaluasi trade-off, dan arsitektur sistem (FreeKiroAI).
- **`general`**: Asisten umum untuk percakapan, cek waktu, dan kalkulasi matematika presisi (AntiGravityModel).
- **`auto`**: Smart router yang otomatis memilih antara delegasi instan untuk tugas sederhana atau kolaborasi tim untuk tugas kompleks.

## Eksekusi Otomatis (Tanpa Perlu /skills)

Jalankan perintah shell berikut langsung di terminal:

```bash
python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py team "<instruksi/pertanyaan>"
```

Atau untuk tugas spesifik:
- **Berpikir Bareng-bareng (Default & Direkomendasikan untuk tugas kompleks/koding):**
  ```bash
  python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py team "<pertanyaan/tugas>"
  ```
- **Spesialis Koding Murni (Cepat):**
  ```bash
  python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py coder "<tugas koding>"
  ```
- **Spesialis Riset & Analisis Teori:**
  ```bash
  python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py researcher "<topik riset>"
  ```
- **Asisten Umum & Kalkulasi:**
  ```bash
  python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py general "<perhitungan/pertanyaan umum>"
  ```

Tampilkan output yang dihasilkan oleh agent kepada pengguna secara rapi dan profesional.
