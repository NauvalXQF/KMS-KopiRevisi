# Requirements — KMS Kopi Revisi (Prototipe Web)

Dokumen kebutuhan dan fitur **Knowledge Management System (KMS)** untuk UMKM kedai kopi.
Bahasa: Indonesia. Status mengacu pada kondisi kode saat dokumen ini ditulis.

## 1. Pendahuluan

Aplikasi membantu pemilik dan karyawan menyimpan, mencari, membagikan, dan memakai
kembali pengetahuan operasional (resep, SOP, supplier, komplain) serta mencatat
stok dan penjualan. Dibangun dengan Flask + SQLAlchemy (MySQL, fallback SQLite),
frontend HTML/CSS/JS + Bootstrap.

### 1.1 Peran pengguna

| Peran | Akses |
| --- | --- |
| Pemilik (PIN `1111`) | Semua fitur, validasi pengetahuan, kelola pengguna, kelola menu & harga, hapus transaksi, export Excel |
| Karyawan (PIN `2222`) | Cari & baca pengetahuan, input pengetahuan baru (perlu validasi), catat stok/penjualan/komplain |

### 1.2 Glosarium

- **Resep**: dokumen pengetahuan kategori Resep & Takaran (dulu berlabel "Pengetahuan").
- **Terbit**: status dokumen yang sudah disetujui dan terlihat semua pengguna.
- **Antrean validasi**: dokumen berstatus `menunggu_validasi` / `revisi` menunggu keputusan pemilik.

## 2. Kebutuhan Fungsional

Format tiap item: kebutuhan → fitur implementasi (acuan file) → status → trace task uji.

### KF-01 Autentikasi PIN

- **Kebutuhan**: hanya staf terdaftar yang bisa masuk, dibedakan per peran.
- **Fitur**:
  - Login PIN dengan hash (`app/routes/auth.py:login`).
  - Rate-limit: 5x gagal diblokir 60 detik, pesan error generik.
  - Registrasi akun oleh pemilik, PIN wajib 4–6 digit angka (`auth.py:tambah`).
  - Nonaktifkan/aktifkan akun (`auth.py:toggle`).
- **Status**: ✅ Sudah ada.
- **Trace**: prasyarat semua task (login sebagai karyawan/pemilik).

### KF-02 Daftar Resep & Pencarian (Pustaka)

- **Kebutuhan**: menemukan resep/SOP/supplier/komplain dengan cepat (T1, T3, T4, T5, T6a).
- **Fitur**:
  - Pencarian kata kunci judul + deskripsi (`pengetahuan.py:daftar`).
  - Filter kategori via dropdown + chip (`pengetahuan_list.html`).
  - Paginasi 12/halaman + navigasi halaman.
  - Karyawan hanya melihat dokumen `terbit` + miliknya sendiri; pemilik melihat semua.
- **Status**: ✅ Sudah ada.
- **Trace**: T1, T3, T4, T5, T6a.

### KF-03 Detail Resep & Takaran (T2)

- **Kebutuhan**: membuka satu dokumen dan membaca takaran bahan secara lengkap.
- **Fitur**:
  - Halaman detail: judul, kategori, status, versi, penulis, waktu update (`pengetahuan_detail.html`).
  - Isi deskripsi (memuat takaran, mis. "gula aren cair 20ml").
  - Lampiran foto/video/PDF, riwayat versi, tombol cetak (print CSS), breadcrumb + kembali.
- **Status**: ✅ Sudah ada. Catatan: takaran masih teks bebas di deskripsi, belum field terstruktur (rencana ke depan).
- **Trace**: T2.

### KF-04 Kontribusi & Revisi Knowledge (T7)

- **Kebutuhan**: karyawan bisa menambah/memperbarui knowledge; pemilik mengendalikan mutu via validasi.
- **Fitur**:
  - Form pengetahuan baru + upload lampiran (`pengetahuan.py:baru`, `helpers.py:save_upload`).
  - Edit menaikkan versi + menyimpan `pengetahuan_versi`; edit karyawan mengembalikan ke antrean.
  - Validasi pemilik: setujui→terbit / kembalikan revisi + catatan (`validasi.py`, `validasi.html`).
  - Notifikasi otomatis ke pemilik (pengajuan) dan penulis (keputusan).
- **Status**: ✅ Sudah ada.
- **Trace**: T7.

### KF-05 Penjualan: filter periode (cashflow)

- **Kebutuhan**: pemilik melihat omzet/cup per hari atau per bulan.
- **Fitur**:
  - Filter `mode=harian|bulanan|semua` + input tanggal/bulan + chip cepat (`penjualan.py:_parse_periode`, `penjualan.html` filter-bar).
  - Kartu statistik konteks periode: cup, omzet, jumlah transaksi + label periode.
  - Waktu transaksi disimpan jam lokal (naive) agar cocok dengan filter.
- **Status**: ✅ Sudah ada.
- **Trace**: diuji manual (di luar paket T1–T7).

### KF-06 Penjualan: master menu anti-salah-input

