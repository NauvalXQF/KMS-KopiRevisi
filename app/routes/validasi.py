from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import Pengetahuan
from app.routes.helpers import get_current_user, kirim_notifikasi, login_required, pemilik_only

bp = Blueprint("validasi", __name__)


@bp.route("/validasi")
@login_required
@pemilik_only
def antrean():
    items = Pengetahuan.query.filter(
        Pengetahuan.status.in_(["menunggu_validasi", "revisi"])
    ).order_by(Pengetahuan.updated_at.desc()).all()
    return render_template("validasi.html", items=items)


@bp.route("/validasi/<int:pid>/setujui", methods=["POST"])
@login_required
@pemilik_only
def setujui(pid):
    p = Pengetahuan.query.get_or_404(pid)
    user = get_current_user()
    p.status = "terbit"
    p.validator_id = user.id
    p.catatan_validasi = None
    db.session.commit()
    if p.penulis_id:
        kirim_notifikasi(p.penulis_id, "Pengetahuan disetujui 🎉",
                         f"'{p.judul}' sudah terbit.",
                         terkait_tipe="pengetahuan", terkait_id=p.id)
    flash("Pengetahuan diterbitkan.", "success")
    return redirect(url_for("validasi.antrean"))


@bp.route("/validasi/<int:pid>/revisi", methods=["POST"])
@login_required
@pemilik_only
def revisi(pid):
    p = Pengetahuan.query.get_or_404(pid)
    user = get_current_user()
    catatan = request.form.get("catatan", "").strip()
    if not catatan:
        flash("Catatan revisi wajib diisi.", "danger")
        return redirect(url_for("validasi.antrean"))
    p.status = "revisi"
    p.validator_id = user.id
    p.catatan_validasi = catatan
    db.session.commit()
    if p.penulis_id:
        kirim_notifikasi(p.penulis_id, "Pengetahuan perlu revisi",
                         f"'{p.judul}': {catatan}",
                         terkait_tipe="pengetahuan", terkait_id=p.id)
    flash("Dikembalikan untuk revisi.", "info")
    return redirect(url_for("validasi.antrean"))
