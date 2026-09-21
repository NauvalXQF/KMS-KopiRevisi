from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Bahan, Supplier, SupplierBahan
from app.routes.helpers import login_required

bp = Blueprint("supplier", __name__)


@bp.route("/supplier")
@login_required
def daftar():
    suppliers = Supplier.query.order_by(Supplier.nama).all()
    bahans = Bahan.query.order_by(Bahan.nama).all()
    relasi = SupplierBahan.query.all()
    return render_template("supplier.html", suppliers=suppliers, bahans=bahans, relasi=relasi)


@bp.route("/supplier/tambah", methods=["POST"])
@login_required
def tambah():
    nama = request.form.get("nama", "").strip()
    if not nama:
        flash("Nama supplier wajib diisi.", "danger")
        return redirect(url_for("supplier.daftar"))
    try:
        rating = int(request.form.get("rating", 0) or 0)
    except ValueError:
        rating = 0
    db.session.add(Supplier(nama=nama, kontak=request.form.get("kontak", "").strip(),
                            alamat=request.form.get("alamat", "").strip(),
                            rating=max(0, min(5, rating))))
    db.session.commit()
    flash("Supplier ditambahkan.", "success")
    return redirect(url_for("supplier.daftar"))


@bp.route("/supplier/hubungkan", methods=["POST"])
@login_required
def hubungkan():
    try:
        supplier_id = int(request.form.get("supplier_id", 0))
        bahan_id = int(request.form.get("bahan_id", 0))
        harga = float(request.form.get("harga_terakhir", 0) or 0)
    except ValueError:
        flash("Input tidak valid.", "danger")
        return redirect(url_for("supplier.daftar"))
    existing = SupplierBahan.query.filter_by(supplier_id=supplier_id, bahan_id=bahan_id).first()
    if existing:
        existing.harga_terakhir = harga
    else:
        db.session.add(SupplierBahan(supplier_id=supplier_id, bahan_id=bahan_id,
                                     harga_terakhir=harga))
    db.session.commit()
    flash("Relasi supplier-bahan disimpan.", "success")
    return redirect(url_for("supplier.daftar"))
