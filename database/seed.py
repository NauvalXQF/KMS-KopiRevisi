"""Isi data demo: python database/seed.py"""
import sys
from datetime import datetime, timedelta
from pathlib import Path
from random import randint

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import (
    Bahan, Kategori, Komplain, Notifikasi, Pengguna, Pengetahuan,
    PengetahuanVersi, Penjualan, Stok, Supplier, SupplierBahan,
)


def reset():
    for m in [Notifikasi, Penjualan, Stok, SupplierBahan, Komplain,
              PengetahuanVersi, Pengetahuan, Bahan, Supplier, Kategori, Pengguna]:
        db.session.query(m).delete()
    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        reset()

        pemilik = Pengguna(nama="Pemilik", peran="pemilik",
                           pin_hash=generate_password_hash("1111"))
        karyawan = Pengguna(nama="Karyawan", peran="karyawan",
                            pin_hash=generate_password_hash("2222"))
        db.session.add_all([pemilik, karyawan])
        db.session.commit()

        kat = {}
        for nama, desc in [
            ("Resep & Takaran", "Resep minuman dan takaran bahan"),
            ("SOP", "Standar operasional buka/tutup toko"),
            ("Supplier & Bahan", "Info supplier, harga, penyimpanan"),
            ("Komplain", "Jenis komplain dan solusinya"),
            ("Data Penjualan", "Catatan dan analisis penjualan"),
        ]:
            k = Kategori(nama=nama, deskripsi=desc)
            db.session.add(k)
            db.session.commit()
            kat[nama] = k

        bahan_list = [
            ("Kopi Arabika", "gram", 1000, "Simpan di wadah kedap udara, suhu ruang, jauh dari cahaya."),
            ("Kopi Robusta", "gram", 1000, "Wadah kedap udara, suhu ruang."),
            ("Susu Full Cream", "ml", 2000, "Kulkas 2-4C, habiskan 3 hari setelah dibuka."),
            ("Gula Aren Cair", "ml", 1500, "Kulkas, tutup rapat, tahan 7 hari."),
            ("Es Batu", "gram", 3000, "Freezer -18C."),
            ("Cup 12oz", "pcs", 50, "Rak kering, jauh dari lembab."),
        ]
        bahan = {}
        for nama, satuan, minimum, simpan in bahan_list:
            b = Bahan(nama=nama, satuan=satuan, stok_minimum=minimum,
                      cara_penyimpanan=simpan)
            db.session.add(b)
            db.session.commit()
            bahan[nama] = b

        sup1 = Supplier(nama="Kopi Nusantara", kontak="0812-0001 (Budi)", alamat="Jl. Kopi No.1, Semarang", rating=5)
        sup2 = Supplier(nama="Susu Segar Jaya", kontak="0812-0002 (Sari)", alamat="Jl. Susu No.2, Semarang", rating=4)
        sup3 = Supplier(nama="KemasanKu", kontak="0812-0003 (Andi)", alamat="Jl. Kemasan No.3, Semarang", rating=4)
        db.session.add_all([sup1, sup2, sup3])
        db.session.commit()
        db.session.add_all([
            SupplierBahan(supplier_id=sup1.id, bahan_id=bahan["Kopi Arabika"].id, harga_terakhir=185000),
            SupplierBahan(supplier_id=sup1.id, bahan_id=bahan["Kopi Robusta"].id, harga_terakhir=120000),
            SupplierBahan(supplier_id=sup2.id, bahan_id=bahan["Susu Full Cream"].id, harga_terakhir=22000),
            SupplierBahan(supplier_id=sup2.id, bahan_id=bahan["Gula Aren Cair"].id, harga_terakhir=35000),
            SupplierBahan(supplier_id=sup3.id, bahan_id=bahan["Cup 12oz"].id, harga_terakhir=800),
        ])
        db.session.commit()

        # Stok: masuk besar, keluar sebagian; buat 1 bahan menipis
        for nama, masuk, keluar in [
            ("Kopi Arabika", 5000, 3500),
            ("Kopi Robusta", 5000, 2000),
            ("Susu Full Cream", 10000, 7500),
            ("Gula Aren Cair", 5000, 4200),   # sisa 800 < minimum 1500 -> menipis
            ("Es Batu", 20000, 12000),
            ("Cup 12oz", 500, 300),
        ]:
            db.session.add(Stok(bahan_id=bahan[nama].id, tipe="masuk", jumlah=masuk,
                                keterangan="Stok awal", dicatat_oleh=pemilik.id))
            db.session.add(Stok(bahan_id=bahan[nama].id, tipe="keluar", jumlah=keluar,
                                keterangan="Pemakaian", dicatat_oleh=karyawan.id))
        db.session.commit()

        pengetahuan_data = [
            ("Resep Kopi Susu Gula Aren", "Resep & Takaran",
             "Espresso 30ml + susu full cream 150ml + gula aren cair 20ml + es batu 100gr. "
             "Tuang susu dulu, lalu espresso agar layer cantik. Takaran untuk cup 12oz.", "terbit"),
            ("Resep Espresso Standar", "Resep & Takaran",
             "Dose 18gr, yield 36gr, waktu 25-30 detik, suhu 92C. Kalibrasi tiap pagi.", "terbit"),
            ("SOP Buka Toko", "SOP",
             "1. Nyalakan mesin 30 mnt sebelumnya 2. Kalibrasi espresso 3. Cek stok susu & es "
             "4. Bersihkan meja 5. Nyalakan kasir.", "terbit"),
            ("SOP Tutup Toko", "SOP",
             "1. Backflush mesin 2. Buang susu sisa 3. Catat stok akhir 4. Matikan listrik 5. Kunci.", "terbit"),
            ("Prosedur Komplain Rasa", "Komplain",
             "Dengarkan - minta maaf - tawarkan remake/ganti menu - catat di log komplain.", "terbit"),
            ("Prosedur Stok Habis", "SOP",
             "Jika bahan habis: tawarkan menu pengganti, catat di stok, hubungi supplier prioritas.", "terbit"),
            ("Daftar Supplier & Harga", "Supplier & Bahan",
             "Kopi Nusantara (Arabika 185rb/kg), Susu Segar Jaya (susu 22rb/L). Rating 4-5.", "terbit"),
            ("Racikan Baru: Kopi Jahe", "Resep & Takaran",
             "Usulan racikan kopi + jahe 10ml, masih uji coba.", "menunggu_validasi"),
            ("SOP Kebersihan Mesin", "SOP",
             "Draft awal, perlu dilengkapi takaran deterjen.", "revisi"),
        ]
        for judul, kategori, deskripsi, status in pengetahuan_data:
            p = Pengetahuan(judul=judul, kategori_id=kat[kategori].id, deskripsi=deskripsi,
                            status=status, versi=1, penulis_id=karyawan.id,
                            validator_id=pemilik.id if status == "terbit" else None,
                            catatan_validasi="Lengkapi detail" if status == "revisi" else None)
            db.session.add(p)
            db.session.commit()
            db.session.add(PengetahuanVersi(pengetahuan_id=p.id, versi=1, judul=judul,
                                            deskripsi=deskripsi, diubah_oleh=karyawan.id))
        db.session.commit()

        # Penjualan: 40 transaksi tersebar jam 08-21 untuk dashboard
        menus = [("Kopi Susu Gula Aren", 15000), ("Espresso", 12000),
                 ("Americano", 13000), ("Latte", 17000), ("Matcha Latte", 18000)]
        base = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        for i in range(40):
            nama, harga = menus[i % len(menus)]
            jam = randint(8, 21)
            waktu = base.replace(hour=jam, minute=randint(0, 59)) - timedelta(days=randint(0, 6))
            db.session.add(Penjualan(nama_menu=nama, jumlah=randint(1, 3),
                                     harga_satuan=harga, waktu=waktu,
                                     dicatat_oleh=karyawan.id))
        db.session.commit()

        db.session.add_all([
            Komplain(jenis="Rasa terlalu pahit", deskripsi="Pelanggan bilang kopi terlalu pahit.",
                     solusi="Remake dengan gula aren tambah 5ml", tindak_lanjut="Kalibrasi ulang grinder",
                     status="selesai", dicatat_oleh=karyawan.id),
            Komplain(jenis="Pelayanan lama", deskripsi="Antre 20 menit saat jam ramai.",
                     solusi="Minta maaf + gratis upgrade", tindak_lanjut="Tambah 1 barista shift sore",
                     status="diproses", dicatat_oleh=karyawan.id),
        ])
        db.session.commit()

        # Notifikasi contoh untuk pemilik (antrean validasi)
        menunggu = Pengetahuan.query.filter_by(status="menunggu_validasi").first()
        if menunggu:
            db.session.add(Notifikasi(pengguna_id=pemilik.id, judul="Pengetahuan menunggu validasi",
                                      pesan=f"'{menunggu.judul}' menunggu validasi.",
                                      terkait_tipe="pengetahuan", terkait_id=menunggu.id))
            db.session.commit()

        print("Seed selesai: PIN pemilik=1111, karyawan=2222")


if __name__ == "__main__":
    main()
