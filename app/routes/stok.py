from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from app import db
from app.models import Bahan, Stok
from app.routes.helpers import get_current_user, login_required

bp = Blueprint("stok", __name__)


def _ringkasan():
    rows = (
        db.session.query(
            Bahan,
            func.coalesce(func.sum(
                db.case((Stok.tipe == "masuk", Stok.jumlah),
                        (Stok.tipe == "keluar", -Stok.jumlah), else_=0)), 0).label("sisa"),
        ).outerjoin(Stok, Stok.bahan_id == Bahan.id)
        .group_by(Bahan.id).order_by(Bahan.nama).all()
    )
    return rows


@bp.route("/stok")
@login_required
def daftar():
    ringkasan = _ringkasan()
    mutasi = Stok.query.order_by(Stok.tanggal.desc()).limit(30).all()
    return render_template("stok.html", ringkasan=ringkasan, mutasi=mutasi)


@bp.route("/stok/catat", methods=["POST"])
@login_required
def catat():
    bahan_id = request.form.get("bahan_id")
    tipe = request.form.get("tipe")
    try:
        jumlah = float(request.form.get("jumlah", 0))
    except ValueError:
        jumlah = 0
    keterangan = request.form.get("keterangan", "").strip()
    if not bahan_id or tipe not in ("masuk", "keluar") or jumlah <= 0:
        flash("Bahan, tipe, dan jumlah valid wajib diisi.", "danger")
        return redirect(url_for("stok.daftar"))
    user = get_current_user()
    db.session.add(Stok(bahan_id=int(bahan_id), tipe=tipe, jumlah=jumlah,
                        keterangan=keterangan, dicatat_oleh=user.id))
    db.session.commit()
    flash("Mutasi stok dicatat.", "success")
    return redirect(url_for("stok.daftar"))


@bp.route("/stok/bahan/tambah", methods=["POST"])
@login_required
def tambah_bahan():
    nama = request.form.get("nama", "").strip()
    satuan = request.form.get("satuan", "gram").strip() or "gram"
    try:
        minimum = float(request.form.get("stok_minimum", 0) or 0)
    except ValueError:
        minimum = 0
    simpan = request.form.get("cara_penyimpanan", "").strip()
    if not nama:
        flash("Nama bahan wajib diisi.", "danger")
        return redirect(url_for("stok.daftar"))
    if Bahan.query.filter_by(nama=nama).first():
        flash("Bahan sudah ada.", "warning")
        return redirect(url_for("stok.daftar"))
    db.session.add(Bahan(nama=nama, satuan=satuan, stok_minimum=minimum,
                         cara_penyimpanan=simpan))
    db.session.commit()
    flash("Bahan ditambahkan.", "success")
    return redirect(url_for("stok.daftar"))
