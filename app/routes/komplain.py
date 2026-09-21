from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Komplain
from app.routes.helpers import get_current_user, login_required

bp = Blueprint("komplain", __name__)


@bp.route("/komplain")
@login_required
def daftar():
    items = Komplain.query.order_by(Komplain.tanggal.desc()).all()
    return render_template("komplain.html", items=items)


@bp.route("/komplain/tambah", methods=["POST"])
@login_required
def tambah():
    jenis = request.form.get("jenis", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()
    if not jenis or not deskripsi:
        flash("Jenis dan deskripsi wajib diisi.", "danger")
        return redirect(url_for("komplain.daftar"))
    user = get_current_user()
    db.session.add(Komplain(jenis=jenis, deskripsi=deskripsi,
                            solusi=request.form.get("solusi", "").strip() or None,
                            tindak_lanjut=request.form.get("tindak_lanjut", "").strip() or None,
                            status="baru", dicatat_oleh=user.id))
    db.session.commit()
    flash("Komplain dicatat.", "success")
    return redirect(url_for("komplain.daftar"))


@bp.route("/komplain/<int:kid>/update", methods=["POST"])
@login_required
def update(kid):
    k = Komplain.query.get_or_404(kid)
    k.solusi = request.form.get("solusi", "").strip() or k.solusi
    k.tindak_lanjut = request.form.get("tindak_lanjut", "").strip() or k.tindak_lanjut
    status = request.form.get("status", k.status)
    if status in ("baru", "diproses", "selesai"):
        k.status = status
    db.session.commit()
    flash("Komplain diperbarui.", "success")
    return redirect(url_for("komplain.daftar"))
