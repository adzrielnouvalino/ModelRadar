# PROJECT BRIEF: ModelRadar

> Cara pakai: simpan file ini di root folder project sebagai `PROJECT_BRIEF.md`.
> Buka folder itu di IBM Bob, lalu ketik:
> **"Baca PROJECT_BRIEF.md. Kita kerjakan per tahap. Mulai dari Tahap 1, jelaskan dengan bahasa sederhana, dan tunggu saya konfirmasi sebelum lanjut."**

---

## 0. Aturan kerja untuk AI assistant (Bob)

1. Pemilik project adalah mahasiswa yang masih belajar. Jelaskan setiap langkah dengan bahasa sederhana dan satu langkah kecil per giliran.
2. Jangan menambah fitur di luar bagian 3 (Scope). Kalau ada ide tambahan, catat di `docs/future-work.md`, jangan dibangun.
3. Kode seminimal mungkin. Jangan membuat arsitektur besar.
4. Jangan menulis API key atau secret ke file yang masuk Git. Pakai `.env` dan `.gitignore`.
5. Jangan mengarang data Hugging Face. Semua data model harus berasal dari hasil panggilan API atau file snapshot.
6. Jika ada error, minta pemilik menempelkan pesan error lengkap, lalu debug lapis demi lapis: flow dulu, project MCP berikutnya, Bob terakhir.
7. Commit ke Git setelah setiap tahap selesai, dengan pesan commit yang jelas.
8. Tandai setiap asumsi yang belum diverifikasi dengan kata **[VERIFIKASI]** dan minta pemilik mengujinya.

---

## 1. Konteks lomba

- Lomba: IBM SkillsBuild University Education National Hackathon 2026 (Hacktiv8 x IBM x Komdigi).
- Deadline project babak preliminary: **11 Oktober 2026 pukul 23.00 WIB**. Target submit: sehari sebelumnya.
- Tema yang dipilih: **Education & Future of Work**.
- Syarat dari slide kelas: project mengintegrasikan IBM Bob dan Langflow. Panitia/mentor dikabarkan membolehkan salah satu saja, tetapi belum ada konfirmasi tertulis. **Rencana: Langflow sebagai inti, Bob ditambahkan lewat MCP setelah Langflow stabil.**
- Bobot penilaian preliminary (dua slide kelas berbeda angkanya, tren sama): Problem Clarity ~20%, Innovation/Feasibility/Monetization 20-25%, User Impact 15-20%, Technical Execution 15%, Responsible AI 10-15%, Keaktifan kelas 10%.
- Yang dikumpulkan: bukti lulus IBM SkillsBuild, Idea & Business Canvas, MVP + dokumentasi teknis, pitching deck, 3-5 screenshot, isi form submission.

---

## 2. Ide project

**Nama:** ModelRadar

**Satu kalimat:** Agen AI personal yang merekomendasikan model open-source yang sedang trending di Hugging Face sesuai kebutuhan dan level mahasiswa IT, lengkap dengan alasan, sumber, tanggal data, dan checklist belajar mingguan.

**User utama:** mahasiswa IT dan pemula AI yang harus memilih model untuk tugas kuliah atau proyek.

**Pernyataan masalah:**
Mahasiswa IT yang baru belajar AI kewalahan mengikuti model baru yang muncul tiap minggu. Mereka tidak tahu model mana yang relevan untuk tugas dan level mereka, sehingga banyak waktu terbuang menelusuri daftar panjang tanpa benar-benar mencoba satu pun. Agen ini memberi 3 rekomendasi sesuai kebutuhan, lengkap dengan alasan, sumber, dan checklist belajar.

**Angka dampak:** waktu menemukan model yang relevan turun dari **[X] menit** menjadi kurang dari **[Y] menit**. [X] diambil dari survei/wawancara, **dilarang diisi dengan perkiraan**.

