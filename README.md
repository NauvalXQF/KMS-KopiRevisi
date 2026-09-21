# KMS Kopi Revisi — Prototipe Web

Prototipe web **Knowledge Management System (KMS)** untuk UMKM kedai kopi. Aplikasi ini membantu pemilik dan karyawan **menyimpan, mencari, membagikan, dan memakai kembali** pengetahuan operasional (resep, SOP, supplier, komplain) serta mencatat stok dan penjualan.

> Prototipe untuk keperluan akademik (Tugas Kelompok Sistem Informasi 2026, Departemen Informatika, Universitas Diponegoro).

## Fitur

**Pengetahuan**
- Pustaka pengetahuan per kategori: Resep & Takaran, SOP, Supplier & Bahan, Komplain, Data Penjualan
- Pencarian kata kunci dan filter kategori
- Input pengetahuan baru (judul, kategori, deskripsi, lampiran foto/video)
- Alur validasi pemilik: menunggu validasi → disetujui / revisi → terbit
- Versi pengetahuan dan notifikasi status

**Operasional**
- Stok bahan: catat masuk/keluar, peringatan stok menipis
- Supplier & bahan: kontak, harga terakhir, rating, cara penyimpanan
- Penjualan per menu
- Log komplain: jenis, solusi, penindaklanjut

**Dashboard**
- Menu terlaris, jam ramai, bahan stok menipis, antrean validasi

## Peran Pengguna

| Peran | Akses |
| --- | --- |
| Pemilik | Semua fitur, validasi pengetahuan, kelola pengguna |
| Karyawan | Cari & baca pengetahuan, input pengetahuan baru (perlu validasi), catat stok/penjualan/komplain |

Login menggunakan PIN (disimpan dalam bentuk hash).

## Halaman

| Rute | Halaman |
| --- | --- |
| `/login` | Login PIN |
| `/` | Dashboard |
| `/pengetahuan` | Pustaka pengetahuan (kategori + pencarian) |
| `/pengetahuan/<id>` | Detail pengetahuan |
| `/pengetahuan/baru` | Form pengetahuan baru |
| `/validasi` | Antrean validasi (pemilik) |
| `/stok` | Stok bahan |
| `/supplier` | Supplier & bahan |
| `/penjualan` | Penjualan |
| `/komplain` | Komplain |
| `/notifikasi` | Notifikasi |

## Tech Stack

| Bagian | Teknologi |
| --- | --- |
| Backend | Python 3.10+, Flask, Flask-SQLAlchemy |
| Database | MySQL 8 (atau MariaDB 10.5+) |
| Driver | PyMySQL |
| Frontend | HTML, CSS, JavaScript |
| Desain UI | Figma |

## Struktur Folder

```
kms-kopi-revisi/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   └── static/
├── database/
│   ├── schema.sql        # tabel + view
│   └── seed.py           # data demo
├── .env.example
├── requirements.txt
├── run.py
└── README.md
```

## Struktur Database

Tabel: `pengguna`, `kategori`, `pengetahuan`, `bahan`, `supplier`, `stok`, `penjualan`, `komplain`
View: `v_stok_menipis`, `v_jam_ramai`, `v_menu_laris`

## Instalasi

**Prasyarat:** Python 3.10+, MySQL 8 (atau MariaDB), `pip`.

```bash
# 1. Clone repositori
git clone <url-repositori>
cd kms-kopi-revisi

# 2. Virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Dependensi
pip install -r requirements.txt

# 4. Buat database
mysql -u root -p -e "CREATE DATABASE kms_kopi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 5. Konfigurasi environment
cp .env.example .env
# lalu edit .env sesuai kredensial MySQL kamu

# 6. Buat tabel & view
mysql -u root -p kms_kopi < database/schema.sql

# 7. Isi data demo
python database/seed.py

# 8. Jalankan
python run.py
```

Buka `http://localhost:5000`.

### Contoh `.env`

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=isi_password_kamu
DB_NAME=kms_kopi
SECRET_KEY=ganti-dengan-string-acak
```

## Akun Demo

| Peran | PIN |
| --- | --- |
| Pemilik | `1111` |
| Karyawan | `2222` |

> PIN ini hanya untuk demo. Ganti sebelum dipakai di lingkungan sebenarnya.

Data demo berisi contoh resep dan takaran, SOP buka/tutup toko, prosedur komplain dan stok habis, data bahan dan supplier, serta riwayat penjualan untuk dashboard.

## Catatan

- Prototipe belum ditujukan untuk produksi penuh; tambahkan HTTPS, backup database, dan pembatasan percobaan login sebelum dipakai sungguhan.
- Belum ada integrasi dengan mesin kasir/POS.
