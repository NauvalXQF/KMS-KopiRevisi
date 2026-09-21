# Changelog — KMS Kopi Revisi

## Cara mencatat perubahan berikutnya (aturan)

1. Tambahkan entri baru di paling atas bagian "Sesi pengembangan", format: tanggal – ringkasan – file terdampak.
2. Gunakan kategori: **Ditambah** / **Diubah** / **Diperbaiki** / **Catatan**.
3. Setiap klaim "terverifikasi" wajib menyebut hasil ujinya (mis. "8 halaman return 200").

## Sesi pengembangan (detail, terverifikasi lokal)

### 2026-09-21 — Resep baru + dokumen (sesi ini)

- **Ditambah**: 3 resep standar (Americano, Latte, Matcha Latte, id 10–12) di `database/seed.py` dan DB aktif `kms_kopi.db` + riwayat versi-1. Cakupan resep ↔ menu kini 5/5.
- **Ditambah**: `requirements.md`, `task.md`, `changelog.md` (dokumen ini).
- **Catatan**: `database/seed.py` masih uncommitted saat dokumen ditulis — commit bersamaan dengan ketiga file dokumen ini.

### 2026-09-21 — Fitur penjualan 4-in-1 + fix waktu lokal

- **Ditambah**: filter periode harian/bulanan/semua + statistik konteks periode (`app/routes/penjualan.py:_parse_periode`, `penjualan.html` filter-bar).
- **Ditambah**: master Menu + CRUD pemilik (`app/models.py:Menu`, `app/routes/menu.py` baru); form kasir jadi dropdown dengan harga dikunci dari master; seed 5 menu.
- **Ditambah**: export Excel `.xlsx` mengikuti filter (`GET /penjualan/export`, dep `openpyxl` di `requirements.txt`).
- **Ditambah**: hapus transaksi permanen khusus pemilik (`POST /penjualan/<id>/hapus`), kolom Subtotal + Aksi di riwayat.
- **Diperbaiki**: waktu transaksi UTC → jam lokal agar cocok dengan filter harian (transaksi 00–07 WIB sebelumnya "hilang" dari filter).
- **Terverifikasi**: filter 3 mode 200 OK, export `.xlsx` valid, tambah via master OK, hapus owner OK + kasir ditolak (302), kelola menu owner OK + kasir ditolak.

### 2026-09-21 — Rename + UI + hardening

- **Diubah**: label "Pengetahuan" → "Resep", "Pustaka Pengetahuan" → "Daftar Resep" (judul/navigasi saja; URL `/pengetahuan`, model, dan tabel tidak diubah).
- **Diubah**: unifikasi `komplain.html`, `notifikasi.html`, `pengguna.html` ke pola `page-title` + `badge-soft-*` + `btn-dark`; hapus `shadow-sm` berlebih; satukan gradient progress dashboard ke caramel; JS inline dipindah ke `app/static/app.js`.
- **Diperbaiki**: token CSS hilang (`--bg-surface-secondary`), typo `--border-strong`, kontras `--text-light`.
- **Diubah (backend)**: `debug` via `FLASK_DEBUG`, warning `SECRET_KEY` kosong, `datetime.utcnow` → `_now()` sadar zona, paginasi Daftar Resep 12/halaman, limit komplain 100, flash saat format upload ditolak, rate-limit login 5x/60 detik + pesan generik + validasi PIN 4–6 digit.
- **Terverifikasi**: compile OK, 8 halaman return 200, login 1111/2222 OK, pagination OK, URL lama tidak rusak.

## Riwayat awal (rekonstruksi dari git log)

> Catatan jujur: pesan commit asal singkat, deskripsi di bawah ditulis ulang dari kondisi kode saat ini.

- `ca41749` — feat: Prototype KMS Kopi Revisi. Fondasi awal: Flask factory + blueprint, model, template, seed demo, README.
- `a98503d` — chore: ignore `.env` dan sqlite db (`.gitignore`).
- `fad54a8` — Memperbarui UI/UX pada prototype. Iterasi awal design system coffee/caramel.
- `1e1c16b` — revisi UI/UX. Penyempurnaan tampilan lanjutan.
- `5eeb511` — REVISI LAGI. Revisi lanjutan (tidak terdokumentasi rinci).
- `17245f0` — benerin auth login. Perbaikan alur login PIN.
- `f8dd4ed` — nambahin perbaikan UI/UX dan grammar. Polish tampilan + bahasa.
- `cbf8cd7` — nambah fitur. Penambahan fitur (mencakup kondisi sebelum sesi rename di atas).
