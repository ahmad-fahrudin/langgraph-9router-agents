---
name: my-agents
description: >-
  Manual-only skill for LangGraph 9Router Agents. DO NOT activate automatically.
  Activate ONLY when the user explicitly runs '/skills' or asks to use 'my-agents'.
---

# My Agents (LangGraph + 9Router Combo)

Skill ini digunakan untuk mendelegasikan tugas ke agent-agent LangGraph yang berjalan menggunakan model Combo 9Router.

## Daftar Agent yang Tersedia
- **`general`** : Asisten umum, percakapan, cek waktu, kalkulator matematika.
- **`coder`** : Spesialis penulisan kode, software engineering, refactor, dan debugging.
- **`researcher`** : Spesialis riset mendalam, analisa komparatif, dan sintesis konsep.

## Cara Menjalankan Agent
Ketika skill ini dipanggil, jalankan agent yang sesuai dengan perintah shell:

```bash
python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py <nama_agent> "<instruksi/pertanyaan>"
```

### Contoh Eksekusi:
1. Jika pengguna meminta bantuan umum atau perhitungan:
   ```bash
   python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py general "Berapa 125 * 18?"
   ```
2. Jika pengguna meminta membuatkan atau mereview kode:
   ```bash
   python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py coder "Buat fungsi rekursif fibonacci di Python"
   ```
3. Jika pengguna meminta riset atau perbandingan:
   ```bash
   python3 /home/fahrudin/Projects/langgraph-9router-agents/run.py researcher "Bandingkan Redis vs Memcached"
   ```

Setelah perintah dieksekusi, tampilkan hasil respons dari agent kepada pengguna secara rapi.
