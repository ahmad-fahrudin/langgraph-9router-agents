# LangGraph 9Router Multi-Agent System (Berpikir Bareng-bareng)

Sistem orkestrasi Multi-Agent berbasis **LangGraph** yang ditenagai oleh model-model spesialis dari **9Router** (`FreeGptCODEX`, `FreeKiroAI`, dan `AntiGravityModel`). Dirancang untuk penalaran kolaboratif tingkat tinggi (**berpikir bareng-bareng**) dan generasi hasil yang ultra cepat, terintegrasi secara otomatis dengan **OpenCode** tanpa perlu manual `/skills`.

---

## 🧠 Pembagian Kepintaran Model (Intelligence Mapping)

Setiap agent dipasangkan dengan model yang paling unggul di ranah kompetensinya:

| Agent | Model 9Router | Spesialisasi & Kepintaran | Latensi / Suhu |
| :--- | :--- | :--- | :--- |
| **`coder`** | **`FreeGptCODEX`** *(GPT-6 Luna)* | Rekayasa software tingkat produksi, penulisan kode modular, type-safe, algoritma, dan debugging mendalam. | ~3.8 detik / `temp=0.1` |
| **`researcher`** | **`FreeKiroAI`** *(DeepSeek 3.2 & Qwen3)* | Riset analitis mendalam, evaluasi komparatif (*trade-offs*, pro-kontra), arsitektur sistem, dan eksplorasi *edge cases*. | ~6.5 detik / `temp=0.3` |
| **`general`** | **`AntiGravityModel`** *(Gemini 3.8 Flash High)* | Asisten serbaguna, pemrosesan cepat dengan 1M konteks, dan *tool calling* presisi (kalkulator matematika & waktu). | Kilat / `temp=0.5` |
| **`team`** *(Default)* | **Multi-Model Kolaboratif** | **Berpikir Bareng-bareng**: Researcher merancang arsitektur & batas sistem, Coder mengimplementasikan kode produksi, dan Supervisor menyusun konsensus solusi final. | Terorkestrasi / `temp=0.1` |
| **`auto`** | **Smart Router** | Evaluasi instan: otomatis memilih rute langsung untuk tugas sederhana, atau kolaborasi tim untuk tugas kompleks. | Adaptif |

---

## ⚡ Fitur Kecepatan & Ketahanan (Speed & Reliability)

1. **Automatic Model Fallback**: Jika salah satu model spesialis sibuk atau mengalami kendala jaringan, sistem secara otomatis beralih ke `AntiGravityModel` tanpa *interupsi* atau kegagalan eksekusi.
2. **Instance Caching**: Inisialisasi klien model di-cache untuk menghilangkan overhead koneksi berulang.
3. **Smart CLI**: Mendukung eksekusi langsung tanpa nama agent (`python3 run.py "<prompt>"`), otomatis mengaktifkan mode kolaborasi tim.
4. **Clean Output**: Opsi `--quiet` (`-q`) untuk integrasi bersih dengan alat pihak ketiga dan otomatisasi OpenCode.

---

## 📁 Struktur Proyek

```text
langgraph-9router-agents/
├── agents/                     # Direktori agent LangGraph
│   ├── __init__.py             # Registry & factory agent
│   ├── core.py                 # Manajemen koneksi LLM, caching & fallback
│   ├── team.py                 # Graf kolaboratif: Researcher + Coder + Supervisor (Berpikir Bareng-bareng)
│   ├── coder.py                # Agent Coder (FreeGptCODEX)
│   ├── researcher.py           # Agent Researcher (FreeKiroAI)
│   └── general.py              # Agent General Assistant (AntiGravityModel)
├── run.py                      # CLI Runner cerdas
├── .env                        # Konfigurasi model dan temperature spesialis
├── .env.example                # Contoh template konfigurasi
├── requirements.txt            # Dependensi Python
├── AGENTS.md                   # Direktif instruksi otomatis untuk OpenCode
└── .agents/skills/my-agents/   # Skill konfigurasi OpenCode
    └── SKILL.md
```

---

## 🚀 Cara Penggunaan

### 1. Otomatis di OpenCode (Tanpa Perlu `/skills`)
Ketika digunakan di OpenCode, agen OpenCode akan **secara otomatis** memanggil sistem multi-agent ini saat menghadapi tugas pemrograman, arsitektur, atau riset kompleks. Anda tidak perlu mengetikkan `/skills` lagi.

### 2. Melalui Terminal / CLI

```bash
# Menampilkan daftar agent dan kapabilitas model
python3 run.py --list

# 1. Otomatis Berpikir Bareng-bareng (Default)
python3 run.py "Bandingkan Redis vs Kafka dan buatkan implementasinya di Python"

# 2. Eksplisit Menjalankan Tim Kolaboratif
python3 run.py team "Rancang sistem distributed rate limiter dengan token bucket"

# 3. Spesialis Koding Murni (Cepat)
python3 run.py coder "Buatkan implementasi LRU Cache di Python"

# 4. Spesialis Riset & Analisis Konseptual
python3 run.py researcher "Kelebihan dan kelemahan database dokumen vs relasional"

# 5. Asisten Umum & Perhitungan
python3 run.py general "Berapa 2^16 dan hitung sin(pi/4)?"
```