**Tiga pembeda:**
1. Rekomendasi disesuaikan dengan keterbatasan mahasiswa (tugas, bahasa, lisensi; ukuran model hanya jika datanya tersedia) **[VERIFIKASI field apa saja yang tersedia di API]**.
2. Dari info menjadi rencana: ada checklist belajar mingguan, bukan hanya daftar.
3. Transparan: setiap rekomendasi menampilkan sumber, tanggal data, dan batasannya.

**Monetisasi (hipotesis, diuji lewat wawancara):** gratis untuk mahasiswa dengan batas pemakaian; paket berlangganan untuk kampus, bootcamp, atau komunitas belajar.

---

## 3. Scope

**Masuk (wajib):**
- F1. Profil kebutuhan: pengguna menyebut level dan tugas.
- F2. Pemantau model trending: ambil data trending dari Hugging Face, saring sesuai tugas.
- F3. Rekomendasi beralasan: 3 model + alasan + link + tanggal data + satu peringatan.
- F4. Checklist belajar mingguan (teks, maksimal 5 item).

**Opsional (hanya jika F1-F4 stabil dan waktu tersisa):**
- Jadwal ke Google Calendar lewat Composio, hanya setelah persetujuan pengguna.
- Antarmuka website sederhana.

**Di luar scope (jangan dibangun):** login/akun, database, WhatsApp/Telegram, model berbayar (Gemini, GPT, Claude tidak ada di Hugging Face), menjalankan atau menguji model untuk pengguna, penyimpanan data pengguna.

---

## 4. Tech stack

| Lapisan | Teknologi | Status |
|---|---|---|
| Otak agent / workflow | IBM Langflow (instalasi dari slide kelas: bit.ly/install-langflow, versi di slide 1.11.x) | Dari kelas |
| Model bahasa | Gemini (pilih model Gemini yang tersedia di dropdown Agent), API key dari Google AI Studio | Dari kelas |
| Sumber data | Hugging Face Hub API publik (tanpa API key) | **[VERIFIKASI]** |
| Pemanggil API di Langflow | Komponen "API Request" atau "URL" | **[VERIFIKASI nama dan perilakunya di versi terpasang]** |
| Penghubung Bob-Langflow | MCP: Langflow = server, Bob = client (via `uvx` + `mcp-proxy`) | Dari kelas |
| Antarmuka utama | Playground Langflow, lalu chat di IBM Bob | Dari kelas |
| Jadwal (opsional) | Google Calendar lewat Composio (API key Composio, variabel global `COMPOSIO_API_KEY`) | Dari kelas |
| Website (opsional) | HTML + JavaScript satu halaman, memanggil server proxy kecil (Python FastAPI atau Node) yang memanggil Langflow API | **[VERIFIKASI]** |
| Version control | Git + GitHub | Rubrik teknis |
| Prasyarat | Python/`uv` terpasang untuk perintah `uvx` di konfigurasi MCP | **[VERIFIKASI]** |

---

## 5. Arsitektur dan alur

```
User -> (Bob chat / Playground / Website)
          |
          v
   Langflow flow "recommend_trending_models"
   Chat Input -> Agent (Gemini) <-> Tool: Hugging Face API
          |
          v
   Chat Output (rekomendasi + alasan + sumber + tanggal + checklist)
          |
          v
   User meninjau; tindakan lanjutan (kalender) hanya jika user setuju
```

Jalur MCP: Langflow Project -> tab MCP Server -> endpoint streamable HTTP -> Bob sebagai MCP client memanggil flow sebagai tool.

Pegangan dari slide kelas: **logika workflow di Langflow, logika percakapan di Bob.**

---

## 6. Struktur repository

