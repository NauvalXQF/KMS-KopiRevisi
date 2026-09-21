-- Skema database KMS Kopi Revisi (MySQL 8 / MariaDB 10.5+)
-- Jalankan: mysql -u root -p kms_kopi < database/schema.sql
CREATE DATABASE IF NOT EXISTS kms_kopi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kms_kopi;

-- 1. Pengguna
CREATE TABLE IF NOT EXISTS pengguna (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(100) NOT NULL,
  peran ENUM('pemilik','karyawan') NOT NULL DEFAULT 'karyawan',
  pin_hash VARCHAR(255) NOT NULL,
  aktif BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Kategori
CREATE TABLE IF NOT EXISTS kategori (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(100) NOT NULL UNIQUE,
  deskripsi TEXT
) ENGINE=InnoDB;

-- 3. Pengetahuan
CREATE TABLE IF NOT EXISTS pengetahuan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  judul VARCHAR(200) NOT NULL,
  kategori_id INT,
  deskripsi TEXT NOT NULL,
  lampiran VARCHAR(255),
  status ENUM('menunggu_validasi','revisi','disetujui','terbit') NOT NULL DEFAULT 'menunggu_validasi',
  versi INT DEFAULT 1,
  penulis_id INT,
  validator_id INT,
  catatan_validasi TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (kategori_id) REFERENCES kategori(id) ON DELETE SET NULL,
  FOREIGN KEY (penulis_id) REFERENCES pengguna(id) ON DELETE SET NULL,
  FOREIGN KEY (validator_id) REFERENCES pengguna(id) ON DELETE SET NULL,
  FULLTEXT KEY ft_pengetahuan (judul, deskripsi)
) ENGINE=InnoDB;

-- 4. Riwayat versi pengetahuan
CREATE TABLE IF NOT EXISTS pengetahuan_versi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pengetahuan_id INT NOT NULL,
  versi INT NOT NULL,
  judul VARCHAR(200) NOT NULL,
  deskripsi TEXT NOT NULL,
  diubah_oleh INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (pengetahuan_id) REFERENCES pengetahuan(id) ON DELETE CASCADE,
  FOREIGN KEY (diubah_oleh) REFERENCES pengguna(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 5. Bahan
CREATE TABLE IF NOT EXISTS bahan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(100) NOT NULL UNIQUE,
  satuan VARCHAR(20) DEFAULT 'gram',
  stok_minimum FLOAT DEFAULT 0,
  cara_penyimpanan TEXT
) ENGINE=InnoDB;

-- 6. Supplier
CREATE TABLE IF NOT EXISTS supplier (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(100) NOT NULL,
  kontak VARCHAR(100),
  alamat TEXT,
  rating INT DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS supplier_bahan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_id INT NOT NULL,
  bahan_id INT NOT NULL,
  harga_terakhir DECIMAL(12,2) DEFAULT 0,
  FOREIGN KEY (supplier_id) REFERENCES supplier(id) ON DELETE CASCADE,
  FOREIGN KEY (bahan_id) REFERENCES bahan(id) ON DELETE CASCADE,
  UNIQUE KEY uq_supplier_bahan (supplier_id, bahan_id)
) ENGINE=InnoDB;

-- 7. Stok (mutasi masuk/keluar)
CREATE TABLE IF NOT EXISTS stok (
  id INT AUTO_INCREMENT PRIMARY KEY,
  bahan_id INT NOT NULL,
  tipe ENUM('masuk','keluar') NOT NULL,
  jumlah FLOAT NOT NULL,
  tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
  keterangan TEXT,
  dicatat_oleh INT,
  FOREIGN KEY (bahan_id) REFERENCES bahan(id) ON DELETE CASCADE,
  FOREIGN KEY (dicatat_oleh) REFERENCES pengguna(id) ON DELETE SET NULL,
  INDEX idx_stok_bahan (bahan_id),
  INDEX idx_stok_tanggal (tanggal)
) ENGINE=InnoDB;

-- 8. Penjualan
CREATE TABLE IF NOT EXISTS penjualan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama_menu VARCHAR(100) NOT NULL,
  jumlah INT NOT NULL DEFAULT 1,
  harga_satuan DECIMAL(12,2) DEFAULT 0,
  waktu DATETIME DEFAULT CURRENT_TIMESTAMP,
  dicatat_oleh INT,
  FOREIGN KEY (dicatat_oleh) REFERENCES pengguna(id) ON DELETE SET NULL,
  INDEX idx_penjualan_waktu (waktu),
  INDEX idx_penjualan_menu (nama_menu)
) ENGINE=InnoDB;

-- 9. Komplain
CREATE TABLE IF NOT EXISTS komplain (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
  jenis VARCHAR(100) NOT NULL,
  deskripsi TEXT NOT NULL,
  solusi TEXT,
  tindak_lanjut TEXT,
  status ENUM('baru','diproses','selesai') NOT NULL DEFAULT 'baru',
  dicatat_oleh INT,
  FOREIGN KEY (dicatat_oleh) REFERENCES pengguna(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 10. Notifikasi
CREATE TABLE IF NOT EXISTS notifikasi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pengguna_id INT NOT NULL,
  judul VARCHAR(200) NOT NULL,
  pesan TEXT,
  dibaca BOOLEAN DEFAULT FALSE,
  terkait_tipe VARCHAR(50),
  terkait_id INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (pengguna_id) REFERENCES pengguna(id) ON DELETE CASCADE,
  INDEX idx_notif_user (pengguna_id, dibaca)
) ENGINE=InnoDB;

-- View: stok menipis (sisa <= stok_minimum)
DROP VIEW IF EXISTS v_stok_menipis;
CREATE VIEW v_stok_menipis AS
SELECT b.id, b.nama, b.satuan, b.stok_minimum,
  COALESCE(SUM(CASE WHEN s.tipe='masuk' THEN s.jumlah WHEN s.tipe='keluar' THEN -s.jumlah ELSE 0 END),0) AS sisa
FROM bahan b LEFT JOIN stok s ON s.bahan_id = b.id
GROUP BY b.id, b.nama, b.satuan, b.stok_minimum
HAVING sisa <= b.stok_minimum;

-- View: jam ramai
DROP VIEW IF EXISTS v_jam_ramai;
CREATE VIEW v_jam_ramai AS
SELECT HOUR(waktu) AS jam, SUM(jumlah) AS total_cup, COUNT(*) AS transaksi
FROM penjualan GROUP BY HOUR(waktu) ORDER BY total_cup DESC;

-- View: menu laris
DROP VIEW IF EXISTS v_menu_laris;
CREATE VIEW v_menu_laris AS
SELECT nama_menu, SUM(jumlah) AS total_terjual, SUM(jumlah*harga_satuan) AS omzet
FROM penjualan GROUP BY nama_menu ORDER BY total_terjual DESC;