- **Kebutuhan**: kasir tidak salah ketik nama/harga menu.
- **Fitur**:
  - Tabel `menu` + CRUD khusus pemilik (`app/routes/menu.py`, kartu Kelola Menu di `penjualan.html`).
  - Form kasir berupa dropdown menu aktif; harga auto-fill readonly dan **dikunci dari master** di backend (`penjualan.py:tambah`).
  - Seed berisi 5 menu: Kopi Susu Gula Aren, Espresso, Americano, Latte, Matcha Latte.
- **Status**: ✅ Sudah ada.
- **Trace**: diuji manual (di luar paket T1–T7).

### KF-07 Penjualan: export Excel & hapus owner-only

- **Kebutuhan**: rekap mudah dibawa (Excel) dan koreksi salah input terkendali.
- **Fitur**:
  - Export `.xlsx` mengikuti filter aktif, maks 5000 baris, header + baris total (`penjualan.py:export`, dep `openpyxl`).
  - Hapus transaksi permanen khusus pemilik (`POST /penjualan/<id>/hapus`, `pemilik_only`); tombol hanya tampil untuk pemilik. Kasir yang salah input wajib koordinasi ke pemilik.
- **Status**: ✅ Sudah ada.
- **Trace**: diuji manual (di luar paket T1–T7).

### KF-08 Stok bahan

- **Kebutuhan**: pantau ketersediaan dan catat mutasi harian + peringatan menipis.
- **Fitur**:
  - Ringkasan sisa per bahan + badge Menipis/Aman, filter chip client-side (`stok.py`, `stok.html`, `app.js`).
  - Form mutasi masuk/keluar + daftar bahan baru (nama unik, satuan, minimum, cara penyimpanan).
  - Riwayat 30 mutasi terakhir.
- **Status**: ✅ Sudah ada.
- **Trace**: pendukung T4 (jalur Stok) dan T5.

### KF-09 Supplier & bahan

- **Kebutuhan**: data rekanan, kontak, rating, harga terakhir (T4).
- **Fitur**:
  - Kartu supplier + badge rating + bahan yang disuplai + harga (`supplier.html`).
  - Tambah supplier (rating 0–5) dan hubungkan bahan–harga (`supplier.py`).
- **Status**: ✅ Sudah ada.
- **Trace**: T4 (jalur Supplier).

### KF-10 Komplain, notifikasi, pengguna, dashboard

- **Kebutuhan**: catat & tindaklanjuti komplain (T6b), info status (notifikasi), kelola akun, ringkasan operasional.
- **Fitur**:
  - Komplain: tambah + update solusi/tindak lanjut/status, limit 100 (`komplain.py`, `komplain.html`).
  - Notifikasi: daftar per pengguna, tandai dibaca/semuanya, badge belum dibaca di navbar (limit 50).
  - Pengguna: tabel akun + tambah + ubah status (pemilik saja).
  - Dashboard: menu terlaris, jam ramai, peringatan stok, antrean validasi (`dashboard.py`, `dashboard.html`).
- **Status**: ✅ Sudah ada.
- **Trace**: T6a/T6b (komplain), T7 (notifikasi validasi).

## 3. Kebutuhan Non-Fungsional

| Kode | Kebutuhan | Status |
| --- | --- | --- |
| KNF-01 | UI minimalis–modern–profesional: satu design system (Plus Jakarta Sans, token coffee/caramel, radius, badge-soft), tanpa shadow berlebih | ✅ Diterapkan di `style.css` + unifikasi 3 halaman (komplain/notifikasi/pengguna) |
| KNF-02 | PIN di-hash, pesan login generik, rate-limit, `SECRET_KEY` dari `.env` (warning bila kosong), debug mati default | ✅ Diterapkan |
| KNF-03 | Berjalan lokal tanpa MySQL (fallback SQLite) untuk demo | ✅ `_build_db_uri()` di `app/__init__.py` |
| KNF-04 | Cetak SOP/resep rapi (print CSS) | ✅ `style.css` media print |
| KNF-05 | Upload dibatasi 16MB, format png/jpg/gif/mp4/mov/pdf, format tak didukung memunculkan peringatan | ✅ `helpers.py:save_upload` |

## 4. Matriks Traceability

| Kebutuhan | Fitur utama | Task uji | Status |
| --- | --- | --- | --- |
| KF-02 | Pencarian + filter kategori | T1, T3, T4, T5, T6a | ✅ |
| KF-03 | Detail + takaran | T2 | ✅ |
| KF-04 | Kontribusi + validasi | T7 | ✅ |
| KF-09 | Supplier & harga | T4 | ✅ |
| KF-08 | Stok & cara penyimpanan | T4 alt, T5 | ✅ |
| KF-10 | Log komplain | T6b | ✅ |
| KF-05/06/07 | Filter, master menu, export, hapus | manual | ✅ |
| KF-01, KNF-01…05 | Auth, UI, keamanan | prasyarat/setup | ✅ |

## 5. Rencana ke Depan (belum ada)

1. Field takaran terstruktur (bahan–jumlah–satuan) agar resep bisa difilter per bahan.
2. Jejak audit untuk transaksi yang dihapus (saat ini hapus permanen tanpa log).
3. Proteksi CSRF pada form dan pembatasan upload per peran.
