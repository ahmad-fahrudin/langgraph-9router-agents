# LangGraph 9Router Multi-Agent System Directives

Repositori ini adalah rumah bagi sistem **LangGraph 9Router Multi-Agent**.

## Model & Kepintaran Spesialis
Sistem ini menggunakan pembagian kerja berdasarkan kepintaran model spesialis dari 9Router:
1. **Coder (`FreeGptCODEX` / GPT-6 Luna)**:
   - Ultra cepat (~3.8s respons)
   - Spesialis rekayasa software, kode produksi, modularitas, penanganan error, dan algoritma.
2. **Researcher (`FreeKiroAI` / DeepSeek 3.2 & Qwen3 Coder Next)**:
   - Penalaran mendalam (deep reasoning)
   - Spesialis analisis komparatif, evaluasi trade-off sistem, arsitektur konseptual, dan eksplorasi skenario batas.
3. **General Assistant (`AntiGravityModel` / Gemini 3.8 Flash High)**:
   - 1M konteks, cepat & adaptif
   - Asisten percakapan, cek waktu, dan kalkulasi matematika akurat via Tool Calling.
4. **Team / Auto (Kolaborasi 'Berpikir Bareng-bareng')**:
   - Memadukan Researcher (Arsitektur & Edge Cases) + Coder (Implementasi Kode Produksi) + Synthesizer (Konsensus Solusi).

## Cara Penggunaan Otomatis
Jalankan melalui shell:
```bash
# Otomatis Berpikir Bareng-bareng (Default)
python3 run.py "<tugas/pertanyaan kompleks>"

# Eksplisit Mode Kolaborasi
python3 run.py team "<tugas/pertanyaan kompleks>"

# Spesialis Koding Murni
python3 run.py coder "<tugas koding>"

# Spesialis Riset & Analisis Teori
python3 run.py researcher "<topik riset>"

# Asisten Umum
python3 run.py general "<perhitungan/pertanyaan umum>"
```
