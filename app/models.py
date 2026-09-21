"""Models KMS Kopi Revisi."""
from datetime import datetime

from app import db


class Pengguna(db.Model):
    __tablename__ = "pengguna"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    peran = db.Column(db.Enum("pemilik", "karyawan"), nullable=False, default="karyawan")
    pin_hash = db.Column(db.String(255), nullable=False)
    aktif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Kategori(db.Model):
    __tablename__ = "kategori"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False, unique=True)
    deskripsi = db.Column(db.Text)


class Pengetahuan(db.Model):
    __tablename__ = "pengetahuan"
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    deskripsi = db.Column(db.Text, nullable=False)
    lampiran = db.Column(db.String(255))  # path file di static/uploads
    status = db.Column(
        db.Enum("menunggu_validasi", "revisi", "disetujui", "terbit"),
        default="menunggu_validasi",
        nullable=False,
    )
    versi = db.Column(db.Integer, default=1)
    penulis_id = db.Column(db.Integer, db.ForeignKey("pengguna.id"))
    validator_id = db.Column(db.Integer, db.ForeignKey("pengguna.id"))
    catatan_validasi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kategori = db.relationship("Kategori", backref="pengetahuan")
    penulis = db.relationship("Pengguna", foreign_keys=[penulis_id])
    validator = db.relationship("Pengguna", foreign_keys=[validator_id])


class PengetahuanVersi(db.Model):
    __tablename__ = "pengetahuan_versi"
    id = db.Column(db.Integer, primary_key=True)
    pengetahuan_id = db.Column(db.Integer, db.ForeignKey("pengetahuan.id"), nullable=False)
    versi = db.Column(db.Integer, nullable=False)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    diubah_oleh = db.Column(db.Integer, db.ForeignKey("pengguna.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Bahan(db.Model):
    __tablename__ = "bahan"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False, unique=True)
    satuan = db.Column(db.String(20), default="gram")
    stok_minimum = db.Column(db.Float, default=0)
    cara_penyimpanan = db.Column(db.Text)


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    rating = db.Column(db.Integer, default=0)  # 1-5


class SupplierBahan(db.Model):
    __tablename__ = "supplier_bahan"
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"), nullable=False)
    bahan_id = db.Column(db.Integer, db.ForeignKey("bahan.id"), nullable=False)
    harga_terakhir = db.Column(db.Numeric(12, 2), default=0)

    supplier = db.relationship("Supplier", backref="daftar_bahan")
    bahan = db.relationship("Bahan", backref="daftar_supplier")


class Stok(db.Model):
    __tablename__ = "stok"
    id = db.Column(db.Integer, primary_key=True)
    bahan_id = db.Column(db.Integer, db.ForeignKey("bahan.id"), nullable=False)
    tipe = db.Column(db.Enum("masuk", "keluar"), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    keterangan = db.Column(db.Text)
    dicatat_oleh = db.Column(db.Integer, db.ForeignKey("pengguna.id"))

    bahan = db.relationship("Bahan", backref="mutasi")


class Penjualan(db.Model):
    __tablename__ = "penjualan"
    id = db.Column(db.Integer, primary_key=True)
    nama_menu = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False, default=1)
    harga_satuan = db.Column(db.Numeric(12, 2), default=0)
    waktu = db.Column(db.DateTime, default=datetime.utcnow)
    dicatat_oleh = db.Column(db.Integer, db.ForeignKey("pengguna.id"))


class Komplain(db.Model):
    __tablename__ = "komplain"
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    jenis = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    solusi = db.Column(db.Text)
    tindak_lanjut = db.Column(db.Text)
    status = db.Column(
        db.Enum("baru", "diproses", "selesai"), default="baru", nullable=False
    )
    dicatat_oleh = db.Column(db.Integer, db.ForeignKey("pengguna.id"))


class Notifikasi(db.Model):
    __tablename__ = "notifikasi"
    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer, db.ForeignKey("pengguna.id"), nullable=False)
    judul = db.Column(db.String(200), nullable=False)
    pesan = db.Column(db.Text)
    dibaca = db.Column(db.Boolean, default=False)
    terkait_tipe = db.Column(db.String(50))  # mis. 'pengetahuan'
    terkait_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