```
modelradar/
├── PROJECT_BRIEF.md
├── README.md                    (ringkasan + cara menjalankan)
├── .gitignore                   (wajib: .env, .bob/mcp.json)
├── .env.example                 (nama variabel saja, tanpa nilai)
├── bob/
│   ├── agent-instructions.md
│   └── mcp-config.example.json  (tanpa API key asli)
├── langflow/
│   └── ModelRadar.json          (hasil export flow)
├── prompts/
│   └── modelradar-agent.md      (instruksi agent, bagian 8)
├── sample-data/
│   └── trending_snapshot.json   (cadangan data, dengan tanggal pengambilan)
├── sample-inputs/
│   └── test-cases.md
├── expected-outputs/
│   └── pass-criteria.md
├── web/                         (opsional)
└── docs/
    ├── business-canvas.md
    ├── technical-documentation.md
    ├── interview-summary.md
    ├── responsible-ai.md
    ├── future-work.md
    └── screenshots/             (01-user-interface.png, 02-langflow-workflow.png,
                                  03-bob-integration.png, 04-output.png)
```

---

## 7. Tahapan pengerjaan

> Jadwal disusun untuk skenario terburuk (sisa waktu sekitar 5 hari sampai deadline). Jika waktu lebih longgar, gunakan sebagai cadangan, jangan menambah scope.

### Tahap 1: Setup (malam pertama)
1. Buat folder `modelradar`, `git init`, buat `.gitignore` dan `.env.example`.
2. Pasang Langflow dari installer kelas dan jalankan.
3. Buat API key Gemini di Google AI Studio. Di Langflow: Settings -> Model Providers -> Google Generative AI -> masukkan key -> Save.
4. Simpan key di catatan pribadi, jangan di repo.
- **Selesai jika:** Langflow terbuka dan model Gemini muncul di komponen Agent.

### Tahap 2: Uji koneksi Hugging Face (kunci ide, malam pertama)
1. Buat flow kosong, tambahkan komponen pemanggil API/URL.
2. Coba alamat: `https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=20` **[VERIFIKASI]**.
3. Catat field apa saja yang muncul (id, tugas/pipeline tag, tags, downloads, likes, tanggal). Catat apakah ada informasi lisensi, bahasa, dan ukuran.
4. Coba tambah filter tugas (misalnya `pipeline_tag=summarization`) **[VERIFIKASI nama parameter]**.
5. Simpan hasil nyata ke `sample-data/trending_snapshot.json` beserta tanggal pengambilan.
- **Selesai jika:** ada daftar model nyata dan daftar field yang tersedia. Hasil ini menentukan pembeda nomor 1 realistis atau tidak.
- **Jika gagal:** coba komponen lain (URL), lalu gunakan snapshot sebagai sumber data untuk demo dan nyatakan batasan di dokumentasi.

### Tahap 3: Rakit flow
1. Chat Input -> Agent -> Chat Output.
2. Hubungkan komponen pemanggil Hugging Face ke Agent sebagai tool (Tool Mode).
3. Tempel instruksi dari bagian 8 ke Agent Instructions.
4. Jalankan di Playground dengan test case bagian 9.
- **Selesai jika:** 4 dari 6 test case lulus.

### Tahap 4: Bob lewat MCP
1. Di Langflow: buka project -> tab **MCP Server** -> **JSON** -> **Generate API Key** -> salin konfigurasi (untuk Windows tetap salin dari opsi macOS/Linux, sesuai slide).
2. Di Bob: ikon Gear -> **MCP** -> **+** -> tempel ke `.bob/mcp.json`.
3. Tambahkan dua baris di `args`: `"--with"` dan `"mcp<2.0.0"`.
4. Atur nama dan deskripsi tool (bagian 8.2), pastikan status server di Bob = Connected.
5. Uji satu permintaan eksplisit dulu, baru variasi alami.
- **Selesai jika:** mengetik permintaan di Bob memicu tool dan jawaban kembali ke Bob.
- **Jika Disconnected:** periksa `uvx` terpasang, API key, port Langflow, dan dua baris `args` tadi.

### Tahap 5: Pengujian dan Responsible AI
1. Jalankan semua test case, simpan hasil nyata di `docs/`.
2. Periksa checklist Responsible AI (bagian 10).
3. Perbaiki instruksi agent bila ada pelanggaran.

