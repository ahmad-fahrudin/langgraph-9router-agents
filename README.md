# LangGraph 9Router Multi-Agent System

Sistem orkestrasi Multi-Agent berbasis **LangGraph** yang ditenagai oleh model-model spesialis dari **9Router** (`FreeGptCODEX`, `FreeKiroAI`, dan `AntiGravityModel`). Dirancang untuk penalaran mandiri dan kolaborasi multi-agent tingkat tinggi via CLI / Python.

---

## 🧠 Pembagian Kepintaran Model (Intelligence Mapping)

Setiap agent dipasangkan dengan model yang paling unggul di ranah kompetensinya:

| Agent | Model 9Router | Spesialisasi & Kepintaran | Latensi / Suhu |
| :--- | :--- | :--- | :--- |
| **`coder`** | **`FreeGptCODEX`** *(GPT-6 Luna)* | Rekayasa software tingkat produksi, penulisan kode modular, type-safe, algoritma, dan debugging mendalam. | ~3.8 detik / `temp=0.1` |
| **`researcher`** | **`FreeKiroAI`** *(DeepSeek 3.2 & Qwen3)* | Riset analitis mendalam, evaluasi komparatif (*trade-offs*, pro-kontra), arsitektur sistem, dan eksplorasi *edge cases*. | ~6.5 detik / `temp=0.3` |
| **`general`** | **`AntiGravityModel`** *(Gemini 3.8 Flash High)* | Asisten serbaguna, pemrosesan cepat dengan 1M konteks, dan *tool calling* presisi (kalkulator matematika & waktu). | Kilat / `temp=0.5` |
| **`team`** *(Default)* | **Multi-Model Kolaboratif** | **Berpikir Bareng-bareng**: Researcher merancang arsitektur & batas sistem $\rightarrow$ Coder mengimplementasikan kode produksi $\rightarrow$ Supervisor menyusun konsensus solusi final. | Terorkestrasi / `temp=0.1` |
| **`auto`** | **Smart Router** | Evaluasi instan: otomatis memilih rute langsung untuk tugas sederhana, atau kolaborasi tim untuk tugas kompleks. | Adaptif |

---

## 💻 Penggunaan via CLI / Terminal

```bash
# Menampilkan daftar agent dan kapabilitas model
python3 run.py --list

# 1. Mode Kolaborasi Tim (Berpikir Bareng-bareng)
python3 run.py team "Bandingkan Redis vs Kafka dan buatkan implementasinya di Python"

# 2. Spesialis Koding Murni (Cepat)
python3 run.py coder "Buatkan implementasi LRU Cache di Python"

# 3. Spesialis Riset & Analisis Konseptual
python3 run.py researcher "Kelebihan dan kelemahan database dokumen vs relasional"

# 4. Asisten Umum & Perhitungan
python3 run.py general "Berapa 100 * 25?"
```
