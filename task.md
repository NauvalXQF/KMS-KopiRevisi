# Paket Task Uji Usability — KMS Kopi Revisi

Skenario uji untuk 7 task knowledge (T1–T7). Format per task: tujuan →
skenario → langkah → pertanyaan verifikasi (+ kunci jawaban dari `database/seed.py`)
→ kriteria sukses → yang dicatat observer.

## Setup umum (wajib sebelum tiap peserta)

- Reset data: `python database/seed.py` (PIN pemilik `1111`, karyawan `2222`).
- Tulis PIN di meja peserta. Observer menyiapkan lembar observasi + stopwatch.
- Urutan eksekusi: **T1 → T2 (dirangkai) → T3 → T4 → T5 → T6 → T7 (T7 wajib terakhir)**.
- Metrik seragam per task: berhasil/gagal, waktu pengerjaan, jumlah klik, butuh bantuan (ya/tidak), 1 pertanyaan kepuasan singkat.
- Peran default peserta: **karyawan (2222)**, kecuali dinyatakan lain.

## T1 — Mencari resep minuman tertentu

- **Tujuan**: menguji kemampuan menemukan knowledge.
- **Skenario**: "Seorang pelanggan memesan Espresso. Cari resep standarnya."
- **Langkah**: login karyawan → Daftar Resep → ketik `espresso` di pencarian.
- **Verifikasi**: "Judul dokumen apa yang muncul paling atas?" → **Resep Espresso Standar**.
- **Sukses**: menemukan dalam ≤2x percobaan kata kunci.
- **Catat**: kata kunci yang dicoba; apakah memakai filter kategori. Catatan: pencarian hanya mencakup judul + deskripsi, bukan nama penulis.

## T2 — Membuka detail resep dan takaran bahan

- **Tujuan**: menguji akses terhadap informasi.
- **Skenario**: "Kamu barista shift pagi dan harus membuat Kopi Susu Gula Aren 12oz sesuai standar." (lanjutan T1)
- **Langkah**: dari hasil pencarian, buka detail resep tersebut, temukan takaran gula aren cair dan susu.
- **Verifikasi**: "Berapa takarannya?" → **gula aren cair 20ml, susu full cream 150ml**.
- **Sukses**: menyebutkan kedua angka tanpa bantuan.
- **Catat**: waktu, jumlah klik dari dashboard, apakah membuka lampiran/riwayat versi, kesulitan yang ditemui.

## T3 — Mencari SOP operasional

- **Tujuan**: menguji navigasi knowledge.
- **Skenario**: "Kamu dapat shift tutup toko pertama kali. Cari SOP-nya."
- **Langkah**: Daftar Resep → filter chip kategori **SOP** → buka **SOP Tutup Toko**.
- **Verifikasi**: "Sebutkan 2 dari 5 langkahnya!" → mis. **backflush mesin + catat stok akhir** (lengkapnya: backflush mesin, buang susu sisa, catat stok akhir, matikan listrik, kunci).
- **Sukses**: memakai filter kategori, bukan scroll manual.
- **Catat**: apakah peserta menemukan chip kategori tanpa diarahkan.

## T4 — Mencari informasi supplier/bahan

- **Tujuan**: menguji pencarian knowledge bisnis. Pilih SATU jalur per peserta.
- **Jalur Supplier (utama)**:
  - **Skenario**: "Susu habis. Ke siapa harus menghubungi dan berapa harga terakhirnya?"
  - **Langkah**: buka halaman Supplier → temukan kartu pemasok susu.
  - **Verifikasi**: "Suppliernya siapa, kontak dan harga terakhir berapa?" → **Susu Segar Jaya, 0812-0002 (Sari), Rp 22.000**.
  - **Sukses**: menemukan kartu + badge harga tanpa bantuan.
  - **Catat**: bila peserta malah membuka halaman Stok, catat sebagai temuan (bukan kesalahan).
- **Jalur Stok (alternatif)**:
  - **Skenario**: "Bagaimana cara menyimpan Susu Full Cream yang benar?"
  - **Verifikasi**: → **kulkas 2–4°C, habiskan 3 hari setelah dibuka**.

## T5 — Mencari solusi ketika bahan habis

- **Tujuan**: menguji akses knowledge troubleshooting.
- **Skenario**: "Gula aren habis di tengah shift ramai. Apa yang harus dilakukan?"
- **Langkah**: cari `stok habis` → buka **Prosedur Stok Habis**.
- **Verifikasi**: "Sebutkan 3 tindakannya!" → **tawarkan menu pengganti, catat di stok, hubungi supplier prioritas**.
- **Sukses**: menemukan dokumen dalam ≤3 menit.

## T6 — Prosedur penanganan komplain

- **Tujuan**: menguji akses knowledge pelayanan. Dipecah dua agar satu task hanya menguji satu hal.
- **T6a (find)**:
  - **Skenario**: "Pelanggan bilang kopinya terlalu pahit. Cari prosedurnya."
  - **Verifikasi**: "Sebutkan alurnya!" → **dengarkan – minta maaf – tawarkan remake/ganti menu – catat di log komplain**.
  - **Sukses**: menemukan dokumen **Prosedur Komplain Rasa** tanpa bantuan.
- **T6b (do, opsional bila waktu cukup)**:
  - **Skenario**: "Catat komplain tersebut di Log Komplain dengan status Diproses."
  - **Sukses**: entri muncul di riwayat komplain.

## T7 — Menambahkan/memperbarui knowledge (wajib terakhir)

- **Tujuan**: menguji proses kontribusi knowledge.
- **Skenario**: "Kamu menemukan takaran baru untuk Kopi Jahe. Ajukan sebagai pengetahuan baru."
- **Langkah**: Tulis Resep → isi judul + kategori **Resep & Takaran** + deskripsi → kirim.
- **Verifikasi**: "Status apa yang muncul pada dokumenmu?" → **menunggu_validasi** (tidak langsung terbit). Agar terbit: login pemilik (1111) → Validasi → Setujui.
- **Sukses**: dokumen terkirim dan muncul di antrean validasi pemilik.
- **Catat**: waktu pengisian form, field yang membingungkan.
- **Perhatian**:
  1. T7 mengotori data (dokumen + notifikasi baru) — jalankan paling terakhir dan reset via `seed.py` antar peserta.
  2. Tentukan peran di awal: karyawan (mengajukan → perlu validasi) atau pemilik. Hasilnya berbeda dan menjadi bahan analisis peran.
  3. "Menambah" dan "memperbarui (edit)" adalah dua alur berbeda — pilih satu per peserta agar waktu terkontrol.

## Kunci jawaban ringkas (untuk fasilitator)

| Task | Jawaban benar |
| --- | --- |
| T1 | Resep Espresso Standar |
| T2 | Gula aren cair 20ml, susu full cream 150ml |
| T3 | Backflush mesin, buang susu sisa, catat stok akhir, matikan listrik, kunci (min. 2) |
| T4 | Susu Segar Jaya / 0812-0002 (Sari) / Rp 22.000 — atau: kulkas 2–4°C, habiskan 3 hari |
| T5 | Tawarkan menu pengganti, catat di stok, hubungi supplier prioritas |
| T6a | Dengarkan, minta maaf, tawarkan remake/ganti menu, catat di log |
| T7 | Status menunggu_validasi → disetujui pemilik → terbit |