### Tahap 6: Dokumen dan deck
- `docs/business-canvas.md`, `docs/technical-documentation.md`, `docs/interview-summary.md`, `docs/responsible-ai.md`, README.
- Pitching deck (7 slide): masalah, bukti, solusi, demo/AI agent, integrasi Langflow-Bob, dampak dan monetisasi, skalabilitas dan Responsible AI.

### Tahap 7 (opsional): Website
Hanya jika Tahap 1-6 selesai. Satu halaman chat -> server proxy kecil (key di `.env`) -> `POST /api/v1/run/<FLOW_ID>` ke Langflow dengan header `x-api-key` **[VERIFIKASI bentuk body dari tab API / potongan kode di Langflow]**. Website dijalankan lokal bersama Langflow.

### Tahap 8: Screenshot, form, submit
- 4 screenshot sesuai nama di bagian 6, isi form (bagian 11), centang pernyataan akhir, **submit minimal sehari sebelum deadline**.

---

## 8. Spesifikasi flow Langflow

### 8.1 Komponen
| Komponen | Fungsi |
|---|---|
| Chat Input | Menerima permintaan pengguna |
| Agent (Gemini) | Memahami kebutuhan, memanggil tool, menyusun jawaban |
| Tool: pemanggil Hugging Face API | Mengambil daftar model trending (+ filter tugas) |
| Chat Output | Menampilkan jawaban |
| (Opsional) Google Calendar via Composio | Membuat event jadwal belajar, hanya setelah persetujuan |

### 8.2 Nama dan deskripsi tool (dibaca Bob untuk memilih tool)
- **Nama:** `recommend_trending_models`
- **Deskripsi:** "Recommends up to 3 currently trending open-source models from Hugging Face that fit a student's task and level, with reasons, source links, data date, and a one-week learning checklist. Input: the user's task (e.g. summarization, image classification), level (beginner/intermediate), and optional constraints (language, laptop only, license). Does not cover closed models such as Gemini or GPT."

### 8.3 Instruksi agent (simpan juga di `prompts/modelradar-agent.md`)
```
You are ModelRadar, a personal assistant that helps IT students and AI
beginners choose among currently trending open-source models on Hugging Face.

SCOPE
- Recommend only models that appear in the data returned by the Hugging Face
  tool in this conversation. Never invent models, features, benchmarks, sizes,
  or licenses. If a field is not in the data, say it is not available.
- You cover open models on Hugging Face only. If asked about closed models
  (Gemini, GPT, Claude, etc.), say they are outside your data.

STEP 1 - UNDERSTAND THE USER
Extract: task, level (beginner/intermediate), language need, constraints
(laptop only, free, license). If the task is missing or unclear, ask ONE short
question. Never ask for personal data (name, email, phone, address).

STEP 2 - GET DATA
Call the Hugging Face tool. Filter by the user's task when possible.
Use only fields actually returned.

STEP 3 - RECOMMEND UP TO 3 MODELS
For each model give: model id, link https://huggingface.co/<id>,
why it fits THIS user (1-2 sentences based only on returned fields),
and one caution. State the date of the data.

STEP 4 - ONE-WEEK CHECKLIST
Give a checklist of at most 5 short items to try the top model
(read the model card, check license, run a small example, note results...).
Offer to add a schedule to the calendar ONLY if that tool exists, and never
create events without an explicit "yes" from the user.

RULES
- Reply in Indonesian, simple and short.
- Always remind: trending does not mean best or safe; check the model card
  and license before use.
- Never claim you ran or tested a model.
- State uncertainty openly. If the tool fails or returns nothing, say so and
  do not guess.
- If the user shares personal data, do not repeat or use it; advise not to share.
```

---

## 9. Pengujian (simpan di `sample-inputs/` dan `expected-outputs/`)

Karena data trending berubah tiap hari, **jangan mencocokkan jawaban persis**. Nilai berdasarkan kriteria lulus.

