from flask import Blueprint, flash, redirect, request, url_for
from sqlalchemy import func

from app import db
from app.models import Menu
from app.routes.helpers import login_required, pemilik_only

bp = Blueprint("menu", __name__)


def _to_harga(raw, default=0.0):
    try:
        return max(0.0, float(raw or default))
    except (TypeError, ValueError):
        return default


@bp.route("/menu/tambah", methods=["POST"])
@login_required
@pemilik_only
def tambah():
    nama = request.form.get("nama", "").strip()
    harga = _to_harga(request.form.get("harga_default", 0))
    if not nama:
        flash("Nama menu wajib diisi.", "danger")
        return redirect(url_for("penjualan.daftar"))
    duplikat = Menu.query.filter(func.lower(Menu.nama) == nama.lower()).first()
    if duplikat:
        flash(f"Menu '{duplikat.nama}' sudah ada.", "warning")
        return redirect(url_for("penjualan.daftar"))
    db.session.add(Menu(nama=nama, harga_default=harga, aktif=True))
    db.session.commit()
    flash(f"Menu '{nama}' ditambahkan.", "success")
    return redirect(url_for("penjualan.daftar"))


@bp.route("/menu/<int:mid>/update", methods=["POST"])
@login_required
@pemilik_only
def update(mid):
    m = Menu.query.get_or_404(mid)
    nama = request.form.get("nama", "").strip()
    harga = _to_harga(request.form.get("harga_default", m.harga_default))
    if nama:
        duplikat = Menu.query.filter(
            func.lower(Menu.nama) == nama.lower(), Menu.id != m.id
        ).first()
        if duplikat:
            flash(f"Nama '{nama}' sudah dipakai menu lain.", "danger")
            return redirect(url_for("penjualan.daftar"))
        m.nama = nama
    m.harga_default = harga
    db.session.commit()
    flash(f"Menu '{m.nama}' diperbarui.", "success")
    return redirect(url_for("penjualan.daftar"))


@bp.route("/menu/<int:mid>/toggle", methods=["POST"])
@login_required
@pemilik_only
def toggle(mid):
    m = Menu.query.get_or_404(mid)
    m.aktif = not m.aktif
    db.session.commit()
    flash(f"Menu '{m.nama}' {'diaktifkan' if m.aktif else 'dinonaktifkan'}.", "info")
    return redirect(url_for("penjualan.daftar"))
