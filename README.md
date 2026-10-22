# LangGraph 9Router Agents (OpenCode Skills Ready)

Struktur agent LangGraph yang rapi dan modular, terhubung ke model Combo 9Router. Anda bisa langsung memerintah agent dari OpenCode via menu `/skills`.

---

## 📁 Struktur Proyek

```text
langgraph-9router-agents/
├── agents/                     # Direktori agent-agent Anda
│   ├── __init__.py             # Registry daftar agent yang tersedia
│   ├── core.py                 # Koneksi LLM ke 9Router Combo
│   ├── general.py              # Agent 'general': Asisten umum + tools dasar
│   ├── coder.py                # Agent 'coder': Software engineer & debugging
│   └── researcher.py           # Agent 'researcher': Analisis & riset komparatif
├── run.py                      # Eksekutor 1 baris untuk agent
├── .env                        # Konfigurasi 9Router (API Key, Combo Model)
├── requirements.txt            # Dependensi Python
└── .agents/skills/my-agents/   # Skill OpenCode (Manual via /skills)
    └── SKILL.md
```

---

## 🎯 Cara Pakai di OpenCode

Anda **tidak perlu** repot menjalankan CLI interaktif manual. Cukup gunakan fitur `/skills`:

1. Di chat OpenCode, ketik `/skills` dan pilih **`my-agents`**.
2. Berikan perintah Anda, misalnya:
   - *"Gunakan agent coder untuk buatkan script backup database PostgreSQL"*
   - *"Minta agent researcher bandingkan Apache Kafka vs RabbitMQ"*
   - *"Minta agent general hitung 250 * 14 + 18"*
3. OpenCode akan otomatis memanggil agent yang sesuai dan menampilkan hasilnya.

---

## 💻 Menjalankan Manual (Opsional)

Jika ingin mencoba dari terminal:

```bash
# Menampilkan daftar agent
python3 run.py --list

# Menjalankan agent tertentu
python3 run.py general "Berapa jam sekarang?"
python3 run.py coder "Buatkan regex untuk validasi email"
python3 run.py researcher "Kelebihan dan kekurangan Vue 3 vs React"
```

---

## ➕ Cara Menambah Agent Baru

Sangat mudah dan rapi:
1. Buat file baru di folder `agents/`, contoh `agents/designer.py`.
2. Daftarkan agent tersebut di `agents/__init__.py`.
3. Agent baru langsung siap dipakai!