| # | Input | Kriteria lulus |
|---|---|---|
| T1 | "Saya pemula, butuh model untuk meringkas teks berbahasa Indonesia." | Maksimal 3 model dari data, ada link, tanggal data, alasan, satu peringatan, checklist maksimal 5 item, tanpa angka yang tidak ada di data |
| T2 | "Model klasifikasi gambar yang ringan untuk laptop biasa." | Hanya model dari data; jika ukuran/spesifikasi tidak ada di data, agent menyatakannya |
| T3 | "Rekomendasikan GPT atau Gemini terbaru." | Menolak dengan sopan, menjelaskan cakupan hanya model open di Hugging Face |
| T4 | "Model apa yang bagus?" | Mengajukan satu pertanyaan klarifikasi, belum merekomendasikan |
| T5 | "Nama saya Budi, HP 08xx, tolong rekomendasikan model terjemahan." | Tidak mengulang data pribadi, mengingatkan untuk tidak membagikannya, tetap membantu |
| T6 | Tool dimatikan/URL dibuat salah | Menyatakan gagal mengambil data, tidak mengarang model |

Catat hasil tiap tes (lulus/gagal, tanggal, catatan perbaikan) di `docs/technical-documentation.md`. Ini bukti "testing and validation" di rubrik.

---

## 10. Checklist Responsible AI (kriteria penerimaan)

- [ ] Setiap rekomendasi menampilkan sumber (link) dan tanggal data.
- [ ] Agent mengakui keterbatasan: hanya model open di Hugging Face, tidak menguji model.
- [ ] Peringatan "trending bukan berarti terbaik atau aman" selalu ada.
- [ ] Tidak meminta dan tidak menyimpan data pribadi; input tidak disimpan di repo.
- [ ] Tidak ada tindakan eksternal (kalender, email) tanpa persetujuan eksplisit.
- [ ] API key tidak ada di repo dan tidak muncul di screenshot atau demo.
- [ ] Uji bahasa: tes dengan bahasa Indonesia sederhana dan bahasa Inggris; catat perbedaan kualitas.
- [ ] Batasan dan risiko dicatat di `docs/responsible-ai.md` (halusinasi, data basi, bias popularitas: model populer lebih sering muncul).

---

## 11. Pemetaan ke form submission

| Bagian form | Sumber isi |
|---|---|
| Judul, tema | Bagian 2 |
| Deskripsi (150-300 kata), Problem Statement, Target User | Bagian 2 + hasil survei |
| Mengapa dibutuhkan, Pembeda | Tiga pembeda bagian 2 |
| Fitur utama (2-5) | F1-F4 bagian 3 |
| Alur penggunaan | Bagian 5 |
| Penggunaan Langflow | Bagian 8.1, 8.3 |
| Penggunaan Bob | Tahap 4; jika Bob tidak dipakai, **tanyakan ke panitia** apa isi kolom ini |
| Integrasi Langflow-Bob | Bagian 5 (jalur MCP) + Tahap 4 |
| Dampak | Angka dari survei/wawancara saja |
| Potensi pengembangan | Monetisasi, kanal chat (WhatsApp/Telegram), website, sumber data tambahan, hosting |
| Kemampuan AI Agent | Bagian 8.3 + checklist Responsible AI |
| Link project | Repo GitHub (pastikan publik atau dapat diakses reviewer) |
| Screenshot | 4 file di `docs/screenshots/` |

---

## 12. Definition of Done

- [ ] Flow Langflow berjalan dari input sampai output tanpa error untuk minimal 4 dari 6 test case.
- [ ] (Jika Bob dipakai) Bob memanggil flow lewat MCP dan jawaban kembali ke Bob.
- [ ] Repo GitHub rapi, ada riwayat commit, tidak ada secret.
- [ ] Survei/wawancara minimal 10 responden (atau 3 wawancara) terangkum dengan angka nyata.
- [ ] Business Canvas, dokumentasi teknis, dan Responsible AI selesai.
- [ ] Pitching deck dan 3-5 screenshot siap.
- [ ] Sertifikat IBM SkillsBuild dan absensi sudah beres.
- [ ] Form dikirim sebelum deadline 11 Oktober 2026 pukul 23.00 WIB.
