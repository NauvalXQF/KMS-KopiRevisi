from flask import Blueprint, flash, redirect, render_template, url_for

from app import db
from app.models import Notifikasi
from app.routes.helpers import get_current_user, login_required

bp = Blueprint("notifikasi", __name__)


@bp.route("/notifikasi")
@login_required
def daftar():
    user = get_current_user()
    items = Notifikasi.query.filter_by(pengguna_id=user.id).order_by(Notifikasi.created_at.desc()).limit(50).all()
    return render_template("notifikasi.html", items=items)


@bp.route("/notifikasi/<int:nid>/baca", methods=["POST"])
@login_required
def baca(nid):
    user = get_current_user()
    n = Notifikasi.query.filter_by(id=nid, pengguna_id=user.id).first_or_404()
    n.dibaca = True
    db.session.commit()
    return redirect(url_for("notifikasi.daftar"))


@bp.route("/notifikasi/baca-semua", methods=["POST"])
@login_required
def baca_semua():
    user = get_current_user()
    Notifikasi.query.filter_by(pengguna_id=user.id, dibaca=False).update({"dibaca": True})
    db.session.commit()
    flash("Semua notifikasi ditandai dibaca.", "info")
    return redirect(url_for("notifikasi.daftar"))
