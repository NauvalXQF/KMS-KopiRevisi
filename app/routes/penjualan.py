from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from app import db
from app.models import Penjualan
from app.routes.helpers import get_current_user, login_required

bp = Blueprint("penjualan", __name__)


@bp.route("/penjualan")
@login_required
def daftar():
    items = Penjualan.query.order_by(Penjualan.waktu.desc()).limit(100).all()
    total_omzet = db.session.query(func.coalesce(func.sum(Penjualan.jumlah * Penjualan.harga_satuan), 0)).scalar()
    total_cup = db.session.query(func.coalesce(func.sum(Penjualan.jumlah), 0)).scalar()
    return render_template("penjualan.html", items=items, total_omzet=total_omzet, total_cup=total_cup)


@bp.route("/penjualan/tambah", methods=["POST"])
@login_required
def tambah():
    nama_menu = request.form.get("nama_menu", "").strip()
    try:
        jumlah = int(request.form.get("jumlah", 1))
        harga = float(request.form.get("harga_satuan", 0) or 0)
    except ValueError:
        flash("Jumlah/harga tidak valid.", "danger")
        return redirect(url_for("penjualan.daftar"))
    if not nama_menu or jumlah <= 0:
        flash("Nama menu dan jumlah wajib diisi.", "danger")
        return redirect(url_for("penjualan.daftar"))
    user = get_current_user()
    db.session.add(Penjualan(nama_menu=nama_menu, jumlah=jumlah, harga_satuan=harga,
                             waktu=datetime.now(timezone.utc), dicatat_oleh=user.id))
    db.session.commit()
    flash("Penjualan dicatat.", "success")
    return redirect(url_for("penjualan.daftar"))
